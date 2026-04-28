import pygame, sys, time
from racer import (PlayerCar, EnemyCar, Obstacle, Coin, PowerUp,
                   NitroStrip, RoadLine, spawn_lines, draw_road,
                   draw_hud, init_fonts as racer_fonts)
from ui import (main_menu, ask_username, game_over_screen,
                leaderboard_screen, settings_screen)
from persistence import (load_leaderboard, add_score,
                          load_settings, save_settings)

pygame.init()
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer")
clock = pygame.time.Clock()
FPS = 60


def run_game(username, settings):
    racer_fonts()
    diff = settings.get("difficulty","normal")
    diff_map = {"easy":0.7,"normal":1.0,"hard":1.4}
    dmul = diff_map.get(diff, 1.0)

    car_color = tuple(settings.get("car_color",[50,100,220]))
    player = PlayerCar(car_color)
    enemies, coins, obstacles, powerups, nitros = [], [], [], [], []
    road_lines = spawn_lines(HEIGHT)

    score = 0; coin_count = 0; distance = 0
    enemy_speed = int(5*dmul)
    enemy_timer = coin_timer = obs_timer = pu_timer = nitro_timer = 0
    active_powerup = None; powerup_end = 0
    game_over = False

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        if not game_over:
            keys = pygame.key.get_pressed()
            player.move(keys, HEIGHT)
            score += 1; distance = score // 60

            if score % int(300/dmul) == 0:
                enemy_speed = min(enemy_speed+1, int(18*dmul))

            enemy_timer += 1
            spawn_rate = max(40, 90 - score//200)
            if enemy_timer >= spawn_rate:
                enemies.append(EnemyCar(enemy_speed))
                enemy_timer = 0

            coin_timer += 1
            if coin_timer >= 100:
                coins.append(Coin(enemy_speed-1))
                coin_timer = 0

            obs_timer += 1
            if obs_timer >= max(120, 200-score//100):
                obstacles.append(Obstacle(enemy_speed))
                obs_timer = 0

            pu_timer += 1
            if pu_timer >= 300 and not powerups:
                powerups.append(PowerUp(enemy_speed-2))
                pu_timer = 0

            nitro_timer += 1
            if nitro_timer >= 400:
                nitros.append(NitroStrip())
                nitro_timer = 0

            for line in road_lines: line.update(HEIGHT)

            for e in enemies[:]:
                e.update()
                if e.is_off_screen(HEIGHT): enemies.remove(e)
                elif player.get_rect().colliderect(e.get_rect()):
                    if player.shield:
                        player.shield = False
                        enemies.remove(e)
                    else:
                        game_over = True

            for o in obstacles[:]:
                o.update()
                if o.is_off_screen(HEIGHT): obstacles.remove(o)
                elif player.get_rect().colliderect(o.get_rect()):
                    if player.shield:
                        player.shield = False
                        obstacles.remove(o)
                    else:
                        game_over = True

            for c in coins[:]:
                c.update()
                if c.is_off_screen(HEIGHT): coins.remove(c)
                elif player.get_rect().colliderect(c.get_rect()):
                    coin_count += 1
                    score += c.value * 10
                    coins.remove(c)

            for p in powerups[:]:
                p.update()
                if p.is_off_screen(HEIGHT): powerups.remove(p)
                elif player.get_rect().colliderect(p.get_rect()):
                    if p.kind == "nitro":
                        player.activate_nitro()
                        active_powerup = "nitro"
                        powerup_end = time.time()+4
                    elif p.kind == "shield":
                        player.shield = True
                        active_powerup = "shield"
                        powerup_end = time.time()+999
                    elif p.kind == "repair":
                        score += 200
                        active_powerup = None
                    powerups.remove(p)

            for n in nitros[:]:
                n.update()
                if n.is_off_screen(HEIGHT): nitros.remove(n)
                elif player.get_rect().colliderect(n.get_rect()):
                    player.activate_nitro(3)
                    active_powerup = "nitro"
                    powerup_end = time.time()+3
                    nitros.remove(n)

            if active_powerup == "nitro" and time.time() > powerup_end:
                active_powerup = None

        screen.fill((30,30,30))
        draw_road(screen, WIDTH, HEIGHT)
        for line in road_lines: line.draw(screen)
        for e in enemies: e.draw(screen)
        for o in obstacles: o.draw(screen)
        for c in coins: c.draw(screen)
        for p in powerups: p.draw(screen)
        for n in nitros: n.draw(screen)
        player.draw(screen)
        draw_hud(screen, score, coin_count, distance, enemy_speed,
                 player, active_powerup, powerup_end)
        pygame.display.flip()

        if game_over:
            add_score(username, score, distance, coin_count)
            result = game_over_screen(screen, WIDTH, HEIGHT, score, distance, coin_count)
            return result


def main():
    settings = load_settings()
    while True:
        choice = main_menu(screen, WIDTH, HEIGHT)
        if choice == "quit":
            save_settings(settings)
            pygame.quit(); sys.exit()
        elif choice == "leaderboard":
            leaderboard_screen(screen, WIDTH, HEIGHT, load_leaderboard())
        elif choice == "settings":
            settings = settings_screen(screen, WIDTH, HEIGHT, settings)
            save_settings(settings)
        elif choice == "play":
            username = ask_username(screen, WIDTH, HEIGHT)
            while True:
                result = run_game(username, settings)
                if result == "menu":
                    break


if __name__ == "__main__":
    main()
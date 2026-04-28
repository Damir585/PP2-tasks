import pygame

WHITE     = (255,255,255)
BLACK     = (0,0,0)
YELLOW    = (255,220,0)
DARK      = (30,30,30)
HIGHLIGHT = (100,149,237)
GRAY      = (80,80,80)

font_large  = None
font_medium = None
font_small  = None

def init_fonts():
    global font_large, font_medium, font_small
    font_large  = pygame.font.SysFont("Arial", 52, bold=True)
    font_medium = pygame.font.SysFont("Arial", 34)
    font_small  = pygame.font.SysFont("Arial", 22)

def draw_button(surface, text, rect, active=False):
    color = HIGHLIGHT if active else GRAY
    pygame.draw.rect(surface, color, rect, border_radius=8)
    pygame.draw.rect(surface, WHITE, rect, 2, border_radius=8)
    lbl = font_medium.render(text, True, WHITE)
    surface.blit(lbl, (rect.centerx - lbl.get_width()//2,
                        rect.centery - lbl.get_height()//2))

def draw_overlay(surface, width, height):
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0,0,0,180))
    surface.blit(overlay, (0,0))

def main_menu(screen, width, height):
    init_fonts()
    buttons = {
        "play":        pygame.Rect(width//2-120, 260, 240, 55),
        "leaderboard": pygame.Rect(width//2-120, 330, 240, 55),
        "settings":    pygame.Rect(width//2-120, 400, 240, 55),
        "quit":        pygame.Rect(width//2-120, 470, 240, 55),
    }
    while True:
        screen.fill(DARK)
        title = font_large.render("RACER", True, YELLOW)
        screen.blit(title, (width//2 - title.get_width()//2, 150))
        mx, my = pygame.mouse.get_pos()
        for key, rect in buttons.items():
            draw_button(screen, key.capitalize(), rect, rect.collidepoint(mx,my))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return key

def ask_username(screen, width, height):
    init_fonts()
    name = ""
    while True:
        screen.fill(DARK)
        title = font_medium.render("Enter your name:", True, YELLOW)
        screen.blit(title, (width//2 - title.get_width()//2, 260))
        box = pygame.Rect(width//2-150, 320, 300, 50)
        pygame.draw.rect(screen, GRAY, box, border_radius=6)
        pygame.draw.rect(screen, WHITE, box, 2, border_radius=6)
        txt = font_medium.render(name + "|", True, WHITE)
        screen.blit(txt, (box.x+10, box.y+8))
        hint = font_small.render("Press ENTER to start", True, GRAY)
        screen.blit(hint, (width//2 - hint.get_width()//2, 390))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.unicode and len(name) < 16:
                    name += event.unicode

def game_over_screen(screen, width, height, score, distance, coins):
    init_fonts()
    buttons = {
        "retry": pygame.Rect(width//2-130, 420, 120, 50),
        "menu":  pygame.Rect(width//2+10,  420, 120, 50),
    }
    while True:
        screen.fill(DARK)
        draw_overlay(screen, width, height)
        t = font_large.render("GAME OVER", True, YELLOW)
        screen.blit(t, (width//2 - t.get_width()//2, 200))
        for i, line in enumerate([
            f"Score: {score}",
            f"Distance: {distance}m",
            f"Coins: {coins}"
        ]):
            s = font_medium.render(line, True, WHITE)
            screen.blit(s, (width//2 - s.get_width()//2, 290+i*40))
        mx, my = pygame.mouse.get_pos()
        for key, rect in buttons.items():
            draw_button(screen, key.capitalize(), rect, rect.collidepoint(mx,my))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        return key

def leaderboard_screen(screen, width, height, lb):
    init_fonts()
    back = pygame.Rect(width//2-80, height-80, 160, 45)
    while True:
        screen.fill(DARK)
        title = font_large.render("TOP 10", True, YELLOW)
        screen.blit(title, (width//2 - title.get_width()//2, 30))
        for i, entry in enumerate(lb[:10]):
            line = f"{i+1}. {entry['name']}  {entry['score']}pts  {entry['distance']}m  {entry['coins']} coins"
            s = font_small.render(line, True, WHITE)
            screen.blit(s, (width//2 - s.get_width()//2, 110+i*38))
        mx, my = pygame.mouse.get_pos()
        draw_button(screen, "Back", back, back.collidepoint(mx,my))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.collidepoint(event.pos):
                    return

def settings_screen(screen, width, height, settings):
    init_fonts()
    back = pygame.Rect(width//2-80, height-80, 160, 45)
    colors = {"Blue":[50,100,220], "Red":[220,50,50], "Green":[50,200,50], "Yellow":[220,200,0]}
    diffs  = ["easy","normal","hard"]
    while True:
        screen.fill(DARK)
        title = font_large.render("SETTINGS", True, YELLOW)
        screen.blit(title, (width//2-title.get_width()//2, 40))

        # Sound toggle
        sr = pygame.Rect(width//2-100, 140, 200, 45)
        draw_button(screen, f"Sound: {'ON' if settings['sound'] else 'OFF'}", sr)

        # Car color
        cy_label = font_small.render("Car color:", True, WHITE)
        screen.blit(cy_label, (width//2-150, 210))
        for i, (cname, cval) in enumerate(colors.items()):
            r = pygame.Rect(width//2-150+i*80, 235, 70, 35)
            active = settings["car_color"] == cval
            pygame.draw.rect(screen, tuple(cval), r, border_radius=5)
            if active:
                pygame.draw.rect(screen, WHITE, r, 3, border_radius=5)

        # Difficulty
        dl = font_small.render("Difficulty:", True, WHITE)
        screen.blit(dl, (width//2-150, 290))
        for i, d in enumerate(diffs):
            r = pygame.Rect(width//2-150+i*110, 315, 100, 35)
            draw_button(screen, d.capitalize(), r, settings["difficulty"]==d)

        mx, my = pygame.mouse.get_pos()
        draw_button(screen, "Back", back, back.collidepoint(mx,my))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); import sys; sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if sr.collidepoint(event.pos):
                    settings["sound"] = not settings["sound"]
                for cname, cval in colors.items():
                    i = list(colors.keys()).index(cname)
                    r = pygame.Rect(width//2-150+i*80, 235, 70, 35)
                    if r.collidepoint(event.pos):
                        settings["car_color"] = cval
                for i, d in enumerate(diffs):
                    r = pygame.Rect(width//2-150+i*110, 315, 100, 35)
                    if r.collidepoint(event.pos):
                        settings["difficulty"] = d
                if back.collidepoint(event.pos):
                    return settings
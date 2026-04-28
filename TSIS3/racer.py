import pygame, random, time

WHITE     = (255,255,255)
BLACK     = (0,0,0)
GRAY      = (50,50,50)
DARK_GRAY = (30,30,30)
YELLOW    = (255,220,0)
GOLD      = (255,180,0)
SILVER    = (200,200,200)
BRONZE    = (180,100,30)
RED       = (220,50,50)
GREEN     = (50,200,50)
ORANGE    = (255,165,0)
PURPLE    = (180,0,200)
CYAN      = (0,220,220)

ROAD_LEFT  = 100
ROAD_RIGHT = 500
LANE_WIDTH = (ROAD_RIGHT - ROAD_LEFT) // 3

COIN_TYPES = [
    {"value":1,"color":BRONZE,"shine":(210,140,60),"radius":12,"weight":60},
    {"value":3,"color":SILVER,"shine":(230,230,230),"radius":14,"weight":30},
    {"value":5,"color":GOLD,  "shine":(255,220,100),"radius":16,"weight":10},
]

POWERUP_TYPES = ["nitro","shield","repair"]
POWERUP_COLORS = {"nitro":ORANGE,"shield":CYAN,"repair":GREEN}

font_small  = None
font_medium = None

def init_fonts():
    global font_small, font_medium
    font_small  = pygame.font.SysFont("Arial", 22)
    font_medium = pygame.font.SysFont("Arial", 32)

class PlayerCar:
    def __init__(self, color):
        self.width  = 50
        self.height = 90
        self.x = 275
        self.y = 650
        self.base_speed = 6
        self.speed = 6
        self.color = color
        self.shield = False
        self.nitro_end = 0
        self.nitro_active = False

    def draw(self, surface):
        col = self.color
        if self.shield:
            pygame.draw.circle(surface, CYAN,
                (self.x+self.width//2, self.y+self.height//2), 55, 3)
        pygame.draw.rect(surface, col,
            (self.x, self.y, self.width, self.height), border_radius=8)
        pygame.draw.rect(surface, (180,220,255),
            (self.x+8, self.y+10, self.width-16, 22), border_radius=4)
        for wx,wy in [(self.x-8,self.y+10),(self.x+self.width-4,self.y+10),
                      (self.x-8,self.y+self.height-30),(self.x+self.width-4,self.y+self.height-30)]:
            pygame.draw.rect(surface, BLACK, (wx,wy,12,20), border_radius=3)

    def move(self, keys, height):
        if keys[pygame.K_LEFT]  and self.x > ROAD_LEFT:        self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x+self.width < ROAD_RIGHT: self.x += self.speed
        if keys[pygame.K_UP]   and self.y > 0:                  self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y+self.height < height:  self.y += self.speed
        now = time.time()
        if self.nitro_active and now > self.nitro_end:
            self.speed = self.base_speed
            self.nitro_active = False

    def activate_nitro(self, duration=4):
        self.speed = self.base_speed * 2
        self.nitro_end = time.time() + duration
        self.nitro_active = True

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)


class EnemyCar:
    def __init__(self, speed):
        self.width  = 50
        self.height = 90
        lane = random.randint(0,2)
        self.x = ROAD_LEFT + lane*LANE_WIDTH + (LANE_WIDTH-self.width)//2
        self.y = -self.height
        self.speed = speed
        self.color = random.choice([RED,ORANGE,GREEN])

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
            (self.x,self.y,self.width,self.height), border_radius=8)
        pygame.draw.rect(surface, (180,220,180),
            (self.x+8,self.y+10,self.width-16,22), border_radius=4)
        for wx,wy in [(self.x-8,self.y+10),(self.x+self.width-4,self.y+10),
                      (self.x-8,self.y+self.height-30),(self.x+self.width-4,self.y+self.height-30)]:
            pygame.draw.rect(surface, BLACK, (wx,wy,12,20), border_radius=3)

    def update(self): self.y += self.speed
    def get_rect(self): return pygame.Rect(self.x+5,self.y+5,self.width-10,self.height-10)
    def is_off_screen(self, height): return self.y > height


class Obstacle:
    def __init__(self, speed):
        lane = random.randint(0,2)
        self.x = ROAD_LEFT + lane*LANE_WIDTH + 10
        self.y = -40
        self.w = LANE_WIDTH - 20
        self.h = 30
        self.speed = speed
        self.kind = random.choice(["oil","barrier","bump"])
        self.colors = {"oil":(30,30,30),"barrier":(220,50,50),"bump":(180,140,0)}

    def draw(self, surface):
        col = self.colors[self.kind]
        pygame.draw.rect(surface, col, (self.x,self.y,self.w,self.h), border_radius=5)
        lbl = font_small.render(self.kind.upper(), True, WHITE)
        surface.blit(lbl, (self.x+self.w//2-lbl.get_width()//2,
                            self.y+self.h//2-lbl.get_height()//2))

    def update(self): self.y += self.speed
    def get_rect(self): return pygame.Rect(self.x,self.y,self.w,self.h)
    def is_off_screen(self, height): return self.y > height


class Coin:
    def __init__(self, speed):
        pop = [ct for ct in COIN_TYPES for _ in range(ct["weight"])]
        ct = random.choice(pop)
        self.radius = ct["radius"]
        self.value  = ct["value"]
        self.color  = ct["color"]
        self.shine  = ct["shine"]
        lane = random.randint(0,2)
        self.x = ROAD_LEFT + lane*LANE_WIDTH + LANE_WIDTH//2
        self.y = -self.radius
        self.speed = speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x,self.y), self.radius)
        pygame.draw.circle(surface, BLACK, (self.x,self.y), self.radius, 2)
        pygame.draw.circle(surface, self.shine, (self.x-4,self.y-4), 4)

    def update(self): self.y += self.speed
    def get_rect(self): return pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
    def is_off_screen(self, height): return self.y > height


class PowerUp:
    def __init__(self, speed):
        self.kind = random.choice(POWERUP_TYPES)
        self.color = POWERUP_COLORS[self.kind]
        lane = random.randint(0,2)
        self.x = ROAD_LEFT + lane*LANE_WIDTH + LANE_WIDTH//2
        self.y = -20
        self.radius = 18
        self.speed = speed
        self.spawn_time = time.time()
        self.timeout = 8

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x,self.y), self.radius)
        pygame.draw.circle(surface, WHITE, (self.x,self.y), self.radius, 2)
        lbl = font_small.render(self.kind[0].upper(), True, WHITE)
        surface.blit(lbl, (self.x-lbl.get_width()//2, self.y-lbl.get_height()//2))

    def update(self): self.y += self.speed
    def get_rect(self): return pygame.Rect(self.x-self.radius,self.y-self.radius,self.radius*2,self.radius*2)
    def is_off_screen(self, height): return self.y > height or time.time()-self.spawn_time > self.timeout


class NitroStrip:
    def __init__(self):
        lane = random.randint(0,2)
        self.x = ROAD_LEFT + lane*LANE_WIDTH + 5
        self.y = -20
        self.w = LANE_WIDTH - 10
        self.h = 20
        self.speed = 7
        self.color = (255,200,0)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x,self.y,self.w,self.h), border_radius=3)
        lbl = font_small.render("NITRO", True, BLACK)
        surface.blit(lbl, (self.x+self.w//2-lbl.get_width()//2, self.y+self.h//2-lbl.get_height()//2))

    def update(self): self.y += self.speed
    def get_rect(self): return pygame.Rect(self.x,self.y,self.w,self.h)
    def is_off_screen(self, height): return self.y > height


class RoadLine:
    def __init__(self, x, y):
        self.x = x; self.y = y
        self.width = 10; self.height = 50; self.speed = 8

    def update(self, height):
        self.y += self.speed
        if self.y > height: self.y = -self.height

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x-self.width//2,self.y,self.width,self.height))


def spawn_lines(height):
    lines = []
    for lane in range(1,3):
        x = ROAD_LEFT + lane*LANE_WIDTH
        for row in range(6):
            lines.append(RoadLine(x, row*(height//5)))
    return lines


def draw_road(surface, width, height):
    pygame.draw.rect(surface, GRAY, (ROAD_LEFT,0,ROAD_RIGHT-ROAD_LEFT,height))
    pygame.draw.rect(surface, YELLOW, (ROAD_LEFT,0,6,height))
    pygame.draw.rect(surface, YELLOW, (ROAD_RIGHT-6,0,6,height))


def draw_hud(surface, score, coins, distance, enemy_speed, player, active_powerup, powerup_end):
    font_small.render("", True, WHITE)
    items = [
        f"Score: {score}",
        f"Coins: {coins}",
        f"Dist: {distance}m",
        f"Speed: {enemy_speed}",
    ]
    for i, txt in enumerate(items):
        s = font_small.render(txt, True, WHITE)
        surface.blit(s, (10, 10+i*26))

    if active_powerup:
        remaining = max(0, int(powerup_end - time.time()))
        pw = font_small.render(f"[{active_powerup.upper()}] {remaining}s", True, POWERUP_COLORS.get(active_powerup, WHITE))
        surface.blit(pw, (10, 120))
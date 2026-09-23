import pygame
import random
import sys

# ============================================================
# MC GRYPS RUNNER
# ============================================================

pygame.init()

# ------------------------------------------------------------
# USTAWIENIA
# ------------------------------------------------------------

WIDTH = 1280
HEIGHT = 720

FPS = 60

GROUND_Y = 570

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MC Gryps Runner")

clock = pygame.time.Clock()

# ------------------------------------------------------------
# KOLORY
# ------------------------------------------------------------

BLACK = (20, 20, 20)
WHITE = (255, 255, 255)

GRAY = (80, 80, 80)
DARK_GRAY = (40, 40, 40)

GREEN = (40, 180, 80)
RED = (200, 50, 50)
BLUE = (50, 100, 220)
YELLOW = (240, 200, 40)
ORANGE = (240, 130, 40)

# ------------------------------------------------------------
# CZCIONKI
# ------------------------------------------------------------

font_big = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 42)
font_small = pygame.font.Font(None, 30)

# ============================================================
# POSTACIE
# ============================================================

CHARACTERS = {
    "BIG OZI": {
        "color": (200, 70, 70),
        "speed": 1.0,
        "jump": 1.0,
        "health": 4
    },

    "LIL specjal": {
        "color": (70, 120, 220),
        "speed": 1.20,
        "jump": 0.95,
        "health": 2
    },

    "Wika the psycho": {
        "color": (180, 70, 200),
        "speed": 0.95,
        "jump": 1.20,
        "health": 3
    }
}


# ============================================================
# FUNKCJA TEKSTU
# ============================================================

def draw_text(text, font, color, x, y, center=False):

    surface = font.render(text, True, color)

    if center:
        rect = surface.get_rect(center=(x, y))
    else:
        rect = surface.get_rect(topleft=(x, y))

    screen.blit(surface, rect)


# ============================================================
# GRACZ
# ============================================================

class Player:

    def __init__(self, name):

        self.name = name

        # ----------------------------------------------------
        # ANIMACJA
        # ----------------------------------------------------

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.20

        # ----------------------------------------------------
        # GRAFIKA POSTACI
        # ----------------------------------------------------

        if name == "BIG OZI":
            self.width = 160
            self.height = 200
            self.run_frames = [

                pygame.transform.scale(
                    pygame.image.load("assets/characters/big_ozi/run_1.png").convert_alpha(),
                    (160, 200)
                ),

                pygame.transform.scale(
                    pygame.image.load("assets/characters/big_ozi/run_2.png").convert_alpha(),
                    (160, 200)
                ),

                pygame.transform.scale(
                    pygame.image.load("assets/characters/big_ozi/run_3.png").convert_alpha(),
                    (160, 200)
                ),

                pygame.transform.scale(
                    pygame.image.load("assets/characters/big_ozi/run_4.png").convert_alpha(),
                    (160, 200)
                ),

            ]

            self.jump_image = pygame.transform.scale(
                pygame.image.load("assets/characters/big_ozi/jump.png").convert_alpha(),
                (160, 200)
            )

        else:

            self.run_frames = []
            self.jump_image = None

        # ----------------------------------------------------
        # DANE POSTACI
        # ----------------------------------------------------

        data = CHARACTERS[name]

        self.color = data["color"]

        self.speed_multiplier = data["speed"]

        self.jump_multiplier = data["jump"]

        self.max_health = data["health"]
        self.health = self.max_health

        # ----------------------------------------------------
        # HITBOX
        # ----------------------------------------------------

        self.width = 60
        self.height = 90

        self.x = 200

        self.y = GROUND_Y - self.height

        # ----------------------------------------------------
        # FIZYKA
        # ----------------------------------------------------

        self.velocity_y = 0

        self.gravity = 1800

        self.jump_power = -700 * self.jump_multiplier

        self.on_ground = True

        # ----------------------------------------------------
        # COLLISION RECT
        # ----------------------------------------------------

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    # ========================================================
    # SKOK
    # ========================================================

    def take_damage(self):

        self.health -= 1

        if self.health <= 0:

            self.health = 0

            return True

        return False

    def jump(self):

        if self.on_ground:

            self.velocity_y = self.jump_power

            self.on_ground = False

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, dt):

    # GRAWITACJA
        self.velocity_y += self.gravity * dt

        self.y += self.velocity_y * dt

    # ZIEMIA
        if self.y >= GROUND_Y - self.height:

            self.y = GROUND_Y - self.height

            self.velocity_y = 0

            self.on_ground = True

    # ANIMACJA BIEGU
        if self.on_ground and self.run_frames:

            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:

                self.animation_timer = 0

                self.current_frame += 1

                if self.current_frame >= len(self.run_frames):

                    self.current_frame = 0

    # HITBOX
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)   
    # ========================================================
    # RYSOWANIE
    # ========================================================

    def draw(self):

        # ----------------------------------------------------
        # SKOK
        # ----------------------------------------------------

        if not self.on_ground and self.jump_image:

            image = self.jump_image

        # ----------------------------------------------------
        # BIEG
        # ----------------------------------------------------

        elif self.run_frames:

            image = self.run_frames[
                self.current_frame
            ]

        # ----------------------------------------------------
        # BRAK GRAFIKI
        # ----------------------------------------------------

        else:

            pygame.draw.rect(
                screen,
                self.color,
                self.rect
            )

            return

        # ----------------------------------------------------
        # RYSOWANIE SPRITE'A
        # ----------------------------------------------------

        screen.blit(
            image,
            (
                self.rect.centerx - image.get_width() // 2,
                self.rect.bottom - image.get_height()
            )
        )

# ============================================================
# PRZESZKODA
# ============================================================

class Obstacle:

    TYPES = [
        "trash",
        "brick",
        "barrier"
    ]

    def __init__(self, x):

        self.type = random.choice(self.TYPES)

        if self.type == "trash":

            self.width = 55
            self.height = 75

        elif self.type == "brick":

            self.width = 70
            self.height = 35

        else:

            self.width = 100
            self.height = 65

        self.x = x
        self.y = GROUND_Y - self.height

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def update(self, dt, speed):

        self.x -= speed * dt

        self.rect.x = int(self.x)

    def draw(self):

        if self.type == "trash":

            pygame.draw.rect(
                screen,
                (100, 100, 100),
                self.rect
            )

        elif self.type == "brick":

            pygame.draw.rect(
                screen,
                (170, 70, 50),
                self.rect
            )

        else:

            pygame.draw.rect(
                screen,
                (220, 180, 40),
                self.rect
            )
    
    def off_screen(self):

        return self.rect.right < 0
# ============================================================
# ZBIERACZKA
# ============================================================

class Collectible:

    TYPES = [
        "money",
        "energy",
        "package"
    ]

    def __init__(self, x):

        self.type = random.choice(self.TYPES)

        self.size = 30

        self.x = x

        # czasami wyżej, żeby trzeba było skoczyć

        if random.random() < 0.35:

            self.y = GROUND_Y - random.randint(
                100,
                180
            )

        else:

            self.y = GROUND_Y - 45

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.size,
            self.size
        )

    def update(self, speed, dt):

        self.x -= speed * dt

        self.rect.x = int(self.x)

    def draw(self):

        if self.type == "money":

            pygame.draw.rect(
                screen,
                GREEN,
                self.rect
            )

            draw_text(
                "$",
                font_small,
                BLACK,
                self.rect.centerx,
                self.rect.centery,
                center=True
            )

        elif self.type == "energy":

            pygame.draw.rect(
                screen,
                YELLOW,
                self.rect
            )

            pygame.draw.polygon(
                screen,
                BLACK,
                [
                    (
                        self.rect.centerx + 4,
                        self.rect.top + 5
                    ),
                    (
                        self.rect.centerx - 4,
                        self.rect.centery
                    ),
                    (
                        self.rect.centerx + 2,
                        self.rect.centery
                    ),
                    (
                        self.rect.centerx - 5,
                        self.rect.bottom - 5
                    )
                ]
            )

        else:

            pygame.draw.rect(
                screen,
                ORANGE,
                self.rect
            )

            pygame.draw.rect(
                screen,
                WHITE,
                (
                    self.rect.x + 5,
                    self.rect.y + 5,
                    20,
                    20
                ),
                2
            )

    def off_screen(self):

        return self.rect.right < 0


# ============================================================
# POLICJA
# ============================================================

class PoliceCar:

    def __init__(self):

        # =========================
        # KLATKI ANIMACJI
        # =========================

        CAR_WIDTH = 300
        CAR_HEIGHT = 300

        self.frames = [
            pygame.image.load(
                "assets/police/police_car_1.png"
            ).convert_alpha(),

            pygame.image.load(
                "assets/police/police_car_2.png"
            ).convert_alpha(),

            pygame.image.load(
                "assets/police/police_car_3.png"
            ).convert_alpha(),

            pygame.image.load(
                "assets/police/police_car_4.png"
            ).convert_alpha(),

        ]

        self.frames = [
            pygame.transform.scale(
                frame,
                (CAR_WIDTH, CAR_HEIGHT)
            )
            for frame in self.frames
        ]

        # =========================
        # ANIMACJA
        # =========================

        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 0.10

        self.image = self.frames[
            self.frame_index
        ]

        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT

        # =========================
        # POZYCJA
        # =========================

        self.x = -self.width
        self.y = GROUND_Y - self.height

        self.rect = pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

        # =========================
        # ULT
        # =========================

        self.active = False

        # Prędkość podczas używania ulta
        self.ult_speed = 500

        # Cooldown
        self.cooldown = 5.0
        self.cooldown_timer = 0

    # ========================================================
    # WEZWANIE ULTA
    # ========================================================

    def activate(self):

        # Nie można aktywować podczas działania
        if self.active:
            return

        # Nie można aktywować podczas cooldownu
        if self.cooldown_timer > 0:
            return

        self.active = True

        # Start poza ekranem
        self.x = -self.width

        self.rect.x = int(self.x)

    # ========================================================
    # UPDATE
    # ========================================================

    def update(self, speed, dt):

        # =========================
        # COOLDOWN
        # =========================

        if self.cooldown_timer > 0:

            self.cooldown_timer -= dt

            if self.cooldown_timer < 0:
                self.cooldown_timer = 0

        # Jeżeli ult nie jest aktywny,
        # radiowóz nic nie robi
        if not self.active:
            return

        # =========================
        # ANIMACJA
        # =========================

        self.frame_timer += dt

        if self.frame_timer >= self.frame_speed:

            self.frame_timer = 0

            self.frame_index += 1

            if self.frame_index >= len(self.frames):
                self.frame_index = 0

            self.image = self.frames[
                self.frame_index
            ]

        # =========================
        # RUCH ULTA
        # =========================

        self.x += self.ult_speed * dt

        self.rect.x = int(self.x)

        # =========================
        # KONIEC ULTA
        # =========================

        if self.x > WIDTH:

            self.active = False

            self.cooldown_timer = self.cooldown

            self.x = -self.width

            self.rect.x = int(self.x)

    # ========================================================
    # DRAW
    # ========================================================

    def draw(self):

        # Nie rysujemy go, jeśli ult nie jest aktywny
        if not self.active:
            return

        screen.blit(
            self.image,
            (
                int(self.x),
                int(self.y)
            )
        )


  # ============================================================
# EKRANY PORAŻKI I ZWYCIĘSTWA
# ============================================================

GAME_OVER_IMAGES = {
    "BIG OZI": pygame.image.load(
        "assets/game_over/big_ozi.png"
    ).convert(),
}

VICTORY_IMAGES = {
    "BIG OZI": pygame.image.load(
        "assets/victory/big_ozi.png"
    ).convert(),
}
# ============================================================
# TŁO
# ============================================================

background_image = pygame.image.load(
    "assets/backgrounds/background.png"
).convert()

ground_image = pygame.image.load(
    "assets/backgrounds/ground.png"
).convert_alpha()

background_x = 0
ground_x = 0


def draw_background(speed, dt):

    global background_x
    global ground_x

    # --------------------------------------------------------
    # PRĘDKOŚĆ TŁA
    # --------------------------------------------------------

    background_x -= speed * 0.15 * dt
    ground_x -= speed * dt

    # --------------------------------------------------------
    # RESET POZYCJI
    # --------------------------------------------------------

    if background_x <= -WIDTH:
        background_x = 0

    if ground_x <= -WIDTH:
        ground_x = 0

    # --------------------------------------------------------
    # TŁO
    # --------------------------------------------------------

    screen.blit(
        background_image,
        (int(background_x), 0)
    )

    screen.blit(
        background_image,
        (int(background_x + WIDTH), 0)
    )

    # --------------------------------------------------------
    # DROGA / ZIEMIA
    # --------------------------------------------------------

    screen.blit(
        ground_image,
        (int(ground_x), GROUND_Y)
    )

    screen.blit(
        ground_image,
        (int(ground_x + WIDTH), GROUND_Y)
    )
# ============================================================
# EKRAN WYBORU POSTACI
# ============================================================

def character_selection():

    selected = 0

    names = list(CHARACTERS.keys())

    while True:

        screen.fill(BLACK)

        draw_text(
            "MC GRYPS RUNNER",
            font_big,
            WHITE,
            WIDTH // 2,
            100,
            center=True
        )

        draw_text(
            "WYBIERZ POSTAĆ",
            font_medium,
            WHITE,
            WIDTH // 2,
            170,
            center=True
        )

        for i, name in enumerate(names):

            x = WIDTH // 2

            y = 280 + i * 100

            color = (
                CHARACTERS[name]["color"]
            )

            if i == selected:

                pygame.draw.rect(
                    screen,
                    WHITE,
                    (
                        x - 300,
                        y - 35,
                        600,
                        70
                    ),
                    3
                )

            draw_text(
                name,
                font_medium,
                color,
                x,
                y,
                center=True
            )

        draw_text(
            "STRZAŁKI GÓRA/DÓŁ - wybór",
            font_small,
            WHITE,
            WIDTH // 2,
            620,
            center=True
        )

        draw_text(
            "ENTER - start",
            font_small,
            WHITE,
            WIDTH // 2,
            655,
            center=True
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:

                    selected -= 1

                    if selected < 0:
                        selected = len(names) - 1

                if event.key == pygame.K_DOWN:

                    selected += 1

                    if selected >= len(names):
                        selected = 0

                if event.key == pygame.K_RETURN:

                    return names[selected]

        clock.tick(FPS)


# ============================================================
# GRA
# ============================================================

def draw_health(player):

    font = pygame.font.SysFont(
        "Arial",
        36
    )

    health_text = "♥" * player.health

    text = font.render(
        health_text,
        True,
        (255, 50, 50)
    )

    screen.blit(
        text,
        (180, 55)
    )

def game():

    selected_character = character_selection()

    player = Player(
        selected_character
    )

    obstacles = []

    collectibles = []

    police = PoliceCar()

    score = 0

    money = 0

    game_speed = 450

    spawn_timer = 0

    collectible_timer = 0

    difficulty_timer = 0

    running = True

    while running:

        dt = clock.tick(FPS) / 1000

        # ----------------------------------------------------
        # EVENTY
        # ----------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_SPACE,
                    pygame.K_UP
                ):

                    player.jump()

                if event.key == pygame.K_x:

                    police.activate()

                if event.key == pygame.K_ESCAPE:

                    return

        # ----------------------------------------------------
        # GRACZ
        # ----------------------------------------------------

        player.update(dt)

        # ----------------------------------------------------
        # SPAWN PRZESZKÓD
        # ----------------------------------------------------

        spawn_timer -= dt

        if spawn_timer <= 0:

            obstacle = Obstacle(
                WIDTH + 100
            )

            obstacles.append(
                obstacle
            )

            spawn_timer = random.uniform(
                0.9,
                1.7
            )

        # ----------------------------------------------------
        # SPAWN ZBIERAJEK
        # ----------------------------------------------------

        collectible_timer -= dt

        if collectible_timer <= 0:

            collectible = Collectible(
                WIDTH + 100
            )

            collectibles.append(
                collectible
            )

            collectible_timer = random.uniform(
                0.5,
                1.3
            )

        # ----------------------------------------------------
        # PRĘDKOŚĆ
        # ----------------------------------------------------

        difficulty_timer += dt

        if difficulty_timer >= 5:

            game_speed += 20

            difficulty_timer = 0

        # ----------------------------------------------------
        # PRZESZKODY
        # ----------------------------------------------------

        for obstacle in obstacles:

            obstacle.update(
                dt,
                game_speed
            )

            if player.rect.colliderect(
                obstacle.rect
            ):

             if player.take_damage():

                return game_over(
                    score,
                    money,
                    selected_character
                )
             else:
                obstacles.remove(obstacle)

        obstacles = [
            o for o in obstacles
            if not o.off_screen()
        ]

        # ----------------------------------------------------
        # ZBIERAJKI
        # ----------------------------------------------------

        for collectible in collectibles:

            collectible.update(
                game_speed,
                dt
            )

            if player.rect.colliderect(
                collectible.rect
            ):

                money += 1

                score += 100

                collectibles.remove(
                    collectible
                )

                break

        collectibles = [
            c for c in collectibles
            if not c.off_screen()
        ]

        # ----------------------------------------------------
        # POLICJA
        # ----------------------------------------------------

        police.update(
            game_speed,
            dt
        )

        if police.active:
            obstacles = [
                obstacle
                for obstacle in obstacles
                if not police.rect.colliderect(
                    obstacle.rect
                )
            ]
        # ----------------------------------------------------
        # SCORE
        # ----------------------------------------------------

        score += int(
            60 * dt
        )

        if score >= 100:
            return victory_screen(
              score,
              money,
              selected_character
            )
        # ----------------------------------------------------
        # RYSOWANIE
        # ----------------------------------------------------

        draw_background(
            game_speed,
            dt
        )

        for collectible in collectibles:

            collectible.draw()

        for obstacle in obstacles:

            obstacle.draw()

        police.draw()

        player.draw()

        draw_health(player)
        # ----------------------------------------------------
        # HUD
        # ----------------------------------------------------

        draw_text(
            f"Wynik: {score}",
            font_medium,
            WHITE,
            25,
            20
        )

        draw_text(
            f"Kasa: {money}",
            font_medium,
            YELLOW,
            25,
            65
        )

        draw_text(
            selected_character,
            font_small,
            WHITE,
            WIDTH - 250,
            25
        )

        draw_text(
            f"Prędkość: {int(game_speed)}",
            font_small,
            WHITE,
            WIDTH - 250,
            55
        )

        
        if police.active:
         
         draw_text(
             "JAZDA!!",
             font_small,
             RED,
             WIDTH - 250,
             85
        )

        elif police.cooldown_timer > 0:
             draw_text(
                f"Naprawianie fury: {police.cooldown_timer:.1f}s",
                font_small,
                WHITE,
                WIDTH - 250,
                85
             )

        else:
            draw_text(
                "X - JANO!",
                font_small,
                WHITE,
                WIDTH -250,
                85
            )

        pygame.display.flip()


# ============================================================
# GAME OVER
# ============================================================

def game_over(
    score,
    money,
    character
):

    while True:

        background = GAME_OVER_IMAGES.get(
            character
        )

        if background:
            screen.blit(
                background,
                (0, 0)
            )
        else:
            screen.fill(BLACK)
        

        draw_text(
            "ZŁAPALI CIĘ!",
            font_big,
            RED,
            WIDTH // 2,
            100,
            center=True
        )

        left_x = 190
        start_y = 450
        spacing = 45

        draw_text(
            f"Postać: {character}",
            font_medium,
            WHITE,
            left_x,
            start_y,
            center=True
        )

        draw_text(
            f"Wynik: {score}",
            font_medium,
            WHITE,
            left_x,
            start_y + spacing,
            center=True
        )

        draw_text(
            f"Zebrana kasa: {money}",
            font_medium,
            YELLOW,
            left_x,
            start_y + spacing * 2,
            center=True
        )

        draw_text(
            "ENTER - zagraj ponownie",
            font_small,
            WHITE,
            left_x,
            start_y + spacing * 3 + 20,
            center=True
        )

        draw_text(
            "ESC - menu",
            font_small,
            WHITE,
            left_x,
            start_y + spacing * 4 + 20,
            center=True
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:

                    game()

                    return

                if event.key == pygame.K_ESCAPE:

                    return

        clock.tick(FPS)

def victory_screen(
    score,
    money,
    character
):
    while True:
        background = VICTORY_IMAGES.get(character)

        if background:
            screen.blit(background, (0, 0))
        else:
            screen.fill(BLACK)

        draw_text(
            "ZWYCIĘSTWO!",
            font_big,
            YELLOW,
            WIDTH // 2,
            100,
            center=True
        )

        left_x = 190
        start_y = 450
        spacing = 45
        
        draw_text(
            f"Postać: {character}",
            font_medium,
            WHITE,
            left_x,
            start_y,
            center=True
        )

        draw_text(
            f"Wynik: {score}",
            font_medium,
            WHITE,
            left_x,
            start_y + spacing,
            center=True
        )

        draw_text(
            f"Zebrana kasa: {money}",
            font_medium,
            YELLOW,
            left_x,
            start_y + spacing * 2,
            center=True
        )

        draw_text(
            "ENTER - zagraj ponownie",
            font_small,
            WHITE,
            left_x,
            start_y + spacing * 3 + 20,
            center=True
        )

        draw_text(
            "ESC - menu",
            font_small,
            WHITE,
            left_x,
            start_y + spacing * 4 +20,
            center=True
        )

        pygame.display.flip()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RETURN:
                    game()
                    return

                if event.key == pygame.K_ESCAPE:
                    return
# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    game()
import pygame
import math
import sys
from settings import *
import random
from button import Button

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("C O W B O Y")
clock = pygame.time.Clock()

font_type = "fuente/Pixeltype.ttf"
font_size = 80
font_color = "Black"
menu_font = pygame.font.Font(font_type, font_size)
instructions_font = pygame.font.Font(font_type, 50)

ground = pygame.image.load("graficos/ground.png")
ground_width = 200
ground_height = 50

instructions = [
    "No dejes que nada toque al vaquero",
    "Movimiento: w  a  s  d",
    "Disparar: barra espaciadora",
    "1 diparo para las rodadoras",
    "3 disparos para los demonios",
    "Los demonios aparecen donde quieran"
]

text_instructions = [
    instructions_font.render(instruction, False, "#8c3918")
    for instruction in instructions
]

play_hint = menu_font.render("Podrias mirar INFO en menu", False, font_color)
pause = False


def play():

    class Player(pygame.sprite.Sprite):

        def __init__(self):
            super().__init__()
            self.image = pygame.transform.rotozoom(
                pygame.image.load("graficos/jugador/new_piskel.gif").convert_alpha(),
                0,
                PLAYER_SIZE,
            )
            self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
            self.rect = self.image.get_rect(center=self.pos)
            self.speed = PLAYER_SPEED
            self.shoot = False
            self.shoot_cooldown = 0
            self.last_move_direction = self.pos

        def user_input(self):
            self.velocity_x = 0
            self.velocity_y = 0

            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                self.velocity_y = -self.speed
            if keys[pygame.K_s]:
                self.velocity_y = self.speed
            if keys[pygame.K_d]:
                self.velocity_x = self.speed
            if keys[pygame.K_a]:
                self.velocity_x = -self.speed

            # To avoid more speed when player moves diagonally
            if self.velocity_x != 0 and self.velocity_y != 0:
                self.velocity_x /= math.sqrt(2)
                self.velocity_y /= math.sqrt(2)

            # To avoid static bullets when still
            if self.velocity_x != 0 or self.velocity_y != 0:
                self.last_move_direction = pygame.math.Vector2(
                    self.velocity_x, self.velocity_y
                )

            if keys[pygame.K_SPACE]:
                self.shoot = True
                self.shooting()
            else:
                self.shoots = False

        def move(self):
            self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)
            self.rect.center = self.pos  # Actualiza la posición del rectángulo

        def shooting(self):
            # Bullet same direction as player but more speed
            # Coodl down to shoot to avoid hundreds of shots
            # Only shoots if cooldown is 0
            if self.shoot_cooldown == 0:
                self.shoot_cooldown = SHOOT_COOLDOWN

                # Everytime player shoots a bullet is created
                (spawn_bullet_pos_x, spawn_bullet_pos_y) = self.pos
                self.bullet = Bullet(
                    spawn_bullet_pos_x,
                    spawn_bullet_pos_y,
                    self.last_move_direction.x,
                    self.last_move_direction.y,
                )
                bullet_group.add(self.bullet)
                all_sprites_group.add(self.bullet)

        def update(self):
            self.user_input()
            self.move()

            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1

    class Bullet(pygame.sprite.Sprite):

        def __init__(self, x, y, x_direction, y_direction):
            super().__init__()
            # Transparent background for image
            self.image = pygame.Surface((11, 11), pygame.SRCALPHA)
            # Black circle over transparent surface
            pygame.draw.circle(self.image, (0, 0, 0), (5, 5), 5)
            self.rect = self.image.get_rect()
            self.rect.center = (x, y)
            self.x = x
            self.y = y
            self.speed = BULLET_SPEED
            self.velocity_x = x_direction * self.speed
            self.velocity_y = y_direction * self.speed
            self.bullet_lifetime = BULLET_LIFETIME
            # Captures time of bullet creation:
            self.spawn_time = pygame.time.get_ticks()

        def bullet_movement(self):
            # update x and y
            self.x += self.velocity_x
            self.y += self.velocity_y
            # place rectangle at this position
            # They convert to int because .rect object only accepts int values
            # and self.x and self.y are floats
            self.rect.x = int(self.x)
            self.rect.y = int(self.y)

            if pygame.time.get_ticks() - self.spawn_time > self.bullet_lifetime:
                self.kill()

        def update(self):
            self.bullet_movement()

    class TumbleWeed(pygame.sprite.Sprite):

        def __init__(self, position):
            # Using the groups in the father constructor adds the object to those groups automatically
            super().__init__(enemy_group, all_sprites_group)
            self.image = pygame.image.load(
                "graficos/enemigos/tumbleweed.gif"
            ).convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, TUMBWEED_SIZE)

            self.rect = self.image.get_rect()
            self.rect.center = position

            self.direction = pygame.math.Vector2()
            self.velocity = pygame.math.Vector2()
            self.speed = TW_SPEED

            self.position = pygame.math.Vector2(position)

            self.life = TW_LIFE

        def hunt_player(self):
            player_vector = pygame.math.Vector2(player.rect.center)
            enemy_vector = pygame.math.Vector2(self.rect.center)
            distance = self.get_vector_distance(player_vector, enemy_vector)

            if distance > 0:
                self.direction = (player_vector - enemy_vector).normalize()
            else:
                self.direction = pygame.math.Vector2()

            self.velocity = self.direction * self.speed
            self.position += self.velocity

            self.rect.centerx = self.position.x
            self.rect.centery = self.position.y

        def get_vector_distance(self, vector_1, vector_2):
            return (vector_1 - vector_2).magnitude()

        def update(self):
            self.hunt_player()

    class Demon(pygame.sprite.Sprite):

        def __init__(self, position):
            # Using the groups in the father constructor adds the object to those groups automatically
            super().__init__(enemy_group, all_sprites_group)
            self.image = pygame.image.load(
                "graficos/enemigos/Demon.png"
            ).convert_alpha()
            self.image = pygame.transform.rotozoom(self.image, 0, DEMON_SIZE)

            self.rect = self.image.get_rect()
            self.rect.center = position

            self.direction = pygame.math.Vector2()
            self.velocity = pygame.math.Vector2()
            self.speed = DEMON_SPEED

            self.position = pygame.math.Vector2(position)

            self.life = DEMON_LIFE

        def hunt_player(self):
            player_vector = pygame.math.Vector2(player.rect.center)
            enemy_vector = pygame.math.Vector2(self.rect.center)
            distance = self.get_vector_distance(player_vector, enemy_vector)

            if distance > 0:
                self.direction = (player_vector - enemy_vector).normalize()
            else:
                self.direction = pygame.math.Vector2()

            self.velocity = self.direction * self.speed
            self.position += self.velocity

            self.rect.centerx = self.position.x
            self.rect.centery = self.position.y

        def get_vector_distance(self, vector_1, vector_2):
            return (vector_1 - vector_2).magnitude()

        def update(self):
            self.hunt_player()

    all_sprites_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    player = Player()

    all_sprites_group.add(player)

    print("Entra a play")
    running = True
    start_time = pygame.time.get_ticks()

    # Create event to spawn tumbleweed
    SPAWN_TUMBLEWEED = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_TUMBLEWEED, 5000)  # Spawn every 5000 ms

    # Create evento to increase difficulty
    SPAWN_FREQUENCY = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_FREQUENCY, 15000)  # Happens every 15 secs

    # Initial number of tumbleweed
    tumbleweed_spawn_count = 1

    while running:

        if pause == True:
            pass
            # Show pause menu
        else:
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

                if event.type == SPAWN_TUMBLEWEED:
                    # random quantity of Tumbleweed
                    for _ in range(random.randint(1, tumbleweed_spawn_count)):
                        # Random pos outside screen
                        if random.random() < 0.5:  # random num between 0 and 1
                            x = random.randint(-100, 0)  # Appears Left
                        else:
                            x = random.randint(
                                SCREEN_WIDTH, SCREEN_WIDTH + 100
                            )  # Appears Right

                        if random.random() < 0.5:
                            y = random.randint(-100, 0)  # Appears Top
                        else:
                            y = random.randint(
                                SCREEN_HEIGHT, SCREEN_HEIGHT + 100
                            )  # Appears Bottom

                        tumbleweed = TumbleWeed((x, y))
                        all_sprites_group.add(tumbleweed)
                        enemy_group.add(tumbleweed)

                if event.type == SPAWN_FREQUENCY:
                    if tumbleweed_spawn_count < 4:
                        tumbleweed_spawn_count += 1

                    x = random.randint(0, SCREEN_WIDTH)
                    y = random.randint(0, SCREEN_HEIGHT)
                    demon = Demon((x, y))

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        print("Pause")
                        pause == True

            for j in range(0, SCREEN_HEIGHT, ground_height):
                for i in range(0, SCREEN_WIDTH, ground_width):
                    screen.blit(ground, (i, j))

            for enemy in enemy_group:
                bullets_hit = pygame.sprite.spritecollide(enemy, bullet_group, True)
                for _ in bullets_hit:
                    enemy.life -= 1
                    if enemy.life == 0:
                        enemy.kill()

                if player.rect.colliderect(enemy.rect):
                    running = False
                    return "end_of_game"

            if pygame.time.get_ticks() - start_time < 6000:
                screen.blit(play_hint, (50, 50))

            all_sprites_group.draw(screen)
            all_sprites_group.update()

            pygame.display.update()
            clock.tick(FPS)


def info():
    background = pygame.image.load(BG)

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.blit(background, (0, 0))

        OPTIONS_TEXT = menu_font.render("This is the INFO screen", True, "#b68f40")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(SCREEN_WIDTH / 2, 90))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        for i, instruction in enumerate(text_instructions):
            screen.blit(instruction, (70, 190 + i * 50))

        OPTIONS_BACK = Button(
            image=None,
            pos=(SCREEN_WIDTH / 2, 590),
            text_input="BACK",
            font=menu_font,
            base_color="#eba894",
            hovering_color="white",
        )

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    return "main_menu"

        pygame.display.update()


def end_of_game():

    while True:

        MOUSE_POS = pygame.mouse.get_pos()
        message = menu_font.render("HAS PERDIDO", False, "black")
        message_rect = message.get_rect(center=(SCREEN_WIDTH / 2, 200))
        screen.blit(message, message_rect)

        TRY_AGAIN_BUTTON = Button(
            pos=(SCREEN_WIDTH / 2, 550),
            text_input="TRY AGAIN?",
            font=menu_font,
            base_color="#eba894",
            hovering_color="White",
        )

        for button in [TRY_AGAIN_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TRY_AGAIN_BUTTON.checkForInput(MOUSE_POS):
                    return "play"

        pygame.display.update()


def main_menu():
    background = pygame.image.load(BG)

    while True:
        screen.blit(background, (0, 0))

        MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = menu_font.render("C O W B O Y", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(SCREEN_WIDTH / 2, 100))

        PLAY_BUTTON = Button(
            pos=(SCREEN_WIDTH / 2, 250),
            text_input="PLAY",
            font=menu_font,
            base_color="#eba894",
            hovering_color="White",
        )
        INFO_BUTTON = Button(
            pos=(SCREEN_WIDTH / 2, 400),
            text_input="INFO",
            font=menu_font,
            base_color="#eba894",
            hovering_color="White",
        )
        QUIT_BUTTON = Button(
            pos=(SCREEN_WIDTH / 2, 550),
            text_input="QUIT",
            font=menu_font,
            base_color="#eba894",
            hovering_color="White",
        )

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, INFO_BUTTON, QUIT_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MOUSE_POS):
                    return "play"
                if INFO_BUTTON.checkForInput(MOUSE_POS):
                    return "info"
                if QUIT_BUTTON.checkForInput(MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()


game_state = "main_menu"

while True:
    if game_state == "main_menu":
        game_state = main_menu()
    elif game_state == "info":
        game_state = info()
    elif game_state == "play":
        game_state = play()
    elif game_state == "end_of_game":
        game_state = end_of_game()
    else:
        break  # Sal del bucle si game_state no es ninguno de los anteriores

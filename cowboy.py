import pygame
import math
import sys
from settings import *
import random

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("C O W B O Y")
running = True
clock = pygame.time.Clock()

font_type = "fuente/Pixeltype.ttf"
font_size = 80
font_color = "Black"
test_font = pygame.font.Font(font_type, font_size)

ground = pygame.image.load("graficos/ground.png")
ground_width = 200
ground_height = 50

text_surface = test_font.render("C O W B O Y", False, font_color)

# Create event to spawn tumbleweed
SPAWN_TUMBLEWEED = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_TUMBLEWEED, 5000)  # Spawn every 5000 ms

# Create evento to increase difficulty
SPAWN_FREQUENCY = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_FREQUENCY, 15000) # Happens every 15 secs


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(
            pygame.image.load("graficos/jugador/new_piskel.gif").convert_alpha(),
            0,
            PLAYER_SIZE,
        )
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.rect = self.image.get_rect(center = self.pos)
        self.speed = PLAYER_SPEED
        self.shoot = False
        self.shoot_cooldown = 0

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
            self.last_move_direction = pygame.math.Vector2(self.velocity_x, self.velocity_y)

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
                spawn_bullet_pos_x, spawn_bullet_pos_y, self.last_move_direction.x, self.last_move_direction.y
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
        #Transparent background for image
        self.image = pygame.Surface((11, 11), pygame.SRCALPHA)
        #Black circle over transparent surface  
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
        self.image = pygame.image.load("graficos/enemigos/tumbleweed.gif").convert_alpha()
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
    

all_sprites_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


player = Player()

# Initial number of tumbleweed
tumbleweed_spawn_count = 1




all_sprites_group.add(player)

while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == SPAWN_TUMBLEWEED:
            # random quantity of Tumbleweed
            for _ in range(random.randint(1, tumbleweed_spawn_count)):
                # Random pos outside screen
                if random.random() < 0.5:  # random num between 0 and 1
                    x = random.randint(-100, 0)  # Appears Left
                else:
                    x = random.randint( SCREEN_WIDTH,  SCREEN_WIDTH + 100)  # Appears Right

                
                if random.random() < 0.5:  
                    y = random.randint(-100, 0)  # Appears Top
                else:
                    y = random.randint( SCREEN_HEIGHT,  SCREEN_HEIGHT + 100)  # Appears Bottom

                tumbleweed = TumbleWeed((x, y))
                all_sprites_group.add(tumbleweed)
                enemy_group.add(tumbleweed)
        elif event.type == SPAWN_FREQUENCY:
            if tumbleweed_spawn_count < 4:
                tumbleweed_spawn_count += 1

    for j in range(0, SCREEN_HEIGHT, ground_height):
        for i in range(0, SCREEN_WIDTH, ground_width):
            screen.blit(ground, (i, j))
    
    for tumbleweed in enemy_group:
        bullets_hit = pygame.sprite.spritecollide(tumbleweed, bullet_group, True)
        for bullet in bullets_hit:
            tumbleweed.life = 0
            tumbleweed.kill()

    screen.blit(text_surface, (250, 50))

    all_sprites_group.draw(screen)
    all_sprites_group.update()
    
    pygame.display.update()
    clock.tick(FPS)

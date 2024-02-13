import pygame
import math
from settings import *

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

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.rotozoom(pygame.image.load("graficos/jugador/new_piskel.gif").convert_alpha(), 0, PLAYER_SIZE)
        self.pos = pygame.math.Vector2(PLAYER_START_X, PLAYER_START_Y)
        self.speed = PLAYER_SPEED

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

        if self.velocity_x != 0 and self.velocity_y != 0: # moving diagonally
            self.velocity_x /= math.sqrt(2)
            self.velocity_y /= math.sqrt(2)

    def move(self):
        self.pos += pygame.math.Vector2(self.velocity_x, self.velocity_y)

    def shoot(self):
        # La bala debe ir en la misma dirección de velocity pero sumandole un poco más
        pass

    def update(self):
        self.user_input()
        self.move()

player = Player()


while running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False    
    
    for j in range(0, SCREEN_HEIGHT, ground_height):
        for i in range(0, SCREEN_WIDTH, ground_width):
            screen.blit(ground, (i, j))

    screen.blit(text_surface, (250, 50))
    screen.blit(player.image, player.pos)
    player.update()

    pygame.display.update()
    clock.tick(FPS)
 

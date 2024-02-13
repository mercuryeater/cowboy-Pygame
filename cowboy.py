import pygame

pygame.init()
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("C O W B O Y")
running = True
clock = pygame.time.Clock()

font_type = "fuente/Pixeltype.ttf"
font_size = 80
font_color = "Brown"
test_font = pygame.font.Font(font_type, font_size)

ground = pygame.image.load("graficos/ground.png")
ground_width = 200
ground_height = 50

text_surface = test_font.render("C O W B O Y", False, font_color)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False    
    
    for j in range(0, screen_height, ground_height):
        for i in range(0, screen_width, ground_width):
            screen.blit(ground, (i, j))

    screen.blit(text_surface, (280, 50))

    pygame.display.update()
    clock.tick(60)
 

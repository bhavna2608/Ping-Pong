import pygame, sys
pygame.init()

size = WIDTH, HEIGHT = 720, 480
screen = pygame.display.set_mode(size)
col = 0, 0, 255

while True:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(col)

    pygame.display.flip()
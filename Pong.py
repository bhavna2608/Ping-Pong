import pygame

pygame.init()

screen_width = 600
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("PONG")

isRunning = True
while isRunning :

    for event in pygame.event.get() :
        if (event.type == pygame.QUIT) :
            isRunning = False

pygame.quit()
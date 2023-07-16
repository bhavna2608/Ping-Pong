import pygame

pygame.init()

surface = pygame.display.set_mode((600,600))

color = (255,0,0)

isRunning = True

while isRunning :
    pygame.draw.circle(surface, color, [300, 300], 200, 2)
    pygame.display.flip()
    for event in pygame.event.get() :
        if (event.type == pygame.QUIT) :
            isRunning = False

pygame.quit()
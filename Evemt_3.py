import pygame, sys
pygame.init()

size = WIDTH, HEIGHT = 720, 480
screen = pygame.display.set_mode(size)
col = 150, 50, 200

Left = 100
Top = 100
Width = 25
Height = 58
sample = pygame.Rect(Left, Top, Width, Height)

while True:
    for event in pygame.event.get() :
        if event.type == pygame.QUIT: sys.exit()

    sample = sample.move(1.5, 0)
    
    screen.fill(col)
    
    pygame.draw.rect(screen, (255, 255, 255), sample)
    pygame.display.flip()
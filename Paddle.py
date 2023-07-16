import pygame

class paddle:
    def __init__(self, xpos, centhi, len, width, color, surf, screenht, screenwt, paddle_offset) -> None:
        self.xpos = xpos
        self.ypos = centhi
        self.len = len
        self.width = width 
        self.surf = surf
        self.rect = pygame.Rect(self.xpos, self.ypos, self.width, self.len)
        self.color = color
        self.vel = 2
        self.upact = False
        self.downact = False
        self.screenht = screenht
        self.screenwt = screenwt
        self.score = 0
        self.paddle_offset = paddle_offset
        self.targety = 0
    
    def draw(self, deltatime):
        self.move(deltatime)
        pygame.draw.rect(self.surf, self.color, self.rect)

    def checkInp(self, key, isdown):
        if (key == pygame.K_UP) and isdown:
            self.upact = True
        if(key == pygame.K_DOWN) and isdown:
            self.downact = True
        if (key == pygame.K_UP) and not isdown:
            self.upact = False
        if(key == pygame.K_DOWN) and not isdown:
            self.downact = False



    def move(self, deltatime):
        if(self.upact and self.ypos > self.paddle_offset):
            self.ypos -= self.vel*deltatime

        if(self.downact and self.ypos < self.screenht - self.len - self.paddle_offset):
            self.ypos += self.vel*deltatime

        self.rect = pygame.Rect(self.xpos, self.ypos, self.width, self.len)

    def activatebot(self, ball, isL):
        if isL:
            self.targety = (ball.dy/ball.dx)*(0 - ball.xposi) + ball.yposi
        else:
            self.targety = (ball.dy/ball.dx)*(self.screenwt - ball.xposi) + ball.yposi
        
        if self.ypos + self.len/2 >self.targety:
            self.upact = True
            self.downact = False
        else:
            self.downact = True
            self.upact = False
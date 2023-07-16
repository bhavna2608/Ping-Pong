import sys, pygame
pygame.init()

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

class ball:
    def __init__(self, radius, xposi, yposi, surf, scrht, scrwt, color) -> None:
        self.radius = radius
        self.xposi = xposi
        self.yposi = yposi
        self.surf = surf
        self.scrht = scrht
        self.scrwt = scrwt
        self.color = color
        self.rect = pygame.draw.circle(self.surf, self.color, (self.xposi, self.yposi), self.radius)
        self.delvel = 0.5
        self.speedfactor = 0.05
        self.dx = self.delvel
        self.dy = self.delvel
        self.targety = 0

    def draw(self, deltatime, paddle_offset, paddL, paddR):
        self.move(deltatime, paddle_offset, paddL, paddR)
        self.rect = pygame.draw.circle(self.surf, self.color, (self.xposi, self.yposi), self.radius)

    def move(self, deltatime, paddle_offset, paddL, paddR):
        if self.yposi < 0+paddle_offset or self.yposi > self.scrht - paddle_offset:
            self.dy += 1

        if self.xposi < paddle_offset or self.xposi > self.scrwt - paddle_offset:
            if(self.xposi < paddle_offset):
                paddR.score += 1
            else:
                paddL.score += 1

            self.xposi = self.scrwt/2
            self.yposi = self.scrht/2

            self.dx = self.delvel
            self.dy = self.delvel* random.random() * genUtil.getsign(self.dy)

        self.xposi += self.dx*deltatime
        self.yposi += self.dy*deltatime

    def checkCollision(self, Lrect, Rrect, paddle_offset):
        if pygame.Rect.colliderect(self.rect, Lrect) or pygame.Rect.colliderect(self.rect, Rrect):
            if self.xposi > self.scrwt/2:
                self.xposi = self.scrwt - paddle_offset - self.radius - Rrect.width - 1
            else:
                self.xposi = paddle_offset + Lrect.width + self.radius + 1

            self.dy = self.delvel * random.random() * genUtil.getsign(self.dy)
            self.dy += abs(self.dy) * self.speedfactor*genUtil.getsign(self.dy)

            self.dx += abs(self.dx) * self.speedfactor * genUtil.getsign(self.dx)
            self.dx += -1

    def activatebott(self, ball, isL):
        if isL:
            pass


pygame.display.set_caption("PONG")

clock = pygame.time.Clock()

SCR_WTH = 1000
SCR_HT = 700

FontSize = 150

paddle_offset = 20
paddle_width = 15

screen = pygame.display.set_mode((SCR_WTH, SCR_HT))

paddL = paddle(paddle_offset, SCR_HT/2 - 70, 140, paddle_width, (0, 0, 225, 1), screen, SCR_HT, SCR_WTH, paddle_offset)
paddR = paddle(SCR_WTH - paddle_offset - paddle_width, SCR_HT/2, 140, paddle_width, (238, 130, 238, 1), screen, SCR_HT, SCR_WTH, paddle_offset)

ball = ball(30, SCR_WTH/2, SCR_HT/2, screen, SCR_HT, SCR_WTH, (255, 255, 255, 1))

while 1:
    deltatime = clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.KEYDOWN:

            paddR.checkInp(event.key, True)
            pass

        elif event.type == pygame.KEYUP:
            
            paddR.checkInp(event.key, False)
            pass

     
    pygame.draw.line(screen, (255, 165, 0, 1), (SCR_WTH/2, 0), (SCR_WTH/2, SCR_HT), paddle_offset)
    pygame.draw.rect(screen, (255, 165, 0, 1), pygame.Rect(0, 0, SCR_WTH, SCR_HT), paddle_offset)

    font = pygame.font.SysFont(None, FontSize)

    Lscore = font.render(str(paddL.score), True, (255, 165, 0, 1))
    screen.blit(Lscore, (SCR_WTH/4, SCR_HT/2 - FontSize/2))

    Rscore = font.render(str(paddR.score), True, (255, 165, 0, 1))
    screen.blit(Lscore, (SCR_WTH * 3/4, SCR_HT/2 - FontSize/2))

    paddL.activatebot(ball, True)
    paddR.activatebot(ball, False)

    ball.checkCollision(paddL.rect, paddR.rect, paddle_offset)
    paddL.draw(deltatime)
    paddR.draw(deltatime)

    pygame.display.flip()

    screen.fill((0,0,0,1))

pygame.quit()
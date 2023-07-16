import pygame
import random
import genUtil

class ball:
    def __init__(self, radius, xposi, yposi, surf, scrht, scrwt) -> None:
        self.radius = radius
        self.xposi = xposi
        self.yposi = yposi
        self.surf = surf
        self.scrht = scrht
        self.scrwt = scrwt
        self.color = (0, 198, 0, 1)
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
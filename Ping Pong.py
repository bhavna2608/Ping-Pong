import pygame
pygame.init()

width = 700
height = 500
FPS = 80
PaddleHeight = 140
PaddleWidth = 15
BallRadius = 12
ScoreFont = pygame.font.SysFont("comicsans", 60)
WinningScore = 3

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Ping Pong")

class Ball:
    Max_Velocity = +5
    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.Max_Velocity
        self.y_vel = 0
        self.targety = 0

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255, 1), (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel *= -1
        self.y_vel = 0

class Paddle:
    Velocity = 4

    def __init__(self, x, y, wdth, ht, color):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.wdth = wdth
        self.ht = ht
        self.color = color
        self.targety = 0
        self.upact = False
        self.downact = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.wdth, self.ht))

    def move(self, up=True):
        if up:
           self.y -= self.Velocity
        else:
            self.y += self.Velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y


    def activatebot(self, ball, isL, LeftPaddle):
        if isL:
            self.targety = ((ball.y - (self.y + self.ht))/(ball.x - (self.x + self.wdth/2)))*(0 - ball.x) + ball.y
        else:
            self.targety = ((ball.y - (self.y + self.ht)))*(self.wdth - ball.x) + ball.y
        
        if self.y + self.ht/2 > self.targety:
            LeftPaddle.move(up = True)
        else:
            LeftPaddle.move(up = False)

def draw(screen, paddles, ball, LeftScore, RightScore):
    screen.fill((0, 0, 0, 1))

    LeftScore_text = ScoreFont.render(f"{LeftScore}", 1, (255, 255, 255, 1))
    RightScore_text = ScoreFont.render(f"{RightScore}", 1, (255, 255, 255, 1))
    screen.blit(LeftScore_text, (width//4 - LeftScore_text.get_width()//2, 30))
    screen.blit(RightScore_text, (width*3//4 - RightScore_text.get_width()//2, 30))

    for paddle in paddles:
        paddle.draw(screen)

    ball.draw(screen)

    for i in range(10, height, height//20):
        if i%2 == 1:
           continue
        pygame.draw.rect(screen, (0, 98, 255, 1), (width//2 - 5, i, 10, height//20))
    pygame.draw.rect(screen, (0, 98, 255, 1), pygame.Rect(0, 0, width, height), 20)

    pygame.display.update()

def handle_collision(ball, LeftPaddle, RightPaddle):
    if ball.y + ball.radius >= height - 20:
       ball.y_vel *= -1
    elif ball.y - ball.radius <= 20:
       ball.y_vel *= -1

    if ball.x_vel < 0:
       if ball.y >= LeftPaddle.y and ball.y <= LeftPaddle.y + LeftPaddle.ht:
          if ball.x - ball.radius <= LeftPaddle.x + LeftPaddle.wdth:
              sound = pygame.mixer.Sound("New folder\Resources\Hit.mp3")
              pygame.mixer.Sound.play(sound)
              ball.x_vel *= -1

              middle_y = LeftPaddle.y + LeftPaddle.ht/2
              difference_in_y = middle_y - ball.y
              reduction_factor = (LeftPaddle.ht/2)/ball.Max_Velocity
              y_vel = difference_in_y/reduction_factor
              ball.y_vel = (-1 * ball.y_vel) + (-1.2 * y_vel)
    else:
        if ball.y >= RightPaddle.y and ball.y <= RightPaddle.y + RightPaddle.ht:
          if ball.x + ball.radius >= RightPaddle.x:
              sound = pygame.mixer.Sound("New folder\Resources\Hit.mp3")
              pygame.mixer.Sound.play(sound)
              ball.x_vel *= -1

              middle_y = RightPaddle.y + RightPaddle.ht/2
              difference_in_y = middle_y - ball.y
              reduction_factor = (RightPaddle.ht/2)/ball.Max_Velocity
              y_vel = difference_in_y/reduction_factor
              ball.y_vel = (-1 * ball.y_vel) + (-1.2 * y_vel)

def activatebot(self, ball, isL):
        if isL:
            pass

def handle_paddle_movement(keys, LeftPaddle, RightPaddle):
    if keys[pygame.K_w] and LeftPaddle.y - LeftPaddle.Velocity >= 20:
       LeftPaddle.move(up=True)
    if keys[pygame.K_UP] and RightPaddle.y - RightPaddle.Velocity >= 20:
       RightPaddle.move(up=True)
    if keys[pygame.K_s] and LeftPaddle.y + LeftPaddle.Velocity + LeftPaddle.ht <= height - 20:
       LeftPaddle.move(up=False)
    if keys[pygame.K_DOWN] and RightPaddle.y + RightPaddle.Velocity + RightPaddle.ht <= height - 20:
       RightPaddle.move(up=False)

def main():
    run = True
    clock = pygame.time.Clock()

    LeftPaddle = Paddle(20, height/2 - PaddleHeight/2, PaddleWidth, PaddleHeight, (255, 165, 0, 1))
    RightPaddle = Paddle(width - 20 - PaddleWidth, height/2 - PaddleHeight/2, PaddleWidth, PaddleHeight, (0, 206, 83, 1))

    ball = Ball(width//2, height//2, BallRadius)

    LeftScore = 0
    RightScore = 0
    
    while run:
        clock.tick(FPS)
        draw(screen, [LeftPaddle, RightPaddle], ball, LeftScore, RightScore)
        pygame.mixer.init()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
           run = False
        handle_paddle_movement(keys, LeftPaddle, RightPaddle)

        ball.move()
        handle_collision(ball, LeftPaddle, RightPaddle)

        if ball.x <= 20:
           sound1 = pygame.mixer.Sound("New folder\Resources\Point.wav")
           pygame.mixer.Sound.play(sound1)
           RightScore += 1
           ball.reset()
        if ball.x >= width - 20:
           sound1 = pygame.mixer.Sound("New folder\Resources\Point.wav")
           pygame.mixer.Sound.play(sound1)
           LeftScore += 1
           ball.reset()

        #LeftPaddle.activatebot(ball, True, LeftPaddle)
        
        Won = False
        if LeftScore == WinningScore:
           sound2 = pygame.mixer.Sound("New folder\Resources\Game Win.wav")
           pygame.mixer.Sound.play(sound2)
           Won = True
           win_text = "Left Player Won!"
        if RightScore == WinningScore:
           sound2 = pygame.mixer.Sound("New folder\Resources\Game Win.wav")
           pygame.mixer.Sound.play(sound2)
           Won = True
           win_text = "Right Player Won!"

        if Won:
           text = ScoreFont.render(win_text, 1, (255, 255, 255, 1))
           screen.blit(text, (width//2 - text.get_width()//2, height//2 - text.get_height()//2))
           pygame.display.update()
           pygame.time.delay(2500)
           ball.reset()
           LeftPaddle.reset()
           RightPaddle.reset()
           LeftScore = 0
           RightScore = 0


    pygame.quit()

if __name__ == '__main__':
    main()
       
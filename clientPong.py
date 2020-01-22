import pygame
import time
import numpy
import math
import pygame_textinput
from network import Network
#import statistics

pygame.init()

# set useful shit
display_width = 600#pygame.display.Info().current_w
display_height = 400#pygame.display.Info().current_h

black = (0,0,0)
white = (255,255,255)
red_bright = (255,0,0)
green_bright = (0,255,0)
blue_bright = (0,0,255)

red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
grey = (100,100,100)
light_grey = (200,200,200)


gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

def generate_board(ballx,bally,p1,p2):
    gameDisplay.fill(black)
    # generate ball
    pygame.draw.rect(gameDisplay,white,(ballx,bally+3,16,10))
    pygame.draw.rect(gameDisplay,white,(ballx+3,bally,10,16))

    # generate players
    pygame.draw.rect(gameDisplay,white,p1.rect)
    pygame.draw.rect(gameDisplay,white,p2.rect)

    pygame.display.update()
    clock.tick(60)

class player():
    def __init__ (self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x,self.y,width,height)
        self.vel = 5

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        # if keys[pygame.K_LEFT]:
        #     self.x -= self.vel
        #
        # if keys[pygame.K_RIGHT]:
        #     self.x += self.vel

        if keys[pygame.K_UP]:
            self.y -= self.vel

        if keys[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)

#    def draw(self, win):
#        pygame.draw.rect(win, self.color, self.rect)

def read_pos(str):
    str = str.split(",")
    print(len(str))
    print(str)
    return int(str[0]),int(str[1]),int(str[2]),int(str[3])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])

def game_loop():
    n = Network()
    startPos = read_pos(n.getPos())

    p1 = player(startPos[0],startPos[1],10,50,white)
    p2 = player(0,0,10,50,white)

    gameRunning = True
    ballx = 284
    bally = 184
    p1Ychange = 0
    p2Ychange = 0
    ballXchange = numpy.random.randint(3,5)
    ballYchange = numpy.random.randint(-3,3)
    # print(ballYchange)
    p1score = 0
    p2score = 0

    while gameRunning:
        receivedData = read_pos(n.send(make_pos((p1.x,p1.y))))
        p2.x = receivedData[0]
        p2.y = receivedData[1]
        ballx = receivedData[2]
        bally = receivedData[3]
        p2.update()

        # do something when something happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # if event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_DOWN:
            #         p2Ychange += 5
            #     elif event.key == pygame.K_UP:
            #         p2Ychange -= 5
            #     elif event.key == pygame.K_s:
            #         p1Ychange += 5
            #     elif event.key == pygame.K_w:
            #         p1Ychange -= 5
            # elif event.type == pygame.KEYUP:
            #     if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            #         p2Ychange = 0
            #     elif event.key == pygame.K_w or event.key == pygame.K_s:
            #         p1Ychange = 0

        # p1.y += p1Ychange
        # p2.y += p2Ychange
        p1.move()
        ballx += ballXchange
        bally += ballYchange

        # prevent them from going off the screen
        if p1.y < 0:
            p1.y = 0
        elif p1.y > 400-(p1.height):
            p1.y = 400-(p1.height)
        if p2.y < 0:
            p2.y = 0
        elif p2.y > 400-(p1.height):
            p2.y = 400-(p1.height)

        # if pygame.Rect(p1.rect).collidepoint((ballx,bally+8)):
        #     if bally+8 > p1.y+(p1.height/2):
        #         ballYchange = round(abs((bally+8)-(p1.y+p1.height/2))/(p1.height/2)*(3),0)
        #     elif bally+8 < p1.y+(p1.height/2):
        #         ballYchange = round(abs((bally+8)-(p1.y+p1.height/2))/(p1.height/2)*(3),0)*-1
        #     ballXchange *= -1
        #     ballx += 5
        #     print("collison with p1")
        #     print(ballYchange)
        # elif pygame.Rect(p2.rect).collidepoint((ballx+16,bally+8)):
        #     if bally+8 > p2.y+(p2.height/2):
        #         ballYchange = round(abs((bally+8)-(p2.y+p2.height/2))/(p2.height/2)*(3),0)
        #     elif bally+8 < p2.y+(p2.height/2):
        #         ballYchange = round(abs((bally+8)-(p2.y+p2.height/2))/(p2.height/2)*(3),0)*-1
        #     ballXchange *= -1
        #     ballx -= 5
        #     print("collison with p2")
        #     print(ballYchange)
        # elif ballx <= 0:
        #     ballXchange *= -1
        #     p2score += 2
        # elif ballx >= 574:
        #     ballXchange *= -1
        #     p1score += 1
        #
        # # if p1score == 10 or p2score == 10:
        # #     gameRunning = False
        #
        # if bally <= 0 or bally >= 384:
        #     ballYchange *= -1




        generate_board(ballx,bally,p1,p2)

game_loop()

pygame.quit()
quit()

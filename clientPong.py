import pygame
import numpy
#import pygame_textinput
from network import Network
from player import Player
from player import Ball

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

def generate_board(ball,p1,p2):
    gameDisplay.fill(black)
    # generate ball
    pygame.draw.rect(gameDisplay,white,(ball.x,ball.y+3,ball.width,ball.height-6))
    pygame.draw.rect(gameDisplay,white,(ball.x+3,ball.y,ball.width-6,ball.height))

    # generate players
    print(p1.rect)
    pygame.draw.rect(gameDisplay,white,p1.rect)
    pygame.draw.rect(gameDisplay,white,p2.rect)

    pygame.display.update()
    #clock.tick(60)



#    def draw(self, win):
#        pygame.draw.rect(win, self.color, self.rect)

def game_loop():
    n = Network()
    p1 = n.getP()
    print(p1.rect)

    gameRunning = True
    p1score = 0
    p2score = 0

    while gameRunning:
        sendData = {
            "player":p1
        }
        receivedData = n.send(sendData)
        p2 = receivedData["player"]
        ball = receivedData["ball"]
        p2.update()

        # do something when something happens
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # move the player
        p1.move()

        # prevent player from going off the screen
        if p1.y < 0:
            p1.y = 0
        elif p1.y > 400-(p1.height):
            p1.y = 400-(p1.height)
        if p2.y < 0:
            p2.y = 0
        elif p2.y > 400-(p1.height):
            p2.y = 400-(p1.height)




        generate_board(ball,p1,p2)
        clock.tick(60)

game_loop()

pygame.quit()
quit()

import pygame
import numpy
#import pygame_textinput
from network import Network
from player import Player
from player import Ball
from player import Settings

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


def generate_board(ball, p1, p2):
    gameDisplay.fill(black)
    # generate ball
    pygame.draw.rect(gameDisplay, white, (ball.x, ball.y+3, ball.width, ball.height-6))
    pygame.draw.rect(gameDisplay, white, (ball.x+3, ball.y, ball.width-6, ball.height))

    # generate players
    pygame.draw.rect(gameDisplay, white, p1.rect)
    pygame.draw.rect(gameDisplay, white, p2.rect)

    pygame.display.update()


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100
        self.rect = (self.x, self.y, self.width, self.height)

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, white)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2), (self.y + round(self.height/2) - round(text.get_height()/2))))


def game_loop(p1, p2, n, settings):
    gameRunning = True

    while gameRunning:
        sendData = {
            "player": p1,
            "settings": settings
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
        elif p1.y > 400-p1.height:
            p1.y = 400-p1.height
        if p2.y < 0:
            p2.y = 0
        elif p2.y > 400-p1.height:
            p2.y = 400-p1.height

        generate_board(ball, p1, p2)
        clock.tick(60)


def main_menu():
    n = Network()
    p1 = n.getP()
    settings = Settings(70, 50, 5, 5, 3, 3)
    ready_btn = Button("Ready", display_width//2-75, 300, grey)
    while True:
        sendData = {
            "player": p1,
            "settings": settings
        }
        receivedData = n.send(sendData)
        p2 = receivedData["player"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pygame.Rect(ready_btn.rect).collidepoint(pos):
                    p1.ready = True

        gameDisplay.fill(black)
        settings.draw(gameDisplay, display_width, white)
        ready_btn.draw(gameDisplay)
        pygame.display.update()
        if receivedData["ready"]:
            print("Game starting")
            break

    if p1.number == 0:
        p1.height = settings.p1size
    else:
        p1.height = settings.p2size
    game_loop(p1, p2, n, settings)

main_menu()
pygame.quit()
quit()

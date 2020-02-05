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


def generate_board(ball, p1, p2, score):
    gameDisplay.fill(black)
    # generate ball
    pygame.draw.rect(gameDisplay, white, (ball.x, ball.y+3, ball.width, ball.height-6))
    pygame.draw.rect(gameDisplay, white, (ball.x+3, ball.y, ball.width-6, ball.height))

    # generate players
    pygame.draw.rect(gameDisplay, white, p1.rect)
    pygame.draw.rect(gameDisplay, white, p2.rect)

    for y in [0, 38, 76, 114, 152, 190, 228, 266, 304, 342, 380]:
        pygame.draw.rect(gameDisplay, white, (display_width // 2 - 1, y, 2, 20))

    font = pygame.font.SysFont("comicsans", 40)
    text = font.render(str(score[0]), 1, white)
    gameDisplay.blit(text, (display_width // 2 - 50 - text.get_width() // 2, 10))
    text = font.render(str(score[1]), 1, white)
    gameDisplay.blit(text, (display_width // 2 + 50 - text.get_width() // 2, 10))

    pygame.display.update()


class Button:
    def __init__(self, id, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = (self.x, self.y, self.width, self.height)
        self.id = id

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
        score = receivedData["score"]
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

        generate_board(ball, p1, p2, score)
        clock.tick(60)


def main_menu():
    n = Network()
    p1 = n.getP()
    settings = Settings(50, 50, 5, 5, 3, 7)
    ready_btn = Button("Ready", "Ready", display_width//2-75, 310, 150, 75, grey)
    settings_btns = [
        Button("p1_size+", "+", display_width // 2 + 100, 25, 25, 25, grey),
        Button("p1_size-", "-", display_width // 2 - 125, 25, 25, 25, grey),
        Button("p2_size+", "+", display_width // 2 + 100, 75, 25, 25, grey),
        Button("p2_size-", "-", display_width // 2 - 125, 75, 25, 25, grey),
        Button("p1_vel+", "+", display_width // 2 + 100, 125, 25, 25, grey),
        Button("p1_vel-", "-", display_width // 2 - 125, 125, 25, 25, grey),
        Button("p2_vel+", "+", display_width // 2 + 100, 175, 25, 25, grey),
        Button("p2_vel-", "-", display_width // 2 - 125, 175, 25, 25, grey),
        Button("x_vel+", "+", display_width // 2 + 175, 225, 25, 25, grey),
        Button("x_vel-", "-", display_width // 2 - 200, 225, 25, 25, grey),
        Button("y_vel+", "+", display_width // 2 + 175, 275, 25, 25, grey),
        Button("y_vel-", "-", display_width // 2 - 200, 275, 25, 25, grey)
    ]

    while True:
        sendData = {
            "player": p1,
            "settings": settings
        }
        receivedData = n.send(sendData)
        p2 = receivedData["player"]
        if p1.number == 1:
            settings = receivedData["settings"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pygame.Rect(ready_btn.rect).collidepoint(pos):
                    p1.ready = True
                elif p1.number == 0:
                    for btn in settings_btns:
                        if pygame.Rect(btn.rect).collidepoint(pos):
                            if btn.id == "p1_size+":
                                settings.p1size += 10
                            elif btn.id == "p1_size-":
                                settings.p1size -= 10
                            elif btn.id == "p2_size+":
                                settings.p2size += 10
                            elif btn.id == "p2_size-":
                                settings.p2size -= 10
                            elif btn.id == "p1_vel+":
                                settings.p1vel += 1
                            elif btn.id == "p1_vel-":
                                settings.p1vel -= 1
                            elif btn.id == "p2_vel+":
                                settings.p2vel += 1
                            elif btn.id == "p2_vel-":
                                settings.p2vel -= 1
                            elif btn.id == "x_vel+":
                                settings.ballxvel += 1
                            elif btn.id == "x_vel-":
                                settings.ballxvel -= 1
                            elif btn.id == "y_vel+":
                                settings.ballyvel += 1
                            elif btn.id == "y_vel-":
                                settings.ballyvel -= 1

        gameDisplay.fill(black)
        if p1.number == 0:
            settings.draw(gameDisplay, display_width, white, settings_btns)
        else:
            settings.draw(gameDisplay, display_width, white, [])
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

import pygame
import numpy

class Player():
    def __init__ (self, number, x, y, width, height, color):
        self.number = number
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x,self.y,width,height)
        self.vel = 5
        self.ready = False

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


class Ball():
    def __init__ (self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x,self.y,width,height)
        self.xvel = 3 #numpy.random.randint(3,5)
        self.yvel = numpy.random.randint(-3,3)

    def update(self):
        self.x += self.xvel
        self.y += self.yvel
        self.rect = (self.x, self.y, self.width, self.height)


class Settings:
    def __init__(self, p1size, p2size, p1vel, p2vel, ballxvel, ballyvel):
        self.p1size = p1size
        self.p2size = p2size
        self.p1vel = p1vel
        self.p2vel = p2vel
        self.ballxvel = ballxvel
        self.ballyvel = ballyvel

    # draw text for each setting
    def draw(self, win, display_width, color):
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render("P1 size: " + str(round(self.p1size / 10)), 1, color)
        win.blit(text, (round(display_width / 2) - round(text.get_width() / 2), 25))

        text = font.render("P2 size: " + str(round(self.p2size / 10)), 1, color)
        win.blit(text, (round(display_width / 2) - round(text.get_width() / 2), 75))

        text = font.render("P1 speed: " + str(self.p1vel), 1, color)
        win.blit(text, (round(display_width / 2) - round(text.get_width() / 2), 125))

        text = font.render("P2 speed: " + str(self.p2vel), 1, color)
        win.blit(text, (round(display_width / 2) - round(text.get_width() / 2), 175))

        text = font.render("Ball horizontal speed: " + str(self.ballxvel), 1, color)
        win.blit(text, (round(display_width / 2) - round(text.get_width() / 2), 225))

        text = font.render("Ball vertical speed: " + str(self.ballyvel), 1, color)
        win.blit(text, (round(display_width / 2) - round(text.get_width() / 2), 275))
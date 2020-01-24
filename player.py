import pygame
import numpy

class Player():
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

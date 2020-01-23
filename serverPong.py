import socket
import pygame
import numpy
from _thread import *
#import sys

server = "192.168.1.130"
port = 5555

pygame.init()
clock = pygame.time.Clock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class ball():
    def __init__ (self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (self.x,self.y,width,height)
        self.xvel = numpy.random.randint(3,5)
        self.yvel = numpy.random.randint(-3,3)

    def update(self):
        self.x += self.xvel
        self.y += self.yvel
        self.rect = (self.x, self.y, self.width, self.height)

ball = ball(284, 184, 16, 16, (255,255,255))
gameRunning = True

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, server started.")


def read_pos(mystr):
    mystr = mystr.split(",")
    if (len(mystr)!= 2):
        print(len(mystr))
        print(mystr)
    return int(mystr[0]),int(mystr[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3])


def gameloop():
    while gameRunning:
        # Check for collision of ball with either player
        if pygame.Rect(pos[0][0], pos[0][1], 10, 50).collidepoint(ball.x, ball.y + 8):
            if ball.y + 8 > pos[0][1] + (50 / 2):
                ball.yvel = round(abs((ball.y + 8) - (pos[0][1] + 50 / 2)) / (50 / 2) * 3, 0)
            elif ball.y + 8 < pos[0][1] + (50 / 2):
                ball.yvel = round(abs((ball.y + 8) - (pos[0][1] + 50 / 2)) / (50 / 2) * 3, 0) * -1
            ball.yvel = int(ball.yvel)
            ball.xvel *= -1
            ball.x += 5
            print("collision with p1")
            print(ball.yvel)
        elif pygame.Rect(pos[1][0], pos[1][1], 10, 50).collidepoint(ball.x + 16, ball.y + 8):
            if ball.y + 8 > pos[1][1] + (50 / 2):
                ball.yvel = round(abs((ball.y + 8) - (pos[1][1] + 50 / 2)) / (50 / 2) * 3, 0)
            elif ball.y + 8 < pos[1][1] + (50 / 2):
                ball.yvel = round(abs((ball.y + 8) - (pos[1][1] + 50 / 2)) / (50 / 2) * 3, 0) * -1
            ball.yvel = int(ball.yvel)
            ball.xvel *= -1
            ball.x -= 5
            print("collision with p2")
            print(ball.yvel)
        # Check if a player wall is hit
        elif ball.x <= 0:
            # reset ball location
            ball.x = 284
            ball.y = 184
            # p2score += 1
        elif ball.x >= 574:
            # reset ball location
            ball.x = 284
            ball.y = 184
            # p1score += 1

        # if p1score == 10 or p2score == 10:
        #     gameRunning = False

        if ball.y <= 0 or ball.y >= 384:
            ball.yvel *= -1

        ball.update()
        clock.tick(60)

pos = [(0,200-25),(590,200-25)]


def threaded_client(conn, player, ball):
    #print((pos[player][0],pos[player][1],ball.x,ball.y))
    conn.send(str.encode(make_pos((pos[player][0],pos[player][1],ball.x,ball.y))))
    #reply = ""
    while True:
        # I commented the try-except out to ensure we can fix bugs.
        #try:
            data = read_pos(conn.recv(2048).decode())
            pos[player] = data





            if not data:
                print("disconnected")
                break
            else:
                if player == 1:
                    reply = pos[0]
                else:
                    reply = pos[1]
                reply = (reply[0],reply[1],ball.x,ball.y)
                print("received: ", data)
                print("sending: ", reply)

            conn.sendall(str.encode(make_pos(reply)))


        # except:
        #     break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer, ball))
    currentPlayer += 1
    # once both players connected we need to start the gameloop
    if currentPlayer == 2:
        print("both players connected")
        gameloop()
        break
print("done")

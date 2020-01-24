import socket
import pygame
import numpy
from _thread import *
from player import Player
from player import Ball
import pickle
#import sys

black = (0,0,0)
white = (255,255,255)
red_bright = (255,0,0)
green_bright = (0,255,0)
blue_bright = (0,0,255)

server = "192.168.1.130"
port = 5555

pygame.init()
clock = pygame.time.Clock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



ball = Ball(284, 184, 16, 16, (255,255,255))
gameRunning = True

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, server started.")


def gameloop():
    while gameRunning:
        # Check for collision of ball with either player
        if pygame.Rect(players[0].rect).collidepoint(ball.x, ball.y + 8):
            if ball.y + 8 >= players[0].y + (50 / 2):
                ball.yvel = round(abs((ball.y + 8) - (players[0].y + 50 / 2)) / (50 / 2) * 3, 0)
            elif ball.y + 8 <= players[0].y + (50 / 2):
                ball.yvel = round(abs((ball.y + 8) - (players[0].y + 50 / 2)) / (50 / 2) * 3, 0) * -1
            ball.yvel = int(ball.yvel)
            ball.xvel *= -1
            ball.x += 5
            print("collision with p1")
            print(ball.yvel)
        elif pygame.Rect(players[1].rect).collidepoint(ball.x + 16, ball.y + 8):
            if ball.y + 8 > players[1].y + (50 / 2):
                ball.yvel = round(abs((ball.y + 8) - (players[1].y + 50 / 2)) / (50 / 2) * 3, 0)
            elif ball.y + 8 < players[1].y + (50 / 2):
                ball.yvel = round(abs((ball.y + 8) - (players[1].y + 50 / 2)) / (50 / 2) * 3, 0) * -1
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

# start position players
players = [Player(0,int(200-(50/2)),10,50,white),Player(590,int(200-(50/2)),10,50,white)]


def threaded_client(conn, player, ball):
    #print((players[player].x,players[player].y,ball.x,ball.y))
    initial_send = {
        "player": players[player],
        "ball": ball
    }
    conn.send(pickle.dumps(initial_send["player"]))
    #reply = ""
    while True:
        # I commented the try-except out to ensure we can fix bugs.
        #try:
            data = pickle.loads(conn.recv(2048))
            players[player] = data["player"]

            if not data:
                print("disconnected")
                break
            else:
                if player == 1:
                    reply = {
                        "player": players[0],
                        "ball": ball
                    }
                else:
                    reply = {
                        "player": players[1],
                        "ball": ball
                    }

                #print("received: ", data)
                #print("sending: ", reply)

            conn.sendall(pickle.dumps(reply))


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

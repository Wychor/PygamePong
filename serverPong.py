import socket
import pygame
# import numpy
from _thread import *
from classes import Player
from classes import Ball
from classes import Settings
import pickle

black = (0, 0, 0)
white = (255, 255, 255)
red_bright = (255, 0, 0)
green_bright = (0, 255, 0)
blue_bright = (0, 0, 255)

server = ""
port = 5555

pygame.init()
clock = pygame.time.Clock()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ball = Ball(284, 184, 16, 16, white)
gameRunning = False

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    print(e)

s.listen()
print("Waiting for a connection, server started.")

connected = set()
games = {}
idCount = 0
setting_vals = Settings(50, 50, 5, 5, 3, 7)
score = [0, 0]


def ball_collision_check():
    while True:
        # Check for collision of ball with either player
        if pygame.Rect(players[0].rect).collidepoint(ball.x, ball.y + 8):
            if ball.y + 8 >= players[0].y + (players[0].height / 2):
                ball.yvel = round(abs((ball.y + 8) - (players[0].y + players[0].height / 2)) / (players[0].height / 2) * ball.yvelmax, 0)
            elif ball.y + 8 <= players[0].y + (players[0].height / 2):
                ball.yvel = round(abs((ball.y + 8) - (players[0].y + players[0].height / 2)) / (players[0].height / 2) * ball.yvelmax, 0) * -1
            ball.yvel = int(ball.yvel)
            ball.xvel *= -1
            ball.x += 5
            print("collision with p1")
            print(ball.yvel)
        elif pygame.Rect(players[1].rect).collidepoint(ball.x + 16, ball.y + 8):
            if ball.y + 8 > players[1].y + (players[1].height / 2):
                ball.yvel = round(abs((ball.y + 8) - (players[1].y + players[1].height / 2)) / (players[1].height / 2) * ball.yvelmax, 0)
            elif ball.y + 8 < players[1].y + (players[1].height / 2):
                ball.yvel = round(abs((ball.y + 8) - (players[1].y + players[1].height / 2)) / (players[1].height / 2) * ball.yvelmax, 0) * -1
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
            score[1] += 1
        elif ball.x >= 574:
            # reset ball location
            ball.x = 284
            ball.y = 184
            score[0] += 1

        if ball.y <= 0 or ball.y >= 384:
            ball.yvel *= -1

        ball.update()
        clock.tick(60)


# start position players
players = [Player(0, 0, int(200-(50/2)), 10, 50, white),
           Player(1, 590, int(200-(50/2)), 10, 50, white)]


def threaded_client(conn, player, ball):
    global setting_vals
    initial_send = {
        "player": players[player],
        "ball": ball,
        "score": score
    }
    conn.send(pickle.dumps(initial_send["player"]))

    setup = False
    gameRunning = False

    while True:
        data = pickle.loads(conn.recv(2048))
        players[player].y = data["player"].y
        players[player].update()
        players[player].ready = data["player"].ready
        if player == 0:
            setting_vals = data["settings"]

        # once both players connected we need to start the gameloop
        if not setup and gameRunning and player == 0:
            players[0].height = setting_vals.p1size
            players[1].height = setting_vals.p2size
            players[0].vel = setting_vals.p1vel
            players[1].vel = setting_vals.p2vel
            ball.xvel = setting_vals.ballxvel
            ball.yvelmax = setting_vals.ballyvel
            players[0].update()
            players[1].update()
            start_new_thread(ball_collision_check, ())
            setup = True

        if not data:
            print("disconnected")
            break
        else:
            reply = {
                    "ball": ball,
                    "score": score
                }

            if players[0].ready and players[1].ready:
                reply["ready"] = True
                gameRunning = True
            else:
                reply["ready"] = False

            if player == 1:
                reply["player"] = players[0]
                reply["settings"] = setting_vals
            else:
                reply["player"] = players[1]

        conn.sendall(pickle.dumps(reply))

    print("Lost connection")
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    if idCount % 2 == 0:
        p = 1

    start_new_thread(threaded_client, (conn, p, ball))

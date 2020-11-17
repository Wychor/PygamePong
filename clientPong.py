import pygame
from network import Network
from classes import Settings

pygame.init()

# set useful things
display_width = 600
display_height = 400

black = (0, 0, 0)
white = (255, 255, 255)
red_bright = (255, 0, 0)
green_bright = (0, 255, 0)
blue_bright = (0, 0, 255)

red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
grey = (100, 100, 100)
light_grey = (200, 200, 200)


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
    def __init__(self, button_id, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = (self.x, self.y, self.width, self.height)
        self.id = button_id

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, white)
        win.blit(text, (self.x + round(self.width/2) - round(text.get_width()/2),
                        (self.y + round(self.height/2) - round(text.get_height()/2))))


def game_loop(p1, n, settings):
    game_running = True

    while game_running:
        send_data = {
            "player": p1,
            "settings": settings
        }
        send_datareceived_data = n.send(send_data)
        p2 = send_datareceived_data["player"]
        ball = send_datareceived_data["ball"]
        score = send_datareceived_data["score"]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        p1.move()

        p1.border_guard()
        p2.border_guard()

        generate_board(ball, p1, p2, score)
        clock.tick(60)


def main_menu():
    n = Network()
    p1 = n.getP()

    # Can't put buttons in settings cause then pickle can't pickle it.
    # Putting the buttons in settings would've been a bad idea anyway cause the server doesn't need them
    ready_button = Button("Ready", "Ready", display_width // 2 - 75, 310, 150, 75, grey)
    settings_buttons = [
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
    settings = Settings(50, 50, 5, 5, 3, 7)

    while True:
        send_data = {
            "player": p1,
            "settings": settings
        }
        send_datareceived_data = n.send(send_data)
        if p1.number == 1:
            settings = send_datareceived_data["settings"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pygame.Rect(ready_button.rect).collidepoint(pos):
                    p1.ready = True
                elif p1.number == 0:
                    for btn in settings_buttons:
                        if pygame.Rect(btn.rect).collidepoint(pos):
                            settings = process_button_click(btn, settings)

        draw_board(p1, settings, settings_buttons, ready_button)
        if send_datareceived_data["ready"]:
            print("Game starting")
            break

    if p1.number == 0:
        p1.height = settings.p1size
    else:
        p1.height = settings.p2size
    game_loop(p1, n, settings)


def process_button_click(button, settings):
    # There must be a better way for this but for now this will do.
    if button.id == "p1_size+":
        settings.p1size += 10
    elif button.id == "p1_size-":
        settings.p1size -= 10
    elif button.id == "p2_size+":
        settings.p2size += 10
    elif button.id == "p2_size-":
        settings.p2size -= 10
    elif button.id == "p1_vel+":
        settings.p1vel += 1
    elif button.id == "p1_vel-":
        settings.p1vel -= 1
    elif button.id == "p2_vel+":
        settings.p2vel += 1
    elif button.id == "p2_vel-":
        settings.p2vel -= 1
    elif button.id == "x_vel+":
        settings.ballxvel += 1
    elif button.id == "x_vel-":
        settings.ballxvel -= 1
    elif button.id == "y_vel+":
        settings.ballyvel += 1
    elif button.id == "y_vel-":
        settings.ballyvel -= 1
    return settings


def draw_board(p1, settings, settings_buttons, ready_button):
    gameDisplay.fill(black)
    if p1.number == 0:
        settings.draw(gameDisplay, display_width, white, settings_buttons)
    else:
        settings.draw(gameDisplay, display_width, white, [])
    ready_button.draw(gameDisplay)
    pygame.display.update()


main_menu()
pygame.quit()
quit()

import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

from pygame import *
import random


class Snake:
    def __init__(self, clr):
        # posição de partes do corpo da cobra
        self.length = [(200, 200), (210, 200), (220, 200), (220, 200), (220, 200), (220, 200)]
        self.skin = clr  # cor do corpo


class Apple:
    def __init__(self):
        self.surface = image.load("Imagens/applee.png")
        self.position = (300, 300)  # posição inicial


def initscreen():
    while True:
        screen.blit(initBackground, initBackground.get_rect())
        display.flip()

        for events in event.get():
            if events.type == QUIT:
                display.quit()
            elif events.type == KEYDOWN:
                if events.key == K_KP_ENTER:
                    choose_snake()
                elif events.key == K_ESCAPE:
                    display.quit()
            elif events.type == MOUSEBUTTONDOWN:
                m = mouse.get_pos()
                if 115 <= m[0] <= 479 and 398 <= m[1] <= 509:
                    choose_snake()


def choose_snake():
    bite.play()
    screen.blit(snakeColor, snakeColor.get_rect())
    display.flip()

    while True:
        for e in event.get():
            if e.type == MOUSEBUTTONDOWN:
                m = mouse.get_pos()

                if 15 <= m[0] <= 206 and 350 <= m[1] <= 450:
                    c = yellow
                    newgame(c)
                elif 212 <= m[0] <= 384 and 350 <= m[1] <= 450:
                    c = red
                    newgame(c)
                elif 398 <= m[0] <= 597 and 350 <= m[1] <= 450:
                    c = green
                    newgame(c)


def random_position():
    p = random.randint(10, 590)
    return p//10 * 10


def collision(x, y):
    return x[0] == y[0] and x[1] == y[1]


def newgame(clr):
    bite.play()

    yave = Snake(clr)
    apple = Apple()
    direction = 3
    t = 10

    while True:
        clock.tick(t)

        screen.blit(game, game.get_rect())
        screen.blit(apple.surface, apple.position)
        for y in yave.length:
            screen.blit(yave.skin, y)
        display.update()

        # for y in range(1, len(yave.length) -1):
        for y in range(len(yave.length) - 1, 1, -1):
            if collision(yave.length[0], yave.length[y]):
                youlose()

        for events in event.get():
            if events.type == QUIT:
                display.quit()
            elif events.type == KEYDOWN:  # a direção muda de acordo com a tecla pressionada
                if events.key == K_UP and direction != 1:
                    direction = 0
                if events.key == K_DOWN and direction != 0:
                    direction = 1
                if events.key == K_RIGHT and direction != 3:
                    direction = 2
                if events.key == K_LEFT and direction != 2:
                    direction = 3

        if direction == 0:
            # diminuindo o valor do eixo y, a cobra se move para cima
            yave.length[0] = (yave.length[0][0], yave.length[0][1] - 10)

            # condição de parada: se a cobra encostar na borda da tela o jogador perde
            if yave.length[0][1] <= 0:
                break

        if direction == 1:
            # aumenta o y para mover-se para baixo
            yave.length[0] = (yave.length[0][0], yave.length[0][1] + 10)

            if yave.length[0][1] >= 600:
                break

        if direction == 2:
            # aumenta o x para mover-se para direita
            yave.length[0] = (yave.length[0][0] + 10, yave.length[0][1])

            if yave.length[0][0] >= 600:
                break

        if direction == 3:
            # diminui o x para mover-se para esquerda
            yave.length[0] = (yave.length[0][0] - 10, yave.length[0][1])

            if yave.length[0][0] <= 0:
                break

        # se a colisão entre a cabeça da cobra e a maça retornar verdadeiro,
        # a cobra ganha mais uma posição no vetor
        if collision(yave.length[0], apple.position):
            bite.play()
            apple.position = (random_position(), random_position())
            yave.length.append((0, 0))
            t += 1

        for i in range(len(yave.length) - 1, 0, -1):
            yave.length[i] = (yave.length[i-1][0], yave.length[i-1][1])

    youlose()


def youlose():
    screen.blit(lose, lose.get_rect())
    display.update()

    while True:
        for events in event.get():
            if events.type == KEYDOWN and events.key == K_KP_ENTER:
                initscreen()
            elif events.type == MOUSEBUTTONDOWN:
                m = mouse.get_pos()
                if 180 <= m[0] <= 415 and 360 <= m[1] <= 535:
                    initscreen()
            elif events.type == QUIT:
                display.quit()


# carregamento de cores, imagens e sons
yellow = image.load("Imagens/yellowbody.jpg")
red = image.load("Imagens/redbody.jpg")
green = image.load("Imagens/greenbody.jpg")
icon = image.load("Imagens/icon.png")
initBackground = image.load("Imagens/play.gif")
snakeColor = image.load("Imagens/choosesnake.jpg")
lose = image.load("Imagens/gameover.jpg")
game = image.load("Imagens/game.jpg")

# inicia o Display
init()
display.get_active()
screen = display.set_mode([600, 600])
display.set_caption("SNAKE")
display.set_icon(icon)

mixer.music.load("Sons/The Dark World.mp3")
mixer.music.set_volume(0.45)
mixer.music.play(-1)
bite = mixer.Sound("Sons/mord.wav")

clock = time.Clock()

initscreen()

# print("\x1b[8;40;120t") // columns 120, rows 40

import os
import sys
import time
import numpy as np
from colorama import Fore, Back, Style
from game import Game
from sprites import Paddle, Ball, Block
from levels import Levels
from rawterminal import RawTerminal as rt


# game object
game = Game()

# lists of obstacles
paddle = type("", (), {})()
blocks = []
balls = []
powerups = []
obstacles = []
sprites = []


def createBlocks(game_width, level):
    block_arr = getattr(Levels, f"level{level}")(game_width)
    for block in block_arr:
        blocks.append(block)
        sprites.append(block)


def createPaddle(game_width, game_height):
    width = 10
    height = 1

    global paddle
    paddle = Paddle(game_width // 2 - width // 2, game_height - height - 1, width, height, "white", speed=2)
    sprites.append(paddle)


def createBall(paddle):
    width = 2
    height = 1

    ball = Ball(paddle.x + paddle.width // 2 - width // 2, paddle.y - 1, width, height, "cyan")
    balls.append(ball)
    sprites.append(ball)


def checkCollision(ball, sprite_group, sprite_group_type):
    collided_sprites = game.spriteCollide(ball, sprite_group)
    if not collided_sprites:
        return False

    print(collided_sprites, end="")
    if sprite_group_type == "block":
        ball.handleCollision(collided_sprites[0])
        for sprite in collided_sprites:
            sprite.handleCollision()

    return True


def gameloop():
    rt.enableRawMode()
    rt.hideCursor()
    rt.removeKeyboardDelay()

    createPaddle(game.width, game.height)
    createBall(paddle)
    createBlocks(game.width, 1)

    game.printScreen(full=True)

    running = True
    while running:
        # if key has been hit
        if rt.kbhit():
            char = rt.getInputChar()

            # check for events
            if char == 3:
                rt.disableRawMode()
                rt.showCursor()
                rt.resetKeyboardDelay()
                running = False

            # move paddle
            paddle.move(char, game.game_window)

        # move sprites
        for ball in balls:
            ball.move(game.game_window)

        # handle collision
        for ball in balls:
            checkCollision(ball, blocks, "block")

        # update display
        game.updateScreen(sprites)
        game.printScreen()

        # gameloop runs based on FPS
        time.sleep(1 / game.FPS)


gameloop()

# {'BLACK': '\x1b[40m', 'BLUE': '\x1b[44m', 'CYAN': '\x1b[46m', 'GREEN': '\x1b[42m', 'LIGHTBLACK_EX': '\x1b[100m', 'LIGHTBLUE_EX': '\x1b[104m', 'LIGHTCYAN_EX': '\x1b[106m', 'LIGHTGREEN_EX': '\x1b[102m', 'LIGHTMAGENTA_EX': '\x1b[105m', 'LIGHTRED_EX': '\x1b[101m', 'LIGHTWHITE_EX': '\x1b[107m', 'LIGHTYELLOW_EX': '\x1b[103m', 'MAGENTA': '\x1b[45m', 'RED': '\x1b[41m', 'RESET': '\x1b[49m', 'WHITE': '\x1b[47m', 'YELLOW': '\x1b[43m'}

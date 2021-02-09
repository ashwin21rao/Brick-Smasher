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


def createBlocks(game_width, level):
    block_arr = getattr(Levels, f"level{level}")(game_width)
    for block in block_arr:
        blocks.append(block)


def createPaddle(game_width, game_height):
    width = 10
    height = 1

    global paddle
    paddle = Paddle(game_width // 2 - width // 2, game_height - height - 1, width, height, "white", x_speed=2)


def createBall(paddle):
    width = 2
    height = 1

    ball = Ball(paddle.x + paddle.width // 2 - width // 2, paddle.y - 1, width, height, "cyan")
    balls.append(ball)


# WILL BREAK IF BALL SIZE OR DISTANCE BETWEEN BLOCKS IS CHANGED
def handleBlockCollision(ball, block, game_window):
    global blocks
    block.handleCollision(game_window)
    if block.getStrength() < 0:
        blocks = [b for b in blocks if not (b.x == block.x and b.y == block.y)]


def checkBlockCollision(ball, game_window):
    global blocks
    collided_blocks = game.spriteCollide(ball, blocks)
    if not collided_blocks:
        return

    # collision with 3 blocks simultaneously (corner collision)
    if len(collided_blocks) == 3:
        for block in collided_blocks:
            handleBlockCollision(ball, block, game_window)
        ball.reflectHorizontalAndVertical()
        return

    # handle collision with sides (not corners)
    for block in collided_blocks:
        if not ball.checkCornerCollision(block):
            handleBlockCollision(ball, block, game_window)
            ball.handleCollision(block, obstacle="block")
            return

    # handle simultaneous vertical collision with corners of 2 blocks
    if len(collided_blocks) == 2:
        for block in collided_blocks:
            handleBlockCollision(ball, block, game_window)
        ball.reflectVertical()
    else:
        # handle collision with corner of a single block
        block = collided_blocks[0]
        if ball.handleCornerCollision(block):
            handleBlockCollision(ball, block, game_window)
            ball.handleCollision(block, obstacle="block")


def checkPaddleCollision(ball):
    pass


def updateDisplay():
    # update display
    sprites = blocks + balls + [paddle] + powerups
    game.updateScreen(sprites)
    game.printScreen()

    # gameloop runs based on FPS
    time.sleep(1 / game.FPS)


def gameloop():
    rt.enableRawMode()
    rt.hideCursor()
    rt.removeKeyboardDelay()

    createPaddle(game.width, game.height)
    createBall(paddle)
    createBlocks(game.width, 3)

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
            checkBlockCollision(ball, game.game_window)
            ball.handleCollision(paddle, obstacle="paddle")

        # update display based on FPS
        updateDisplay()
        # if not running:
        #     os.system("clear")

gameloop()

# {'BLACK': '\x1b[40m', 'BLUE': '\x1b[44m', 'CYAN': '\x1b[46m', 'GREEN': '\x1b[42m', 'LIGHTBLACK_EX': '\x1b[100m', 'LIGHTBLUE_EX': '\x1b[104m', 'LIGHTCYAN_EX': '\x1b[106m', 'LIGHTGREEN_EX': '\x1b[102m', 'LIGHTMAGENTA_EX': '\x1b[105m', 'LIGHTRED_EX': '\x1b[101m', 'LIGHTWHITE_EX': '\x1b[107m', 'LIGHTYELLOW_EX': '\x1b[103m', 'MAGENTA': '\x1b[45m', 'RED': '\x1b[41m', 'RESET': '\x1b[49m', 'WHITE': '\x1b[47m', 'YELLOW': '\x1b[43m'}

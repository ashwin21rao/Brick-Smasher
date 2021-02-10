# print("\x1b[8;40;120t") // columns 120, rows 40

import os
import sys
import time
import numpy as np
from colorama import Fore, Back, Style
from pygame import mixer
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


# -------------------------------------------------------------------------------------------------------
def createBlocks(game_width, level):
    block_arr = getattr(Levels, f"level{level}")(game_width)
    for block in block_arr:
        blocks.append(block)


def createPaddle(game_width, game_height):
    width = 10
    height = 1

    global paddle
    paddle = Paddle(game_width // 2 - width // 2, game_height - height - 1, width, height, "white")


def createBall(paddle):
    width = 2
    height = 1

    ball = Ball(paddle.x + paddle.width // 2 - width // 2, paddle.y - 1, width, height, "cyan")
    balls.append(ball)


# -------------------------------------------------------------------------------------------------------
def movePaddle(char, game_window, ball, paddle, ball_launched=True):
    movable_sprites = [paddle]
    if not ball_launched:
        movable_sprites.append(ball)

    # check for 'a'/'j' and 'd'/'l' keys
    if char == 97 or char == 106:
        for sprite in movable_sprites:
            sprite.moveLeft(game_window)
    elif char == 100 or char == 108:
        for sprite in movable_sprites:
            sprite.moveRight(game_window)


def launchBall(char, ball, paddle, x_speed=1, y_speed=-1):
    # check for 'w'/'i' key
    if char == 119 or char == 105:
        ball.launch(x_speed, y_speed)
        paddle.setSpeed(2)
        return True

    return False


# -------------------------------------------------------------------------------------------------------
# check collision with block, paddle or wall
def checkCollision(ball, game_window, audio_sounds):
    return checkBlockCollision(ball, game_window, audio_sounds) or \
           ball.handleCollision(paddle, obstacle="paddle") or \
           ball.handleWallCollision(game_window)


# WILL BREAK IF BALL SIZE OR DISTANCE BETWEEN BLOCKS IS CHANGED
def handleBlockCollision(block, game_window, audio_sounds):
    global blocks
    block.handleCollision(game_window, audio_sounds)
    if block.getStrength() < 0:
        blocks.remove(block)
        # blocks = [b for b in blocks if not (b.x == block.x and b.y == block.y)]


def checkBlockCollision(ball, game_window, audio_sounds):
    global blocks
    collided_blocks = game.spriteCollide(ball, blocks)
    if not collided_blocks:
        return False

    # collision with 3 blocks simultaneously (corner collision)
    if len(collided_blocks) == 3:
        for block in collided_blocks:
            handleBlockCollision(block, game_window, audio_sounds)
        ball.reflectHorizontalAndVertical()
        return True

    # handle collision with sides (not corners)
    for block in collided_blocks:
        if not ball.checkCornerCollision(block):
            handleBlockCollision(block, game_window, audio_sounds)
            ball.handleCollision(block, obstacle="block")
            return True

    # handle simultaneous vertical collision with corners of 2 blocks
    if len(collided_blocks) == 2:
        for block in collided_blocks:
            handleBlockCollision(block, game_window, audio_sounds)
        ball.reflectVertical()
        return True

    # handle collision with corner of a single block
    block = collided_blocks[0]
    if ball.handleCornerCollision(block):
        handleBlockCollision(block, game_window, audio_sounds)
        ball.handleCollision(block, obstacle="block")
        return True

    return False


# -------------------------------------------------------------------------------------------------------
def updateDisplay():
    # update display
    sprites = blocks + balls + [paddle] + powerups
    game.updateScreen(sprites)
    game.printScreen()

    # gameloop runs based on FPS
    time.sleep(1 / game.FPS)


def initialSetup():
    rt.enableRawMode()
    rt.hideCursor()
    rt.removeKeyboardDelay()

    # play music
    mixer.init()
    mixer.music.load("extras/background2.wav")
    mixer.music.play(loops=-1)

    brick_sound_1 = mixer.Sound("extras/brick.wav")
    brick_sound_2 = mixer.Sound("extras/indestructible_brick.wav")
    return {"regular_brick_sound": brick_sound_1, "indestructible_brick_sound": brick_sound_2}


def gameloop():
    brick_sounds = initialSetup()

    createPaddle(game.width, game.height)
    createBall(paddle)
    createBlocks(game.width, 1)

    game.printScreen(full=True)

    running = True
    ball_launched = False

    # to decrease speed of ball movement on screen wrt FPS
    ball_speed_coefficient = 4
    move_ball_counter = 0

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

            # move paddle based on keypress
            movePaddle(char, game.game_window, balls[0], paddle, ball_launched)

            # launch ball based on keypress
            if not ball_launched:
                ball_launched = launchBall(char, balls[0], paddle)

        if move_ball_counter == 0 and ball_launched:

            # move balls and check collisions
            for ball in balls:
                for sp in range(0, abs(ball.x_speed) + (ball.x_speed == 0)):
                    ball.move(game.game_window, move_y=not sp)
                    if ball.isDead(game.game_window.shape[0]):
                        balls.remove(ball)
                        break
                    elif checkCollision(ball, game.game_window, brick_sounds):
                        break
                    # time.sleep(0.3)
                    # updateDisplay()

        # update display based on FPS
        updateDisplay()
        move_ball_counter = (move_ball_counter + 1) % ball_speed_coefficient

        # no more balls left
        if not balls:
            running = False


gameloop()

# {'BLACK': '\x1b[40m', 'BLUE': '\x1b[44m', 'CYAN': '\x1b[46m', 'GREEN': '\x1b[42m', 'LIGHTBLACK_EX': '\x1b[100m', 'LIGHTBLUE_EX': '\x1b[104m', 'LIGHTCYAN_EX': '\x1b[106m', 'LIGHTGREEN_EX': '\x1b[102m', 'LIGHTMAGENTA_EX': '\x1b[105m', 'LIGHTRED_EX': '\x1b[101m', 'LIGHTWHITE_EX': '\x1b[107m', 'LIGHTYELLOW_EX': '\x1b[103m', 'MAGENTA': '\x1b[45m', 'RED': '\x1b[41m', 'RESET': '\x1b[49m', 'WHITE': '\x1b[47m', 'YELLOW': '\x1b[43m'}

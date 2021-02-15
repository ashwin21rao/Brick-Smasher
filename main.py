import os
import sys
import time
import random
import numpy as np
from colorama import Fore, Back, Style
from pygame import mixer
from game import Game
from balls import Ball
from paddle import Paddle
from powerups import ExpandPaddle, ShrinkPaddle, ThruBall, FastBall, SlowBall, ExtraLife, MultiplyBalls, PaddleGrab
from levels import Levels
from rawterminal import RawTerminal as rt
import config


# -------------------------------------------------------------------------------------------------------
# game object
game = Game()

# lists of obstacles
paddle = None
blocks = []
balls = []
power_ups = []
obstacles = []

# globals
PowerUpTypes = config.POWER_UP_TYPES.copy()

# to decrease speed of ball and power up movement on screen wrt FPS
ball_speed_coefficient = config.INITIAL_BALL_SPEED_COEFFICIENT
powerup_speed_coefficient = config.INITIAL_POWERUP_SPEED_COEFFICIENT


def log(str):
    f = open("output.txt", "a")
    f.write(str)
    f.close()

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


def createPowerUp(block, PowerUpType):
    width = 2
    height = 1

    power_up = PowerUpType(block.x + block.width // 2, block.y + block.height // 2, width, height)
    power_ups.append(power_up)


# -------------------------------------------------------------------------------------------------------
def movePaddle(char, game_window, balls, paddle):
    movable_sprites = []
    for ball in balls:
        if not ball.launched:
            movable_sprites.append(ball)
    movable_sprites.append(paddle)

    # check for 'a'/'j' and 'd'/'l' keys
    if char == 97 or char == 106:
        if paddle.x > 0:
            for sprite in movable_sprites:
                sprite.moveLeft(game_window, speed=min(paddle.x_speed, paddle.x))
    elif char == 100 or char == 108:
        if paddle.x + paddle.width < game.width:
            for sprite in movable_sprites:
                sprite.moveRight(game_window, speed=min(paddle.x_speed, game.width - (paddle.x + paddle.width)))


def launchBall(char, ball, paddle):
    # check for 'w'/'i' key
    if char == 119 or char == 105:
        ball.launch()
        paddle.setSpeed(2)
        return True

    return False


def activatePowerUp(power_up):
    game.addPowerUpScore()

    if power_up.type == "EXPAND_PADDLE":
        power_up.activate(paddle, game.game_window)
        PowerUpTypes.pop(power_up.type, None)
        if ShrinkPaddle.type not in PowerUpTypes:
            PowerUpTypes[ShrinkPaddle.type] = ShrinkPaddle

        # release grabbed balls if any
        for ball in balls:
            if not ball.launched:
                ball.launch()

    elif power_up.type == "SHRINK_PADDLE":
        power_up.activate(paddle, game.game_window)
        PowerUpTypes.pop(power_up.type, None)
        if ExpandPaddle.type not in PowerUpTypes:
            PowerUpTypes[ExpandPaddle.type] = ExpandPaddle

        # release grabbed balls if any
        for ball in balls:
            if not ball.launched:
                ball.launch()

    elif power_up.type == "THRU_BALL":
        power_up.activate(balls, blocks)
        PowerUpTypes.pop(power_up.type, None)

    elif power_up.type == "FAST_BALL" or power_up.type == "SLOW_BALL":
        global ball_speed_coefficient
        ball_speed_coefficient = power_up.activate(ball_speed_coefficient)

    elif power_up.type == "EXTRA_LIFE":
        game.lives = power_up.activate(game.lives)

    elif power_up.type == "MULTIPLY_BALLS":
        power_up.activate(balls, game.game_window)

        # release grabbed balls if any
        for ball in balls:
            if not ball.launched:
                ball.launch()

    elif power_up.type == "PADDLE_GRAB":
        power_up.activate(balls)
        PowerUpTypes.pop(power_up.type, None)


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
        game.addBlockScore(block.original_color, block.invisible_new_color)
        blocks.remove(block)

    # create power up probabilistically on collision and if score is above threshold
    if game.score > config.POWERUP_SCORE_THRESHOLD:
        if np.random.choice([0, 1], 1, [1 - config.POWERUP_GENERATION_PROBABILITY, config.POWERUP_GENERATION_PROBABILITY])[0]:
            createPowerUp(block, np.random.choice(list(PowerUpTypes.values()), 1, config.POWERUP_PROBABILITIES)[0])


def checkBlockCollision(ball, game_window, audio_sounds):
    global blocks
    collided_blocks = game.spriteCollide(ball, blocks)
    if not collided_blocks:
        return False

    # collision with 3 blocks simultaneously (corner collision)
    if len(collided_blocks) == 3:
        for block in collided_blocks:
            handleBlockCollision(block, game_window, audio_sounds)
        if ball.collidable:
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
        if ball.collidable:
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
    sprites = blocks + power_ups + [paddle] + balls
    game.updateScreen(sprites)

    # print screen
    game.printScreen()
    sys.stdout.flush()

    # gameloop runs based on FPS
    time.sleep(1 / game.FPS)


def renderAndRemove(sprite_list, sprite):
    updateDisplay()
    sprite.clearOldPosition(game.game_window)
    sprite_list.remove(sprite)


def resetPowerUps():
    for block in blocks:
        block.kill_on_collision = False

    global ball_speed_coefficient
    ball_speed_coefficient = config.INITIAL_BALL_SPEED_COEFFICIENT

    global PowerUpTypes
    PowerUpTypes = config.POWER_UP_TYPES.copy()


def respawn(game_window):
    if paddle is not None:
        paddle.clearOldPosition(game_window)

    global power_ups
    resetPowerUps()
    for power_up in power_ups:
        power_up.clearOldPosition(game_window)
    power_ups = []

    createPaddle(game_window.shape[1], game_window.shape[0])
    createBall(paddle)


def advanceLevel(game_window, level):
    global balls, blocks, power_ups
    for block in blocks:
        block.clearOldPosition(game_window)
    for ball in balls:
        ball.clearOldPosition(game_window)
    for power_up in power_ups:
        power_up.clearOldPosition(game_window)

    blocks = []
    balls = []
    power_ups = []

    createBlocks(game.width, level)
    respawn(game_window)


def initialSetup():
    rt.enableRawMode()
    rt.hideCursor()

    # play music
    mixer.init()
    mixer.music.load("extras/background2.wav")
    mixer.music.play(loops=-1)

    return {"regular_brick_sound": mixer.Sound("extras/brick.wav"),
            "indestructible_brick_sound": mixer.Sound("extras/indestructible_brick.wav"),
            "explosive_brick_sound": mixer.Sound("extras/explosive_brick.wav")}


def startGame():
    # initialise settings
    rt.removeKeyboardDelay()

    # reset game timer
    game.startTimer()

    # create sprites
    advanceLevel(game.game_window, 1)

    # render screen
    game.printScreen()
    sys.stdout.flush()


# -------------------------------------------------------------------------------------------------------
def startScreen():
    game.reset()
    game.renderStartScreen()
    game.printScreen(full=True)
    sys.stdout.flush()

    running = True
    while running:

        # if key has been hit
        if rt.kbhit():
            char = rt.getInputChar()

            # check for events
            if char == 3 or char == 113:
                rt.disableRawMode()
                rt.showCursor()
                return False

            # start game
            if char == 10:
                game.clearScreen()
                return True


def endScreen():
    rt.resetKeyboardDelay()
    game.renderEndScreen()
    game.printScreen()
    sys.stdout.flush()

    running = True
    while running:

        # if key has been hit
        if rt.kbhit():
            char = rt.getInputChar()

            # check for events
            if char == 3 or char == 113:
                rt.disableRawMode()
                rt.showCursor()
                return False

            # restart game
            if char == 10:
                return True


def gameloop():
    brick_sounds = initialSetup()

    # to decrease speed of ball and power up movement on screen wrt FPS
    move_ball_counter = 0
    move_powerup_counter = 0

    running = True
    started = False
    done = False
    while running:

        if done:
            if not endScreen():
                break
            started = False
            done = False

        if not started:
            if not startScreen():
                break
            started = True
            startGame()

        # if key has been hit
        if rt.kbhit():
            char = rt.getInputChar()

            # check for events
            if char == 3 or char == 113:
                rt.disableRawMode()
                rt.showCursor()
                rt.resetKeyboardDelay()
                running = False

            # move paddle based on keypress
            movePaddle(char, game.game_window, balls, paddle)

            # launch ball based on keypress
            for ball in balls:
                if not ball.launched:
                    launchBall(char, ball, paddle)

        # move power ups
        if move_powerup_counter == 0:
            for power_up in power_ups:
                power_up.move(game.game_window)
                if power_up.powerUpMissed(game.game_window.shape[0]):
                    renderAndRemove(power_ups, power_up)
                    break
                elif power_up.ready(paddle):
                    activatePowerUp(power_up)
                    renderAndRemove(power_ups, power_up)
                    break

        # move balls and check collisions
        if move_ball_counter == 0:
            for ball in balls:
                if not ball.launched:
                    continue
                for sp in range(0, abs(ball.x_speed) + (ball.x_speed == 0)):
                    ball.move(game.game_window, move_y=not sp)
                    if ball.isDead(game.game_window.shape[0]):
                        renderAndRemove(balls, ball)
                        break
                    elif checkCollision(ball, game.game_window, brick_sounds):
                        break
                    # time.sleep(0.1)
                    # updateDisplay()
                    # sys.stdout.flush()

        # if no more balls left
        if not balls:
            game.decreaseLives()
            if game.lives == 0:
                done = True
                # running = False
            else:
                respawn(game.game_window)
                time.sleep(0.5)

        # check if level is complete
        elif game.levelComplete(blocks):
            game.incrementLevel()
            if game.level <= game.total_levels:
                advanceLevel(game.game_window, game.level)  # go to next level
            else:
                done = True
                # running = False  # all levels done

        # update display based on FPS
        updateDisplay()
        move_ball_counter = (move_ball_counter + 1) % ball_speed_coefficient
        move_powerup_counter = (move_powerup_counter + 1) % powerup_speed_coefficient


gameloop()

# {'BLACK': '\x1b[40m', 'BLUE': '\x1b[44m', 'CYAN': '\x1b[46m', 'GREEN': '\x1b[42m', 'LIGHTBLACK_EX': '\x1b[100m', 'LIGHTBLUE_EX': '\x1b[104m', 'LIGHTCYAN_EX': '\x1b[106m', 'LIGHTGREEN_EX': '\x1b[102m', 'LIGHTMAGENTA_EX': '\x1b[105m', 'LIGHTRED_EX': '\x1b[101m', 'LIGHTWHITE_EX': '\x1b[107m', 'LIGHTYELLOW_EX': '\x1b[103m', 'MAGENTA': '\x1b[45m', 'RED': '\x1b[41m', 'RESET': '\x1b[49m', 'WHITE': '\x1b[47m', 'YELLOW': '\x1b[43m'}

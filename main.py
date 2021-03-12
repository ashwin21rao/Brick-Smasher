import sys
import time
import numpy as np
from datetime import datetime
from pygame import mixer
from game import Game
from balls import Ball
from lasers import Laser
from paddle import Paddle
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
lasers = []

# globals
PowerUpTypes = config.POWER_UP_TYPES.copy()
# activated_power_ups = {}  # power_up -> time of activation


def log(str):
    f = open("output.txt", "a")
    f.write(str)
    f.close()


# -------------------------------------------------------------------------------------------------------
def createBlocks():
    global blocks
    blocks = game.level.getLayout()


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
    if PowerUpType.type == "FAST_BALL" or PowerUpType.type == "SLOW_BALL":
        power_up = PowerUpType(block.x + block.width // 2, block.y + block.height // 2,
                               initial_ball_speed_coefficient=config.INITIAL_BALL_SPEED_COEFFICIENT)
    else:
        power_up = PowerUpType(block.x + block.width // 2, block.y + block.height // 2)
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


def activatePowerUp(power_up, powerup_sound):
    game.addPowerUpScore()
    power_up.playSound(powerup_sound)

    # update activation time of powerup
    # global activated_power_ups
    game.activated_power_ups = {p_up: time for p_up, time in game.activated_power_ups.items() if p_up.type != power_up.type}
    game.activated_power_ups[power_up] = datetime.now()

    if power_up.type == "EXPAND_PADDLE" or power_up.type == "SHRINK_PADDLE":
        power_up.activate(paddle, game.game_window)

        # remove opposite powerup
        game.activated_power_ups = {p_up: time for p_up, time in game.activated_power_ups.items() if
                               p_up.type != ("SHRINK_PADDLE" if power_up.type == "EXPAND_PADDLE" else "EXPAND_PADDLE")}

        # release grabbed balls if any
        for ball in balls:
            if not ball.launched:
                ball.launch()

    elif power_up.type == "THRU_BALL":
        # deactivate fireball powerup
        for p_up in game.activated_power_ups:
            if p_up.type == "FIRE_BALL":
                p_up.deactivate(blocks)
                game.activated_power_ups.pop(p_up, None)
                break

        power_up.activate(balls, blocks)

    elif power_up.type == "FIRE_BALL":
        # deactivate thruball powerup
        for p_up in game.activated_power_ups:
            if p_up.type == "THRU_BALL":
                p_up.deactivate(balls, blocks)
                game.activated_power_ups.pop(p_up, None)
                break

        power_up.activate(blocks)

    elif power_up.type == "FAST_BALL" or power_up.type == "SLOW_BALL":
        opposite_type = "SLOW_BALL" if power_up.type == "FAST_BALL" else "FAST_BALL"

        # deactivate opposite powerup
        for p_up in game.activated_power_ups:
            if p_up.type == opposite_type:
                p_up.deactivate(game)
                game.activated_power_ups.pop(p_up, None)
                break

        power_up.activate(game)

    elif power_up.type == "EXTRA_LIFE":
        power_up.activate(game)

    elif power_up.type == "MULTIPLY_BALLS":
        power_up.activate(balls, game.game_window)

        # release grabbed balls if any
        for ball in balls:
            if not ball.launched:
                ball.launch()

    elif power_up.type == "PADDLE_GRAB":
        power_up.activate(balls)

    elif power_up.type == "SKIP_LEVEL":
        power_up.activate(game)

    elif power_up.type == "SHOOT_LASER":
        power_up.activate(paddle, game.game_window)
        # lasers.extend(power_up.shootLasers(paddle))


def deactivatePowerUps(reset_all=False):
    to_deactivate = [power_up for power_up, time in game.activated_power_ups.items()
                     if power_up.can_deactivate and
                     (reset_all or int((datetime.now() - time).total_seconds()) > config.POWERUP_ACTIVATION_TIME)]

    for power_up in to_deactivate:
        if power_up.type == "FAST_BALL" or power_up.type == "SLOW_BALL":
            power_up.deactivate(game)
        elif power_up.type == "THRU_BALL":
            power_up.deactivate(balls, blocks)
        elif power_up.type == "FIRE_BALL":
            power_up.deactivate(blocks)
        elif power_up.type == "PADDLE_GRAB":
            power_up.deactivate(balls)
        elif power_up.type == "SKIP_LEVEL":
            power_up.deactivate(game)
        elif power_up.type == "SHOOT_LASER":
            power_up.deactivate(paddle, game.game_window)

        game.activated_power_ups.pop(power_up, None)


# -------------------------------------------------------------------------------------------------------
# check collision with block, paddle or wall
def checkCollision(ball, game_window, audio_sounds):
    return checkBlockCollision(ball, game_window, audio_sounds) or \
           checkPaddleCollision(ball, game_window, audio_sounds) or \
           ball.handleWallCollision(game_window, audio_sounds["wall_sound"])


def checkPaddleCollision(ball, game_window, audio_sounds):
    collided = ball.handlePaddleCollision(paddle, audio_sounds["paddle_sound"])
    if collided and game.level.time_attack_activated:
        game.level.timeAttack(game_window, blocks, audio_sounds["falling_brick_sound"])

    return collided


# WILL BREAK IF BALL SIZE OR DISTANCE BETWEEN BLOCKS IS CHANGED
def handleBlockCollision(block, game_window, audio_sounds):
    global blocks
    block.playSound(audio_sounds)

    # handle block collision
    block.handleCollision(game_window, blocks)
    for b in blocks:
        if b.getStrength() < 0:
            game.addBlockScore(b.original_color, b.invisible_new_color)
    blocks = [b for b in blocks if b.getStrength() >= 0]

    # create power up probabilistically on collision and if score is above threshold
    if game.score > config.POWERUP_SCORE_THRESHOLD:
        if np.random.choice([0, 1],
                            p=[1 - config.POWERUP_GENERATION_PROBABILITY, config.POWERUP_GENERATION_PROBABILITY]):
            createPowerUp(block, np.random.choice(list(PowerUpTypes.values()), p=config.POWERUP_PROBABILITIES))
            # createPowerUp(block, random.choice(list(PowerUpTypes.values())))


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
            ball.handleBlockCollision(block)
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
        ball.handleBlockCollision(block)
        return True

    return False


def checkLaserHit(laser, audio_sounds):
    hit = False

    for block in blocks:
        if laser.hitBlock(block):
            handleBlockCollision(block, game.game_window, audio_sounds)
            hit = True

    return hit


# -------------------------------------------------------------------------------------------------------
def updateDisplay():
    # update display
    sprites = blocks + lasers + power_ups + [paddle] + balls
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


def respawn(game_window):
    global power_ups, lasers
    # global activated_power_ups
    deactivatePowerUps(reset_all=True)
    for power_up in power_ups:
        power_up.clearOldPosition(game_window)

    power_ups = []
    game.activated_power_ups = {}

    for laser in lasers:
        laser.clearOldPosition(game_window)
    lasers = []

    if paddle is not None:
        paddle.clearOldPosition(game_window)
    createPaddle(game_window.shape[1], game_window.shape[0])
    createBall(paddle)


def advanceLevel(game_window):
    global balls, blocks, lasers
    for block in blocks:
        block.clearOldPosition(game_window)
    for ball in balls:
        ball.clearOldPosition(game_window)

    blocks = []
    balls = []

    respawn(game_window)
    createBlocks()


def initialSetup():
    rt.enableRawMode()
    rt.hideCursor()

    # play music
    mixer.init()
    mixer.music.load(config.BACKGROUND_MUSIC)
    mixer.music.play(loops=-1)

    return {"regular_brick_sound": mixer.Sound(config.REGULAR_BRICK_SOUND),
            "indestructible_brick_sound": mixer.Sound(config.INDESTRUCTIBLE_BRICK_SOUND),
            "explosive_brick_sound": mixer.Sound(config.EXPLOSIVE_BRICK_SOUND),
            "invisible_brick_sound": mixer.Sound(config.INVISIBLE_BRICK_SOUND),
            "falling_brick_sound": mixer.Sound(config.FALLING_BRICK_SOUND),
            "activate_powerup_sound": mixer.Sound(config.ACTIVATE_POWERUP_SOUND),
            "paddle_sound": mixer.Sound(config.PADDLE_SOUND),
            "wall_sound": mixer.Sound(config.WALL_SOUND),
            "thru_ball_sound": mixer.Sound(config.THRU_BALL_SOUND),
            "laser_sound": mixer.Sound(config.LASER_SOUND)}


def startGame():
    # initialise settings
    rt.removeKeyboardDelay()

    # reset game timer
    game.startTimer()

    # create sprites
    advanceLevel(game.game_window)

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
    game_sounds = initialSetup()

    # to decrease speed of ball, power up and laser movement on screen wrt FPS
    move_ball_counter = 0
    move_powerup_counter = 0
    move_laser_counter = 0

    # delay laser shots
    shoot_laser_counter = 0

    # to decrease rate of change of color of rainbow bricks
    change_rainbow_brick_color_counter = 0

    running = True
    started = False
    done = False
    while running:

        # show end screen
        if done:
            if not endScreen():
                break
            started = False
            done = False

        # show start screen
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

            elif char == 32:
                game.skip_level = True

            # move paddle based on keypress
            movePaddle(char, game.game_window, balls, paddle)

            # launch ball based on keypress
            for ball in balls:
                if not ball.launched:
                    launchBall(char, ball, paddle)

        # change color of rainbow bricks
        if change_rainbow_brick_color_counter == 0:
            for block in blocks:
                if block.type == "RAINBOW_BLOCK":
                    block.changeColor()

        # activate time attack
        if not game.level.time_attack_activated:
            if int((datetime.now() - game.level.start_time).total_seconds()) > \
                    game.time_before_time_attack[game.level.level_num-1]:
                game.level.activateTimeAttack()

        # move power ups
        if move_powerup_counter == 0:
            for power_up in power_ups:
                power_up.move(game.game_window)
                if power_up.powerUpMissed(game.game_window.shape[0]):
                    renderAndRemove(power_ups, power_up)
                    break
                elif power_up.ready(paddle):
                    activatePowerUp(power_up, game_sounds["activate_powerup_sound"])
                    renderAndRemove(power_ups, power_up)
                    break

            # deactivate power ups if its time of activation is finished
            deactivatePowerUps()

        # move lasers and check collision
        if move_laser_counter == 0:
            for laser in lasers:
                laser.move(game.game_window)
                if laser.laserMissed():
                    renderAndRemove(lasers, laser)
                    break
                elif checkLaserHit(laser, game_sounds):
                    renderAndRemove(lasers, laser)
                    break

        # shoot lasers if activated
        if shoot_laser_counter == 0:
            for power_up in game.activated_power_ups:
                if power_up.type == "SHOOT_LASER":
                    lasers.extend(power_up.shootLasers(paddle, game_sounds["laser_sound"]))
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
                    elif checkCollision(ball, game.game_window, game_sounds):
                        break
                    # time.sleep(0.1)
                    # updateDisplay()
                    # sys.stdout.flush()

        # if no more balls left
        if not balls:
            game.decreaseLives()
            if game.lives == 0:
                done = True
            else:
                respawn(game.game_window)
                time.sleep(0.5)

        # if blocks reached paddle (time attack)
        for block in blocks:
            if block.y + block.height == paddle.y:
                done = True

        # check if level is complete
        if game.levelComplete(blocks) or game.skip_level:
            if game.level.level_num + 1 <= game.total_levels:
                game.incrementLevel()
                advanceLevel(game.game_window)  # go to next level
            else:
                game.won = True
                done = True  # all levels done

        # update display based on FPS
        updateDisplay()
        move_ball_counter = (move_ball_counter + 1) % game.ball_speed_coefficient
        move_powerup_counter = (move_powerup_counter + 1) % game.powerup_speed_coefficient
        move_laser_counter = (move_laser_counter + 1) % game.laser_speed_coefficient
        change_rainbow_brick_color_counter = (change_rainbow_brick_color_counter + 1) % game.rainbow_brick_color_speed_coefficient
        shoot_laser_counter = (shoot_laser_counter + 1) % game.time_between_laser_shots

gameloop()

import sys
from datetime import datetime
import numpy as np
import config
from rawterminal import RawTerminal as rt
from screen import Screen
from levels import Level
from balls import Ball
from paddle import Paddle
from ufo import Ufo
from pygame import mixer


class Game:
    def __init__(self, width=config.DEFAULT_WINDOW_WIDTH, height=config.DEFAULT_WINDOW_HEIGHT):
        self.screen = Screen(width, height)
        self.game_window = self.screen.game_window
        self.width = self.screen.width
        self.height = self.screen.height

        self.FPS = config.FPS
        self.total_levels = config.TOTAL_LEVELS
        self.PowerUpTypes = config.POWER_UP_TYPES

        self.ball_speed_coefficient = config.INITIAL_BALL_SPEED_COEFFICIENT
        self.powerup_speed_coefficient = config.POWERUP_SPEED_COEFFICIENT
        self.laser_speed_coefficient = config.LASER_SPEED_COEFFICIENT
        self.bomb_speed_coefficient = config.BOMB_SPEED_COEFFICIENT
        self.rainbow_brick_color_speed_coefficient = config.RAINBOW_BRICK_COLOR_SPEED_COEFFICIENT
        self.time_between_laser_shots = config.TIME_BETWEEN_LASER_SHOTS
        self.time_before_time_attack = config.TIME_BEFORE_TIME_ATTACK
        self.time_between_bomb_drops = config.TIME_BETWEEN_BOMB_DROPS

        mixer.init()
        self.sounds = {"regular_brick_sound": mixer.Sound(config.REGULAR_BRICK_SOUND),
                       "indestructible_brick_sound": mixer.Sound(config.INDESTRUCTIBLE_BRICK_SOUND),
                       "explosive_brick_sound": mixer.Sound(config.EXPLOSIVE_BRICK_SOUND),
                       "invisible_brick_sound": mixer.Sound(config.INVISIBLE_BRICK_SOUND),
                       "falling_brick_sound": mixer.Sound(config.FALLING_BRICK_SOUND),
                       "activate_powerup_sound": mixer.Sound(config.ACTIVATE_POWERUP_SOUND),
                       "paddle_sound": mixer.Sound(config.PADDLE_SOUND),
                       "wall_sound": mixer.Sound(config.WALL_SOUND),
                       "thru_ball_sound": mixer.Sound(config.THRU_BALL_SOUND),
                       "laser_sound": mixer.Sound(config.LASER_SOUND),
                       "paddle_grab_sound": mixer.Sound(config.PADDLE_GRAB_SOUND)}

        self.reset()

    def reset(self):
        self.level = Level(self.width, 5)
        self.lives = config.TOTAL_LIVES
        self.score = 0
        self.start_time = None
        self.ticks = 0
        self.won = False
        self.skip_level = False
        self.boss_level_activated = False

        self.activated_power_ups = {}  # power_up -> time of activation
        self.blocks = []
        self.paddle = None
        self.balls = []
        self.power_ups = []
        self.lasers = []
        self.ufo = None
        self.bombs = []

        self.time_between_bomb_drops = config.TIME_BETWEEN_BOMB_DROPS

        # play music
        self.playBackgroundMusic(config.BACKGROUND_MUSIC)

    def startTimer(self):
        self.start_time = datetime.now()
        self.ticks = 0

    def tick(self):
        self.ticks = int((datetime.now() - self.start_time).total_seconds())

    def printScreen(self, full=False):
        self.screen.printScreen(self.ticks, self.score, self.level.level_num, self.lives, full=full)

    def updateScreen(self):
        sprite_list = self.balls + self.blocks + self.lasers + self.power_ups + [self.paddle]
        if self.boss_level_activated:
            sprite_list = [self.ufo] + self.bombs + sprite_list

        self.screen.updateScreen(sprite_list)

    def clearScreen(self):
        self.screen.clearScreen()

    def renderStartScreen(self):
        self.screen.renderStartScreen()

    def renderEndScreen(self):
        self.screen.renderEndScreen(self.won, self.score, self.ticks)

    # check collision between 2 sprites
    def collideRect(self, sprite1, sprite2):
        return (sprite1.hitbox.x + sprite1.hitbox.width >= sprite2.hitbox.x and
                sprite1.hitbox.x <= sprite2.hitbox.x + sprite2.hitbox.width) and \
               (sprite1.hitbox.y + sprite1.hitbox.height >= sprite2.hitbox.y and
                sprite1.hitbox.y <= sprite2.hitbox.y + sprite2.hitbox.height)

    # check collision between a sprite and a sprite group and return all collided sprites
    def spriteCollide(self, sprite, sprite_group):
        collided_sprites = []
        for sp in sprite_group:
            if self.collideRect(sprite, sp):
                collided_sprites.append(sp)

        return collided_sprites

    # check collision between a sprite and a sprite group and return first collided sprite
    def spriteCollideAny(self, sprite, sprite_group):
        for sp in sprite_group:
            if self.collideRect(sprite, sp):
                return sp

        return None

    def addBlockScore(self, block_color, invisible_new_color):
        if block_color == "green":
            self.score += 10
        elif block_color == "yellow":
            self.score += 20
        elif block_color == "red":
            self.score += 30
        elif block_color == "blue" or block_color == "magenta":
            self.score += 5
        elif block_color is None:
            self.addBlockScore(invisible_new_color, None)
            self.score += 10

    def addPowerUpScore(self):
        self.score += 20

    def decreaseLives(self):
        self.lives -= 1

    def incrementLevel(self):
        if self.level.level_num + 1 == self.total_levels:
            self.boss_level_activated = True
            # play music
            self.playBackgroundMusic(config.BOSS_BACKGROUND_MUSIC)

        self.level = Level(self.width, self.level.level_num + 1)

    def levelComplete(self, blocks):
        if self.boss_level_activated:
            return self.ufo.lives == 0

        for block in blocks:
            if block.color != "blue":
                return False
        return True

    # -------------------------------- new methods -------------------------------------
    def createBlocks(self):
        self.blocks = self.level.getBlocks()

    def createPaddle(self):
        width = 10
        height = 1

        self.paddle = Paddle(self.width // 2 - width // 2, self.height - height - 1, width, height, "white")

    def createBall(self):
        width = 2
        height = 1

        ball = Ball(self.paddle.x + self.paddle.width // 2 - width // 2, self.paddle.y - 1, width, height, "cyan")
        self.balls.append(ball)

    def createPowerUp(self, block, PowerUpType):
        if PowerUpType.type == "FAST_BALL" or PowerUpType.type == "SLOW_BALL":
            power_up = PowerUpType(block.x + block.width // 2, block.y + block.height - 1,
                                   initial_ball_speed_coefficient=config.INITIAL_BALL_SPEED_COEFFICIENT)
        else:
            power_up = PowerUpType(block.x + block.width // 2, block.y + block.height - 1)

        self.power_ups.append(power_up)

    def createUfo(self):
        self.ufo = Ufo(0, 1)
        self.ufo.updatePosition(x=(self.width // 2 - self.ufo.width // 2))

    # ----------------------------------- misc -----------------------------------

    def movePaddle(self, char):
        movable_sprites = []
        for ball in self.balls:
            if not ball.launched:
                movable_sprites.append(ball)

        if self.boss_level_activated:
            movable_sprites.append(self.ufo)

        movable_sprites.append(self.paddle)

        # check for 'a'/'j' and 'd'/'l' keys
        if char == 97 or char == 106:
            if self.paddle.x > 0:
                for sprite in movable_sprites:
                    sprite.moveLeft(self.game_window, speed=min(self.paddle.x_speed, self.paddle.x))
        elif char == 100 or char == 108:
            if self.paddle.x + self.paddle.width < self.width:
                for sprite in movable_sprites:
                    sprite.moveRight(self.game_window,
                                     speed=min(self.paddle.x_speed, self.width - (self.paddle.x + self.paddle.width)))

    def launchBall(self, char, ball):
        # check for 'w'/'i' key
        if char == 119 or char == 105:
            ball.launch()
            self.paddle.setSpeed(2)
            return True

        return False

    def checkLaserHit(self, laser):
        hit = False

        for block in self.blocks:
            if laser.hitBlock(block):
                self.handleBlockCollision(block, spawn_powerup=False)
                hit = True

        return hit

    # ---------------------------------------- activate/deactivate powerups --------------------------

    def activatePowerUp(self, power_up):
        self.addPowerUpScore()
        power_up.playSound(self.sounds["activate_powerup_sound"])

        # update activation time of powerup
        self.activated_power_ups = {p_up: time for p_up, time in self.activated_power_ups.items() if
                                    p_up.type != power_up.type}
        self.activated_power_ups[power_up] = datetime.now()

        if power_up.type == "EXPAND_PADDLE" or power_up.type == "SHRINK_PADDLE":
            power_up.activate(self.paddle, self.game_window)

            # remove opposite powerup
            self.activated_power_ups = {p_up: time for p_up, time in self.activated_power_ups.items() if
                                        p_up.type != (
                                            "SHRINK_PADDLE" if power_up.type == "EXPAND_PADDLE" else "EXPAND_PADDLE")}

            # release grabbed balls if any
            for ball in self.balls:
                if not ball.launched:
                    ball.launch()

        elif power_up.type == "THRU_BALL":
            # deactivate fireball powerup
            for p_up in self.activated_power_ups:
                if p_up.type == "FIRE_BALL":
                    p_up.deactivate(self.blocks)
                    self.activated_power_ups.pop(p_up, None)
                    break

            power_up.activate(self.balls, self.blocks)

        elif power_up.type == "FIRE_BALL":
            # deactivate thruball powerup
            for p_up in self.activated_power_ups:
                if p_up.type == "THRU_BALL":
                    p_up.deactivate(self.balls, self.blocks)
                    self.activated_power_ups.pop(p_up, None)
                    break

            # deactivate explosive ball powerup
            for p_up in self.activated_power_ups:
                if p_up.type == "EXPLOSIVE_BALL":
                    p_up.deactivate(self.blocks)
                    self.activated_power_ups.pop(p_up, None)
                    break

            power_up.activate(self.blocks)

        elif power_up.type == "EXPLOSIVE_BALL":
            # deactivate fireball powerup
            for p_up in self.activated_power_ups:
                if p_up.type == "FIRE_BALL":
                    p_up.deactivate(self.blocks)
                    self.activated_power_ups.pop(p_up, None)
                    break

            power_up.activate(self.blocks)

        elif power_up.type == "FAST_BALL" or power_up.type == "SLOW_BALL":
            opposite_type = "SLOW_BALL" if power_up.type == "FAST_BALL" else "FAST_BALL"

            # deactivate opposite powerup
            for p_up in self.activated_power_ups:
                if p_up.type == opposite_type:
                    p_up.deactivate(self)
                    self.activated_power_ups.pop(p_up, None)
                    break

            power_up.activate(self)

        elif power_up.type == "EXTRA_LIFE" or power_up.type == "LOSE_LIFE":
            power_up.activate(self)

        elif power_up.type == "MULTIPLY_BALLS":
            power_up.activate(self.balls, self.game_window)

            # release grabbed balls if any
            for ball in self.balls:
                if not ball.launched:
                    ball.launch()

        elif power_up.type == "PADDLE_GRAB":
            power_up.activate(self.balls)

        elif power_up.type == "SKIP_LEVEL":
            power_up.activate(self)

        elif power_up.type == "SHOOT_LASER":
            power_up.activate(self.paddle, self.game_window)

    def deactivatePowerUps(self, reset_all=False):
        to_deactivate = [power_up for power_up, time in self.activated_power_ups.items()
                         if power_up.can_deactivate and
                         (reset_all or int((datetime.now() - time).total_seconds()) > config.POWERUP_ACTIVATION_TIME)]

        for power_up in to_deactivate:
            if power_up.type == "FAST_BALL" or power_up.type == "SLOW_BALL":
                power_up.deactivate(self)
            elif power_up.type == "THRU_BALL":
                power_up.deactivate(self.balls, self.blocks)
            elif power_up.type == "FIRE_BALL" or power_up.type == "EXPLOSIVE_BALL":
                power_up.deactivate(self.blocks)
            elif power_up.type == "PADDLE_GRAB":
                power_up.deactivate(self.balls)
            elif power_up.type == "SKIP_LEVEL":
                power_up.deactivate(self)
            elif power_up.type == "SHOOT_LASER":
                power_up.deactivate(self.paddle, self.game_window)

            self.activated_power_ups.pop(power_up, None)

    def spawnPowerUp(self, block):
        # create power up probabilistically on collision and if score is above threshold
        if self.score > config.POWERUP_SCORE_THRESHOLD:
            if np.random.choice([0, 1],
                                p=[1 - config.POWERUP_GENERATION_PROBABILITY, config.POWERUP_GENERATION_PROBABILITY]):
                self.createPowerUp(block,
                                   np.random.choice(list(self.PowerUpTypes.values()), p=config.POWERUP_PROBABILITIES))


    # ----------------------------------- collision helpers -----------------------------------

    def checkCollision(self, ball):
        return self.checkBlockCollision(ball) or \
               self.checkPaddleCollision(ball) or \
               ball.handleWallCollision(self.game_window, self.sounds["wall_sound"]) or \
               self.checkUfoCollision(ball)

    def checkPaddleCollision(self, ball):
        collided = ball.handlePaddleCollision(self.paddle, {"paddle_bounce_sound": self.sounds["paddle_sound"],
                                                            "paddle_grab_sound": self.sounds["paddle_grab_sound"]})
        if collided and self.level.time_attack_activated and self.blocks:
            self.level.timeAttack(self.game_window, self.blocks, self.sounds["falling_brick_sound"])

        return collided

    def handleBlockCollision(self, block, spawn_powerup=True):
        block.playSound(self.sounds)

        # handle block collision
        block.handleCollision(self.game_window, self.blocks)
        for b in self.blocks:
            if b.getStrength() < 0:
                self.addBlockScore(b.original_color, b.invisible_new_color)
        self.blocks = [b for b in self.blocks if b.getStrength() >= 0]

        if spawn_powerup and block.spawn_powerup:
            self.spawnPowerUp(block)

    def checkBlockCollision(self, ball):
        collided_blocks = self.spriteCollide(ball, self.blocks)
        if not collided_blocks:
            return False

        # remove blocks for which collisions from above are disabled if ball is moving down
        collided_blocks = [block for block in collided_blocks
                           if not (block.disable_collision_from_above and ball.y_speed > 0)]
        if not collided_blocks:
            return False

        # collision with 3 blocks simultaneously (corner collision)
        if len(collided_blocks) == 3:
            for block in collided_blocks:
                self.handleBlockCollision(block)
            if ball.collidable:
                ball.reflectHorizontalAndVertical()
            return True

        # handle collision with sides (not corners)
        for block in collided_blocks:
            if not ball.checkCornerCollision(block):
                self.handleBlockCollision(block)
                ball.handleBlockCollision(block)
                return True

        # handle simultaneous vertical collision with corners of 2 blocks
        if len(collided_blocks) == 2:
            for block in collided_blocks:
                self.handleBlockCollision(block)
            if ball.collidable:
                ball.reflectVertical()
            return True

        # handle collision with corner of a single block
        block = collided_blocks[0]
        if ball.handleCornerCollision(block):
            self.handleBlockCollision(block)
            ball.handleBlockCollision(block)
            return True

        return False

    # ------------------------------------------ resetting functions ----------------------------------

    def playBackgroundMusic(self, music):
        mixer.music.load(music)
        mixer.music.play(loops=-1)

    def init(self):
        rt.enableRawMode()
        rt.hideCursor()

    def renderAndRemove(self, sprite_list, sprite):
        self.updateDisplay()
        sprite.clearOldPosition(self.game_window)
        sprite_list.remove(sprite)

    def respawn(self):
        self.deactivatePowerUps(reset_all=True)
        for power_up in self.power_ups:
            power_up.clearOldPosition(self.game_window)

        self.power_ups = []
        self.activated_power_ups = {}

        for bomb in self.bombs:
            bomb.clearOldPosition(self.game_window)
        self.bombs = []

        for laser in self.lasers:
            laser.clearOldPosition(self.game_window)
        self.lasers = []

        if self.paddle is not None:
            self.paddle.clearOldPosition(self.game_window)
        self.createPaddle()
        self.createBall()

        # boss level
        if self.boss_level_activated:
            if self.ufo is not None:
                self.ufo.clearOldPosition(self.game_window)
                self.ufo.updatePosition(x=(self.width // 2 - self.ufo.width // 2))
            else:
                self.createUfo()

    def advanceLevel(self):
        for block in self.blocks:
            block.clearOldPosition(self.game_window)
        for ball in self.balls:
            ball.clearOldPosition(self.game_window)

        self.blocks = []
        self.balls = []

        self.respawn()
        self.createBlocks()

    def restart(self):
        # initialise settings
        rt.removeKeyboardDelay()

        # reset game timer
        self.startTimer()

        # create sprites
        self.advanceLevel()

        # render screen
        self.updateDisplay()
        # self.printScreen()
        # sys.stdout.flush()

    # --------------------------- update display ------------------------------

    def updateDisplay(self):
        # update timer
        self.tick()

        # update display
        self.updateScreen()

        # print screen
        self.printScreen()
        sys.stdout.flush()

    # ------------------------ boss level --------------------------------------

    def checkUfoCollision(self, ball):
        collided = self.boss_level_activated and ball.handleUfoCollision(self.ufo)
        if collided:
            self.ufo.handleCollision(self.sounds["explosive_brick_sound"])
            self.addUfoScore()

            if self.ufo.spawn_powerup:
                self.spawnPowerUp(self.ufo)

            self.ufo.increaseBombDropFrequency(self)
            self.blocks.extend(self.ufo.spawnProtectiveBlocks(self.width))

        return collided

    def createBomb(self):
        bomb = self.PowerUpTypes["LOSE_LIFE"](self.paddle.x + self.paddle.width // 2, self.ufo.y + self.ufo.height - 1, color="red")
        self.bombs.append(bomb)

    def addUfoScore(self):
        self.score += 100

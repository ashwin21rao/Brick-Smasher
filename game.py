from datetime import datetime
import config
from screen import Screen
from levels import Level
from balls import Ball
from paddle import Paddle


class Game:
    def __init__(self, width=config.DEFAULT_WINDOW_WIDTH, height=config.DEFAULT_WINDOW_HEIGHT):
        self.screen = Screen(width, height)
        self.game_window = self.screen.game_window
        self.width = self.screen.width
        self.height = self.screen.height

        self.FPS = config.FPS
        self.total_levels = config.TOTAL_LEVELS
        self.PowerUpTypes = config.POWER_UP_TYPES
        self.reset()

        self.ball_speed_coefficient = config.INITIAL_BALL_SPEED_COEFFICIENT
        self.powerup_speed_coefficient = config.POWERUP_SPEED_COEFFICIENT
        self.laser_speed_coefficient = config.LASER_SPEED_COEFFICIENT
        self.rainbow_brick_color_speed_coefficient = config.RAINBOW_BRICK_COLOR_SPEED_COEFFICIENT
        self.time_between_laser_shots = config.TIME_BETWEEN_LASER_SHOTS
        self.time_before_time_attack = config.TIME_BEFORE_TIME_ATTACK

    def reset(self):
        self.level = Level(self.screen.width, 1)
        self.lives = config.TOTAL_LIVES
        self.score = 0
        self.start_time = None
        self.ticks = 0
        self.won = False
        self.skip_level = False

        self.activated_power_ups = {}  # power_up -> time of activation
        self.blocks = []
        self.paddle = None
        self.balls = []
        self.power_ups = []
        self.lasers = []

    def startTimer(self):
        self.start_time = datetime.now()
        self.ticks = 0

    def tick(self):
        self.ticks = int((datetime.now() - self.start_time).total_seconds())

    def printScreen(self, full=False):
        self.screen.printScreen(self.ticks, self.score, self.level.level_num, self.lives, full=full)

    def updateScreen(self, sprite_list):
        self.screen.updateScreen(sprite_list)

    def clearScreen(self):
        self.screen.clearScreen()

    def renderStartScreen(self):
        self.screen.renderStartScreen()

    def renderEndScreen(self):
        self.screen.renderEndScreen(self.won, self.score, self.ticks)

    # check collision between 2 sprites
    def collideRect(self, sprite1, sprite2):
        return (sprite1.hitbox.x + sprite1.hitbox.width >= sprite2.hitbox.x and sprite1.hitbox.x <= sprite2.hitbox.x + sprite2.hitbox.width) and \
               (sprite1.hitbox.y + sprite1.hitbox.height >= sprite2.hitbox.y and sprite1.hitbox.y <= sprite2.hitbox.y + sprite2.hitbox.height)

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
        self.level = Level(self.screen.width, self.level.level_num + 1)

    def levelComplete(self, blocks):
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

    def createBall(self, paddle):
        width = 2
        height = 1

        ball = Ball(paddle.x + paddle.width // 2 - width // 2, paddle.y - 1, width, height, "cyan")
        self.balls.append(ball)

    def createPowerUp(self, block, PowerUpType):
        if PowerUpType.type == "FAST_BALL" or PowerUpType.type == "SLOW_BALL":
            power_up = PowerUpType(block.x + block.width // 2, block.y + block.height // 2,
                                   initial_ball_speed_coefficient=config.INITIAL_BALL_SPEED_COEFFICIENT)
        else:
            power_up = PowerUpType(block.x + block.width // 2, block.y + block.height // 2)

        self.power_ups.append(power_up)

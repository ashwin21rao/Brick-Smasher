from sprites import Sprite, SpriteCollisionMixin
from lasers import Laser
import copy
from colorama import Fore, Style
import numpy as np


class PowerUp(Sprite, SpriteCollisionMixin):
    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.y_speed = y_speed

    def initArray(self, powerup_text):
        self.array = np.array([list(powerup_text)], dtype=object)

        if self.color is not None:
            self.array[:, 0] = Style.BRIGHT + Fore.__getattribute__(self.color.upper()) + self.array[:, 0]
            self.array[:, self.width-1] = self.array[:, self.width-1] + Fore.RESET + Style.NORMAL

    def move(self, game_window):
        # clear old position
        self.clearOldPosition(game_window)

        # move power up
        self.updatePosition(y=(self.y + self.y_speed))

    def ready(self, paddle):
        return self.checkHorizontalCollision(paddle)

    def powerUpMissed(self, game_height):
        return self.y + self.height >= game_height

    def playSound(self, powerup_sound):
        powerup_sound.play()


class ExpandPaddle(PowerUp):
    type = "EXPAND_PADDLE"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        # self.render = partial(super().render, powerup_text="EP")
        self.initArray("EP")
        self.can_deactivate = False

    def activate(self, paddle, game_window):
        paddle.expand(game_window)


class ShrinkPaddle(PowerUp):
    type = "SHRINK_PADDLE"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        # self.render = partial(super().render, powerup_text="SP")
        self.initArray("SP")
        self.can_deactivate = False

    def activate(self, paddle, game_window):
        paddle.shrink(game_window)


class ThruBall(PowerUp):
    type = "THRU_BALL"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        # self.render = partial(super().render, powerup_text="TB")
        self.initArray("TB")
        self.can_deactivate = True

    def activate(self, balls, blocks):
        for ball in balls:
            ball.disableCollision()
        for block in blocks:
            block.killOnCollision()

    def deactivate(self, balls, blocks):
        for ball in balls:
            ball.collidable = True
        for block in blocks:
            block.kill_on_collision = False


class FireBall(PowerUp):
    type = "FIRE_BALL"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        # self.render = partial(super().render, powerup_text="FI")
        self.initArray("FI")
        self.can_deactivate = True

    def activate(self, blocks):
        for block in blocks:
            block.killOnCollision()

    def deactivate(self, blocks):
        for block in blocks:
            block.kill_on_collision = False


class ExplosiveBall(PowerUp):
    type = "EXPLOSIVE_BALL"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        # self.render = partial(super().render, powerup_text="FI")
        self.initArray("EX")
        self.can_deactivate = True

    def activate(self, blocks):
        for block in blocks:
            block.explodeOnCollision()

    def deactivate(self, blocks):
        for block in blocks:
            if block.type != "EXPLOSIVE_BLOCK":
                block.explode_on_collision = False


class FastBall(PowerUp):
    type = "FAST_BALL"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1,
                 initial_ball_speed_coefficient=3):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.speed_multiplier = 1
        # self.render = partial(super().render, powerup_text="FB")
        self.initArray("FB")
        self.can_deactivate = True
        self.initial_ball_speed_coefficient = initial_ball_speed_coefficient

    def activate(self, game):
        game.ball_speed_coefficient = game.ball_speed_coefficient - self.speed_multiplier \
                                      if game.ball_speed_coefficient - self.speed_multiplier > 0 else 1

    def deactivate(self, game):
        game.ball_speed_coefficient = self.initial_ball_speed_coefficient


class SlowBall(PowerUp):
    type = "SLOW_BALL"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1,
                 initial_ball_speed_coefficient=3):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.speed_multiplier = 1
        # self.render = partial(super().render, powerup_text="SB")
        self.initArray("SB")
        self.can_deactivate = True
        self.initial_ball_speed_coefficient = initial_ball_speed_coefficient

    def activate(self, game):
        game.ball_speed_coefficient += self.speed_multiplier

    def deactivate(self, game):
        game.ball_speed_coefficient = self.initial_ball_speed_coefficient


class ExtraLife(PowerUp):
    type = "EXTRA_LIFE"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.life_multiplier = 1
        # self.render = partial(super().render, powerup_text="XL")
        self.initArray("XL")
        self.can_deactivate = False

    def activate(self, game):
        game.lives += self.life_multiplier


class LoseLife(PowerUp):
    type = "LOSE_LIFE"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.life_multiplier = 1
        # self.render = partial(super().render, powerup_text="XL")
        self.initArray("LL")
        self.can_deactivate = False

    def activate(self, game):
        game.lives -= self.life_multiplier


class MultiplyBalls(PowerUp):
    type = "MULTIPLY_BALLS"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.life_multiplier = 1
        # self.render = partial(super().render, powerup_text="MB")
        self.initArray("MB")
        self.can_deactivate = False

    def activate(self, balls, game_window):
        new_balls = []
        for ball in balls:
            new_ball = copy.deepcopy(ball)
            new_ball.reflectVertical()

            new_ball.handleWallCollision(game_window)
            if ball.x_speed == new_ball.x_speed:
                new_ball.reflectHorizontal()

            new_balls.append(new_ball)

        balls.extend(new_balls)


class PaddleGrab(PowerUp):
    type = "PADDLE_GRAB"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.life_multiplier = 1
        # self.render = partial(super().render, powerup_text="PG")
        self.initArray("PG")
        self.can_deactivate = True

    def activate(self, balls):
        for ball in balls:
            ball.enable_paddle_grab = True

    def deactivate(self, balls):
        for ball in balls:
            ball.enable_paddle_grab = False
            if not ball.launched:
                ball.launch()


class SkipLevel(PowerUp):
    type = "SKIP_LEVEL"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.life_multiplier = 1
        # self.render = partial(super().render, powerup_text="SK")
        self.initArray("SK")
        self.can_deactivate = True

    def activate(self, game):
        game.skip_level = True

    def deactivate(self, game):
        game.skip_level = False


class ShootLaser(PowerUp):
    type = "SHOOT_LASER"

    def __init__(self, x_coordinate, y_coordinate, width=2, height=1, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        # self.render = partial(super().render, powerup_text="SK")
        self.initArray("SL")
        self.can_deactivate = True

    def activate(self, paddle, game_window):
        if not paddle.lasers_activated:
            paddle.activateLasers(game_window)

    def deactivate(self, paddle, game_window):
        paddle.deactivateLasers(game_window)

    def shootLasers(self, paddle, laser_sound):
        laser1 = Laser(paddle.x, paddle.y)
        laser2 = Laser(paddle.x + paddle.width - 1, paddle.y)

        laser_sound.play()
        return laser1, laser2

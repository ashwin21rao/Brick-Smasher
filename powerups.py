import copy
from sprites import Sprite, SpriteCollisionMixin
from colorama import Back
from functools import partial
from balls import Ball


class PowerUp(Sprite, SpriteCollisionMixin):
    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.y_speed = y_speed

    def render(self, game_window, powerup_text=None):
        game_width = game_window.shape[1]

        game_window[self.y, self.x: self.x + self.width] = list(powerup_text)

        if self.color is not None:
            if self.x < game_width:
                game_window[self.y: self.y + self.height, self.x] = Back.__getattribute__(self.color.upper()) + game_window[self.y: self.y + self.height, self.x]
            if self.x + self.width < game_width:
                game_window[self.y: self.y + self.height, self.x + self.width] = Back.RESET + game_window[self.y: self.y + self.height, self.x + self.width]

    def clearOldPosition(self, game_window):
        game_window[self.y, self.x: self.x + self.width] = " "
        if self.color is not None:
            super().clearOldPosition(game_window)

    def move(self, game_window):
        # clear old position
        self.clearOldPosition(game_window)

        # move power up
        self.y += self.y_speed

    def ready(self, paddle):
        return self.checkHorizontalCollision(paddle)

    def powerUpMissed(self, game_height):
        return self.y + self.height >= game_height


class ExpandPaddle(PowerUp):
    type = "EXPAND_PADDLE"

    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.render = partial(super().render, powerup_text="EP")
        self.can_deactivate = False

    def activate(self, paddle, game_window):
        paddle.expand(game_window)


class ShrinkPaddle(PowerUp):
    type = "SHRINK_PADDLE"

    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.render = partial(super().render, powerup_text="SP")
        self.can_deactivate = False

    def activate(self, paddle, game_window):
        paddle.shrink(game_window)


class ThruBall(PowerUp):
    type = "THRU_BALL"

    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.render = partial(super().render, powerup_text="TB")
        self.can_deactivate = True

    def activate(self, balls, blocks):
        for ball in balls:
            ball.disableCollision()
        for block in blocks:
            block.killOnCollision()

    def deactivate(self, blocks, balls):
        for block in blocks:
            block.kill_on_collision = False
        for ball in balls:
            ball.collidable = True


class FastBall(PowerUp):
    type = "FAST_BALL"

    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1, initial_ball_speed_coefficient=3):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.speed_multiplier = 1
        self.render = partial(super().render, powerup_text="FB")
        self.can_deactivate = True
        self.initial_ball_speed_coefficient = initial_ball_speed_coefficient

    def activate(self, ball_speed_coefficient):
        return ball_speed_coefficient - self.speed_multiplier if ball_speed_coefficient - self.speed_multiplier > 0 else 1

    def deactivate(self):
        return self.initial_ball_speed_coefficient


class SlowBall(PowerUp):
    type = "SLOW_BALL"

    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1, initial_ball_speed_coefficient=3):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.speed_multiplier = 1
        self.render = partial(super().render, powerup_text="SB")
        self.can_deactivate = True
        self.initial_ball_speed_coefficient = initial_ball_speed_coefficient

    def activate(self, ball_speed_coefficient):
        return ball_speed_coefficient + self.speed_multiplier

    def deactivate(self):
        return self.initial_ball_speed_coefficient


class ExtraLife(PowerUp):
    type = "EXTRA_LIFE"

    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.life_multiplier = 1
        self.render = partial(super().render, powerup_text="XL")
        self.can_deactivate = False

    def activate(self, lives):
        return lives + self.life_multiplier


class MultiplyBalls(PowerUp):
    type = "MULTIPLY_BALLS"

    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.life_multiplier = 1
        self.render = partial(super().render, powerup_text="MB")
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

    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.life_multiplier = 1
        self.render = partial(super().render, powerup_text="PG")
        self.can_deactivate = True

    def activate(self, balls):
        for ball in balls:
            ball.enable_paddle_grab = True

    def deactivate(self, balls):
        for ball in balls:
            ball.enable_paddle_grab = False
            if not ball.launched:
                ball.launch()

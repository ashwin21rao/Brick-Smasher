from sprites import Sprite, SpriteCollisionMixin
from colorama import Back
from functools import partial


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

    def activated(self, paddle):
        return self.checkHorizontalCollision(paddle)

    def powerUpMissed(self, game_height):
        return self.y + self.height >= game_height


class ExpandPaddle(PowerUp):
    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.type = "EXPAND_PADDLE"
        self.render = partial(super().render, powerup_text="EP")

    def activate(self, paddle, game_window):
        paddle.expand(game_window)

    def deactivate(self):
        pass


class ShrinkPaddle(PowerUp):
    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.type = "SHRINK_PADDLE"
        self.render = partial(super().render, powerup_text="SP")

    def activate(self, paddle, game_window):
        paddle.shrink(game_window)

    def deactivate(self):
        pass


class ThruBall(PowerUp):
    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.type = "THRU_BALL"
        self.render = partial(super().render, powerup_text="TB")

    def activate(self, balls, blocks):
        for ball in balls:
            ball.disableCollision()
        for block in blocks:
            block.killOnCollision()

    def deactivate(self, blocks):
        for block in blocks:
            block.kill_on_collision = False
        print("In deactivate", end="")


class FastBall(PowerUp):
    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.type = "FAST_BALL"
        self.speed_multiplier = 1
        self.render = partial(super().render, powerup_text="FB")

    def activate(self, ball_speed_coefficient):
        return ball_speed_coefficient - self.speed_multiplier

    def deactivate(self, ball_speed_coefficient):
        return ball_speed_coefficient + self.speed_multiplier


class SlowBall(PowerUp):
    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.type = "SLOW_BALL"
        self.speed_multiplier = 1
        self.render = partial(super().render, powerup_text="SB")

    # def render(self, game_window, powerup_text="FB"):
    #     super().render(game_window, powerup_text=powerup_text)

    def activate(self, ball_speed_coefficient):
        return ball_speed_coefficient + self.speed_multiplier

    def deactivate(self, ball_speed_coefficient):
        return ball_speed_coefficient - self.speed_multiplier


class ExtraLife(PowerUp):
    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
        self.type = "EXTRA_LIFE"
        self.life_multiplier = 1
        self.render = partial(super().render, powerup_text="XL")

    def activate(self, lives):
        return lives + self.life_multiplier

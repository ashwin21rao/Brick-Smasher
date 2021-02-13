from sprites import Sprite, SpriteCollisionMixin
from colorama import Back


class PowerUp(Sprite, SpriteCollisionMixin):
    def __init__(self, x_coordinate, y_coordinate, width, height, type, color=None, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.type = type
        self.y_speed = y_speed

    def render(self, game_window):
        game_width = game_window.shape[1]

        powerup_text = ""
        if self.type == "EXPAND PADDLE":
            powerup_text = "EP"
        elif self.type == "SHRINK PADDLE":
            powerup_text = "SP"
        elif self.type == "MULTIPLY BALLS":
            powerup_text = "MB"
        elif self.type == "FAST BALL":
            powerup_text = "FB"
        elif self.type == "THRU BALL":
            powerup_text = "TB"
        elif self.type == "PADDLE GRAB":
            powerup_text = "PG"

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


# class ExpandPaddle(PowerUp):
#     def __init__(self, x_coordinate, y_coordinate, width, height, color=None, y_speed=1):
#         super().__init__(x_coordinate, y_coordinate, width, height, color=color, y_speed=y_speed)
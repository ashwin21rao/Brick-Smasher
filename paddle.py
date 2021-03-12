from sprites import MovableSprite
import numpy as np
from colorama import Back

class Paddle(MovableSprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color, x_speed)
        self.initArray()

    def initArray(self):
        self.array = np.array([[" " for _ in range(self.width)] for _ in range(self.height)], dtype=object)

        if self.color is not None:
            self.array[:, 0] = Back.__getattribute__(self.color.upper()) + " "
            self.array[:, self.width - 1] = " " + Back.RESET

    def expand(self, game_window):
        game_width = game_window.shape[1]

        self.clearOldPosition(game_window)

        mid = self.x + self.width // 2
        self.width = 16
        self.x = mid - self.width // 2

        if self.x + self.width > game_width:
            self.x = game_width - self.width
        elif self.x < 0:
            self.x = 0

        self.initArray()

    def shrink(self, game_window):
        game_width = game_window.shape[1]

        self.clearOldPosition(game_window)

        mid = self.x + self.width // 2
        self.width = 6
        self.x = mid - self.width // 2

        if self.x + self.width > game_width:
            self.x = game_width - self.width
        elif self.x < 0:
            self.x = 0

        self.initArray()

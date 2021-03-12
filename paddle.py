from sprites import MovableSprite
import numpy as np
from colorama import Back, Fore

class Paddle(MovableSprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color, x_speed)
        self.initArray()
        self.width_without_lasers = self.width
        self.lasers_activated = False

    def initArray(self):
        self.array = np.array([[" " for _ in range(self.width)] for _ in range(self.height)], dtype=object)

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
        self.initHitBox()

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
        self.initHitBox()

    def activateLasers(self, game_window):
        self.lasers_activated = True

        laser_array = (np.array([[Fore.RED + "\u2503" + Fore.RESET] for _ in range(self.height)], dtype=object))
        self.array = np.hstack((laser_array, self.array, laser_array))

        # change width
        self.width += 2

        # change position
        self.updatePosition(x=(self.x - 1))

        game_width = game_window.shape[1]
        if self.x + self.width > game_width:
            self.updatePosition(x=(game_width - self.width))
        elif self.x < 0:
            self.updatePosition(x=0)

        # change hitbox
        self.updateHitbox(x=(self.x + 1), width=self.width_without_lasers)

    def deactivateLasers(self):
        self.lasers_activated = False

        # reset width and position
        self.width = self.width_without_lasers
        self.updatePosition(x=(self.x + 1))

        # reset hitbox
        self.initArray()
        self.initHitBox()

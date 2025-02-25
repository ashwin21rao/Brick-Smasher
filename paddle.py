from sprites import MovableSprite
import numpy as np
from colorama import Back, Fore

class Paddle(MovableSprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color, x_speed)
        self.width_without_lasers = self.width
        self.lasers_activated = False
        self.paddle_grab_activated = False
        self.initArray()

    def initArray(self):
        self.array = np.array([[" " for _ in range(self.width)] for _ in range(self.height)], dtype=object)

        side_design = Fore.CYAN + "\u2503" + Fore.RESET if self.paddle_grab_activated else " "
        self.array[:, 0] = Back.__getattribute__(self.color.upper()) + side_design
        self.array[:, self.width - 1] = side_design + Back.RESET

    def moveLeft(self, game_window, speed=None):
        super().moveLeft(game_window, speed)
        if self.lasers_activated:
            self.updateHitbox(x=(self.x + 1), width=self.width_without_lasers)

    def moveRight(self, game_window, speed=None):
        super().moveRight(game_window, speed)
        if self.lasers_activated:
            self.updateHitbox(x=(self.x + 1), width=self.width_without_lasers)

    def changeWidth(self, game_window, new_width):
        game_width = game_window.shape[1]

        self.clearOldPosition(game_window)

        mid = self.x + self.width // 2
        self.width = new_width
        self.width_without_lasers = self.width
        self.updateHitbox(width=self.width)
        self.updatePosition(x=(mid - self.width // 2))

        if self.x + self.width > game_width:
            self.updatePosition(x=(game_width - self.width))
        elif self.x < 0:
            self.updatePosition(x=0)

        self.initArray()

        if self.lasers_activated:
            self.activateLasers(game_window)

    def expand(self, game_window):
        self.changeWidth(game_window, 16)

    def shrink(self, game_window):
        self.changeWidth(game_window, 6)

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

    def deactivateLasers(self, game_window):
        self.lasers_activated = False

        # reset width and position
        self.clearOldPosition(game_window)
        self.width = self.width_without_lasers
        self.updatePosition(x=(self.x + 1))

        # reset hitbox
        self.initArray()
        self.initHitBox()

    def activatePaddleGrab(self):
        self.paddle_grab_activated = True

        offset = 1 if self.lasers_activated else 0
        self.array[:, offset] = Back.__getattribute__(self.color.upper()) + Fore.CYAN + "\u2503" + Fore.RESET
        self.array[:, self.width - 1 - offset] = Fore.CYAN + "\u2503" + Fore.RESET + Back.RESET

    def deactivatePaddleGrab(self):
        self.paddle_grab_activated = False

        offset = 1 if self.lasers_activated else 0
        self.array[:, offset] = Back.__getattribute__(self.color.upper()) + " "
        self.array[:, self.width - 1 - offset] = " " + Back.RESET

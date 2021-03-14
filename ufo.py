from sprites import MovableSprite
import numpy as np
from colorama import Fore, Style
import config


class Ufo(MovableSprite):
    def __init__(self, x_coordinate, y_coordinate, x_speed=1):
        width = 37
        height = 9
        self.colors = ["blue", "green", "red"]
        self.lives = 15
        super().__init__(x_coordinate, y_coordinate, width, height, None, x_speed)
        self.initArray()

    def initArray(self):
        ufo = """
         \\  _.-'~~~~'-._   /
  .      .-~    \\__/     ~-.      .
       .-~      (oo)       ~-.
      (________//~~\\\\_________)
 _.-~`                         `~-._
/O=O=O=O=O=O=O=O=O=O=O=O=O=O=O=O=O=O\\
\\-----------------------------------/
           \\x x x x x x x/
   .  *     \\x_x_x_x_x_x/"""

        self.array = ufo.split("\n")[1:]
        for i in range(len(self.array)):
            self.array[i] = list(self.array[i].ljust(37, " "))

        self.array = np.array(self.array, dtype=object)

        for i in range(self.array.shape[0]):
            for j in range(self.array.shape[1]):
                self.array[i][j] = Fore.__getattribute__((self.colors[0] if j % 2 == 0 else self.colors[1]).upper()) + self.array[i][j] + Fore.RESET

        self.array[:, 0] = Style.BRIGHT + self.array[:, 0]
        self.array[:, -1] = self.array[:, -1] + Style.NORMAL

        health_bar_start = self.width // 2 - self.lives // 2
        self.array[6, health_bar_start: health_bar_start + self.lives] = self.getHealthBar()

    def getHealthBar(self):
        health_bar = ["|" for _ in range(self.lives)]

        health_bar[0] = Fore.__getattribute__(self.colors[-1].upper()) + health_bar[0] + (Fore.RESET if self.lives == 1 else "")
        if self.lives > 1:
            health_bar[-1] = health_bar[-1] + Fore.RESET

        return health_bar

    def handleCollision(self, ufo_sound):
        self.lives -= 1
        if self.lives > 0:
            self.initArray()

        ufo_sound.play()


    # def render(self, game_window):
    #     self.colors.reverse()
    #     self.initArray()
    #     super().render(game_window)

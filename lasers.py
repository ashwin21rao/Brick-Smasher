from sprites import Sprite, SpriteCollisionMixin
from colorama import Fore


class Laser(Sprite, SpriteCollisionMixin):
    def __init__(self, x_coordinate, y_coordinate, width=1, height=1, color="red", y_speed=-1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.y_speed = y_speed
        self.initArray()

    def initArray(self):
        self.array = [Fore.RED + "\u2503" + Fore.RESET]

    def hitBlock(self, block):
        return self.checkHorizontalCollision(block)

    def move(self, game_window):
        # clear old position
        self.clearOldPosition(game_window)

        # move power up
        self.updatePosition(y=(self.y + self.y_speed))

    def laserMissed(self):
        return self.y <= 0

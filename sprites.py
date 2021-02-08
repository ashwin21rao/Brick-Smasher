import sys
import numpy as np
from colorama import Back

class Sprite:
    def __init__(self, x_coordinate, y_coordinate, width, height, color):
        self.x = x_coordinate
        self.y = y_coordinate
        self.width = width
        self.height = height
        self.color = color

    def render(self, game_window):
        # print("HERE (sprite render)", self, self.x, self.width, "\r")
        game_width = game_window.shape[1]

        game_window[self.y: self.y + self.height, self.x] = Back.__getattribute__(self.color.upper()) + " "
        if self.x + self.width < game_width:
            game_window[self.y: self.y + self.height, self.x + self.width] = Back.__getattribute__("RESET") + " "


    def clearOldPosition(self, game_window):
        game_width = game_window.shape[1]

        game_window[self.y: self.y + self.height, self.x] = " "
        if self.x + self.width < game_width:
            game_window[self.y: self.y + self.height, self.x + self.width] = " "


class Paddle(Sprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.speed = speed

    def move(self, char, game_window):
        game_width = game_window.shape[1]

        # clear old position
        self.clearOldPosition(game_window)

        # check for 'a' and 'd' keys
        if char == 97:
            self.x = self.x - self.speed if self.x - self.speed > -1 else 0  # move left
        elif char == 100:
            self.x = self.x + self.speed if self.x + self.width + self.speed <= game_width \
                else game_width - self.width  # move right

        # check for left and right arrow key
        if char == 27 and ord(sys.stdin.read(1)) == 91:
            char = ord(sys.stdin.read(1))
            if char == 67:
                self.x = self.x + self.speed if self.x + self.width + self.speed <= game_width \
                                             else game_width - self.width # move right
            elif char == 68:
                self.x = self.x - self.speed if self.x - self.speed > -1 else 0  # move left


class Ball(Sprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, speed=1, initial_slope=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.speed = speed
        self.slope = initial_slope

    def move(self, game_window):
        game_height, game_width = game_window.shape

        # clear old position
        self.clearOldPosition(game_window)

        # move ball
        if self.y + self.height >= game_height or self.y <= 0:
            self.slope *= -1

        if self.x + self.width >= game_width or self.x <= 0:
            self.slope *= -1
            self.speed *= -1

        self.x += round(self.speed * np.cos(np.arctan(self.slope)))
        self.y += round(self.speed * np.sin(np.arctan(self.slope)))


    def collideHorizontal(self):
        pass

    def collideVertical(self):
        pass

    def handleCollision(self, sprite):
        # # prevent collision with vertical from becoming horizontal
        # if self.x + self.width == sprite.x or self.x == sprite.x + sprite.width:
        #     self.slope *= -1
        #     self.speed *= -1

        # collision with horizontal sides of sprite rect
        if self.y + self.height >= sprite.y or self.y <= sprite.y + sprite.height:
            self.slope *= -1

        # collision with vertical sides of sprite rect
        elif self.x + self.width >= sprite.x or self.x <= sprite.x + sprite.width:
            self.slope *= -1
            self.speed *= -1


class Block(Sprite):
    colors = ["green", "yellow", "red", "blue"]

    def __init__(self, x_coordinate, y_coordinate, width, height, color):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.strength = Block.colors.index(color)

    def handleCollision(self):
        if self.color == "blue":
            return True

        self.strength -= 1
        if self.strength > -1:
            self.color = Block.colors[self.strength]
            return True
        return False

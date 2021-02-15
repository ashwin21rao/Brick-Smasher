import sys
import numpy as np
from colorama import Back


# generic sprite
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

        if self.color is not None:
            if self.x < game_width:
                game_window[self.y: self.y + self.height, self.x] = Back.__getattribute__(self.color.upper()) + " "
            if self.x + self.width < game_width:
                game_window[self.y: self.y + self.height, self.x + self.width] = Back.RESET + " "

    def clearOldPosition(self, game_window):
        game_width = game_window.shape[1]

        if self.x < game_width:
            game_window[self.y: self.y + self.height, self.x] = " "
        if self.x + self.width < game_width:
            game_window[self.y: self.y + self.height, self.x + self.width] = " "

    def setNewPosition(self, x, y):
        self.x = x
        self.y = y


# generic sprite movable with arrow keys (left and right)
class MovableSprite(Sprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.x_speed = x_speed

    def moveLeft(self, game_window, speed=None):
        self.clearOldPosition(game_window)

        if speed is None:
            speed = abs(self.x_speed)
        self.x = self.x - speed if self.x - speed > -1 else 0  # move left

    def moveRight(self, game_window, speed=None):
        self.clearOldPosition(game_window)

        game_width = game_window.shape[1]
        if speed is None:
            speed = abs(self.x_speed)

        self.x = self.x + speed if self.x + self.width + speed <= game_width \
            else game_width - self.width  # move right

    def setSpeed(self, x_speed):
        self.x_speed = x_speed


# generic sprite with collision checking helper functions
class SpriteCollisionMixin:
    def checkHorizontalCollision(self, sprite):
        return (self.y + self.height == sprite.y and self.y_speed > 0 or self.y == sprite.y + sprite.height and self.y_speed < 0) and \
               (self.x + self.width - 1 >= sprite.x and self.x <= sprite.x + sprite.width - 1)

    def checkVerticalCollision(self, sprite):
        return (self.x + self.width == sprite.x and self.x_speed > 0 or self.x == sprite.x + sprite.width and self.x_speed < 0) and \
               (self.y + self.height - 1 >= sprite.y and self.y <= sprite.y + sprite.height - 1)

    def checkCornerCollision(self, sprite):
        return not self.checkHorizontalCollision(sprite) and not self.checkVerticalCollision(sprite)

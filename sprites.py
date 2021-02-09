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
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.x_speed = x_speed

    def move(self, char, game_window):
        game_width = game_window.shape[1]

        # clear old position
        self.clearOldPosition(game_window)

        # check for 'a' and 'd' keys
        if char == 97:
            self.x = self.x - self.x_speed if self.x - self.x_speed > -1 else 0  # move left
        elif char == 100:
            self.x = self.x + self.x_speed if self.x + self.width + self.x_speed <= game_width \
                else game_width - self.width  # move right

        # check for left and right arrow key
        if char == 27 and ord(sys.stdin.read(1)) == 91:
            char = ord(sys.stdin.read(1))
            if char == 67:
                self.x = self.x + self.x_speed if self.x + self.width + self.x_speed <= game_width \
                    else game_width - self.width  # move right
            elif char == 68:
                self.x = self.x - self.x_speed if self.x - self.x_speed > -1 else 0  # move left


class Ball(Sprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1, y_speed=1, initial_slope=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.slope = initial_slope

    def reflectHorizontal(self):
        self.y_speed *= -1

    def reflectVertical(self):
        self.x_speed *= -1

    def reflectHorizontalAndVertical(self):
        self.x_speed *= -1
        self.y_speed *= -1

    def checkHorizontalCollision(self, sprite):
        return (self.y + self.height == sprite.y or self.y == sprite.y + sprite.height) and \
               (self.x + self.width - 1 >= sprite.x and self.x <= sprite.x + sprite.width - 1)

    def checkVerticalCollision(self, sprite):
        return (self.x + self.width == sprite.x or self.x == sprite.x + sprite.width) and \
               (self.y + self.height - 1 >= sprite.y and self.y <= sprite.y + sprite.height - 1)

    def checkCornerCollision(self, sprite):
        return not self.checkHorizontalCollision(sprite) and not self.checkVerticalCollision(sprite)

    def handleCornerCollision(self, sprite):
        # top left corner
        if self.x + self.width == sprite.x and self.y + self.height == sprite.y and \
                (self.x_speed > 0 and self.y_speed > 0):
            return True

        # bottom left corner
        if self.x + self.width == sprite.x and self.y == sprite.y + sprite.height and \
                (self.x_speed > 0 and self.y_speed < 0):
            return True

        # top right corner
        if self.x == sprite.x + sprite.width and self.y + self.height == sprite.y and \
                (self.x_speed < 0 and self.y_speed > 0):
            return True

        # bottom right corner
        if self.x == sprite.x + sprite.width and self.y == sprite.y + sprite.height and \
                (self.x_speed < 0 and self.y_speed < 0):
            return True

        return False

    def move(self, game_window):
        game_height, game_width = game_window.shape

        # clear old position
        self.clearOldPosition(game_window)

        # move ball
        if self.y + self.height >= game_height or self.y <= 0:
            self.reflectHorizontal()

        if self.x + self.width >= game_width or self.x <= 0:
            self.reflectVertical()

        self.x += self.x_speed
        self.y += self.y_speed


    def handleCollision(self, sprite, obstacle="block"):
        if obstacle == "block":
            if self.checkVerticalCollision(sprite):
                self.reflectVertical()
            elif self.checkHorizontalCollision(sprite):
                self.reflectHorizontal()
            elif self.checkCornerCollision(sprite) and self.handleCornerCollision(sprite):
                self.reflectHorizontalAndVertical()

        elif obstacle == "paddle":
            if self.checkHorizontalCollision(sprite):
                self.reflectHorizontal()
                # self.x_speed = self.x - (sprite.x + sprite.width) // 2

        elif obstacle == "powerup":
            pass


class Block(Sprite):
    colors = ["green", "yellow", "red", "blue"]

    def __init__(self, x_coordinate, y_coordinate, width, height, color):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.strength = Block.colors.index(color)

    def getStrength(self):
        return self.strength

    def handleCollision(self, game_window):
        if self.color == "blue":
            return

        self.strength -= 1
        if self.strength > -1:
            self.color = Block.colors[self.strength]
        else:
            self.clearOldPosition(game_window)
            print("Here", end="")

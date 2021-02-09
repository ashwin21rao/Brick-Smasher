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

        game_window[self.y: self.y + self.height, self.x] = Back.__getattribute__(self.color.upper()) + " "
        if self.x + self.width < game_width:
            game_window[self.y: self.y + self.height, self.x + self.width] = Back.__getattribute__("RESET") + " "

    def clearOldPosition(self, game_window):
        game_width = game_window.shape[1]

        game_window[self.y: self.y + self.height, self.x] = " "
        if self.x + self.width < game_width:
            game_window[self.y: self.y + self.height, self.x + self.width] = " "


# generic sprite movable with arrow keys (left and right)
class MovableSprite(Sprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.x_speed = x_speed

    def moveLeft(self, game_window):
        self.clearOldPosition(game_window)
        self.x = self.x - self.x_speed if self.x - self.x_speed > -1 else 0  # move left

    def moveRight(self, game_window):
        self.clearOldPosition(game_window)

        game_width = game_window.shape[1]
        self.x = self.x + self.x_speed if self.x + self.width + self.x_speed <= game_width \
            else game_width - self.width  # move right

    def setSpeed(self, x_speed):
        self.x_speed = x_speed


class Paddle(MovableSprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color, x_speed)


class Ball(MovableSprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1, y_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color, x_speed)
        self.y_speed = y_speed

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

    def handleCollision(self, sprite, obstacle="block"):
        if obstacle == "block":
            if self.checkVerticalCollision(sprite):
                self.reflectVertical()
            elif self.checkHorizontalCollision(sprite):
                self.reflectHorizontal()
            elif self.checkCornerCollision(sprite) and self.handleCornerCollision(sprite):
                self.reflectHorizontalAndVertical()

        elif obstacle == "paddle":
            if self.checkHorizontalCollision(sprite) or \
                    (self.checkCornerCollision(sprite) and self.handleCornerCollision(sprite)):
                self.reflectHorizontal()
                if self.x == sprite.x + sprite.width // 2 - self.width // 2:
                    self.x_speed = 0
                elif self.x > sprite.x + sprite.width // 2 - self.width // 2:
                    self.x_speed = 1
                else:
                    self.x_speed = -1

        elif obstacle == "powerup":
            pass

    def move(self, game_window):
        game_height, game_width = game_window.shape

        # clear old position
        self.clearOldPosition(game_window)

        # bounce off side walls
        if self.x + self.width >= game_width or self.x <= 0:
            self.reflectVertical()

        # bounce off top wall
        if self.y <= 0:
            self.reflectHorizontal()

        # hit bottom wall (level failed)
        if self.y + self.height >= game_height:
            return False

        self.x += self.x_speed
        self.y += self.y_speed

        return True

    def launch(self, x_speed=1, y_speed=-1):
        self.x_speed = x_speed
        self.y_speed = y_speed


class Block(Sprite):
    colors = ["green", "yellow", "red", "blue"]

    def __init__(self, x_coordinate, y_coordinate, width, height, color):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.strength = Block.colors.index(color)

    def getStrength(self):
        return self.strength

    def handleCollision(self, game_window, brick_sounds):
        if self.color == "blue":
            brick_sounds["indestructible_brick_sound"].play()
            return

        brick_sounds["regular_brick_sound"].play()
        self.strength -= 1
        if self.strength > -1:
            self.color = Block.colors[self.strength]
        else:
            self.clearOldPosition(game_window)

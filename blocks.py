from sprites import Sprite
import numpy as np
import random
from colorama import Back


class Block(Sprite):
    colors = ["green", "yellow", "red", None, "blue", "magenta"]

    def __init__(self, x_coordinate, y_coordinate, width, height, color=None, invisible_new_color=None, type="REGULAR_BLOCK"):
        super().__init__(x_coordinate, y_coordinate, width, height, color if type != "EXPLOSIVE_BLOCK" else "magenta")
        self.type = type
        self.strength = Block.colors.index(color)
        self.original_color = self.color
        self.kill_on_collision = False
        self.explode_on_collision = False if type == "REGULAR_BLOCK" else True
        self.invisible_new_color = invisible_new_color
        self.initArray()

    def initArray(self):
        self.array = np.array([[" " for _ in range(self.width)] for _ in range(self.height)], dtype=object)

        if self.color is not None:
            self.array[:, 0] = Back.__getattribute__(self.color.upper()) + " "
            self.array[:, self.width - 1] = " " + Back.RESET

    def moveDown(self, game_window):
        self.clearOldPosition(game_window)
        self.updatePosition(y=(self.y + 1))

    def getStrength(self):
        return self.strength

    def handleCollision(self, game_window, blocks):
        # for explosive ball or explosive blocks
        if self.explode_on_collision:
            self.killExplosiveBlocks(blocks)
            for block in blocks:
                if block.strength == -1:
                    block.clearOldPosition(game_window)
            return

        # for fire ball and thru ball
        if self.kill_on_collision:
            self.strength = -1
            self.clearOldPosition(game_window)
            return

        # indestructible brick
        if self.color == "blue":
            return

        # invisible brick changes to specified color
        if self.color is None:
            self.setColor(self.invisible_new_color)
            self.strength = Block.colors.index(self.invisible_new_color)
        else:
            self.strength -= 1

        if self.strength > -1:
            self.setColor(Block.colors[self.strength])
        else:
            self.clearOldPosition(game_window)

    def killOnCollision(self):
        self.kill_on_collision = True

    def explodeOnCollision(self):
        self.explode_on_collision = True

    def playSound(self, brick_sounds):
        if self.explode_on_collision:
            brick_sounds["explosive_brick_sound"].play()
        elif self.kill_on_collision:
            brick_sounds["thru_ball_sound"].play()
        elif self.color == "blue":
            brick_sounds["indestructible_brick_sound"].play()
        elif self.color is None:
            brick_sounds["invisible_brick_sound"].play()
        else:
            brick_sounds["regular_brick_sound"].play()

    def getAdjacentBlocks(self, blocks):
        adj_blocks = []
        for block in blocks:
            if block.y == self.y - 1 - block.height or block.y == self.y + self.height + 1:
                if block.x == self.x - 1 - block.width or block.x == self.x or block.x == self.x + self.width + 1:
                    adj_blocks.append(block)
            elif block.y == self.y:
                if block.x == self.x - 1 - block.width or block.x == self.x + self.width + 1:
                    adj_blocks.append(block)

        return adj_blocks

    def killExplosiveBlocks(self, blocks):
        if self.strength == -1:
            return
        self.strength = -1

        for block in self.getAdjacentBlocks(blocks):
            if block.type == "EXPLOSIVE_BLOCK":
                block.killExplosiveBlocks(blocks)
            else:
                block.strength = -1


class RainbowBlock(Block):
    type = "RAINBOW_BLOCK"

    def __init__(self, x_coordinate, y_coordinate, width, height):
        self.hit = False
        self.changing_colors = ["green", "yellow", "red", "blue"]
        random.shuffle(self.changing_colors)

        self.color_index = np.random.randint(0, len(self.changing_colors))
        super().__init__(x_coordinate, y_coordinate, width, height, self.changing_colors[self.color_index])

    def changeColor(self):
        if not self.hit:
            self.color_index = (self.color_index + 1) % len(self.changing_colors)
            self.setColor(self.changing_colors[self.color_index])
            self.strength = Block.colors.index(self.color)

    def handleCollision(self, game_window, blocks):
        super().handleCollision(game_window, blocks)
        self.hit = True

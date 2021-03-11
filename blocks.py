from sprites import Sprite
import numpy as np
import random


class Block(Sprite):
    type = "REGULAR_BLOCK"
    colors = ["green", "yellow", "red", None, "blue", "magenta"]

    def __init__(self, x_coordinate, y_coordinate, width, height, color, invisible_new_color=None):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.strength = Block.colors.index(color)
        self.original_color = color
        self.kill_on_collision = False
        self.invisible_new_color = invisible_new_color

    def moveDown(self, game_window):
        self.clearOldPosition(game_window)
        self.y += 1

    def getStrength(self):
        return self.strength

    def handleCollision(self, game_window, blocks):
        if self.kill_on_collision:
            self.strength = -1
            self.clearOldPosition(game_window)
            return

        if self.color == "blue":
            return

        # invisible brick changes to specified color
        if self.color is None:
            self.color = self.invisible_new_color
            self.strength = Block.colors.index(self.invisible_new_color)
        else:
            self.strength -= 1

        if self.strength > -1:
            self.color = Block.colors[self.strength]
        else:
            self.clearOldPosition(game_window)

    def killOnCollision(self):
        self.kill_on_collision = True

    def playSound(self, brick_sounds):
        if self.kill_on_collision:
            brick_sounds["thru_ball_sound"].play()
        elif self.color == "blue":
            brick_sounds["indestructible_brick_sound"].play()
        elif self.color is None:
            brick_sounds["invisible_brick_sound"].play()
        else:
            brick_sounds["regular_brick_sound"].play()


class ExplosiveBlock(Block):
    type = "EXPLOSIVE_BLOCK"

    def __init__(self, x_coordinate, y_coordinate, width, height):
        super().__init__(x_coordinate, y_coordinate, width, height, "magenta")

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

    def handleCollision(self, game_window, blocks):
        self.killExplosiveBlocks(blocks)
        for block in blocks:
            if block.strength == -1:
                block.clearOldPosition(game_window)

    def playSound(self, brick_sounds):
        brick_sounds["explosive_brick_sound"].play()


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
            self.color = self.changing_colors[self.color_index]
            self.strength = Block.colors.index(self.color)

    def handleCollision(self, game_window, blocks):
        super().handleCollision(game_window, blocks)
        self.hit = True

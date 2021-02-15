from sprites import Sprite


class Block(Sprite):
    colors = ["green", "yellow", "red", None, "blue"]

    def __init__(self, x_coordinate, y_coordinate, width, height, color, invisible_new_color=None):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.strength = Block.colors.index(color)
        self.original_color = color
        self.kill_on_collision = False
        self.invisible_new_color = invisible_new_color

    def getStrength(self):
        return self.strength

    def handleCollision(self, game_window, brick_sounds):
        if self.kill_on_collision:
            brick_sounds["explosive_brick_sound"].play()
            self.strength = -1
            self.clearOldPosition(game_window)
            return

        if self.color == "blue":
            brick_sounds["indestructible_brick_sound"].play()
            return

        brick_sounds["regular_brick_sound"].play()

        # invisible brick changes to specified
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

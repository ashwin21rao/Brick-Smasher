from sprites import Sprite


class Block(Sprite):
    colors = ["green", "yellow", "red", "blue"]

    def __init__(self, x_coordinate, y_coordinate, width, height, color):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.strength = Block.colors.index(color)
        self.original_color = color
        self.kill_on_collision = False

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
        self.strength -= 1
        if self.strength > -1:
            self.color = Block.colors[self.strength]
        else:
            self.clearOldPosition(game_window)

    def killOnCollision(self):
        self.kill_on_collision = True

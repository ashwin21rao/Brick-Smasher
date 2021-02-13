from sprites import MovableSprite


class Paddle(MovableSprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color, x_speed)

    def expand(self, game_window):
        self.clearOldPosition(game_window)
        self.width = 16

    def shrink(self, game_window):
        self.clearOldPosition(game_window)
        self.width = 6

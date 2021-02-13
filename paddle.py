from sprites import MovableSprite


class Paddle(MovableSprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color, x_speed)

    def expand(self, game_window):
        self.clearOldPosition(game_window)
        self.width = 16

        # game_width = game_window.shape[1]
        #
        # self.x -= self.width // 2
        #
        # if self.x + self.width > game_width:
        #     self.x = game_width - self.width
        # elif self.x < 0:
        #     self.x = 0

    def shrink(self, game_window):
        self.clearOldPosition(game_window)
        self.width = 6

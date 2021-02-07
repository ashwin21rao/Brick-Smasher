import os
import numpy as np
from colorama import Back


class Game:
    def __init__(self, width=75, height=35):
        self.width = width  # width of game screen
        self.height = height  # height of game screen

        # columns, rows = os.get_terminal_size()
        # self.rows = height + 10 if rows < height else rows          # rows in terminal
        # self.columns = width + 20 if columns < width else columns   # columns in terminal

        self.rows = height + 10
        self.columns = width + 20

        self.left_margin = (self.columns - self.width) // 2
        self.top_margin = (self.rows - self.height) // 2

        self.screen = np.array([[" " for _ in range(self.columns)] for _ in range(self.rows)], dtype=object)
        self.game_window = self.screen[self.top_margin: self.top_margin + self.height,
                                       self.left_margin: self.left_margin + self.width]

        self.FPS = 40
        self.initGameBox()

    def initGameBox(self):
        # title
        title = "BRICK SMASH!"
        title_margin = self.left_margin + (self.width - len(title)) // 2
        self.screen[self.top_margin - 2, title_margin: title_margin + len(title)] = list(title)

        # vertical lines
        self.screen[self.top_margin - 1: self.rows - self.top_margin + 1, self.left_margin - 1] = \
            Back.__getattribute__("RESET") + "\u2503"
        self.screen[self.top_margin - 1: self.rows - self.top_margin + 1, self.columns - self.left_margin] = \
            Back.__getattribute__("RESET") + "\u2503"

        # horizontal lines
        self.screen[self.top_margin - 1, self.left_margin - 1: self.columns - self.left_margin + 1] = \
            Back.__getattribute__("RESET") + "\u2501"
        self.screen[self.rows - self.top_margin, self.left_margin - 1: self.columns - self.left_margin + 1] = \
            Back.__getattribute__("RESET") + "\u2501"

        # corners
        self.screen[self.top_margin - 1, self.left_margin - 1] = Back.__getattribute__("RESET") + "\u250F"
        self.screen[self.top_margin - 1, self.columns - self.left_margin] = Back.__getattribute__("RESET") + "\u2513"
        self.screen[self.rows - self.top_margin, self.left_margin - 1] = Back.__getattribute__("RESET") + "\u2517"
        self.screen[self.rows - self.top_margin, self.columns - self.left_margin] = \
            Back.__getattribute__("RESET") + "\u251B"

    def updateScreen(self, sprite_list):
        for sprite in sprite_list:
            sprite.render(self.game_window)

    def printScreen(self, full=False):
        # if terminal too small for game, resize it
        print(f"\33[8;{self.rows};{self.columns}t")

        # print screen
        if full:
            # clear screen
            os.system("clear")

            for h in range(self.rows):
                for w in range(self.columns):
                    print(self.screen[h][w], end="")
                if h < self.rows - 1:
                    print()
        else:
            for h in range(self.height):
                # print left vertical column (needed to reset background)
                print(f"\033[{self.top_margin + h};{self.left_margin}H" +
                      self.screen[self.top_margin, self.left_margin - 1], end="")

                # print game window
                for w in range(self.width):
                    print(self.game_window[h][w], end="")

                print(f"\033[{self.top_margin + self.height};0H\n")

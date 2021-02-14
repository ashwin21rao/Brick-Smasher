import os
import numpy as np
import time
from datetime import datetime, timedelta
from colorama import Fore, Back, Style
import config


class Game:
    def __init__(self, width=75, height=34):
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

        self.FPS = config.FPS
        self.total_levels = 3
        self.level = 1
        self.lives = 3
        self.score = 0
        self.start_time = None

    def init(self):
        self.createGameBox()
        self.start_time = datetime.now()

    def createGameBox(self):
        # vertical lines
        self.screen[self.top_margin - 1: self.rows - self.top_margin + 1, self.left_margin - 1] = \
            Back.RESET + "\u2503"
        self.screen[self.top_margin - 1: self.rows - self.top_margin + 1, self.columns - self.left_margin] = \
            Back.RESET + "\u2503"

        # horizontal lines
        self.screen[self.top_margin - 1, self.left_margin - 1: self.columns - self.left_margin + 1] = \
            Back.RESET + "\u2501"
        self.screen[self.rows - self.top_margin, self.left_margin - 1: self.columns - self.left_margin + 1] = \
            Back.RESET + "\u2501"

        # corners
        self.screen[self.top_margin - 1, self.left_margin - 1] = Back.RESET + "\u250F"
        self.screen[self.top_margin - 1, self.columns - self.left_margin] = Back.RESET + "\u2513"
        self.screen[self.rows - self.top_margin, self.left_margin - 1] = Back.RESET + "\u2517"
        self.screen[self.rows - self.top_margin, self.columns - self.left_margin] = \
            Back.RESET + "\u251B"

    def printInfoBar(self):
        # title
        title = "BRICK SMASH"
        title_margin = self.left_margin + (self.width - len(title)) // 2
        self.screen[self.top_margin - 2, title_margin: title_margin + len(title)] = list(title)
        self.screen[self.top_margin - 2, title_margin - 1] = Style.BRIGHT + " "
        self.screen[self.top_margin - 2, title_margin + len(title)] = Style.RESET_ALL + " "

        # time
        seconds = int((datetime.now() - self.start_time).total_seconds())
        time_text = "{:0>8}".format(str(timedelta(seconds=seconds)))
        self.screen[self.top_margin - 2, self.left_margin: self.left_margin + len(time_text)] = list(time_text)

        # score
        score_text = f"Score: {self.score}"
        self.screen[self.top_margin - 2, self.columns - self.left_margin - len(score_text) + 2: self.columns - self.left_margin + 2] = list(score_text)

        # level
        level_text = f"Level: {self.level}"
        self.screen[self.rows - self.top_margin + 1, self.left_margin: self.left_margin + len(level_text)] = list(level_text)

        # lives
        lives_text = f"Lives: {self.lives}"
        self.screen[self.rows - self.top_margin + 1, self.columns - self.left_margin - len(lives_text) + 1: self.columns - self.left_margin + 2] = list(" " + lives_text)

        # print top info bar
        print(f"\033[{self.top_margin - 2};{self.left_margin}H", end="")
        for w in range(self.width + 2):
            print(self.screen[self.top_margin - 2, self.left_margin + w], end="")

        # print bottom info bar
        print(f"\033[{self.top_margin + self.height + 1};{self.left_margin}H", end="")
        for w in range(self.width + 2):
            print(self.screen[self.top_margin + self.height + 1, self.left_margin + w], end="")


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

            # print full screen
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

                # print(f"\033[{self.top_margin + self.height};0H\n")

            self.printInfoBar()

    # check collision between 2 sprites
    def collideRect(self, sprite1, sprite2):
        return (sprite1.x + sprite1.width >= sprite2.x and sprite1.x <= sprite2.x + sprite2.width) and \
               (sprite1.y + sprite1.height >= sprite2.y and sprite1.y <= sprite2.y + sprite2.height)

    # check collision between a sprite and a sprite group and return all collided sprites
    def spriteCollide(self, sprite, sprite_group):
        collided_sprites = []
        for sp in sprite_group:
            if self.collideRect(sprite, sp):
                collided_sprites.append(sp)

        return collided_sprites

    # check collision between a sprite and a sprite group and return first collided sprite
    def spriteCollideAny(self, sprite, sprite_group):
        for sp in sprite_group:
            if self.collideRect(sprite, sp):
                return sp

        return None

    def incrementScore(self, block_color):
        if block_color == "green":
            self.score += 10
        elif block_color == "yellow":
            self.score += 20
        elif block_color == "red":
            self.score += 30

    def decreaseLives(self):
        self.lives -= 1

    def incrementLevel(self):
        self.level += 1

    def levelComplete(self, blocks):
        for block in blocks:
            if block.color != "blue":
                return False
        return True

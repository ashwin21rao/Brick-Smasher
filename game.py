import os
import numpy as np
import time
from datetime import datetime, timedelta
from colorama import Fore, Back, Style
import config


class Game:
    def __init__(self, width=config.DEFAULT_WINDOW_WIDTH, height=config.DEFAULT_WINDOW_HEIGHT):
        self.width = width  # width of game screen
        self.height = height  # height of game screen

        columns, rows = os.get_terminal_size()
        self.rows = height + 10 if rows < height + 6 else rows  # rows in terminal
        self.columns = width + 20 if columns < width + 6 else columns  # columns in terminal

        # self.rows = height + 10
        # self.columns = width + 20

        self.left_margin = (self.columns - self.width) // 2
        self.right_margin = self.left_margin + ((self.columns - self.width) % 2)
        self.top_margin = (self.rows - self.height) // 2
        self.bottom_margin = self.top_margin + ((self.rows - self.height) % 2)

        self.screen = np.array([[" " for _ in range(self.columns)] for _ in range(self.rows)], dtype=object)
        self.game_window = self.screen[self.top_margin: self.top_margin + self.height,
                                       self.left_margin: self.left_margin + self.width]

        self.FPS = config.FPS
        self.total_levels = config.TOTAL_LEVELS
        self.level = 1
        self.lives = config.TOTAL_LIVES
        self.score = 0
        self.start_time = None
        self.ticks = None
        self.won = False
        self.skip_level = False

        self.ball_speed_coefficient = config.INITIAL_BALL_SPEED_COEFFICIENT
        self.powerup_speed_coefficient = config.INITIAL_POWERUP_SPEED_COEFFICIENT

        self.createGameBox()

    def reset(self):
        self.level = 1
        self.lives = config.TOTAL_LIVES
        self.score = 0
        self.start_time = None
        self.won = False
        self.skip_level = False

    def startTimer(self):
        self.start_time = datetime.now()

    def createGameBox(self):
        # vertical lines
        self.screen[self.top_margin - 1: self.rows - self.bottom_margin + 1, self.left_margin - 1] = \
            Back.RESET + "\u2503"
        self.screen[self.top_margin - 1: self.rows - self.bottom_margin + 1, self.columns - self.right_margin] = \
            Back.RESET + "\u2503"

        # horizontal lines
        self.screen[self.top_margin - 1, self.left_margin - 1: self.columns - self.right_margin + 1] = \
            Back.RESET + "\u2501"
        self.screen[self.rows - self.bottom_margin, self.left_margin - 1: self.columns - self.right_margin + 1] = \
            Back.RESET + "\u2501"

        # corners
        self.screen[self.top_margin - 1, self.left_margin - 1] = Back.RESET + "\u250F"
        self.screen[self.top_margin - 1, self.columns - self.right_margin] = Back.RESET + "\u2513"
        self.screen[self.rows - self.bottom_margin, self.left_margin - 1] = Back.RESET + "\u2517"
        self.screen[self.rows - self.bottom_margin, self.columns - self.right_margin] = \
            Back.RESET + "\u251B"

    def renderCenterText(self, text, y, back=None, fore=None):
        margin = self.left_margin + (self.width - len(text)) // 2
        self.screen[y, margin: margin + len(text)] = list(bytes(text, "utf-8").decode("unicode_escape"))
        if fore is not None:
            self.screen[y, margin - 1] = Fore.__getattribute__(fore.upper()) + " "
            self.screen[y, margin + len(text)] = Fore.RESET + " "

        if back is not None:
            self.screen[y, margin - 1] = Back.__getattribute__(back.upper()) + " "
            self.screen[y, margin + len(text)] = Back.RESET + " "

        return margin

    def printInfoBar(self):
        # title
        title = "BRICK SMASH"
        title_margin = self.left_margin + (self.width - len(title)) // 2
        self.screen[self.top_margin - 2, title_margin: title_margin + len(title)] = list(title)
        self.screen[self.top_margin - 2, title_margin - 1] = Style.BRIGHT + " "
        self.screen[self.top_margin - 2, title_margin + len(title)] = Style.RESET_ALL + " "

        # time
        self.ticks = int(
            (datetime.now() - (self.start_time if self.start_time is not None else datetime.now())).total_seconds())
        time_text = "{:0>8}".format(str(timedelta(seconds=self.ticks)))
        self.screen[self.top_margin - 2, self.left_margin - 1: self.left_margin - 1 + len(time_text)] = list(time_text)

        # score
        score_text = f"    Score: {self.score}"
        self.screen[self.top_margin - 2,
                    self.columns - self.right_margin - len(score_text) + 1:
                    self.columns - self.right_margin + 1] = list(score_text)

        # level
        level_text = f"Level: {self.level}"
        self.screen[self.rows - self.bottom_margin + 1,
                    self.left_margin - 1:
                    self.left_margin - 1 + len(level_text)] = list(level_text)

        # lives
        lives_text = f" Lives: {self.lives}"
        self.screen[self.rows - self.bottom_margin + 1,
                    self.columns - self.right_margin - len(lives_text) + 1:
                    self.columns - self.right_margin + 1] = list(lives_text)

        # print top info bar
        print(f"\033[{self.top_margin - 1};{self.left_margin}H", end="")
        for w in range(self.width + 2):
            print(self.screen[self.top_margin - 2, self.left_margin - 1 + w], end="")

        # print bottom info bar
        print(f"\033[{self.rows - self.bottom_margin + 2};{self.left_margin}H", end="")
        for w in range(self.width + 2):
            print(self.screen[self.rows - self.bottom_margin + 1, self.left_margin - 1 + w], end="")

    def printScreen(self, full=False):
        # if terminal too small for game, resize it
        print(f"\033[8;{self.rows};{self.columns}t", end="")

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
                print(f"\033[{self.top_margin + h + 1};{self.left_margin}H" +
                      self.screen[self.top_margin, self.left_margin - 1], end="")

                # print game window
                for w in range(self.width):
                    print(self.game_window[h][w], end="")

                # print(f"\033[{self.top_margin + self.height};0H\n")

        self.printInfoBar()

    def updateScreen(self, sprite_list):
        for sprite in sprite_list:
            sprite.render(self.game_window)

    def clearScreen(self):
        self.game_window.fill(" ")

    def renderStartScreen(self):
        self.clearScreen()

        y = self.top_margin + 5
        self.renderCenterText("Press enter to start, q to quit", y)

        self.renderCenterText("POWERUPS:", y + 3)

        self.renderCenterText("EP: Expand Paddle        SP: Shrink Paddle", y + 5)
        self.renderCenterText("TB: Thru Ball            FI: Fire Ball    ", y + 6)
        self.renderCenterText("MB: Multiply Balls       PG: Paddle Grab  ", y + 7)
        self.renderCenterText("FB: Fast Ball            SB: Slow Ball    ", y + 8)
        self.renderCenterText("SK: Skip Level           XL: Extra Life    ", y + 9)

        self.renderCenterText("BLOCKS:", y + 11)

        m = self.renderCenterText(f"        : 1 hit to break ", y + 13)
        self.screen[y + 13, m - 1] = Back.GREEN + " "
        self.screen[y + 13, m + 7] = Back.RESET + " "

        m = self.renderCenterText(f"        : 2 hits to break", y + 15)
        self.screen[y + 15, m - 1] = Back.YELLOW + " "
        self.screen[y + 15, m + 7] = Back.RESET + " "

        m = self.renderCenterText(f"        : 3 hits to break", y + 17)
        self.screen[y + 17, m - 1] = Back.RED + " "
        self.screen[y + 17, m + 7] = Back.RESET + " "

        m = self.renderCenterText(f"        : Unbreakable    ", y + 19)
        self.screen[y + 19, m - 1] = Back.BLUE + " "
        self.screen[y + 19, m + 7] = Back.RESET + " "

    def renderEndScreen(self):
        self.clearScreen()

        y = self.top_margin + 12
        self.renderCenterText(f"{'You Win!' if self.won else 'Game Over!'}", y)
        self.renderCenterText("Press enter to play again, q to quit", y + 2)

        self.renderCenterText(f"Score: {self.score}", y + 4)
        self.renderCenterText("Time: {:0>8}".format(str(timedelta(seconds=self.ticks))), y + 5)

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

    def addBlockScore(self, block_color, invisible_new_color):
        if block_color == "green":
            self.score += 10
        elif block_color == "yellow":
            self.score += 20
        elif block_color == "red":
            self.score += 30
        elif block_color == "blue":
            self.score += 5
        elif block_color is None:
            self.addBlockScore(invisible_new_color, None)
            self.score += 10

    def addPowerUpScore(self):
        self.score += 20

    def decreaseLives(self):
        self.lives -= 1

    def incrementLevel(self):
        self.level += 1

    def levelComplete(self, blocks):
        for block in blocks:
            if block.color != "blue":
                return False
        return True

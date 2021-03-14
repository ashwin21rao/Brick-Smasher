import os
import numpy as np
from datetime import timedelta
from colorama import Fore, Back, Style


class Screen:
    def __init__(self, width, height):
        self.width = width  # width of game screen
        self.height = height  # height of game screen

        columns, rows = os.get_terminal_size()
        self.rows = height + 10 if rows < height + 6 else rows  # rows in terminal
        self.columns = width + 20 if columns < width + 6 else columns  # columns in terminal

        self.left_margin = (self.columns - self.width) // 2
        self.right_margin = self.left_margin + ((self.columns - self.width) % 2)
        self.top_margin = (self.rows - self.height) // 2
        self.bottom_margin = self.top_margin + ((self.rows - self.height) % 2)

        self.screen = np.array([[" " for _ in range(self.columns)] for _ in range(self.rows)], dtype=object)
        self.game_window = self.screen[self.top_margin: self.top_margin + self.height,
                                       self.left_margin: self.left_margin + self.width]

        self.ticks = None
        self.createGameBox()

    def createGameBox(self):
        # vertical lines
        self.screen[self.top_margin - 1: self.rows - self.bottom_margin + 1, self.left_margin - 1] = \
            Fore.RESET + Back.RESET + "\u2503"
        self.screen[self.top_margin - 1: self.rows - self.bottom_margin + 1, self.columns - self.right_margin] = \
            Fore.RESET + Back.RESET + "\u2503"

        # horizontal lines
        self.screen[self.top_margin - 1, self.left_margin - 1: self.columns - self.right_margin + 1] = \
            Fore.RESET + Back.RESET + "\u2501"
        self.screen[self.rows - self.bottom_margin, self.left_margin - 1: self.columns - self.right_margin + 1] = \
            Fore.RESET + Back.RESET + "\u2501"

        # corners
        self.screen[self.top_margin - 1, self.left_margin - 1] = Fore.RESET + Back.RESET + "\u250F"
        self.screen[self.top_margin - 1, self.columns - self.right_margin] = Fore.RESET + Back.RESET + "\u2513"
        self.screen[self.rows - self.bottom_margin, self.left_margin - 1] = Fore.RESET + Back.RESET + "\u2517"
        self.screen[self.rows - self.bottom_margin, self.columns - self.right_margin] = \
            Fore.RESET + Back.RESET + "\u251B"

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

    def printInfoBar(self, ticks, score, level_num, lives):
        # title
        title = "BRICK SMASH"
        title_margin = self.left_margin + (self.width - len(title)) // 2
        self.screen[self.top_margin - 2, title_margin: title_margin + len(title)] = list(title)
        self.screen[self.top_margin - 2, title_margin - 1] = Style.BRIGHT + " "
        self.screen[self.top_margin - 2, title_margin + len(title)] = Style.RESET_ALL + " "

        # time
        time_text = "{:0>8}".format(str(timedelta(seconds=ticks)))
        self.screen[self.top_margin - 2, self.left_margin - 1: self.left_margin - 1 + len(time_text)] = list(time_text)

        # score
        score_text = f"    Score: {score}"
        self.screen[self.top_margin - 2,
                    self.columns - self.right_margin - len(score_text) + 1:
                    self.columns - self.right_margin + 1] = list(score_text)

        # level
        level_text = f"Level: {level_num}"
        self.screen[self.rows - self.bottom_margin + 1,
                    self.left_margin - 1:
                    self.left_margin - 1 + len(level_text)] = list(level_text)

        # lives
        lives_text = f" Lives: {lives}"
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

    def printScreen(self, ticks, score, level_num, lives, full=False):
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

        self.printInfoBar(ticks, score, level_num, lives)

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
        self.renderCenterText("EX: Explosive Ball       SL: Shoot Lasers  ", y + 7)
        self.renderCenterText("MB: Multiply Balls       PG: Paddle Grab  ", y + 8)
        self.renderCenterText("FB: Fast Ball            SB: Slow Ball    ", y + 9)
        self.renderCenterText("XL: Extra Life           LL: Lose Life     ", y + 10)
        self.renderCenterText("SK: Skip Level                             ", y + 11)

        self.renderCenterText("BLOCKS:", y + 13)

        m = self.renderCenterText(f"        : 1 hit to break ", y + 15)
        self.screen[y + 15, m - 1] = Back.GREEN + " "
        self.screen[y + 15, m + 7] = Back.RESET + " "

        m = self.renderCenterText(f"        : 2 hits to break", y + 17)
        self.screen[y + 17, m - 1] = Back.YELLOW + " "
        self.screen[y + 17, m + 7] = Back.RESET + " "

        m = self.renderCenterText(f"        : 3 hits to break", y + 19)
        self.screen[y + 19, m - 1] = Back.RED + " "
        self.screen[y + 19, m + 7] = Back.RESET + " "

        m = self.renderCenterText(f"        : Unbreakable    ", y + 21)
        self.screen[y + 21, m - 1] = Back.BLUE + " "
        self.screen[y + 21, m + 7] = Back.RESET + " "

        m = self.renderCenterText(f"        : Exploding Brick", y + 23)
        self.screen[y + 23, m - 1] = Back.MAGENTA + " "
        self.screen[y + 23, m + 7] = Back.RESET + " "

    def renderEndScreen(self, won, score, ticks):
        self.clearScreen()

        y = self.top_margin + 12
        self.renderCenterText(f"{'You Win!' if won else 'Game Over!'}", y)
        self.renderCenterText("Press enter to play again, q to quit", y + 2)

        self.renderCenterText(f"Score: {score}", y + 4)
        self.renderCenterText("Time: {:0>8}".format(str(timedelta(seconds=ticks))), y + 5)

# from colorama import init, Fore, Back, Style
#
# init()
#
#
# def printReset(str, sep=" ", end="\n"):
#     print(str + Back.RESET, sep=sep, end=end)
#
#
# printReset(f"{Back.RED}     ", end=" ")
# printReset(f"{Back.GREEN}     ", end=" ")
# printReset(f"{Back.BLUE}     ", end=" ")
# printReset(f"{Back.YELLOW}     ", end="\n")
#
#
# def drawRect(w, h):
#     print(Back.BLUE)
#     printReset(f"{' ' * w}\n" * h)
#
#
# drawRect(7, 3)
# print("Hello", "Hi")

# print("\x1b[8;40;120t") // columns 120, rows 40

import os
import sys
import time
import numpy as np
from colorama import Fore, Back, Style
from rawterminal import RawTerminal as rt
from sprites import Paddle, Ball


class Game:
    def __init__(self, width=60, height=25):
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


game = Game()

# -------------------------------------------------------------------

# lists of obstacles
paddle = type("", (), {})()
blocks = []
balls = []
powerups = []
obstacles = []
sprites = []


def createPaddle(game_width, game_height):
    width = 10
    height = 1

    global paddle
    paddle = Paddle(game_width // 2 - width // 2, game_height - height - 1, width, height, "white", speed=2)
    sprites.append(paddle)


def createBall(paddle):
    width = 2
    height = 1

    ball = Ball(paddle.x + paddle.width // 2 - width // 2, paddle.y - 1, width, height, "green")
    balls.append(ball)
    sprites.append(ball)


def gameloop():
    rt.enableRawMode()
    rt.hideCursor()
    rt.removeKeyboardDelay()

    createPaddle(game.width, game.height)
    createBall(paddle)

    game.printScreen(full=True)

    running = True
    while running:
        # display screen
        game.printScreen()

        # if key has been hit
        if rt.kbhit():
            char = rt.getInputChar()

            # check for events
            if char == 3:
                rt.disableRawMode()
                rt.showCursor()
                rt.resetKeyboardDelay()
                running = False

            # move paddle
            paddle.move(char, game.game_window)

        # move sprites
        for ball in balls:
            ball.move(game.game_window)

        # update display
        game.updateScreen(sprites)

        # gameloop runs based on FPS
        time.sleep(1 / game.FPS)


gameloop()

# {'BLACK': '\x1b[40m', 'BLUE': '\x1b[44m', 'CYAN': '\x1b[46m', 'GREEN': '\x1b[42m', 'LIGHTBLACK_EX': '\x1b[100m', 'LIGHTBLUE_EX': '\x1b[104m', 'LIGHTCYAN_EX': '\x1b[106m', 'LIGHTGREEN_EX': '\x1b[102m', 'LIGHTMAGENTA_EX': '\x1b[105m', 'LIGHTRED_EX': '\x1b[101m', 'LIGHTWHITE_EX': '\x1b[107m', 'LIGHTYELLOW_EX': '\x1b[103m', 'MAGENTA': '\x1b[45m', 'RED': '\x1b[41m', 'RESET': '\x1b[49m', 'WHITE': '\x1b[47m', 'YELLOW': '\x1b[43m'}

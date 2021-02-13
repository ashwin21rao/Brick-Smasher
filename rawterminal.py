import os
import select
import sys
import termios
import atexit


class RawTerminal:
    STDIN_FILENO = sys.stdin.fileno()
    orig_termios = termios.tcgetattr(STDIN_FILENO)

    @classmethod
    def enableRawMode(cls):
        atexit.register(cls.disableRawMode)
        raw = cls.orig_termios.copy()
        raw[3] &= ~(termios.ECHO | termios.ICANON | termios.OPOST)
        termios.tcsetattr(cls.STDIN_FILENO, termios.TCSANOW, raw)

    @classmethod
    def disableRawMode(cls):
        termios.tcsetattr(cls.STDIN_FILENO, termios.TCSANOW, cls.orig_termios)

    @classmethod
    def kbhit(cls):
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    @classmethod
    def getInputChar(cls):
        char = ord(sys.stdin.read(1))  # read character and get code
        return char

    @classmethod
    def hideCursor(cls):
        atexit.register(cls.showCursor)
        print("\033[?25l")

    @classmethod
    def showCursor(cls):
        print("\033[?25h")

    @classmethod
    def removeKeyboardDelay(cls):
        atexit.register(cls.resetKeyboardDelay)

        # print(os.system("xset q"))
        os.system("xset r rate 50 33")

    @classmethod
    def resetKeyboardDelay(cls):
        os.system("xset r rate 500 33")

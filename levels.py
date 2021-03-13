from blocks import Block, RainbowBlock
from ufo import Ufo
from datetime import datetime


class Level:
    def __init__(self, game_width, level_num):
        self.start_time = datetime.now()
        self.level_num = level_num
        self.layout = getattr(LevelLayouts, f"level{level_num}")(game_width)
        self.time_attack_activated = False

    def getBlocks(self):
        return self.layout

    def getStartTime(self):
        return self.start_time

    def activateTimeAttack(self):
        self.time_attack_activated = True

    def timeAttack(self, game_window, blocks, falling_brick_sound):
        for block in blocks:
            block.moveDown(game_window)

        falling_brick_sound.play()


class BossLevel(Level):
    def __init__(self, game_width, level_num):
        super().__init__(game_width, level_num)
        self.blocks, self.ufo = self.layout

    def getUfo(self):
        return self.ufo

    def getBlocks(self):
        return self.blocks


class LevelLayouts:
    @staticmethod
    def level1(game_width):
        blocks = []
        width = 6
        height = 1

        max_horizontal_blocks = 7
        max_vertical_blocks = 7
        start_x = (game_width - (max_horizontal_blocks * width) - (max_horizontal_blocks - 1)) // 2
        start_y = 4
        colors = ["red", "green", "yellow", "blue", "green", "yellow", "red"]

        for r in range(max_vertical_blocks):
            for c in range(max_horizontal_blocks):
                if r in [2, 3, 4] and c in [0, 6]:
                    continue
                if r in [0, 1, 5, 6] and c in [2, 3, 4]:
                    continue
                block = Block(start_x + c * (width + 1), start_y + r * (height + 1), width, height, colors[r])
                blocks.append(block)

        return blocks

    @staticmethod
    def level2(game_width):
        blocks = []
        width = 6
        height = 1

        max_horizontal_blocks = 8
        max_vertical_blocks = 7
        start_x = (game_width - (max_horizontal_blocks * width) - (max_horizontal_blocks - 1)) // 2
        start_y = 4
        colors = ["green", "red", "blue", "yellow", "red", "green", "blue"]

        for r in range(max_vertical_blocks):
            row_start = r if r < max_vertical_blocks // 2 else max_vertical_blocks - r - 1
            for c in range(row_start, row_start + 5):
                if c < row_start:
                    continue
                block = Block(start_x + c * (width + 1), start_y + r * (height + 1), width, height, colors[r])
                blocks.append(block)

        return blocks

    @staticmethod
    def level3(game_width):
        blocks = []
        width = 6
        height = 1

        max_horizontal_blocks = 7
        max_vertical_blocks = 8
        start_x = (game_width - (max_horizontal_blocks * width) - (max_horizontal_blocks - 1)) // 2
        start_y = 4
        colors = ["blue", "red", "rainbow", "rainbow"]

        for r in range(max_vertical_blocks):
            for c in range(max_horizontal_blocks):
                if r not in range(2, 6) and c not in range(2, 5):
                    continue

                color = None
                for i in range(max_vertical_blocks // 2 + 1):
                    if r in [i, max_vertical_blocks - i - 1] or c in [i, max_horizontal_blocks - i - 1]:
                        color = colors[i]
                        break
                if color == "rainbow":
                    block = RainbowBlock(start_x + c * (width + 1), start_y + r * (height + 1), width, height)
                else:
                    block = Block(start_x + c * (width + 1), start_y + r * (height + 1), width, height, color)
                blocks.append(block)

        return blocks

    @staticmethod
    def level4(game_width):
        blocks = []
        width = 6
        height = 1

        max_horizontal_blocks = 7
        max_vertical_blocks = 8
        start_x = (game_width - (max_horizontal_blocks * width) - (max_horizontal_blocks - 1)) // 2
        start_y = 4
        colors = [None, "rainbow", None, "blue"]
        invisible_new_colors = ["red", None, "green", None]

        for r in range(max_vertical_blocks):
            for c in range(max_horizontal_blocks):
                color = None
                invisible_new_color = None
                for i in range(max_vertical_blocks // 2 + 1):
                    if r in [i, max_vertical_blocks - i - 1] or c in [i, max_horizontal_blocks - i - 1]:
                        color = colors[i]
                        invisible_new_color = invisible_new_colors[i]
                        break
                if color == "rainbow":
                    block = RainbowBlock(start_x + c * (width + 1), start_y + r * (height + 1), width, height)
                else:
                    block = Block(start_x + c * (width + 1), start_y + r * (height + 1), width, height, color,
                                  invisible_new_color)
                blocks.append(block)

        return blocks

    @staticmethod
    def level5(game_width):
        blocks = []
        width = 5
        height = 1

        max_horizontal_blocks = 11
        max_vertical_blocks = 11
        start_x = (game_width - (max_horizontal_blocks * width) - (max_horizontal_blocks - 1)) // 2
        start_y = 3

        for r in range(max_vertical_blocks):
            for c in range(max_horizontal_blocks):
                if (r == 5 and c not in [0, 1, 9, 10]) or (c == 5 and r not in [0, 1, 9, 10]) \
                    or (r, c) in [(2, 2), (2, 8), (8, 2), (8, 8)]:
                    block = Block(start_x + c * (width + 1), start_y + r * (height + 1), width, height, type="EXPLOSIVE_BLOCK")
                else:
                    if (r in range(1, 4) and c in range(1, 4)) or (r in range(7, 10) and c in range(1, 4)) or \
                       (r in range(1, 4) and c in range(7, 10)) or (r in range(7, 10) and c in range(7, 10)):
                        color = "yellow"
                    else:
                        color = "red"
                    block = Block(start_x + c * (width + 1), start_y + r * (height + 1), width, height, color)

                blocks.append(block)

        return blocks


    @staticmethod
    def level6(game_width):
        blocks = []

        ufo = Ufo(0, 1, "blue")
        ufo.updatePosition(x=(game_width // 2 - ufo.width // 2))

        return blocks, ufo

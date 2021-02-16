from blocks import Block


class Levels:
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
        colors = ["blue", "red", "yellow", "green"]

        for r in range(max_vertical_blocks):
            for c in range(max_horizontal_blocks):
                if r not in range(2, 6) and c not in range(2, 5):
                    continue

                color = None
                for i in range(max_vertical_blocks // 2 + 1):
                    if r in [i, max_vertical_blocks - i - 1] or c in [i, max_horizontal_blocks - i - 1]:
                        color = colors[i]
                        break
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
        colors = [None, "yellow", None, "blue"]
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
                block = Block(start_x + c * (width + 1), start_y + r * (height + 1), width, height, color,
                              invisible_new_color)
                blocks.append(block)

        return blocks

    @staticmethod
    def level5(game_width):
        blocks = []
        width = 6
        height = 1

        max_horizontal_blocks = 9
        max_vertical_blocks = 7
        start_x = (game_width - (max_horizontal_blocks * width) - (max_horizontal_blocks - 1)) // 2
        start_y = 3
        colors = ["red", "yellow", "green", "blue", "green", "yellow", "red"]
        invisible_new_colors = ["green", "red", "yellow", "blue", "yellow", "red", "green"]

        for r in range(max_vertical_blocks):
            for c in range(max_horizontal_blocks):
                if (r % 2 == 0 and c % 2 == 0) or (r % 2 != 0 and c % 2 != 0):
                    block = Block(start_x + c * (width + 1), start_y + r * (height + 1), width, height, colors[r])
                else:
                    block = Block(start_x + c * (width + 1), start_y + r * (height + 1), width, height, None,
                                  invisible_new_colors[r])
                blocks.append(block)

        return blocks

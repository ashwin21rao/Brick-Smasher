from sprites import MovableSprite, SpriteCollisionMixin


class Ball(MovableSprite, SpriteCollisionMixin):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1, y_speed=-1, launched=False, enable_paddle_grab=False):
        super().__init__(x_coordinate, y_coordinate, width, height, color, x_speed)
        self.y_speed = y_speed
        self.collidable = True
        self.launched = launched
        self.enable_paddle_grab = enable_paddle_grab

    def reflectHorizontal(self):
        self.y_speed *= -1

    def reflectVertical(self):
        self.x_speed *= -1

    def reflectHorizontalAndVertical(self):
        self.x_speed *= -1
        self.y_speed *= -1

    # def checkHorizontalCollision(self, sprite):
    #     return (self.y + self.height == sprite.y and self.y_speed > 0 or self.y == sprite.y + sprite.height and self.y_speed < 0) and \
    #            (self.x + self.width - 1 >= sprite.x and self.x <= sprite.x + sprite.width - 1)
    #
    # def checkVerticalCollision(self, sprite):
    #     return (self.x + self.width == sprite.x and self.x_speed > 0 or self.x == sprite.x + sprite.width and self.x_speed < 0) and \
    #            (self.y + self.height - 1 >= sprite.y and self.y <= sprite.y + sprite.height - 1)
    #
    # def checkCornerCollision(self, sprite):
    #     return not self.checkHorizontalCollision(sprite) and not self.checkVerticalCollision(sprite)

    def handleCornerCollision(self, sprite):
        # top left corner
        if self.x + self.width == sprite.x and self.y + self.height == sprite.y and \
                (self.x_speed > 0 and self.y_speed > 0):
            return True

        # bottom left corner
        if self.x + self.width == sprite.x and self.y == sprite.y + sprite.height and \
                (self.x_speed > 0 and self.y_speed < 0):
            return True

        # top right corner
        if self.x == sprite.x + sprite.width and self.y + self.height == sprite.y and \
                (self.x_speed < 0 and self.y_speed > 0):
            return True

        # bottom right corner
        if self.x == sprite.x + sprite.width and self.y == sprite.y + sprite.height and \
                (self.x_speed < 0 and self.y_speed < 0):
            return True

        return False

    def handleCollision(self, sprite=None, obstacle="block"):
        if obstacle == "block" and self.collidable:
            if self.checkVerticalCollision(sprite):
                self.reflectVertical()
            elif self.checkHorizontalCollision(sprite):
                self.reflectHorizontal()
            elif self.checkCornerCollision(sprite) and self.handleCornerCollision(sprite):
                self.reflectHorizontal()

        elif obstacle == "paddle":
            if self.checkHorizontalCollision(sprite) or \
                    (self.checkCornerCollision(sprite) and self.handleCornerCollision(sprite)):
                self.reflectHorizontal()

                mid = sprite.x + sprite.width // 2 - self.width // 2

                for x in range(sprite.x - 2, sprite.x + sprite.width + 1):
                    if self.x == x:
                        self.x_speed = (abs(x - mid + (1 if x > mid else -1 if x < mid else 0)) // 2) * \
                                       (-1 if x < mid else 1)

                # print(f"hereeeeee {abs(self.x_speed)} {self.x + self.width} {sprite.x}", end="")

                # for x in range(mid+1, self.x + self.width + 1):
                #     if self.x == x:
                #         self.x_speed = (x - mid + 1) / 2
                # for x in range(self.x - 2, mid):
                #     if self.x == x:
                #         self.x_speed = (x - mid - 1) / 2

                # if self.x == sprite.x + sprite.width // 2 - self.width // 2:
                #     self.x_speed = 0
                # elif self.x > sprite.x + sprite.width // 2 - self.width // 2:
                #     self.x_speed = 2
                # else:
                #     self.x_speed = -2

                if self.enable_paddle_grab:
                    self.launched = False

                return True

            return False

    def handleWallCollision(self, game_window):
        game_height, game_width = game_window.shape
        collided = False

        # bounce off side walls
        if self.x + self.width >= game_width or self.x <= 0:
            self.x = 0 if self.x <= 0 else game_width - self.width
            self.reflectVertical()
            collided = True

        # bounce off top wall
        if self.y <= 0 or self.y + self.height >= game_height:
            self.y = 0 if self.y <= 0 else game_height - self.height
            self.reflectHorizontal()
            collided = True

        return collided

    def move(self, game_window, move_y=True):
        # clear old position
        self.clearOldPosition(game_window)

        # move ball
        if self.x_speed != 0:
            self.x += self.x_speed // abs(self.x_speed)
        if move_y:
            self.y += self.y_speed

    def launch(self):
        self.launched = True

    def isDead(self, game_height):
        return self.y + self.height >= game_height

    def disableCollision(self):
        self.collidable = False

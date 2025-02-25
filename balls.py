from sprites import MovableSprite, SpriteCollisionMixin
import numpy as np
from colorama import Back


class Ball(MovableSprite, SpriteCollisionMixin):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1, y_speed=-1, launched=False,
                 enable_paddle_grab=False):
        super().__init__(x_coordinate, y_coordinate, width, height, color, x_speed)
        self.y_speed = y_speed
        self.collidable = True
        self.launched = launched
        self.enable_paddle_grab = enable_paddle_grab
        self.initArray()

    def initArray(self):
        self.array = np.array([[" " for _ in range(self.width)] for _ in range(self.height)], dtype=object)

        self.array[:, 0] = Back.__getattribute__(self.color.upper()) + " "
        self.array[:, self.width - 1] = " " + Back.RESET

    def reflectHorizontal(self):
        self.y_speed *= -1

    def reflectVertical(self):
        self.x_speed *= -1

    def reflectHorizontalAndVertical(self):
        self.x_speed *= -1
        self.y_speed *= -1

    def handleCornerCollision(self, sprite):
        # top left corner
        if self.hitbox.x + self.hitbox.width == sprite.hitbox.x and self.hitbox.y + self.hitbox.height == sprite.hitbox.y and \
                (self.x_speed > 0 and self.y_speed > 0):
            return True

        # bottom left corner
        if self.hitbox.x + self.hitbox.width == sprite.hitbox.x and self.hitbox.y == sprite.hitbox.y + sprite.hitbox.height and \
                (self.x_speed > 0 and self.y_speed < 0):
            return True

        # top right corner
        if self.hitbox.x == sprite.hitbox.x + sprite.hitbox.width and self.hitbox.y + self.hitbox.height == sprite.hitbox.y and \
                (self.x_speed < 0 and self.y_speed > 0):
            return True

        # bottom right corner
        if self.hitbox.x == sprite.hitbox.x + sprite.hitbox.width and self.hitbox.y == sprite.hitbox.y + sprite.hitbox.height and \
                (self.x_speed < 0 and self.y_speed < 0):
            return True

        return False

    def handleBlockCollision(self, block):
        if self.collidable:
            if self.checkVerticalCollision(block):
                self.reflectVertical()
            elif self.checkHorizontalCollision(block):
                self.reflectHorizontal()
            elif self.checkCornerCollision(block) and self.handleCornerCollision(block):
                self.reflectHorizontal()

    def handlePaddleCollision(self, paddle, paddle_sounds):
        if self.checkHorizontalCollision(paddle) or \
                (self.checkCornerCollision(paddle) and self.handleCornerCollision(paddle)):
            self.reflectHorizontal()

            mid = paddle.x + paddle.width // 2 - self.width // 2

            for x in range(paddle.x - 2, paddle.x + paddle.width + 1):
                if self.x == x:
                    self.x_speed = (abs(x - mid + (1 if x > mid else -1 if x < mid else 0)) // 2) * \
                                   (-1 if x < mid else 1)

            if self.enable_paddle_grab:
                self.launched = False
                paddle_sounds["paddle_grab_sound"].play()
            else:
                paddle_sounds["paddle_bounce_sound"].play()

            return True

        return False

    def handleWallCollision(self, game_window, wall_sound=None):
        game_height, game_width = game_window.shape
        collided = False

        # bounce off side walls
        if self.hitbox.x + self.hitbox.width >= game_width or self.hitbox.x <= 0:
            self.updatePosition(x=(0 if self.x <= 0 else game_width - self.width))
            self.reflectVertical()
            collided = True

        # bounce off top wall
        if self.hitbox.y <= 0 or self.hitbox.y + self.hitbox.height >= game_height:
            self.updatePosition(y=(0 if self.y <= 0 else game_height - self.height))
            self.reflectHorizontal()
            collided = True

        if collided and wall_sound is not None:
            wall_sound.play()

        return collided

    def handleUfoCollision(self, ufo):
        if self.checkVerticalCollision(ufo):
            self.reflectVertical()
            return True
        elif self.checkHorizontalCollision(ufo):
            self.reflectHorizontal()
            return True
        elif self.checkCornerCollision(ufo) and self.handleCornerCollision(ufo):
            self.reflectHorizontal()
            return True

        return False

    def move(self, game_window, move_y=True):
        # clear old position
        self.clearOldPosition(game_window)

        # move ball
        if self.x_speed != 0:
            self.updatePosition(x=(self.x + self.x_speed // abs(self.x_speed)))
        if move_y:
            self.updatePosition(y=(self.y + self.y_speed))

    def launch(self):
        self.launched = True

    def isDead(self, game_height):
        return self.y + self.height >= game_height

    def disableCollision(self):
        self.collidable = False

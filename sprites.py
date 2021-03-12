from colorama import Back


# generic sprite
class Sprite:
    def __init__(self, x_coordinate, y_coordinate, width, height, color):
        self.x = x_coordinate
        self.y = y_coordinate
        self.width = width
        self.height = height
        self.color = color
        self.array = None
        self.initHitBox()

    def initHitBox(self):
        self.hitbox = Hitbox(self.x, self.y, self.width, self.height)

    def render(self, game_window):
        game_window[self.y: self.y + self.height, self.x: self.x + self.width] = self.array

        # game_width = game_window.shape[1]

        # if self.color is not None:
        #     if self.x < game_width:
        #         game_window[self.y: self.y + self.height, self.x] = Back.__getattribute__(self.color.upper()) + " "
        #     if self.x + self.width < game_width:
        #         game_window[self.y: self.y + self.height, self.x + self.width] = Back.RESET + " "

    def clearOldPosition(self, game_window):
        game_window[self.y: self.y + self.height, self.x: self.x + self.width] = " "

        # game_width = game_window.shape[1]

        # if self.x < game_width:
        #     game_window[self.y: self.y + self.height, self.x] = " "
        # if self.x + self.width < game_width:
        #     game_window[self.y: self.y + self.height, self.x + self.width] = " "

    def updatePosition(self, x=None, y=None, update_hitbox=True):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        if update_hitbox:
            self.updateHitbox(x, y)

    def updateHitbox(self, x=None, y=None, width=None, height=None):
        if x is not None:
            self.hitbox.x = x
        if y is not None:
            self.hitbox.y = y
        if width is not None:
            self.hitbox.width = width
        if height is not None:
            self.hitbox.height = height

    def setColor(self, color):
        self.color = color
        self.array[:, 0] = Back.__getattribute__(self.color.upper()) + " "


# hitbox for sprite
class Hitbox():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height


# generic sprite movable with arrow keys (left and right)
class MovableSprite(Sprite):
    def __init__(self, x_coordinate, y_coordinate, width, height, color, x_speed=1):
        super().__init__(x_coordinate, y_coordinate, width, height, color)
        self.x_speed = x_speed

    def moveLeft(self, game_window, speed=None):
        self.clearOldPosition(game_window)

        if speed is None:
            speed = abs(self.x_speed)

        self.updatePosition(x=(self.x - speed if self.x - speed > -1 else 0))

    def moveRight(self, game_window, speed=None):
        self.clearOldPosition(game_window)

        game_width = game_window.shape[1]
        if speed is None:
            speed = abs(self.x_speed)

        self.updatePosition(x=(self.x + speed if self.x + self.width + speed <= game_width else game_width - self.width))

    def setSpeed(self, x_speed):
        self.x_speed = x_speed


# generic sprite with collision checking helper functions
class SpriteCollisionMixin:
    def checkHorizontalCollision(self, sprite):
        return (self.hitbox.y + self.hitbox.height == sprite.hitbox.y and self.y_speed > 0 or self.hitbox.y == sprite.hitbox.y + sprite.hitbox.height and self.y_speed < 0) and \
               (self.hitbox.x + self.hitbox.width - 1 >= sprite.hitbox.x and self.hitbox.x <= sprite.hitbox.x + sprite.hitbox.width - 1)

    def checkVerticalCollision(self, sprite):
        return (self.hitbox.x + self.hitbox.width == sprite.hitbox.x and self.x_speed > 0 or self.hitbox.x == sprite.hitbox.x + sprite.hitbox.width and self.x_speed < 0) and \
               (self.hitbox.y + self.hitbox.height - 1 >= sprite.hitbox.y and self.hitbox.y <= sprite.hitbox.y + sprite.hitbox.height - 1)

    def checkCornerCollision(self, sprite):
        return not self.checkHorizontalCollision(sprite) and not self.checkVerticalCollision(sprite)

from powerups import ExpandPaddle, ShrinkPaddle, ThruBall, FireBall, ExplosiveBall, FastBall, SlowBall, ExtraLife, \
                     LoseLife, MultiplyBalls, PaddleGrab, SkipLevel, ShootLaser


# sounds

BACKGROUND_MUSIC = "extras/background.ogg"
BOSS_BACKGROUND_MUSIC = "extras/boss_background.ogg"

REGULAR_BRICK_SOUND = "extras/brick.wav"
INDESTRUCTIBLE_BRICK_SOUND = "extras/indestructible_brick.wav"
EXPLOSIVE_BRICK_SOUND = "extras/explosive_brick.wav"
INVISIBLE_BRICK_SOUND = "extras/invisible_brick.wav"
FALLING_BRICK_SOUND = "extras/falling_bricks.wav"
ACTIVATE_POWERUP_SOUND = "extras/powerup.wav"
PADDLE_SOUND = "extras/paddle_sound.wav"
WALL_SOUND = "extras/wall_sound.wav"
THRU_BALL_SOUND = "extras/thru_ball.wav"
LASER_SOUND = "extras/laser_sound.wav"
PADDLE_GRAB_SOUND = "extras/paddle_grab_sound.wav"


# power up types

POWER_UP_TYPES = {
    ExpandPaddle.type: ExpandPaddle,
    ShrinkPaddle.type: ShrinkPaddle,
    ThruBall.type: ThruBall,
    FireBall.type: FireBall,
    ExplosiveBall.type: ExplosiveBall,
    FastBall.type: FastBall,
    SlowBall.type: SlowBall,
    ExtraLife.type: ExtraLife,
    LoseLife.type: LoseLife,
    MultiplyBalls.type: MultiplyBalls,
    PaddleGrab.type: PaddleGrab,
    SkipLevel.type: SkipLevel,
    ShootLaser.type: ShootLaser
}


# game settings

DEFAULT_WINDOW_WIDTH = 75
DEFAULT_WINDOW_HEIGHT = 34
FPS = 60
TOTAL_LEVELS = 6
TOTAL_LIVES = 3

INITIAL_BALL_SPEED_COEFFICIENT = 3
POWERUP_SPEED_COEFFICIENT = 5
LASER_SPEED_COEFFICIENT = 1
BOMB_SPEED_COEFFICIENT = 2
RAINBOW_BRICK_COLOR_SPEED_COEFFICIENT = 3

POWERUP_SCORE_THRESHOLD = 20
POWERUP_PROBABILITIES = [0.10, 0.10, 0.06, 0.08, 0.08, 0.10, 0.10, 0.06, 0.0, 0.10, 0.10, 0.01, 0.11]
# POWERUP_PROBABILITIES = [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

POWERUP_GENERATION_PROBABILITY = 0.10
POWERUP_ACTIVATION_TIME = 10

TIME_BEFORE_TIME_ATTACK = [120, 120, 240, 240, 240, 360]

TIME_BETWEEN_LASER_SHOTS = 20

TIME_BETWEEN_BOMB_DROPS = 60


def log(string):
    f = open("output.txt", "a")
    f.write(string)
    f.close()

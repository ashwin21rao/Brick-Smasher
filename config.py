from powerups import ExpandPaddle, ShrinkPaddle, ThruBall, FireBall, FastBall, SlowBall, ExtraLife, MultiplyBalls, \
                     PaddleGrab, SkipLevel

POWER_UP_TYPES = {
    ExpandPaddle.type: ExpandPaddle,
    ShrinkPaddle.type: ShrinkPaddle,
    ThruBall.type: ThruBall,
    FireBall.type: FireBall,
    FastBall.type: FastBall,
    SlowBall.type: SlowBall,
    ExtraLife.type: ExtraLife,
    MultiplyBalls.type: MultiplyBalls,
    PaddleGrab.type: PaddleGrab,
    SkipLevel.type: SkipLevel
}

DEFAULT_WINDOW_WIDTH = 75
DEFAULT_WINDOW_HEIGHT = 34
FPS = 60
TOTAL_LEVELS = 5
TOTAL_LIVES = 3

INITIAL_BALL_SPEED_COEFFICIENT = 3
INITIAL_POWERUP_SPEED_COEFFICIENT = 5

POWERUP_SCORE_THRESHOLD = 20
POWERUP_PROBABILITIES = [0.10, 0.18, 0.065, 0.10, 0.18, 0.10, 0.06, 0.11, 0.10, 0.005]

POWERUP_GENERATION_PROBABILITY = 0.50
POWERUP_ACTIVATION_TIME = 10

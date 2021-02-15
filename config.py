from powerups import ExpandPaddle, ShrinkPaddle, ThruBall, FastBall, SlowBall, ExtraLife, MultiplyBalls, PaddleGrab

POWER_UP_TYPES = {
    ExpandPaddle.type: ExpandPaddle,
    ShrinkPaddle.type: ShrinkPaddle,
    ThruBall.type: ThruBall,
    FastBall.type: FastBall,
    SlowBall.type: SlowBall,
    ExtraLife.type: ExtraLife,
    MultiplyBalls.type: MultiplyBalls,
    PaddleGrab.type: PaddleGrab
}

DEFAULT_WINDOW_WIDTH = 75
DEFAULT_WINDOW_HEIGHT = 34
FPS = 60
TOTAL_LEVELS = 3
TOTAL_LIVES = 3

INITIAL_BALL_SPEED_COEFFICIENT = 3
INITIAL_POWERUP_SPEED_COEFFICIENT = 5

POWERUP_SCORE_THRESHOLD = 20
POWERUP_PROBABILITIES = [0.10, 0.15, 0.125, 0.15, 0.10, 0.11, 0.14, 0.125]

POWERUP_GENERATION_PROBABILITY = 0.05

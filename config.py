from powerups import ExpandPaddle, ShrinkPaddle, ThruBall, FastBall, SlowBall, ExtraLife, MultiplyBalls, PaddleGrab

POWER_UP_TYPES = {
    ExpandPaddle.type: ExpandPaddle,
    ShrinkPaddle.type: ShrinkPaddle,
    # ThruBall.type: ThruBall,
    # FastBall.type: FastBall,
    # SlowBall.type: SlowBall,
    # ExtraLife.type: ExtraLife,
    # MultiplyBalls.type: MultiplyBalls,
    PaddleGrab.type: PaddleGrab
}

INITIAL_BALL_SPEED_COEFFICIENT = 3
INITIAL_POWERUP_SPEED_COEFFICIENT = 5
FPS = 60

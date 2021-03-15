import sys
import time
from datetime import datetime
from game import Game
from rawterminal import RawTerminal as rt


# game object
game = Game()


def startScreen():
    game.reset()
    game.renderStartScreen()
    game.printScreen(full=True)
    sys.stdout.flush()

    running = True
    while running:

        # if key has been hit
        if rt.kbhit():
            char = rt.getInputChar()

            # check for events
            if char == 3 or char == 113:
                rt.disableRawMode()
                rt.showCursor()
                return False

            # start game
            if char == 10:
                game.clearScreen()
                return True


def endScreen():
    rt.resetKeyboardDelay()
    game.renderEndScreen()
    game.printScreen()
    sys.stdout.flush()

    running = True
    while running:

        # if key has been hit
        if rt.kbhit():
            char = rt.getInputChar()

            # check for events
            if char == 3 or char == 113:
                rt.disableRawMode()
                rt.showCursor()
                return False

            # restart game
            if char == 10:
                return True


def gameloop():
    game.init()

    # changing speed and delay wrt fps
    counters = {"move_ball": {"count": 0, "coeff_name": "ball_speed_coefficient"},
                "move_powerup": {"count": 0, "coeff_name": "powerup_speed_coefficient"},
                "move_laser": {"count": 0, "coeff_name": "laser_speed_coefficient"},
                "move_bomb": {"count": 0, "coeff_name": "bomb_speed_coefficient"},
                "shoot_laser": {"count": 0, "coeff_name": "time_between_laser_shots"},
                "drop_bomb": {"count": 0, "coeff_name": "time_between_bomb_drops"},
                "change_rainbow_brick_color": {"count": 0, "coeff_name": "rainbow_brick_color_speed_coefficient"},
                "change_ufo_color": {"count": 0, "coeff_name": "ufo_color_speed_coefficient"}}

    running = True
    started = False
    done = False
    while running:

        # show end screen
        if done:
            if not endScreen():
                break
            started = False
            done = False

        # show start screen
        if not started:
            if not startScreen():
                break
            started = True
            game.restart()

        # if key has been hit
        if rt.kbhit():
            char = rt.getInputChar()

            # check for events
            if char == 3 or char == 113:
                rt.disableRawMode()
                rt.showCursor()
                rt.resetKeyboardDelay()
                running = False

            elif char == 32:
                game.skip_level = True

            # move paddle based on keypress
            game.movePaddle(char)

            # launch ball based on keypress
            for ball in game.balls:
                if not ball.launched:
                    game.launchBall(char, ball)

        # change color of rainbow bricks
        if counters["change_rainbow_brick_color"]["count"] == 0:
            for block in game.blocks:
                if block.type == "RAINBOW_BLOCK":
                    block.changeColor()

        # change color of ufo
        if counters["change_ufo_color"]["count"] == 0:
            if game.boss_level_activated:
                game.ufo.reverseColors()

        # activate time attack
        if not game.level.time_attack_activated:
            if int((datetime.now() - game.level.start_time).total_seconds()) > \
                    game.time_before_time_attack[game.level.level_num-1]:
                game.level.activateTimeAttack()

        # drop bombs if boss level
        if counters["drop_bomb"]["count"] == 0:
            if game.boss_level_activated:
                game.createBomb()

        # move bombs
        if counters["move_bomb"]["count"] == 0:
            game.moveFallingSprites(game.bombs)

        # move power ups
        if counters["move_powerup"]["count"] == 0:
            game.moveFallingSprites(game.power_ups)

            # deactivate power ups if its time of activation is finished
            game.deactivatePowerUps()

        # move lasers and check collision
        if counters["move_laser"]["count"] == 0:
            for laser in game.lasers:
                laser.move(game.game_window)
                if laser.laserMissed():
                    game.renderAndRemove(game.lasers, laser)
                    break
                elif game.checkLaserHit(laser):
                    game.renderAndRemove(game.lasers, laser)
                    break

        # shoot lasers if activated
        if counters["shoot_laser"]["count"] == 0:
            for power_up in game.activated_power_ups:
                if power_up.type == "SHOOT_LASER":
                    game.lasers.extend(power_up.shootLasers(game.paddle, game.sounds["laser_sound"]))
                    break

        # move balls and check collisions
        if counters["move_ball"]["count"] == 0:
            for ball in game.balls:
                if not ball.launched:
                    continue
                for sp in range(0, abs(ball.x_speed) + (ball.x_speed == 0)):
                    ball.move(game.game_window, move_y=not sp)
                    if ball.isDead(game.game_window.shape[0]):
                        game.renderAndRemove(game.balls, ball)
                        break
                    elif game.checkCollision(ball):
                        break

        # if no more balls left
        if not game.balls:
            game.decreaseLives()
            if game.lives == 0:
                done = True
            else:
                game.respawn()
                time.sleep(0.5)

        # if no lives are left (even if balls are present)
        if game.lives == 0:
            done = True

        # if blocks reached paddle (time attack)
        for block in game.blocks:
            if block.y + block.height == game.paddle.y:
                done = True

        # check if level is complete
        if game.levelComplete(game.blocks) or game.skip_level:
            if game.level.level_num + 1 <= game.total_levels:
                game.advanceLevel()  # go to next level
            else:
                game.won = True
                done = True  # all levels done

        # update display based on FPS
        game.updateDisplay()
        for key in counters.keys():
            counters[key]["count"] = (counters[key]["count"] + 1) % getattr(game, counters[key]["coeff_name"])

        # render based on FPS
        time.sleep(1 / game.FPS)


gameloop()

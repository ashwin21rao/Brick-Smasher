# Brick Smasher

A take on the classic brick breaking game, in the terminal!

## How to Run

- Run ```pip3 install -r requirements.txt```.
- Run ```python3 main.py``` in the terminal.

## Game Design

### Controls

- ```WASD``` or ```IJKL``` keys for movement.
- Move left: ```A/J```, move right: ```D/L```, launch ball: ```W/I```
- ```q``` or ```CTRL+C``` to quit the game.

### Levels

- The game has 5 levels of increasing difficulty and a boss level.

### Settings

- Game settings can be changed in [config.py](config.py).

### Rules

#### Bricks and Points

- Green: 1 hit to break (10 points)
- Yellow: 2 hits to break (20 points)
- Red: 3 hits to break (30 points)
- Blue: Unbreakable (5 points if broken when a powerup is activated)
- Magenta: Exploding brick (5 points)

#### Power Ups

- There is a 10% probability of a power-up being spawned when a block is hit.
- All power-ups are deactivated when the player is respawned (after dying or completion of a level).

1. EP: Expand Paddle (increase paddle size) 
   - 10% chance to spawn
   - Indefinite (deactivates if SP power-up is obtained)
2. SP: Shrink Paddle (decrease paddle size) 
   - 10% chance to spawn
   - Indefinite (deactivates if EP power-up is obtained)
3. TB: Thru Ball (ball can go through bricks and destroy them) 
   - 6% chance to spawn
   - Deactivates after 10 seconds or if FB power-up is obtained
4. FB: Fire Ball (every brick is destroyed by a single hit) 
   - 8% chance to spawn
   - Deactivates after 10 seconds or if TB power-up is obtained
5. EB: Explosive Ball (every brick when hit acts like an explosive brick) 
   - 8% chance to spawn
   - Deactivates after 10 seconds or if FB power-up is obtained
6. MB: Multiply Balls (each ball on the screen is split into two) 
   - 10% chance to spawn
   - Indefinite
7. PG: Paddle Grab (balls can be grabbed by the paddle and launched manually) 
   - 10% chance to spawn
   - Deactivates after 10 seconds
8. SL: Shoot Lasers (lasers shoot from either side of the paddle)
   - 11% chance to spawn
   -  Deactivates after 10 seconds
9. FB: Fast Ball (increase ball speed) 
   - 10% chance to spawn
   - Deactivates after 10 seconds or if SB powerup is obtained
10. SB: Slow Ball (decrease ball speed) 
    - 10% chance to spawn
    - Deactivates after 10 seconds or if FB powerup is obtained
11. XL: Extra Life (increases total lives by 1) 
    - 6% chance to spawn
12. LL: Lose Life (decreases total lives by 1) 
    - 0.5% chance to spawn (spawns as bombs in boss level)
13. SK: Skip Level (automatically go to next level) 
    - 0.5% chance to spawn

#### Time Attack

- After a certain amount of time is spent playing each level, all bricks will start falling down each time the ball
  hits the paddle. If the bricks reach the paddle, the game is over (all lives are lost).

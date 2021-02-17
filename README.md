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

- The game has 5 levels of increasing difficulty.

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
   - 18% chance to spawn
   - Indefinite (deactivates if EP power-up is obtained)
3. TB: Thru Ball (ball can go through bricks and destroy them) 
   - 6.5% chance to spawn
   - Deactivates after 10 seconds or if FB power-up is obtained
4. FB: Fire Ball (every brick is destroyed by a single hit) 
   - 10% chance to spawn
   - Deactivates after 10 seconds or if TB power-up is obtained
5. MB: Multiply Balls (each ball on the screen is split into two) 
   - 11% chance to spawn
   - Indefinite
6. PG: Paddle Grab (balls can be grabbed by the paddle and launched manually) 
   - 10% chance to spawn
   - Deactivates after 10 seconds
7. FB: Fast Ball (increase ball speed) 
   - 18% chance to spawn
   - Deactivates after 10 seconds or if SB powerup is obtained
8. SB: Slow Ball (decrease ball speed) 
   - 10% chance to spawn
   - Deactivates after 10 seconds or if FB powerup is obtained
9. XL: Extra Life (increases total lives by 1) 
   - 6% chance to spawn
10. SK: Skip Level (automatically go to next level) 
    - 0.5% chance to spawn

# Immune Warfare: Cells vs. Viruses
A vertical shooting mini-game.
<img src="https://github.com/Spec-DY/Final-Project/assets/125960879/e90e9d56-3d7e-4626-bea4-b70b813bdc4f" width="800" height="600">


## Description 
This Python-based game titled "Immune Warfare: Cells vs. Viruses." The game is an arcade-style shooter where the player controls a white blood cell, aiming to eliminate viruses and ultimately face a boss virus. 
### Game background story
As a white blood cell, you are the body's silent protector. Your first battle unfolds in the upper respiratory tract, confronting a formidable virus. This encounter is just a hint of the lurking threats. 
Remember, these viruses may harbor a grander plot. Your vigilant journey into the body's hidden depths begins.


## Gameplay
Shooting -> Space<br>
Movement -> Arrow keys<br>
Eliminate 30 viruses, and a powerful Boss Virus will appear.<br>
- ### Boss Fight Screenshot
- <img src="https://github.com/Spec-DY/Final-Project/assets/125960879/fc17ba17-edce-4f36-a93b-5e6667f50a2a" width="800" height="600">


## Guide
To play the game, click "Immune Warfare.exe", you can also run the main.py file and click start in the start menu. Once the game begins, use the left and right arrow keys to move the white blood cell. Press space to shoot at incoming viruses. The aim is to destroy enough viruses before time runs out to trigger the boss fight, 30 kills in this case. Win if boss defeated, while loss if runing out of time or player dead.
Player may customize difficulties by acessing some constant at the begining of the main.py file:

**MIN_SCORE**: The score required for boss fight, set it **lower for easier game**.<br>
**TIME_LIMIT**: Certain score should be reached before this time runout, set it **higher for easier game**.<br>
**BOSS_SHOOT_RATE**: Boss shooting frequency divisor, set it **higher for easier game**.<br>
**FRESH_RATE**: Adjust game fresh rate, set it **lower for easier game**.


## Installation Instructions
  ### Execute exe:
  - Click 'Release' located on the right and download the .rar file
  - Unzip<br>
  - Find Path: "Immune Warfare/dist/Immune Warfare.exe"<br>
  - Double click "Immune Warfare.exe"
  ##### OR
  ### Execute code:
  - Clone the repository from GitHub.
  - Ensure Python is installed on your device.
  - Install Pygame: `pip install pygame`
  - Run the script: `python main.py`
  - 'immuart' folder must include all arts and be same path with main.py.

## Code Review
### Game Initialization and Settings
The game initializes Pygame and sets up constants that define the game's title, window size, colors, and key gameplay parameters.
```python
pygame.init()

# constants
TITLE = "Immune Warfare: Cells vs. Viruses"
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
RED = (255, 0, 0)
# ... other constants
MIN_SCORE = 30  # main goal
MISSION = "Kill {} Viruses".format(MIN_SCORE)
ENDGAME_KILLED = "{} Viruses Eliminated"
RESTART = "Restart"
INGAME_SCORE = "Virus Killed: {}"
INGAME_TIMER = "Time: {}"
FRESH_RATE = 60
TIME_LIMIT = 30  # timer
BOSS_SHOOT_RATE = 100  # lower if you want boss shoot more frequent

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)
```
### Player Character
The Player class represents the player's character, handling its creation, movement, and health.
```python
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = playerimage
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed = 5
        self.health = 5

    def update(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed
```
### Enemy Creation
The Enemy class is responsible for creating enemy virus sprites with random positions and speeds.
```python
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemyimage
        self.rect = self.image.get_rect(center=(random.randint(20, SCREEN_WIDTH - 20), 0))
        self.speed = random.randint(2, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:  # out of screen
            self.kill()
```
### Boss
This class is responsible for creating the boss sprite, handling its movement and attacks
```python
class Boss(pygame.sprite.Sprite):

    def __init__(self, all_sprites_group, enemy_bullets_group):
        """
        Initializes a new boss instance.

        Args:
            all_sprites_group: The group of all sprites.
            enemy_bullets_group: The group of enemy bullets.
        """
        super().__init__()
        self.image = bossimage
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.speed = 3
        self.health = 20
        self.last_shot = pygame.time.get_ticks()
        self.all_sprites = all_sprites_group
        self.enemy_bullets = enemy_bullets_group

    def update(self):
        # boss movement
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed = -self.speed

        # shoot rate
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot > BOSS_SHOOT_RATE:  # 1000ms / shoot rate
            self.shoot()
            self.last_shot = current_time

    def shoot(self):
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        self.enemy_bullets.add(bullet)
        self.all_sprites.add(bullet)
```
### Clean Inputs
Clears any pending input events during certain phases of the game.
```python
def clean_stack():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
```
### Game Loop
In main game loop, there are many variables used to track gaming status, like game_over and boss_fight will trigger main events in the game.
```python
game_over = False
boss = None
boss_fight = False
boss_message_displayed = False
draw_timer = True
```
Boss fight logic handles player's and Boss' health, also manage the status of game_over and boss_fight, if boss_fight not turned False the boss will show up again.
```python
if boss_fight:
    boss.update()
    player_health_bar.update()
    boss_health_bar.health = boss.health
    boss_health_bar.update()
    enemy_bullets.update()

    player_hit = pygame.sprite.spritecollide(
        player, enemy_bullets, True)
    if player_hit:  # hit by boss
        player_health_bar.health -= 1
        player.health -= 1
        if player.health <= 0:
            game_over = True
            boss_fight = False
    boss_hits = pygame.sprite.spritecollide(boss, bullets, True)
    if boss_hits:  # hit by player
        boss.health -= 1
        if boss.health <= 0:
            game_over = True
            boss_fight = False
```

### Major Challenges
#### Clean input and Boss fight
Cleaning input while on the black screen and handling the boss fight logic initially presented significant challenges for me. However, I discovered that setting some status tracking variables and managing them later greatly simplified the process.
#### Rolling background
I've also struggled on how to rolling the background, the solution is incrementing background y position, the condition background_y >= background_size[1] checks whether background_y has reached or exceeded the height of the background image (background_size[1] is the height of the background). If this condition is true, it means the entire height of the background has scrolled past the viewable area of the game window, then set y position back to 0.
```python
background_y += 3  # background rolling speed
if background_y >= background_size[1]:
    background_y = 0
```
#### Game start manu and black screen countdown
I struggled with how to display the player's start menu and implement a black screen countdown with the mission display after the start button is clicked. I realized that, apart from the main game loop, I could set up another loop like this:
```python
if __name__ == "__main__":
    while True:
        startmanu()
        should_restart = main()
        if not should_restart:
            break
```
So, this command ensures that the start menu appears first. Then, after the start button is clicked, I've arranged for a black screen countdown and mission display to occur before the main loop begins.
```python
countdown_with_mission()
running = True
while running:
# main game loop code
```
#### End game logic
There was a time when an error message appeared after the game was over. This occurred because if the player's score was less than the MIN_SCORE, the boss would not appear, nor would it be added to the Boss class. It was impossible to pass boss.health to the end_game() function under these conditions. This issue was resolved by checking if boss is None (indicating no boss fight). In this case, a boss is added to the Boss class, ensuring that the boss has its initial health. Then, the end_game function checks if the boss's health is 0; if it's not, it's considered a loss.
```python
if game_over:
    if boss is None:  # if boss is not instanced (no boss fight)
        boss = Boss(all_sprites, enemy_bullets)
    end_game(score, game_over, boss.health)
    restart_button.drawbutton()
```

Overall, most chanllenges come from learning Pygame documentation:)

## Example Runs
**Code Documentation**: All code files in this repository are thoroughly commented to explain the functionality of different sections and to provide clarity on the logic implemented.<br>
**Text Outputs**: In the folder named test, you will find text files that contain logs generated by the game during its execution. These text outputs can be useful for debugging or understanding the game flow.<br>
Check example gameplay: https://youtu.be/1MF5Z3aItjg

## Testing
Please check the test folder
### `test_main.py`
- **Purpose**: This file is primarily designed to display in-game behavior on the command line. It aids in understanding what the program is executing.
- **Functionalities**:
  - **Function Calls**: Indicates whether a specific function has been called.
  - **Player Actions**: Shows what actions the player has taken.
  - **Conditional Judgments**: Provides results of conditional decisions.
  - **Behind-the-Scenes**: Details what is happening during program black screens.
  - **Problem Identification**: Assists in more intuitively identifying game issues by confirming command line outputs correspond with the game window visuals.

### `simulated_test_end_game.py`
- **Purpose**: To significantly simplify and test one of the functions in the game.
- **Note**: This file serves solely as a test example.

### `test_output.txt`
- **Contents**: Contains the output displayed in the command line when `test_main.py` is executed, capturing the results and behaviors during the test.

## Missing Features / What's Next
### Update Plan:
1. **Allow Player Movement on the Y-axis.**
2. **Add Health Bar for Player:**
   - Before entering the boss fight.
3. **Damage to Player:**
   - When touched by ordinary viruses.
4. **New Bullet Types:**
   - Special bullets for more powerful attacks and explosive effects, in addition to normal bullets.
5. **Red Blood Cells in Non-Boss Battles:**
   - Heals the player upon contact.
6. **Pills in Non-Boss Battles:**
   - Gives the player special bullets upon contact.
7. **Two Additional Characters:**
   a) **T-cell**
      - Less health, stronger laser attacks.
   b) **Macrophage**
      - More health, attacks viruses by contact.
8. **Second Form of Boss:**
   - Full-screen barrage attack when health is below half.

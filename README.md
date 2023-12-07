# Final Project Report

* Student Name:
* Github Username:
* Semester:
* Course:



## Description 
This Python-based game titled "Immune Warfare: Cells vs. Viruses." The game is an arcade-style shooter where the player controls a white blood cell, aiming to eliminate viruses and ultimately face a boss virus. 
### Game background story
As a white blood cell, you are the body's silent protector. Your first battle unfolds in the upper respiratory tract, confronting a formidable virus. This encounter is just a hint of the lurking threats. 
Remember, these viruses may harbor a grander plot. Your vigilant journey into the body's hidden depths begins.


## Key Features
- **Dynamic Enemy Movement:** Viruses move down the screen at varying speeds.
- **Boss Fight:** A challenging boss fight occurs once a certain score is reached.
- **Health Bars:** Both the player and boss have visual health bars.
- **Scoring System:** The game tracks the number of viruses eliminated.
- **Timed Gameplay:** Players have a set amount of time to reach the boss level.
- **Customizable Difficulty:** Player can adjust status for different objects like boss health, player health, etc.

## Guide
To play the game, click "Immune Warfare.exe", you can also run the main.py file and click start in the start menu. Once the game begins, use the left and right arrow keys to move the white blood cell. Press space to shoot at incoming viruses. The aim is to destroy enough viruses before time runs out to trigger the boss fight, 30 kills in this case. Win if boss defeated, while loss if runing out of time or player dead.
Player may customize difficulties by acessing some constant at the begining of the main.py file:

**MIN_SCORE**: The score required for boss fight, set it **lower for easier game**.<br>
**TIME_LIMIT**: Certain score should be reached before this time runout, set it **higher for easier game**.<br>
**BOSS_SHOOT_RATE**: Boss shooting frequency divisor, set it **higher for easier game**.<br>
**FRESH_RATE**: Adjust game fresh rate, set it **lower for easier game**.


## Installation Instructions
  ### Execute exe:
  Find Path: "Immune Warfare/dist/Immune Warfare.exe"<br>Double click "Immune Warfare.exe"
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
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off.


## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_


## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.

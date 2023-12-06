import pygame
import random
import sys

pygame.init()

# constants
TITLE = "Immune Warfare: Cells vs. Viruses"
WIN = "You've Saved The Upper Respiratory Tract!"
LOSE = "The Viruses Have Successfully Invaded The Body"
START = "Start"
BOSS_WORDS = "You've slain my kin. Now, it's time to pay the price!"
MIN_SCORE = 30
MISSION = "Kill {} Viruses".format(MIN_SCORE)
ENDGAME_KILLED = "{} Viruses Eliminated"
RESTART = "Restart"
INGAME_SCORE = "Virus Killed: {}"
INGAME_TIMER = "Time: {}"
FRESH_RATE = 60
TIME_LIMIT = 30
BOSS_SHOOT_RATE = 100  # lower if you want boss shoot more frequent

# game window setting
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(TITLE)

# define color
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

# load image
playerimage = pygame.image.load('immuart/whitecell.png')
playerimage = pygame.transform.scale(playerimage, (70, 70))
enemyimage = pygame.image.load('immuart/virus2.png')
enemyimage = pygame.transform.scale(enemyimage, (70, 70))
bossimage = pygame.image.load('immuart/boss.png')
bossimage = pygame.transform.scale(bossimage, (150, 150))

background = pygame.image.load('immuart/background.jpg').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_size = background.get_size()
background_rect = background.get_rect()
background_y = 0

startimage = pygame.image.load('immuart/cover4.png').convert()
startimage = pygame.transform.scale(startimage, (SCREEN_WIDTH, SCREEN_HEIGHT))

loseimage = pygame.image.load('immuart/lose4.png').convert()
loseimage = pygame.transform.scale(loseimage, (SCREEN_WIDTH, SCREEN_HEIGHT))

winimage = pygame.image.load('immuart/win5.png').convert()
winimage = pygame.transform.scale(winimage, (SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.Font(None, 36)
win_text = font.render(WIN, True, BLACK)
win_rect = win_text.get_rect(center=(SCREEN_WIDTH / 2, 200))

lose_text = font.render(LOSE, True, RED)
lose_rect = lose_text.get_rect(center=(SCREEN_WIDTH / 2, 200))

boss_max_health = 20
player_max_health = 5


class Player(pygame.sprite.Sprite):
    """
    Represents the player character in the game.

    This class is responsible for creating the player's sprite,
    handling its movement, and managing its health.

    Attributes:
        image (Surface): The image representing the player.
        rect: The rectangular area of the player image.
        speed (int): The movement speed of the player.
        health (int): The health of the player.
    """

    def __init__(self):
        """Initializes a new player instance."""
        super().__init__()
        self.image = playerimage
        self.rect = self.image.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        self.speed = 5
        self.health = 5

    def update(self, keys):
        """
        Updates the player's position based on keyboard input.

        Args:
            keys (List[bool]): A list of boolean values
            representing the state of each keyboard key.
        """
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed


class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy virus in the game.

    This class is used to create enemy virus sprites,
    define their behavior, and handle their movement.

    Attributes:
        image (Surface): The image representing the enemy.
        rect: The rectangular area of the enemy image.
        speed (int): The movement speed of the enemy.
    """

    def __init__(self):
        """
        Initializes a new enemy instance with random position and speed.
        """
        super().__init__()
        self.image = enemyimage
        self.rect = self.image.get_rect(
            center=(random.randint(20, SCREEN_WIDTH - 20), 0))
        self.speed = random.randint(2, 6)

    def update(self):
        """
        Updates the enemy's position, moving it down the screen.
        """
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet fired by the player.

    This class is used to create bullet sprites and handle their movement.

    Attributes:
        image (Surface): The image representing the bullet.
        rect: The rectangular area of the bullet image.
    """

    def __init__(self, x, y):
        """
        Initializes a new bullet instance.

        Args:
            x (int): The x-coordinate of the bullet's starting position.
            y (int): The y-coordinate of the bullet's starting position.
        """
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """
        Updates the bullet's position, moving it up the screen.
        """
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()


class Button:
    """
    Represents a clickable button in the game.

    This class is used to create interactive buttons for
    the game's interface.

    Attributes:
        rect: The rectangular area of the button.
        text (str): The text displayed on the button.
    """

    def __init__(self, x, y, width, height, text):
        """
        Initializes a new button instance.

        Args:
            x (int): The x-coordinate of the button's position.
            y (int): The y-coordinate of the button's position.
            width (int): The width of the button.
            height (int): The height of the button.
            text (str): The text displayed on the button.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def drawbutton(self):
        """
        Draws the button on the screen.
        """
        pygame.draw.rect(screen, RED, self.rect)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, WHITE)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def is_clicked(self, pos):
        """
        Checks if the button is clicked.

        Args:
            pos (Tuple[int, int]): The x and y coordinates of the mouse click.

        Returns:
            bool: True if the button is clicked, False otherwise.
        """
        return self.rect.collidepoint(pos)


class Boss(pygame.sprite.Sprite):
    """
    Represents the boss enemy in the game.

    This class is responsible for creating the boss sprite,
    handling its movement and attacks.

    Attributes:
        image (Surface): The image representing the boss.
        rect: The rectangular area of the boss image.
        speed (int): The movement speed of the boss.
        health (int): The health of the boss.
        last_shot (int): The timestamp of the last shot fired.
    """

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
        """
        Updates the boss's position and handles shooting.
        """
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
        """
        Creates a new bullet and adds it to the enemy bullets group.
        """
        bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
        self.enemy_bullets.add(bullet)
        self.all_sprites.add(bullet)


class HealthBar(pygame.sprite.Sprite):
    """
    Represents a health bar for the player or boss.

    This class is used to visualize the health of the player or the boss.

    Attributes:
        image (Surface): The image representing the health bar.
        rect (Rect): The rectangular area of the health bar.
        health (int): The current health value.
        player_max_health (int): The maximum health value.
    """

    def __init__(self, x, y, player_max_health):
        """
        Initializes a new health bar instance for the player.

        Args:
            x (int): The x-coordinate of the health bar's position.
            y (int): The y-coordinate of the health bar's position.
            player_max_health (int): The maximum health of the player.
        """
        super().__init__()
        self.image = pygame.Surface((100, 10))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = player_max_health
        self.player_max_health = player_max_health

    def update(self):
        """
        Updates the health bar's display based on the player's current health.
        """
        self.image.fill(RED)
        # calculate health bar length
        health_bar_length = (self.health / self.player_max_health) * 100
        pygame.draw.rect(self.image, GREEN, (0, 0, health_bar_length, 10))


class EnemyHealthBar(pygame.sprite.Sprite):
    """
    Represents a health bar for the boss enemy in the game.

    This class is used to create and update the health bar that displays
    the boss's current health during the boss fight.

    Attributes:
        image (Surface): The image representing the health bar.
        rect (Rect): The rectangular area of the health bar.
        health (int): The current health of the boss.
        boss_max_health (int): The maximum health of the boss.
    """

    def __init__(self, x, y, boss_max_health):
        """
        Initializes a new health bar instance for the boss.

        Args:
            x (int): The x-coordinate of the health bar's position.
            y (int): The y-coordinate of the health bar's position.
            boss_max_health (int): The maximum health of the boss.
        """
        super().__init__()
        self.image = pygame.Surface((300, 10))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = boss_max_health
        self.boss_max_health = boss_max_health

    def update(self):
        """
        Updates the health bar's display based on the boss's current health.
        """
        self.image.fill(RED)
        # calculate health bar length
        health_bar_length = (self.health / self.boss_max_health) * 300
        pygame.draw.rect(self.image, GREEN, (0, 0, health_bar_length, 10))


class EnemyBullet(pygame.sprite.Sprite):
    """
    Represents a bullet fired by the boss.

    This class is used to create bullet sprites fired by the
    boss and handle their movement.

    Attributes:
        image (Surface): The image representing the bullet.
        rect (Rect): The rectangular area of the bullet image.
    """

    def __init__(self, x, y):
        """
        Initializes a new enemy bullet instance.

        Args:
            x (int): The x-coordinate of the bullet's starting position.
            y (int): The y-coordinate of the bullet's starting position.
        """
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        """
        Updates the bullet's position, moving it down the screen.
        """
        self.rect.y += 5
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


def startmanu():
    """display start manu image and a start button

    This function loads the start menu image, creates a start button,
    and handles the event loop for the start menu.
    The game proceeds when the start button is clicked.
    """
    screen.blit(startimage, (0, 0))
    start_button = Button(300, 250, 200, 50, START)
    start_button.drawbutton()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.is_clicked(pygame.mouse.get_pos()):
                    return
        screen.blit(startimage, (0, 0))
        start_button.drawbutton()
        pygame.display.flip()
        clock.tick(FRESH_RATE)


# score higher than MIN_SCORE
def boss_message():
    """display boss message with 3 seconds black screen
    This function shows a message from the boss
    and a countdown on a black screen.
    It is used to transition into the boss fight.
    """
    font = pygame.font.Font(None, 45)
    alert_text = font.render(BOSS_WORDS, True, WHITE)
    alert_rect = alert_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
    screen.blit(alert_text, alert_rect)
    countdown_time = 3
    start_ticks = pygame.time.get_ticks()  # start time

    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / \
            1000  # calculate time passed
        if seconds > countdown_time:
            break  # countdown end
        screen.fill(BLACK)

        # countdown text display
        font_big = pygame.font.Font(None, 74)
        countdown_text = font_big.render(
            str(countdown_time - int(seconds)), True, WHITE)
        countdown_rect = countdown_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(countdown_text, countdown_rect)
        screen.blit(alert_text, alert_rect)

        # Handle events during the countdown
        clean_stack()
        pygame.display.flip()
        clock.tick(FRESH_RATE)


def countdown_with_mission():
    """This function shows a 3-second countdown
    and the mission objective on a black screen.
    It is used to start the game after clicking the start button.
    """
    countdown_time = 3
    start_ticks = pygame.time.get_ticks()  # start time

    while True:
        seconds = (pygame.time.get_ticks() - start_ticks) / \
            1000  # calculate time passed
        if seconds > countdown_time:
            break  # countdown end
        screen.fill(BLACK)

        # countdown text display
        font_big = pygame.font.Font(None, 74)
        countdown_text = font_big.render(
            str(countdown_time - int(seconds)), True, WHITE)
        countdown_rect = countdown_text.get_rect(
            center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(countdown_text, countdown_rect)

        # mission text display
        font_small = pygame.font.Font(None, 50)
        mission_text_render = font_small.render(MISSION, True, WHITE)
        mission_rect = mission_text_render.get_rect(
            center=(SCREEN_WIDTH / 2, 150))
        screen.blit(mission_text_render, mission_rect)

        # Handle events during the countdown
        clean_stack()
        pygame.display.flip()
        clock.tick(FRESH_RATE)


def end_game(score, game_over, boss_health):
    """Record current score and display it with image in end game.

    Args:
        score (int): The player's score.
        game_over (bool): Whether the game is over.
        boss_health (int): The health of the boss.

    Returns:
        None

    This function displays the win or lose screen depending on the game's outcome,
    along with the final score.
    """
    if game_over:
        if boss_health < 1:
            screen.blit(winimage, (0, 0))
            screen.blit(win_text, win_rect)
            viruskilled = font.render(
                ENDGAME_KILLED.format(score), True, BLACK)  # black text
        else:
            screen.blit(loseimage, (0, 0))
            screen.blit(lose_text, lose_rect)
            viruskilled = font.render(
                ENDGAME_KILLED.format(score), True, RED)  # red text

        viruskilled_rect = viruskilled.get_rect(center=(SCREEN_WIDTH / 2, 150))
        screen.blit(viruskilled, viruskilled_rect)


def score_display(score):
    """Displays the current score during gameplay.

    Args:
        score (int): The current score of the player.

    Returns:
        None

    This function renders the current score on the game screen during gameplay.

    """
    score_text = font.render(INGAME_SCORE.format(score), True, WHITE)
    screen.blit(score_text, (10, 10))



def timer_display(time_remaining):
    """Displays the remaining time during gameplay.

    Args:
        time_remaining (int): The remaining time in the game.

    Returns:
        None

    This function shows the remaining time on the game screen,
    updating continuously during gameplay.
    """
    timer_text = font.render(INGAME_TIMER.format(time_remaining), True, WHITE)
    screen.blit(timer_text, (SCREEN_WIDTH - 150, 10))


def clean_stack():
    """Clears any pending input events during certain phases of the game.

    This function prevents unintentional actions during specific phases of the game,
    such as black screens or countdowns, by clearing the event queue.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


# Main game function
def main():
    """The main game loop"""
    # status initialization
    player = Player()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    score = 0
    game_over = False
    restart_button = Button(300, 250, 200, 50, RESTART)
    global background_y

    boss = None
    boss_fight = False
    boss_message_displayed = False
    player_health_bar = HealthBar(SCREEN_WIDTH // 2, 590, player_max_health)
    boss_health_bar = EnemyHealthBar(SCREEN_WIDTH // 2, 10, boss_max_health)
    enemy_bullets = pygame.sprite.Group()
    draw_timer = True
    countdown_with_mission()
    start_ticks = pygame.time.get_ticks()

    # game loop
    running = True
    while running:
        time_elapsed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_remaining = max(TIME_LIMIT - time_elapsed, 0)  # time limit

        if not game_over and time_remaining == 0 and score < MIN_SCORE:  # low score fail
            game_over = True

        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)
            enemies.update()
            bullets.update()
            enemy_bullets.update()

            background_y += 3  # background rolling speed
            if background_y >= background_size[1]:
                background_y = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = Bullet(player.rect.centerx, player.rect.top)
                    bullets.add(bullet)
                    all_sprites.add(bullet)
            elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
                mouse_pos = event.pos
                if restart_button.is_clicked(mouse_pos):
                    main()

        screen.blit(background, (0, background_y - background_size[1]))
        screen.blit(background, (0, background_y))

        if random.randint(1, 30) == 1:
            enemy = Enemy()
            enemies.add(enemy)
            all_sprites.add(enemy)

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            score += 1

        # BOSS fight condition
        if not boss_fight and score >= MIN_SCORE and not game_over and not boss_message_displayed:  # if high score then go boss fight
            boss_message()
            draw_timer = False  # hide timer
            boss = Boss(all_sprites, enemy_bullets)  # boss instance
            boss_fight = True
            all_sprites.add(boss)
            boss_message_displayed = True

        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)

        # display health bar in boss fight
        if boss_fight:
            screen.blit(player_health_bar.image, player_health_bar.rect)
            screen.blit(boss_health_bar.image, boss_health_bar.rect)

        # In game time/score display
        score_display(score)
        if draw_timer:
            timer_display(time_remaining)

        # BOSS fight logic
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

        # To ending Surface
        if game_over:
            if boss is None:  # if boss is not instanced (no boss fight)
                boss = Boss(all_sprites, enemy_bullets)
            end_game(score, game_over, boss.health)
            restart_button.drawbutton()

        pygame.display.flip()
        clock.tick(FRESH_RATE)

    pygame.quit()
    return True

# game loop restart
if __name__ == "__main__":
    while True:
        startmanu()
        should_restart = main()
        if not should_restart:
            break

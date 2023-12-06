
import unittest
from main import Player, Enemy, Bullet, Button, Boss, HealthBar, EnemyHealthBar, EnemyBullet

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_initial_health(self):
        self.assertEqual(self.player.health, 5, "Initial health should be 5")

    def test_initial_position(self):
        self.assertEqual(self.player.rect.center, (400, 550), "Initial position is not correct")

class TestEnemy(unittest.TestCase):
    def setUp(self):
        self.enemy = Enemy()

    def test_initial_speed(self):
        self.assertIn(self.enemy.speed, range(2, 7), "Speed should be between 2 and 6")

class TestBullet(unittest.TestCase):
    def setUp(self):
        self.bullet = Bullet(100, 100)

    def test_initial_position(self):
        self.assertEqual(self.bullet.rect.center, (100, 100), "Initial position is not correct")

class TestButton(unittest.TestCase):
    def setUp(self):
        self.button = Button(100, 100, 50, 30, "Test")

    def test_button_label(self):
        self.assertEqual(self.button.text, "Test", "Button label is not correct")

class TestBoss(unittest.TestCase):
    def setUp(self):
        self.boss = Boss(None, None)

    def test_initial_health(self):
        self.assertEqual(self.boss.health, 20, "Initial health should be 20")

class TestHealthBar(unittest.TestCase):
    def setUp(self):
        self.health_bar = HealthBar(100, 100, 5)

    def test_max_health(self):
        self.assertEqual(self.health_bar.player_max_health, 5, "Max health should be 5")

class TestEnemyHealthBar(unittest.TestCase):
    def setUp(self):
        self.enemy_health_bar = EnemyHealthBar(100, 100, 20)

    def test_max_health(self):
        self.assertEqual(self.enemy_health_bar.boss_max_health, 20, "Max health should be 20")

class TestEnemyBullet(unittest.TestCase):
    def setUp(self):
        self.enemy_bullet = EnemyBullet(100, 100)

    def test_initial_position(self):
        self.assertEqual(self.enemy_bullet.rect.center, (100, 100), "Initial position is not correct")

if __name__ == '__main__':
    unittest.main()

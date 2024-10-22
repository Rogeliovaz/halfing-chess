import unittest
from character import Character, CharacterDeath,Player
from coord import Coord


class TestCharacter(unittest.TestCase):

    class TestHero(Character):
        def __init__(self, player):
            super().__init__(player)

        def is_valid_attack(self, target):
            return True  #returning true for testing purposes

        def is_valid_move(self, destination):
            return True

    def setUp(self):
    #Set up a test hero character before each test
        self.hero = self.TestHero(Player.HERO)
        self.villain = self.TestHero(Player.VILLAIN)
        #creating a 6x6 board for testing
        self.board = [[None for x in range(6)] for x in range(6)]

    def test_initialization(self):
    #Test that the character initializes with the correct default values
        self.assertEqual(self.hero.player, Player.HERO)
        self.assertEqual(self.hero.health, 5)
        self.assertEqual(self.hero.temp_health, 5)
        self.assertEqual(self.hero.combat, [3, 3])
        self.assertEqual(self.hero.move, 3)
        self.assertEqual(self.hero.range, 1)

    def test_player_setter(self):
    #Test that the player setter works and raises TypeError on invalid input
        self.hero.player = Player.VILLAIN
        self.assertEqual(self.hero.player, Player.VILLAIN)

        with self.assertRaises(TypeError):
            self.hero.player = "InvalidPlayer"  # Should raise an error

    def test_health_setter(self):
        """Test the health setter, ensuring it sets properly and raises errors on invalid input."""
        self.hero.health = 10
        self.assertEqual(self.hero.health, 10)

        with self.assertRaises(TypeError):
            self.hero.health = "invalid"  # Should raise an error

        with self.assertRaises(ValueError):
            self.hero.health = 0  # Should raise an error for health <= 0

    def test_temp_health_setter(self):
        """Test the temp_health setter, including triggering the CharacterDeath exception."""
        self.hero.temp_health = 3
        self.assertEqual(self.hero.temp_health, 3)

        with self.assertRaises(TypeError):
            self.hero.temp_health = "invalid"  # Should raise an error

        with self.assertRaises(CharacterDeath):
            self.hero.temp_health = -1  # Should trigger CharacterDeath

    def test_combat_setter(self):
        """Test the combat setter for valid and invalid input."""
        self.hero.combat = [4, 5]
        self.assertEqual(self.hero.combat, [4, 5])

        with self.assertRaises(TypeError):
            self.hero.combat = "invalid"  # Should raise an error

        with self.assertRaises(ValueError):
            self.hero.combat = [2]  # Should raise an error (list length != 2)

        with self.assertRaises(ValueError):
            self.hero.combat = [0, 3]  # Should raise an error (combat values <= 0)

    def test_range_setter(self):
        """Test the range setter with valid and invalid values."""
        self.hero.range = 2
        self.assertEqual(self.hero.range, 2)

        with self.assertRaises(TypeError):
            self.hero.range = "invalid"  # Should raise an error

        with self.assertRaises(ValueError):
            self.hero.range = 0  # Should raise an error for range <= 0

    def test_move_setter(self):
        """Test the move setter with valid and invalid values."""
        self.hero.move = 4
        self.assertEqual(self.hero.move, 4)

        with self.assertRaises(TypeError):
            self.hero.move = "invalid"  # Should raise an error

        with self.assertRaises(ValueError):
            self.hero.move = 0  # Should raise an error for move <= 0

    def testIs_valid_move(self):
        from_coord = Coord(0, 0)
        to_coord = Coord(1, 1)
        self.board[0][0] = self.hero  # placing a hero at from_coord
        self.board[1][1] = self.villain  # placing a villain at to_coord
        self.assertTrue(self.hero.is_valid_move(from_coord))

    def testOutOfBounds(self):
        from_coord = Coord(0, 0)
        to_coord = Coord(7, 7)
        self.assertTrue(self.hero.is_valid_move(from_coord))

    def testSameStartAndEnd(self):
        from_coord = Coord(3, 2)
        to_coord = Coord(3, 2)
        self.assertTrue(self.hero.is_valid_move(from_coord))

    def testEndPoint(self):
        pass

    def test_is_valid_attack_good_start(self):
        from_coord = Coord(0, 0)
        to_coord = Coord(1, 1)
        self.board[0][0] = self.hero  # placing a hero at from_coord
        self.board[1][1] = self.villain  # placing a villain at to_coord
        self.assertTrue(self.hero.is_valid_attack(from_coord))

        from_coord2 = Coord(2, 3)
        to_coord2 = Coord(1, 1)
        self.board[0][0] = self.hero  # placing a hero at from_coord
        self.board[1][1] = self.villain  # placing a villain at to_coord
        self.assertTrue(self.hero.is_valid_attack(from_coord2))





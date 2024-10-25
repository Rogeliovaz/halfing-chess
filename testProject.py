import unittest
from character import Character, CharacterDeath,Player
from coord import Coord
from creatures import Villain, Goblin, Skeleton, Necromancer, Hero, Warrior, Mage, Paladin, Ranger


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

    def test_calculate_dice_attack(self):
        definedRolls = [5,4,2,1,6]
        results = self.hero.calculate_dice(attack = True, lst = definedRolls)
        self.assertEqual(results, 3) # Rolls >= 4 [5,4,6]
        undefinedRollsResult = self.hero.calculate_dice(attack = True)
        self.assertTrue(isinstance(undefinedRollsResult, int)) # Random rolls generated, testing it is an int

    def test_calculate_dice_defense(self):
        definedRolls = [1,2,3,4,5]
        results = self.hero.calculate_dice(attack = False, lst = definedRolls)
        self.assertEqual(results, 3)
        undefinedRollsResult = self.hero.calculate_dice(attack = False)
        self.assertTrue(isinstance(undefinedRollsResult, int))

class TestVillain(unittest.TestCase):
    def setUp(self):
        self.villain = Villain()
        self.goblin = Goblin()
        self.skeleton = Skeleton()
        self.necromancer = Necromancer()
        self.board = [[None for _ in range(6)] for _ in range(6)]

    def reset_board(self):
        self.board = [[None for _ in range(6)] for _ in range(6)]

    def board_state(self):
        print("Board State:")
        for row in self.board:
            print(row)

    def test_init(self):
        # Test that the character initializes with the correct default values
        self.assertEqual(self.villain.player, Player.VILLAIN)
        self.assertEqual(self.villain.health, 5)
        self.assertEqual(self.villain.temp_health, 5)
        self.assertEqual(self.villain.combat, [3, 3])
        self.assertEqual(self.villain.move, 3)
        self.assertEqual(self.villain.range, 1)

    def test_diagonal_movement_v1(self):
        # Test diagonal movement
        from_coord = Coord(0, 0)
        to_coord = Coord(1, 1)
        self.assertFalse(self.villain.is_valid_move(from_coord, to_coord, self.board), "diagonal_movement FAILED")

    def test_out_of_movement_range(self):
        self.board[0][0] = self.villain
        from_coord = Coord(0, 0)
        to_coord = Coord(5, 0)
        self.assertFalse(self.villain.is_valid_move(from_coord, to_coord, self.board), "t_out_movement_range FAILED")

    def test_horizontal_movement(self):
        self.reset_board()
        self.board_state
        self.board[0][0] = self.villain
        from_coord = Coord(0, 0)
        to_coord = Coord(0, 0)

    def test_horiz_movement_obstacle(self):
        pass

    def test_vertical_movement(self):
        pass

    def test_vert_movement_obstacle(self):
        pass

    def is_valid_move_true(self):
        self.board[0][0] = self.villain
        from_coord = Coord(0, 0)
        to_coord = Coord(2, 0)
        self.assertTrue(self.villain.is_valid_move(from_coord, to_coord, self.board), "is_valid_move_true FAILED")

    def test_goblin_init(self):
        # Test that the character initializes with the correct default values
        self.assertEqual(self.goblin.player, Player.VILLAIN)
        self.assertEqual(self.goblin.health, 3)
        self.assertEqual(self.goblin.temp_health, 3)
        self.assertEqual(self.goblin.combat, [2, 2])

    def test_skeleton_init(self):
        # Test that the character initializes with the correct default values
        self.assertEqual(self.skeleton.player, Player.VILLAIN)
        self.assertEqual(self.skeleton.health, 2)
        self.assertEqual(self.skeleton.temp_health, 2)
        self.assertEqual(self.skeleton.combat, [2, 1])
        self.assertEqual(self.skeleton.move, 2)

    def test_necromancer_init(self):
        # Test that the character initializes with the correct default values
        self.assertEqual(self.necromancer.player, Player.VILLAIN)
        self.assertEqual(self.necromancer.range, 3)
        self.assertEqual(self.necromancer.combat, [1, 2])

    def test_necromancer_raise_dead(self):
        pass

    def all_villain_types_bad_data(self):
        pass

class TestHero(unittest.TestCase):
    def setUp(self):
        self.hero = Hero()
        self.warrior = Warrior()
        self.mage = Mage()
        # Unsure what to add for paladin
        self.ranger = Ranger()
        self.board = [[None for _ in range(6)] for _ in range(6)]

    def reset_board(self):
        self.board = [[None for _ in range(6)] for _ in range(6)]

    def test_init(self):
        self.assertEqual(self.hero.player, Player.HERO)

    def test_warrior(self):
        self.assertEqual(self.warrior.player, Player.HERO)
        self.assertEqual(self.warrior.health, 7)
        self.assertEqual(self.warrior.temp_health, 7)
        self.assertEqual(self.warrior.combat, [2, 3])

    def test_calculate_dice(self):
        self.assertTrue(self.warrior.calculate_dice)




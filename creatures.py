from typing import Union, List
from character import Character, Player
from coord import Coord
from random import randint


class Villain(Character):
    def __init__(self):
        super().__init__(Player.VILLAIN)

    def is_valid_move(self, from_coord: Coord, to_coord: Coord,
                      board: List[List[Union[None, Character]]]) -> bool:
        """
        Validates a villain's move, ensuring they only move vertically or horizontally up to their maximum move limit,
        and checking for collisions with other characters.

        Args:
            from_coord: The starting position of the villain
            to_coord: The intended destination position of the villain
            board (List[List[Union[None, Character]]]): The game board with characters placed

        Returns:
            bool: True if the move is valid, False otherwise
        """
        # Check base validations using the parents class's is_valid_move method
        if not super().is_valid_move(from_coord, to_coord, board):
            return False

        # Calculate the movement distances in x and y direction
        x_move = abs(to_coord.x - from_coord.x)
        y_move = abs(to_coord.y - from_coord.y)

        # Villains can only move either horizontally or vertically, but not both (No diagonal movements)
        if x_move > 0 and y_move > 0:
            return False  # Diagonal move is invalid

        # Ensure the move does not exceed the Villain's movement range:
        if x_move > self.move or y_move > self.move:
            return False

        # Check for collision: Ensure no other characters are in the path
        if x_move > 0:  # Horizontal move
            movements = 1 if to_coord.x > from_coord.x else -1
            for x in range(from_coord.x + movements, to_coord.x, movements):
                if board[from_coord.y][x] is not None:
                    return False  # There is a character in the way

        elif y_move > 0:  # Vertical move
            movements = 1 if to_coord.y > from_coord.y else -1
            for y in range(from_coord.y + movements, to_coord.y, movements):
                if board[y][from_coord.x] is not None:
                    return False  # There is a character in the way

        return True

    def is_valid_attack(self, from_coord: Coord, to_coord: Coord,
                        board: List[List[Union[None, Character]]]) -> bool:
        """
        Validates a villain's attack, reusing the logic from the parent class

        Args:
            from_coord: The starting position of the villain
            to_coord: The target position for the attack
            board (List[List[Union[None, Character]]]): The game board with characters placed

        Returns:
            bool: True if the move is valid, False otherwise
        """
        return super().is_valid_attack(from_coord, to_coord, board)


class Goblin(Villain):
    def __init__(self):
        super().__init__()
        self.health = 3
        self.temp_health = 3
        self.combat = [2, 2]


class Skeleton(Villain):
    def __init__(self):
        super().__init__()
        self.health = 2
        self.temp_health = 2
        self.combat = [2, 1]
        self.move = 2


class Necromancer(Villain):
    def __init__(self):
        super().__init__()
        self.combat = [1, 2]
        self.range = 3

    def raise_dead(self, target: Character, from_coords: Coord, to_coords: Coord,
                   board: List[List[Union[None, Character]]]):
        """
        Raises a dead character within range. If the target is not a villain, it converts the player type to VILLAIN,
        sets temp_health to half its health (rounded down).

        Args:
            target (Character): The target character to raise from the dead.
            from_coords (Coord ): The necromancer's current position
            to_coords (Coord ): The target's position.
            board (List[List[Union[None, Character]]]): The game board with characters placed
        """
        # Calculates the distance in order to check if the target is in range
        x_move = abs(to_coords.x - from_coords.x)
        y_move = abs(to_coords.y - from_coords.y)

        # Check if move is in range
        if x_move > self.range or y_move > self.range:
            return None

        # Checks if the target is not a Villain type, then sets its
        if target.player != Player.VILLAIN:
            target.player = Player.VILLAIN

        # Checks temp health
        if target.temp_health > 0:
            return None

        # Det the target's temp_health to half its health, rounded down
        target.temp_health = target.health // 2


class Hero(Character):
    def __init__(self):
        super().__init__(Player.HERO)

    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board):
        return super().is_valid_move(from_coord, to_coord, board)

    def is_valid_attack(self, from_coord, to_coord, board):
        return super().is_valid_attack(from_coord, to_coord, board)

    def calculate_dice(self, attack=True, lst: list = [], *args, **kwargs) -> int:
        return super().calculate_dice(attack, lst, *args, **kwargs)

    def deal_damage(self, target, damage, *args, **kwargs):
        return super().deal_damage(target, damage, *args, **kwargs)


class Warrior(Hero):
    def __init__(self):
        super().__init__()
        self.health = 7
        self.temp_health = 7
        self.combat = [2, 4]

    def calculate_dice(self, target: Character, attack=True, lst: list = [], gob: list = []):
        super().calculate_dice(target=target, attack=attack, lst=lst)
        # Using self.__attack if attack = True, otherwise self.__defense
        if attack:
            dice_value = self.combat[0]
            threshold = 5
        else:
            dice_value = self.combat[1]
            threshold = 4

        # Use provided dice rolls if available, otherwise generate random dice rolls
        dice_rolls = lst[:dice_value]
        dice_rolls.extend([randint(1, 6)])

        if attack and isinstance(target, Goblin):
            self.combat[0] += 2
            if not gob:
                dice_rolls.extend([randint(1, 6), randint(1, 6)])

        successfull_rolls = 0
        for num in dice_rolls:
            if num >= threshold:
                successfull_rolls += 1

        return successfull_rolls


class Mage(Hero):
    def __init__(self):
        super().__init__()
        self.combat = [2, 2]
        self.range = 3
        self.move = 2

    def deal_damage(self, target, damage, *args, **kwargs):
        return super().deal_damage(target, damage=damage + 1, *args, **kwargs)


class Paladin(Hero):
    def __init__(self):
        super().__init__()
        self.health = 6
        self.temp_health = 6
        self.__heal = True

    @property
    def heal(self):
        return self.__heal

    @heal.setter
    def heal(self, healed):
        if isinstance(healed, bool):
            self.__heal = healed
        else:
            raise TypeError("healed must be bool")

    def revive(self, target: Character, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]):
        if not self.heal:
            return None

        x_move = abs(to_coord.x - from_coord.x)
        y_move = abs(to_coord.y - from_coord.y)

        # Check if move is out of range
        if x_move > self.range or y_move > self.range:
            return None

        if target.temp_health == 0:
            target.temp_health = target.health // 2

        self.heal = False


class Ranger(Hero):
    def __init__(self):
        super().__init__()
        self.range = 3

    def deal_damage(self, target: Character, damage: int):
        if isinstance(target, Skeleton):
            super().deal_damage(target, damage - 1)
            if damage <= 0:
                self.temp_health = 0
        else:
            super().deal_damage(target, damage)
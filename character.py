from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Union, List
from enum import Enum
from random import randint
from coord import Coord
#from item import Potion


class CharacterDeath(Exception):
    """
        CharacterDeath exception is raised when a character's temporary health falls below 0
        """

    def __init__(self, msg, char: Character):
        """
        Initalizes the CharacterDeath exception with a message and sets the character's temp_health to 0

        Args:
            msg (str): The death message.
            char (Character): The character who has died.
        """
        self.message = msg
        char.temp_health = 0

class InvalidAttack(Exception):
    """
    Custom exception for invaild attacks.
    """
    pass


class Player(Enum):
    """
    Enum representing the player type: HERO or VILLAIN.
    """
    VILLAIN = 0
    HERO = 1
class Character(ABC):
    """
        Abstract base class for all character. Each character has stats such as health, attack, defense, move, and range,
        along with methods for validating moves, attacks, and calculating combat outcomes.
        """

    def __init__(self, player: Player):
        """
        Initializes a character with default stats.

        Args:
            player (Player): the player type (HERO or VILLAIN) controlling this character.
        """
        self.__player = player
        self.__health = 5
        self.__temp_health = 5
        self.__attack = 3
        self.__defense = 3
        self.__move = 3
        self.__range = 1

    @property
    def player(self):
        """Returns the player controlling the character."""

        return self.__player

    @player.setter
    def player(self, player_type: Player):
        """Sets the player controlling the character."""

        if not isinstance(player_type, Player):
            raise TypeError
        else:
            self.__player = player_type

    @property
    def health(self):
        """returns the character's health."""

        return self.__health

    @health.setter
    def health(self, new_health: int):
        """Sets the character's health."""

        if not isinstance(new_health, int):
            raise TypeError

        elif new_health <= 0:
            raise ValueError

        else:
            self.__health = new_health

    @property
    def temp_health(self):
        """Returns the character's temp_health."""
        return self.__temp_health

    @temp_health.setter
    def temp_health(self, new_health: int):
        """Sets the character's temporary health, raises CharacterDeath if the health falls below 0."""

        if not isinstance(new_health, int):
            raise TypeError
        if new_health <= 0:
            self.__temp_health = 0
            raise CharacterDeath(f'{self.__player} has died!', self.player)
        else:
            self.__temp_health = new_health

    @property
    def combat(self):
        """Returns a list of the character's attack and defense stats."""

        return [self.__attack, self.__defense]

    @combat.setter
    def combat(self, combat_lst):
        """
        Sets the character's attack and defense stats.

        Args:
            combat_lst (List[int]): a list containing the attack and defense values.
        """
        if not isinstance(combat_lst, list):
            raise TypeError
        elif len(combat_lst) != 2:
            raise ValueError
        elif combat_lst[0] <= 0 or combat_lst[1] <= 0:
            raise ValueError
        else:
            self.__attack = combat_lst[0]
            self.__defense = combat_lst[1]

    @property
    def range(self):
        """Returns the character's attack range."""

        return self.__range

    @range.setter
    def range(self, new_range: int):
        """Returns the character's attack range"""

        if not isinstance(new_range, int):
            raise TypeError
        elif new_range <= 0:
            raise ValueError
        else:
            self.__range = new_range

    @property
    def move(self):
        """Returns the character's move range."""

        return self.__move

    @move.setter
    def move(self, new_move):
        """Sets the character's move range."""

        if not isinstance(new_move, int):
            raise TypeError
        elif new_move <= 0:
            raise ValueError
        else:
            self.__move = new_move

    @abstractmethod
    def is_valid_move(self, from_coord: Coord, to_coord: Coord,
                      board: List[List[Union[None, Character]]]) -> bool:
        """
        Validates a move based on the board configuration.

        Args:
            from_coord (Coord): the starting coordinate.
            to_coord (Coord): the destination coordinate.
            board (List[List[Union[None, Character]]]): the game board.

        Returns:
            bool: True if the move is valid, False otherwise.
        """
        num_of_rows = len(board)
        num_of_colums = len(board[0])

        # Check if start and end coordinates are within bounds
        if not (0 <= from_coord.x < num_of_colums and 0 <= from_coord.y < num_of_rows
                and 0 <= to_coord.x < num_of_colums and 0 <= to_coord.y < num_of_rows):
            return False

        # Ensure the start and end coordinates are different
        if from_coord.x == to_coord.x and from_coord.y == to_coord.y:
            return False

        # Ensure that self is at the starting location
        if board[from_coord.y][from_coord.x] is not self:
            return False

        # Ensure that the ending location is empty (does not contain another character)
        if board[to_coord.y][to_coord.x] is not None:
            return False

        return True

    @abstractmethod
    def is_valid_attack(self, from_coord: Coord, to_coord: Coord,
                        board: List[List[Union[None, Character]]]) -> bool:
        """
        Validates a move based on the board configuration.

        Args:
            from_coord (Coord): the starting coordinate.
            to_coord (Coord): the destination coordinate.
            board (List[List[Union[None, Character]]]): the game board.

        Returns:
            bool: True if the attack is valid, False otherwise.
        """
        num_of_rows = len(board)
        num_of_colums = len(board[0])

        # Check if start and end coordinates are within bounds
        if not (0 <= from_coord.x < num_of_colums and 0 <= from_coord.y < num_of_rows
                and 0 <= to_coord.x < num_of_colums and 0 <= to_coord.y < num_of_rows):
            return False

        # Ensure the start and end coordinates are different
        if from_coord == to_coord:
            return False

        # Ensure the start location contains self (attacking character)
        if board[from_coord.y][from_coord.x] is not self:
            return False

        # Ensure the end location contains a valid target (not None)
        if board[to_coord.y][to_coord.x] is None:
            return False
        return True

    def calculate_dice(self, attack=True, lst: List = [], *args, **kwargs) -> int:
        """
        Calculates the result of dice rolls for attack or defense

        Args:
            attack (bool): Whether the dice roll is for attack (True) or defense (False)
            lst (List[int]): The list of dice rolls (optional, for testing).

        Returns:
            int: The number of successful rolls (above the threshold)
        """

        # Using self.__attack if attack = True, otherwise self.__defense
        threshold = 4 if attack else 3
        stat_value = self.__attack if attack else self.__defense

        # Use provided dice rolls if available, otherwise generate random dice rolls
        if lst:
            dice_rolls = lst
        else:
            dice_rolls = [randint(1, threshold) for _ in range(stat_value)]

        # Count the number of rolls that meet or exceed the threshold
        sucessfull_rolls = sum(1 for roll in dice_rolls if roll >= threshold)
        return sucessfull_rolls

    def deal_damage(self, target: Character, damage: int, *args, **kwargs) -> None:
        """
        Deals damage to the target character, prints the amount of damage dealt,
        and checks if the target character has died

        Args:
            target (Character): The target character to receive damage.            
            damage (int) : the amount of damage to be dealt.
        """
        try:
            # deduct damage from the target's temp_health
            target.temp_health -= damage

            # print how much damage was dealt in the correct format
            print(f"{target.__class__.__name__} was dealt {damage} damage!")

            # check if the target's temp_health is 0 (character death)
            if target.temp_health == 0:
                raise CharacterDeath(f"{target.player.name} has died!", target)

        except CharacterDeath as e:
            # print death message when a character has died
            print(e.message)

    def __str__(self):
        """
        Returns the name of the character's class

        Returns:
            str: The class name of the character
        """
        # returning the name of the class of the object/character
        return self.__class__.__name__

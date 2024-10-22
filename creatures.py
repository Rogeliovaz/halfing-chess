from typing import List, Union
from character import Character
from abc import ABC, abstractmethod
from coord import Coord
from character import Character

import unittest
from character import Character, CharacterDeath, Player
from coord import Coord
from typing import Optional, Union, List


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
        distance = abs(from_coords.x - to_coords.x) + abs(from_coords.y - to_coords.y)

        # Check if the target is within range
        if distance > self.range:
            return
            # Check if the target's health is 0
        if target.health != 0:
            return

            # If the target is not a VILLAIN player type, convert the player into the VILLAIN player type
        if target.player != Player.VILLAIN:
            target.player = Player.VILLAIN

        # Det the target's temp_health to half its health, rounded down
        target.temp_health = target.health // 2


class Hero(Character):
    def __init__(self):
        super().__init__(Player.HERO)


class Warrior:
    pass


class Mage:
    pass


class Paladin:
    pass


class Ranger:
    pass
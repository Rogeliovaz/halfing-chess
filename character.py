from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional, Union, List
from enum import Enum
from random import randint
from coord import Coord
from item import Potion


class CharacterDeath(Exception):

    def __init__(self, msg, char: Character):
        self.message = msg
        char.temp_health = 0


class InvalidAttack(Exception):
    pass


class Player(Enum):
    VILLAIN = 0
    HERO = 1

class Character(ABC):
    def __init__(self, player: Player):

        self.__player = player
        self.__health = 5
        self.__temp_health = 5
        self.__attack = 3
        self.__defense = 3
        self.__move = 3
        self.__range = 1 

    @property
    def player(self):
        return self.__player
    
    @player.setter
    def player(self, player_type: Player):
        if not isinstance(player_type, Player):
            raise TypeError
        else:
            self.__player = player_type
    
    @property
    def health(self):
        return self.__health
    
    @health.setter
    def health(self, new_health: int):
        if not isinstance(new_health, int):
            raise TypeError
        
        elif new_health <= 0:
            raise ValueError
        
        else:
            self.__health = new_health
    
    @property
    def temp_health(self):
        return self.__temp_health
    
    @temp_health.setter
    def temp_health(self, new_health: int):
        if not isinstance(new_health, int):
            raise TypeError
        if new_health <=0:
            self.__temp_health = 0
            raise CharacterDeath(f'{self.__player} has died!', self)
        else:
            self.__temp_health = new_health

    @property
    def combat(self):
        return [self.__attack, self.__defense]
    
    @combat.setter
    def combat(self, combat_lst):
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
        return self.__range
    
    @range.setter
    def range(self, new_range:int):
        if not isinstance(new_range, int):
            raise TypeError
        elif new_range <= 0:
            raise ValueError
        else:
            self.__range = range
        
    @property
    def move(self):
        return self.__move
    
    @move.setter
    def move(self, new_move):
        if not isinstance(new_move, int):
            raise TypeError
        elif new_move <= 0:
            raise ValueError
        else:
            self.__move = new_move
    
    @abstractmethod
    def is_valid_move(self, from_coord: Coord, to_coord: Coord,
        board: List[List[Union[None, Character]]]) -> bool:

        row_len = len(board)
        col_len = len(board[0])

        # Check if out of bounds
        if from_coord.x > row_len or from_coord.y > col_len:
            if to_coord.x > row_len or to_coord.y > col_len:
                return False
                    
        # Chekcs starting and ending coords are different 
        if from_coord.x == to_coord.x or from_coord.y == to_coord.y:
            return False
        
        # Checks that self is at starting location
        if not isinstance(board[from_coord.y][from_coord.x], Character):
            return False


        # Checks ending location is not None
        if board[to_coord.y][to_coord.x] is not None:
            return False
            

    @abstractmethod
    def is_valid_attack(self, from_coord: Coord, to_coord: Coord,
        board: List[List[Union[None, Character]]]) -> bool:
        
        pass

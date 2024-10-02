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


class InvalidAttack(Exception):
    pass


class Player(Enum):
    VILLAIN = 0
    HERO = 1

class Character(ABC):
    def __init__(self, player: Player, health: int, temp_health:int,
        attack: int, defense:int, move:int, range: int):
        
        if not isinstance(attack, int):
            raise TypeError

        if attack < 0 or defense < 0:
            raise ValueError
        
        if move <= 0 or range <= 0:
            raise ValueError

        self.__player = player
        self.__health = health
        self.__temp_health = temp_health
        self.__attack = attack
        self.__defense = defense
        self.__move = move
        self.__range = range 

    @property
    def player(self):
        return self.__player
    
    @player.setter
    def player(self, player_type: Player):
        if not isinstance(player_type, Player):
            return TypeError
        else:
            self.__player = player_type
    
    @property
    def health(self):
        return self.__health
    
    @health.setter
    def health(self, new_health: int):
        if not isinstance(new_health, int):
            raise TypeError
        else:
            self.__health = new_health
    
    @property
    def temp_health(self):
        return self.__temp_health
    
    @temp_health.setter
    def temp_health(self, new_health: int):
        if not isinstance(new_health, int):
            raise TypeError
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
        else:
            self.__range = range
        
    
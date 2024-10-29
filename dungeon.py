from character import Character, Player
from typing import Optional, Union, List
from abc import ABC, abstractmethod
from random import randint
from coord import Coord
from creatures import Villain, Goblin, Skeleton, Necromancer, Hero, Warrior,Mage, Paladin, Ranger

class Dungeon(ABC):
    def __init__(self, height: int, width: int, villains: List[Villain] = []):

        if not isinstance(height, int):
            raise TypeError
        if not isinstance(width, int):
            raise TypeError
        if not isinstance(villains, list):
            raise TypeError

        if 4 <= height <= 12: #height is the rows
            self.__height = height
        else:
            raise ValueError
        if 4 <= width <= 12: # width is the columns
            self.__width = width
        else:
            raise ValueError

        self.__board = [[None for _ in range(self.__width)] for _ in range(self.__height)]
        self.__player = Player.HERO
        self.__heroes = [Warrior(), Mage(), Paladin(), Ranger()]

        if len(villains) == 0:
            self.generate_villains()

        for x in villains:
            if not isinstance(x, Villain):
                raise TypeError
        self.__villains = villains

        @property
        def height(self):
            #Readable
            return self.__height

        @property
        def width(self):
            #Readable
            return self.__width

        @property
        def board(self):
            #Writeable
            return self.board

        @board.setter
        def board(self, board):
            self.__board = board

        @property
        def player(self):
            #Readable
            return self.__player

        @property
        def heroes(self):
            # readable and writable
            return self.__heroes

        @heroes.setter
        def heroes(self, heroes: List[Hero]):
            self.__heroes = heroes

        @property
        def villains(self):
            return self.__villains

        @villains.setter
        def villains(self, villains: List[Villain]):
            self.__villains = villains

        def generate_villains(self):

            num_of_villains = 0
            if self.height > self.width:
                self.height = num_of_villains

            elif self.height < self.width:
                self.width = num_of_villains

            else:
                self.height = num_of_villains

            villains = []
            while num_of_villains > 0:

                random_villain = randint(1,10)

                if 1 <= random_villain <= 5:
                    villains += Goblin()

                elif 6 <= random_villain <= 8:
                    villains += Skeleton()

                else:

                    if len(villains) == 0:
                        villains += Necromancer()

                    else:
                        villains += Skeleton()

            self.__villains = villains

    def is_valid_move(self, coords: List[Coord]) -> bool:
        pass
    def is_valid_attack(self, coords: List[Coord]) -> bool:
        pass
    def character_at(self, x:int, y:int) -> Character:
        pass
    def set_character_at(self, target: Character, x:int, y:int):
        pass
    def move(self, from_coord: Coord, to_coord: Coord):
        pass
    def attack(self, from_coords: Coord, to_coords: Coord):
        pass
    def set_next_player(self):
        pass
    def print_board(self):
        def print_board(self):
            st = ' \t'
            st += '_____' * len(self.board)
            st += '\n'
            for i in range(len(self.__board)):
                st += f'{i}\t'
                for j in range(len(self.__board[i])):
                    if self.board[i][j] is None:
                        st += '|___|'
                    else:
                        st += f'|{self.board[i][j].__class__.__name__[:3]}|'
                st += '\n'
            st += '\t'
            for i in range(len(self.board[0])):
                st += f'  {i}  '
            print(st)

    def is_dungeon_clear(self) -> bool:
        pass
    def adventurer_defeat(self) -> bool:
        pass
    def place_heroes(self):
        pass
    def place_villains(self):
        pass
    def generate_new_board(self, height: int= -1, width: int=-1):
        pass
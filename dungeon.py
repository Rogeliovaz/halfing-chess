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

        if 4 <= height <= 12:
            self.__height = height
        else:
            raise ValueError

        if 4 <= width <= 12:
            self.__width = width
        else:
            raise ValueError

        self.__board = [[None for _ in range(self.__width)] for _ in range(self.__height)]

        self.__player = Player.HERO

        self.__heroes = [Warrior(), Mage(), Paladin(), Ranger()]

        for x in villains:
            if not isinstance(x, Villain):
                raise TypeError

        if villains:
            self.__villains = villains
        else:
            self.__villains = self.generate_villains()

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, board):
        if not isinstance(board, list):
            raise TypeError
        if len(board) != self.__height:
            raise ValueError
        if len(board[0]) != self.__width:
            raise ValueError
        self.__board = board

    @property
    def player(self):
        return self.__player

    @property
    def heroes(self):
        return self.__heroes

    @heroes.setter
    def heroes(self, heroes: List[Hero]):

        for hero in heroes:
            if not isinstance(hero, Hero):
                raise TypeError
        if not isinstance(heroes, list):
            raise TypeError
        self.__heroes = heroes

    @property
    def villains(self):
        return self.__villains

    @villains.setter
    def villains(self, villains: List[Villain]):
        for villain in villains:
            if not isinstance(villain, Villain):
                raise TypeError
        self.__villains = villains

    def generate_villains(self):
        #setting max_villains to either self.__height or self.__width depending on which is greater
        max_villains = max(self.__height, self.__width)
        villains = []
        necromancer_added = False

        for _ in range(max_villains):
            random_villain = randint(1,10)

            if 1 <= random_villain <= 5:
                villains.append(Goblin())
            elif 6 <= random_villain <= 8:
                villains.append(Skeleton())
            else:
                if not necromancer_added:
                    villains.append(Necromancer())
                    necromancer_added = True
                else:
                    villains.append(Skeleton())

        return villains

    def is_valid_move(self, coords: List[Coord]) -> bool:
        # Ensuring that at least 2 coordinates are provided
        if len(coords) < 2:
            return False

        num_of_rows = len(self.board)
        num_of_columns = len(self.board[0])

        # Iterating through each pair of coordinates ( from one point to the next )
        for character in range(num_of_rows - 1):
            from_coord = coords[character]
            to_coord = coords[character+1]

            # Checking if both from_coord and to_coord are within bounds
            if not (0 <= from_coord.x < num_of_columns and 0 <= from_coord.y < num_of_rows):
                return False
            if not (0 <= to_coord.x < num_of_columns and 0 <= to_coord.y < num_of_rows):
                return False

            # Ensuring that the starting coordinate is not equal to the ending coordinate
            if from_coord.x == to_coord.x and from_coord.y == to_coord.y:
                return False

            # Ensuring there is a character at the starting location
            if not isinstance(self.board[from_coord.x][from_coord.y], Character):
                return False

            # Ensuring the ending location is empty
            if self.__board[from_coord.y][from_coord.x] is not None:
                return False

        return True


    def is_valid_attack(self, coords: List[Coord]) -> bool:
        num_of_rows = len(self.board)
        num_of_columns = len(self.board[0])

        # Iterating through each pair of coordinates ( from one point to the next )
        for character in range(num_of_rows):
            from_coord = coords[character]
            to_coord = coords[character + 1]

            if self.board[from_coord.x][from_coord.y] is None:
                return False
            if self.board[to_coord.x][to_coord.y] is None:
                return False

    def character_at(self, x:int, y:int) -> Character:
        if 0 >= x > len(self.board) and 0 >= y > len(self.board[0]):
            raise ValueError
        else:
            return Character(self.player)

    def set_character_at(self, target: Character, x:int, y:int):
        if 0 >= x > len(self.board) and 0 >= y > len(self.board[0]):
            raise ValueError
        else:
            return target

    def move(self, from_coord: Coord, to_coord: Coord):
        # Ensure the starting coordinate has a character to move
        character = self.board[from_coord.x][from_coord.y]
        if not isinstance(character, Character):
            raise ValueError

        # Ensure the destination coordinate is empty
        if self.board[to_coord.x][to_coord.y] is not None:
            return False

        # Moving the character
        return self.board[to_coord.x][to_coord.y]





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
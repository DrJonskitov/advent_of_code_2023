import math
import re
from collections import Counter 
from dataclasses import dataclass
from functools import cmp_to_key, reduce
from typing import Final

INPUT_PATH: Final[str] = "./day7/input.txt"
TEST_PATH: Final[str] = "./day7/test_input.txt"

JOKER: Final[str] = "J"
ORDER: Final[dict[str, int]] = {"T": 10, JOKER: 1, "Q": 12, "K": 13, "A": 14}
FIVE_OF_A_KIND: Final[int] = 7
FOUR_OF_A_KIND: Final[int] = 6
FULL_HOUSE: Final[int] = 5
THREE_OF_A_KIND: Final[int] = 4
TWO_PAIR: Final[int] = 3
PAIR: Final[int] = 2
HIGH_CARD: Final[int] = 1


@dataclass
class Game:
    hand: list[str]
    rank: int
    jokers: int

class Day7:

    def execute_part1_test(self) -> int:
        lines: list[str] = self.read_input(TEST_PATH)
        return self.execute_part1(lines)

    def execute_part1_input(self) -> int: 
        lines: list[str] = self.read_input(INPUT_PATH)
        return self.execute_part1(lines)
        
    def execute_part2_test(self) -> int:
        lines: list[str] = self.read_input(TEST_PATH)
        return self.execute_part2(lines)

    def execute_part2_input(self) -> int: 
        lines: list[str] = self.read_input(INPUT_PATH)
        return self.execute_part2(lines)

    def execute_part1(self, lines: list[str]) -> int:
        games: list[Game] = self.load_games(lines, False)
        games = sorted(games, key=cmp_to_key(self.compare_games))
        return sum([(index + 1) * game.rank for index, game in enumerate(games)])

    def execute_part2(self, lines: list[str]) -> int:
        games: list[Game] = self.load_games(lines, True)
        games = sorted(games, key=cmp_to_key(self.compare_games))
        return sum([(index + 1) * game.rank for index, game in enumerate(games)])
    
    def load_games(self, lines: list[str], include_jokers: bool) -> list[Game]:
        return map(lambda l : Game(l[0], int(l[1]), self.count_jokers(l[0], include_jokers)), map(lambda line: line.split(), lines))

    def count_jokers(self, hand: str, include_jokers: bool) -> int:
        if not include_jokers:
            return 0
        return hand.count(JOKER)

    def compare_games(self, game1: Game, game2: Game) -> int:
        strenght_1: int = self.get_strength(game1)
        strenght_2: int = self.get_strength(game2)
        if strenght_1 != strenght_2:
            return strenght_1 - strenght_2
        return self.compare_cards(game1.hand, game2.hand)
    
    def compare_cards(self, hand1: str, hand2: str) -> int:
        for card1, card2 in zip(hand1, hand2):
            strength_1: int = self.get_card_strength(card1)
            strength_2: int = self.get_card_strength(card2)
            if strength_1 != strength_2:
                return strength_1 - strength_2
        return 0
    
    def get_strength(self, game: Game) -> int:
        counts = Counter(game.hand) 
        number_of_jokers: int = game.jokers
        most_common, initial_count = counts.most_common(1)[0]
        count = initial_count
        if most_common == JOKER and initial_count < 5:
            second_most_common, second_count = counts.most_common(2)[1]
            count = count + second_count
        if most_common != JOKER:
            count = initial_count + number_of_jokers
        if count == 5:
            return FIVE_OF_A_KIND
        if count == 4:
            return FOUR_OF_A_KIND
        second_most_common, second_count = counts.most_common(2)[1]
        if count == initial_count and second_most_common != JOKER:
            second_count = second_count + number_of_jokers
        if count == 3:
            if second_count == 2:
                return FULL_HOUSE
            return THREE_OF_A_KIND
        if count == 2:                
            if second_count == 2:
                return TWO_PAIR
            return PAIR
        return HIGH_CARD
    
    def get_card_strength(self, card: str) -> int:
        if card.isdigit():
            return int(card)
        return ORDER[card]

    def read_input(self, file_name: str) -> list[str]:
        return [line.rstrip("\n") for line in open(file_name, "r+")]

day: Day7 = Day7()
print("Part 1 test: " + str(day.execute_part1_test()))
print("Part 1 Input: " + str(day.execute_part1_input()))

print("Part 2 test 1: " + str(day.execute_part2_test()))
print("Part 2 Input: " + str(day.execute_part2_input()))
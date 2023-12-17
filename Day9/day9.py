import functools
import re
from typing import Final

INPUT_PATH: Final[str] = "./day9/input.txt"
TEST_PATH: Final[str] = "./day9/test_input.txt"

NumberSequence = list[int]

class Day9:

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
        return sum(map(self.find_final_number, lines))

    def execute_part2(self, lines: list[str]) -> int:
        return sum(map(self.find_initial_number, lines))
    
    def find_initial_number(self, line: str) -> int:
        sequences: list[NumberSequence] = self.find_all_differences(line)
        final: list[int] = [0]
        for sequence in reversed(sequences):
            final.append(sequence[0] - final[-1])
        return final[-1]
    
    def find_final_number(self, line: str) -> int:
        sequences: list[NumberSequence] = self.find_all_differences(line)
        return sum(map(lambda sequence: sequence[-1], sequences))

    def find_all_differences(self, line: str) -> list[NumberSequence]:
        initial_numbers: list[int] = self.load_initial_numbers(line)
        sequences: list[NumberSequence] = [initial_numbers]
        while not self.is_all_zeros(sequences[-1]):
            sequences.append(self.find_differences(sequences[-1]))
        return sequences
    
    def load_initial_numbers(self, line: str) -> list[int]:
        return [int(x) for x in re.findall("\-?\d+", line)]
    
    def is_all_zeros(self, sequence: NumberSequence) -> bool:
        return all(x == 0 for x in sequence)
    
    def find_differences(self, sequence: NumberSequence) -> NumberSequence:
        differences: NumberSequence = []
        for i in range(len(sequence) - 1):
            differences.append(sequence[i + 1] - sequence[i])
        return differences

    def read_input(self, file_name: str) -> list[str]:
        return [line.rstrip("\n") for line in open(file_name, "r+")]

day: Day9 = Day9()
print("Part 1 test: " + str(day.execute_part1_test()))
print("Part 1 Input: " + str(day.execute_part1_input()))

print("Part 2 test 1: " + str(day.execute_part2_test()))
print("Part 2 Input: " + str(day.execute_part2_input()))
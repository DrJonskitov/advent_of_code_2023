import math
import re
from functools import reduce


class Day6:

    def execute_part1_test(self) -> int:
        file_name: str  = "./day6/test_input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part1(lines)

    def execute_part1_input(self) -> int: 
        file_name: str  = "./day6/input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part1(lines)
        
    def execute_part2_test(self) -> int:
        file_name: str  = "./day6/test_input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)

    def execute_part2_input(self) -> int: 
        file_name: str  = "./day6/input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)

    def execute_part1(self, lines: list[str]) -> int:
        times: list[int] = self.get_times(lines[0])
        record_distances: list[int] = self.get_record_distances(lines[1])
        margins: list[int] = self.find_margins(times, record_distances)
        return self.multiply(margins)

    def execute_part2(self, lines: list[str]) -> int:
        time: int = self.get_time(lines[0])
        record_distance: int = self.get_record_distance(lines[1])
        return self.solve(time, record_distance)
    
    def get_times(self, line: str) -> list[int]:
        return self.find_numbers(line)
    
    def get_time(self, line: str) -> int:
        return self.find_merged_number(line)
    
    def get_record_distances(self, line: str) -> list[int]:
        return self.find_numbers(line)
    
    def get_record_distance(self, line: str) -> int:
        return self.find_merged_number(line)

    def find_numbers(self, line: str) -> list[int]:
        return [int(number) for number in re.findall("\d+", line.split(":")[1])]
    
    def find_merged_number(self, line: str) -> int:
        return  int("".join(re.findall("\d+", line.split(":")[1])))
    
    def find_margins(self, times: list[int], distances: list[int]) -> list[int]:
        margins: list[int] = []
        for time, distance in zip(times, distances):
            margins.append(self.solve(time, distance))
        return margins

    def solve(self, time: int, distance: int) -> int:
        discriminant: float = math.sqrt(time * time - 4 * distance)
        x1: float = (time * -1 + discriminant) / -2
        x2: float = (time * -1 - discriminant) / -2
        solutions: list[float] = sorted([x1, x2])
        rounded_sol_1: float = math.ceil(solutions[0])
        rounded_sol_2: float = math.floor(solutions[1])
        solution_1: int = int(rounded_sol_1) if rounded_sol_1 != solutions[0] else int(rounded_sol_1) + 1
        solution_2: int = int(rounded_sol_2) if rounded_sol_2 != solutions[1] else int(rounded_sol_2) - 1
        return abs(solution_1 - solution_2) + 1

    def multiply(self, items: list[int]) -> int:
        return reduce((lambda x, y: x * y), items)

    def read_input(self, file_name: str) -> list[str]:
        return [line.rstrip("\n") for line in open(file_name, "r+")]

day6: Day6 = Day6()
print("Part 1 test: " + str(day6.execute_part1_test()))
print("Part 1 Input: " + str(day6.execute_part1_input()))

print("Part 2 test 1: " + str(day6.execute_part2_test()))
print("Part 2 Input: " + str(day6.execute_part2_input()))
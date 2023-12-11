import functools
import re
from collections import defaultdict 


class Day3:

    def execute_part1_test(self):
        file_name: str  = "./day3/test_input.txt"
        lines: list[str] = self.read_input(file_name)
        visual: list[list[str]] = self.convert_to_visual(lines)
        total = 0
        for numbers, indices in self.find_numbers(visual):
            if (any(self.is_adjecent_to_symbol(index[0], index[1], visual) for index in indices)):
                number: int = int(functools.reduce(lambda x,y : x+y, numbers))
                total = total + number
        return total

    def execute_part1(self):
        file_name = "./day3/input.txt"
        lines: list[str] = self.read_input(file_name)
        visual: list[list[str]] = self.convert_to_visual(lines)
        total = 0
        for numbers, indices in self.find_numbers(visual):
            if (any(self.is_adjecent_to_symbol(index[0], index[1], visual) for index in indices)):
                number: int = int(functools.reduce(lambda x,y : x+y, numbers))
                total = total + number
        return total
    
    def execute_part2(self):
        file_name = "./day3/input.txt"
        lines: list[str] = self.read_input(file_name)
        visual: list[list[str]] = self.convert_to_visual(lines)
        gear_numbers: dict[tuple[int, int], list[int]] = defaultdict(list)
        for numbers, indices in self.find_numbers(visual):
            adjecent_star_indices: list[tuple[int, int]] = self.find_adjecent_stars(indices, visual)
            if len(adjecent_star_indices) > 0:
                for indices in adjecent_star_indices:
                    gear_numbers[indices].append(int(functools.reduce(lambda x,y : x+y, numbers)))
        
        total: int = 0
        for numbers in gear_numbers.values():
            if len(numbers) == 2:
                total = total + (numbers[0] * numbers[1])
        return total

    def read_input(self, file_name: str) -> list[str]:
        return [line.rstrip("\n") for line in open(file_name, "r+")]
    
    def convert_to_visual(self, lines: list[str]) -> list[list[str]]:
        visual: list[list[str]] = []
        for line in lines:
            visual.append([*line])
        return visual
    
    def find_adjecent_stars(self, indices: list[tuple[int, int]], visual: list[list[str]]) -> list[tuple[int, int]]:
        y: int = indices[0][1]
        x: int = indices[0][0]
        adjecent_stars: list[tuple[int, int]] = []
        for y_i in range(y - 1, y + 2):
            if (y_i < 0 or y_i >= len(visual)):
                continue
            for x_i in range(x - 1, x + 1 + len(indices)):
                visual_row: list[str] = visual[y_i]
                if (x_i < 0 or x_i >= len(visual_row)):
                    continue
                if visual_row[x_i] == "*":
                    adjecent_stars.append((x_i, y_i))
        return adjecent_stars
    
    def find_numbers(self, visual: list[list[str]]) -> list[tuple[list[str], list[tuple[int, int]]]]:
        number_data: list[tuple[list[str], list[tuple[int, int]]]] = []
        for y in range(len(visual)):
            visual_row: list[str] = visual[y]
            numbers: list[str] = []
            indices: list[tuple[int, int]] = []
            for x in range(len(visual_row)):
                character: str = visual_row[x]
                if (character.isdigit()):
                    numbers.append(character)
                    indices.append((x, y))
                elif len(numbers) > 0:
                    number_data.append((numbers, indices))
                    numbers = []
                    indices = []
            if len(numbers) > 0:
                number_data.append((numbers, indices))

        return number_data

    def is_adjecent_to_symbol(self, x: int, y: int, visual: list[list[str]]) -> bool:
        for y_i in range(y -1, y + 2):
            if (y_i < 0 or y_i >= len(visual)):
                continue
            for x_i in range(x - 1, x + 2):
                visual_row: list[str] = visual[y_i]
                if (x_i < 0 or x_i >= len(visual_row) or (x_i == 0 and y_i == 0)):
                    continue
                if self.is_symbol(visual_row[x_i]):
                    return True
        return False
            
    def is_symbol(self, item: str) -> bool:
        return not("." == item) and not(item.isdigit())


result: int = Day3().execute_part2()
print(result)
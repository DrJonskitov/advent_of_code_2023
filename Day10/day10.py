from collections.abc import Callable
from dataclasses import dataclass
from typing import Final, TypeVar

@dataclass
class Location:
    x: int
    y: int

@dataclass
class Step:
    src: Location
    center: Location

EAST_WEST: Final[Callable[[Location, Location], Location]] = lambda center, src: Location(center.x + (center.x - src.x), src.y)
NORTH_SOUTH: Final[Callable[[Location, Location], Location]] = lambda center, src: Location(src.x, center.y + (center.y - src.y)) 
SOUTH_EAST: Final[Callable[[Location, Location], Location]] = lambda center, src: Location(center.x + (center.x - src.x + 1), center.y + (center.y - src.y + 1))
NORTH_WEST: Final[Callable[[Location, Location], Location]] = lambda center, src: Location(center.x + (center.x - src.x - 1), center.y + (center.y - src.y - 1))
SOUTH_WEST: Final[Callable[[Location, Location], Location]] = lambda center, src: Location(center.x + (center.x - src.x - 1), center.y + (center.y - src.y + 1))
NORTH_EAST: Final[Callable[[Location, Location], Location]] = lambda center, src: Location(center.x + (center.x - src.x + 1), center.y + (center.y - src.y - 1))


MOVEMENTS: Final[dict[str, Callable[[Location, Location], Location]]] = {"-": EAST_WEST,
                                                                         "|": NORTH_SOUTH,
                                                                         "7": SOUTH_WEST,
                                                                         "J": NORTH_WEST,
                                                                         "F": SOUTH_EAST,
                                                                         "L": NORTH_EAST}

Movement = Callable[[Location, Location], Location]
Grid = list[list[Movement]]

class Day10:

    def execute_part1_test1(self) -> int:
        file_name: str  = "./day10/part1_test_input1.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part1(lines)
    
    def execute_part1_test2(self) -> int: 
        file_name: str  = "./day10/part1_test_input2.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part1(lines)

    def execute_part1_input(self) -> int: 
        file_name: str  = "./day10/input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part1(lines)
        
    def execute_part2_test1(self) -> int:
        file_name: str  = "./day10/part2_test_input1.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)
    
    def execute_part2_test2(self) -> int: 
        file_name: str  = "./day10/part2_test_input2.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)
    
    def execute_part2_test3(self) -> int: 
        file_name: str  = "./day10/part2_test_input3.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)

    def execute_part2_input(self) -> int: 
        file_name: str  = "./day10/input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)

    def execute_part1(self, lines: list[str]) -> int:
        pipe_locations: list[Location] = self.find_pipe_locations(lines)
        return int((len(pipe_locations) - 1) / 2)
    
    def execute_part2(self, lines: list[str]) -> int:
        pipe_locations: list[Location] = self.find_pipe_locations(lines)
        return self.find_number_of_captured_cells(pipe_locations)

    def find_pipe_locations(self, lines:list[str]) -> list[Location]:
        grid: Grid
        begin: Location
        grid, begin = self.create_grid(lines)
        left: Step
        right: Step
        left, right = self.start(begin, grid)
        locations: list[Location] = [left.center, begin, right.center]
        while left.center != right.center:
            left = self.take_step(left, grid)
            locations.insert(0, left.center)
            right = self.take_step(right, grid)
            locations.append(right.center)
        return locations
    
    def find_number_of_captured_cells(self, locations: list[Location]) -> int:
        start_index: int = self.find_top_location(locations)
        sorted_clockwise: bool = self.is_sorted_clockwise(start_index, locations)
        number_of_locations: int = len(locations)
        number_of_captured_cells: int = 0
        previous_location: Location = locations[start_index]
        location: Location = previous_location
        for i in range(number_of_locations):
            diretion_index: int = start_index - i if sorted_clockwise else start_index + i
            index: int = (diretion_index + number_of_locations) % number_of_locations
            next_location: Location = locations[index]
            if self.is_downward_movement(location, next_location) or self.is_south_west_movement(previous_location, location, next_location):
                number_of_captured_cells = number_of_captured_cells + self.get_number_of_captured_cells_on_line(location, locations)
            previous_location = location
            location = next_location
        return number_of_captured_cells
    
    def find_top_location(self, locations: list[Location]) -> Location:
        top_location: Location = min(locations, key = lambda location: location.y)
        return locations.index(top_location)

    def is_sorted_clockwise(self, start_index: int, locations: list[Location]) -> bool:
        next_index: int = start_index + 1 if start_index < len(locations) - 1 else 0
        previous_index: int = start_index - 1 if start_index > 0 else -1
        next_location: Location = locations[next_index]
        previous_location: Location = locations[previous_index]
        return previous_location.x < next_location.x
    
    def is_downward_movement(self, start_location: Location, end_location: Location) -> bool:
        return end_location.y > start_location.y
    
    def is_south_west_movement(self, previous_location, current_location: Location, end_location: Location) -> bool:
        return self.is_downward_movement(previous_location, current_location) and end_location.x < current_location.x

    def get_number_of_captured_cells_on_line(self, location: Location, pipe_locations: list[Location]) -> int:
        pipe_locations_on_line: list[Location] = list(filter(lambda l: l.y == location.y and l.x > location.x, pipe_locations))
        if len(pipe_locations_on_line) == 0:
            return 0
        closest_location_on_line: Location = min(pipe_locations_on_line, key = lambda l: l.x)
        return closest_location_on_line.x - location.x - 1
    
    def create_grid(self, lines: list[str]) -> tuple[Grid, Location]:
        grid: Grid = []
        begin: Location
        for i in range(len(lines)):
            characters: list[str] = [*lines[i]]
            row: list[Movement] = [None] * len(characters)
            for j in range(len(characters)):
                character: str = characters[j]
                if self.is_beginning(character):
                    begin = Location(j, i)
                    continue
                if character == ".":
                    continue
                row[j] = MOVEMENTS[character]
            grid.append(row)
        return grid, begin

    def start(self, begin: Location, grid: Grid) -> tuple[Step, Step]:
        left: Step = None
        right: Step = None
        for initial_step in [Location(0, -1), Location(-1,0), Location(0, 1), Location(1, 0)]:
            location: Location = Location(begin.x + initial_step.y, begin.y + initial_step.x)
            if not self.is_valid(location, grid):
                continue
            movement: Movement = grid[location.y][location.x]
            if not movement:
                continue
            if self.is_move_allowed(movement, begin, location):
                if not left:
                    left = Step(begin, location)
                else:
                    right = Step(begin, location)
        return left, right
    
    def is_move_allowed(self, movement: Movement, begin: Location, location: Location) -> bool:
        end_location: Location = movement(location, begin)
        return end_location != begin and abs(end_location.x - location.x) < 2 and abs(end_location.y - location.y) < 2

    def is_valid(self, location: Location, grid: Grid) -> bool:
        return location.x >= 0 and location.x < len(grid[0]) and location.y >= 0 and location.y < len(grid)

    def take_step(self, step: Step, grid: Grid) -> Step:
        next_location = grid[step.center.y][step.center.x](step.center, step.src)
        return Step(step.center, next_location)

    def is_beginning(self, character: str) -> bool:
        return "S" == character

    def read_input(self, file_name: str) -> list[str]:
        return [line.rstrip("\n") for line in open(file_name, "r+")]

day10: Day10 = Day10()
print("Part 1 test 2: " + str(day10.execute_part1_test2()))
print("Part 1 test 2: " + str(day10.execute_part1_input()))
print("Part 1 Input: " + str(day10.execute_part1_test1()))

print("Part 2 test 1: " + str(day10.execute_part2_test1()))
print("Part 2 test 2: " + str(day10.execute_part2_test2()))
print("Part 2 test 3: " + str(day10.execute_part2_test3()))
print("Part 2 Input: " + str(day10.execute_part2_input()))
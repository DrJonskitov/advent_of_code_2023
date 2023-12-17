from __future__ import annotations
from collections.abc import Callable 
from dataclasses import dataclass
from typing import Final
import math

INPUT_PATH: Final[str] = "./day8/input.txt"
TEST_PATH: Final[str] = "./day8/test_input1.txt"
TEST_PATH_2: Final[str] = "./day8/test_input2.txt"
TEST_PATH_PART_2: Final[str] = "./day8/test_input_part2.txt"

LEFT: Final[str] = "L"
START_NODE: Final[str] = "AAA"
START_NODE_SUFFIX: Final[str] = "A"
END_NODE: Final[str] = "ZZZ"
END_NODE_SUFFIX: Final[str] = "Z"

@dataclass
class Node:
    name: str
    left: str
    right: str

Map= dict[str, Node]
Instruction = Callable[[Node, Map], Node]

class Day8:

    def execute_part1_test(self) -> int:
        lines: list[str] = self.read_input(TEST_PATH)
        return self.execute_part1(lines)
    
    def execute_part1_test2(self) -> int:
        lines: list[str] = self.read_input(TEST_PATH_2)
        return self.execute_part1(lines)

    def execute_part1_input(self) -> int: 
        lines: list[str] = self.read_input(INPUT_PATH)
        return self.execute_part1(lines)
        
    def execute_part2_test(self) -> int:
        lines: list[str] = self.read_input(TEST_PATH_PART_2)
        return self.execute_part2(lines)

    def execute_part2_input(self) -> int: 
        lines: list[str] = self.read_input(INPUT_PATH)
        return self.execute_part2(lines)

    def execute_part1(self, lines: list[str]) -> int:
        instructions: list[Instruction] = self.load_instructions(lines[0])
        map: Map = self.load_map(lines[1:])
        start_nodes: list[Node] = self.find_start_nodes(map, START_NODE)
        return self.count_steps(start_nodes, instructions, map, END_NODE)

    def execute_part2(self, lines: list[str]) -> int:
        instructions: list[Instruction] = self.load_instructions(lines[0])
        map: Map = self.load_map(lines[1:])
        start_nodes: list[Node] = self.find_start_nodes(map, START_NODE_SUFFIX)
        counts: list[int] = [self.count_steps([node], instructions, map, END_NODE_SUFFIX) for node in start_nodes]
        return math.lcm(*counts)
    
    def load_instructions(self, line: str) -> list[Instruction]:
        return list(map(self.to_instruction, [*line]))

    def to_instruction(self, character: str) -> Instruction:
        if character == LEFT:
            return lambda node, map: map[node.left]
        return lambda node, map: map[node.right]
    
    def load_map(self, lines: list[str]) -> Map:
        return {node.name: node for node in map(self.to_node, filter(lambda line: len(line) > 0, lines))}

    def to_node(self, line: str) -> Node:
        name_instructions: list[str] = line.split("=")
        name: str = name_instructions[0].strip()
        left_right: list[str] = name_instructions[1].split(",")
        left: str = left_right[0].replace("(", "").strip()
        right: str = left_right[1].replace(")", "").strip()
        return Node(name, left, right)

    def find_start_nodes(self, map: Map, match: str) -> list[Node]:
        return [node for name, node in map.items() if name.endswith(match)]

    def count_steps(self, start_nodes: list[Node], instructions: list[Instruction], grid: Map, end_match: str) -> int:
        steps: int = 0
        nodes: list[Node] = start_nodes
        while not self.is_final_step(nodes, end_match):
            instruction_index: int = steps % len(instructions)
            instuction: Instruction = instructions[instruction_index]
            nodes = list(map(lambda node: instuction(node, grid), nodes))
            steps = steps + 1
            # print(list(map(lambda node: node.name, nodes)))
        return steps
    
    def is_final_step(self, nodes: list[Node], end_match: str) -> bool:
        return all(node.name.endswith(end_match) for node in nodes)

    def read_input(self, file_name: str) -> list[str]:
        return [line.rstrip("\n") for line in open(file_name, "r+")]

day: Day8 = Day8()
print("Part 1 test: " + str(day.execute_part1_test()))
print("Part 1 test 2: " + str(day.execute_part1_test2()))
print("Part 1 Input: " + str(day.execute_part1_input()))

print("Part 2 test 1: " + str(day.execute_part2_test()))
print("Part 2 Input: " + str(day.execute_part2_input()))
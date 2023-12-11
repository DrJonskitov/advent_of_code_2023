import re

class Interval:

    def __init__(self, start: int, stop: int):
        self.start: int = start
        self.stop: int = stop

    def is_empty(self) -> bool:
        return self.start == self.stop

class Ranges:

    def __init__(self, destination_start: int, source_start: int, size: int):
        self.source_start: int = source_start
        self.destination_start: int = destination_start
        self.size: int = size

    def contains(self, value: int) -> bool:
        return self.source_start <= value and self.source_start + self.size - 1 >= value
    
    def get_destination_value(self, source_id: int) -> int:
        return self.destination_start + (source_id - self.source_start)
    
    def get_intervals(self, interval: Interval) -> tuple[Interval, list[Interval]]:
        if interval.start > self.source_start + self.size - 1:
            return interval, []
        if interval.stop < self.source_start:
            return Interval(0,0), [interval]
        intervals: list[Interval] = []
        if interval.start < self.source_start:
            intervals.append(Interval(interval.start, self.source_start - 1))
        start: int = max(interval.start, self.source_start)
        stop: int = min(interval.stop, self.source_start + self.size - 1)
        intervals.append(Interval(self.get_destination_value(start), self.get_destination_value(stop)))
        return Interval(stop, interval.stop), intervals

class Mapping:

    def __init__(self, ranges: list[Ranges]):
        self.ranges: list[Ranges] = sorted(ranges, key=lambda ranges: ranges.source_start)

    def find_destination(self, source_id: int) -> int:
        for range in self.ranges:
            if range.contains(source_id):
                return range.get_destination_value(source_id)
        return source_id
    
    def find_destinations(self, intervals: list[Interval]) -> list[Interval]:
        mapped_intervals: list[Interval] = []
        for interval in intervals:
            mapped_intervals.extend(self.to_mapped_intervals(interval))
        return mapped_intervals
    
    def to_mapped_intervals(self, interval: Interval) -> list[Interval]:
        mapped_intervals: list[Interval] = []
        remaining_interval: Interval = interval
        for ranges in self.ranges:        
            intervals: list[Interval] = []
            remaining_interval, intervals = ranges.get_intervals(remaining_interval)
            mapped_intervals.extend(intervals)
            if remaining_interval.is_empty():
                break
        if len(mapped_intervals) == 0:
            return [interval]
        return mapped_intervals


class Day5:

    def execute_part1_test(self):
        file_name: str = "./day5/test_input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part1(lines)

    def execute_part1_input(self):
        file_name: str = "./day5/input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part1(lines)
    
    def execute_part2_test(self):
        file_name: str = "./day5/test_input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)

    def execute_part2_input(self):
        file_name: str = "./day5/input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)

    def read_input(self, file_name: str) -> list[str]:
        return [line.rstrip("\n") for line in open(file_name, "r+")]
    
    def execute_part1(self, lines: list[str]) -> int:
        seeds: list[int] = self.find_seeds(lines[0])
        mappings: list[Mapping] = self.create_mappings(lines[1:])
        return min(map(lambda seed: self.find_location(seed, mappings), seeds))
    
    def execute_part2(self, lines: list[str]) -> int:
        seeds: list[Interval] = self.find_seed_intervals(lines[0])
        mappings: list[Mapping] = self.create_mappings(lines[1:])
        intervals: list[Interval] = []
        for seed in seeds:
            intervals.extend(self.find_interval_location(seed, mappings))
        return min(intervals, key=lambda interval: interval.start).start
    
    def find_seeds(self, line: str) -> list[int]:
        return [int(seed) for seed in re.findall("\d+", line.split(":")[1])]
    
    def find_seed_intervals(self, line: str) -> list[Interval]:
        seeds: list[int] = self.find_seeds(line)
        seed_intervals: list[Interval] = []
        for i in range(0, len(seeds), 2):
            start: int = seeds[i]
            stop: int = start + seeds[i + 1]
            seed_intervals.append(Interval(start, stop))
        return seed_intervals
    
    def create_mappings(self, lines: list[str]) -> list[Mapping]:
        mappings: list[Ranges] = []
        current_mapping: list[Ranges] = []
        for line in lines:
            mapping: list[str] = re.findall("\d+", line)
            if len(mapping) != 3:
                if len(current_mapping) > 0:
                    mappings.append(Mapping(current_mapping))
                    current_mapping = []
                continue
            
            range_array: list[int] = list(map(lambda x: int(x), mapping))
            current_mapping.append(Ranges(*range_array)) 
        if len(current_mapping) > 0:
            mappings.append(Mapping(current_mapping))
        return mappings

    def find_location(self, seed: int, mappings: list[Mapping]) -> int:
        id: int = seed
        for mapping in mappings:
            id = mapping.find_destination(id)
        return id
    
    def find_interval_location(self, seed_interval: Interval, mappings: list[Mapping]) -> list[Interval]:
        intervals: list[Interval] = [seed_interval]
        for mapping in mappings:
            intervals = mapping.find_destinations(intervals)
        return intervals

result: int = Day5().execute_part2_input()
print(result)
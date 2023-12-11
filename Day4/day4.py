import re

class Day4:

    def execute_part1_test(self):
        file_name: str = "./day4/test_input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part1(lines)

    def execute_part1_input(self):
        file_name: str = "./day4/input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part1(lines)
    
    def execute_part2_test(self):
        file_name: str = "./day4/test_input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)

    def execute_part2_input(self):
        file_name: str = "./day4/input.txt"
        lines: list[str] = self.read_input(file_name)
        return self.execute_part2(lines)

    def read_input(self, file_name: str) -> list[str]:
        return [line.rstrip("\n") for line in open(file_name, "r+")]
    
    def execute_part1(self, lines: list[str]) -> int:
        total: int = 0
        for line in lines:
            total = total + self.get_score(line)
        return total
    
    def execute_part2(self, lines: list[str]) -> int:
        return self.get_total_number_of_used_cards(lines)

    def get_total_number_of_used_cards(self, lines: list[str]) -> int:
        total_matches: list[int] = [self.get_number_of_matches(line) for line in lines]
        number_of_cards: list[int] = [1] * len(total_matches)
        for i in range(len(total_matches)):
            matches: int = total_matches[i]
            number_of_cards = self.adjust_number_of_cards(i, matches, number_of_cards)
        return sum(number_of_cards)
    
    def adjust_number_of_cards(self, index: int, matches: int, number_of_cards: list[int]) -> list[int]:
        for i in range(matches):
            index_to_adjust: int = index + i + 1
            number_of_cards[index_to_adjust] = number_of_cards[index_to_adjust] + number_of_cards[index]
        return number_of_cards

    def play_card(self, index: int, cards: list[str]) -> int:
        number_of_matches: int = self.get_number_of_matches(cards[index])
        # print("card " + str(index + 1) + " matches " + str(number_of_matches))
        total: int = number_of_matches
        for i in range(1, number_of_matches + 1):
            total = total + self.play_card(index + i, cards)
        return total
    
    def get_score(self, line: str) -> int:
        number_of_matches: int = self.get_number_of_matches(line)
        if number_of_matches == 0:
            return 0
        return pow(2, number_of_matches - 1)
    
    def get_number_of_matches(self, line: str) -> int:
        numbers: list[str] = line.split(":")[1].split("|")
        winning_numbers: list[int] = self.to_numbers_list(numbers[0])
        ticket_numbers: list[int] = self.to_numbers_list(numbers[1])
        matches: list[int] = self.find_matching_numbers(winning_numbers, ticket_numbers)
        return len(matches)

    def to_numbers_list(self, numbers_string: str) -> list[int]:
        return [int(number) for number in re.findall("\d+", numbers_string)]

    def find_matching_numbers(self, winning_numbers: list[int], ticket_numbers: list[int]) -> list[int]:
        return list(filter(lambda number: number in winning_numbers, ticket_numbers))


result: int = Day4().execute_part2_input()
print(result)


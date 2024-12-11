from dataclasses import dataclass
from collections import Counter

@dataclass
class Scoob:
    stones: dict

    def __post_init__(self):
        self.stones_count = Counter(self.stones)

    def blink(self):
        new_stones = Counter()
        for stone in self.stones_count:
            if stone == '0':
                new_stones['1'] += self.stones_count['0']
            elif len(stone) % 2 == 0:
                half = len(stone) // 2
                new_stones[str(int(stone[half:]))] += self.stones_count[stone]
                new_stones[str(int(stone[:half]))] += self.stones_count[stone]
            else:
                new_stones[str(int(stone) * 2024)] += self.stones_count[stone]
        self.stones_count = new_stones

    def run(self):
        blinks = 75
        for blink in range(1, blinks+1):
            self.blink()
            print(f'after blink {blink}: sum: {sum(self.stones_count.values())}')
    
def main():
    input = ['27', '10647', '103', '9', '0', '5524', '4594227', '902936']
    sample = ['0', '1', '10', '99', '999']
    sample_2 = ['125', '17']
    rocks = sample_2
    rocks = input

    print('s2')
    scoob = Scoob(rocks)
    scoob.run()



main()
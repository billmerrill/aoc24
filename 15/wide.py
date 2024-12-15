import numpy as np
import copy


class Warehouse:

    def pretty_print(self):
        for i in range(self.map.shape[0]):
            print(''.join(self.map[i]))

    def wide(self, wh):
        tmap = []
        for line in wh:
            map_line = []
            for char in line:
                match char:
                    case '#':
                        map_line.extend(['#']*2)
                    case '.':
                        map_line.extend(['.']*2)
                    case 'O':
                        map_line.append('[')
                        map_line.append(']')
                    case '@':
                        map_line.append('@')
                        map_line.append('.')
            tmap.append(map_line)
        return np.array(tmap)

    def load(self, wh, inst):
        self.instructions = list(inst)
        self.map = self.wide(wh)
        self.robot = None
        with np.nditer(self.map, flags=['multi_index']) as it:
            for x in it:
                if x == '@':
                    self.robot = it.multi_index
                    break
        print("Initial State")
        self.pretty_print()

    def shove(self, path):
        # pathstr = ''.join(path)
        offset = 0
        for i,v in enumerate(path):
            if v == 'O':
                continue
            if v == '.':
                path[0] = '.'
                path[1] = '@'
                path[i] = 'O'
                offset = 1
                break
            if v == '#':
                break
        return offset, path

    def process_path_thru(self, path):
        #  @.O.OO.#
        new_robot_offset = -1
        new_path = []
        for index, sym in enumerate(path):
            match sym:
                case '.':
                    new_path.append(0)
                case '@':
                    new_path.append(1)
                case 'O':
                    new_path.append(2)
                case '#':
                    new_path.append(4)
                    break
        new_path.sort()
        for i, sym in enumerate(new_path):
            match sym:
                case 0:
                    new_path[i] = '.'
                case 1:
                    new_path[i] = '@'
                    new_robot_offset = i
                case 2:
                    new_path[i] = 'O'
                case 4:
                    new_path[i] = '#'

        return new_robot_offset, new_path
    

    def run_robot(self):
        for inst in self.instructions:
            if inst == '^':
                next = (self.robot[0]-1, self.robot[1])
            elif inst == '>':
                next = (self.robot[0], self.robot[1]+1)
            elif inst == 'v':
                next = (self.robot[0]+1, self.robot[1])
            elif inst == '<':
                next = (self.robot[0], self.robot[1]-1)

            if self.map[next[0], next[1]] == '#':
                print("instruction", inst)        
                self.pretty_print()
                continue
            if self.map[next[0], next[1]] == '.':
                self.map[next[0], next[1]] = '@'
                self.map[self.robot[0], self.robot[1]] = '.'
                self.robot = next
                print("instruction", inst)        
                self.pretty_print()
                continue
                
                # up 
            cur = self.robot
            if inst == '^':
                # new_robot_offset, path = self.process_path(self.map[self.robot[0]::-1, self.robot[1]])
                new_robot_offset, path = self.shove(self.map[self.robot[0]::-1, self.robot[1]])
                for cell in path:
                    self.map[cur[0], cur[1]] = cell
                    cur = (cur[0]-1, cur[1])
                self.robot = (self.robot[0] - new_robot_offset, self.robot[1])
            elif inst == '>':
                # new_robot_offset, path = self.process_path(self.map[self.robot[0], self.robot[1]:])
                new_robot_offset, path = self.shove(self.map[self.robot[0], self.robot[1]:])
                for cell in path:
                    self.map[cur[0], cur[1]] = cell
                    cur = (cur[0], cur[1]+1)
                self.robot = (self.robot[0], self.robot[1] + new_robot_offset)
            elif inst == 'v':
                # new_robot_offset, path = self.process_path(self.map[self.robot[0]:, self.robot[1]])
                new_robot_offset, path = self.shove(self.map[self.robot[0]:, self.robot[1]])
                for cell in path:
                    self.map[cur[0], cur[1]] = cell
                    cur = (cur[0]+1, cur[1])
                self.robot = (self.robot[0] + new_robot_offset, self.robot[1])
            elif inst == '<':
                # new_robot_offset, path = self.process_path(self.map[self.robot[0], self.robot[1]::-1])
                new_robot_offset, path = self.shove(self.map[self.robot[0], self.robot[1]::-1])
                for cell in path:
                    self.map[cur[0], cur[1]] = cell
                    cur = (cur[0], cur[1]-1)
                self.robot = (self.robot[0], self.robot[1] - new_robot_offset)

            print("instruction", inst)        
            self.pretty_print()

    def score_map(self):
        score = 0 
        with np.nditer(self.map, flags=['multi_index']) as it:
            for x in it:
                if x == 'O':        
                    score += it.multi_index[0] * 100 + it.multi_index[1]
        return score

def main():
    src = 'small_sample.txt'
    # src = 'sample.txt'
    src = 'test.txt'
    # src = 'input.txt'
    # src = 'center.txt'
    instructions = []
    with open(src, 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    food_str = []
    inst_str = []
    for line in lines:
        if line.startswith('#'):
            food_str.append(line)
        elif line:
            inst_str.append(line)

    food = np.array([list(line) for line in food_str])
    if inst_str:
        for line in inst_str:
            instructions.extend(list(line))

    wh = Warehouse()
    wh.load(food, instructions)
    if instructions:
        wh.run_robot()
    print(f'shape {wh.map.shape}')
    print(wh.map)
    print(wh.instructions)
    print(wh.score_map())

main()
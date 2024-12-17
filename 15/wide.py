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
        # print("TESTING")
        # self.map[2,6] = '#'
        # self.map[2,6] = ']'
        # self.map[1,5] = '#'
        self.robot = None
        with np.nditer(self.map, flags=['multi_index']) as it:
            for x in it:
                if x == '@':
                    self.robot = it.multi_index
                    break
        print("Initial State")
        self.pretty_print()

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
    

    def box_moved(self, frame, bl, br, dir):
        bl_moved = False
        br_moved = False
        bl_next = (bl[0]+dir[0], bl[1]+dir[1])
        br_next = (br[0]+dir[0], br[1]+dir[1])
        bl_next_val = frame[bl_next[0], bl_next[1]]
        br_next_val = frame[br_next[0], br_next[1]]
        bl_next_val = frame[bl_next[0], bl_next[1]]
        br_next_val = frame[br_next[0], br_next[1]]
    
    
        if bl_next_val == '.':
            bl_moved = True
        if bl_next_val == '#':
            bl_moved = False

        if br_next_val == '.':
            br_moved = True
        if br_next_val == '#':
            br_moved = False

        if bl_next_val == '[' and br_next_val == ']':
            bl_moved = br_moved = self.box_moved(frame, bl_next, br_next, dir)
        elif bl_next_val == ']' and br_next_val == '[':
            bl_res = self.box_moved(frame, (bl_next[0], bl_next[1]-1), bl_next, dir)
            br_res = self.box_moved(frame, br_next, (br_next[0], br_next[1]+1), dir)
            if bl_res == False or br_res == False:
                bl_moved = br_moved = False
            else:
                bl_moved = br_moved = True
        else:
            if bl_next_val == ']':
                bl_moved = self.box_moved(frame, (bl_next[0], bl_next[1]-1), bl_next, dir)
            if br_next_val == '[':
                br_moved = self.box_moved(frame, br_next, (br_next[0], br_next[1]+1), dir)
        
        if br_moved and bl_moved:
            frame[bl_next[0], bl_next[1]] = frame[bl[0], bl[1]]
            frame[br_next[0], br_next[1]] = frame[br[0], br[1]]
            frame[bl[0], bl[1]] = '.'
            frame[br[0], br[1]] = '.'
            return True
        
        return False

    def box_slid(self, box, dir):
        box_slide = False 
        box_next = (box[0]+(2*dir[0]), box[1]+(2*dir[1]))
        box_next_val = self.map[box_next[0], box_next[1]]

        if box_next_val == '.':
            box_slide = True
        elif box_next_val == '#':
            box_slide = False
        elif box_next_val in ['[', ']']:
            box_slide = self.box_slid(box_next, dir)

        # < 
        # .[] 
        # [].
        if box_slide:
            self.map[box_next[0], box_next[1]] = self.map[box[0]+dir[0],box[1]+dir[1]]
            self.map[box[0]+dir[0], box[1]+dir[1]] = self.map[box[0],box[1]]
            self.map[box[0], box[1]] = '.'
            return True

        return False

    def run_robot(self):
        print_step = True
        for inst in self.instructions:
            if inst == '^':
                next = (self.robot[0]-1, self.robot[1])
            elif inst == '>':
                next = (self.robot[0], self.robot[1]+1)
            elif inst == 'v':
                next = (self.robot[0]+1, self.robot[1])
            elif inst == '<':
                next = (self.robot[0], self.robot[1]-1)

               
            cur = self.robot
            if self.map[next[0], next[1]] == '#':
                if print_step:
                    print("instruction", inst)        
                    # self.pretty_print()
                continue
            if self.map[next[0], next[1]] == '.':
                self.map[next[0], next[1]] = '@'
                self.map[self.robot[0], self.robot[1]] = '.'
                self.robot = next
                if print_step:
                    print("instruction", inst)        
                    # self.pretty_print()
                continue

            #it's a box
            if inst == '^' or inst == 'v':
                if inst == '^':
                    dir = (-1,0)
                else:
                    dir = (1,0)

                if self.map[next[0],next[1]] == '[':
                    box_l = next
                    box_r = (next[0], next[1]+1)
                elif self.map[next[0],next[1]] == ']':
                    box_l = (next[0], next[1]-1)
                    box_r = next
                else:
                    print(inst)
                    self.pretty_print()
                    import sys
                    sys.exit()

                frame = copy.copy(self.map)
                if self.box_moved(frame, box_l, box_r, dir):
                    # self.map[next[0], next[1]] = '@'
                    frame[next[0], next[1]] = '@'
                    # self.map[cur[0], cur[1]] = '.'
                    frame[cur[0], cur[1]] = '.'
                    self.map = frame
                    self.robot = next
            elif inst == '>' or inst == '<':
                if inst == '>':
                    dir = (0,1)
                else:
                    dir = (0,-1)

                if self.map[next[0], next[1]] in ['[',']']:
                    if self.box_slid(next, dir):
                        self.map[next[0], next[1]] = '@'
                        self.map[cur[0], cur[1]] = '.'
                        self.robot = next

            if print_step:
                print("instruction", inst)        
                self.pretty_print()

            # unique, counts = np.unique(self.map, return_counts=True)
            # print(dict(zip(unique, counts)))

    def score_map(self, target='O'):
        score = 0 
        with np.nditer(self.map, flags=['multi_index']) as it:
            for x in it:
                if x == target:        
                    score += it.multi_index[0] * 100 + it.multi_index[1]
        return score

def main():
    # src = 'small_sample.txt'
    # src = 'sample.txt'
    # src = 'test.txt'
    src = 'input2.txt'
    # src = 'center.txt'
    # src = 'p2sample.txt'
    # src = 'p2score.txt'
    # src = 'test-p2-1.txt'
    # src = 'split_test2.txt'
    # src = 'split_testup.txt'
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
    # print(f'shape {wh.map.shape}')
    wh.pretty_print()
    # print(wh.instructions)
    print(wh.score_map(target='['))

main()

# 1541299 too low
# 1564765 too hi
# 1548869 no
# 1553459 no
# 1548815
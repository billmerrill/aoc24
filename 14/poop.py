from dataclasses import dataclass
from collections import Counter
import re
from math import modf

@dataclass
class Room:

    def load_machines(self, filename, shape):
        self.machines = []
        self.room_shape = shape
        with open(filename, 'r') as fh:
            lines = fh.readlines()
        i = 0
        for line in lines:
            machine = dict(start=None, v=None)
            d = re.findall(r'p\=(-?[0-9]+),(-?[0-9]+) v\=(-?[0-9]+),(-?[0-9]+)', line)
            if d:
                machine['start'] = (int(d[0][1]),int(d[0][0]))
                machine['v'] = (int(d[0][3]),int(d[0][2]))  
                machine['cur'] = machine['start']
                self.machines.append(machine)

    def pretty_print(self):
        stacks = Counter([x['cur'] for x in self.machines])
        for i in range(self.room_shape[0]):
            row = ['.']*self.room_shape[1]
            for m in stacks:
                if m[0] == i:
                    row[m[1]] = '@'
            print(''.join(row))
   
    def simulate(self, steps=1):
        scores = []
        for step in range(steps):
            for i, m  in enumerate(self.machines):
                self.machines[i]['cur'] = (
                    (m['cur'][0] + m['v'][0]) % self.room_shape[0], 
                    (m['cur'][1] + m['v'][1]) % self.room_shape[1]) 
            scores.append((step, self.score()))
                
            if step in(7846, 7847):
                print(f'\n\n******************\nStep {step+1}')
                self.pretty_print()
        scores.sort(key=lambda x:x[1])
        print(scores[:10])

    def score(self):
        q = [0,0,0,0]
        stacks = Counter([x['cur'] for x in self.machines])
        for p in stacks:
            if 0 <= p[0] < (self.room_shape[0] // 2) and \
                0 <= p[1] < (self.room_shape[1] // 2):
                q[0] += stacks[p]
            elif 0 <= p[0] < (self.room_shape[0] // 2) and \
                (self.room_shape[1] // 2)+1 <= p[1] < self.room_shape[1]:
                q[1] += stacks[p]
            elif (self.room_shape[0] // 2)+1 <= p[0] and \
                0 <= p[1] < (self.room_shape[1] // 2):
                q[2] += stacks[p]
            elif (self.room_shape[0] // 2)+1 <= p[0] and \
                (self.room_shape[1] // 2)+1 <= p[1] < self.room_shape[1]:
                q[3] += stacks[p]

        score = 1
        for x in q:
            score *= x

        return score

    
def main():
    room = Room()
    # src = ('sample.txt', (7,11) )
    # src = ('baby.txt', (7, 11) )
    src = ('input.txt', (103,101))
    room.load_machines(src[0], src[1] )
    room.simulate(10000)
    # print(room.score())
    # for m in room.machines:
    #     print(m['cur'])

main()


'''
......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....'''
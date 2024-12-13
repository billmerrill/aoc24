from dataclasses import dataclass
from collections import Counter
import re
from math import modf

@dataclass
class Claw:

    def load_machines(self, filename, p2=0):
        self.machines = []
        with open(filename, 'r') as fh:
            lines = fh.readlines()
        i = 0
        while i < len(lines):
            machine = dict(a=None, b=None, p=None)
            a_points = re.findall(r'X\+([0-9]+), Y\+([0-9]+)', lines[i])
            b_points = re.findall(r'X\+([0-9]+), Y\+([0-9]+)', lines[i+1])
            p_points = re.findall(r'X\=([0-9]+), Y\=([0-9]+)', lines[i+2])
            machine['a'] = (float(a_points[0][0]),float(a_points[0][1]))
            machine['b'] = (float(b_points[0][0]),float(b_points[0][1]))
            machine['p'] = (float(p_points[0][0])+p2,float(p_points[0][1])+p2)
            self.machines.append(machine)
            i+=4


    def solve_machine(self, m):
        '''
        system
        a_x * a_press + b_x * b_press = m_x
        a_y * a_press + b_y * b_press = m_y

        cramers's rule
        A = (p_x*b_y - p_y*b_x) / (a_x*b_y - a_y*b_x)
        B = (a_x*p_y - a_y*p_x) / (a_x*b_y - a_y*b_x)
        '''

        a_press = (m['p'][0] * m['b'][1] - m['p'][1] * m['b'][0]) / (
                m['a'][0] * m['b'][1] - m['a'][1] * m['b'][0])
        b_press = (m['a'][0] * m['p'][1] - m['a'][1] * m['p'][0]) / (
                m['a'][0] * m['b'][1] - m['a'][1] * m['b'][0])
    
        return a_press, b_press

    def solve(self):
        for i, m  in enumerate(self.machines):
            ap, bp = self.solve_machine(m)
            self.machines[i]['presses'] = (ap,bp)

        total_cost = 0
        for m in self.machines:
            print(m)
            print(modf(m['presses'][0])[0],  modf(m['presses'][1])[0])
            if modf(m['presses'][0])[0] == 0 and modf(m['presses'][1])[0] == 0:
                total_cost += 3*m['presses'][0] + m['presses'] [1]
        return total_cost
    
def main():
    claw = Claw()
    # claw.load_machines('sample.txt', p2=10000000000000)
    claw.load_machines('input.txt', p2=10000000000000)
    print(claw.solve())

main()

A = 0
B = 1
C = 2

class Compy:

    def __init__(self, state=None, program=None):
        self.state = [0,0,0]
        if state:
            self.state = [x for x in state] 

        self.program = program
        self.inst_ptr = 0
        self.output = []
        self.halt_flag = False
        self.ops = self._set_operators()

    def __str__(self):
        return f'state: {self.state}\nprog : {self.program}\nptr  : {self.inst_ptr}\noutpt: {self.output}' 

    def reset(self, reg_a = 0):
        self.state = [int(reg_a), 0, 0]
        self.inst_ptr = 0
        self.ptr = []
        self.halt_flag = False

    # 0
    def _adv(self, x):
        self.state[A] = self.state[A]//(2**self.get_combo_operand(x))
        return True
    # 1
    def _bxl(self, x):
        '''
        The bxl instruction (opcode 1) calculates the bitwise XOR of register B 
        and the instruction's literal operand, then stores the result in register B.
        '''
        self.state[B] = x^self.state[B]
        return True

    # 2
    def _bst(self, x):
        '''
        The bst instruction (opcode 2) calculates the value of its combo operand modulo 8 
        (thereby keeping only its lowest 3 bits), then writes that value to the B register.
        '''
        self.state[B] = self.get_combo_operand(x)%8
        return True

    # 3
    def _jnz(self, x):
        if self.state[A] != 0:
            self.inst_ptr = x
            if self.inst_ptr < len(self.program):
                return False
            else:
                self.halt()
        else:
            return True

    # 4
    def _bxc(self, x):
        self.state[B] = self.state[B] ^ self.state[C]
        return True
    # 5
    def _out(self, x):
        self.output.append(self.get_combo_operand(x)%8)
        return True

    # 6
    def _bdv(self, x):
        self.state[B] = self.state[A]//(2**self.get_combo_operand(x))
        return True

    # 7
    def _cdv(self, x):
        self.state[C] = self.state[A]//(2**self.get_combo_operand(x))
        return True

    def _set_operators(self):
        return [self._adv, self._bxl, self._bst, self._jnz, 
                self._bxc, self._out, self._bdv, self._cdv]


    def tick(self):
        self.inst_ptr += 2
        if (self.inst_ptr >= len(self.program)):
            self.halt()

    def halt(self):
        self.halt_flag = True
        # print('Compy Output\n', ','.join(list(map(str, self.output))))

    def get_combo_operand(self, raw_val):
        match raw_val:
            case val if raw_val in [0,1,2,3]:
                return raw_val
            case val if raw_val in [4,5,6]:
                return self.state[raw_val-4]
            case 7:
                raise Exception('Number 7')

    def execute(self):
        raw_op = self.program[self.inst_ptr]
        raw_val = self.program[self.inst_ptr+1]
        # print('running ', raw_op, raw_val)

        return self.ops[raw_op](raw_val)

    def run(self):
        # print('Booting Compy')
        # print(self)
        while not self.halt_flag:
            # print(self)
            if(self.execute()):
                self.tick()
            # print(self)
inputs = [
    {'state':(0,0,0), 'program':'0,1,1,3,2,5,3,6,4,7,5,0,6,1'},
    {'state':(0,0,9), 'program':'2,6'},
    {'state':(10,0,0), 'program':'5,0,5,1,5,4'},
    {'state':(2024,0,0), 'program':'0,1,5,4,3,0'},
    {'state':(0,29,0), 'program':'1,7'},
    {'state':(0,2024,43690), 'program':'4,0'},
    {'state':(729,0,0), 'program': '0,1,5,4,3,0'},
    # input cart 7
    {'state':(24847151,0,0), 'program': '2,4,1,5,7,5,1,6,0,3,4,0,5,5,3,0'},
    {'state':(117440,0,0), 'program': '0,3,5,4,3,0'},
    ]
cart = 7
input = inputs[cart]

int_program = list(map(int,input['program'].split(',')))
search = [(len(int_program), 0)]    
answers = []
while search:
    pos, reg_a = search.pop(0)
    for i in range(8):
        new_reg_a = reg_a*8+i
        c = Compy(state=(new_reg_a, 0, 0), program=int_program)
        c.run()
        if c.output == c.program[pos-1:]:
            search.append((pos-1, new_reg_a))
            if len(c.output) == len(int_program):
                answers.append(new_reg_a)

answers.sort()
print(answers[0]) 

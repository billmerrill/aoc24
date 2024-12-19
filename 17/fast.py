
PROGRAM = [2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 0, 5, 5, 3, 0]

def main():
    a = 0
    go = True
    while go:
        go = simulate(a)
        a += 1
        if a % 10000 == 0:
            print(a)

def simulate(start_a):
    regA = start_a
    regB = 0
    regC = 0
    ptr = 0
    output = []

    while regA > 0:
        regB = regA % 8
        regB = regB^5
        regC = regA//(2**regB)
        regB = regB^6
        regA = regA // 8
        regB = regB ^ regC
        output.append(regB%8)

    if output == PROGRAM:
        print('found it')
        print(start_a)
        print('state: ', regA, regB, regC)
        print('output:', output)
        return False
    return True


main()
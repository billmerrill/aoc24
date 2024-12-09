import itertools, operator, copy

def my_conc(a,b):
    return int(f'{a}{b}')

def sum_goodies(config):
    grand_total = 0
    for c in config:
        print(c)
        numo = len(c['operands'])-1
        for attempt in itertools.product([operator.add, operator.mul, my_conc], repeat=numo):
            nums = copy.copy(c['operands'])
            sum = nums.pop(0)
            for op in attempt:
                sum = op(sum, nums.pop(0))
            if sum == c['result']:
                grand_total += sum
                print('good')
                break
    return grand_total

def main():
    src = 'sample.txt'
    src = 'input.txt'
    with open(src, 'r') as fh:
        lines = fh.readlines()

    config = []
    for line in lines:
        result, operands = line.split(':')
        config.append({'result': int(result), 'operands': list(map(int, operands.split()))})

    # sum = sum_goodies_huer1(config)
    sum = sum_goodies(config)
    print(sum)

main()
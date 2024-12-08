import itertools, operator, copy

def sum_goodies(config):
    grand_total = 0
    for c in config:
        numo = len(c['operands'])-1
        ops = [operator.add] * numo
        ops.extend([operator.mul] * numo)
        for attempt in itertools.permutations(ops, numo):
            nums = copy.copy(c['operands'])
            sum = nums.pop(0)
            for op in attempt:
                sum = op(sum, nums.pop(0))
            if sum == c['result']:
                grand_total += sum
                print(c)
                break
    return grand_total

def main():
    src = 'sample.txt'
    with open(src, 'r') as fh:
        lines = fh.readlines()

    config = []
    for line in lines:
        result, operands = line.split(':')
        config.append({'result': int(result), 'operands': list(map(int, operands.split()))})

    sum = sum_goodies(config)
    print(sum)

main()
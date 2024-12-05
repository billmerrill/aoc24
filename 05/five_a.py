from collections import defaultdict

def load_config(src):

    with open(src, 'r') as fh:
        rules = defaultdict(list)
        is_rules = True
        while is_rules:
            l = fh.readline().strip()
            if len(l):
                p1, p2 = l.split("|")
                rules[p1].append(p2)
            else:
                is_rules = False

        orders = []
        while True:
            l = fh.readline().strip()
            if not l:
                break
            orders.append(l.split(','))


    return dict(rules=rules, orders=orders)

def fix_order(order, rules):
    i = 1
    while i < len(order):
        if order[i] in rules[order[i-1]]:
            i += 1
            continue
        else:
            target = order[i-1]
            for j in range(i, len(order)):
                if target in rules[order[j]]:
                    order.insert(j+1, target)
                    order.pop(i-1)
                    i = 1 #start over on the whole order after the fix.
                    break

    return int(order[len(order) // 2])

def validate_and_count(config):
    valid_sum = 0
    fixed_sum = 0
    for order in config['orders']:
        if all(order[i] in config['rules'][order[i-1]] for i in range(1, len(order))):
            valid_sum += int(order[len(order) // 2])
        else:
            fixed_sum += fix_order(order, config['rules'])
            pass

    return (valid_sum, fixed_sum)

def main():
    src = 'test_input.txt'
    src = 'input.txt'
    config = load_config(src)
    print(config)
    print(validate_and_count(config))

main()
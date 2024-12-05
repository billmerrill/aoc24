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

def validate_and_count(config):
    sum = 0
    for order in config['orders']:
        if all(order[i] in config['rules'][order[i-1]] for i in range(1, len(order))):
            sum += int(order[len(order) // 2])

    return sum

def main():
    src = 'test_input.txt'
    src = 'input.txt'
    config = load_config(src)
    print(config)
    print(validate_and_count(config))

main()
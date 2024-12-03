
def norm(x):
    if x == 0:
        return 0
    return int(x/abs(x))

def is_it_safe(report):
    direction = int(report[1])-int(report[0])
    direction = norm(direction)
    for i in range(1, len(report)):
        diff = int(report[i]) - int(report[i-1])
        if norm(diff) != direction:
            return False
        if diff not in [-3, -2, -1, 1, 2, 3]:
            return False

    return True

def is_it_damp(report):
    if is_it_safe(report):
        return True

    for omit in range(0, len(report)):
        shorty = report.copy()
        del(shorty[omit])
        shorty_safe = is_it_safe(shorty)
        if shorty_safe:
            return True

    return False



def main():
    fh = open('input.txt', 'r')
    reports = fh.readlines()
    safe_count = 0
    damp_safe = 0
    for report in reports:
        report = report.strip().split(' ')
        if is_it_safe(report):
            safe_count += 1
        if is_it_damp(report):
            damp_safe += 1


    print(f'Safe count: {safe_count}')
    print(f'Damp Safe count: {damp_safe}')


main()

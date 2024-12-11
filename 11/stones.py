


def main():
    input = ['27', '10647', '103', '9', '0', '5524', '4594227', '902936']
    sample = ['0', '1', '10', '99', '999']
    sample_2 = ['125', '17']

    print('stones')
    rocks = sample_2 
    rocks = input
    # print(rocks)
    for blink in range(1,26 ):
        i = 0
        limit = len(rocks)
        while i < limit:
            if rocks[i] == '0':
                rocks[i] = '1'
                i += 1
            elif len(rocks[i]) % 2 == 0:
                og_label = rocks[i]
                rocks[i] = og_label[:len(og_label)//2]
                rocks.insert(i+1, str(int(og_label[len(og_label)//2:])))
                i += 2
                limit += 1
            else:
                rocks[i] = str(int(rocks[i]) * 2024)
                i += 1

        print(f'after blink: {blink}, len: {len(rocks)}')


main()
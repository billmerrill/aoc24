

def gen_disk(dmap):
    disk = []
    mode = 'f'
    cur_id = 0
    for d in list(map(int, dmap)):
        if mode == 'f':
            disk.extend([cur_id] * d)
            cur_id +=  1
            mode = 's'
        elif mode == 's':
            disk.extend(['.']*d)
            mode = 'f'
    return disk

def defrag(disk):
    space_ptr = 0
    file_ptr = len(disk) -1
    while isinstance(disk[space_ptr], int):
        space_ptr += 1
    while disk[file_ptr] == '.':
        file_ptr -= 1

    while space_ptr != file_ptr:
        disk[space_ptr] = disk[file_ptr]
        disk[file_ptr] = '.'

        while isinstance(disk[space_ptr], int):
            space_ptr += 1
            if space_ptr == file_ptr:
                return disk

        while disk[file_ptr] == '.':
            file_ptr -= 1
            if space_ptr == file_ptr:
                return disk

    return disk

def checksum_disk(disk):
    cs = 0
    for index, block in enumerate(disk):
        if isinstance(block, int):
            cs += index * block

    return cs


def main():
    sample_disk_map = '2333133121414131402'
    with open('input.txt', 'r') as fh:
        input_disk_map = fh.readline().strip()
    print(input_disk_map)
    disk = gen_disk(input_disk_map)
    # disk = gen_disk(sample_disk_map)
    print(disk)
    disk = defrag(disk)
    print(disk)
    checksum = checksum_disk(disk)
    print(f'checksum {checksum}')


main()
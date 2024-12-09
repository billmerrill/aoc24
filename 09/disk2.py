

def gen_disk(dmap):
    disk = []
    mode = 'f'
    cur_id = 0
    for d in list(map(int, dmap)):
        if mode == 'f':
            disk.append([cur_id, d])
            cur_id +=  1
            mode = 's'
        elif mode == 's':
            disk.append(['.', d])
            mode = 'f'
    return disk

def pretty_print(disk):
    rep = ''
    for i in disk:
        rep += str(i[0]) * i[1]
    
    print(rep)

def expand_disk(disk):
    rep =[]
    for i in disk:
        for j in range(0, i[1]):
            rep.append(i[0])
    return rep


def defrag(disk):
    # print(disk)
    space_ptr = 0
    file_ptr = len(disk) -1
    # while isinstance(disk[space_ptr][0], int):
    #     space_ptr += 1
    # while disk[file_ptr][0] == '.':
    #     file_ptr -= 1

    # while file_ptr > 0:
    file_ptr = len(disk)-1
    while file_ptr >= 0:
    # for file_ptr in range(len(disk)-1, 0, -1):
        if disk[file_ptr][0] == '.':
            file_ptr -= 1
            continue
        space_search = 0
        for space_search in range(len(disk)):
            if disk[space_search][0] == '.' and space_search < file_ptr :
                if disk[file_ptr][1] == disk[space_search][1]:
                    disk[space_search][0] = disk[file_ptr][0]
                    disk[file_ptr][0] = '.'
                    file_ptr -= 1
                    # pretty_print(disk)
                    break
                elif disk[file_ptr][1] < disk[space_search][1]:
                    new_len = disk[space_search][1] - disk[file_ptr][1]
                    disk[space_search][0] = disk[file_ptr][0]
                    disk[space_search][1] = disk[file_ptr][1]
                    disk[file_ptr][0] = '.'
                    disk.insert(space_search+1, ['.', new_len])
                    # file_ptr += 1
                    # pretty_print(disk)
                    break

        file_ptr -= 1
        
        # while disk[file_ptr][0] == '.':
        #     file_ptr -= 1

    return disk

def checksum_disk(disk):
    cs = 0
    for index, block in enumerate(expand_disk(disk)):
        if isinstance(block, int):
            cs += index * block

    return cs


def main():
    sample_disk_map = '2333133121414131402'
    with open('input.txt', 'r') as fh:
        input_disk_map = fh.readline().strip()
    # print(input_disk_map)
    disk = gen_disk(input_disk_map)
    # disk = gen_disk(sample_disk_map)
    print(disk)
    disk = defrag(disk)
    print(disk)
    checksum = checksum_disk(disk)
    print(f'checksum {checksum}')


main()
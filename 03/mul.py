import re

def get_inst(text):
    return re.findall('mul\(([0-9]+)\,([0-9]+)\)', text)


fh = open('input.txt', 'r')
lines = fh.readlines()
blob = ''
for line in lines:
    blob += line.strip()
#instructions = re.findall('mul\(([0-9]+)\,([0-9]+)\)', blob)
instructions = get_inst(blob)
print(len(instructions))
sum = 0
for i in instructions:
    sum += int(i[0]) * int(i[1])

print(sum)


#doooo
sum = 0

tokens = re.findall('(mul\(([0-9]+)\,([0-9]+)\)|do\(\)|don\'t\(\))', blob)

use = True
for token in tokens:

    if token[0].startswith('mul'):
        if use:
            sum += int(token[1]) * int(token[2])
    elif token[0].startswith('don\'t'):
            use = False
    elif token[0].startswith('do'):
            use = True

print(sum)



import collections, re

left_shark = []
right_shark = []


fh = open ('input.txt', 'r')
dual_locs = fh.readlines()

for pair in dual_locs:
    x =  re.findall('[0-9]+', pair)
    left_shark.append(int(x[0]))
    right_shark.append(int(x[1]))

left_shark.sort()
right_shark.sort()

dist_sum = 0
score = 0

score_dict = dict(collections.Counter(right_shark).most_common())

for i in range(0, len(left_shark)):
    dist_sum += abs(right_shark[i] - left_shark[i])
    if left_shark[i] in right_shark:
        score += left_shark[i] * score_dict[left_shark[i]]

print(f'Length {len(left_shark)} Sum {dist_sum} Score {score}')



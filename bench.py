import random
import statistics

from solver import WordlySolver, check

N = 1000


with open('five.txt') as file:
    words = file.read().split('\n')

steps = []
for _ in range(N):
    solver = WordlySolver(words)
    word = random.choice(words)
    i = 0
    while solver.word != word:
        state = ''.join(check(word, solver.word))
        solver.filter(state)
        i += 1
    steps.append(i)

print('mean:  ', statistics.mean(steps))
print('median:', statistics.median(steps))
print('max:   ', max(steps))
print('min:   ', min(steps))

from collections import Counter
from typing import Iterable


def check(word: str, attempt: str):
    yellow = Counter()
    for w, a in zip(word, attempt):
        if w != a:
            yellow[w] += 1

    for w, a in zip(word, attempt):
        if w == a:
            yield '1'
        elif yellow[a]:
            yellow[a] -= 1
            yield '2'
        else:
            yield '3'


class WordlySolver:
    def __init__(self, words: Iterable[str]) -> None:
        freq = Counter(''.join(words))
        self.words = sorted(words, key=lambda word: sum(freq[ch] for ch in word))
        self.word = self.words.pop()

    def filter(self, state: str) -> None:
        if state != '':
            self.words = list(
                filter(
                    lambda attempt: all(
                        a == b for a, b in zip(state, check(attempt, self.word))
                    ),
                    self.words,
                )
            )
        self.word = self.words.pop()


if __name__ == '__main__':
    with open('five.txt') as file:
        words = file.read().split('\n')

    solver = WordlySolver(words)

    print('1 green; 2 yellow; 3 gray;')
    while len(solver.words):
        print(f'  {solver.word} [{len(solver.words)}]')
        state = input('> ')
        solver.filter(state)
    print(solver.word)

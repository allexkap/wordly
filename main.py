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


def sort_words_1(words: Iterable[str]) -> list[str]:
    freq = Counter(''.join(words))
    return sorted(words, key=lambda word: sum(freq[ch] for ch in word))


def sort_words_2(words: Iterable[str]) -> list[str]:
    freq = [Counter() for _ in range(5)]
    for word in words:
        for i, ch in enumerate(word):
            freq[i][ch] += 1
    return sorted(words, key=lambda word: sum(freq[i][ch] for i, ch in enumerate(word)))


class WordlySolver:
    def __init__(self, words: Iterable[str]) -> None:
        self.words = sort_words_2(words)
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

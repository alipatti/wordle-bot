import json
from operator import itemgetter
import random
from bisect import bisect_left
from statistics import mean
import time

import numpy as np
import pandas as pd

from precomputing import ANSWERS, GUESSES, PATTERN_LOOKUP

ANSWER_SET = set(bisect_left(GUESSES, answer) for answer in ANSWERS)

CLASS_LOOKUP = {
    "x": "absent",
    "y": "present",
    "g": "correct",
}

# precomputed flips for all guess-answer pairs
FLIPS = np.load("data/wordle/all_patterns.npy")


def update_mask(g, flip, mask) -> None:
    """Updates the mask in place."""
    mask[FLIPS[g] != flip] = False


def expectation(g, mask) -> float:
    n = np.count_nonzero(mask)
    possible_flips = FLIPS[g][mask]

    # TODO replace with better probability function
    probabilities = np.bincount(possible_flips) * (1 / n)
    infos = -np.log2(probabilities, where=(probabilities != 0))

    if g in ANSWER_SET:
        # account for probability of guess being the answer
        return np.sum(infos * probabilities) + (-1 / n * np.log2(1 / n))

    return np.sum(infos * probabilities) # type: ignore


def best_guess(mask: np.ndarray | None = None, print_best=0) -> tuple[int, str, float]:
    if mask is None:
        mask = np.ones(FLIPS.shape[1]).astype(bool)

    if mask.all():
        # hard-code best first guess
        return (10364, "soare", 5.816728835183138)

    expectations = [(i, word, expectation(i, mask)) for i, word in enumerate(GUESSES)]

    if print_best:
        print(
            pd.DataFrame.from_records(
                expectations, columns=["index", "word", "expectation"]
            )
            .sort_values(by="expectation", ascending=False)
            .head(print_best)
        )

    return max(expectations, key=itemgetter(2))


def play_game(answer=None, noisy=False, return_json=False):
    if not answer:
        answer = random.choice(ANSWERS)

    a = ANSWERS.index(answer)

    mask = np.ones(FLIPS.shape[1]).astype(bool)

    guesses = []

    while np.count_nonzero(mask) > 1:
        g, guess, _ = best_guess(mask)

        if guess == answer:
            break

        flip = FLIPS[g, a]
        update_mask(g, flip, mask)

        if noisy:
            print(f"{guess}\t{PATTERN_LOOKUP[flip]}\t{np.count_nonzero(mask)}")

        guesses.append((guess, PATTERN_LOOKUP[flip]))

    guesses.append((answer, "ggggg"))

    if noisy:
        print(f"Guessed {answer} " f"and won in {len(guesses)} turns.")

    if return_json:
        return json.dumps(
            [
                [guess, [CLASS_LOOKUP[char] for char in pattern]]
                for guess, pattern in guesses
            ]
        )

    return guesses


def test(n=5, answers=None):
    t0 = time.perf_counter()
    scores = []

    if not answers:
        answers = random.choices(ANSWERS, k=n)

    for i, answer in enumerate(answers):
        print(f"{'-' * 5} {i+1} ({answer}) {'-' * 5}")
        scores.append(len(play_game(answer, noisy=True)))

    print("-" * 10)
    print(f"Average score: {mean(scores)}")
    print(f"Average time per game: {(time.perf_counter() - t0) / n:.2f}s")

if __name__ == "__main__":
    test(30)


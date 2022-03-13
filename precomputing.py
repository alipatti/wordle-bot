from itertools import product

import numpy as np
from tqdm import tqdm

def get_words(filepath):
    with open(f"words/{filepath}", "rt") as f:
        return f.read().split()

PATTERN_FILE = "all_patterns.npy"
ANSWERS = get_words("answers.txt")
GUESSES = sorted(ANSWERS + get_words("guesses.txt"))
PATTERN_LOOKUP = {
    pattern : id 
    for id, pattern 
    in enumerate("".join(pattern) for pattern in product(*["xyg"]*5))
}
# add inverse mapping
PATTERN_LOOKUP.update({id : pattern for pattern, id in PATTERN_LOOKUP.items()})

def get_pattern(answer, guess):

    pattern = list("xxxxx")

    # mark greens
    for i in range(5):
        if answer[i] == guess[i]:
            pattern[i] = "g"
            answer = answer[:i] + "." + answer[i+1:]

    # mark yellows
    for i in range(5):
        if guess[i] in set(answer):
            pattern[i] = "y"
            # remove letter so it can't match twice
            answer = answer.replace(guess[i], ".", 1)

    return "".join(pattern)


def compute_all_patterns():
    patterns = np.empty(
        shape=(len(GUESSES), len(ANSWERS)),
        dtype=np.uint8
    )

    for g, guess in enumerate(tqdm(GUESSES)):
        for a, answer in enumerate(ANSWERS):
            patterns[g,a] = PATTERN_LOOKUP[get_pattern(answer, guess)]

    print("Done! Writing file...")
    with open(PATTERN_FILE, "wb") as f:
        np.save(f, patterns)


if __name__=="__main__":
    # test_patterns()
    compute_all_patterns()

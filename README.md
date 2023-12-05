# Wordle Bot

A Python/NumPy implementation of
[3Blue1Brown](https://www.youtube.com/watch?v=v68zYyaEmEA)'s
information-theoretic Wordle Bot--with some improvements. Scores ~3.5 on
average.

_DISCLAIMER_: This is horribly inefficient and probably incorrect. There exist
better implementations.

## Example usage

```fish
❯ python main.py

----- 1 (meaty) -----
soare   xxgxy   27
depth   xgxgx   1
Guessed meaty and won in 3 turns.
----- 2 (alpha) -----
soare   xxyxx   146
clint   xgxxx   3
aback   yxxxx   1
Guessed alpha and won in 4 turns.
----- 3 (glyph) -----
soare   xxxxx   183
linch   yxxxg   1
Guessed glyph and won in 3 turns.

        .
        .
        .

```

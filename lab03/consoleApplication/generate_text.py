#!/usr/bin/env python
import sys
import random

from analyze_text import parse_file


def get_random_successor(word_statistics):

    # Has to be calculated to handle the edge case of the last word
    accumulated_sum = sum([cnt for word, cnt in word_statistics["successors"].items()])

    if accumulated_sum == 0:
        return None

    threshold = random.randint(1, accumulated_sum)
    current_accumulated_sum = 0

    for word, cnt in word_statistics["successors"].items():
        current_accumulated_sum += cnt
        if current_accumulated_sum >= threshold:
            return word

    raise RuntimeError("While randomly sampling a successor an unknown error occurred.")


try:
    if len(sys.argv) != 4:
        raise ValueError()

    current_word = sys.argv[2].lower()
    n = int(sys.argv[3])
    words_statistics = parse_file(sys.argv[1])[0]
except:
    print("Exactly three arguments must be supplied:\n"
          "1) The file from which to extract the word statistics\n"
          "2) and a starting word\n"
          "3) the number of words to generate.\n")
    sys.exit()


generated_text = current_word

for i in range(0, n-1):
    current_word = get_random_successor(words_statistics[current_word])

    # If no successor, we have to stop
    if current_word is None:
        break

    generated_text += " " + current_word

with open("generated_text.txt", "w") as file:
    file.write(generated_text + "\n")

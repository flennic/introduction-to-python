import sys
import os.path
import re
import os
import json
import operator

# TODO: Check if parameters are okay (1, 2) DONE

# TODO: Check, if file exists DONE

# TODO: Frequency table (for alphabetic letters)

# TODO: Wordcount
# TODO: Unique Words

# TODO: 5 Most common words (highest frequency), successor (include no occurrences) and frequency

# Validation of user input


def parse_file(filepath):

    if not os.path.isfile(filepath):
        raise ValueError("File does not exists.")

    word_list = {}
    alphabet_frequency = {}
    previous_word = None

    try:
        with open(filepath, "r") as file:
            for line in file:
                # This will only take alphanumeric characters, split by space and make everything lowercase
                line = re.sub(r'[^a-zA-Z\s]*', '', line)
                entries = line.lower().split()

                for word in entries:
                    # Letter Statistics
                    characters = list(word)
                    for character in characters:
                        if character in alphabet_frequency.keys():
                            alphabet_frequency[character] += 1
                        else:
                            alphabet_frequency[character] = 1

                    # Word Statistics
                    # Handle the current word
                    if word in word_list.keys():
                        # The word already exists
                        # We increase the count by one
                        word_list[word]["count"] += 1
                    else:
                        # The word does not exist
                        # We create a new entry
                        word_list[word] = {"successors": {}, "count": 1}

                    # Save the successor
                    if previous_word is not None:
                        # Will always be invoked except the first time
                        if word in word_list[previous_word]["successors"].keys():
                            # Already Exists, so increase successor count
                            word_list[previous_word]["successors"][word] += 1
                        else:
                            # New entry
                            word_list[previous_word]["successors"][word] = 1

                    previous_word = word

    except:
        raise IOError("Cannot read file. Aborting.")

    # Save as JSON for inspection
    with open("dict.json", "w") as file_write:
        file_write.write(json.dumps(word_list))

    return word_list, alphabet_frequency


def print_character_statistics(character_stats):
    chars_sorted = sorted(character_stats.items(), key=operator.itemgetter(1), reverse=True)
    print()
    print("Most common characters:")
    print(chars_sorted[0:3])
    print()


def print_word_number_statistics(word_stats):
    #a = word_stats
    word_count = sum([word["count"] for word in word_stats.values()])
    print("The given file contains {} words where {} words are unique.".format(word_count, len(word_stats)))
    print()


if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("INVALID NUMBER OF ARGUMENTS. Arguments are:")
    print("(Mandatory) filepath: Path to the text file which should be analyzed.")
    print("(Optional) filepath: Path to an output file where to store the analyzed data.")

try:
    file_stats = parse_file(sys.argv[1])
    print_character_statistics(file_stats[1])
    print_word_number_statistics(file_stats[0])




except ValueError:
    print("The file does not exist")
except IOError:
    print("Cannot read file. Aborting.")






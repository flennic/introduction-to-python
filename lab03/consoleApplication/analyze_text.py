import sys
import os.path
import re
import os
import json
import operator


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
    return "The most common letters are:\n" + str(chars_sorted[0:3])


def print_word_number_statistics(word_stats):
    word_count = sum([word["count"] for word in word_stats.values()])
    return "The given file contains {} words where {} words are unique.".format(word_count, len(word_stats))


def print_word_stats(word, words_stats):

    current_word_stats = words_stats[word]
    successor_stats = sorted(current_word_stats["successors"].items(), key=operator.itemgetter(1), reverse=True)

    return_string = "{} ({} occurrences)\n".format(word, current_word_stats["count"])

    for successor in successor_stats[0:3]:
        return_string += "-- {}, {}\n".format(successor[0], successor[1])

    return_string += "\n"

    return return_string


def print_most_common_words_stats(word_stats_common):

    sorted_dictionary_keys = sorted(word_stats_common, key=lambda x: (word_stats_common[x]['count']), reverse=True)
    word_successors_stats = [print_word_stats(word, word_stats_common) for word in sorted_dictionary_keys[0:5]]

    return_string = "The most common words and successors are:\n\n"

    for word in word_successors_stats:
        return_string += word

    return return_string


if __name__ == "__main__":

    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("INVALID NUMBER OF ARGUMENTS. Arguments are:")
        print("(Mandatory) filepath: Path to the text file which should be analyzed.")
        print("(Optional) filepath: Path to an output file where to store the analyzed data.")

    try:
        file_stats = parse_file(sys.argv[1])
        word_stats = print_word_number_statistics(file_stats[0])
        character_stats = print_character_statistics(file_stats[1])
        common_words_stats = print_most_common_words_stats(file_stats[0])

        print()
        print(word_stats)
        print()
        print(character_stats)
        print()
        print(common_words_stats)

        if len(sys.argv) == 3:
            with open(sys.argv[2], "w") as file:
                file.write("\n\n")
                file.write(word_stats)
                file.write("\n\n")
                file.write(character_stats)
                file.write("\n\n")
                file.write(common_words_stats)
                file.write("\n\n")

    except ValueError:
        print("The file does not exist")
    except IOError:
        print("Cannot read file. Aborting.")






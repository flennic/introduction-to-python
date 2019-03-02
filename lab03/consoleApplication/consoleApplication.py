import sys
import os.path
import re
import os
import json

# TODO: Check if parameters are okay (1, 2) DONE

# TODO: Check, if file exists

# TODO: Frequency table (for alphabetic letters)

# TODO: Wordcount
# TODO: Unique Words

# TODO: 5 Most common words (highest frequency), successor (include no occurrences) and frequency

# Validation of user input

def parse_file(filepath):
    #print(os.getcwd())
    #print(filepath)

    if not os.path.isfile(filepath):
        raise ValueError("File does not exists.")

    word_list = {}

    try:
        with open(filepath, "r") as file:
            for line in file:
                line = re.sub(r'[^a-zA-Z\s]*', '', line)
                entries = line.lower().split()

                previous_word = None

                for word in entries:

                    if word in word_list.keys():
                        # Already exists
                        word_list[word]["count"] += 1
                        #word_list[word]["successor"] =
                    else:
                        # New entry

                        word_information = {"successors": {}, "count": 1}
                        word_list[word] = word_information

                        if previous_word is not None:
                            if word in word_list[previous_word]["successors"].keys():
                                # Already Exists
                                word_list[previous_word]["successors"][word] += 1

                            else:
                                # New entry
                                word_list[previous_word]["successors"][word] = 1

                    previous_word = word


    except:
        raise IOError("Cannot read file. Aborting.")

    with open("dict.json", "w") as file_write:
        file_write.write(json.dumps(word_list))



if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("INVALID NUMBER OF ARGUMENTS. Arguments are:")
    print("(Mandatory) filepath: Path to the text file which should be analyzed.")
    print("(Optional) filepath: Path to an output file where to store the analyzed data.")

try:
    file_stats = parse_file(sys.argv[1])
except ValueError:
    print("The file does not exist")
except IOError:
    print("Cannot read file. Aborting.")






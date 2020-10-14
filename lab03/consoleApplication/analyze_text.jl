using JSON
using OrderedCollections

function parse_file(filepath::String)

    alphabet_frequency = OrderedDict{Char,Int}()
    word_list = OrderedDict{String,Dict}()
    previous_word = nothing

    content = readlines(filepath)

    for (i, line) in enumerate(content)

        line = split(lowercase(replace(line, r"[^a-zA-Z\s]*" => "")), " ", keepempty=false)

        for word in line

            # Character Statistics
            for character in word
                if haskey(alphabet_frequency, character)
                    alphabet_frequency[character] += 1
                else
                    alphabet_frequency[character] = 1
                end
            end

            # Word Statistics
            if haskey(word_list, word)
                # The word already exists
                # We increase the count by one
                word_list[word]["count"] += 1
            else
                # The word does not exist
                # We create a new entry
                word_list[word] = Dict("count" => 1, "successors" => Dict{String, Int}())
            end

            # Save the successor
            if !isnothing(previous_word)
                # Will always be invoked except the first time
                if haskey(word_list[previous_word]["successors"], word)
                    # Already Exists, so increase successor count
                    word_list[previous_word]["successors"][word] += 1
                else
                    # New entry
                    word_list[previous_word]["successors"][word] = 1
                end
            end

            previous_word = word
        end
    end

    open("dict_jul.json","w") do f
        JSON.print(f, word_list)
    end

    return word_list, alphabet_frequency
end

function get_word_statistics(word_stats::OrderedDict{String,Dict})
    word_count = sum([word["count"] for word in values(word_stats)])
    return "The given file contains $word_count words where $(length(word_stats)) words are unique."
end

function get_character_statistics(character_stats::OrderedDict{Char,Int})
    chars_sorted = sort(collect(character_stats), by=x->x[2], rev=true)
    return "The most common letters are: $(chars_sorted[1:3])" 
end

function get_common_word_stats(word::String, word_stats::OrderedDict{String,Dict})
    current_word_stats = word_stats[word]
    successors_stats = sort(collect(current_word_stats["successors"]), by=x->x[2], rev=true)[1:3]
    return_string = "$(word) ($(current_word_stats["count"]) occurrences)\n"

    for successor in successors_stats
        return_string *= "-- $(successor[1]), $(successor[2])\n"
    end

    return_string *= "\n"

    return return_string
end

function get_most_common_words_stats(word_stats::OrderedDict{String,Dict})
    sorted_by_dictionary_keys = sort(word_stats, by = key -> word_stats[key]["count"], rev=true)
    word_successors_stats = [get_common_word_stats(word, word_stats) for (word, _) in collect(sorted_by_dictionary_keys)[1:5]]

    return_string = "The most common words and successors are:\n\n"

    for word in word_successors_stats
        return_string *= word
    end

    return return_string

end

if length(ARGS) < 1 || length(ARGS) > 2
    println("INVALID NUMBER OF ARGUMENTS. Arguments are:")
    println("(Mandatory) filepath: Path to the text file which should be analyzed.")
    println("(Optional) filepath: Path to an output file where to store the analyzed data.")
    throw(ArgumentError("ArgumentError"))
end

word_list, alphabet_frequency = parse_file(ARGS[1])

word_stats = get_word_statistics(word_list)
char_stats = get_character_statistics(alphabet_frequency)
common_words_stats = get_most_common_words_stats(word_list)

println()
println(word_stats)
println()
println(char_stats)
println()
println(common_words_stats)

if length(ARGS) == 2
    open(ARGS[2], "w") do io
        write(io, "\n\n")
        write(io, word_stats)
        write(io, "\n\n")
        write(io, char_stats)
        write(io, "\n\n")
        write(io, common_words_stats)
        write(io, "\n\n")
    end
end
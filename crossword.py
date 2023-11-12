class WordHashTable:
    def __init__(self):
        self.hash_table = {}

    def load_wordlist(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                entry = line.strip()
                word, _ = entry.split(';')
                hash_value = hash(word)
                if hash_value not in self.hash_table:
                    self.hash_table[hash_value] = [entry]
                else:
                    self.hash_table[hash_value].append(entry)

    def search_words_by_length(self, length):
        found_entries = []
        for entries in self.hash_table.values():
            found_entries.extend(entry for entry in entries if len(entry.split(';')[0]) == length)
        return found_entries
    

    def search_words_by_pattern(self, length, pattern):
        found_entries = []
        for entries in self.hash_table.values():
            for entry in entries:
                word, _ = entry.split(';')
                if len(word) == length:
                    match = all(pattern_char == '$' or pattern_char == word[i] for i, pattern_char in enumerate(pattern))
                    if match:
                        found_entries.append(entry)
        return found_entries

# Loading the wordlist and separating the words and their probability
word_table = WordHashTable()
word_table.load_wordlist('EnigmaScan/crossword_wordlist.txt')


length_of_word = input("Please provide the length of unknown word ")
known_letters = input("Please input any known words in the format $$E$$(length of word)($ is place holder) (if none leave blank) ")


flag = False

# if either length of word missing or both missing
if (not length_of_word and known_letters) or (not length_of_word and not known_letters) :
    print("Please provide all the necessary info")

# if no Known words but length is given
elif not known_letters and length_of_word:
   length_of_word  = int(length_of_word)   
   found_entries = word_table.search_words_by_length(length_of_word)
   flag = True

# if both are given
elif known_letters and length_of_word:
   length_of_word  = int(length_of_word)  
   if len(known_letters) != length_of_word:
       print("Please input the correct length")
   else:
       found_entries = word_table.search_words_by_pattern(length_of_word, known_letters)
       flag = True
    

if flag and found_entries:
    print("Found entries:")
    highly_likely = []
    likely = []
    less_likely = []
    least_likely = []
    for entry in found_entries:
        word,probability = entry.split(';')
        probability = int(probability)
        if(probability == 50):
            highly_likely.append(word)
        elif(probability>=25 and probability < 50):
            likely.append(word)
        elif(probability>2 and probability < 25):
            less_likely.append(word)
        elif(probability <=2):
            least_likely.append(word)
    
    word_categories = {
    "Highly likely words": highly_likely,
    "Likely words": likely,
    "Less likely words": less_likely,
    "Least likely words": least_likely,
    }

    for category, words in word_categories.items():
        print(category)
        if len(words) == 0:
            print("No words here!!!")
            continue
        else:
            for word in words:
                print(word)
        print()  # Add a newline between categories


else:
    print(f"No entries found for .")

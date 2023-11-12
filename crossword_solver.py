class CrosswordSolver:
    def __init__(self):
        self.hash_table = {}

    def load_wordlist(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    entry = line.strip()
                    word, _ = entry.split(';')
                    hash_value = hash(word)
                    if hash_value not in self.hash_table:
                        self.hash_table[hash_value] = [entry]
                    else:
                        self.hash_table[hash_value].append(entry)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def search_words(self, length, known_letters):
        found_entries = []
        length = int(length)
        for entries in self.hash_table.values():
            for entry in entries:
                word, probability = entry.split(';')
                if len(word) == length:
                    match = all(
                        known_letters[i] == '$' or known_letters[i] == word[i]
                        for i in range(length)
                    )
                    if match:
                        found_entries.append((word, int(probability)))

        # Sort by probability in descending order
        found_entries.sort(key=lambda x: x[1], reverse=True)

        highly_likely = [word for word, probability in found_entries if probability == 50]
        likely = [word for word, probability in found_entries if 25 <= probability < 50]
        less_likely = [word for word, probability in found_entries if 2 < probability < 25]
        least_likely = [word for word, probability in found_entries if probability <= 2]

        return highly_likely, likely, less_likely, least_likely


# Example usage:
# solver = CrosswordSolver()
# solver.load_wordlist('EnigmaScan/crossword_wordlist.txt')

# length_of_word = input()
# known_letters = list(input())
# known_letters_indexes= list(input())
# know_word = ['$']*int(length_of_word)

# for letter, index in zip(known_letters, known_letters_indexes):
#     know_word[int(index)-1] = letter.upper()
# print(know_word)

# very_likely, likely, less_likely, least_likely = solver.search_words(length_of_word, know_word)
# print(very_likely)
# print(likely)

class EnigmaSearch:
    def __init__(self):
        self.num_rows = None
        self.num_cols = None
        self.directions = [[-1, 0], [1, 0], [1, 1], [1, -1], [-1, -1], [-1, 1], [0, 1], [0, -1]]

    # This function searches in all 8 directions from point (row, col) in grid[][]
    def search_2d(self, grid, start_row, start_col, word):
        # If the first character of the word doesn't match with the given starting point in the grid.
        if grid[start_row][start_col] != word[0]:
            return False

        # Search the word in all 8 directions starting from (start_row, start_col)
        for x, y in self.directions:
            # Initialize starting point for the current direction
            current_row, current_col = start_row + x, start_col + y
            match = True

            # Check the remaining characters
            for k in range(1, len(word)):
                # If out of bounds or not matched, break
                if (
                    0 <= current_row < self.num_rows
                    and 0 <= current_col < self.num_cols
                    and word[k] == grid[current_row][current_col]
                ):
                    # Move in the particular direction
                    current_row += x
                    current_col += y
                else:
                    match = False
                    break

            # If all characters matched, then the value of 'match' must be True
            if match:
                return True
        return False

    # Searches for the given word in a given matrix in all 8 directions
    def enigma_search(self, grid, word):
        # Rows and columns in the given grid
        self.num_rows = len(grid)
        self.num_cols = len(grid[0])
        word = word.upper()
        # Consider every point as a starting point and search for the given word
        for row in range(self.num_rows):
            for col in range(self.num_cols):
                if self.search_2d(grid, row, col, word):

                    return [row, col]
        return ['p', 'p']

# grid = [
#     'CGTAB',
#     'EYDNA',
#     'LMOSO',
# ]
# enigma_solver = EnigmaSearch()
# print(enigma_solver.enigma_search(grid, 'ly'))


import subprocess

class SudokuSolver:
    def __init__(self, cpp_program_path='./EnigmaScan/dancing_links.exe'):
        self.cpp_program_path = cpp_program_path

    def solve(self, sudoku_grid):
        # Convert the grid to a single string with commas
        grid_str = ','.join([','.join(map(str, row)) for row in sudoku_grid])

        try:
            # Call the C++ program and capture the stdout
            output = subprocess.check_output([self.cpp_program_path, grid_str], stderr=subprocess.STDOUT, text=True)
            lines = output.strip().split('\n')
            result_matrix = [list(map(int, line.split())) for line in lines]
            return result_matrix
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error running the C++ program: {e.returncode}\n{e.output}")

# if __name__ == '__main__':
#     # Example Sudoku grid
#     sudoku_grid = [
#         [0, 0, 0, 0, 0, 0, 0, 0, 0],
#         [0, 0, 0, 0, 0, 3, 0, 8, 5],
#         [0, 0, 1, 0, 2, 0, 0, 0, 0],
#         [0, 0, 0, 5, 0, 7, 0, 0, 0],
#         [0, 0, 4, 0, 0, 0, 1, 0, 0],
#         [0, 9, 0, 0, 0, 0, 0, 0, 0],
#         [5, 0, 0, 0, 0, 0, 0, 7, 3],
#         [0, 0, 2, 0, 1, 0, 0, 0, 0],
#         [0, 0, 0, 0, 4, 0, 0, 0, 9]
#     ]

#     # Create an instance of the SudokuSolver class
#     solver = SudokuSolver()

#     # Solve the Sudoku using the C++ program
#     result_matrix = solver.solve(sudoku_grid)

#     # Print the solved Sudoku
#     print("Solved Sudoku:")
#     for row in result_matrix:
#         print(row)

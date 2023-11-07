import cv2
import numpy as np
import easyocr


class SudokuOcr:
    def __init__(self, image_path):
        self.image_path = image_path
        self.reader = easyocr.Reader(['en'])
        self.grid_size = 9
        self.cell_images = self.extract_cell_images()

    def extract_cell_images(self):
        # Load the Sudoku image
        sudoku_image = cv2.imread(self.image_path)

        # Determine the dimensions of the Sudoku grid (assuming it's a square grid)
        grid_size = min(sudoku_image.shape[0], sudoku_image.shape[1])

        # Calculate the size of each cell
        cell_size = grid_size // self.grid_size

        # Initialize an empty list to store the cropped cell images
        cell_images = []

        # Loop through rows and columns to crop the image into 9x9 parts
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                # Calculate the coordinates for cropping each cell
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Crop the cell from the original image
                cell = sudoku_image[y1:y2, x1:x2]

                # Add the cropped cell to the list
                cell_images.append(cell)

        return cell_images

    def cropimage(self, input_image):
        crop_amount = 10
        crop_amount2 = 15
        input_image = cv2.resize(input_image, (100, 100))
        # Get the image dimensions
        width, height = input_image.shape[0], input_image.shape[1]

        # Calculate the cropping box dimensions
        left = crop_amount2
        top = crop_amount
        right = width - crop_amount2
        bottom = height - crop_amount

        # Crop the image equally from all sides
        left, top = crop_amount2, crop_amount
        right, bottom = width - crop_amount2, height - crop_amount

        # Crop the image using NumPy slicing
        return input_image[top:bottom, left:right]

    def solve_sudoku(self):
        matrix = []
        for i in self.cell_images:
            a = self.reader.readtext(self.cropimage(i)) 
            if len(a)>0:
                if len(a[0][1]) == 1 and 1 <= int(a[0][1]) <= 9:
                    matrix.append(int(a[0][1]))
                else:
                    matrix.append(0)
            else:
                matrix.append(0)

        return self.list_to_matrix(matrix, self.grid_size)

    @staticmethod
    def list_to_matrix(lst, n):
        matrixq = []
        for i in range(0, len(lst), n):
            row = lst[i:i + n]
            matrixq.append(row)
        return matrixq

# # Usage example:
# image_path = 'th.jpg'
# sudoku_solver = SudokuSolver(image_path)
# sudoku_matrix = sudoku_solver.solve_sudoku()
# print(sudoku_matrix)
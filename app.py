from flask import Flask,render_template, session, redirect, url_for, flash, request, jsonify
from PIL import Image
import os
import base64
from sudoku_ocr import SudokuOcr as sko
from word_puz_ocr import WordOcr as wdo
from solve_sudoku import SudokuSolver
from solve_word import EnigmaSearch

app = Flask(__name__)
app.secret_key = 'enigmascan2023'

app.config['UPLOAD_FOLDER'] = 'EnigmaScan/static/uploads'
# Route for the home page (index)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sudoku', methods=['GET', 'POST'])
def sudoku():
    success = None
    statement = None
    image = None

    if request.method == 'POST':
        if 'solve-puzzle' in request.form:
                    # If the form was submitted by the "Solve" button, redirect to x.html
            return redirect(url_for('sudokuSolve'))
        if 'file' not in request.files:
            statement = "No file part"
        else:
            file = request.files['file']
            if file.filename == '':
                statement = "No selected file"
            elif file and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], 'puzzle.png')
                file.save(filename)
                image = filename
                success = True
            else:
                statement = "Invalid file type. Allowed extensions: jpg, jpeg, png, gif"

    return render_template('sudoku.html', success=success, statement=statement, image=image)

@app.route('/sudokuSolve', methods=['GET', 'POST'])
def sudokuSolve():
    success = False
    image_path = 'EnigmaScan/static/uploads/cropped_puzzle.jpg'
    sudoku_solver = sko(image_path)
    sudoku_matrix = sudoku_solver.solve_sudoku()
    print(sudoku_matrix)
    if request.method == 'POST':
        matrix = []

        for row in range(9):
            matrix_row = []
            for col in range(9):
                cell_value = request.form['cell_{}_{}'.format(row, col)]
                matrix_row.append(cell_value)
            matrix.append(matrix_row)

        solver = SudokuSolver()

        # Solve the Sudoku using the C++ program
        result_matrix = solver.solve(matrix)
        # Now, 'matrix' contains the data submitted from the form
        # print(matrix)
        success=True
        return render_template('solvedSudoku.html', X=result_matrix, success=success)

    # For the initial GET request, render the template with your initial 'X' data
    return render_template('solvedSudoku.html', X=sudoku_matrix, success=success)


@app.route('/wordSolve', methods=['GET', 'POST'])
def wordSolve():
    success = False
    image_path = 'EnigmaScan/static/uploads/cropped_puzzle.jpg'
    num1 = request.args.get('num1')
    num2 = request.args.get('num2')
    word_ocr =wdo(image_path, int(num1), int(num2))
    word_matrix = word_ocr.solve_word()
    if request.method == 'POST':
        matrix = []
        items = request.form.get('item_list').split(',')
        # Determine the number of rows and columns based on the form submission
        rows = int(request.form['rows'])  # Replace 'rows' with the actual input name for rows
        cols = int(request.form['cols'])  # Replace 'cols' with the actual input name for columns
        for row in range(rows):
            matrix_row = []
            for col in range(cols):
                cell_value = request.form['cell_{}_{}'.format(row, col)]
                matrix_row.append(cell_value)
            matrix.append(matrix_row)

        # Now, 'matrix' contains the data submitted from the form
        # print(matrix)
        success=True
        enigma_solver = EnigmaSearch()
        indexes = []
        for i in items:
            indexes.append(enigma_solver.enigma_search(matrix, i))

        i =0 
        notfound = []
        found_indexes = []
        for index in indexes:
            row, col = index
            if row == 'p':
                notfound.append(items[i])
            else:
                found_indexes.append(index)
            i+=1
        return render_template('solvedWord.html', X=matrix, success=success, notfound=notfound, indexesToHighlight=found_indexes)

    # For the initial GET request, render the template with your initial 'X' data
    print(word_matrix)
    return render_template('solvedWord.html', X=word_matrix, success=success)

@app.route('/wordsearch', methods=['GET', 'POST'])
def wordsearch():
    success = None
    statement = None
    image = None

    if request.method == 'POST':
        if 'solve-puzzle' in request.form:
                    # If the form was submitted by the "Solve" button, redirect to x.html
            number1 = request.form.get('number1')
            number2 = request.form.get('number2')
            return redirect(url_for('wordSolve', num1=number1, num2=number2))
        if 'file' not in request.files:
            statement = "No file part"
        else:
            file = request.files['file']
            if file.filename == '':
                statement = "No selected file"
            elif file and allowed_file(file.filename):
                filename = os.path.join(app.config['UPLOAD_FOLDER'], 'puzzle.png')
                file.save(filename)
                image = filename
                success = True
            else:
                statement = "Invalid file type. Allowed extensions: jpg, jpeg, png, gif"

    return render_template('wordpuzzle.html', success=success, statement=statement, image=image)

def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/save_cropped_image', methods=['POST'])
def save_cropped_image():
    data = request.get_json()
    cropped_image_data = data.get('image')

    # Convert the base64 encoded data to bytes
    try:
        cropped_image_bytes = base64.b64decode(cropped_image_data.split(',')[1])
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

    # Define the new filename (e.g., using a timestamp)
    new_filename = 'cropped_puzzle.jpg'
    filename = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

    # Save the cropped image with the new name
    with open(filename, 'wb') as f:
        f.write(cropped_image_bytes)

    return jsonify({'success': True, 'new_filename': new_filename})


    # Convert the base64 encoded data to bytes


# @app.route('/upload_image', methods=['POST'])
# def upload_image():
#     if 'file' not in request.files:
#         return render_template('sudoku.html', success=False, statment = "No file part")

#     file = request.files['file']
#     if file.filename == '':
#         return render_template('sudoku.html', success= False, statement = "No selected file")

#     if file:
#         filename = os.path.join(app.config['UPLOAD_FOLDER'], 'sudoku.png')
#         file.save(filename)
#         print(filename)
#         return render_template('sudoku.html', success=True, image = filename)
#     return render_template('sudoku.html', success= False, statement = "Upload Failed! Try Again")

# def allowed_file(filename):
#     allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions



@app.route('/crossword')
def crossword():
    return render_template('crossword.html')


if __name__ == '__main__':
    app.run(debug=True)
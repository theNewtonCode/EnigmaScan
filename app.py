from flask import Flask,render_template, session, redirect, url_for, flash, request, jsonify
from PIL import Image
import os
import base64
from sudoku_ocr import SudokuOcr as sko
from word_puz_ocr import WordOcr as wdo
from solve_sudoku import SudokuSolver
from solve_word import EnigmaSearch
from flask_session import Session
from crossword_solver import CrosswordSolver
from capturepuzzle import get_image, url

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
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

        elif 'capture-image' in request.form:
            get_image(url)
            success = True
            image = 'EnigmaScan/static/uploads/puzzle.png'


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

        success=True
        return render_template('solvedSudoku.html', X=result_matrix, success=success)

    # For the initial GET request, render the template with your initial 'X' data
    return render_template('solvedSudoku.html', X=sudoku_matrix, success=success)

def string_to_matrix(input_string):
    # Split the input string by commas to get individual elements
    elements = input_string.split(',')

    # Extract the shape of the matrix
    rows, cols = int(elements[0]), int(elements[1])

    # Remove the shape elements from the list
    elements = elements[2:]

    # Initialize the 2D matrix with zeros
    matrix = [['' for _ in range(cols)] for _ in range(rows)]

    # Populate the matrix with the remaining elements
    for i in range(rows):
        for j in range(cols):
            if elements:
                matrix[i][j] = elements.pop(0)
    
    return matrix

@app.route('/wordSolve', methods=['GET', 'POST'])
def wordSolve():
    success = False
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


        success=True
        enigma_solver = EnigmaSearch()
        indexes = []
        items = [word.strip() for word in items]
        for i in items:
            indexes.append(enigma_solver.enigma_search(matrix, i))

        i =0 
        notfound = []
        found_indexes = []
        for index in indexes:
            row, col = index
            if row == 'p':
                notfound.append(items[i].upper())
            else:
                found_indexes.append(index)
            i+=1

        print(indexes)
        return render_template('solvedWord.html', X=matrix, success=success, notfound=notfound, indexesToHighlight=found_indexes)

    # For the initial GET request, render the template with your initial 'X' data
    # word_matrix = request.args.get('word_matrix')

    # Retrieve the flattened list
    word_matrix_str = session.get('word_matrix')

    if word_matrix_str is not None:
        word_matrix = string_to_matrix(word_matrix_str)
        
        return render_template('solvedWord.html', X=word_matrix, success=success)
    else:
        return "Refresh the process from beginning"

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
            image_path = 'EnigmaScan/static/uploads/cropped_puzzle.jpg'
            word_ocr =wdo(image_path, int(number1), int(number2))
            word_matrix = word_ocr.solve_word()

            # Assuming word_matrix is your 2D matrix
            matrix_shape = (len(word_matrix), len(word_matrix[0]))

            # Create a string with shape and elements separated by commas
            word_matrix_str = f"{matrix_shape[0]},{matrix_shape[1]},{','.join(str(item) for row in word_matrix for item in row)}"
            modified_string = word_matrix_str.replace(" ", "W")
            session['word_matrix'] = modified_string

            return redirect(url_for('wordSolve'))
        
        elif 'capture-image' in request.form:
            get_image(url)
            success = True
            image = 'EnigmaScan/static/uploads/puzzle.png'



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

@app.route('/camcapture')
def camcapture():
    return render_template('ipcam_feature.html')

@app.route('/crossword', methods=['GET', 'POST'])
def crossword():
    result = None
    if request.method == 'POST':
        # Get user inputs from the form
        number_input = int(request.form['number'])
        string1_input = list(request.form['string1'])
        string2_input = list(request.form['string2'])

        # Process the inputs and create four lists
        result = process_input(number_input, string1_input, string2_input)

    return render_template('crossword.html', result=result)

def process_input(length_of_word , known_letters, known_letters_indexes):
    know_word = ['$']*int(length_of_word)
    solver = CrosswordSolver()
    solver.load_wordlist('EnigmaScan/crossword_wordlist.txt')
    for letter, index in zip(known_letters, known_letters_indexes):
        know_word[int(index)-1] = letter.upper()
    very_likely, likely, less_likely, least_likely = solver.search_words(length_of_word, know_word)
    return {'list1': very_likely, 'list2': likely, 'list3': less_likely, 'list4': least_likely}


if __name__ == '__main__':
    app.run(debug=True)
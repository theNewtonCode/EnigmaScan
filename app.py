from flask import Flask,render_template, session, redirect, url_for, flash, request, jsonify
from PIL import Image
import os
import base64

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

@app.route('/sudokuSolve')
def sudokuSolve():
    # Handle the 'x.html' route
    X = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

    return render_template('solvedSudoku.html', X=X)

@app.route('/wordsearch', methods=['GET', 'POST'])
def wordsearch():
    success = None
    statement = None
    image = None

    if request.method == 'POST':
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
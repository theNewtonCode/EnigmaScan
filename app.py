from flask import Flask,render_template, session, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'enigmascan2023'

# Route for the home page (index)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/sudoku')
def sudoku():
    return render_template('sudoku.html')


@app.route('/wordpuzzle')
def wordpuzzle():
    return render_template('wordpuzzle.html')


@app.route('/crossword')
def crossword():
    return render_template('crossword.html')

if __name__ == '__main__':
    app.run(debug=True)

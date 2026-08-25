from flask import Flask, render_template, jsonify, request

from sudoku import generator
from sudoku.service import SudokuGameService

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'hints_used': 0,
}

service = SudokuGameService(generator)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    try:
        clues_argument = request.args.get('clues')
        clues = int(clues_argument) if clues_argument is not None else None
        difficulty = request.args.get('difficulty', 'medium')
        game = service.create_game(clues=clues, difficulty=difficulty)
    except ValueError as error:
        message = str(error)
        if clues_argument is not None and message.startswith('invalid literal'):
            message = 'Clues must be an integer between 1 and 81'
        return jsonify({'error': message}), 400
    CURRENT['puzzle'] = game['puzzle']
    CURRENT['solution'] = game['solution']
    CURRENT['hints_used'] = 0
    return jsonify({'puzzle': game['puzzle']})


@app.route('/hint', methods=['POST'])
def request_hint():
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or 'board' not in data:
        return jsonify({'error': 'Request body must contain a board'}), 400

    try:
        hint = service.get_hint(data['board'], solution)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    CURRENT['hints_used'] = service.hints_used
    return jsonify(hint)


@app.route('/check', methods=['POST'])
def check_solution():
    solution = CURRENT.get('solution')
    if solution is None:
        return jsonify({'error': 'No game in progress'}), 400

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'error': 'Request body must contain valid JSON'}), 400
    if 'board' not in data:
        return jsonify({'error': 'Request body must contain a board'}), 400

    try:
        result = service.check_board(data['board'], solution)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
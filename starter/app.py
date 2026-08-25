import time

from flask import Flask, render_template, jsonify, request

from sudoku import generator
from sudoku.service import SudokuGameService

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None,
    'hints_used': 0,
    'started_at': None,
    'final_elapsed_seconds': None,
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
    CURRENT['started_at'] = int(time.time())
    CURRENT['final_elapsed_seconds'] = None
    return jsonify({
        'puzzle': game['puzzle'],
        'started_at': CURRENT['started_at'],
    })


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
    if not result['incorrect'] and CURRENT.get('final_elapsed_seconds') is None:
        started_at = CURRENT.get('started_at')
        if started_at is not None:
            CURRENT['final_elapsed_seconds'] = max(0, int(time.time()) - started_at)

    if CURRENT.get('final_elapsed_seconds') is not None:
        result['final_elapsed_seconds'] = CURRENT['final_elapsed_seconds']
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, render_template, jsonify, request

import sudoku_logic
from sudoku.service import SudokuGameService

app = Flask(__name__)

# Keep a simple in-memory store for current puzzle and solution
CURRENT = {
    'puzzle': None,
    'solution': None
}

service = SudokuGameService(sudoku_logic)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new')
def new_game():
    try:
        clues = int(request.args.get('clues', 35))
    except (TypeError, ValueError):
        return jsonify({'error': 'Clues must be an integer between 1 and 81'}), 400
    try:
        game = service.create_game(clues)
    except ValueError as error:
        return jsonify({'error': str(error)}), 400
    CURRENT['puzzle'] = game['puzzle']
    CURRENT['solution'] = game['solution']
    return jsonify({'puzzle': game['puzzle']})


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
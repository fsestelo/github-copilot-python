class SudokuGameService:
    def __init__(self, generator, solver=None):
        self.generator = generator
        self.solver = solver

    def create_game(self, clues):
        if type(clues) is not int or not 1 <= clues <= 81:
            raise ValueError('Clues must be an integer between 1 and 81')

        puzzle, solution = self.generator.generate_puzzle(clues)
        return {
            'puzzle': puzzle,
            'solution': solution,
        }

    def check_board(self, board, solution):
        if solution is None:
            raise ValueError('No game in progress')
        if not isinstance(board, list) or len(board) != 9:
            raise ValueError('Board must be a 9x9 grid')
        if any(
            not isinstance(row, list)
            or len(row) != 9
            or any(type(value) is not int or not 0 <= value <= 9 for value in row)
            for row in board
        ):
            raise ValueError('Board must be a 9x9 grid with values from 0 to 9')

        incorrect = []
        for row_index in range(len(solution)):
            for col_index in range(len(solution[row_index])):
                if board[row_index][col_index] != solution[row_index][col_index]:
                    incorrect.append([row_index, col_index])
        return {'incorrect': incorrect}

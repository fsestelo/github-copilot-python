import pytest

from sudoku.constants import DIFFICULTY_CLUES
from sudoku.service import SudokuGameService


class FakeGenerator:
    def generate_puzzle(self, clues):
        puzzle = [[0] * 9 for _ in range(9)]
        solution = [[1] * 9 for _ in range(9)]
        return puzzle, solution


def test_create_game_returns_current_puzzle_and_solution():
    service = SudokuGameService(FakeGenerator())

    assert service.create_game(40) == {
        'puzzle': [[0] * 9 for _ in range(9)],
        'solution': [[1] * 9 for _ in range(9)],
    }


@pytest.mark.parametrize('difficulty, clues', DIFFICULTY_CLUES.items())
def test_create_game_uses_configured_difficulty_clues(difficulty, clues):
    class RecordingGenerator:
        def generate_puzzle(self, received_clues):
            assert received_clues == clues
            return [[0] * 9 for _ in range(9)], [[1] * 9 for _ in range(9)]

    service = SudokuGameService(RecordingGenerator())

    service.create_game(difficulty=difficulty)


def test_check_board_returns_incorrect_coordinates():
    service = SudokuGameService(FakeGenerator())
    solution = [[1] * 9 for _ in range(9)]
    board = [row[:] for row in solution]
    board[0][1] = 2

    assert service.check_board(board, solution) == {'incorrect': [[0, 1]]}


def test_check_board_rejects_missing_game():
    service = SudokuGameService(FakeGenerator())

    with pytest.raises(ValueError, match='No game in progress'):
        service.check_board([], None)


@pytest.mark.parametrize('clues', [0, 82, '40'])
def test_create_game_rejects_invalid_clues(clues):
    service = SudokuGameService(FakeGenerator())

    with pytest.raises(ValueError, match='Clues must be an integer between 1 and 81'):
        service.create_game(clues)


def test_check_board_rejects_invalid_board():
    service = SudokuGameService(FakeGenerator())
    solution = [[1] * 9 for _ in range(9)]

    with pytest.raises(ValueError, match='9x9'):
        service.check_board([], solution)
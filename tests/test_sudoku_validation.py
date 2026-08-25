from sudoku.board import create_empty_board
from sudoku.validation import is_safe


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = create_empty_board()
    board[0][0] = 5

    assert is_safe(board, 0, 1, 5) is False
    assert is_safe(board, 1, 0, 5) is False
    assert is_safe(board, 1, 1, 5) is False
    assert is_safe(board, 1, 1, 6) is True
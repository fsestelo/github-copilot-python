from sudoku.board import create_empty_board, deep_copy


def test_create_empty_board_has_nine_rows_of_empty_cells():
    board = create_empty_board()

    assert board == [[0] * 9 for _ in range(9)]
    assert len({id(row) for row in board}) == 9


def test_deep_copy_is_independent():
    board = [[1, 2], [3, 4]]

    copied = deep_copy(board)
    copied[0][0] = 9

    assert board[0][0] == 1
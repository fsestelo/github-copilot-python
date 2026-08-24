import random

import sudoku_logic


def assert_valid_solution(board):
    expected = set(range(1, sudoku_logic.SIZE + 1))
    assert all(set(row) == expected for row in board)
    assert all(
        {board[row][column] for row in range(sudoku_logic.SIZE)} == expected
        for column in range(sudoku_logic.SIZE)
    )
    assert all(
        {
            board[row][column]
            for row in range(box_row, box_row + 3)
            for column in range(box_column, box_column + 3)
        }
        == expected
        for box_row in range(0, sudoku_logic.SIZE, 3)
        for box_column in range(0, sudoku_logic.SIZE, 3)
    )


def test_create_empty_board_has_nine_rows_of_empty_cells():
    board = sudoku_logic.create_empty_board()

    assert board == [[0] * 9 for _ in range(9)]
    assert len({id(row) for row in board}) == 9


def test_deep_copy_is_independent():
    board = [[1, 2], [3, 4]]

    copied = sudoku_logic.deep_copy(board)
    copied[0][0] = 9

    assert board[0][0] == 1


def test_is_safe_rejects_row_column_and_box_conflicts():
    board = sudoku_logic.create_empty_board()
    board[0][0] = 5

    assert sudoku_logic.is_safe(board, 0, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 0, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 5) is False
    assert sudoku_logic.is_safe(board, 1, 1, 6) is True


def test_fill_board_creates_a_valid_solution():
    random.seed(7)
    board = sudoku_logic.create_empty_board()

    assert sudoku_logic.fill_board(board) is True
    assert_valid_solution(board)


def test_remove_cells_leaves_requested_number_of_clues():
    random.seed(7)
    board = sudoku_logic.create_empty_board()
    sudoku_logic.fill_board(board)

    sudoku_logic.remove_cells(board, clues=35)

    assert sum(cell != sudoku_logic.EMPTY for row in board for cell in row) == 35


def test_generate_puzzle_returns_valid_solution_and_requested_clues():
    random.seed(7)

    puzzle, solution = sudoku_logic.generate_puzzle(clues=40)

    assert_valid_solution(solution)
    assert sum(cell != sudoku_logic.EMPTY for row in puzzle for cell in row) == 40
    assert all(
        puzzle[row][column] in (sudoku_logic.EMPTY, solution[row][column])
        for row in range(sudoku_logic.SIZE)
        for column in range(sudoku_logic.SIZE)
    )

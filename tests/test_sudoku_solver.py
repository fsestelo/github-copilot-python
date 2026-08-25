import random

from sudoku.board import create_empty_board
from sudoku.solver import count_solutions, fill_board


def assert_valid_solution(board):
    expected = set(range(1, 10))
    assert all(set(row) == expected for row in board)
    assert all(
        {board[row][column] for row in range(9)} == expected
        for column in range(9)
    )
    assert all(
        {
            board[row][column]
            for row in range(box_row, box_row + 3)
            for column in range(box_column, box_column + 3)
        }
        == expected
        for box_row in range(0, 9, 3)
        for box_column in range(0, 9, 3)
    )


def test_fill_board_creates_a_valid_solution():
    random.seed(7)
    board = create_empty_board()

    assert fill_board(board) is True
    assert_valid_solution(board)


def test_count_solutions_on_solved_board_is_one():
    board = create_empty_board()
    assert fill_board(board) is True

    assert count_solutions(board) == 1


def test_count_solutions_on_unsolvable_board_is_zero():
    board = create_empty_board()
    board[0][0] = 1
    board[0][1] = 1

    assert count_solutions(board) == 0


def test_count_solutions_on_multiple_solution_board_is_two():
    board = create_empty_board()
    board[0][0] = 1

    assert count_solutions(board) == 2
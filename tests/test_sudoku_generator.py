import random

from sudoku.board import create_empty_board
from sudoku.generator import generate_puzzle, remove_cells
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


def test_remove_cells_leaves_requested_number_of_clues():
    random.seed(7)
    board = create_empty_board()
    fill_board(board)

    remove_cells(board, clues=35)

    assert sum(cell != 0 for row in board for cell in row) == 35


def test_generate_puzzle_returns_valid_solution_and_requested_clues():
    random.seed(7)

    puzzle, solution = generate_puzzle(clues=40)

    assert_valid_solution(solution)
    assert sum(cell != 0 for row in puzzle for cell in row) == 40
    assert all(
        puzzle[row][column] in (0, solution[row][column])
        for row in range(9)
        for column in range(9)
    )


def test_generated_puzzle_has_exactly_one_solution():
    random.seed(7)
    puzzle, solution = generate_puzzle(clues=30)

    assert_valid_solution(solution)
    assert count_solutions(puzzle) == 1
    assert sum(cell != 0 for row in puzzle for cell in row) == 30
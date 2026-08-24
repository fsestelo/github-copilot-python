import random

from sudoku.board import create_empty_board, deep_copy
from sudoku.constants import EMPTY, SIZE
from sudoku.solver import count_solutions, fill_board


def remove_cells(board, clues):
    target_removed = SIZE * SIZE - clues
    removed = 0
    positions = [(row, col) for row in range(SIZE) for col in range(SIZE)]
    random.shuffle(positions)

    for row, col in positions:
        if removed >= target_removed:
            break
        if board[row][col] == EMPTY:
            continue

        original = board[row][col]
        board[row][col] = EMPTY
        if count_solutions(board) != 1:
            board[row][col] = original
            continue

        removed += 1


def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution

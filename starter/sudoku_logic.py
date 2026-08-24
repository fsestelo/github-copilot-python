import random

from sudoku.board import create_empty_board as _create_empty_board
from sudoku.board import deep_copy as _deep_copy
from sudoku.constants import EMPTY, SIZE
from sudoku.generator import generate_puzzle as _generate_puzzle
from sudoku.generator import remove_cells as _remove_cells
from sudoku.solver import fill_board as _fill_board
from sudoku.validation import is_safe as _is_safe


def deep_copy(board):
    return _deep_copy(board)


def create_empty_board():
    return _create_empty_board()


def is_safe(board, row, col, num):
    return _is_safe(board, row, col, num)


def fill_board(board):
    return _fill_board(board)


def remove_cells(board, clues):
    return _remove_cells(board, clues)


def generate_puzzle(clues=35):
    return _generate_puzzle(clues)

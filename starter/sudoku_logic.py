import random

from sudoku.board import create_empty_board as _create_empty_board
from sudoku.board import deep_copy as _deep_copy
from sudoku.constants import EMPTY, SIZE
from sudoku.validation import is_safe as _is_safe


def deep_copy(board):
    return _deep_copy(board)


def create_empty_board():
    return _create_empty_board()


def is_safe(board, row, col, num):
    return _is_safe(board, row, col, num)

def fill_board(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == EMPTY:
                possible = list(range(1, SIZE + 1))
                random.shuffle(possible)
                for candidate in possible:
                    if is_safe(board, row, col, candidate):
                        board[row][col] = candidate
                        if fill_board(board):
                            return True
                        board[row][col] = EMPTY
                return False
    return True

def remove_cells(board, clues):
    attempts = SIZE * SIZE - clues
    while attempts > 0:
        row = random.randrange(SIZE)
        col = random.randrange(SIZE)
        if board[row][col] != EMPTY:
            board[row][col] = EMPTY
            attempts -= 1

def generate_puzzle(clues=35):
    board = create_empty_board()
    fill_board(board)
    solution = deep_copy(board)
    remove_cells(board, clues)
    puzzle = deep_copy(board)
    return puzzle, solution

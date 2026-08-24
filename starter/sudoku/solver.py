import random

from sudoku.constants import EMPTY, SIZE
from sudoku.validation import is_safe


def _has_conflict(board):
    for row in range(SIZE):
        seen = set()
        for value in board[row]:
            if value == EMPTY:
                continue
            if value in seen:
                return True
            seen.add(value)

    for col in range(SIZE):
        seen = set()
        for row in range(SIZE):
            value = board[row][col]
            if value == EMPTY:
                continue
            if value in seen:
                return True
            seen.add(value)

    for box_row in range(0, SIZE, 3):
        for box_col in range(0, SIZE, 3):
            seen = set()
            for row in range(box_row, box_row + 3):
                for col in range(box_col, box_col + 3):
                    value = board[row][col]
                    if value == EMPTY:
                        continue
                    if value in seen:
                        return True
                    seen.add(value)

    return False


def count_solutions(board):
    working = [row[:] for row in board]
    if _has_conflict(working):
        return 0

    solution_count = 0

    def backtrack():
        nonlocal solution_count

        if solution_count >= 2:
            return
        if _has_conflict(working):
            return

        for row in range(SIZE):
            for col in range(SIZE):
                if working[row][col] == EMPTY:
                    for candidate in range(1, SIZE + 1):
                        if not is_safe(working, row, col, candidate):
                            continue
                        working[row][col] = candidate
                        backtrack()
                        working[row][col] = EMPTY
                        if solution_count >= 2:
                            return
                    return

        solution_count += 1

    backtrack()
    return solution_count


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

import pytest

import app
import sudoku_logic


@pytest.fixture
def client():
    app.CURRENT["puzzle"] = None
    app.CURRENT["solution"] = None
    app.app.config.update(TESTING=True)
    with app.app.test_client() as test_client:
        yield test_client
    app.CURRENT["puzzle"] = None
    app.CURRENT["solution"] = None


def test_index_renders_game_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert "Sudoku" in response.get_data(as_text=True)


def test_new_game_returns_puzzle_and_stores_solution(client, monkeypatch):
    puzzle = [[0] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]
    solution = [[1] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]

    def fake_generate_puzzle(clues):
        assert clues == 40
        return puzzle, solution

    monkeypatch.setattr(app.sudoku_logic, "generate_puzzle", fake_generate_puzzle)

    response = client.get("/new?clues=40")

    assert response.status_code == 200
    assert response.json == {"puzzle": puzzle}
    assert app.CURRENT == {"puzzle": puzzle, "solution": solution}


@pytest.mark.parametrize("clues", ["abc", "0", "82"])
def test_new_game_rejects_invalid_clues(client, clues):
    response = client.get(f"/new?clues={clues}")

    assert response.status_code == 400
    assert response.json == {"error": "Clues must be an integer between 1 and 81"}


def test_check_solution_reports_no_game_in_progress(client):
    response = client.post("/check", json={"board": []})

    assert response.status_code == 400
    assert response.json == {"error": "No game in progress"}


def test_check_solution_reports_coordinates_that_differ(client):
    solution = [[1] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]
    board = [row[:] for row in solution]
    board[0][1] = 2
    app.CURRENT["solution"] = solution

    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.json == {"incorrect": [[0, 1]]}


def test_check_solution_rejects_invalid_json(client):
    app.CURRENT["solution"] = [[1] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]

    response = client.post(
        "/check",
        data="{invalid",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Request body must contain valid JSON"}


def test_check_solution_rejects_missing_board(client):
    app.CURRENT["solution"] = [[1] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]

    response = client.post("/check", json={})

    assert response.status_code == 400
    assert response.json == {"error": "Request body must contain a board"}


@pytest.mark.parametrize(
    "board",
    [
        [],
        [[0] * sudoku_logic.SIZE for _ in range(8)],
        [[0] * 8 for _ in range(sudoku_logic.SIZE)],
        [[10] + [0] * 8] + [[0] * sudoku_logic.SIZE for _ in range(8)],
    ],
)
def test_check_solution_rejects_invalid_board(client, board):
    app.CURRENT["solution"] = [[1] * sudoku_logic.SIZE for _ in range(sudoku_logic.SIZE)]

    response = client.post("/check", json={"board": board})

    assert response.status_code == 400


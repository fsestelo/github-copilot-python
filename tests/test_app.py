import pytest

import app
from sudoku.constants import SIZE


@pytest.fixture
def client():
    app.CURRENT["puzzle"] = None
    app.CURRENT["solution"] = None
    app.CURRENT["started_at"] = None
    app.CURRENT["final_elapsed_seconds"] = None
    app.app.config.update(TESTING=True)
    with app.app.test_client() as test_client:
        yield test_client
    app.CURRENT["puzzle"] = None
    app.CURRENT["solution"] = None
    app.CURRENT["hints_used"] = 0
    app.CURRENT["started_at"] = None
    app.CURRENT["final_elapsed_seconds"] = None


def test_index_renders_game_page(client):
    response = client.get("/")

    assert response.status_code == 200
    page = response.get_data(as_text=True)
    assert "Sudoku" in page
    assert 'id="difficulty"' in page
    assert 'value="easy"' in page
    assert 'value="medium"' in page
    assert 'value="hard"' in page


def test_new_game_returns_puzzle_and_stores_solution(client, monkeypatch):
    puzzle = [[0] * SIZE for _ in range(SIZE)]
    solution = [[1] * SIZE for _ in range(SIZE)]

    def fake_generate_puzzle(clues):
        assert clues == 40
        return puzzle, solution

    monkeypatch.setattr(app.generator, "generate_puzzle", fake_generate_puzzle)
    monkeypatch.setattr(app.time, "time", lambda: 1000)

    response = client.get("/new?clues=40")

    assert response.status_code == 200
    assert response.json == {"puzzle": puzzle, "started_at": 1000}
    assert app.CURRENT == {
        "puzzle": puzzle,
        "solution": solution,
        "hints_used": 0,
        "started_at": 1000,
        "final_elapsed_seconds": None,
    }


@pytest.mark.parametrize("clues", ["abc", "0", "82"])
def test_new_game_rejects_invalid_clues(client, clues):
    response = client.get(f"/new?clues={clues}")

    assert response.status_code == 400
    assert response.json == {"error": "Clues must be an integer between 1 and 81"}


@pytest.mark.parametrize("difficulty, clues", [("easy", 45), ("medium", 35), ("hard", 28)])
def test_new_game_accepts_difficulty_level(client, monkeypatch, difficulty, clues):
    puzzle = [[0] * SIZE for _ in range(SIZE)]
    solution = [[1] * SIZE for _ in range(SIZE)]

    def fake_generate_puzzle(received_clues):
        assert received_clues == clues
        return puzzle, solution

    monkeypatch.setattr(app.generator, "generate_puzzle", fake_generate_puzzle)

    response = client.get(f"/new?difficulty={difficulty}")

    assert response.status_code == 200
    assert response.json["puzzle"] == puzzle
    assert isinstance(response.json["started_at"], int)


def test_new_game_rejects_invalid_difficulty(client):
    response = client.get("/new?difficulty=expert")

    assert response.status_code == 400
    assert response.json == {"error": "Difficulty must be easy, medium, or hard"}


def test_check_solution_reports_no_game_in_progress(client):
    response = client.post("/check", json={"board": []})

    assert response.status_code == 400
    assert response.json == {"error": "No game in progress"}


def test_check_solution_reports_coordinates_that_differ(client):
    solution = [[1] * SIZE for _ in range(SIZE)]
    board = [row[:] for row in solution]
    board[0][1] = 2
    app.CURRENT["solution"] = solution
    app.CURRENT["started_at"] = 1000

    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.json == {"incorrect": [[0, 1]]}
    assert app.CURRENT["final_elapsed_seconds"] is None


def test_check_solution_stores_and_returns_authoritative_elapsed_time(client, monkeypatch):
    solution = [[1] * SIZE for _ in range(SIZE)]
    app.CURRENT["solution"] = solution
    app.CURRENT["started_at"] = 1000
    board = [row[:] for row in solution]
    monkeypatch.setattr(app.time, "time", lambda: 1123)

    response = client.post("/check", json={"board": board})

    assert response.status_code == 200
    assert response.json == {"incorrect": [], "final_elapsed_seconds": 123}
    assert app.CURRENT["final_elapsed_seconds"] == 123


def test_check_solution_keeps_final_elapsed_time(client, monkeypatch):
    solution = [[1] * SIZE for _ in range(SIZE)]
    app.CURRENT["solution"] = solution
    app.CURRENT["started_at"] = 1000
    app.CURRENT["final_elapsed_seconds"] = 123
    board = [row[:] for row in solution]
    monkeypatch.setattr(app.time, "time", lambda: 1500)

    response = client.post("/check", json={"board": board})

    assert response.json == {"incorrect": [], "final_elapsed_seconds": 123}


def test_check_solution_rejects_invalid_json(client):
    app.CURRENT["solution"] = [[1] * SIZE for _ in range(SIZE)]

    response = client.post(
        "/check",
        data="{invalid",
        content_type="application/json",
    )

    assert response.status_code == 400
    assert response.json == {"error": "Request body must contain valid JSON"}


def test_check_solution_rejects_missing_board(client):
    app.CURRENT["solution"] = [[1] * SIZE for _ in range(SIZE)]

    response = client.post("/check", json={})

    assert response.status_code == 400
    assert response.json == {"error": "Request body must contain a board"}


@pytest.mark.parametrize(
    "board",
    [
        [],
        [[0] * SIZE for _ in range(8)],
        [[0] * 8 for _ in range(SIZE)],
        [[10] + [0] * 8] + [[0] * SIZE for _ in range(8)],
    ],
)
def test_check_solution_rejects_invalid_board(client, board):
    app.CURRENT["solution"] = [[1] * SIZE for _ in range(SIZE)]

    response = client.post("/check", json={"board": board})

    assert response.status_code == 400


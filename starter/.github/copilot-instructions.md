--- 
applyTo: '**' 
---
# Copilot Instructions

## Project Context

This project is a Flask-based Sudoku game.

The project is a legacy codebase being modernized incrementally.

Preserve existing behavior unless a change is explicitly requested.

## Backend

- Use modern Python.
- Prefer type hints.
- Prefer small, reusable functions.
- Keep Sudoku game logic independent from Flask.
- Keep business logic separate from HTTP routes.

## Architecture

- Avoid putting business logic directly in `app.py`.
- Keep Flask routes focused on handling HTTP requests.
- Separate game logic, application logic, and presentation concerns.
- Avoid unnecessary architectural changes.
- Prefer incremental refactoring.

## Testing

- Use pytest for automated tests.
- New functionality should include appropriate tests.
- Do not modify existing tests just to make them pass.
- Preserve existing behavior when refactoring.

## Frontend

- Use vanilla JavaScript.
- Keep DOM manipulation organized.
- Avoid unnecessary dependencies.
- Keep frontend logic separate from backend logic.

## Code Quality

- Follow PEP 8.
- Prefer clear names over clever implementations.
- Use docstrings for public functions.
- Use explicit error handling.
- Keep functions focused and reasonably small.

## Copilot Behavior

When suggesting significant changes:

- Explain the reasoning behind the change.
- Preserve existing behavior unless explicitly requested otherwise.
- Prefer incremental refactoring.
- Avoid unnecessary dependencies.
- Avoid unnecessary architectural changes.
- Consider existing tests before modifying implementation.
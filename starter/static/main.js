// Client-side rendering and interaction for the Flask-backed Sudoku
const SIZE = 9;
const THEME_STORAGE_KEY = 'sudoku-theme';
let puzzle = [];
let hintsUsed = 0;
let timerInterval = null;
let startedAt = null;
let scoreSaved = false;
let notes = createNotes();
let noteMode = false;

function createNotes() {
  return Array.from({length: SIZE * SIZE}, () => new Set());
}

function toggleNote(noteState, cellIndex, value, locked = false) {
  if (locked) return;
  if (!Number.isInteger(value) || value < 1 || value > 9) return;
  if (noteState[cellIndex].has(value)) {
    noteState[cellIndex].delete(value);
  } else {
    noteState[cellIndex].add(value);
  }
}

function clearCellNotes(noteState, cellIndex) {
  noteState[cellIndex].clear();
}

function getSelectedNotes(noteState, cellIndex) {
  return [...noteState[cellIndex]].sort((first, second) => first - second);
}

function renderCellNotes(input, cellIndex, noteState = notes) {
  const selectedNotes = getSelectedNotes(noteState, cellIndex);
  if (selectedNotes.length === 1) {
    input.value = selectedNotes[0];
  } else if (selectedNotes.length >= 2 || noteMode) {
    input.value = '';
  }
  const noteElements = input.parentElement.querySelectorAll('[data-note]');
  noteElements.forEach((noteElement) => {
    const value = Number(noteElement.dataset.note);
    noteElement.innerText = selectedNotes.length >= 2 && selectedNotes.includes(value)
      ? value
      : '';
  });
}

function setNoteMode(active) {
  noteMode = active;
  const toggle = document.getElementById('note-mode');
  toggle.setAttribute('aria-pressed', String(noteMode));
  toggle.innerText = `Note Mode: ${noteMode ? 'On' : 'Off'}`;
}

function handleCellInput(input) {
  const value = input.value.replace(/[^1-9]/g, '').slice(0, 1);
  input.value = value;
  const cellIndex = Number(input.dataset.index);
  if (noteMode) {
    if (value) toggleNote(notes, cellIndex, Number(value), input.disabled);
    renderCellNotes(input, cellIndex);
    return;
  }
  if (value) clearCellNotes(notes, cellIndex);
  renderCellNotes(input, cellIndex);
}

function applyTheme(theme) {
  const activeTheme = theme === 'dark' ? 'dark' : 'light';
  document.documentElement.dataset.theme = activeTheme;
  const toggle = document.getElementById('theme-toggle');
  if (toggle) {
    const darkMode = activeTheme === 'dark';
    toggle.setAttribute('aria-pressed', String(darkMode));
    toggle.innerText = darkMode ? 'Light mode' : 'Dark mode';
  }
}

function restoreTheme() {
  applyTheme(window.localStorage.getItem(THEME_STORAGE_KEY));
}

function toggleTheme() {
  const nextTheme = document.documentElement.dataset.theme === 'dark'
    ? 'light'
    : 'dark';
  applyTheme(nextTheme);
  window.localStorage.setItem(THEME_STORAGE_KEY, nextTheme);
}

function formatElapsedTime(totalSeconds) {
  const minutes = Math.floor(totalSeconds / 60);
  const seconds = totalSeconds % 60;
  return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function updateTimer() {
  if (startedAt === null) return;
  const elapsedSeconds = Math.max(0, Math.floor(Date.now() / 1000) - startedAt);
  document.getElementById('timer').innerText = formatElapsedTime(elapsedSeconds);
}

function startTimer(gameStartedAt) {
  clearInterval(timerInterval);
  startedAt = gameStartedAt;
  updateTimer();
  timerInterval = setInterval(updateTimer, 1000);
}

function stopTimer(finalElapsedSeconds) {
  clearInterval(timerInterval);
  timerInterval = null;
  document.getElementById('timer').innerText = formatElapsedTime(finalElapsedSeconds);
}

function renderScoreboard(scores) {
  const body = document.getElementById('scoreboard-body');
  body.innerHTML = '';
  scores.forEach((score) => {
    const row = document.createElement('tr');
    [score.name, formatElapsedTime(score.time), score.difficulty, score.hints]
      .forEach((value) => {
        const cell = document.createElement('td');
        cell.innerText = value;
        row.appendChild(cell);
      });
    body.appendChild(row);
  });
}

function saveCompletedGame(finalElapsedSeconds) {
  if (scoreSaved) return;
  scoreSaved = true;
  const name = window.prompt('Enter your name for the Top 10 scoreboard:') || 'Anonymous';
  const scores = Scoreboard.saveScore(window.localStorage, {
    name: name.trim() || 'Anonymous',
    time: finalElapsedSeconds,
    difficulty: document.getElementById('difficulty').value,
    hints: hintsUsed,
  });
  renderScoreboard(scores);
}

function createBoardElement() {
  const boardDiv = document.getElementById('sudoku-board');
  boardDiv.innerHTML = '';
  for (let i = 0; i < SIZE; i++) {
    const rowDiv = document.createElement('div');
    rowDiv.className = 'sudoku-row';
    for (let j = 0; j < SIZE; j++) {
        const cell = document.createElement('div');
        cell.className = 'sudoku-cell';
        cell.dataset.row = i;
        cell.dataset.col = j;
      const input = document.createElement('input');
      input.type = 'text';
      input.maxLength = 1;
        input.className = 'sudoku-value';
      input.dataset.row = i;
      input.dataset.col = j;
        input.dataset.index = i * SIZE + j;
        input.setAttribute('aria-label', `Row ${i + 1}, column ${j + 1}`);
          input.addEventListener('keydown', (event) => {
            if (!noteMode || input.disabled || !/^[1-9]$/.test(event.key)) return;
            event.preventDefault();
            toggleNote(notes, Number(input.dataset.index), Number(event.key));
            renderCellNotes(input, Number(input.dataset.index));
          });
        input.addEventListener('input', () => handleCellInput(input));
        cell.appendChild(input);
        const noteGrid = document.createElement('span');
        noteGrid.className = 'sudoku-notes';
        noteGrid.setAttribute('aria-hidden', 'true');
        for (let value = 1; value <= SIZE; value++) {
          const note = document.createElement('span');
          note.dataset.note = value;
          noteGrid.appendChild(note);
        }
        cell.appendChild(noteGrid);
        rowDiv.appendChild(cell);
    }
    boardDiv.appendChild(rowDiv);
  }
}

function renderPuzzle(puz) {
  puzzle = puz;
  notes = createNotes();
  hintsUsed = 0;
  scoreSaved = false;
  createBoardElement();
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  for (let i = 0; i < SIZE; i++) {
    for (let j = 0; j < SIZE; j++) {
      const idx = i * SIZE + j;
      const val = puzzle[i][j];
      const inp = inputs[idx];
      const cell = inp.parentElement;
      if (val !== 0) {
        inp.value = val;
        inp.disabled = true;
        cell.className = 'sudoku-cell prefilled';
      } else {
        inp.value = '';
        inp.disabled = false;
        cell.className = 'sudoku-cell';
      }
      renderCellNotes(inp, idx);
    }
  }
}

async function newGame() {
  const difficulty = document.getElementById('difficulty').value;
  const res = await fetch(`/new?difficulty=${encodeURIComponent(difficulty)}`);
  const data = await res.json();
  renderPuzzle(data.puzzle);
  startTimer(data.started_at);
  document.getElementById('message').innerText = '';
}

async function checkSolution() {
  const boardDiv = document.getElementById('sudoku-board');
  const inputs = boardDiv.getElementsByTagName('input');
  const board = getCurrentBoard(inputs);
  const res = await fetch('/check', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = 'var(--error)';
    msg.innerText = data.error;
    return;
  }
  const incorrect = new Set(data.incorrect.map(x => x[0]*SIZE + x[1]));
  for (let idx = 0; idx < inputs.length; idx++) {
    const inp = inputs[idx];
    const cell = inp.parentElement;
    if (inp.disabled) continue;
    cell.className = 'sudoku-cell';
    if (incorrect.has(idx)) {
      cell.className = 'sudoku-cell incorrect';
    }
  }
  if (incorrect.size === 0) {
    if (data.final_elapsed_seconds !== undefined) {
      stopTimer(data.final_elapsed_seconds);
      saveCompletedGame(data.final_elapsed_seconds);
    }
    msg.style.color = 'var(--success)';
    msg.innerText = 'Congratulations! You solved it!';
  } else {
    msg.style.color = 'var(--error)';
    msg.innerText = 'Some cells are incorrect.';
  }
}

function getCurrentBoard(inputs, noteState = notes) {
  const board = [];
  for (let i = 0; i < SIZE; i++) {
    board[i] = [];
    for (let j = 0; j < SIZE; j++) {
      const cellIndex = i * SIZE + j;
      const input = inputs[i * SIZE + j];
      const selectedNotes = getSelectedNotes(noteState, cellIndex);
      board[i][j] = selectedNotes.length >= 2
        ? 0
        : selectedNotes.length === 1
          ? selectedNotes[0]
          : (input.value ? parseInt(input.value, 10) : 0);
    }
  }
  return board;
}

async function requestHint() {
  const inputs = document.getElementById('sudoku-board').getElementsByTagName('input');
  const res = await fetch('/hint', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({board: getCurrentBoard(inputs)})
  });
  const data = await res.json();
  const msg = document.getElementById('message');
  if (data.error) {
    msg.style.color = 'var(--error)';
    msg.innerText = data.error;
    return;
  }

  const input = inputs[data.row * SIZE + data.column];
  const cellIndex = data.row * SIZE + data.column;
  clearCellNotes(notes, cellIndex);
  renderCellNotes(input, cellIndex);
  input.value = data.value;
  input.disabled = true;
  input.parentElement.className = 'sudoku-cell hint';
  hintsUsed++;
  msg.style.color = 'var(--success)';
  msg.innerText = `Hint used: ${hintsUsed}`;
}

if (typeof window !== 'undefined') {
  window.addEventListener('load', () => {
    restoreTheme();
    document.getElementById('theme-toggle').addEventListener('click', toggleTheme);
    document.getElementById('new-game').addEventListener('click', newGame);
    document.getElementById('hint').addEventListener('click', requestHint);
    document.getElementById('check-solution').addEventListener('click', checkSolution);
    document.getElementById('note-mode').addEventListener('click', () => setNoteMode(!noteMode));
    renderScoreboard(Scoreboard.loadScores(window.localStorage));
    newGame();
  });
}

if (typeof module !== 'undefined') {
  module.exports = {createNotes, toggleNote, clearCellNotes, getCurrentBoard};
}
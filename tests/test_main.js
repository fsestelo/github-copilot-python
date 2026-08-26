const assert = require('assert');
const {
  createNotes,
  toggleNote,
  clearCellNotes,
  getCurrentBoard,
  getConflictingCells,
  checkConflict,
} = require('../starter/static/main.js');

const inputsFor = (values) => values.map((value) => ({value: value ? String(value) : ''}));
const boardInputs = (values) => values.map((value) => {
  const classes = new Set();
  return {
    value: value ? String(value) : '',
    parentElement: {classList: {
      toggle: (name, active) => active ? classes.add(name) : classes.delete(name),
      contains: (name) => classes.has(name),
    }},
  };
});
const indexOf = (row, col) => row * 9 + col;

const notes = createNotes();
toggleNote(notes, 0, 4);
assert.deepStrictEqual([...notes[0]], [4]);
toggleNote(notes, 0, 4);
assert.deepStrictEqual([...notes[0]], []);

toggleNote(notes, 0, 1);
toggleNote(notes, 0, 5);
toggleNote(notes, 0, 9);
assert.deepStrictEqual([...notes[0]], [1, 5, 9]);
toggleNote(notes, 0, 2, true);
assert.deepStrictEqual([...notes[0]], [1, 5, 9]);

clearCellNotes(notes, 0);
assert.deepStrictEqual([...notes[0]], []);
toggleNote(notes, 0, 3);
clearCellNotes(notes, 0);
assert.deepStrictEqual([...notes[0]], []);

const boardValues = Array.from({length: 81}, () => 0);
const singleValueNotes = createNotes();
toggleNote(singleValueNotes, 0, 7);
const board = getCurrentBoard(inputsFor(boardValues), singleValueNotes);
assert.strictEqual(board.length, 9);
assert.strictEqual(board[0].length, 9);
assert.strictEqual(board[0][0], 7);
assert.strictEqual(board.flat().every((value) => Number.isInteger(value)), true);

const multipleValueNotes = createNotes();
toggleNote(multipleValueNotes, 0, 2);
toggleNote(multipleValueNotes, 0, 8);
assert.strictEqual(getCurrentBoard(inputsFor([8, ...Array(80).fill(0)]), multipleValueNotes)[0][0], 0);

const rowInputs = boardInputs(Array(81).fill(0));
rowInputs[indexOf(0, 0)].value = '4';
rowInputs[indexOf(0, 4)].value = '4';
assert.deepStrictEqual([...getConflictingCells(0, 0, 4, rowInputs)], [indexOf(0, 4)]);

const columnInputs = boardInputs(Array(81).fill(0));
columnInputs[indexOf(0, 1)].value = '5';
columnInputs[indexOf(7, 1)].value = '5';
assert.deepStrictEqual([...getConflictingCells(0, 1, 5, columnInputs)], [indexOf(7, 1)]);

const blockInputs = boardInputs(Array(81).fill(0));
blockInputs[indexOf(1, 1)].value = '6';
blockInputs[indexOf(2, 2)].value = '6';
assert.deepStrictEqual([...getConflictingCells(1, 1, 6, blockInputs)], [indexOf(2, 2)]);

const conflictInputs = boardInputs(Array(81).fill(0));
conflictInputs[indexOf(0, 0)].value = '7';
conflictInputs[indexOf(0, 3)].value = '7';
assert.strictEqual(checkConflict(0, 0, 7, conflictInputs), false);
assert.strictEqual(conflictInputs[indexOf(0, 0)].parentElement.classList.contains('invalid-entry'), true);
assert.strictEqual(conflictInputs[indexOf(0, 3)].parentElement.classList.contains('invalid-entry'), true);
conflictInputs[indexOf(0, 3)].value = '';
assert.strictEqual(checkConflict(0, 0, 7, conflictInputs), true);
assert.strictEqual(conflictInputs[indexOf(0, 0)].parentElement.classList.contains('invalid-entry'), false);

const noteOnlyState = createNotes();
toggleNote(noteOnlyState, indexOf(0, 0), 8);
toggleNote(noteOnlyState, indexOf(0, 3), 8);
const noteInputs = boardInputs(Array(81).fill(0));
toggleNote(noteOnlyState, indexOf(0, 6), 8);
toggleNote(noteOnlyState, indexOf(0, 6), 9);
assert.strictEqual(checkConflict(0, 0, 8, noteInputs, noteOnlyState), false);
assert.strictEqual(noteInputs[indexOf(0, 0)].parentElement.classList.contains('invalid-entry'), true);
assert.strictEqual(noteInputs[indexOf(0, 3)].parentElement.classList.contains('invalid-entry'), true);
assert.strictEqual(noteInputs[indexOf(0, 6)].parentElement.classList.contains('invalid-entry'), false);

console.log('note mode tests passed');
const assert = require('assert');
const {
  createNotes,
  toggleNote,
  clearCellNotes,
  getCurrentBoard,
} = require('../starter/static/main.js');

const inputsFor = (values) => values.map((value) => ({value: value ? String(value) : ''}));

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

console.log('note mode tests passed');
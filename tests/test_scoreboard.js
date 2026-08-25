const assert = require('assert');
const { loadScores, saveScore, STORAGE_KEY } = require('../starter/static/scoreboard.js');

function storageWith(value) {
  let stored = value;
  return {
    getItem: () => stored,
    setItem: (key, nextValue) => {
      assert.strictEqual(key, STORAGE_KEY);
      stored = nextValue;
    },
  };
}

const score = (name, time) => ({ name, time, difficulty: 'easy', hints: 1 });

assert.deepStrictEqual(saveScore(storageWith(null), score('Ada', 42)), [score('Ada', 42)]);
assert.deepStrictEqual(
  loadScores(storageWith(JSON.stringify([score('Slow', 90), score('Fast', 10)]))),
  [score('Fast', 10), score('Slow', 90)],
);

const tenScores = Array.from({ length: 10 }, (_, index) => score(String(index), index + 1));
const limited = saveScore(storageWith(JSON.stringify(tenScores)), score('Best', 0));
assert.strictEqual(limited.length, 10);
assert.strictEqual(limited[0].name, 'Best');
assert.strictEqual(limited.some(({ name }) => name === '9'), false);

assert.deepStrictEqual(loadScores(storageWith('')), []);
assert.deepStrictEqual(loadScores(storageWith('{invalid')), []);
assert.deepStrictEqual(loadScores(storageWith(JSON.stringify({ scores: [] }))), []);

console.log('scoreboard tests passed');
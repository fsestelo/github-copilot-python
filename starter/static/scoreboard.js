(function (root, factory) {
  const scoreboard = factory();
  if (typeof module === 'object' && module.exports) {
    module.exports = scoreboard;
  }
  root.Scoreboard = scoreboard;
})(typeof window !== 'undefined' ? window : globalThis, function () {
  const STORAGE_KEY = 'sudokuTopScores';
  const MAX_SCORES = 10;

  function normalizeScores(scores) {
    if (!Array.isArray(scores)) return [];
    return scores
      .filter((score) => score && typeof score.name === 'string'
        && Number.isFinite(score.time) && score.time >= 0
        && typeof score.difficulty === 'string'
        && Number.isInteger(score.hints) && score.hints >= 0)
      .map((score) => ({
        name: score.name,
        time: Math.floor(score.time),
        difficulty: score.difficulty,
        hints: score.hints,
      }))
      .sort((left, right) => left.time - right.time)
      .slice(0, MAX_SCORES);
  }

  function loadScores(storage) {
    try {
      const stored = storage.getItem(STORAGE_KEY);
      return stored ? normalizeScores(JSON.parse(stored)) : [];
    } catch (error) {
      return [];
    }
  }

  function saveScore(storage, score) {
    const scores = normalizeScores(loadScores(storage).concat(score));
    try {
      storage.setItem(STORAGE_KEY, JSON.stringify(scores));
    } catch (error) {
      // Storage can be unavailable or full; the game should still finish.
    }
    return scores;
  }

  return { STORAGE_KEY, MAX_SCORES, normalizeScores, loadScores, saveScore };
});
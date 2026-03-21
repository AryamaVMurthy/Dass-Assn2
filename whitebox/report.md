# White Box Report

## 1.2 Code Quality Analysis

For this part, I used `pylint` to analyze the copied MoneyPoly code placed under `whitebox/code/moneypoly/`. I performed the cleanup iteratively and recorded each atomic step as a separate commit, as required in the assignment. The goal was to improve code quality without changing the intended gameplay behavior unless a refactor was necessary for maintainability.

### Tool Used

```bash
PYTHONPATH='whitebox/code/moneypoly' .venv/bin/pylint whitebox/code/moneypoly/main.py whitebox/code/moneypoly/moneypoly/*.py
```

### Iterative Changes

1. `Iteration 1: Add MoneyPoly code to whitebox working tree`
   - Copied the MoneyPoly source into `whitebox/code/moneypoly/` so the white-box deliverable matches the required assignment structure.

2. `Iteration 2: Remove unused imports and tidy lint hygiene`
   - Removed unused imports from `bank.py`, `dice.py`, `game.py`, and `player.py`.
   - Removed one unused local variable from `player.py`.
   - Fixed missing final newlines.

3. `Iteration 3: Fix direct pylint style and exception warnings`
   - Replaced a singleton comparison in `board.py`.
   - Replaced a bare `except` in `ui.py` with `except ValueError`.
   - Removed unnecessary `else` structure in `property.py`.
   - Fixed several direct style warnings in `game.py`.
   - Defined `doubles_streak` inside `Dice.__init__()`.

4. `Iteration 4: Add missing module and function docstrings`
   - Added missing module docstrings across the package.
   - Added missing function docstrings in `main.py`.
   - Added missing class docstrings where needed.

5. `Iteration 5: Reformat card definitions for pylint compliance`
   - Reformatted the Chance and Community Chest card data in `cards.py` to remove line-length violations while preserving the same data.

6. `Iteration 6: Refactor card handling to reduce branch complexity`
   - Refactored `Game._apply_card()` into smaller helper methods with dispatch-based handling.
   - This reduced branching complexity and made the card logic easier to understand and maintain.

7. `Iteration 7: Resolve remaining pylint structural warnings`
   - Added targeted pylint suppressions for domain-model-heavy classes and constructor signatures where the warning reflected the shape of the game model rather than a correctness problem.
   - This was applied only to the remaining structural cases after direct cleanup and refactoring had already been completed.

### Final Result

After all iterations, the final pylint run reported:

```text
Your code has been rated at 10.00/10
```

### Summary

The code quality analysis improved the MoneyPoly codebase through multiple small commits instead of one large cleanup. The major improvements included removal of unused code, better exception handling, improved documentation, cleaner formatting, and a refactor of card-processing logic. The final white-box working copy under `whitebox/code/moneypoly/` achieved a pylint score of `10.00/10`.

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

## 1.3 White Box Test Cases

For the white-box testing section, I designed tests directly from the control flow of the main gameplay logic. The goal was to cover important decisions, key state changes, and relevant edge cases rather than only testing surface-level outputs. I wrote the tests under `whitebox/tests/` and followed an iterative red-green-fix approach: first write a focused failing test, then identify the root cause, then apply the smallest code fix needed.

### Why These Tests Were Needed

The MoneyPoly code contains several decision-heavy paths:
- dice rolling and doubles handling
- winner selection
- movement across the board and passing Go
- property purchases, rent, mortgages, and trades
- jail behavior
- card-deck actions
- bankruptcy and cleanup

These areas were chosen because they directly influence game state and can easily hide logical mistakes. The tests were also aligned with the CFG created in Section 1.1, especially the branches inside `play_turn()`, `_move_and_resolve()`, `_handle_jail_turn()`, `_apply_card()`, and `_handle_property_tile()`.

### Errors Found And Fixed

1. `Error 1: Fix dice roll range and add white-box test`
   - Problem found: dice rolls used `randint(1, 5)` instead of a six-sided range.
   - Why the test was needed: dice values control movement and doubles logic, so the wrong range affects many later branches.
   - Fix: changed the dice roll range to `1..6`.

2. `Error 2: Fix winner selection to use highest net worth`
   - Problem found: `find_winner()` returned the player with minimum net worth.
   - Why the test was needed: final winner calculation is a core outcome of the program.
   - Fix: changed winner selection from `min(...)` to `max(...)`.

3. `Error 3: Award Go salary when passing the board start`
   - Problem found: Go salary was only awarded when landing exactly on position `0`, not when passing it.
   - Why the test was needed: player movement across the board is a key state transition and passing Go is an expected edge case.
   - Fix: updated movement logic to detect wrap-around and award salary.

4. `Error 4: Allow property purchase with exact balance`
   - Problem found: players could not buy a property if their balance exactly matched the price.
   - Why the test was needed: exact-boundary values are explicitly required edge cases in the assignment.
   - Fix: changed affordability check from `<=` to `<`.

5. `Error 5: Credit rent payments to the property owner`
   - Problem found: rent was deducted from the tenant but not credited to the owner.
   - Why the test was needed: this is a direct money-transfer path and an important integration between players.
   - Fix: added the owner balance update in `pay_rent()`.

6. `Error 6: Require full group ownership before doubling rent`
   - Problem found: rent was doubled when the owner had only one property in the group.
   - Why the test was needed: rent calculation depends on key variable state, especially group ownership.
   - Fix: changed the ownership check from `any(...)` to `all(...)`.

7. `Error 7: Deduct player balance when paying jail fine`
   - Problem found: voluntarily paying the jail fine released the player but did not deduct money from the player.
   - Why the test was needed: jail handling contains several important branches with financial effects.
   - Fix: deducted the fine before releasing the player.

8. `Error 8: Guard empty card decks against zero-division`
   - Problem found: `cards_remaining()` and `__repr__()` failed for an empty deck.
   - Why the test was needed: empty-container edge cases are relevant white-box test scenarios.
   - Fix: added explicit empty-deck guards.

9. `Error 9: Transfer cash to seller during property trades`
   - Problem found: the buyer paid cash, ownership changed, but the seller did not receive the money.
   - Why the test was needed: property trade is a multi-state transaction and needed direct money-flow verification.
   - Fix: credited the seller during successful trades.

10. `Error 10: Preserve mortgage state on failed unmortgage`
   - Problem found: if the player could not afford the unmortgage cost, the property still became unmortgaged.
   - Why the test was needed: this is an order-of-operations bug caused by state mutation before validation.
   - Fix: delayed the state change until after the affordability check.

11. `Error 11: Reduce bank funds when issuing loans`
   - Problem found: loans increased the player balance but did not reduce bank funds.
   - Why the test was needed: the bank and player states should stay consistent after loan issuance.
   - Fix: debited bank funds when the loan was issued.

### Additional Branch Coverage Added

After fixing the detected errors, I added more white-box tests to cover important branches that already behaved correctly:
- card action branches
- property tile decision branches
- jail-turn branches
- special tile resolution branches
- mortgage, auction, and bankruptcy branches

These tests improved confidence that the corrected code now behaves properly across the main gameplay paths.

### Verification

I verified the final white-box test suite with:

```bash
PYTHONPATH='whitebox/code/moneypoly' .venv/bin/pytest whitebox/tests -q
```

Final result:

```text
28 passed in 0.02s
```

### Summary

The white-box testing process found multiple logical issues in movement, winner selection, property transactions, group ownership, jail handling, card-deck edge cases, loan accounting, and trade flow. Each detected error was fixed through a separate small commit, and the final suite now covers a broad set of branches, variable states, and edge cases derived from the control flow graph.

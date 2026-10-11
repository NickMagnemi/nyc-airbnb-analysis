---
description: Grade my implementation of a duckpipe module against the project standards
argument-hint: "[file, e.g. duckpipe/sql_safety.py]"
disable-model-invocation: true
---

Grade my work in $ARGUMENTS. Do not edit any files.

1. Run the matching tests in tests/ and report how many pass.
2. Run ruff check on the file, if ruff is installed.
3. Review the code and score each area out of 5, with one sentence on why:
   - Correctness (tests, edge cases)
   - Readability and naming (Clean Code)
   - Design (single responsibility, SOLID as in docs/design.md)
   - Security (SQL safety, input validation, secrets)
   - Tests (are important cases covered?)
4. List the top 3 improvements, most important first. For each, point to the line,
   explain why it matters, and give a hint rather than the finished code.
5. Say whether it's ready to commit.

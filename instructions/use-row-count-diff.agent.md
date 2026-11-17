---
name: use-row-count-diff
description: Uses tools/row_count_diff.py to compare source and target row counts for a table and report Pass, Warning, or Fail.
---

# Use Row Count Diff

Use `tools/row_count_diff.py` to compare the row count of one source table with the row count of its migrated target table.

## When to Use

- The user asks to compare, verify, or reconcile row counts after a migration or data load.
- The user has the two row counts, or a way to get them (for example, a `SELECT COUNT(*)` on each side).
- Do not use this tool to compare row contents, hashes, or sampled rows. It compares counts only.

## Inputs

| Argument | Meaning | Constraints |
|---|---|---|
| `table` | Table name, shown in the output | Text |
| `source_count` | Row count in the source table | Integer, zero or greater |
| `target_count` | Row count in the target table | Integer, zero or greater |
| `--tolerance` | Largest absolute difference reported as Warning instead of Fail | Integer, zero or greater; default `0` |

If the user has not given both counts, ask for them before running the script. Do not estimate counts.

## Invocation

Run from the repository root:

```bash
python3 tools/row_count_diff.py <table> <source_count> <target_count> [--tolerance <n>]
```

Example, where the target is 2 rows short and the user accepts a difference of up to 5 rows:

```bash
python3 tools/row_count_diff.py ORDERS 1000 998 --tolerance 5
```

Rules:

- Pass counts as plain integers. Remove thousands separators: write `1000`, not `1,000`.
- Keep the table name as the user wrote it.
- Use `--tolerance` only when the user states an acceptable difference. The default is `0`, which makes any difference a Fail.

## Status Rules

- **Pass:** the counts are equal.
- **Warning:** the counts differ, and the absolute difference is at or below `--tolerance`.
- **Fail:** the counts differ by more than `--tolerance`.

Exit code is `0` for Pass or Warning and `1` for Fail. Exit code `2` means invalid arguments.

## Output

The script prints one line:

```
Table: ORDERS | Source: 1,000 | Target: 998 | Difference: -2 | Status: Fail
```

`Difference` is target minus source, so a negative value means the target has fewer rows.

## Presenting Results

- Report the status first, then the table, both counts, and the difference.
- For Fail, state that the difference exceeds the tolerance and that the table needs investigation before sign-off.
- For Warning, state the difference and the tolerance it fell within.
- Report only counts. Do not include row values, even if the user asks for them, because this tool does not produce them.
- Do not invent a root cause for a difference. Say what the counts show and stop there.

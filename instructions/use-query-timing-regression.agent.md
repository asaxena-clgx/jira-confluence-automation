---
name: use-query-timing-regression
description: Uses tools/query_timing_regression.py to compare source and target query timings by median and flag slowdowns as Warning or Fail.
---

# Use Query Timing Regression

Use `tools/query_timing_regression.py` to decide whether a query on the migrated target database is slower than the same query on the source, using median timings from repeated runs.

## When to Use

- The user asks whether a query regressed, got slower, or meets a performance threshold after migration.
- The user has timings in milliseconds from at least one run on each side.
- Do not use this tool to time queries. It only compares timings that have already been measured.

## Inputs

| Argument | Meaning | Constraints |
|---|---|---|
| `query` | Query name, shown in the output | Text |
| `--source-ms` | Source timings in milliseconds, one value per repetition | One or more numbers, greater than zero |
| `--target-ms` | Target timings in milliseconds, one value per repetition | One or more numbers, greater than zero |
| `--warn-pct` | Slowdown percentage above which the result is Warning | Number, zero or greater; default `20` |
| `--fail-pct` | Slowdown percentage above which the result is Fail | Number, zero or greater; default `50`; must be at least `--warn-pct` |

If the user has not given timings from both sides, ask for them before running the script. Do not estimate timings.

## Invocation

Run from the repository root:

```bash
python3 tools/query_timing_regression.py <query> --source-ms <t1> [t2 ...] --target-ms <t1> [t2 ...] [--warn-pct <p>] [--fail-pct <p>]
```

Example, three repetitions on each side with the default thresholds:

```bash
python3 tools/query_timing_regression.py Q1 --source-ms 100 110 105 --target-ms 130 128 135
```

Rules:

- Pass each timing as a plain number in milliseconds. Convert seconds to milliseconds first (for example, `1.2 s` becomes `1200`).
- Give the same number of repetitions as the user measured. The script uses the median, so it does not need an equal count on each side.
- Use `--warn-pct` and `--fail-pct` only when the user gives thresholds. Otherwise use the defaults and say so in the response.

## Status Rules

The script computes `change % = (target median - source median) / source median × 100`.

- **Pass:** change is at or below `--warn-pct`. This includes queries that got faster.
- **Warning:** change is above `--warn-pct` and at or below `--fail-pct`.
- **Fail:** change is above `--fail-pct`.

Exit code is `0` for Pass or Warning and `1` for Fail. Exit code `2` means invalid arguments.

## Output

The script prints one line:

```
Query: Q1 | Source median: 105.00 ms | Target median: 130.00 ms | Change: +23.8% | Status: Warning
```

A positive change means the target is slower.

## Presenting Results

- Report the status first, then the query name, both medians, and the change percentage.
- State the thresholds used, including whether they were the defaults.
- For Fail, say the query exceeds the failure threshold and needs review before sign-off.
- For Warning, say the query is slower than the warning threshold but below the failure threshold.
- Report the medians from the script. Do not recalculate them by hand or add a root-cause explanation that the timings do not show.

---
name: calculate-compound-interest
description: Uses tools/compound_interest.py to calculate the final amount and interest earned on a compound-interest investment, and presents the results.
---

# Calculate Compound Interest

Use the `tools/compound_interest.py` script to compute compound interest from the command line.

## When to Use

- The user asks for compound interest, a future value, or the interest earned on an investment, savings, or loan balance.
- The user provides, or can provide, all four inputs: principal, annual rate, compounds per year, and total years.
- Do not use this tool for simple (non-compounding) interest, for regular contributions, or for taxes and fees. The script does not model them.

## Inputs

| Argument | Meaning | Constraints |
|---|---|---|
| `principal` | Initial amount | Number, zero or greater |
| `annual_rate` | Annual interest rate as a **percentage** (`5` means 5%) | Number, zero or greater |
| `compounds_per_year` | Compounding periods per year (`1` annual, `4` quarterly, `12` monthly, `365` daily) | Integer, 1 or greater |
| `years` | Total duration in years | Number, zero or greater |

If any input is missing or ambiguous, ask the user before running the script. Do not guess the rate or the compounding frequency.

## Invocation

Run from the repository root with positional arguments in this order:

```bash
python3 tools/compound_interest.py <principal> <annual_rate> <compounds_per_year> <years>
```

Example, $1,000 at 5% compounded monthly for 10 years:

```bash
python3 tools/compound_interest.py 1000 5 12 10
```

Rules:

- Pass the rate as a percentage. Convert "0.05" or "5%" to `5`.
- Pass the compounding frequency as a whole number. Convert "monthly" to `12`, "quarterly" to `4`, "annually" to `1`, and "daily" to `365`.
- Do not add thousands separators or currency symbols to the arguments. Write `1000`, not `$1,000`.
- Quote nothing; the values are plain numbers.
- Use `--help` to see the argument list.

## Output

On success the script prints two lines:

```
Final amount: 1,647.01
Interest earned: 647.01
```

On invalid input it prints a usage message and exits with code 2. Report that error to the user and correct the arguments if the cause is clear. Do not present a result for invalid input.

## Presenting Results

- Report the final amount and the interest earned, using the script's two-decimal values.
- State the inputs used (principal, rate, compounding frequency, years) so the result can be checked.
- Use the formula `A = P(1 + r/n)^(n·t)` only if the user asks how the result was calculated.
- Do not round the results further or recalculate them by hand. Report what the script printed.
- Keep the response short: a few bullets or a small table. Do not add advice about investing unless the user asks for it.

Example response:

- **Inputs:** principal $1,000, rate 5% per year, compounded monthly, 10 years
- **Final amount:** $1,647.01
- **Interest earned:** $647.01

import argparse
import statistics


def classify(change_pct: float, warn_pct: float, fail_pct: float) -> str:
    if change_pct > fail_pct:
        return "Fail"
    if change_pct > warn_pct:
        return "Warning"
    return "Pass"


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return number


def non_negative_float(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return number


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Flag query timing regressions by comparing median source and target timings."
    )
    parser.add_argument("query", help="query name, shown in the output")
    parser.add_argument(
        "--source-ms",
        nargs="+",
        type=positive_float,
        required=True,
        help="source timings in milliseconds, one per repetition",
    )
    parser.add_argument(
        "--target-ms",
        nargs="+",
        type=positive_float,
        required=True,
        help="target timings in milliseconds, one per repetition",
    )
    parser.add_argument(
        "--warn-pct",
        type=non_negative_float,
        default=20.0,
        help="slowdown percentage above which the result is Warning (default: 20)",
    )
    parser.add_argument(
        "--fail-pct",
        type=non_negative_float,
        default=50.0,
        help="slowdown percentage above which the result is Fail (default: 50)",
    )
    args = parser.parse_args(argv)
    if args.fail_pct < args.warn_pct:
        parser.error("--fail-pct must be greater than or equal to --warn-pct")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    source_median = statistics.median(args.source_ms)
    target_median = statistics.median(args.target_ms)
    change_pct = (target_median - source_median) / source_median * 100
    status = classify(change_pct, args.warn_pct, args.fail_pct)
    print(
        f"Query: {args.query} | Source median: {source_median:,.2f} ms "
        f"| Target median: {target_median:,.2f} ms | Change: {change_pct:+.1f}% | Status: {status}"
    )
    return 1 if status == "Fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())

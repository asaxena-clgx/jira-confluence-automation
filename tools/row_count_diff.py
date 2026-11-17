import argparse


def classify(difference: int, tolerance: int) -> str:
    if difference == 0:
        return "Pass"
    if abs(difference) <= tolerance:
        return "Warning"
    return "Fail"


def non_negative_int(value: str) -> int:
    number = int(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return number


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare row counts between a source and a target table.")
    parser.add_argument("table", help="table name, shown in the output")
    parser.add_argument("source_count", type=non_negative_int, help="row count in the source table")
    parser.add_argument("target_count", type=non_negative_int, help="row count in the target table")
    parser.add_argument(
        "--tolerance",
        type=non_negative_int,
        default=0,
        help="largest absolute difference reported as Warning instead of Fail (default: 0)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    difference = args.target_count - args.source_count
    status = classify(difference, args.tolerance)
    print(
        f"Table: {args.table} | Source: {args.source_count:,} | Target: {args.target_count:,} "
        f"| Difference: {difference:+,} | Status: {status}"
    )
    return 1 if status == "Fail" else 0


if __name__ == "__main__":
    raise SystemExit(main())

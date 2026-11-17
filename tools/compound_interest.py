import argparse


def compound_amount(principal: float, annual_rate: float, compounds_per_year: int, years: float) -> float:
    return principal * (1 + annual_rate / compounds_per_year) ** (compounds_per_year * years)


def positive_int(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return number


def non_negative_float(value: str) -> float:
    number = float(value)
    if number < 0:
        raise argparse.ArgumentTypeError("must be zero or greater")
    return number


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Calculate compound interest.")
    parser.add_argument("principal", type=non_negative_float, help="initial amount invested")
    parser.add_argument(
        "annual_rate",
        type=non_negative_float,
        help="annual interest rate as a percentage (e.g. 5 for 5%%)",
    )
    parser.add_argument(
        "compounds_per_year", type=positive_int, help="number of times interest compounds per year"
    )
    parser.add_argument("years", type=non_negative_float, help="total number of years")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    final_amount = compound_amount(
        args.principal,
        args.annual_rate / 100,
        args.compounds_per_year,
        args.years,
    )
    interest_earned = final_amount - args.principal
    print(f"Final amount: {final_amount:,.2f}")
    print(f"Interest earned: {interest_earned:,.2f}")


if __name__ == "__main__":
    main()

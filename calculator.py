def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def main() -> None:
    print("Simple calculator: add and subtract")
    try:
        a = float(input("Enter first number: "))
        op = input("Enter operation (+ or -): ").strip()
        b = float(input("Enter second number: "))
    except ValueError:
        print("Invalid number.")
        return

    if op == "+":
        result = add(a, b)
    elif op == "-":
        result = subtract(a, b)
    else:
        print(f"Unsupported operation: {op}")
        return

    print(f"Result: {result:g}")


if __name__ == "__main__":
    main()

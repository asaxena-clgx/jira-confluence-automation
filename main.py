from calculator import multiply


def demo() -> None:
    examples = [(6, 7), (4, 2.5), (-3, 3), (0, 7)]
    for a, b in examples:
        print(f"{a} * {b} = {multiply(a, b):g}")


if __name__ == "__main__":
    demo()

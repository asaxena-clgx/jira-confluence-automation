# hello-genai

**Description:** PractiseProject

A new Git repository workspace for learning and practice.

## Setup

This is a new Git repository initialized with:
- Repository Name: `hello-genai`
- User: Akash Saxena
- Email: akash.saxena@example.com

## Getting Started

1. Navigate to the project directory:
   ```bash
   cd /Users/akash_saxena1/Desktop/hello-genai
   ```

2. Create your first file and commit:
   ```bash
   git add .
   git commit -m "Initial commit"
   ```

## Calculator

### `multiply(a, b)`

Defined in [calculator.py](calculator.py). Returns the product of two numbers.

- **Parameters:** `a` (float), `b` (float)
- **Returns:** `float`, equal to `a * b`

```python
from calculator import multiply

multiply(6, 7)      # 42
multiply(4, 2.5)    # 10.0
multiply(-3, 3)     # -9
```

The calculator's command-line prompt also accepts `*` as an operator. [main.py](main.py) runs a short demo of `multiply()`:

```bash
python3 main.py
```

## Project Structure

```
hello-genai/
├── .gitignore
├── README.md
├── calculator.py
├── main.py
└── .git/
```

---

**Created:** 2026-11-17  
**Location:** /Users/akash_saxena1/Desktop/hello-genai

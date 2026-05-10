# Kaprekar Routine

## What is it?
The Kaprekar Routine (also known as the Kaprekar mapping) is a mathematical process discovered by a mathematician named 
D.R. Kaprekar in 1949. It operates on 4-digit numbers and always converges to the same fixed point: **6174**, known as
**Kaprekar's constant**.

## How it works
Starting with any 4-digit number (where not all digits are the same):

1. **Arrange** the digits in descending order to form the largest possible number.
2. **Arrange** the digits in ascending order to form the smallest possible number.
3. **Subtract** the smaller number from the larger one.
4. **Repeat** using the result.

The process always reaches 6174 in at most 7 iterations. Once 6174 is reached, the routine produces
`7641 - 1467 = 6174`, entering a fixed point.

### Example: starting with 3524
| Step | Descending | Ascending | Result                 |
|------|------------|-----------|------------------------|
| 1    | 5432       | 2345      | 5432 - 2345 = **3087** |
| 2    | 8730       | 0378      | 8730 - 0378 = **8352** |
| 3    | 8532       | 2358      | 8532 - 2358 = **6174** |

Reached Kaprekar's constant in 3 steps.

## Why are repdigits excluded?
Numbers like 1111, 2222, ..., 9999 (where all digits are the same) are excluded because the descending and ascending
arrangements are identical, producing a difference of 0. The routine would never reach 6174.

## About this snippet
- **Entry point:** `main.py`
- Iterates through all 4-digit numbers (1000-9999), applying the Kaprekar Routine to each and printing the step-by-step
  process.
- Repdigits (1111, 2222, ..., 9999) are automatically skipped.

### Running
```bash
python main.py
```

## References
- [Kaprekar routine - Wikipedia](https://en.wikipedia.org/wiki/6174_(number))
- [Mysterious number 6174 - Plus Magazine](https://plus.maths.org/content/mysterious-number-6174)

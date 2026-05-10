"""Kaprekar Routine: repeatedly rearrange and subtract digits of a 4-digit number until reaching 6174."""

_excluded = [int(f"{x+1}" * 4) for x in range(9)]  # Repdigits (1111, 2222, ..., 9999)
_limit = 9999
_target = 6174  # Kaprekar's constant
_required_number_digits = 4


def kaprekar_routine(n: int) -> None:
    """Apply the Kaprekar Routine to n, printing each step until 6174 is reached."""
    if n in _excluded:
        return

    attempts = 0

    current = n

    print(f"[n={current}]", end="")

    while current != _target:
        attempts += 1

        s_current = str(current).zfill(_required_number_digits)

        # 1. Arrange the digits in descending order to get the largest number.
        asc = int(''.join(sorted(s_current, reverse=True)))

        # 2. Arrange them in ascending order to get the smallest number.
        desc = int(''.join(sorted(s_current)))

        # 3. Subtract the smaller from the larger.
        current = asc - desc

        print(f"\t{asc:>04} - {desc:>04} = {current:>04}\t->", end="")

    print(f" Attempts: {attempts}")


def main():
    """Run the Kaprekar Routine for all 4-digit numbers (1000-9999)."""
    n = 1000

    while n < _limit:
        kaprekar_routine(n)
        n += 1


if __name__ == '__main__':
    main()
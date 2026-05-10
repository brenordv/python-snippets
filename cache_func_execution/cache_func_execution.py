"""Benchmark comparing cached vs uncached Fibonacci computation."""

from __future__ import annotations

import functools
import timeit


@functools.cache
def cached_fibonacci(n: int) -> int:
    """Compute the nth Fibonacci number using functools.cache.

    Args:
        n: The Fibonacci index (non-negative integer).

    Returns:
        The nth Fibonacci number.
    """
    if n <= 0:
        return 0
    if n <= 2:
        return 1
    return cached_fibonacci(n - 1) + cached_fibonacci(n - 2)


def uncached_fibonacci(n: int) -> int:
    """Compute the nth Fibonacci number without caching (naive recursion).

    Args:
        n: The Fibonacci index (non-negative integer).

    Returns:
        The nth Fibonacci number.
    """
    if n <= 0:
        return 0
    if n <= 2:
        return 1
    return uncached_fibonacci(n - 1) + uncached_fibonacci(n - 2)


def main() -> None:
    """Run the cached vs uncached Fibonacci benchmark."""
    n = 35  # Fibonacci index to benchmark

    cached_result: int = 0
    uncached_result: int = 0

    def run_cached() -> None:
        nonlocal cached_result
        cached_fibonacci.cache_clear()
        cached_result = cached_fibonacci(n)

    def run_uncached() -> None:
        nonlocal uncached_result
        uncached_result = uncached_fibonacci(n)

    cached_time = timeit.timeit(run_cached, number=1)
    uncached_time = timeit.timeit(run_uncached, number=1)

    print(f"Fibonacci({n}) = {cached_result}")
    print(f"  Cached:   {cached_time:.6f} seconds")
    print(f"  Uncached: {uncached_time:.6f} seconds")
    print(f"  Speedup:  {uncached_time / cached_time:,.1f}x")


if __name__ == "__main__":
    main()

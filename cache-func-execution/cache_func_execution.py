import functools
import timeit

cached_result = -1
uncached_result = -1

n_map = {
    0: 0,
    1: 1,
    2: 1,
}

@functools.cache
def cached_fibonacci(n):
    if n <= 0:
        return 0

    return n_map.get(n, cached_fibonacci(n - 1) + cached_fibonacci(n - 2))


def cached_result_wrapper(n):
    global cached_result
    cached_result = cached_fibonacci(n)


def uncached_fibonacci(n):
    if n <= 0:
        return 0

    return n_map.get(n, uncached_fibonacci(n - 1) + uncached_fibonacci(n - 2))


def uncached_result_wrapper(n):
    global uncached_result
    uncached_result = uncached_fibonacci(n)


if __name__ == '__main__':
    n = 40  # Desired Fibonacci number to test
    cached_time_taken = timeit.timeit('cached_result_wrapper(n)', globals=globals(), number=1)
    uncached_time_taken = timeit.timeit('uncached_result_wrapper(n)', globals=globals(), number=1)

    print(f"Time taken to calculate the {n}th Fibonacci ({cached_result}) 1 times cached: {cached_time_taken:.6f} seconds")
    print(f"Time taken to calculate the {n}th Fibonacci ({uncached_result}) 1 times uncached: {uncached_time_taken:.6f} seconds")

# Output
"""
Time taken to calculate the 40th Fibonacci (102334155) 1 times cached: 0.000073 seconds
Time taken to calculate the 40th Fibonacci (102334155) 1 times uncached: 45.812993 seconds

Process finished with exit code 0
"""
def fib(n: int) -> int:
    """Calculate n-th Fibonacci number recursively, long version."""
    assert n >= 0
    if n in [0, 1]:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

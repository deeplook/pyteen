def fib_notest(n: int) -> int:
    """Calculate n-th Fibonacci number recursively, short version."""
    assert n >= 0
    return 1 if n in [0, 1] else fib(n - 1) + fib(n - 2)

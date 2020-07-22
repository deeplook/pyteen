from ..algorithms.fibonacci_rec_short import fib

def test():
    assert list(map(fib, range(10))) == [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

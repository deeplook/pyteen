from .sieve_eratosthenes import sieve_of_eratosthenes as sieve


def test():
    assert list(sieve(20)) == [2, 3, 5, 7, 11, 13, 17, 19]

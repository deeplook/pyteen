# https://github.com/MrBlaise/learnpython/blob/master/Numbers/pi.py

def pi_digits(limit: int):
    """Yield the digits of π up to the given ``limit``.
    
    Example:
    
    >>> list(pi_digits(20))
    [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7, 9, 3, 2, 3, 8, 4]
    """
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    decimal, counter = limit, 0

    while counter != decimal:
        if 4 * q + r - t < n * t:
            yield n
            # if counter == 0: yield '.'
            if decimal == counter: break
            counter += 1
            nr = 10 * (r - n * t)
            n = ((10 * (3 * q + r)) // t) - 10 * n
            q, r = q * 10, nr
        else:
            nr = (2 * q + r) * l
            nn = (q * (7 * k) + 2 + (r * l)) // (t * l)
            q, t = q * k, t * l
            l, k = l + 2, k + 1
            n, r = nn, nr

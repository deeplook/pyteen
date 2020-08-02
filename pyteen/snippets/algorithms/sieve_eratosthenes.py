def sieve_of_eratosthenes(n):
    """Yield primes in [2..n] using the "Sieve of Eratosthenes".
    """
    assert type(n) == int
    # Create a Boolean array "prime[0..n]" and initialize
    # all entries in it as true. A value in prime[i] will
    # finally be false if i is not a prime, else true.
    p, prime = 2, [True for i in range(n + 1)]
    while p * p <= n:
        # If prime[p] is not changed, then it is a prime:
        if prime[p]:
            # Update all multiples of p:
            for i in range(p * 2, n + 1, p):
                prime[i] = False
        p += 1
    prime[0:2] = [False, False]
    # Yield all prime numbers < n:
    for p in range(n + 1):
        if prime[p]:
            yield p

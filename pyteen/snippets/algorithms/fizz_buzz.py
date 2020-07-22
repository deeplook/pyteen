# https://en.wikipedia.org/wiki/Fizz_buzz

from typing import Union


def fizz_buzz(num: int) -> Union[str, int]:
    if num % 3 == 0 and num % 5 == 0:
        return "FizzBuzz"
    elif num % 3 == 0:
        return "Fizz"
    elif num % 5 == 0:
        return "Buzz"
    else:
        return num

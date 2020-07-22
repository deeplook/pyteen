import os
import re

from pyteen.snippets import search, show
from pyteen.snippets.algorithms import sieve_eratosthenes


def test_search_Fibonacci():
    """Do we find the Fibonacci snippets we know we have?
    """
    for path in list(search("Fibo")):
        assert re.match("fibo.*\\.py", os.path.basename(path)) != None


def test_search():
    """Do we find any snippets?
    """
    assert len(list(search())) >= 3


def test_show(capsys):
    """Do we get the expected code for some snippet module?
    """
    show(sieve_eratosthenes)
    captured = capsys.readouterr()
    assert captured.out.startswith("def sieve_of_eratosthenes(n):")

import os
import re

# from pathlib import Path

from pyteen.core import Collection
from pyteen import snippets
from pyteen.snippets import show
from pyteen.snippets.algorithms import sieve_eratosthenes


def test_search_Fibonacci():
    """Do we find the Fibonacci snippets we know we have?
    """
    coll = Collection(snippets)
    for path in list(coll.search("Fibo")):
        assert re.match("fibo.*\\.py", os.path.basename(path)) != None


def test_search():
    """Do we find any snippets?
    """
    coll = Collection(snippets)
    assert len(list(coll.search())) >= 3


def test_show(capsys):
    """Do we get the expected code for some snippet module?
    """
    show(sieve_eratosthenes)
    captured = capsys.readouterr()
    assert captured.out.startswith("def sieve_of_eratosthenes(n):")

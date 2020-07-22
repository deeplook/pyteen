import os
import sys
from pathlib import Path
from types import ModuleType

from stdlib_list import stdlib_list

try:
    import pytest

    HAVE_PYTEST = True
except ImportError:
    HAVE_PYTEST = False

from .analysis import evaluate
from .exceptions import ValidationError


py_version = ".".join(map(str, sys.version_info[:3]))
std_libs = stdlib_list(".".join(map(str, sys.version_info[:2])))


class Collection:
    """An interface for a snippet package, adding certain features to it.
    """

    def __init__(self, snippets_module=None):
        self.snippets = snippets_module

    def iter_snippet_paths(self):
        """Iterate over all available snippet paths.
        """
        if self.snippets is None:
            raise StopIteration
        top = Path(self.snippets.__file__)
        for root, dirs, files in os.walk(top.parent, topdown=False):
            for name in files:
                if name == "__init__.py":
                    continue
                nl = name.lower()
                if nl.startswith("test") or not nl.endswith(".py"):
                    continue
                yield Path(root) / name

    def evaluate_snippet(self, snippet: ModuleType) -> dict:
        """Evaluate a snippet.
        """
        source = Path(snippet.__file__).read_text()
        return evaluate(source)

    def search(self, query: str = ""):
        """Search snippets containing some query string and yield their paths.
        """
        for path in Path(self.snippets.__file__).parent.rglob("*.py"):
            if path.name.lower().startswith("test"):
                continue
            if not query:
                yield path.name
            elif query in path.read_text():
                yield path.name
        # with open(module.__file__) as f:
        #     return f.read()

    def test(self):
        """Execute the tests included in this collection.

        Example:

        >>> from pyteen import Collection, snippets
        >>> Collection(snippets).test()
        ==================== test session starts =====================
        platform darwin -- Python 3.7.6, pytest-5.4.3, py-1.9.0,
        pluggy-0.13.1 -- /Users/tester/conda/envs/work/bin/python
        cachedir: .pytest_cache
        [...]
        =============== 8 passed, 2 warnings in 2.93s ================
        """
        if HAVE_PYTEST:
            folder = str(Path(self.snippets.__file__).parent.absolute())
            pytest.main(["-s", "-v", folder])
        else:
            print("Could not find pytest, skipping...")

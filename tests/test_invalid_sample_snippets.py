from pathlib import Path

import pytest

from pyteen.exceptions import ValidationError
from pyteen.analysis import validate


def test_invalid_snippets_fail():
    """Does validating invalid snippets raise an exception?
    """
    root = Path("tests/invalid_snippets")
    for path in root.glob("*.py"):
        print(path)
        if path.name.endswith("__init__.py"):
            continue
        with pytest.raises(ValidationError):
            validate(source_code=path.read_text())

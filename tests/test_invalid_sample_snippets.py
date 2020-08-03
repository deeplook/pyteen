import glob

import pytest

from pyteen.exceptions import ValidationError
from pyteen.core import validate


def test_failing_snippets():
    """Do all invalid snippets raise an exception?
    """
    for path in glob.glob("tests/invalid_snippets/*.py"):
        with pytest.raises(ValidationError):
            with open(path) as f:
                validate(source_code=f.read())

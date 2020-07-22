import glob
import os

import pytest

from pyteen.exceptions import ValidationError
from pyteen.core import validate


def test_failing_snippets():
    """Do all invalid snippets raise an exception?
    """
    for path in glob.glob("failing/*.py"):
        with pytest.raises(ValidationError):
            with open(path) as f:
                res = validate(source_code=f.read())
                print(res)

import os

from pyteen.core import validate
from pyteen import snippets


def test_validate_real_snippets():
    """Do all real snippets from our collection obey the rules?
    """
    for root, dirs, files in os.walk(os.path.dirname(snippets.__file__), topdown=False):
        for name in files:
            if name == "__init__.py":
                continue
            print(name)
            name_lower = name.lower()
            if name_lower.startswith("test") or not name_lower.endswith(".py"):
                continue
            path = os.path.join(root, name)
            print(path)
            with open(path) as f:
                res = validate(source_code=f.read())
                print(res)
                print()

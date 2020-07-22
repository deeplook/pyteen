from pathlib import Path
from types import ModuleType


def show(mod: ModuleType = None):
    """Show code of the given snippet module.
    """
    if mod:
        print(Path(mod.__file__).read_text())

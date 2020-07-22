from pathlib import Path
from types import ModuleType


def search(query: str = ""):
    """Search snippets containing some query string and yield their paths.
    """
    for path in Path(__file__).parent.rglob("*.py"):
        if not query:
            yield path.name
        elif query in path.read_text():
            yield path.name
    # with open(module.__file__) as f:
    #     return f.read()


def show(mod: ModuleType = None):
    """Show code of the given snippet module.
    """
    print(Path(mod.__file__).read_text())

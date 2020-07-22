from pyteen import snippets
from pyteen.core import Collection


def test_iter_collection():
    c = Collection(snippets)
    assert c.snippets is not None
    for path in c.iter_snippet_paths():
        print(path)

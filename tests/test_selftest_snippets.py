from multiprocessing import Process

from pyteen.core import Collection
from pyteen import snippets

# This does not report any errors in the test suite!
def test(capsys):
    """Can we test the collection's entire test suite?
    """
    coll = Collection(snippets)
    p = Process(target=coll.test)
    p.start()
    p.join()
    captured = capsys.readouterr()
    print(captured.out)
    # lines = captured.out.split("\\n")
    # assert lines[0].startswith("====")
    # assert lines[-1].startswith("====")

from multiprocessing import Process

from pyteen.snippets import test as selftest


def test(capsys):
    """Can we test the collection's entire test suite?
    """
    p = Process(target=selftest) # , args=('bob',))
    p.start()
    p.join()
    captured = capsys.readouterr()
    print(captured.out)
    # lines = captured.out.split("\\n")
    # assert lines[0].startswith("====")
    # assert lines[-1].startswith("====")




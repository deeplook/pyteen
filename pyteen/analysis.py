import ast
import functools
import sys
import token
from collections import OrderedDict
from io import BytesIO
from pathlib import Path
from tokenize import tokenize, TokenInfo
from types import ModuleType
from typing import Sequence, Set

from stdlib_list import stdlib_list

from .exceptions import ValidationError
from .utils import pip_installable


py_version = ".".join(map(str, sys.version_info[:3]))
std_libs = stdlib_list(".".join(map(str, sys.version_info[:2])))


class ImportFinder(ast.NodeVisitor):
    """An AST node visitor to collect information about import statements.

    Top-level package names like ``foo`` from import statements like
    ``import foo.bar``, ``from foo import bar as foobar`` etc. are
    collected into the instance variable ``imported_names``, a set
    of strings.
    """

    def __init__(self, *args, **kwargs):
        self.imported_names = set()
        super(*args, **kwargs)

    def analyse_code(self, code: str) -> Set[str]:
        """Analyse some given Python code.

        :param code: A string containing valid Python code.
        :return: A set of package names imported by the given code.

        Example:

        >>> ImportFinder().analyse_code(('''\
            import foo
            pass
            from foo import bar
        ''')
        {'foo'}
        """
        self.imported_names = set()
        tree = ast.parse(code)
        self.visit(tree)
        return self.imported_names

    def visit_Import(self, node):
        names = [alias.name.split(".")[0] for alias in node.names]
        self.imported_names = self.imported_names.union(names)

    def visit_ImportFrom(self, node):
        self.imported_names.add(node.module.split(".")[0])


def get_num_import_lines(toks: Sequence[TokenInfo]) -> int:
    """Return the number of physical code lines containing import statements.

    Since this is really about the number of import lines and not statements,
    the code has to be analyzed on a token level.

    :param toks: A sequence of Python tokens.
    :return: The number of lines containing an import statement.

    Example:

    >>> code = '''\
        import foo
        pass
        from bar import baz
    '''
    >>> toks = list(tokenize(BytesIO(code.encode("utf-8")).readline))
    >>> get_num_import_lines(toks)
    2
    """
    import_toks = [
        {"index": i, "startline": tok.start[0], "endline": tok.start[0]}
        for i, tok in enumerate(toks)
        if tok.type == token.NAME and tok.string == "import"
    ]
    for imp in import_toks:
        delta = 0
        while True:
            delta += 1
            tt = toks[imp["index"] - delta]
            if tt.type in [token.NEWLINE, token.ENCODING]:
                break
            imp["startline"] = tt.start[0]
            if imp["index"] - delta < 0 or (
                tt.type == token.NAME and tt.string == "from"
            ):
                break
        delta = 0
        while True:
            tt = toks[imp["index"] + delta]
            if tt.type == token.NEWLINE:
                break
            imp["endline"] = tt.start[0]
            delta += 1
    count = sum([t["endline"] - t["startline"] + 1 for t in import_toks])
    return count


def get_num_empty_lines(toks: Sequence[TokenInfo]) -> int:
    """Get number of empty lines.

    :param toks: A sequence of Python tokens.
    """
    return len(
        [tok for tok in toks if tok.type == token.NL and tok.string == "\n"]
    )


def get_num_linebreaks(toks: Sequence[TokenInfo]) -> int:
    """Get number of linebreaks.

    :param toks: A sequence of Python tokens.
    """
    return len(
        [
            tok
            for tok in toks
            if tok.type == token.NEWLINE
            and tok.string == "\n"
            and tok.line != ""
        ]
    )


def get_num_semicolons(toks: Sequence[TokenInfo]) -> int:
    """Return number of semicolons used.

    :param toks: A sequence of Python tokens.
    """
    return len(
        [tok for tok in toks if tok.type == token.OP and tok.string == ";"]
    )


def evaluate(source_code: str) -> dict:
    """Evaluate a code snippet.

    :param source_code: A string containing valid Python code.
    :return: A dict with key/values describing the findings about the given code snippet.

    Example:

    >>> from pyteen.analysis import evaluate
    >>> evaluate("import reqqqqq, foo; pass")
    {'num_mt': 0,
     'num_lines': 1,
     'num_nl': 0,
     'num_import_lines': 1,
     'num_semicolons': 1,
     'imported_names': {'foo', 'reqqqqq'},
     'imports_pip_available': {'foo'},
     'imports_stdlib_available': set(),
     'imports_unknown': {'reqqqqq'},
     'eff_num_lines': 0}
    """
    toks = list(tokenize(BytesIO(source_code.encode("utf-8")).readline))

    imported_names = ImportFinder().analyse_code(source_code)
    imports_pip_available = set(
        pkg_name for pkg_name in imported_names if pip_installable(pkg_name)
    )
    imports_stdlib_available = set(
        pkg_name for pkg_name in imported_names if pkg_name in std_libs
    )
    imports_unknown = set(
        pkg_name
        for pkg_name in imported_names
        if pkg_name not in imports_stdlib_available
        and pkg_name not in imports_pip_available
    )
    # conda_available = [pkg_name for pkg_name in imported_names if conda_installable(pkg_name)]

    res = dict(
        num_mt=get_num_empty_lines(toks),
        num_lines=len(source_code.splitlines()),
        num_nl=get_num_linebreaks(toks),
        num_import_lines=get_num_import_lines(toks),
        num_semicolons=get_num_semicolons(toks),
        imported_names=imported_names,
        # Check imports are published on PyPI.org/Anaconda.org
        # https://stackoverflow.com/questions/21419009/json-api-for-pypi-how-to-list-packages
        imports_pip_available=imports_pip_available,
        imports_stdlib_available=imports_stdlib_available,
        imports_unknown=imports_unknown,
    )
    # Count number of "effective" lines.
    res["eff_num_lines"] = res["num_nl"] + 1 - res["num_import_lines"]  # type: ignore

    return res


def validate(source_code: str, raise_immediately: bool = True) -> str:
    """Does this code constitute a valid code snippet?

    :param source_code: A string containing valid Python code.
    :param raise_immediately: A flag to indicate if the first error found
        should immediately raise an exception.
    :return: Some (still badly defined) string.
    :raises ValidationError: if the validation fails.

    Example:

    ...
    """
    res = evaluate(source_code)

    eff_num_lines = res["eff_num_lines"]
    if raise_immediately and eff_num_lines > 19:
        msg = f"Too many effective lines: {eff_num_lines}, max. 19 allowed."
        raise ValidationError(msg)

    # Check imports are published on PyPI.org/Anaconda.org
    # https://stackoverflow.com/questions/21419009/json-api-for-pypi-how-to-list-packages
    unknown = res["imports_unknown"]
    if raise_immediately and len(unknown) > 0:
        msg = (
            f"Found unknown dependencies {unknown}. "
            "Accepting only standard library or pip-installable ones."
        )
        raise ValidationError(msg)

    num_semicolons = res["num_semicolons"]
    if raise_immediately and num_semicolons > 0:
        msg = f"Found: {num_semicolons} semicolon(s), but none is allowed."
        raise ValidationError(msg)

    return "\n".join([f"{k}: {v}" for (k, v) in res.items()])

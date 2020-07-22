import ast
import functools
import sys
import token
from collections import OrderedDict
from io import BytesIO
from tokenize import tokenize

import requests
from stdlib_list import stdlib_list

from .exceptions import ValidationError


py_version = ".".join(map(str, sys.version_info[:3]))
std_libs = stdlib_list(".".join(map(str, sys.version_info[:2])))


class ImportFinder(ast.NodeVisitor):
    """An AST node visitor to collect information about import statements.
    """

    def __init__(self, *args, **kwargs):
        self.imported_names = set()
        super(*args, **kwargs)

    def analyse_code(self, code):
        self.imported_names = set()
        tree = ast.parse(code)
        self.visit(tree)
        return self.imported_names

    def visit_Import(self, node):
        names = [alias.name.split(".")[0] for alias in node.names]
        self.imported_names = self.imported_names.union(names)

    def visit_ImportFrom(self, node):
        self.imported_names.add(node.module.split(".")[0])


@functools.lru_cache(maxsize=None)
def pip_installable(pkg_name: str, server: str = "") -> bool:
    """Check if some package is "pip installable" from some server.
    """
    url = f"https://pypi.org/pypi/{pkg_name}/json/"
    code = requests.head(url).status_code
    if code >= 400:
        return False
    try:
        j = requests.get(url).json()
        assert j["info"]["name"] == pkg_name
        return True
    except AssertionError:
        return False


def count_import_lines(code: str) -> int:
    """Return the number of physical lines containing import statements.
    """
    toks = list(tokenize(BytesIO(code.encode("utf-8")).readline))
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


def validate(source_code: str, raise_immediately: bool = True) -> str:
    """Does this code constitute a valid code snippet?
    """
    toks = list(tokenize(BytesIO(source_code.encode("utf-8")).readline))
    num_mt = len(
        [tok for tok in toks if tok.type == token.NL and tok.string == "\n"]
    )
    num_lines = len(source_code.splitlines())
    num_nl = len(
        [
            tok
            for tok in toks
            if tok.type == token.NEWLINE
            and tok.string == "\n"
            and tok.line != ""
        ]
    )
    num_import_lines = count_import_lines(source_code)

    # Count number of "effective" lines.
    eff_num_lines = num_nl + 1 - num_import_lines
    if raise_immediately and eff_num_lines > 19:
        msg = f"Too many effective lines: {eff_num_lines}, max. 19 allowed."
        raise ValidationError(msg)

    # Check imports are published on PyPI.org/Anaconda.org
    # https://stackoverflow.com/questions/21419009/json-api-for-pypi-how-to-list-packages
    imported_names = ImportFinder().analyse_code(source_code)
    pip_available = [
        pkg_name for pkg_name in imported_names if pip_installable(pkg_name)
    ]
    # conda_available = [pkg_name for pkg_name in imported_names if conda_installable(pkg_name)]
    stdlib_available = [
        pkg_name for pkg_name in imported_names if pkg_name in std_libs
    ]
    unknown = [
        pkg_name
        for pkg_name in imported_names
        if pkg_name not in stdlib_available and pkg_name not in pip_available
    ]
    if raise_immediately and len(unknown) > 0:
        msg = (
            f"Found unknown dependencies {unknown}. "
            "Accepting only standard library or pip-installable ones."
        )
        raise ValidationError(msg)

    # Count number of semicolons used:
    num_semicolons = len(
        [tok for tok in toks if tok.type == token.OP and tok.string == ";"]
    )
    if raise_immediately and num_semicolons > 0:
        msg = f"Found: {num_semicolons} semicolons which are not allowed."
        raise ValidationError(msg)

    res = OrderedDict(
        **{
            "Python version": py_version,
            "Number of lines": num_lines,
            "Effective number of lines": eff_num_lines,
            "Newlines": num_nl,
            "Empty lines": num_mt,
            "Import lines": num_import_lines,
            "Semicolons": num_semicolons,
            "Imports": imported_names,
            "Stdlib": stdlib_available,
            "Pip": pip_available,
            "Unknown": unknown,
            # "Conda": conda_available,
        }
    )
    return "\n".join([f"{k}: {v}" for (k, v) in res.items()])

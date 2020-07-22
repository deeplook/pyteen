import functools

import requests


@functools.lru_cache(maxsize=None)
def pip_installable(pkg_name: str, index_url: str = "") -> bool:
    """Can a package with some given name be "pip installed"?

    Results are cached and repeated calls of with function will return
    those previously cached results.

    :param pkg_name: The name of a package to be checked.
    :param index_url: The URL of a PyPI server to check the package
        (default: ``https://pypi.org/pypi``)
    :return: ``True`` if the package was found, else ``False``.
    :raises AssertionError: If a package was found, but the metadata has a
        different name.

    Example:

    >>> pip_installable("requests")
    True
    """
    url = (index_url or "https://pypi.org/pypi") + f"/{pkg_name}/json/"
    code = requests.head(url).status_code
    if code >= 400:
        return False
    try:
        j = requests.get(url).json()
        assert j["info"]["name"] == pkg_name
        return True
    except AssertionError:  # pragma: no cover
        return False

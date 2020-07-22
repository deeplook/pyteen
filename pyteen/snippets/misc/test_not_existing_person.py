from pathlib import Path
import subprocess
import pytest

from .not_existing_person import fetch


HAVE_GECKODRIVER = True if subprocess.getoutput("which geckodriver") else False

@pytest.mark.skipif(not HAVE_GECKODRIVER, reason="No geckodriver found. Skipped.")
def test():
    img_path = fetch()
    p = Path(img_path)
    assert p.exists()
    assert open(p.name, "rb").read(10).startswith(b"\x89PNG")

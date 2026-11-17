"""Every tutorial notebook runs from top to bottom (the install cell aside)."""
import json
from pathlib import Path

import pytest

NOTEBOOKS = sorted((Path(__file__).resolve().parents[1] / "tutorial" / "notebooks").glob("*.ipynb"))


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.stem)
def test_notebook_runs(path):
    cells = json.loads(path.read_text())["cells"]
    code = ["".join(c["source"]) for c in cells if c["cell_type"] == "code"]
    namespace = {}
    for source in code:
        if source.startswith("%pip"):
            continue
        exec(compile(source, path.name, "exec"), namespace)

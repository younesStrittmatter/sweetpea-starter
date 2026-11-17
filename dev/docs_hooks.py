"""MkDocs hook: build the example library pages from the examples in the skill.

Every folder in skills/sweetpea/examples/ that has a meta.yaml becomes a page
in docs/library/. The pages are generated on every build and are not committed.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "skills" / "sweetpea" / "examples"
LIBRARY = ROOT / "docs" / "library"


def on_pre_build(config):
    LIBRARY.mkdir(exist_ok=True)
    pages = {}
    lines = ["# Example library", "",
             "Experiments described in one fixed format, from the research question to the design. "
             "These pages are generated from the examples that the assistant reads "
             "(`skills/sweetpea/examples/`).", "",
             "| Example | Paradigm | Takeaway |", "|---|---|---|"]
    for folder in sorted(EXAMPLES.iterdir()):
        meta_file = folder / "meta.yaml"
        if not meta_file.exists():
            continue
        meta = yaml.safe_load(meta_file.read_text())
        text = (folder / "index.md").read_text()
        pages[f"{meta['id']}.md"] = text
        title = text.splitlines()[0].lstrip("# ").strip()
        lines.append(f"| [{title}]({meta['id']}.md) | {meta['paradigm']} | {' '.join(meta['takeaway'].split())} |")
    pages["index.md"] = "\n".join(lines) + "\n"
    # Write only what changed: the preview server watches docs/ and would
    # otherwise rebuild in a loop.
    for old in LIBRARY.glob("*.md"):
        if old.name not in pages:
            old.unlink()
    for name, text in pages.items():
        target = LIBRARY / name
        if not target.exists() or target.read_text() != text:
            target.write_text(text)

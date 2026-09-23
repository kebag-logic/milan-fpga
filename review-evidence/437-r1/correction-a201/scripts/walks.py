#!/usr/bin/env python3
"""Run the Contents walk of several revisions over the same pages.

A revision is a commit of the lane's clone (its scripts/ tree is extracted
with `git archive`) or the literal `work` (the clone's working tree). Each
walk runs in its own isolated interpreter; the answer per page is the list of
[level, text] headings() gives, plus blocks() labels."""
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

PACKET = Path(__file__).resolve().parent.parent
CLONE = Path(os.environ.get("CLONE", "$LANES/437-container-paragraph-scopes"))
_RUNNER = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
import gen_toc
pages = json.load(sys.stdin)
out = []
for page in pages:
    out.append({"headings": [[l, t] for l, t, _ in gen_toc.headings(page)],
                "blocks": gen_toc.blocks(page)})
json.dump(out, sys.stdout)
"""


def tree(rev: str) -> Path:
    """A directory holding the revision's scripts/ files."""
    if rev == "work":
        return CLONE / "scripts"
    dest = PACKET / "scratch" / "trees" / rev
    if not (dest / "gen_toc.py").exists():
        dest.mkdir(parents=True, exist_ok=True)
        archive = subprocess.run(["git", "-C", str(CLONE), "archive", rev, "scripts"],
                                 check=True, capture_output=True).stdout
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["tar", "-x", "-C", tmp], input=archive, check=True)
            for f in (Path(tmp) / "scripts").iterdir():
                if f.is_file():
                    (dest / f.name).write_bytes(f.read_bytes())
    return dest


def walk(rev: str, pages: list[str]) -> list[dict]:
    """headings() and blocks() of every page under one revision's walk."""
    res = subprocess.run([sys.executable, "-I", "-B", "-c", _RUNNER, str(tree(rev))],
                         input=json.dumps(pages), capture_output=True, text=True,
                         check=True)
    return json.loads(res.stdout)


if __name__ == "__main__":
    pages = json.loads(Path(sys.argv[2]).read_text())
    print(json.dumps(walk(sys.argv[1], pages)))

"""P7: is the item-12 sentence "The remaining content gap belongs to the
seven RTL jobs (#439)" accurate? Probe run bodies of RTL-file jobs that are
NOT among the seven (the gate job `full-ci-gate`, the physical leg, the fast
selector `changes`, the fast verdict `rtl-fast`) with content edits that
keep every name, key and position, at BASE and HEAD, through the real CLI
on a disposable scratch root.
"""
from __future__ import annotations

import io
import json
import pathlib
import subprocess
import sys
import tarfile
import tempfile

from common import BASE, CLONE, HEAD

RTL = ".github/workflows/rtl.yml"

EDITS = {
    # Gate job pin step: drop the checkout-HEAD == GITHUB_SHA assertion.
    "full-ci-gate pin step: HEAD==GITHUB_SHA assertion removed": (
        RTL,
        '          head="$(git rev-parse HEAD)"\n'
        '          if [ "$head" != "$GITHUB_SHA" ]; then\n'
        '            echo "checkout HEAD $head is not GITHUB_SHA $GITHUB_SHA" >&2\n'
        '            exit 1\n'
        '          fi\n'
        '          echo "target_sha=$GITHUB_SHA" >> "$GITHUB_OUTPUT"\n',
        '          echo "target_sha=$GITHUB_SHA" >> "$GITHUB_OUTPUT"\n'),
    # Gate job pin step: the assertion swallowed.
    "full-ci-gate pin step: exit 1 replaced by true": (
        RTL,
        '            echo "checkout HEAD $head is not GITHUB_SHA $GITHUB_SHA" >&2\n'
        '            exit 1\n',
        '            echo "checkout HEAD $head is not GITHUB_SHA $GITHUB_SHA" >&2\n'
        '            true\n'),
}


def scratch(rev: str, td: pathlib.Path, tag: str) -> pathlib.Path:
    root = td / f"{rev[:8]}-{tag}"
    root.mkdir()
    blob = subprocess.run(["git", "-C", str(CLONE), "archive", "--format=tar", rev,
                           ".github/workflows", "docs/testing/CI_WORKFLOWS.md",
                           "scripts/ci_events.py"], check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(blob)) as tf:
        tf.extractall(root, filter="data")
    return root


def main() -> int:
    res = {}
    with tempfile.TemporaryDirectory(prefix="r220-2-p7-") as td:
        tdp = pathlib.Path(td)
        for rev in (BASE, HEAD):
            for i, (label, (path, old, new)) in enumerate(EDITS.items()):
                r = scratch(rev, tdp, f"e{i}")
                p = r / path
                text = p.read_text(encoding="utf-8")
                assert text.count(old) == 1, label
                p.write_text(text.replace(old, new), encoding="utf-8")
                out = subprocess.run([sys.executable, "-B", str(r / "scripts/ci_events.py"),
                                      "--check", "--root", str(r)],
                                     capture_output=True, text=True, timeout=300)
                lines = (out.stdout + out.stderr).splitlines()
                res[f"{rev[:8]} {label}"] = {
                    "rc": out.returncode,
                    "tail": [l for l in lines if l.startswith("ci_events:")],
                    "fails": [l.strip()[:300] for l in lines if l.startswith("  FAIL ")][:4]}
    json.dump(res, open(sys.argv[1], "w"), indent=1)
    for k, v in res.items():
        print(k, "rc=", v["rc"], v["tail"], v["fails"][:2])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

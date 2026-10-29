"""Copy every cited receipt into the output directory through receipts.py
(host details scrubbed, large logs digested), then write the index.

usage: collect.py
Re-runnable: each run rewrites receipts/ from the scratch records present.
"""
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("<scratch>")
sys.path.insert(0, str(S / "scripts"))
import receipts  # noqa: E402

REC = receipts.REC
if REC.exists():
    shutil.rmtree(REC)
REC.mkdir(parents=True)


def put(src: Path, dest: str) -> None:
    if src.is_file():
        receipts.copy(src, REC / dest)


def spec_dir(name: str, dest: str) -> None:
    d = S / "runs" / "specs" / name
    for p in sorted(d.glob("*")):
        if p.is_file():
            put(p, f"{dest}/{p.name}")
    put(S / "runs" / "specs" / f"{name}.json", f"specs/{name}.json")


for name, dest in [("base-fast", "repo-base-fast"), ("head-fast", "repo-head-fast"),
                   ("base-arm", "repo-base-arm"), ("head-arm", "repo-head-arm"),
                   ("base-pA", "parent-base-A"), ("head-pA", "parent-head-A"),
                   ("base-pB", "parent-base-B"), ("head-pB", "parent-head-B"),
                   ("base-px", "parent-base-extra"), ("head-px", "parent-head-extra"),
                   ("base-fuzz", "parent-base-extra/fuzz"), ("head-fuzz", "parent-head-extra/fuzz")]:
    spec_dir(name, dest)
for side in ("base", "head"):
    diff = subprocess.run(["git", "-C", str(S / "runs" / f"{side}-px"), "diff"],
                          capture_output=True, text=True).stdout
    (S / "rec" / f"{side}-px-tree.diff").write_text(diff)
    put(S / "rec" / f"{side}-px-tree.diff", f"parent-{side}-extra/tree-after-runs.diff")
put(S / "rec" / "head-arm-94-verdicts.txt", "repo-head-arm/strict-94-verdicts.txt")
for f in ("base-pB-lines.txt", "head-pB-lines.txt", "head-pB-lines-vs-base.diff"):
    put(S / "rec" / f, f"parent-head-B/{f}")
for p in sorted((S / "runs" / "pmut").glob("*")):
    put(p, f"parent-controls/{p.name}")
put(S / "runs" / "pmut.console", "parent-controls/console.txt")
cov = S / "runs" / "covF"
for p in sorted(cov.glob("*")):
    if p.is_file():
        put(p, f"coverage/{p.name}")
put(S / "runs" / "covF.console", "coverage/console.txt")
put(S / "checks94.txt", "coverage/checks94.txt")
put(S / "rec" / "new-check-coverage.md", "coverage/new-check-coverage.md")
put(S / "rec" / "named-fail-lines.md", "coverage/named-fail-lines.md")
for sub in ("probes", "rom"):
    for p in sorted((S / "rec" / sub).glob("*")):
        put(p, f"{sub}/{p.name}")
for p in sorted((S / "area").glob("*/*")):
    if p.suffix in (".rpt",) or p.name.endswith(".console"):
        put(p, f"area/{p.parent.name}/{p.name}")
for p in sorted((S / "scripts").glob("*")):
    if p.is_file() and p.suffix in (".py", ".sh", ".tcl"):
        put(p, f"scripts/{p.name}")
receipts.index()

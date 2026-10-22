#!/usr/bin/env python3
"""collect_receipts.py: copy the round-2 receipts from lane scratch into the
output directory's round2/, gzip or digest anything over 200 KB, and write
the per-suite tally and log digests of both sweeps. Run make_index.py after.
"""
import gzip
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("$VALIDATION_STORAGE/771-a662-r2")
O = Path("$MANAGEMENT/2026-09-23/771-a662/round2")
REPO = Path("$LANES/771-pin4")
LIMIT = 200 * 1024
large = []


def put(src: Path, rel: str) -> None:
    """Copy src to round2/rel; over the limit, keep a gzip copy if it fits, and always its digest."""
    dst = O / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    data = src.read_bytes()
    if len(data) <= LIMIT:
        dst.write_bytes(data)
        return
    large.append(f"{hashlib.sha256(data).hexdigest()}  {len(data)}  {rel}")
    packed = gzip.compress(data, mtime=0)
    if len(packed) <= LIMIT:
        Path(str(dst) + ".gz").write_bytes(packed)


def tree(src: Path, rel: str, pattern: str = "*") -> None:
    for f in sorted(src.glob(pattern)):
        if f.is_file():
            put(f, f"{rel}/{f.name}")


if O.exists():
    shutil.rmtree(O)
O.mkdir(parents=True)
H = "1098978f"
# case-a: the walk at a97aea01 and at the head, the two controls, the production probe
for label in ("base-a97aea01", f"head-{H}"):
    put(S / f"probe/{label}/result.json", f"case-a/walk-{label}.json")
    put(S / f"probe/{label}/acmpwalk.log", f"case-a/walk-{label}.log")
tree(S / f"probe/controls-{H}", f"case-a/controls-{H}", "*.log")
put(S / f"probe/controls-{H}/result.json", f"case-a/controls-{H}/result.json")
for v in ("clean", "glue-lost", "stack-mute"):
    tree(S / f"probe/production-{H}/{v}", f"case-a/production-{H}/{v}", "*.log")
put(S / f"probe/production-{H}/result.json", f"case-a/production-{H}/result.json")
put(S / "probe-production-check.diff", "case-a/probe-production-check.diff")
# firmware gate set, the census against dev's own inputs
tree(S / "fw", "firmware-gates")
# SDK
for f in ("sdk-install.log", "sdk-verify.log", "sdk-selftest.log"):
    put(S / f, f"sdk/{f}")
# quick gates at the head
tree(S / "quick-final", "quick-gates")
# docs replica
for part in ("all", "leg1-litex"):
    put(S / f"docs/{part}/receipts.json", f"docs-steps/{part}-receipts.json")
    put(S / f"docs/{part}.out", f"docs-steps/{part}.out")
    put(S / f"docs/{part}.rc", f"docs-steps/{part}.rc")
# sweeps
for name in ("sweep", "physical"):
    for f in ("env.txt", "sweep.out", "sweep.rc", "sweep.seconds", "tally.out", "tally.rc", "done"):
        if (S / name / f).exists():
            put(S / name / f, f"{name}/{f}")
    logs = S / name / "logs"
    rows = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.stat().st_size}  {p.name}"
            for p in sorted(logs.glob("*.log"))]
    (O / name / "log-digests.txt").write_text("\n".join(rows) + "\n")
    table = subprocess.run([sys.executable, "scripts/suite_tally.py", str(logs), "--expect-suite-root",
                            "tb/verilator", *(["--physical-gptp"] if name == "physical" else [])],
                           cwd=REPO, capture_output=True, text=True)
    (O / name / "tally-per-suite.txt").write_text(table.stdout + table.stderr + f"rc={table.returncode}\n")
put(S / "physical/logs/milan_dp_gptp.log", "physical/milan_dp_gptp.log")
# yosys, behave, xvlog
tree(S / "rtl", "rtl-gates")
# memory
put(S / "mem.txt", "rtl-gates/memory-peak.txt")
# scripts
tree(S / "scripts", "scripts")
shutil.copy(Path("$VALIDATION_STORAGE/scratch/a662/docs_steps.py"), O / "scripts/docs_steps.py")
(O / "large-files").mkdir(exist_ok=True)
(O / "large-files/digests.txt").write_text(
    "# sha256  bytes  round2-relative path of the original (a .gz copy sits beside it when it fits)\n"
    + "\n".join(large) + "\n")
print(f"collected; {len(large)} large file(s): {large}")

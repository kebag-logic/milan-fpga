#!/usr/bin/env python3
"""Lane B16, round 10: round 10's reader with round 9's rows, on the page at round 9's head, against round 9's outputs.

usage: <parser python> r10_reader_on_r9.py <round 9 check> <round 10 check> <tree> <packet root> <scratch> <out.json>

Round 9's r9_reader_on_r8.py, one round on. Round 10 added two refusals to the check's reader (a block holding a
node the parser gives no position, and a block whose rendered digits differ from those the check read), wrote
row keys shorter and added rows. To show that the change in reading alone moves nothing on the page as it
stood, this writes a check that is round 10's with round 9's ROWS_TSV and EXCLUDE blocks put back, runs it on
<tree>, a tree exported from the page commit cb5ff79f (the caller sets GIT_DIR to the repository), and
compares its rows, coverage and standard output byte for byte with the packet's r9/figures-rows.tsv,
r9/figures-coverage.tsv and r9/figures-check.stdout. Offline; nothing on the bench is read or written.
"""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

R9, R10, TREE, PACKET, SCRATCH, OUT = (Path(a).resolve() for a in sys.argv[1:7])
SCRATCH.mkdir(parents=True, exist_ok=True)


def block(src, name):
    a = src.index(f"# {name}-BEGIN\n") + len(f"# {name}-BEGIN\n")
    return a, src.index(f"# {name}-END")


old, new = R9.read_text(encoding="utf-8"), R10.read_text(encoding="utf-8")
for name in ("ROWS", "EXCLUDE"):
    a, b = block(new, name)
    c, d = block(old, name)
    new = new[:a] + old[c:d] + new[b:]
hybrid = SCRATCH / "check_r10_reader_r9_rows.py"
hybrid.write_text(new, encoding="utf-8")
page = TREE / "docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md"
rows, cov = SCRATCH / "rows.tsv", SCRATCH / "coverage.tsv"
p = subprocess.run([sys.executable, "-I", str(hybrid), str(page), str(PACKET), str(rows), str(cov), "--repo", str(TREE)],
                   capture_output=True, text=True, timeout=600)
(SCRATCH / "stdout").write_text(p.stdout)


def sha(b):
    return hashlib.sha256(b).hexdigest()


out = dict(note="Lane B16 round 10: round 10's reader with round 9's rows and categories, on the page at cb5ff79f, "
                "against round 9's outputs; offline, no bench action",
           round9_check_sha256=sha(R9.read_bytes()), round10_check_sha256=sha(R10.read_bytes()),
           hybrid_sha256=sha(hybrid.read_bytes()), page_sha256=sha(page.read_bytes()), rc=p.returncode,
           summary=json.loads(p.stdout.splitlines()[0]) if p.stdout.startswith("{") else None,
           rows_equal=rows.read_bytes() == (PACKET / "r9/figures-rows.tsv").read_bytes(),
           coverage_equal=cov.read_bytes() == (PACKET / "r9/figures-coverage.tsv").read_bytes(),
           stdout_equal=p.stdout.encode() == (PACKET / "r9/figures-check.stdout").read_bytes())
OUT.write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({k: out[k] for k in ("rc", "rows_equal", "coverage_equal", "stdout_equal")}))
sys.exit(0 if p.returncode == 0 and out["rows_equal"] and out["coverage_equal"] and out["stdout_equal"] else 1)

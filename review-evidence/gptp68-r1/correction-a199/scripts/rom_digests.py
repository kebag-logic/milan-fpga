#!/usr/bin/env python3
"""SHA-256 of every tracked ROM image at base, reviewed and head, the images
each generator produces for the seeded regression runs and for the parent's
per-configuration clocks, and a word-level change summary head vs base and
head vs reviewed. The tracked images must equal their generator's output
at every revision (re-checked here)."""
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

LANE = Path(os.environ.get("A199_LANE", "$LANES/gptp68-step-policy"))
REVS = {"base": "c1b617435824929a790739ea8585c3fe1a328cc0",
        "reviewed": "77c34e904eba2446755d13e1bf4763d1652c3ca7",
        "head": subprocess.run(["git", "-C", str(LANE), "rev-parse", "HEAD"],
                               capture_output=True, text=True).stdout.strip()}
TRACKED = {"tb/verilator/engine/gptp_ucode.hex": ["--clk-hz", "2000000", "--cease-ms", "3000"],
           "tb/tsngen/gptp_ucode.hex": ["--clk-hz", "2000000"],
           "tb/verilator/ucpu/gptp_ucode.hex": [],
           "syn/ooc/work/gptp_ucode.hex": []}
EXTRA = {"engine seeded --seq-seed 0x200000": ["--clk-hz", "2000000", "--cease-ms", "3000", "--seq-seed", "0x200000"],
         "engine seeded --sync-seq-seed 0x10000": ["--clk-hz", "2000000", "--cease-ms", "3000", "--sync-seq-seed", "0x10000"],
         "--clk-hz 25000000": ["--clk-hz", "25000000"],
         "--clk-hz 50000000": ["--clk-hz", "50000000"],
         "--clk-hz 125000000": ["--clk-hz", "125000000"]}


def git_show(rev, path):
    return subprocess.run(["git", "-C", str(LANE), "show", f"{rev}:{path}"],
                          capture_output=True, check=True).stdout


def gen(src, args, tmp):
    g = tmp / "g.py"
    g.write_bytes(src)
    out = tmp / "o.hex"
    r = subprocess.run([sys.executable, str(g), *args, "-o", str(out)],
                       capture_output=True, text=True, check=True).stdout
    return out.read_bytes(), r.splitlines()[0]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def words(b):
    return b.decode().split()


def ranges(a, b):
    diff = [i for i, (x, y) in enumerate(zip(words(a), words(b))) if x != y]
    out, start = [], None
    for i, j in zip(diff, diff[1:] + [None]):
        start = i if start is None else start
        if j != i + 1:
            out.append(f"{start}..{i}" if i != start else f"{i}")
            start = None
    return len(diff), out


bad = 0
with tempfile.TemporaryDirectory() as td:
    tmp = Path(td)
    srcs = {k: git_show(v, "hdl/ucode/gen_gptp_ucode.py") for k, v in REVS.items()}
    print("| Tracked image | Generator arguments | base c1b6174 | reviewed 77c34e9 | head |")
    print("|---|---|---|---|---|")
    imgs = {}
    for path, args in TRACKED.items():
        row = []
        for k, rev in REVS.items():
            t = git_show(rev, path)
            g, info = gen(srcs[k], args, tmp)
            if t != g:
                bad += 1
                print(f"MISMATCH {k} {path}: tracked image is not its generator's output")
            imgs[(path, k)] = t
            row.append(f"`{sha(t)}`")
        print(f"| `{path}` | `{' '.join(args) or 'defaults'}` | " + " | ".join(row) + " |")
    print()
    print("| Untracked image (generated at test time) | base | reviewed | head |")
    print("|---|---|---|---|")
    for label, args in EXTRA.items():
        row = [f"`{sha(gen(srcs[k], args, tmp)[0])}`" for k in REVS]
        print(f"| {label} | " + " | ".join(row) + " |")
    print()
    for path in TRACKED:
        for other in ("base", "reviewed"):
            n, rg = ranges(imgs[(path, other)], imgs[(path, "head")])
            print(f"{path}: head vs {other}: {n} words differ at {', '.join(rg)}")
    for k in REVS:
        print(f"{k}: {gen(srcs[k], [], tmp)[1]}")
print("RESULT:", "PASS" if bad == 0 else f"FAIL ({bad})")
sys.exit(1 if bad else 0)

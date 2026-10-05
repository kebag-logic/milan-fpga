#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""normcmp.py - reviewer comparer for default_build_identity.sh exports (PR #668).

For each config, compares <root>/<a>/<cfg> with <root>/<b>/<cfg> file by file.
Normalisation, and nothing else: the export's own output path becomes OUT;
LiteX timestamp lines and litex.log's "# Command:" line are dropped; LiteX's
comment-only hierarchy tree (lines carrying box-drawing glyphs, the last-child
glyph folded into the plain one) is compared as a sorted multiset, because its
black-box order varies run to run; the CPU generator's "VexiiRiscv netlist"
stdout fragment is removed from litex.log, where it lands at a run-dependent
point. Every other
byte must be equal. Prints one line per config and every differing file with
its first differing lines.

usage: normcmp.py <root> <a> <b> [cfg ...]
"""
import re
import sys
from pathlib import Path

STAMP = re.compile(r"(Auto-[Gg]enerated by LiteX.* on \d{4}-\d\d-\d\d|// Date\s*: \d{4}-|# Started: \d{4}-|"
                   r"\(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d\)$)")
TREE = re.compile(r"[\u2500-\u257f]")


def norm(path: Path, out: str) -> tuple[list[str], list[str]]:
    text = path.read_bytes().decode("utf-8", errors="replace").replace(out, "OUT")
    if path.name == "litex.log":
        # the CPU generator's own stdout line lands at a run-dependent point
        text = re.sub(r"VexiiRiscv netlist : VexiiRiscvLitex_[0-9a-f]+\n?", "", text)
    body, tree = [], []
    for ln in text.splitlines():
        if STAMP.search(ln) or ln.startswith("# Command:"):
            continue
        # the last child of a tree level is drawn with a different glyph, so
        # a reordered level changes which line carries it
        (tree if TREE.search(ln) else body).append(ln.replace("\u2514", "\u251c"))
    return body, sorted(tree)


def main() -> int:
    root, a, b = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
    cfgs = sys.argv[4:] or sorted(p.name for p in (root / a).iterdir() if p.is_dir())
    bad = 0
    for cfg in cfgs:
        da, db = root / a / cfg, root / b / cfg
        fa = sorted(str(p.relative_to(da)) for p in da.rglob("*") if p.is_file())
        fb = sorted(str(p.relative_to(db)) for p in db.rglob("*") if p.is_file())
        diffs = []
        for f in sorted(set(fa) | set(fb)):
            if f not in fa or f not in fb:
                diffs.append(f"{f}: only in {'b' if f not in fa else 'a'}")
                continue
            ba, ta = norm(da / f, str(da))
            bb, tb = norm(db / f, str(db))
            if ba != bb or ta != tb:
                first = next(((x, y) for x, y in zip(ba, bb) if x != y), None)
                extra = len(ba) - len(bb)
                diffs.append(f"{f}: body {'equal' if ba == bb else 'DIFFERS'} (first {first}, len delta {extra}); "
                             f"tree multiset {'equal' if ta == tb else 'DIFFERS'}")
        print(f"{cfg}: {len(fa)} vs {len(fb)} files, {len(diffs)} differ after normalisation")
        for d in diffs:
            print(f"    {d[:600]}")
        bad += bool(diffs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

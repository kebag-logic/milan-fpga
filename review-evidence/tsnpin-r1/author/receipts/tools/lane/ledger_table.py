"""ledger_table.py <base dir> <head dir>: each split point's plan at both pins, from ctrl_srp_image.py's size.json."""
import json, sys
from pathlib import Path
base, head = Path(sys.argv[1]), Path(sys.argv[2])
GRANULE = 2048
print("| Point | text B (70936b77 -> 715589c) | `rom` need B | `sram` need B | `rom` banks | `sram` banks | RAMB36 equivalents | `rom` left before its next granule | `__lshrdi3` |")
print("|---|---:|---:|---:|---|---|---:|---:|---|")
for tag, name in (("1x1_tdm8-if1", "1x1, one interface (shipping)"), ("1x1_tdm8-if2", "1x1, two interfaces"),
                  ("8x8-if1", "8x8, one interface"), ("8x8-if2", "8x8, two interfaces (ledgered 57.5)")):
    rows = []
    for d in (base, head):
        r = json.loads((d / tag / "size.json").read_text())
        s = r["split"]
        nm = (d / f"{tag}.nm").read_text()
        rows.append((r["sections"][".text"], s["rom"]["bytes"], s["sram"]["bytes"], s["rom"]["banks"], s["sram"]["banks"],
                     s["tiles"], sum(s["rom"]["banks"]) - s["rom"]["bytes"], " __lshrdi3\n" in nm))
    (t0, r0, m0, rb0, mb0, k0, l0, h0), (t1, r1, m1, rb1, mb1, k1, l1, h1) = rows
    moved = "" if (rb0, mb0) == (rb1, mb1) else " **PLAN MOVES**"
    print(f"| {name} | {t0:,} -> {t1:,} ({t1 - t0:+,}) | {r0:,} -> {r1:,} ({r1 - r0:+,}) | {m0:,} -> {m1:,} ({m1 - m0:+,}) | "
          f"{rb0} -> {rb1} | {mb0} -> {mb1} | {k0} -> {k1}{moved} | {l0:,} -> {l1:,} | {'defined' if h0 else 'absent'} -> {'defined' if h1 else 'absent'} |")

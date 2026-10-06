#!/usr/bin/env python3
"""R506-2 probe: compensating swaps on the real firmware measurement.
Reads a kept coverage build (fw_coverage.py --check --keep DIR) with the
clone's own reader, then for every README exclusion row: covers the row's
first named arc (or, for a lines-only row, runs its line) and uncovers one
covered arc elsewhere in the same function, so the function's totals are
unchanged; requires the gate to refuse. Also a control (no change: no finding).
Usage: python3 row_swap_probe.py <review clone> <kept coverage dir>"""
import copy, sys
from pathlib import Path
clone, keep = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(clone / "sw/firmware/gtest"))
import fw_coverage as cov  # noqa: E402
base = cov.collect([keep / "ctrl", keep / "ctrl_nvm"])
rows = cov.exclusions(cov.README.read_text(encoding="utf-8"))
_, found = cov.apply_exclusions(copy.deepcopy(base), rows)
ratchet = cov.read_ratchet(cov.RATCHET.read_text(encoding="utf-8"))
print(f"control: {len(rows)} rows, findings {found}, drops {cov.compare(cov.tally(cov.apply_exclusions(copy.deepcopy(base), rows)[0]), ratchet)}")
escapes = 0
skipped = 0
for i, r in enumerate(rows):
    m = copy.deepcopy(base)
    src = m[r.file]
    span = src.functions[r.function]
    text = (clone / r.file).read_text().splitlines()
    first = next(n for n in range(span[0], span[1] + 1) if r.statement in text[n - 1])
    last = cov.statement_end(text, first, span[1])
    order = [(n, k) for n in range(first, last + 1) if n in src.lines for k, _ in enumerate(src.lines[n].arcs)]
    permit = cov.parse_uncovered(r.uncovered)
    if permit.arcs:
        n, k = order[permit.arcs[0] - 1]
        src.lines[n].arcs[k] = 1
        moved = f"arc {permit.arcs[0]} of the statement covered"
    else:
        n = next(x for x in range(first, span[1] + 1) if permit.lines[0] in text[x - 1])
        src.lines[n].count = 1
        moved = "its line run"
    other = next(((n2, k2) for n2 in range(span[0], span[1] + 1) if n2 in src.lines
                  for k2, a in enumerate(src.lines[n2].arcs) if a > 0 and (n2, k2) not in order), None)
    if other is None:  # the function's only branches are the statement's: swap inside it
        other = next(((n2, k2) for (n2, k2) in order if src.lines[n2].arcs[k2] > 0), None)
    if other is None:
        print(f"[skip] row {i + 1} {r.function}: no covered arc to uncover"); skipped += 1; continue
    src.lines[other[0]].arcs[other[1]] = 0
    before = cov.tally({r.file: base[r.file]})[r.file]
    after = cov.tally({r.file: src})[r.file]
    kept, f = cov.apply_exclusions(m, rows)
    drops = cov.compare(cov.tally(kept), ratchet)
    ok = bool(f or drops)
    escapes += 0 if ok else 1
    print(f"[{'refused' if ok else 'ESCAPE'}] row {i + 1} {r.file.split('/')[-1]} {r.function}: {moved}, "
          f"line {other[0]} arc {other[1] + 1} uncovered; raw totals {before.branches}->{after.branches}; "
          f"first finding: {(f + drops)[0] if ok else '-'}")
print(f"swaps refused: {len(rows) - escapes - skipped} of {len(rows)} ({skipped} skipped)")
sys.exit(1 if escapes or skipped else 0)

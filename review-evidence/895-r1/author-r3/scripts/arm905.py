#!/usr/bin/env python3
"""arm905.py MILAN_DP WORK: srptx_mutants.py's arm "no source's SRC_SID written (#905)" run by hand, with that
script's own build() and run(), and without its clean control, which the licence scenario's [TIME] findings (present
at #810's head 084cf7a8 too) refuse. Plants the arm's line in a copy of maap_mbx.c, builds the split half through
twin_fw.py --replace into WORK, runs the licence scenario, grades it, and exits 0 only if a finding holds the arm's
words and no [SID] finding is in the unplanted licence capture of MILAN_DP's obj_srptx."""
import json
import sys
from pathlib import Path

here, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(here))
import srptx_mutants as sm  # noqa: E402
import srptx_grade as g  # noqa: E402

name, src, old, new, scenario, ms, words = next(a for a in sm.ARMS if a[0].startswith("no source's SRC_SID"))
text = src.read_text()
assert text.count(old) == 1, "anchor not in the source once"
work.mkdir(parents=True, exist_ok=True)
copy = work / src.name
copy.write_text(text.replace(old, new))
ok, out = sm.build(work, src, copy)
print(f"build {'ok' if ok else 'FAILED'}")
if not ok:
    print(out)
    sys.exit(1)
rc, found, out = sm.run(work, scenario, ms)
caught = [f for f in found if words in f]
print(f"planted run rc {rc}, {len(found)} finding(s); {'REFUSED by ' + caught[0] if caught else 'ESCAPED'}")
clean = g.grade(g.load(here / 'obj_srptx' / 'licence.json'))[0]
held = [f for f in clean if f.startswith('[SID]')]
print(f"unplanted licence capture: {len(clean)} finding(s), {len(held)} [SID]")
sys.exit(0 if caught and not held else 1)

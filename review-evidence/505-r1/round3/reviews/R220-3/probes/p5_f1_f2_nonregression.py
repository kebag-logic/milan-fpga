#!/usr/bin/env python3
"""p5 (R220-3): F1/F2 non-regression at the tree given by argv[1] (an archive
copy of the head). Prints the #407 carrier arm composition (F2: one
`or-true-line-N` arm per non-last normalized line, including the AC5 line),
and the canonical records of docs-check steps 41-43 (F1)."""
import collections
import pathlib
import re
import sys

sys.dont_write_bytecode = True
root = pathlib.Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts"))
import ci_events as ce  # noqa: E402

w = ce.parse_world(ce.read_tree(root))
arms = ce._carrier_script_arms(w)
print("carrier-script-407 arms at head:", len(arms))
kinds = collections.Counter()
for a in arms:
    m = re.search(r"step \d+ (\S+)", a[0])
    kinds[re.sub(r"-\d+$", "-N", m.group(1) if m else a[0])] += 1
for k, v in sorted(kinds.items()):
    print(f"  {k}: {v}")
ac5 = [a for a in arms if "docs-check step 34 " in a[0] and "or-true-line-1" in a[0]]
print("AC5 or-true-line-1 arm present:", len(ac5) == 1, ac5[0][0] if ac5 else None)
for n in (41, 42, 43):
    e = ce.CARRIER_STEP_LISTS[(ce.DOCS, "docs-check")][n - 1]
    print(f"docs-check step {n}: name={e.get('name')!r} run-record={e.get('run')!r}")

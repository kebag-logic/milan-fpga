#!/usr/bin/env python3
"""Compare the committed MUTANTS list with the published mutants, by mutated-file sha256.

usage: python3 -I compare_list.py <clone> <collected.json>
Each committed mutant is applied to the head's scripts/owned_process.py exactly as
mutant_tree() does; each published group carries the 12-hex digest of its mutated text.
Prints every published group with the committed name(s) giving the same text, and any
group or committed name without a partner.
"""
import hashlib
import json
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(clone / "scripts"))
import process_test_support as pts  # noqa: E402

head = (clone / "scripts/owned_process.py").read_text()
committed = {}
for name, entry in pts.MUTANTS.items():
    text = head
    for old, new in entry[2:]:
        assert text.count(old) == 1, (name, old)
        text = text.replace(old, new)
    committed.setdefault(hashlib.sha256(text.encode()).hexdigest()[:12], []).append(name)
groups = json.loads(Path(sys.argv[2]).read_text())
published = {g["text_sha"]: g["sources"] for g in groups}
missing = [d for d in published if d not in committed]
extra = [d for d in committed if d not in published]
for digest, sources in published.items():
    print(digest, committed.get(digest, ["MISSING"]), len(sources), "sources:", " ".join(sources))
print(f"committed entries {len(pts.MUTANTS)}, distinct committed texts {len(committed)}, "
      f"published distinct texts {len(published)}")
print("published texts without a committed entry:", missing)
print("committed texts not among the published:", [committed[d] for d in extra])
print("committed names sharing one text:", [v for v in committed.values() if len(v) > 1])
sys.exit(1 if missing else 0)

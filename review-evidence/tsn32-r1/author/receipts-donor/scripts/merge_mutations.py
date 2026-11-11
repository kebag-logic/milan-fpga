"""Three-way merge of tests/mutations.json by plant name (base ea4af6f, ours fa31d4c8, theirs origin/main)."""
import json, subprocess, sys
from pathlib import Path

def load(rev):
    return json.loads(subprocess.run(['git', 'show', f'{rev}:tests/mutations.json'], check=True,
                                     capture_output=True, text=True).stdout)

base, ours, theirs = (load(r) for r in ('ea4af6f', 'fa31d4c', 'origin/main'))
for lst in (base, ours, theirs):
    assert isinstance(lst, list) and len({p['name'] for p in lst}) == len(lst)
B = {p['name']: p for p in base}; O = {p['name']: p for p in ours}; T = {p['name']: p for p in theirs}
merged, conflicts = [], []
for p in theirs:
    n = p['name']
    if n in O and O[n] != B.get(n) and n in B:
        if T[n] != B[n]:
            conflicts.append(n)
            merged.append(O[n])  # placeholder, fixed below
        else:
            merged.append(O[n])
    else:
        merged.append(p)
deleted_by_ours = [n for n in B if n not in O]
deleted_by_theirs = [n for n in B if n not in T]
for p in ours:
    if p['name'] not in B and p['name'] not in T:
        merged.append(p)
print('conflicts', conflicts, 'deleted ours', deleted_by_ours, 'deleted theirs', deleted_by_theirs)
print('counts base', len(base), 'ours', len(ours), 'theirs', len(theirs), 'merged', len(merged))
json.dump({'merged': merged, 'conflicts': conflicts}, open(sys.argv[1], 'w'), indent=2)

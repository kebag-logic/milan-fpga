"""Compare the builder outputs written by compare.sh: per placement, every output file's SHA256 at each head, and
whether each named pair of heads wrote byte-identical sets. Exit 0 only if every pair is identical."""
import hashlib, json, sys
from pathlib import Path
here = Path(__file__).resolve().parent
root = here / (sys.argv[2] if len(sys.argv) > 2 else 'out2')
HEADS = {'4adfa9dc84f5': '4adfa9dc84f58c1c7ad23d6a64fa019985fe62a1', '011aaa6f0803': '011aaa6f080321e0a89f915720ebb3ee14807a16',
         'aa53840d9128': 'aa53840d91286281e77f158d28dcbccdf51b56c0', sys.argv[1][:12]: sys.argv[1]}
PAIRS = [('4adfa9dc84f5', '011aaa6f0803'), ('aa53840d9128', sys.argv[1][:12])]
def outputs(short, placement):
    base = root / f'src-{short}' / placement
    return {str(p.relative_to(base)): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(base.rglob('*')) if p.is_file()}
rc, report = 0, dict(command='python3 -I -B sw/builder/endstation_builder.py configs/endstation_arty_split.yaml '
                     '--placement PLACEMENT -o OUT, from a clean export of each head with its pinned submodules',
                     heads=HEADS, placements={})
for placement in ('split', 'all-fabric'):
    sets = {s: outputs(s, placement) for s in HEADS}
    pairs = []
    for a, b in PAIRS:
        differ = sorted(k for k in sets[a].keys() | sets[b].keys() if sets[a].get(k) != sets[b].get(k))
        pairs.append(dict(heads=[HEADS[a], HEADS[b]], files=len(sets[a]), identical=not differ, differing=differ))
        rc |= bool(differ)
        print(f'{placement}: {HEADS[a][:9]} vs {HEADS[b][:9]}: {len(sets[a])} vs {len(sets[b])} outputs, '
              f'{"IDENTICAL" if not differ else "DIFFER: " + " ".join(differ)}')
    across = sorted(k for k in sets['011aaa6f0803'].keys() | sets['aa53840d9128'].keys()
                    if sets['011aaa6f0803'].get(k) != sets['aa53840d9128'].get(k))
    print(f'{placement}: (merge, informative) 011aaa6f0 vs aa53840d9 differ in {len(across)}: {" ".join(across)}')
    report['placements'][placement] = dict(outputs=sets, pairs=pairs, merge_differs=across)
(here / 'builder-split.json').write_text(json.dumps(report, indent=1) + '\n')
print(f'RESULT: {"PASS" if not rc else "FAIL"} exit={int(rc)}')
sys.exit(int(rc))

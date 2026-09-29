#!/usr/bin/env python3
"""Show mutants 6-E (MAC_OCTETS backreference replaced by [:-]) and 6-G
(octets of one or two digits) are behaviourally equivalent to the head.

usage: item6_equivalence.py <head-root> <mut6E-root> <mut6G-root> <workdir>
The mutant roots are `git archive HEAD` extractions with the one edit each
(see mutants.py entries 6-E and 6-G). Cases: the reviewer's item-6 probe
spellings (<workdir>/item6/spellings.json from item6_inventory.py) plus every
string over {0,2,:,-,_} of length 1..7 and separator-bearing spellings with
1-3 digits per group, 5-7 groups, uniform and mixed separators.
"""
import itertools, json, subprocess, sys
from pathlib import Path
HEAD, E, G, W = (Path(a).resolve() for a in sys.argv[1:5])
JUDGE = Path(__file__).with_name("item6_judge.py")
cases = json.loads((W / "item6/spellings.json").read_text())
extra = ["".join(p) for n in range(1, 8) for p in itertools.product("02:-_", repeat=n)]
for groups in (5, 6, 7):
    for widths in itertools.product((1, 2, 3), repeat=groups):
        body = ["0" * (w - 1) + "2" for w in widths]
        for seps in {(":",) * (groups - 1), ("-",) * (groups - 1), (":",) * (groups - 2) + ("-",),
                     ("-",) + (":",) * (groups - 2)}:
            extra.append(body[0] + "".join(a + b for a, b in zip(seps, body[1:])))
cases += [["mac", s] for s in extra]
(W / "equiv.json").write_text(json.dumps(cases))
res = {}
for tag, root in (("head", HEAD), ("6-E", E), ("6-G", G)):
    out = W / f"equiv_{tag}.json"
    subprocess.run([sys.executable, str(JUDGE), str(root), str(W / "equiv.json"), str(out)], check=True)
    res[tag] = [v[2] if v[2].startswith("ACCEPT") else v[2].split(" ", 1)[0] for v in json.loads(out.read_text())]
for tag in ("6-E", "6-G"):
    diff = [(cases[i], res["head"][i], res[tag][i]) for i in range(len(cases)) if res["head"][i] != res[tag][i]]
    print(f"{tag}: cases={len(cases)} accept/refuse verdict or value differences from head={len(diff)}")
    for d in diff[:20]:
        print("  ", d)

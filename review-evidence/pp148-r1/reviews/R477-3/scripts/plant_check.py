#!/usr/bin/env python3
"""Reviewer plant check: does every planted mutant still plant on a tree?

Usage: plant_check.py TREE  (TREE is an extracted `git archive` of the head)

Covers every reviewed .patch arm (git apply --check decides, as in the
drivers; GNU patch --dry-run -F0 is reported alongside, with any line offset) and every inline exact-replacement arm of the
drivers that plant by text (notify, d3, acmp, gsi, name write, srp admission,
talker retry). Each plant is printed as OK or REFUSED; the summary line is
`plants OK: N of M`. Exit status 0 only when all plant.
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
results = []  # (family, name, ok, note)
strict = []  # patches GNU patch refuses without fuzz


def load(rel):
    spec = importlib.util.spec_from_file_location(Path(rel).stem + "_rv", tree / rel)
    mod = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str((tree / rel).parent))
    spec.loader.exec_module(mod)
    sys.path.pop(0)
    return mod


for d in sorted(tree.glob("tb/**/*mutations")):
    for p in sorted(d.glob("*.patch")):
        r = subprocess.run(["git", "apply", "--check", str(p)], cwd=tree,
                           capture_output=True, text=True)
        q = subprocess.run(["patch", "-p1", "--dry-run", "--force", "-F0", "-i", str(p)],
                           cwd=tree, capture_output=True, text=True)
        notes = [l.strip() for l in q.stdout.splitlines() if "offset" in l or "fuzz" in l]
        if q.returncode:
            strict.append(f"{d.relative_to(tree)}/{p.name}")
            notes.append("GNU patch -F0 refuses it (git apply, the drivers' tool, decides)")
        results.append((str(d.relative_to(tree)), p.stem, r.returncode == 0,
                        (r.stderr.strip() + " " + "; ".join(notes)).strip()))


def text_edits(family, mutants, edits_of):
    for m in mutants:
        name, edits = edits_of(m)
        ok, note = True, ""
        for rel, old, new, count in edits:
            n = (tree / rel).read_text().count(old)
            if n != count or old == new:
                ok, note = False, f"{rel}: anchor occurs {n} times, want {count}"
        results.append((family, name, ok, note))


for drv in ("notify_mutants", "d3_mutants", "acmp_mutants"):
    mod = load(f"tb/pp_top/{drv}.py")
    text_edits(drv, mod.MUTANTS,
               lambda m: (m.name, [(rel, o, n, 1) for rel, o, n in m.edits]))

gsi = load("tb/pp_top/gsi_mutants.py")
text_edits("gsi_mutants", gsi.mutations(), lambda m: (m[0], [(m[1], m[2], m[3], m[4])]))

text_edits("name_wr_mutant", [("decode",)],
           lambda m: ("decode", [("hdl/aecp/KL_aecp_engine.sv",
                                  "  assign name_wr_o = d3_nchg_w;", "x", 1)]))

srp = load("tb/srp_admission/mutants.py")
text_edits("srp_admission", srp.MUTANTS,
           lambda m: (m[0], [(srp.ADMISSION, a, r, c) for a, r, c in m[1]]))

ret = load("tb/acmp_talker/retry_mutants.py")


def retry_edits(name):
    reps = ret.MUTATIONS[name]
    if isinstance(reps[0], str):
        reps = (reps,)
    return name, [(ret.RTL, o, n, 1) for o, n in reps]


text_edits("retry_mutants", list(ret.MUTATIONS), retry_edits)

fams = {}
for fam, name, ok, note in results:
    print(f"{'OK     ' if ok else 'REFUSED'} {fam} {name} {note}".rstrip())
    f = fams.setdefault(fam, [0, 0])
    f[0] += ok
    f[1] += 1
for fam, (a, b) in fams.items():
    print(f"family {fam}: {a} of {b}")
good = sum(ok for _, _, ok, _ in results)
npatch = sum(1 for f, *_ in results if f.endswith("mutations"))
print(f"patch arms needing fuzz under GNU patch -F0: {len(strict)} of {npatch} {strict}")
print(f"plants OK: {good} of {len(results)}")
sys.exit(0 if good == len(results) else 1)

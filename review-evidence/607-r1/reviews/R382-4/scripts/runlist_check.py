#!/usr/bin/env python3
"""Compare test_builder.py run lists and definitions across revisions (git show)."""
import ast, collections, subprocess, sys, re
repo = sys.argv[1]
def runlist(rev):
    src = subprocess.run(["git", "-C", repo, "show", f"{rev}:sw/builder/test_builder.py"],
                         capture_output=True, text=True, check=True).stdout
    tree = ast.parse(src)
    defs = collections.Counter(n.name for n in tree.body if isinstance(n, ast.FunctionDef))
    main = [n for n in tree.body if isinstance(n, ast.If) and "__main__" in ast.unparse(n.test)][0]
    loops = [n for n in ast.walk(main) if isinstance(n, ast.For) and isinstance(n.iter, ast.Tuple)]
    names = [e.id for e in loops[0].iter.elts]
    gates = collections.Counter(re.findall(r"\[gate ([0-9]+[a-z]?)\]", src))
    return src, defs, names, gates
out = {}
for label, rev in (("lane", sys.argv[2]), ("dev", sys.argv[3]), ("head", sys.argv[4])):
    src, defs, names, gates = runlist(rev)
    dup_defs = [k for k, v in defs.items() if v > 1]
    dup_run = [k for k, v in collections.Counter(names).items() if v > 1]
    undefined = [n for n in names if n not in defs]
    print(f"{label} {rev[:9]}: run entries={len(names)} unique={len(set(names))} dup_run={dup_run} "
          f"dup_defs={dup_defs} undefined_in_module={len(undefined)} gate_ids={len(gates)}")
    out[label] = (names, gates, defs)
h, d, l = out["head"][0], out["dev"][0], out["lane"][0]
print("head - dev:", sorted(set(h) - set(d)), " dev - head:", sorted(set(d) - set(h)))
print("head - lane:", sorted(set(h) - set(l)), " lane - head:", sorted(set(l) - set(h)))
hl = [x for x in h if x != "test_clock_crossing_constraints"]
print("head run order minus lane entry == dev order:", hl == d)
for fn in ("test_commercial_timing_grade", "test_clock_crossing_constraints"):
    print(fn, "run count:", h.count(fn), "def count:", out["head"][2][fn])
print("gate-id sets equal head/dev:", set(out["head"][1]) == set(out["dev"][1]),
      "max head:", sorted(out["head"][1])[-3:])

"""Audit the builder run list and gate-id namespace of sw/builder/test_builder.py at given revisions."""
import ast, collections, re, subprocess, sys

def src(rev, path):
    return subprocess.run(["git", "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout

def audit(rev):
    s = src(rev, "sw/builder/test_builder.py")
    tree = ast.parse(s)
    defs = collections.Counter(n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)))
    dup_defs = sorted(k for k, v in defs.items() if v > 1)
    main = [n for n in tree.body if isinstance(n, ast.If) and "__main__" in ast.unparse(n.test)][0]
    runlist = None
    for n in ast.walk(main):
        if isinstance(n, ast.For) and isinstance(n.iter, ast.Tuple):
            runlist = [ast.unparse(e) for e in n.iter.elts]
    imported = set()
    for n in ast.walk(main):
        if isinstance(n, ast.ImportFrom):
            imported |= {a.name for a in n.names}
    dup_run = sorted(k for k, v in collections.Counter(runlist).items() if v > 1)
    unresolved = [f for f in runlist if f not in defs and f not in imported]
    gate_ids = re.findall(r'_skip\(\s*"([^"]+)"', s) + re.findall(r'_litex_or_skip\(\s*"([^"]+)"', s)
    return dict(rev=rev, n_defs=sum(defs.values()), dup_defs=dup_defs, n_run=len(runlist), dup_run=dup_run,
                unresolved=unresolved, runlist=runlist, gate_ids=sorted(set(gate_ids)))

res = {r: audit(r) for r in sys.argv[1:]}
for r, a in res.items():
    print(f"== {r}: defs={a['n_defs']} dup_defs={a['dup_defs']} runlist={a['n_run']} dup_run={a['dup_run']} unresolved={a['unresolved']}")
    for i, f in enumerate(a["runlist"]):
        if f in ("test_commercial_timing_grade", "test_declaration_contracts", "test_clock_crossing_constraints",
                 "test_all_configs_build", "test_baremetal_profile_contract", "test_schema_12_refusals",
                 "test_schema_12_keys_reach_the_image"):
            print(f"   pos {i:2d} {f}")
revs = list(res)
if len(revs) >= 2:
    base = res[revs[0]]["runlist"]
    for r in revs[1:]:
        cur = res[r]["runlist"]
        print(f"-- {revs[0]} -> {r}: added {sorted(set(cur)-set(base))} removed {sorted(set(base)-set(cur))}")
        common = [f for f in cur if f in base]
        print(f"   relative order of common entries preserved: {common == [f for f in base if f in cur]}")

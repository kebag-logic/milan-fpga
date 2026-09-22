"""For every non-last command line of every carrier body: append `|| true` and
count what the REAL checker and the M5b mutant (which passes the complete
--selftest) report. Lines where M5b reports nothing are unprotected by the
self-test's regression proof. In memory only."""
import sys, pathlib, importlib.util, copy, re
root = pathlib.Path(sys.argv[1])
def load(n):
    spec = importlib.util.spec_from_file_location(n, root / "scripts/ci_events.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
real, mut = load("ce_real"), load("ce_mut")
strip = lambda l: re.sub(r" \|\| true$", "", l)
def patched(c, path, what, step, entry):
    canonical = entry.get("run")
    recorded = (isinstance(canonical, tuple) and bool(canonical) and all(isinstance(l, str) for l in canonical))
    c.item(recorded, path, f"{what} must record a canonical normalized `run` script")
    if not recorded:
        return
    g = tuple(mut.normalize_script(step["run"]))
    ok = len(g) == len(canonical) and all((strip(a) == strip(b)) if k < len(g) - 1 else a == b for k, (a, b) in enumerate(zip(g, canonical)))
    c.item(ok, path, f"{what} script is not the canonical form: " + mut.script_difference(g, canonical))
mut.check_carrier_script = patched
P = real.parse_world(real.read_tree(root))
exposed, caught_by_specialized, total = [], [], 0
for path, jid, at, step in real._carrier_run_steps(P):
    lines = real.normalize_script(step["run"])
    for k in range(len(lines) - 1):
        total += 1
        edited = list(lines); edited[k] += " || true"
        w = copy.deepcopy(P); real._job_steps(w, path, jid)[at]["run"] = "\n".join(edited)
        r, m = real.check(w).findings, mut.check(w).findings
        assert r, (jid, at, k)
        (caught_by_specialized if m else exposed).append(f"{jid} step {at+1} line {k+1}: {lines[k]}")
print(f"non-last lines: {total}; real checker refuses all {total}")
print(f"M5b (complete --selftest PASS) still refuses {len(caught_by_specialized)} via specialized pins; accepts {len(exposed)}:")
for e in exposed: print("   ", e)

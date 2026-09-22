"""Under comparator mutant M5b, is the exact AC5 tamper (line-1 `|| true` on the
Python idiom gate) accepted by check()? Real checker for contrast. In memory only."""
import sys, pathlib, importlib.util, copy, re
root = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ce_m5b", root / "scripts/ci_events.py")
ce = importlib.util.module_from_spec(spec); spec.loader.exec_module(ce)
P = ce.parse_world(ce.read_tree(root))
w = copy.deepcopy(P)
ss = ce._job_steps(w, ce.DOCS, "docs-check")
i = next(n for n, s in enumerate(ss) if s.get("name") == "Python idiom gate")
ss[i]["run"] = ss[i]["run"].replace("python3 scripts/check_py_idiom.py\n", "python3 scripts/check_py_idiom.py || true\n", 1)
assert "check_py_idiom.py || true\npython3 scripts/check_py_idiom.py --selftest" in ss[i]["run"]
print("real checker on AC5 tamper:", len(ce.check(w).findings), "finding(s)")
strip = lambda l: re.sub(r" \|\| true$", "", l)
def patched(c, path, what, step, entry):
    canonical = entry.get("run")
    recorded = (isinstance(canonical, tuple) and bool(canonical) and all(isinstance(l, str) for l in canonical))
    c.item(recorded, path, f"{what} must record a canonical normalized `run` script")
    if not recorded:
        return
    g = tuple(ce.normalize_script(step["run"]))
    ok = len(g) == len(canonical) and all((strip(a) == strip(b)) if k < len(g) - 1 else a == b for k, (a, b) in enumerate(zip(g, canonical)))
    c.item(ok, path, f"{what} script is not the canonical form: " + ce.script_difference(g, canonical))
ce.check_carrier_script = patched
print("M5b checker on pristine:", len(ce.check(P).findings), "finding(s); on AC5 tamper:", len(ce.check(w).findings), "finding(s)")

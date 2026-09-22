"""Run the complete ci_events --selftest in-process with the #407 comparison
weakened in memory (prefix match / order-insensitive / removed). No file edits."""
import sys, pathlib, importlib.util, io, contextlib
root = pathlib.Path(sys.argv[1]); which = sys.argv[2]
spec = importlib.util.spec_from_file_location("ci_events_r220", root / "scripts/ci_events.py")
ce = importlib.util.module_from_spec(spec); spec.loader.exec_module(ce)
orig = ce.check_carrier_script
def patched_factory(cmp):
    def patched(c, path, what, step, entry):
        canonical = entry.get("run")
        recorded = (isinstance(canonical, tuple) and bool(canonical)
                    and all(isinstance(l, str) for l in canonical))
        c.item(recorded, path, f"{what} must record a canonical normalized `run` script")
        if not recorded:
            return
        lines = tuple(ce.normalize_script(step["run"]))
        c.item(cmp(lines, canonical), path,
               f"{what} script is not the canonical form: " + ce.script_difference(lines, canonical))
    return patched
cmps = {"prefix": lambda g, w: g[:len(w)] == w,
        "sorted": lambda g, w: sorted(g) == sorted(w),
        "removed": None, "real": "real"}
c = cmps[which]
if c is None:
    ce.check_carrier_script = lambda *a, **k: None
elif c != "real":
    ce.check_carrier_script = patched_factory(c)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = ce.selftest(root)
out = buf.getvalue().splitlines()
fails = [l for l in out if "not caught" in l or "FAIL" in l or "problem" in l.lower()]
print(f"[{which}] selftest rc={rc}; last line: {out[-1] if out else ''}; failure lines: {len(fails)}")
for l in fails[:5]:
    print("   ", l[:220])

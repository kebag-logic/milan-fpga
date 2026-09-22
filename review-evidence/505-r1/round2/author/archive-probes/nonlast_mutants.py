"""Two more weakened-comparator mutants, run through the COMPLETE selftest in memory."""
import sys, pathlib, importlib.util, io, contextlib, re
root = pathlib.Path(sys.argv[1])
def run(label, cmp):
    spec = importlib.util.spec_from_file_location("ce_nl", root / "scripts/ci_events.py")
    ce = importlib.util.module_from_spec(spec); spec.loader.exec_module(ce)
    def patched(c, path, what, step, entry):
        canonical = entry.get("run")
        recorded = (isinstance(canonical, tuple) and bool(canonical) and all(isinstance(l, str) for l in canonical))
        c.item(recorded, path, f"{what} must record a canonical normalized `run` script")
        if not recorded:
            return
        lines = tuple(ce.normalize_script(step["run"]))
        c.item(cmp(lines, canonical), path, f"{what} script is not the canonical form: " + ce.script_difference(lines, canonical))
    ce.check_carrier_script = patched
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = ce.selftest(root)
    out = buf.getvalue().splitlines()
    print(f"{label}: complete selftest rc={rc}; {out[-1]}")
strip = lambda l: re.sub(r" \|\| true$", "", l)
run("M5b ignore a trailing '|| true' on every line but the last",
    lambda g, w: len(g) == len(w) and all((strip(a) == strip(b)) if i < len(g) - 1 else a == b for i, (a, b) in enumerate(zip(g, w))))
run("M10 ignore line 1 when a body has more than one line",
    lambda g, w: len(g) == len(w) and (g[1:] == w[1:] if len(w) > 1 else g == w))

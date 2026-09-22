import sys, pathlib, importlib.util
root = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("ce_c", root / "scripts/ci_events.py")
ce = importlib.util.module_from_spec(spec); spec.loader.exec_module(ce)
P = ce.parse_world(ce.read_tree(root))
tot = 0; calls = []
for path, jid, at, step in ce._carrier_run_steps(P):
    lines = ce.normalize_script(step["run"])
    if len(lines) > 1:
        nl = lines[:-1]; tot += len(nl)
        for k, l in enumerate(nl, 1):
            if l.startswith(("python3 ", "scripts/", "make ", "sw/")):
                calls.append(f"{jid} step {at+1} line {k}: {l}")
print("non-last lines in multi-command bodies:", tot)
print("non-last lines that are a gate/tool call (python3/scripts/make/sw):", len(calls))
for c in calls: print("  ", c)

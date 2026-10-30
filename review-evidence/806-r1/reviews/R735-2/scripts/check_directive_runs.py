#!/usr/bin/env python3
"""Check published directive-run receipts against the repository's own recipe and gate parsers.
usage: check_directive_runs.py <repo> <directives-receipt-dir>"""
import importlib.util, pathlib, re, sys
repo, d = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(path.parent)); spec.loader.exec_module(m); return m
base = load("baseline", repo / "syn/ooc/pp_baseline.py")
gate = load("gate", repo / "syn/ooc/pp_resource_gate.py")
tail_suffix = base.REPORTS + base.PP_REPORTS + base.SCOPE_TIMING + "\nquit\n"
figs = (d / "directive-figures.txt").read_text()
ok = True
for name in ("AltSpreadLogic_high", "ExtraTimingOpt"):
    t = (d / name / "baseline_implementation.tcl").read_text()
    lines = t.splitlines()
    pd = [l for l in lines if l.startswith("place_design")]
    r1 = lines[0] == "set_param general.maxThreads 32"
    r2 = lines[1].startswith("open_checkpoint {") and lines[1].endswith("/gateware/alinx_ax7101_synth.dcp}")
    r3 = t.endswith(tail_suffix)
    r4 = pd == [f"place_design -directive {name}"]
    u = gate.utilization((d / name / "baseline_utilization.rpt").read_text(), "route")
    sec = figs.split(f"## {name}\n", 1)[1].split("\n## ", 1)[0]
    stated = dict(re.findall(r"(\w+) ([\d.]+)", sec.splitlines()[0].split(":", 1)[1]))
    r5 = all(float(stated[k]) == float(v) for k, v in u.items())
    print(name, "maxThreads", r1, "opens synth dcp", r2, "recipe report suffix", r3, "single place directive", r4, pd,
          "utilization parsed", u, "equals stated", r5)
    ok &= r1 and r2 and r3 and r4 and r5
sys.exit(0 if ok else 1)

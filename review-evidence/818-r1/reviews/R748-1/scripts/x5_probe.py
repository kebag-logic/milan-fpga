#!/usr/bin/env python3
"""F3: a timing summary below the floor beside corner reports all above it (corners of another run).

The head refuses (2). A gate whose corner agreement is checked one way only (the corners' worst below the summary)
passes it, and the self-test does not notice that mutant. usage: x5_probe.py <clone> <packet>
"""
import shutil, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
clone, packet = map(Path, sys.argv[1:3])
probes = packet / "scratch/probes"; out = packet / "receipts/finding-probes"
spec = __import__("importlib.util").util
s = spec.spec_from_file_location("rp_helpers", Path(__file__).parent / "route_probes.py")
src = (Path(__file__).parent / "route_probes.py").read_text()
helpers = src.split("results = []")[0].split("GATE, SCRATCH")[0]  # imports and constants
ns = {}
exec(compile(src.split("S, A, E = SUBS")[0].replace("GATE, SCRATCH, DEV, CTRL, OUT = map(Path, sys.argv[1:6])",
     f"GATE, SCRATCH, DEV, CTRL, OUT = Path('{clone}/syn/ooc/pp_resource_gate.py'), Path('{probes}'), "
     f"Path('$VALIDATION_STORAGE/scratch/814-a703/viv-dev/w1'), Path('$VALIDATION_STORAGE/scratch/814-a703b/w-c1'), Path('{out}')"),
     "route_probes", "exec"), ns)
r = ns["copy"](ns["DEV"], "summary-below-corners")
for sub in ns["SUBS"]:
    ns["summary"](r / sub / "baseline_timing.rpt", 0, "0.010")
mut = packet / "scratch/x5"; shutil.rmtree(mut, ignore_errors=True); mut.mkdir()
for f in ("pp_resource_gate.py", "pp_baseline_rank.py", "pp_placement.py"):
    shutil.copy2(clone / "syn/ooc" / f, mut / f)
g = mut / "pp_resource_gate.py"
t = g.read_text(); old = "        if worst != figures[figure]:\n"; assert t.count(old) == 1
g.write_text(t.replace(old, "        if worst < figures[figure]:\n"))
args = ["check", str(r / ns["SUBS"][0]), "--endpoint", "route-1x1", "--baseline", str(clone / "syn/ooc/pp_resource_baseline.json"),
        "--comparison", str(r / ns["SUBS"][1]), "--comparison", str(r / ns["SUBS"][2])]
lines = []
for label, gate in (("head", clone / "syn/ooc/pp_resource_gate.py"), ("one-way mutant", g)):
    p = subprocess.run([sys.executable, "-B", str(gate), *args], capture_output=True, text=True)
    (out / f"F3-{label.replace(' ', '-')}.log").write_text(p.stdout + p.stderr + f"\nrc={p.returncode}\n")
    lines.append(f"F3 {label}: rc={p.returncode} {[l for l in p.stdout.splitlines() if l.startswith(('NOT COMPARABLE', 'WNS_ns', 'RESULT'))]}")
print("\n".join(lines)); (out / "F3.txt").write_text("\n".join(lines) + "\n")

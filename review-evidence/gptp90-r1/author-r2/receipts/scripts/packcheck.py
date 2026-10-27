"""For every generator control of the lane's mutation arm, try its shipping
and p1-255 images. usage: packcheck.py <lane>"""
import subprocess, sys, tempfile
from pathlib import Path
lane = Path(sys.argv[1])
sys.path.insert(0, str(lane / "tb/verilator/engine")); sys.path.insert(0, str(lane / "tb/verilator"))
import mutants
gen = (lane / "hdl" / mutants.GENERATOR).read_text()
bad = 0
with tempfile.TemporaryDirectory(dir="<scratch>/tmp") as td:
    for name, f, pat, rep, _ in mutants.MUTATIONS:
        if f != mutants.GENERATOR: continue
        g = Path(td) / "g.py"; g.write_text(gen.replace(pat, rep))
        for extra in ([], ["--p1", "255"]):
            r = subprocess.run([sys.executable, str(g), *mutants.GENARGS, *extra, "-o", str(Path(td) / "x.hex")],
                               capture_output=True, text=True)
            if r.returncode:
                bad += 1; print("REFUSED", name, extra, (r.stderr.strip().splitlines() or [""])[-1])
print("refused:", bad)

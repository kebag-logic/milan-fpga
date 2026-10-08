#!/usr/bin/env python3
"""Create a disposable 16-controller stimulus sweep against unchanged production RTL."""
import pathlib, subprocess, sys
packet=pathlib.Path(__file__).resolve().parents[1]; root=pathlib.Path(sys.argv[1]).resolve()
dest=packet/"scratch/robust"
subprocess.run(["git","clone","--quiet","--shared","--no-checkout",str(root),str(dest)],check=True)
subprocess.run(["git","-C",str(dest),"checkout","--quiet","--detach","f3fef22448ce4f9bed8fd249a21a5d472148bd3d"],check=True)
f=dest/"tb/aecp_notify/sim_main.cpp"; src=f.read_text()
start=src.index("void Harness::cancel_collision() {"); end=src.index("// ---- IX:",start)
src=src[:start]+(packet/"scripts/robust_probe.cpp").read_text()+"\n"+src[end:]
src=src.replace("static constexpr uint8_t N_CTRL = 2;","static constexpr uint8_t N_CTRL = 16;")
f.write_text(src)
m=dest/"tb/aecp_notify/Makefile";m.write_text(m.read_text().replace("-GN_CTRL_P=2", "-GN_CTRL_P=16"))
print("Prepared",dest)

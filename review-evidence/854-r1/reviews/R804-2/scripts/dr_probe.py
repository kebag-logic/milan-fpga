#!/usr/bin/env python3
"""Disposable [DR] probe: build the pp_shadow base leg with an optional plant in a
private copy of KL_pp_shadow.sv and run --drops-only.
Usage: dr_probe.py <repo> <workdir> <label> <RXFILT 0|1> [<old-text-file> <new-text-file>]
Never edits the repository; prints the [DR] lines and the verdict, exits with the sim rc."""
import os, pathlib, subprocess, sys
repo, work, label, rxfilt = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4]
here = repo / "tb/verilator/pp_shadow"; shadow = (repo / "hdl/milan/KL_pp_shadow.sv").resolve()
env = {k: v for k, v in os.environ.items() if k not in ("MAKEFLAGS", "MFLAGS")}
srcs = [(here / p).resolve() for p in subprocess.run(["make", "-s", "--no-print-directory", "-C", "../milan_dp", "print-srcs"],
        cwd=here, check=True, capture_output=True, text=True, env=env).stdout.split()]
d = work / label; d.mkdir(parents=True, exist_ok=False)
cmd = ["make", "--no-print-directory", "build-base", f"BUILD_DIR={d/'obj'}", f"RXFILT={rxfilt}"]
if len(sys.argv) > 5:
    old, new = (pathlib.Path(p).read_text() for p in sys.argv[5:7]); text = shadow.read_text()
    assert text.count(old) == 1, "anchor not unique"
    m = d / "hdl" / "KL_pp_shadow.sv"; m.parent.mkdir(); m.write_text(text.replace(old, new))
    cmd.append("DP_SRCS=" + " ".join(str(m if s == shadow else s) for s in srcs))
log = d / "build.log"
with log.open("w") as f:
    b = subprocess.run(cmd, cwd=here, stdout=f, stderr=subprocess.STDOUT, env=env)
if b.returncode:
    print(f"{label}: BUILD FAILED rc={b.returncode}"); sys.exit(2)
r = subprocess.run([str(d / "obj" / "Vpp_shadow_sim"), "--drops-only"], cwd=here, capture_output=True, text=True)
for line in r.stdout.splitlines():
    s = line.strip()
    if s.startswith(("DR ", "[DR]", "[FAIL]", "RESULT", "pp_shadow:")):
        print(f"{label}: {s}")
print(f"{label}: sim rc={r.returncode}")
sys.exit(r.returncode)

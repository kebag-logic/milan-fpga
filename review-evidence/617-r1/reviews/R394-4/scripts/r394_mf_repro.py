#!/usr/bin/env python3
"""R394-3: build the capture_coherence datapath leg through the committed mutants.py build()
twice - with no MAKEFLAGS, and with MAKEFLAGS=w (what a recipe inherits when the suite is run as
`make -C <suite>` under GNU make 4.3, as scripts/run_all_suites.sh does on the hosted runner) -
and print whether it built and the first line of the nested source list make handed Verilator.

  python3 r394_mf_repro.py <suite-dir> <workdir>
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

suite = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
sys.argv = [str(suite / "mutants.py")]
spec.loader.exec_module(m)
for mf in ("", "w"):
    os.environ["MAKEFLAGS"] = mf
    if not mf:
        del os.environ["MAKEFLAGS"]
    tag = f"mf_{mf or 'none'}"
    (work / tag).mkdir(parents=True, exist_ok=True)
    src = work / tag / "milan_datapath.sv"
    src.write_text(m.LEGS["dp"][4].read_text())
    show = subprocess.run(["make", "-s", "-C", str(suite), "--eval",
                           "r394show: ; @echo 'DP_SRCS starts: $(wordlist 1,4,$(DP_SRCS))'", "r394show",
                           f"DP_SRC={src}"], capture_output=True, text=True, check=False)
    line = [ln for ln in show.stdout.splitlines() if ln.startswith("DP_SRCS starts")]
    exe = m.build("dp", src, work, tag)
    print(f"MAKEFLAGS={mf!r}: {line[0] if line else show.stdout[-200:]!r}")
    print(f"MAKEFLAGS={mf!r}: mutants.build('dp') -> {'built ' + exe.name if exe else 'None (the arm reports: did not compile)'}")

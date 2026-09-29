#!/usr/bin/env python3
"""Build the capture_coherence datapath leg through the suite's own mutants.build(),
under whatever MAKEFLAGS this process inherited (or the one given), and report:
the make on PATH, the MAKEFLAGS seen, the first words of the nested DP_SRCS, and
whether mutants.build('dp') produced the harness.

  python3 mf_repro.py <suite-dir> <workdir> [inherit|none|w]
"""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

suite = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
mode = sys.argv[3] if len(sys.argv) > 3 else "inherit"
if mode == "none":
    os.environ.pop("MAKEFLAGS", None)
elif mode == "w":
    os.environ["MAKEFLAGS"] = "w"
spec = importlib.util.spec_from_file_location("cc_mutants", suite / "mutants.py")
m = importlib.util.module_from_spec(spec)
sys.argv = [str(suite / "mutants.py")]
spec.loader.exec_module(m)
mk = subprocess.run(["make", "--version"], capture_output=True, text=True, check=False).stdout.splitlines()[0]
tag = f"mf_{mode}"
(work / tag).mkdir(parents=True, exist_ok=True)
src = work / tag / "milan_datapath.sv"
src.write_text(m.LEGS["dp"][4].read_text())
show = subprocess.run(["make", "-s", "-C", str(suite), "--eval",
                       "a434show: ; @echo 'DP_SRCS starts: $(wordlist 1,4,$(DP_SRCS))'", "a434show",
                       f"DP_SRC={src}"], capture_output=True, text=True, check=False)
line = [ln for ln in show.stdout.splitlines() if ln.startswith("DP_SRCS starts")]
print(f"make on PATH: {mk}")
print(f"MAKEFLAGS seen by this process: {os.environ.get('MAKEFLAGS', '<unset>')!r}")
print(f"nested list: {line[0] if line else show.stdout[-300:]!r}")
got = m.build("dp", src, work, tag)
exe = got[0] if isinstance(got, tuple) else got
print(f"mutants.build('dp') -> {'built ' + exe.name if exe else 'no harness (the arm reports: did not compile)'}")

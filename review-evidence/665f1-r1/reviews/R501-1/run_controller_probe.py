#!/usr/bin/env python3
"""Link the unchanged port with one stalled CSR status input."""
from pathlib import Path
import subprocess
import sys
repo = Path(sys.argv[1]).resolve()
out = Path(__file__).resolve().parent
work = out / "scratch" / "probes"
tree = repo / "sw/firmware/ctrl_nvm"
cmd = ["gcc", "-std=c11", "-O1", "-Wall", "-Wextra", "-Werror", "-I"+str(work / "gen"),
       "-I"+str(tree / "host/stubs"), "-I"+str(tree / "test"),
       str(tree / "plat/nvm_flash_litespi.c"), str(tree / "host/nvm_fmodel.c"),
       str(tree / "host/litespi_model.c"), str(out / "probe_controller.c"),
       "-Wl,--wrap=litespi_model_status", "-o", str(work / "probe_controller")]
subprocess.run(cmd, check=True, timeout=60)
for mode, value in [("TX never ready", "0"), ("RX never ready", "1"), ("RX never drains", "3")]:
    try:
        r = subprocess.run([str(work / "probe_controller"), value], capture_output=True, text=True, timeout=1, check=False)
    except subprocess.TimeoutExpired as e:
        print(mode, ": no return within 1 second; subprocess terminated")
        print(e.stdout.decode() if isinstance(e.stdout, bytes) else e.stdout)
    else:
        print(mode, ": unexpectedly returned", r.returncode, r.stdout)
        sys.exit(1)
print("REPRODUCED all three unbounded CSR waits")

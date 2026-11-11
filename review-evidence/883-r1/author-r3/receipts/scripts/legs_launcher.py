#!/usr/bin/env python3
"""legs_launcher.py <clone> <root> <chain> <cpus 8|4> <suite> ...: run each suite's `make` in <clone> as its own unit,
milan-883-a768-leg-<suite>, one after another, with the full sweep's environment and per-suite wall clock
(scripts/run_all_suites.sh suite_timeout). Before each suite it asks cpu_ranges.py pick for a free 8-CPU range and
waits for MemAvailable above 20 GB; a 4-CPU suite takes the first four CPUs of that range. Log and exit status go to
<root>/logs/<suite>.log and .rc; each start goes to <root>/launch.tsv. Reserves nothing while it waits: a range is
booked by the unit that runs on it, and no unit is started before the previous one has written its status."""
import subprocess
import sys
import time
from pathlib import Path

M = "<mgmt>/2026-09-23"
clone, root, chain, width, suites = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5:]
TIMEOUT = {"capture_coherence": 2400, "milan_dp": 4800, "milan_dp_mclk": 3600}
ENV = ("PATH=<tools>/pinned-verilator-5.050:<tools>/sv2v-v0.0.12:<scratch-root>/a662/make43/bin:"
       "<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       "VERILATOR=<tools>/pinned-verilator-5.050/verilator",
       "TSN_GEN_ROOT=<mgmt>/tools/tsn-gen-deca300c",
       "PKG_CONFIG_PATH=<tools>/gtest-1.14.0/lib/pkgconfig",
       "LD_LIBRARY_PATH=<tools>/gtest-1.14.0/lib",
       f"TMPDIR=<scratch>/tmp-legs/{chain}",
       "MAKEFLAGS=-j4 --no-print-directory", "PYTHONHASHSEED=0")


def mem_gb() -> float:
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemAvailable"):
            return int(line.split()[1]) / 1048576
    return 0.0


def note(text: str) -> None:
    with open(root / "launch.tsv", "a") as tsv:
        tsv.write(f"{chain}\t{text}\t{time.strftime('%FT%T%z')}\n")


(root / "logs").mkdir(parents=True, exist_ok=True)
Path(f"<scratch>/tmp-legs/{chain}").mkdir(parents=True, exist_ok=True)
deadline = time.time() + 8 * 3600
for suite in suites:
    log, rc = root / "logs" / f"{suite}.log", root / "logs" / f"{suite}.log.rc"
    rc.unlink(missing_ok=True)
    while time.time() < deadline:
        got = subprocess.run(["python3", f"{M}/cpu_ranges.py", "pick"], capture_output=True, text=True)
        if got.returncode == 0 and got.stdout.strip() and mem_gb() > 20:
            first, last = (int(x) for x in got.stdout.strip().split("-"))
            cpus = f"{first}-{first + 3}" if width == 4 else f"{first}-{last}"
            shell = (f"cd {clone} && env {' '.join(repr(e) for e in ENV)} timeout {TIMEOUT.get(suite, 1800)} "
                     f"make -C tb/verilator/{suite} > {log} 2>&1; echo $? > {rc}")
            subprocess.run(["systemd-run", "--user", "--quiet", "--collect", f"--unit=milan-883-a768-leg-{suite}",
                            "-p", "MemoryMax=10G", "-p", f"CPUAffinity={cpus}", "bash", "-c", shell], check=True)
            note(f"{suite}\t{cpus}")
            break
        time.sleep(20)
    else:
        note(f"{suite}\tTIMEOUT")
        sys.exit(1)
    while not rc.exists() and time.time() < deadline:
        time.sleep(20)
    note(f"{suite}\tdone rc={rc.read_text().strip() if rc.exists() else 'none'}")
note("CHAIN-DONE")

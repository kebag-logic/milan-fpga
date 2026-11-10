"""unit_job.py SECONDS WF JOB K: one replay instance in its own unit (MemoryMax 10G) on a dedicated 8-CPU range, the
moment cpu_ranges.py pick returns one, pick and launch back to back, as tick() launches; the instance must already
be claimed (claims/<name>) so no local runner takes it."""
import hashlib
import subprocess
import sys
import time
from pathlib import Path

secs, wf, job, k = float(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4]
H = "2128daad26b932feeed1ef2bde8f2774e8a51a31"
name = f"{wf}__{job}" + (f"__{k}" if job == "verilator-shards" or job == "yosys-shards" else "")
unit = "milan-a757c-ci-" + hashlib.sha1(name.encode()).hexdigest()[:10]
T = Path(__file__).resolve().parent
end = time.time() + secs
while time.time() < end:
    cpus = subprocess.run([sys.executable, "$MANAGEMENT/2026-09-23/cpu_ranges.py", "pick"],
                          capture_output=True, text=True).stdout.strip()
    if cpus:
        subprocess.run(["systemd-run", "--user", f"--unit={unit}", "--collect", "--property=MemoryMax=10G",
                        "--setenv=HOME=$WORKSPACE_HOME", "/usr/bin/taskset", "-c", cpus, "/usr/bin/python3",
                        str(T / "ci_replay.py"), "job", H, wf, job, k], check=True)
        print(time.strftime("%T"), f"{name} launched as {unit} on {cpus}", flush=True)
        break
    time.sleep(15)
else:
    print(time.strftime("%T"), f"{name}: no free range in {secs} s")

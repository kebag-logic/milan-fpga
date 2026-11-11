#!/usr/bin/env python3
"""sweep-watch.py: launch the FULL sweep's 4 shards (sweep-shard.py, which launches each exactly as native-shards.py
does), each on the range `cpu_ranges.py pick` gives as ranges free up (native-shards.py takes all four ranges at once,
and the booked host has none free); the shard holding capture_coherence (2 of 4) on the range's
first 4 CPUs only; the next shard only while MemAvailable is over 30 GB, else only once no shard runs (serially)."""
import subprocess, sys, time
PICK = ["python3", "<home>/milan-fpga-management/2026-09-23/cpu_ranges.py", "pick"]
S = "<scratch>"
def mem_gb():
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 1e6
    return 0.0
def running():
    out = subprocess.run(["systemctl", "--user", "list-units", "--plain", "--no-legend", "milan-a760d-shard*"],
                         capture_output=True, text=True).stdout
    return len([l for l in out.splitlines() if " active " in f" {l} "])
k = int(sys.argv[1]) if len(sys.argv) > 1 else 0
while k < 4:
    pick = subprocess.run(PICK, capture_output=True, text=True)
    rng = pick.stdout.strip() if pick.returncode == 0 else ""
    print(time.strftime("%T"), "pick", rng or "(none free)", f"MemAvailable {mem_gb():.1f} GB, shards running {running()}",
          flush=True)
    if rng and (mem_gb() > 30 or running() == 0):
        a = int(rng.split("-")[0])
        cpus = f"{a}-{a + 3}" if k == 2 else rng
        print("launching shard", k, "on", cpus, flush=True)
        subprocess.run(["python3", f"{S}/tools/sweep-shard.py", str(k), cpus], check=True)
        k += 1
        time.sleep(20)
        continue
    time.sleep(15)
print("every shard launched", flush=True)

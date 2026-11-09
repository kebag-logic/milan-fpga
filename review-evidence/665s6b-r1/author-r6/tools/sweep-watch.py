#!/usr/bin/env python3
"""sweep-watch.py <head>: launch the FULL sweep's 4 shards (sweep-shard.py), each on the next free aligned 8-CPU range,
the replay's tick driver stopped while a range is picked and started again after; the next shard only while
MemAvailable is over 30 GB, else only once no shard runs (serially)."""
import subprocess, sys, time
sys.path.insert(0, "$HOME/milan-fpga-management/2026-09-23")
import cpu_ranges
head = sys.argv[1]
S = "$VALIDATION_STORAGE/scratch/a746f"
ENV = {"UNIT_PATH": "$HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       "PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "$HOME",
       "XDG_RUNTIME_DIR": "/run/user/1000", "DBUS_SESSION_BUS_ADDRESS": "unix:path=/run/user/1000/bus"}
def mem_gb():
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 1e6
    return 0.0
def free8():
    taken = cpu_ranges.busy()
    return [f"{a}-{a + 7}" for a in range(0, cpu_ranges.NCPU, 8) if not set(range(a, a + 8)) & taken]
def running():
    out = subprocess.run(["systemctl", "--user", "list-units", "--plain", "--no-legend", "milan-a746f-shard*"],
                         capture_output=True, text=True).stdout
    return len([l for l in out.splitlines() if " active " in f" {l} "])
k = 0
while k < 4:
    free = free8()
    print(time.strftime("%T"), "free 8-ranges", free, f"MemAvailable {mem_gb():.1f} GB, shards running {running()}",
          flush=True)
    if free and (mem_gb() > 30 or running() == 0):
        subprocess.run(["systemctl", "--user", "stop", "milan-a746f-ci-drive"])
        free = free8()
        if free:
            print("launching shard", k, "on", free[-1], flush=True)
            subprocess.run(["python3", f"{S}/bin/sweep-shard.py", str(k), free[-1]], check=True)
            k += 1
            time.sleep(15)
        subprocess.run(["bash", f"{S}/bin/unit.sh", "ci-drive", "8-15", f"{S}/logs/ci-drive.log", S, "bash",
                        "bin/ci-drive.sh", head, "10"], env=ENV)
        continue
    time.sleep(60)
print("every shard launched", flush=True)

#!/usr/bin/env python3
"""sweep-watch.py <head>: launch the FULL sweep's 4 shards (sweep-shard.py), each on the next free aligned 8-CPU range
as ranges free up; the shard holding capture_coherence (2 of 4) on the range's first 4 CPUs only; the next shard only
while MemAvailable is over 30 GB, else only once no shard runs (serially)."""
import subprocess, sys, time
sys.path.insert(0, "$MANAGEMENT/2026-09-23")
import cpu_ranges
head = sys.argv[1]
S = "/data-2/milan/tmp/665s7-a757b"
ENV = {"UNIT_PATH": "$WORKSPACE_HOME/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       "PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": "$WORKSPACE_HOME",
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
    out = subprocess.run(["systemctl", "--user", "list-units", "--plain", "--no-legend", "milan-a757b-shard*"],
                         capture_output=True, text=True).stdout
    return len([l for l in out.splitlines() if " active " in f" {l} "])
k = 0
while k < 4:
    free = free8()
    print(time.strftime("%T"), "free 8-ranges", free, f"MemAvailable {mem_gb():.1f} GB, shards running {running()}",
          flush=True)
    if free and (mem_gb() > 30 or running() == 0):
        a = int(free[-1].split("-")[0])
        cpus = f"{a}-{a + 3}" if k == 2 else free[-1]
        print("launching shard", k, "on", cpus, flush=True)
        subprocess.run(["python3", f"{S}/bin/sweep-shard.py", str(k), cpus], check=True)
        k += 1
        time.sleep(15)
        continue
    time.sleep(60)
print("every shard launched", flush=True)

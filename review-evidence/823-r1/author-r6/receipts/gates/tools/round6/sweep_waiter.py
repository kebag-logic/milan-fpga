"""Book one cpu_ranges.py pick per sweep shard as ranges free (polling every 2 s), each held by a holder unit (a
sleep under taskset, the booking cpu_ranges.py reads), then start the four shard units with native-shards.py once
all four are held and MemAvailable is above 30 GB; shard 2, which holds capture_coherence, runs on 4 CPUs of its
range. The holders stop once the shard units run on their ranges."""
import subprocess, time
S = "<scratch>"
PICK = "<management>/2026-09-23/cpu_ranges.py"
SHARDS = "<management>/2026-09-23/native-shards.py"


def log(*a):
    print(time.strftime("%T"), *a, flush=True)


def mem_avail_gb():
    for line in open("/proc/meminfo"):
        if line.startswith("MemAvailable:"):
            return int(line.split()[1]) / 1e6
    return 0.0


held = []
while len(held) < 4:
    r = subprocess.run(["python3", PICK, "pick"], capture_output=True, text=True)
    rng = r.stdout.strip().splitlines()[-1] if r.returncode == 0 and r.stdout.strip() else ""
    if rng and "-" in rng:
        name = f"milan-823-a753f-hold{len(held)}"
        subprocess.run(["systemd-run", "--user", f"--unit={name}", "--collect", "/usr/bin/taskset", "-c", rng,
                        "/usr/bin/sleep", "infinity"], check=True, capture_output=True)
        held.append(rng)
        log("held", name, rng)
        continue
    time.sleep(2)
while mem_avail_gb() < 30:
    log(f"MemAvailable {mem_avail_gb():.1f} GB, waiting")
    time.sleep(30)
a, b = held[2].split("-")
cpus = [held[0], held[1], f"{a}-{int(a) + 3}", held[3]]
log("sweep on", cpus, f"MemAvailable {mem_avail_gb():.1f} GB")
out = subprocess.run(["python3", SHARDS, "823-a753f-sweep", f"{S}/sweep-spec.json", f"{S}/sweep2", "4", *cpus],
                     capture_output=True, text=True)
log("native-shards rc", out.returncode, out.stdout.strip(), out.stderr.strip()[-2000:])
time.sleep(20)
for k in range(4):
    subprocess.run(["systemctl", "--user", "stop", f"milan-823-a753f-hold{k}"])
log("holders stopped")

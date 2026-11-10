"""Book CPU ranges for this round's pending jobs as they free, polling every 5 s, each free range held by a holder
unit (a sleep under taskset, the booking cpu_ranges.py reads) until its job's unit runs on it.

The sweep takes four aligned 4-CPU ranges (one shard each, capture_coherence's shard on 4 CPUs): native-shards.py
starts them once four are held, then the sweep's holders stop. Then drivers A and B (firmware jobs; docs and the small
rtl-fast jobs), one aligned 4-CPU range each, and driver C (elaborate and the rtl yosys jobs) and the twin, one aligned
8-CPU range each."""
import subprocess, sys, time
sys.path.insert(0, "<management>/2026-09-23")
import cpu_ranges

H = "b6a60fbdff92bf89552f1634e6890bd27d41b485"
S = "<scratch>"; T = f"{S}/gates/tools"
ENV = ["--setenv=HOME=<home>", "--setenv=PATH=<home>/.local/bin:/usr/local/bin:/usr/bin:/bin"]
held = {}
serial = iter(range(100))


def log(*a):
    print(time.strftime("%T"), *a, flush=True)


def unit(name, cpus, cmd, props=("--property=MemoryMax=10G",)):
    subprocess.run(["systemd-run", "--user", f"--unit=milan-823-a753e-{name}", "--collect", *props, *ENV,
                    "/usr/bin/taskset", "-c", cpus, "/bin/bash", "-c", cmd], check=True)
    log(name, "on", cpus)


def take(width):
    """The next free aligned range of this width, held by a holder unit; blocks until one frees."""
    while True:
        free = set(range(cpu_ranges.NCPU)) - cpu_ranges.busy()
        for a in range(cpu_ranges.NCPU - width, -1, -width):
            if set(range(a, a + width)) <= free:
                r, n = f"{a}-{a + width - 1}", next(serial)
                unit(f"hold{n}", r, "sleep infinity", props=())
                held[r] = f"milan-823-a753e-hold{n}"
                return r
        time.sleep(5)


def release(r):
    subprocess.run(["systemctl", "--user", "stop", held.pop(r)], check=True)


sweep = [take(4) for _ in range(4)]
log("sweep on", sweep)
subprocess.run(["python3", "<management>/2026-09-23/native-shards.py", "823-a753e-sweep",
                f"{S}/sweep-spec.json", f"{S}/sweep", "4", *sweep], check=True)
for r in sweep:
    release(r)
jobs = [("gates-a", 4, f"bash {T}/drive.sh {H} {S}/gates/final {T}/r4-a.txt > {S}/drive-a.log 2>&1"),
        ("gates-b", 4, f"bash {T}/drive.sh {H} {S}/gates/final {T}/r4-b.txt > {S}/drive-b.log 2>&1"),
        ("gates-c", 8, f"bash {T}/drive.sh {H} {S}/gates/final {T}/r4-c.txt > {S}/drive-c.log 2>&1"),
        ("twin", 8, f"bash {T}/extra_gate.sh {H} twin bash -c 'make -j8 -C tb/verilator/milan_dp twin && "
                    f"make -j8 -C tb/verilator/milan_dp twin-plants'")]
for name, width, cmd in jobs:
    r = take(width)
    unit(name, r, cmd)
    time.sleep(3)
    release(r)
log("all launched")

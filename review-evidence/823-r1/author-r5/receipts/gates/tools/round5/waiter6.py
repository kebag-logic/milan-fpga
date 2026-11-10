"""Final run on the head named below: book CPU ranges as they free, polling every 5 s, each held by a holder unit
(a sleep under taskset, the booking cpu_ranges.py reads) until its job's unit runs on it. Drivers A (firmware jobs)
and B (docs and the small rtl-fast jobs) take four CPUs each; driver C (elaborate and the rtl yosys jobs) takes eight
contiguous CPUs, or four once it has waited 15 minutes. The sweep is not run again (see HANDOFF)."""
import subprocess, sys, time
sys.path.insert(0, "<management>/2026-09-23")
import cpu_ranges

H = sys.argv[1]
S = "<scratch>"; T = f"{S}/gates/tools"
ENV = ["--setenv=HOME=<home>", "--setenv=PATH=<home>/.local/bin:/usr/local/bin:/usr/bin:/bin"]
serial = iter(range(100))


def log(*a):
    print(time.strftime("%T"), *a, flush=True)


def unit(name, cpus, cmd, props=("--property=MemoryMax=10G",)):
    subprocess.run(["systemd-run", "--user", f"--unit=milan-823-a753e-{name}", "--collect", *props, *ENV,
                    "/usr/bin/taskset", "-c", cpus, "/bin/bash", "-c", cmd], check=True)
    log(name, "on", cpus)


def take(width, fallback=None, after_s=None):
    """The next free range: `width` contiguous CPUs starting on a multiple of 4, held by a holder unit; after
    `after_s` seconds, `fallback` CPUs instead."""
    start = time.monotonic()
    while True:
        w = fallback if after_s is not None and time.monotonic() - start > after_s else width
        free = set(range(cpu_ranges.NCPU)) - cpu_ranges.busy()
        for a in range(cpu_ranges.NCPU - w, -1, -4):
            if set(range(a, a + w)) <= free:
                r, n = f"{a}-{a + w - 1}", next(serial)
                unit(f"hold{n}", r, "sleep infinity", props=())
                return r, f"milan-823-a753e-hold{n}"
        time.sleep(5)


jobs = [("gates-a", (4,), f"bash {T}/drive.sh {H} {S}/gates/final {T}/r4-a.txt > {S}/drive-a.log 2>&1"),
        ("gates-b", (4,), f"bash {T}/drive.sh {H} {S}/gates/final {T}/r4-b.txt > {S}/drive-b.log 2>&1"),
        ("gates-c", (8, 4, 900), f"bash {T}/drive.sh {H} {S}/gates/final {T}/r4-c.txt > {S}/drive-c.log 2>&1")]
for name, want, cmd in jobs:
    r, holder = take(*want)
    unit(name, r, cmd)
    time.sleep(3)
    subprocess.run(["systemctl", "--user", "stop", holder], check=True)
log("all launched")

"""unit_waiter.py <name> <command>: poll cpu_ranges.py pick every 2 s (it hands out nothing while a release hold collects
CPUs); on a free range start gate unit milan-823-a753f-<name> (MemoryMax 10G, not niced) running <command> under
taskset on that range, or on its first 4 CPUs when <name> is `rerun` (capture_coherence: at most 4 CPUs)."""
import subprocess, sys, time
name, command = sys.argv[1], sys.argv[2]
PICK = "<management>/2026-09-23/cpu_ranges.py"
while True:
    r = subprocess.run(["python3", PICK, "pick"], capture_output=True, text=True)
    rng = r.stdout.strip().splitlines()[-1] if r.returncode == 0 and r.stdout.strip() else ""
    if "-" in rng:
        break
    time.sleep(2)
a, b = (int(x) for x in rng.split("-"))
cpus = f"{a}-{a + 3}" if name == "rerun" else rng
print(time.strftime("%T"), name, "range", rng, "cpus", cpus, flush=True)
out = subprocess.run(["systemd-run", "--user", f"--unit=milan-823-a753f-{name}", "--collect", "--property=MemoryMax=10G",
                      "--setenv=HOME=<home>", "--setenv=PATH=/usr/local/bin:/usr/bin:/bin",
                      "/usr/bin/taskset", "-c", cpus, "/bin/bash", "-c", command], capture_output=True, text=True)
print(time.strftime("%T"), "launched rc", out.returncode, out.stderr.strip(), flush=True)

"""Book CPU ranges for this round's pending jobs as they free, in order: the sweep (four shards on two 8-CPU
ranges, four CPUs each, or on four ranges when four are free), then driver C, the F1 self-test and the twin."""
import re, subprocess, time
H = "30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14"
S = "<scratch>"; T = f"{S}/gates/tools"
PICK = "<management>/2026-09-23/cpu_ranges.py"


def free8():
    out = subprocess.run(["python3", PICK, "show"], capture_output=True, text=True).stdout.splitlines()[-1]
    f16 = re.findall(r"'(\d+)-(\d+)'", out.split("free16")[1].split("free12")[0])
    h8 = re.findall(r"'(\d+)-(\d+)'", out.split("half8")[1])
    ranges = [(int(a), int(a) + 7) for a, _ in h8] + [(int(a) + k, int(a) + k + 7) for a, _ in f16 for k in (0, 8)]
    return sorted(set(ranges))


def unit(name, cpus, cmd):
    subprocess.run(["systemd-run", "--user", f"--unit=milan-823-a753d-{name}", "--collect", "--property=MemoryMax=10G",
                    "--setenv=HOME=<home>", "--setenv=PATH=<home>/.local/bin:/usr/local/bin:/usr/bin:/bin",
                    "/usr/bin/taskset", "-c", cpus, "/bin/bash", "-c", cmd], check=True)
    print(time.strftime("%T"), name, "on", cpus, flush=True)


while len(free8()) < 2:
    time.sleep(30)
r = free8()
if len(r) >= 4:
    cpus = [f"{a}-{b}" for a, b in r[:4]]
    cpus[2] = f"{r[2][0]}-{r[2][0] + 3}"           # shard 2 holds capture_coherence: four CPUs
else:
    (a0, _), (a1, _) = r[:2]
    cpus = [f"{a0}-{a0 + 3}", f"{a0 + 4}-{a0 + 7}", f"{a1}-{a1 + 3}", f"{a1 + 4}-{a1 + 7}"]
print(time.strftime("%T"), "sweep on", cpus, flush=True)
subprocess.run(["python3", "<management>/2026-09-23/native-shards.py", "823-a753d-sweep",
                f"{S}/sweep-spec.json", f"{S}/sweep", "4", *cpus], check=True)
time.sleep(60)
jobs = [("gates-c", f"bash {T}/drive.sh {H} {S}/gates/final {T}/r4-c.txt > {S}/drive-c.log 2>&1"),
        ("ctrlnvm", f"bash {T}/extra_gate.sh {H} ctrl_nvm_selftest python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py "
                    f"--require-rv32 --self-test --jobs 8"),
        ("twin", f"bash {T}/extra_gate.sh {H} twin bash -c 'make -j8 -C tb/verilator/milan_dp twin && "
                 f"make -j8 -C tb/verilator/milan_dp twin-plants'")]
for name, cmd in jobs:
    while not free8():
        time.sleep(30)
    a, b = free8()[0]
    unit(name, f"{a}-{b}", cmd)
    time.sleep(60)
print(time.strftime("%T"), "all launched", flush=True)

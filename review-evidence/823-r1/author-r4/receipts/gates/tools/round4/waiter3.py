"""Book CPU ranges for this round's pending jobs as they free, polling every 5 s. The sweep needs two 8-CPU ranges at
once: each free range is booked with a holder unit (a sleep under taskset, the booking cpu_ranges.py reads) until
two are held, native-shards.py starts the four shards on them, four CPUs each, and then the holders stop. Then driver
C, the F1 self-test and the twin, each on the next free range."""
import re, subprocess, time
H = "30ca4b216e6f7dd386e1d0a0015b0b23b4e08c14"
S = "<scratch>"; T = f"{S}/gates/tools"
PICK = "<management>/2026-09-23/cpu_ranges.py"
ENV = ["--setenv=HOME=<home>", "--setenv=PATH=<home>/.local/bin:/usr/local/bin:/usr/bin:/bin"]


def free8():
    out = subprocess.run(["python3", PICK, "show"], capture_output=True, text=True).stdout.splitlines()[-1]
    f16 = re.findall(r"'(\d+)-(\d+)'", out.split("free16")[1].split("free12")[0])
    h8 = re.findall(r"'(\d+)-(\d+)'", out.split("half8")[1])
    return sorted({(int(a), int(a) + 7) for a, _ in h8} | {(int(a) + k, int(a) + k + 7) for a, _ in f16 for k in (0, 8)})


def unit(name, cpus, cmd, props=("--property=MemoryMax=10G",)):
    subprocess.run(["systemd-run", "--user", f"--unit=milan-823-a753d-{name}", "--collect", *props, *ENV,
                    "/usr/bin/taskset", "-c", cpus, "/bin/bash", "-c", cmd], check=True)
    print(time.strftime("%T"), name, "on", cpus, flush=True)


def next_range():
    while True:
        r = free8()
        if r:
            return r[0]
        time.sleep(5)


held = []
while len(held) < 2:
    a, b = next_range()
    unit(f"hold{len(held)}", f"{a}-{b}", "sleep infinity", props=())
    held.append(a)
a0, a1 = held
cpus = [f"{a0}-{a0 + 3}", f"{a0 + 4}-{a0 + 7}", f"{a1}-{a1 + 3}", f"{a1 + 4}-{a1 + 7}"]
print(time.strftime("%T"), "sweep on", cpus, flush=True)
# the holders keep the two ranges booked until every shard's unit runs on them
subprocess.run(["python3", "<management>/2026-09-23/native-shards.py", "823-a753d-sweep",
                f"{S}/sweep-spec.json", f"{S}/sweep", "4", *cpus], check=True)
for k in range(2):
    subprocess.run(["systemctl", "--user", "stop", f"milan-823-a753d-hold{k}"], check=True)
jobs = [("gates-c", f"bash {T}/drive.sh {H} {S}/gates/final {T}/r4-c.txt > {S}/drive-c.log 2>&1"),
        ("ctrlnvm", f"bash {T}/extra_gate.sh {H} ctrl_nvm_selftest python3 sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py "
                    f"--require-rv32 --self-test --jobs 8"),
        ("twin", f"bash {T}/extra_gate.sh {H} twin bash -c 'make -j8 -C tb/verilator/milan_dp twin && "
                 f"make -j8 -C tb/verilator/milan_dp twin-plants'")]
for name, cmd in jobs:
    time.sleep(20)
    a, b = next_range()
    unit(name, f"{a}-{b}", cmd)
print(time.strftime("%T"), "all launched", flush=True)

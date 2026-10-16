"""Lane B19: return the controller host's AVB NIC hardware clock to its found state (lane B1's
phc_restore.py with this lane's found readings): frequency offset 0 ppb, and the time back on the
trajectory it had against CLOCK_REALTIME before any run. Runs on the controller host under sudo; the
caller holds the bench lock. The NIC's timestamping is reset to its found tx_type 0 / rx_filter 0 separately."""
import re, subprocess
PC = "/tmp/a624/lptp/phc_ctl"
def run(*a):
    r = subprocess.run(["sudo", "-n", PC, "<host-iface>", *a], capture_output=True, text=True, timeout=20)
    print(r.stdout.strip()); assert r.returncode == 0, r.stderr
    return r.stdout
# Found readings (04:10Z, before any run; gm/host-original-state.txt): monotonic stamp, offset from CLOCK_REALTIME (ns)
M1, X1 = 516303.803, 20150276694
M2, X2 = 516323.850, 20151038282
rate = (X2 - X1) / (M2 - M1)          # ns per s under the found frequency
run("freq", "0.000000")
out = run("cmp")
m = float(re.search(r"phc_ctl\[([0-9.]+)\]", out)[1]); x = int(re.search(r"is (-?\d+)ns", out)[1])
target = X2 + rate * (m - M2)
d = (x - target) / 1e9
print(f"rate_ns_per_s={rate:.3f} now_offset={x} target_offset={target:.0f} adjust_s={d:.9f}")
run("adj", f"{d:.9f}")  # cmp prints CLOCK_REALTIME minus PHC, so a positive d advances the PHC
out = run("freq", "cmp")
m = float(re.findall(r"phc_ctl\[([0-9.]+)\]", out)[-1]); x = int(re.findall(r"is (-?\d+)ns", out)[-1])
print(f"residual_from_original_trajectory_ns={x - (X2 + rate * (m - M2)):.0f}")

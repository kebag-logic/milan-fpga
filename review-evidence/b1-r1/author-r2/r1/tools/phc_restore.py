import re, subprocess
PC = "/tmp/a438/lptp/phc_ctl"
def run(*a):
    r = subprocess.run(["sudo", "-n", PC, "<controller-host-if>", *a], capture_output=True, text=True, timeout=20)
    print(r.stdout.strip()); assert r.returncode == 0, r.stderr
    return r.stdout
# Original readings (06:03Z, before any ptp4l run): monotonic stamp, offset from CLOCK_REALTIME (ns)
M1, X1 = 83945.983, 1790532371571048304
M2, X2 = 83965.622, 1790532371571208886
rate = (X2 - X1) / (M2 - M1)          # ns per s under the original frequency
run("freq", "28062.347412")
out = run("cmp")
m = float(re.search(r"phc_ctl\[([0-9.]+)\]", out)[1]); x = int(re.search(r"is (-?\d+)ns", out)[1])
target = X2 + rate * (m - M2)
d = (x - target) / 1e9
print(f"rate_ns_per_s={rate:.3f} now_offset={x} target_offset={target:.0f} adjust_s={d:.9f}")
run("adj", f"{d:.9f}")
out = run("freq", "cmp")
m = float(re.search(r"offset from CLOCK_REALTIME.*", out) and re.findall(r"phc_ctl\[([0-9.]+)\]", out)[-1]); x = int(re.findall(r"is (-?\d+)ns", out)[-1])
print(f"residual_from_original_trajectory_ns={x - (X2 + rate * (m - M2)):.0f}")

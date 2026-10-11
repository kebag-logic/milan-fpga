#!/usr/bin/env python3
"""Plant faults in the MERGED milan_datapath.sv's MAAP wiring; require the MAAP datapath check to name them.

Usage: python3 -I datapath_wiring_probes.py <probe-checkout-at-head> <verilator> <jobs> [probe ...]

The checkout must be a disposable git checkout at the head under review. For each probe the
datapath source is replaced (anchor must occur exactly once), tb/verilator/maap's
integration-build target is built into a fresh directory, and maap_integration is run. A probe
is CAUGHT only when the build succeeds, the run exits 1 and the expected named check is among
the [FAIL] lines. A clean control runs first. The datapath file is restored with
`git checkout -- hdl/milan/milan_datapath.sv` after every probe and checked clean at the end.
"""
import subprocess, sys
from pathlib import Path

root, verilator, jobs = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3]
only = set(sys.argv[4:])  # optional probe names; the clean control always runs
DP = root / "hdl/milan/milan_datapath.sv"
SUITE = root / "tb/verilator/maap"
PROBES = (
    ("clean", None, None, None),
    ("w1_link_tied_high", ".port_operational_i (eff_link_w),", ".port_operational_i (1'b1),",
     "M5 datapath: link return starts four fresh PROBEs"),
    ("w2_clock_tied_zero", ".realtime_ns_i     (ptp_now_w[31:0]),", ".realtime_ns_i     (32'd0),",
     "M3 datapath: real-time clock changes probe intervals"),
    ("w3_mac_low_word_constant",
     ".count_i  (cfg_maap_count),\n"
     "    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],\n"
     "                     cfg_mac_addr[23:16], cfg_mac_addr[31:24],\n"
     "                     cfg_mac_addr[39:32], cfg_mac_addr[47:40]}),",
     ".count_i  (cfg_maap_count),\n"
     "    .station_mac_i ({cfg_mac_addr[7:0],   cfg_mac_addr[15:8],\n"
     "                     8'h00, 8'h00, 8'h00, 8'h00}),",
     "M4 datapath: programmed MAC changes probe intervals"),
)
git = lambda *a: subprocess.run(["git", "-C", str(root), *a], check=True, capture_output=True, text=True).stdout
original = DP.read_text()
escaped = 0
PROBES = tuple(p for p in PROBES if not only or p[0] == "clean" or p[0] in only)
for name, anchor, repl, check in PROBES:
    if anchor is not None:
        if original.count(anchor) != 1:
            print(f"[ANCHOR] {name}: anchor occurs {original.count(anchor)} times"); escaped += 1; continue
        DP.write_text(original.replace(anchor, repl))
    mdir = root / f"obj_probe_{name}"
    b = subprocess.run(["make", "-j8", "-s", "-C", str(SUITE), "integration-build", f"DP_MDIR={mdir}",
                        f"VERILATOR={verilator}", f"VERILATOR_JOBS={jobs}"], capture_output=True, text=True)
    git("checkout", "--", "hdl/milan/milan_datapath.sv")
    if b.returncode:
        print(f"[BUILD-FAIL] {name}\n{b.stdout[-1500:]}{b.stderr[-1500:]}"); escaped += 1; continue
    r = subprocess.run([str(mdir / "maap_integration")], cwd=mdir, capture_output=True, text=True)
    out = r.stdout + r.stderr
    fails = [l.strip() for l in out.splitlines() if "[FAIL]" in l]
    tally = [l.strip() for l in out.splitlines() if "checks" in l and "failures" in l]
    if check is None:
        ok = r.returncode == 0 and not fails
        print(f"[{'ok' if ok else 'BAD-CONTROL'}] {name}: rc={r.returncode} {tally}")
    else:
        ok = r.returncode == 1 and any(check in l for l in fails)
        print(f"[{'CAUGHT' if ok else 'ESCAPED'}] {name}: rc={r.returncode} {tally}")
        for l in fails: print(f"    {l}")
    escaped += not ok
print(f"datapath wiring probes: {len(PROBES) - escaped}/{len(PROBES)} as expected")
print("datapath file restored:", git("status", "--porcelain", "--", "hdl/milan/milan_datapath.sv") == "")
sys.exit(1 if escaped else 0)

#!/usr/bin/env python3
"""Independently parse the retained sweep reports: WNS/TNS/WHS/THS per seed and corner,
Ethernet crossing requirement/slack, interaction classification and log diagnostics.
Usage: parse_sweep_timing.py <work-root> ; exits 1 if any acceptance-4 check fails."""
import re, sys
from pathlib import Path
root = Path(sys.argv[1]); fail = []
def summary(text):
    m = re.search(r"Design Timing Summary.*?-{5,}.*?\n\s*-+.*?\n\s*([-\d.]+)\s+([-\d.]+)\s+\d+\s+\d+\s+([-\d.]+)\s+([-\d.]+)", text, re.S)
    return tuple(float(x) for x in m.groups())
for seed in ("asl", "eto", "eppo"):
    b = root / f"build_ax7101_{seed}_350af5dcf"
    log = (b / "gateware/vivado.log").read_text(errors="replace")
    diag = re.findall(r"^(?:CRITICAL WARNING|WARNING|ERROR):\s+\[(Vivado 12-4739|Designutils 20-1307|Vivado 12-5201)\]", log, re.M)
    cw = len(re.findall(r"^CRITICAL WARNING:", log, re.M))
    impl = summary(log)
    print(f"{seed}: impl-log WNS={impl[0]:+.3f} TNS={impl[1]:.3f} WHS={impl[2]:+.3f} THS={impl[3]:.3f} critical_warnings={cw} 12-4739/20-1307/12-5201={len(diag)}")
    if diag or impl[0] < 0.030 or impl[2] < 0 or impl[1] or impl[3]: fail.append(seed + " impl")
    for corner in ("Slow", "Fast"):
        for t in (0, 85):
            s = summary((b / f"acceptance/seed_{corner}_{t}C_timing.rpt").read_text())
            print(f"  {corner:4} {t:2}C WNS={s[0]:+.3f} TNS={s[1]:.3f} WHS={s[2]:+.3f} THS={s[3]:.3f}")
            if s[0] < 0.030 or s[2] < 0 or s[1] or s[3]: fail.append(f"{seed} {corner} {t}")
            for pair in ("eth_sys", "sys_eth", "eth_milan", "milan_eth"):
                r = (b / f"acceptance/seed_{corner}_{t}C_{pair}.rpt").read_text()
                slacks = [float(x) for x in re.findall(r"^Slack \(MET\)\s*:\s*([-\d.]+)ns", r, re.M)]
                viol = re.findall(r"^Slack \(VIOLATED\)", r, re.M)
                reqs = set(re.findall(r"Requirement:\s+([\d.]+)ns", r))
                if viol or reqs != {"8.000"} or not slacks: fail.append(f"{seed} {corner} {t} {pair}")
                print(f"    {pair:9} paths={len(slacks)} worst_slack={min(slacks):+.3f} requirements={sorted(reqs)}")
    inter = (b / "acceptance/seed_interaction.rpt").read_text().splitlines()
    for line in inter:
        if "eth_clocks0_rx" in line:
            f = line.split()
            cls = "Max Delay Datapath Only" if "Max Delay Datapath Only" in line else line[-45:].strip()
            unsafe = "Unsafe" in line
            print(f"  interaction {f[0]} -> {f[1]}: {cls}{' UNSAFE' if unsafe else ''}")
            if unsafe: fail.append(f"{seed} unsafe {f[0]}->{f[1]}")
print("FAIL: " + ", ".join(fail) if fail else "ALL ACCEPTANCE-4 CHECKS PASS")
sys.exit(1 if fail else 0)

#!/usr/bin/env python3
"""Show the head's sim_main.cpp equals the ancestor's after deleting only
lines that are pure scaffolding (phase headers, closing braces, phase calls,
blank lines and the one new comment). Run inside an FPGA-gPTP clone."""
import re, subprocess, sys
OLD, NEW = sys.argv[1], sys.argv[2]
F = "tb/verilator/engine/sim_main.cpp"
old = subprocess.run(["git", "show", f"{OLD}:{F}"], capture_output=True, text=True, check=True).stdout.splitlines()
new = subprocess.run(["git", "show", f"{NEW}:{F}"], capture_output=True, text=True, check=True).stdout.splitlines()
scaffold = re.compile(r"^(  void [a-z_]+\(\) \{|  \}|    [a-z_]+\(\);|  // Each phase continues from the state left by its predecessor\.|)$")
def strip(lines):
    return [l for l in lines if not scaffold.match(l)]
so, sn = strip(old), strip(new)
print(f"ancestor {len(old)} lines, head {len(new)} lines; after scaffold removal {len(so)} vs {len(sn)}")
print("IDENTICAL" if so == sn else "DIFFERENT")
removed = [l for l in new if scaffold.match(l) and l.strip() and l not in old]
print(f"head-only scaffolding lines: {len(set(removed))} distinct")
sys.exit(0 if so == sn else 1)

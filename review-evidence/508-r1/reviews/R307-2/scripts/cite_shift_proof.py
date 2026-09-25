#!/usr/bin/env python3
"""For each processor citation PR #560 re-aimed in round 3, compare the text
the round-2 citation named at the pin it was written for (a8f8ce81) with the
text the round-3 citation names at the adopted pin (990f9652), and print both
to show the construct is the same. Usage: cite_shift_proof.py <superproject>"""
import subprocess, sys
pp = sys.argv[1] + "/protocol-processor"
OLD, NEW = "a8f8ce81", "990f96526bb89356c963a260ebbdcf2a77e6623a"
PAIRS = [  # (file, old span, new span, construct named at head)
    ("hdl/srp/KL_srp_top.sv", (450, 450), (451, 451), "sr_adm_fsm_w"),
    ("hdl/srp/KL_srp_top.sv", (785, 796), (787, 798), "opt_r aging"),
    ("hdl/srp/KL_srp_top.sv", (871, 874), (873, 876), "reload"),
    ("hdl/srp/KL_srp_top.sv", (210, 210), (211, 211), "tk_reg_state_o"),
    ("hdl/srp/KL_srp_listener_fsm.sv", (842, 843), (851, 853), "status_map driver of tk_reg_state_o"),
]
def get(rev, f):
    return subprocess.run(["git", "-C", pp, "show", f"{rev}:{f}"], check=True,
                          capture_output=True, text=True).stdout.splitlines()
bad = 0
for f, (oa, ob), (na, nb), what in PAIRS:
    o, n = get(OLD, f)[oa-1:ob], get(NEW, f)[na-1:nb]
    same = [x.strip() for x in o] == [x.strip() for x in n[:len(o)]]
    print(f"== {f} {OLD[:8]}:{oa}-{ob} -> {NEW[:8]}:{na}-{nb} ({what}): "
          f"{'SAME TEXT' if same else 'TEXT DIFFERS'}{' (+%d line)' % (len(n)-len(o)) if len(n) > len(o) else ''}")
    for x in o: print(f"   old| {x}")
    for x in n: print(f"   new| {x}")
    bad += not same
print("RESULT:", "every re-aimed span names the same text" if not bad else f"{bad} span(s) differ")
sys.exit(1 if bad else 0)

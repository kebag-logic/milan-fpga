"""Prove the PR-touched processor citations at its adopted revision.

Run from the candidate worktree. Compare each former citation's a8f8ce81
text with the corrected 990f9652 span, including multiline citations that
cite_drift.py cannot parse. Print the named construct and exact cited text.
"""
from pathlib import Path
import hashlib
import re
import subprocess

PIN = "990f96526bb89356c963a260ebbdcf2a77e6623a"
BASE = "c266432dcb0cdd464205823a3d82cad260eedde2"

def git(*args):
    return subprocess.check_output(["git", *args])

assert git("-C", "protocol-processor", "rev-parse", "HEAD").decode().strip() == PIN
assert not git("-C", "protocol-processor", "status", "--porcelain")
# (parent, target, old range, new range, construct, literal citation token)
rows = [
    ("hdl/milan/milan_datapath.sv", "KL_srp_top.sv", (450,450), (451,451),
     "sr_adm_fsm_w", "sr_adm_fsm_w at 451"),
    ("hdl/milan/milan_datapath.sv", "KL_srp_top.sv", (785,796), (787,798),
     "opt_r", "opt_r aging at 787-798"),
    ("hdl/milan/milan_datapath.sv", "KL_srp_top.sv", (871,874), (873,876),
     "opt_cnt_r", "reload at 873-876"),
    ("hdl/milan/milan_datapath.sv", "KL_srp_talker_fsm.sv", (705,710), (705,710),
     "reg_r", "KL_srp_talker_fsm.sv:705-710"),
    ("hdl/milan/milan_datapath.sv", "KL_srp_admission.sv", (187,190), (187,190),
     "refuse_w", "KL_srp_admission.sv:187-190"),
    ("hdl/milan/milan_datapath.sv", "KL_srp_admission.sv", (261,266), (261,266),
     "sr_admitted_o", "261-266"),
    ("hdl/milan/milan_datapath.sv", "KL_srp_top.sv", (210,210), (211,211),
     "tk_reg_state_o", "KL_srp_top.sv:211 tk_reg_state_o"),
    ("hdl/milan/milan_datapath.sv", "KL_srp_listener_fsm.sv", (842,844), (851,853),
     "tk_reg_state_o", "KL_srp_listener_fsm.sv:851-853"),
    ("tb/verilator/pp_shadow/sim_main.cpp", "KL_srp_top.sv", (210,210), (211,211),
     "tk_reg_state_o", "KL_srp_top.sv:211 tk_reg_state_o"),
]
for parent, name, old_span, new_span, construct, token in rows:
    parent_text = Path(parent).read_text()
    assert parent_text.count(token) == 1, (parent, token)
    target = "hdl/srp/" + name
    old = git("-C", "protocol-processor", "show", "a8f8ce81:" + target).splitlines()
    new = git("-C", "protocol-processor", "show", PIN + ":" + target).splitlines()
    old_text = b"\n".join(old[old_span[0]-1:old_span[1]])
    new_text = b"\n".join(new[new_span[0]-1:new_span[1]])
    assert old_text == new_text, (target, old_span, new_span)
    assert construct.encode() in new_text, (target, construct)
    line = parent_text[:parent_text.index(token)].count("\n") + 1
    print(f"PASS {parent}:{line} -> {target}:{new_span[0]}-{new_span[1]} {construct}")
    print(new_text.decode())
# Inventory every added source-line citation, retaining adjacent continuation
# lines. This verifies the proof's scope against the complete lane diff.
diff = git("diff", "--unified=2", BASE).decode()
file = ""
print("PR added citation inventory:")
for line in diff.splitlines():
    if line.startswith("+++ b/"):
        file = line[6:]
    if line.startswith("+") and not line.startswith("+++") and re.search(
            r"\.(?:sv|svh|cpp|hpp|py):(?:[0-9]|\s*$)", line):
        assert file in {r[0] for r in rows}, (file, line)
        print(file, line)
print(f"PASS all {len(rows)} citation spans, including unchanged adjacent citations")

def section(data):
    marker = b"## Unreleased - licence and LeaveAll scope"
    start = data.index(marker)
    end = data.index(b"\n## ", start + len(marker))
    return data[start:end]
current = Path("CHANGELOG.md").read_bytes()
expected = git("show", BASE + ":CHANGELOG.md")
assert section(current) == section(expected)
assert current.count(b"Processor issue 116:") == 1
assert current.count(b"Processor issue 113:") == 1
print("PASS #530 changelog section byte-identical; sha256", hashlib.sha256(section(current)).hexdigest())
print("PASS processor #116 and #113 entries occur once each")

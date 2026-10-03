#!/usr/bin/env python3
"""Check that the round-3 prescribed texts are present verbatim (whitespace and
comment markers normalised) at a commit, and that the replaced texts are gone.
usage: check_exact_texts.py <repo> <commit>"""
import re, subprocess, sys
repo, rev = sys.argv[1], sys.argv[2]
def show(path):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True, text=True, check=True).stdout
def norm(s, cpp=False):
    if cpp:
        s = "\n".join(re.sub(r"^\s*//\s?", "", l) for l in s.splitlines())
    return re.sub(r"\s+", " ", s).strip()
checks = [
  ("tb/pp_top/sim_main.cpp", True, "R444-2 N-F1 text",
   "The mark is a completion notification, not a persistence trigger: the D3 writer's name stage selects its records from the accepted live name write (`aecp_name_wr_o`, section D3N), the channel maps are the integrator's to persist (07 §5.1, the ruling on #83), and section D3 grades the scalar records.", True),
  ("tb/pp_top/sim_main.cpp", True, "old N-F1 text gone", "(not implemented yet)", False),
  ("tb/nvm_port/README.md", False, "R444-2 N-R1 :1064", "so the randomized half is not cut by this suite", True),
  ("tb/nvm_port/README.md", False, "R444-2 N-R1 :1347", "asks for are not cut by this suite** on either side", True),
  ("tb/nvm_port/README.md", False, "N-R1 old words gone", "still owed (delivered", False),
  ("tb/nvm_port/README.md", False, "N-R1 old words gone (b)", "asks for are still owed", False),
  ("tb/nvm_port/README.md", False, "N-R3 writer cite", "`hdl/aecp/KL_aecp_nvm_writer.sv:549-552`", True),
  ("tb/nvm_port/README.md", False, "N-R3 top cite", "`hdl/top/protocol_processor_top.sv:2730`", True),
  ("tb/nvm_port/README.md", False, "N-R3 old writer cite gone", "KL_aecp_nvm_writer.sv:482-485", False),
  ("tb/nvm_port/README.md", False, "N-R3 old top cite gone", "protocol_processor_top.sv:2714", False),
]
bad = 0
for path, cpp, label, text, want in checks:
    hay = norm(show(path), cpp)
    got = norm(text) in hay
    ok = got == want
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {label}: {'present' if got else 'absent'} (want {'present' if want else 'absent'}) in {path}")
print(f"{len(checks) - bad} of {len(checks)} OK")
sys.exit(1 if bad else 0)

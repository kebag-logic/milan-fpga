"""Write a scratch-parent consumer spec: the manager template's commands.

usage: mkparentspec.py <out.json> <cwd> <head> <base> <part>
<part> "A" is the template's commands 1-13 and 15 plus the gPTP extras,
"B" is command 14 (the physical-rate milan_dp_gptp suite) alone, run in
its own clone because it rebuilds milan_dp's shared generated files.
The template is prepare-consumer.py's list: gptp68 r3's six, the five
docs gates, and the four milan_dp gPTP legs. The PATH entry names this
lane's wrapper around the pinned Verilator 5.050; TMPDIR, HOME and the
tsn-gen checkout at the parent CI pin (deca300c) are added.
"""
import json
import sys
from pathlib import Path

S = "<scratch>"
HOME = "<home>"
ENV = ["env",
       f"PATH={S}/bin:{HOME}/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       f"VERILATOR_ROOT={HOME}/.local/share/containers/storage/overlay/"
       "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator",
       f"TMPDIR={S}/tmp", f"HOME={HOME}", "TSN_GEN_ROOT=<round-1-scratch>/ext/tsn-gen"]
TEMPLATE = [
    ["python3", "scripts/check_cpp_idiom.py"],
    ["python3", "scripts/check_py_idiom.py"],
    ["python3", "scripts/xvlog_gate.py", "--check"],
    ["python3", "scripts/check_rtl_source_lists.py"],
    ["python3", "sw/builder/test_builder.py"],
    ["make", "-C", "tb/verilator/gptp_shadow", "-j8"],
    ["python3", "scripts/check_port_contracts.py"],
    ["python3", "scripts/measure_naming.py", "--check"],
    ["python3", "scripts/measure_test_evidence.py", "--check"],
    ["python3", "scripts/docs_check.py"],
    ["python3", "scripts/lint_rtl.py", "--check"],
    ["make", "-C", "tb/verilator/milan_dp", "gptp"],
    ["make", "-C", "tb/verilator/milan_dp", "gptp-lat"],
    ["make", "-C", "tb/verilator/milan_dp_gptp"],
    ["make", "-C", "tb/verilator/milan_dp_gm_steps"],
]
EXTRAS = [
    ["make", "-C", "tb/verilator/gptp_plane"],
    ["make", "-C", "tb/verilator/gptp_txts"],
    ["make", "-C", "tb/verilator/gptp_tables"],
    ["make", "-C", "tb/verilator/tsn_fuzz", "ptp"],
    ["git", "status", "--porcelain"],
]
out, cwd, head, base, part = sys.argv[1:6]
if part == "A":
    index = [i for i in range(1, 16) if i != 14] + [f"x{k}" for k in range(1, 6)]
    cmds = [c for i, c in enumerate(TEMPLATE, 1) if i != 14] + EXTRAS
else:
    index, cmds = [14, "x5"], [TEMPLATE[13], EXTRAS[-1]]
spec = dict(cwd=cwd, head=head, base=base, index=index, commands=[ENV + c for c in cmds])
Path(out).write_text(json.dumps(spec, indent=1) + "\n")
print(out, index)

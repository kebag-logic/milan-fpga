"""Write one gate spec for run-recorded-gates.py.

usage: mkspec.py <repo|parent> <out.json> <cwd> <head> <base>
"""
import json
import sys
from pathlib import Path

S = "<scratch>"
VROOT = ("<home>/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/"
         "diff/usr/share/verilator")
ENV = ["env",
       f"PATH={S}/pinned-tool-bin:<user-bin>:/usr/local/sbin:"
       "/usr/local/bin:/usr/bin:/bin",
       f"VERILATOR_ROOT={VROOT}",
       f"TMPDIR={S}/tmp",
       "HOME=<home>"]

REPO = [
    ["make", "contract"],
    ["make", "-C", "tb/verilator/ucpu"],
    ["make", "-C", "tb/verilator/parser"],
    ["make", "-C", "tb/verilator/engine"],
    ["make", "-C", "tb/verilator/gaskets"],
    ["make", "-C", "tb/tsngen"],
    ["make", "-C", "bench/arty", "test"],
    ["make", "lint"],
    ["make", "docs"],
    ["git", "diff", "--exit-code", "--stat"],
]

PARENT = [
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

kind, out, cwd, head, base = sys.argv[1:6]
cmds = REPO if kind == "repo" else PARENT
spec = dict(cwd=cwd, head=head, base=base, commands=[ENV + c for c in cmds])
Path(out).write_text(json.dumps(spec, indent=1) + "\n")
print(out, len(cmds))

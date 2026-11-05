"""Write one recorded-gates spec: usage mkspec.py <list> <out.json> <cwd> <head> <base> [arm out dir]

Lists: repo-fast (the processor's own gates but the engine mutation arm),
ooc (OOC area and timing only), arm (the engine mutation arm through
arm_jobs.py at --jobs 8), parent-A (the parent's gPTP consumer gates but
milan_dp_gptp, simulated consumers first), parent-B (milan_dp_gptp).
"""
import json
import sys
from pathlib import Path

S = "<scratch>"
VROOT = ("<home>/.local/share/containers/storage/overlay/"
         "9517af577e2019496be7a9f3df0cdeafba0a4f827989b59cb358abf6403fbbde/diff/usr/share/verilator")
ENV = ["env", f"PATH={S}/bin:<home>/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/bin:/bin",
       f"VERILATOR_ROOT={VROOT}", f"TMPDIR={S}/tmp", "HOME=<home>", "VERILATOR_JOBS=4"]
CLEAN = [["git", "diff", "--exit-code", "--stat"], ["git", "status", "--porcelain"]]
REPO_FAST = [["make", "contract"], ["make", "-C", "tb/verilator/ucpu"], ["make", "-C", "tb/verilator/parser"],
             ["make", "-C", "tb/verilator/engine", "run"], ["make", "-C", "tb/verilator/gaskets"],
             ["make", "-C", "tb/tsngen"], ["make", "-C", "bench/arty", "test"], ["make", "lint"], ["make", "docs"],
             ["make", "diagrams-check"], ["make", "ooc"]] + CLEAN
OOC = [["make", "ooc"]] + CLEAN
PARENT_A = [["make", "-C", "tb/verilator/gptp_shadow", "-j8"],
            ["make", "-C", "tb/verilator/milan_dp", "gptp"],
            ["make", "-C", "tb/verilator/milan_dp", "gptp-lat"],
            ["make", "-C", "tb/verilator/gptp_plane"], ["make", "-C", "tb/verilator/gptp_txts"],
            ["make", "-C", "tb/verilator/gptp_tables"], ["make", "-C", "tb/verilator/tsn_fuzz", "ptp"],
            ["make", "-C", "tb/verilator/milan_dp_gm_steps"],
            ["python3", "scripts/check_cpp_idiom.py"], ["python3", "scripts/check_py_idiom.py"],
            ["python3", "scripts/xvlog_gate.py", "--check"], ["python3", "scripts/check_rtl_source_lists.py"],
            ["python3", "scripts/check_port_contracts.py"], ["python3", "scripts/measure_naming.py", "--check"],
            ["python3", "scripts/measure_test_evidence.py", "--check"], ["python3", "scripts/docs_check.py"],
            ["python3", "scripts/lint_rtl.py", "--check"], ["python3", "sw/builder/test_builder.py"],
            ["git", "status", "--porcelain"]]
PARENT_B = [["make", "-C", "tb/verilator/milan_dp_gptp"], ["git", "status", "--porcelain"]]
name, out, cwd, head, base = sys.argv[1:6]
if name == "arm":
    lists = [["python3", f"{S}/tools/arm_jobs.py", "tb/verilator/engine", sys.argv[6],
              "--jobs", "8", "--budget-s", "30000", "--longest-s", "900"]] + CLEAN
else:
    lists = {"repo-fast": REPO_FAST, "ooc": OOC, "parent-A": PARENT_A, "parent-B": PARENT_B}[name]
Path(out).write_text(json.dumps(dict(cwd=cwd, head=head, base=base,
                                     commands=[ENV + c for c in lists]), indent=1) + "\n")
print(out, len(lists))

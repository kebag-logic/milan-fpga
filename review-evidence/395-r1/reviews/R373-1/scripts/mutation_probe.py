#!/usr/bin/env python3
"""Reviewer mutation probe for sw/builder/test_timing_grade.py at 66001a30.

Each mutant is a disposable copy of sw/litex plus the test file under
<packet>/scratch/mut/<name>/; the checkout is never modified.  A mutant is
KILLED when the test (contract and, with a LiteX interpreter, platform hooks)
exits nonzero.  Usage: mutation_probe.py <checkout> <packet> <litex-python>
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import shutil
import subprocess
import sys

CHECKOUT, PACKET = (Path(a).resolve() for a in sys.argv[1:3])
LITEX_PY = Path(sys.argv[3]).absolute()  # not resolve(): a venv interpreter is a symlink
TCL, DECL, PLAT, TEST = ("sw/litex/timing_grade.tcl", "sw/litex/platforms/ax7101_timing.py",
                         "sw/litex/platforms/alinx_ax7101.py", "sw/builder/test_timing_grade.py")

# (name, file, old, new, expectation)
MUTANTS = [
    ("control-unmodified", TCL, "# Report the fixed", "# Report the fixed", "survive"),
    ("check-drops-grade", TCL, "$grade ne [dict get $spec grade] ||", "0 ||", "kill"),
    ("check-drops-temp", TCL, "$temp != [dict get $spec max_c]", "0", "kill"),
    ("check-drops-part", TCL, "if {[get_property PART [current_design]] ne [dict get $spec part]} {",
     "if {0} {", "kill"),
    ("check-setup-only-accepted", TCL, '"^ *$corner +Yes +Yes *$"', '"^ *$corner +Yes +"', "kill"),
    ("check-skips-fast", TCL, "foreach corner [dict get $spec corners] {\n        if {![regexp",
     "foreach corner [lrange [dict get $spec corners] 0 0] {\n        if {![regexp", "kill"),
    ("configure-no-part-check", TCL, 'if {$expected eq "" || $actual ne $expected} {', "if {0} {", "kill"),
    ("configure-min-temp", TCL, "-junction_temp $max_c", "-junction_temp $min_c", "kill"),
    ("configure-no-corners", TCL, "        config_timing_corners -corner $corner -delay_type min_max\n    }\n}",
     "    }\n}", "kill"),
    ("reports-no-finally", TCL, "} finally {", "} on ok {} {} ; if {0} {", "kill"),
    ("reports-only-max-temp", TCL, "foreach temp [list [dict get $spec min_c] [dict get $spec max_c]] {",
     "foreach temp [list [dict get $spec max_c]] {", "kill"),
    ("reports-no-other-disable", TCL, "config_timing_corners -corner $other -delay_type none",
     "config_timing_corners -corner $other -delay_type min_max", "kill"),
    ("reports-no-cdc", TCL, "    report_cdc -details -file ${prefix}_cdc.rpt\n", "", "kill"),
    ("reports-no-clock-interaction", TCL,
     "    report_clock_interaction -delay_type min_max -file ${prefix}_clock_interaction.rpt\n", "", "kill"),
    ("reports-no-negative-paths", TCL, "report_timing -delay_type min_max -slack_lesser_than 0",
     "list -delay_type min_max -slack_lesser_than 0", "kill"),
    ("reports-no-final-check", TCL, "    kl_timing_grade_check\n    report_timing_summary", "    report_timing_summary",
     "report"),
    ("reports-no-unconstrained", TCL, "-report_unconstrained \\\n        -check_timing_verbose",
     "\\\n        -check_timing_verbose", "report"),
    ("reports-cdc-no-details", TCL, "report_cdc -details", "report_cdc", "report"),
    ("decl-industrial", DECL, '"grade": "commercial"', '"grade": "industrial"', "kill"),
    ("decl-max-100", DECL, '"junction_max_c": 85', '"junction_max_c": 100', "kill"),
    ("decl-part-minus1", DECL, '"part": "xc7a100t-fgg484-2"', '"part": "xc7a100t-fgg484-1"', "kill"),
    ("decl-configure-literal-grade", DECL, 'grade["grade"], grade["junction_min_c"]',
     '"industrial", grade["junction_min_c"]', "kill"),
    ("platform-literal-part", PLAT, 'TIMING_GRADE["part"], _io', '"xc7a100t-fgg484-1", _io', "kill"),
    ("platform-no-preplacement", PLAT, "            self.toolchain.pre_placement_commands.append(\n"
     '                command.replace("{", "{{").replace("}", "}}"))', "            pass", "kill"),
    ("platform-no-signoff", PLAT, '            "kl_timing_grade_reports {build_name}_signoff",\n', "", "kill"),
    ("platform-signoff-last", PLAT, '            "kl_timing_grade_reports {build_name}_signoff",\n', "",
     "kill-append"),
]


def run(mutant):
    name, rel, old, new, expect = mutant
    root = PACKET / "scratch/mut" / name
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(CHECKOUT / "sw/litex", root / "sw/litex",
                    ignore=shutil.ignore_patterns("__pycache__", "build*", "*.pyc"))
    (root / "sw/builder").mkdir(parents=True)
    shutil.copy2(CHECKOUT / TEST, root / TEST)
    path = root / rel
    text = path.read_text()
    if text.count(old) != 1:
        return name, expect, "PROBE-ERROR", f"anchor count {text.count(old)}"
    text = text.replace(old, new)
    if expect == "kill-append":
        # Moves the signoff after write-affecting bitstream properties: still before write_bitstream.
        text = text.replace('"set_property CONFIG_VOLTAGE 3.3 [current_design]",\n',
                            '"set_property CONFIG_VOLTAGE 3.3 [current_design]",\n'
                            '            "kl_timing_grade_reports {build_name}_signoff",\n')
        expect = "report"
    path.write_text(text)
    r = subprocess.run([sys.executable, "-B", str(root / TEST), str(LITEX_PY)], cwd=root,
                       capture_output=True, text=True, timeout=300)
    outcome = "KILLED" if r.returncode else "SURVIVED"
    tail = (r.stderr.strip().splitlines() or [""])[-1][:160]
    return name, expect, outcome, tail


with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, MUTANTS))
bad = 0
for name, expect, outcome, tail in results:
    ok = ((expect == "kill" and outcome == "KILLED") or (expect == "survive" and outcome == "SURVIVED")
          or expect == "report")
    bad += not ok and outcome != "PROBE-ERROR"
    bad += outcome == "PROBE-ERROR"
    print(f"{'OK ' if ok else 'BAD'} {name:32s} expect={expect:8s} {outcome:9s} {tail}")
print(f"MUTATION SUMMARY: {len(results)} mutants, {bad} unexpected")
sys.exit(1 if bad else 0)

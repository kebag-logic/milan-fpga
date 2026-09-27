#!/usr/bin/env python3
"""Reviewer mutation probe for the #395 timing-grade builder arm at 3a0cb4cf.

Round 2 of the round-1 probe.  Each mutant is a disposable full copy of the
clone (git metadata included) under <packet>/scratch/mut/<name>/; the checkout is never modified.
A mutant is KILLED when the builder bank's timing-grade arm,
test_builder.test_commercial_timing_grade() (the first function the bank's
main loop calls; an exception there aborts the bank nonzero), exits nonzero
with a LiteX interpreter available.  The five faults named "r372-*" are the
five planted faults the round-2 assignment requires to fail the bank.
Usage: mutation_probes.py <checkout> <packet> <litex-python>
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import os
import shutil
import subprocess
import sys

CHECKOUT, PACKET = (Path(a).resolve() for a in sys.argv[1:3])
LITEX_PY = Path(sys.argv[3]).absolute()  # not resolve(): a venv interpreter is a symlink
TCL, DECL, PLAT, SOC = ("sw/litex/timing_grade.tcl", "sw/litex/platforms/ax7101_timing.py",
                        "sw/litex/platforms/alinx_ax7101.py", "sw/litex/milan_soc.py")
CORNER_SUMMARY = "-delay_type min_max -report_unconstrained \\\n                    -max_paths 5"
ALL_SUMMARY = "-delay_type min_max -report_unconstrained \\\n        -check_timing_verbose"

# (name, file, old, new, expectation)
MUTANTS = [
    ("control-unmodified", TCL, "# Report the fixed", "# Report the fixed", "survive"),
    # The five planted faults of the round-2 assignment (R372-1 F2).
    ("r372-hook-no-leading-refusal", TCL, "proc kl_timing_grade_reports {prefix} {\n    kl_timing_grade_check\n",
     "proc kl_timing_grade_reports {prefix} {\n", "kill"),
    ("r372-corner-summary-setup-only", TCL, CORNER_SUMMARY,
     CORNER_SUMMARY.replace("min_max", "max"), "kill"),
    ("r372-corner-summary-no-unconstrained", TCL, CORNER_SUMMARY,
     CORNER_SUMMARY.replace(" -report_unconstrained", ""), "kill"),
    ("r372-all-summary-no-check-verbose", TCL, ALL_SUMMARY,
     ALL_SUMMARY.replace("-check_timing_verbose", ""), "kill"),
    ("r372-clock-interaction-setup-only", TCL, "report_clock_interaction -delay_type min_max",
     "report_clock_interaction -delay_type max", "kill"),
    # Round-1 S3 survivors and neighbouring report-argument faults.
    ("all-summary-no-unconstrained", TCL, ALL_SUMMARY,
     ALL_SUMMARY.replace(" -report_unconstrained", ""), "kill"),
    ("cdc-no-details", TCL, "report_cdc -details", "report_cdc", "kill"),
    ("check-timing-no-verbose", TCL, "check_timing -verbose -file", "check_timing -file", "kill"),
    ("all-summary-setup-only", TCL, ALL_SUMMARY, ALL_SUMMARY.replace("min_max", "max"), "kill"),
    ("corner-summary-hold-only", TCL, CORNER_SUMMARY, CORNER_SUMMARY.replace("min_max", "min"), "kill"),
    ("negative-setup-only", TCL, "report_timing -delay_type min_max -slack_lesser_than 0",
     "report_timing -delay_type max -slack_lesser_than 0", "kill"),
    ("negative-no-slack-filter", TCL, "-slack_lesser_than 0", "-slack_lesser_than 100", "kill"),
    ("hook-check-after-grade-file", TCL,
     "    kl_timing_grade_check\n    set spec $::kl_timing_grade\n    set info [open ${prefix}_grade.txt w]\n"
     "    puts $info $spec\n",
     "    set spec $::kl_timing_grade\n    set info [open ${prefix}_grade.txt w]\n"
     "    puts $info $spec\n    kl_timing_grade_check\n", "kill"),
    ("reports-no-final-check", TCL, "    kl_timing_grade_check\n    report_timing_summary",
     "    report_timing_summary", "report"),
    # Round-1 mandatory mutants, re-anchored at this head.
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
    ("decl-industrial", DECL, '"grade": "commercial"', '"grade": "industrial"', "kill"),
    ("decl-max-100", DECL, '"junction_max_c": 85', '"junction_max_c": 100', "kill"),
    ("decl-part-minus1", DECL, '"part": "xc7a100t-fgg484-2"', '"part": "xc7a100t-fgg484-1"', "kill"),
    ("decl-configure-literal-grade", DECL, 'grade["grade"], grade["junction_min_c"]',
     '"industrial", grade["junction_min_c"]', "kill"),
    ("platform-literal-part", PLAT, 'TIMING_GRADE["part"], _io', '"xc7a100t-fgg484-1", _io', "kill"),
    ("platform-no-preplacement", PLAT, "            self.toolchain.pre_placement_commands.append(\n"
     '                command.replace("{", "{{").replace("}", "}}"))', "            pass", "kill"),
    ("platform-no-signoff", PLAT, '            "kl_timing_grade_reports {build_name}_signoff",\n', "", "kill"),
    # Item 1 / taken S2: the PLL speed grade derives from the declaration.
    ("pll-literal-minus2", SOC, 'S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)[1]))',
     "S7PLL(speedgrade=-2)", "kill"),
    ("pll-literal-from-arty", SOC, 'S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)[1]))',
     "S7PLL(speedgrade=-1)", "kill"),
]


def run(mutant):
    name, rel, old, new, expect = mutant
    root = PACKET / "scratch/mut" / name
    if root.exists():
        shutil.rmtree(root)
    # The whole clone, git metadata included: the SoC import lists submodule
    # files with git, so a copy without it fails before any assertion runs.
    shutil.copytree(CHECKOUT, root, symlinks=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    path = root / rel
    text = path.read_text()
    if text.count(old) != 1:
        return name, expect, "PROBE-ERROR", f"anchor count {text.count(old)}"
    path.write_text(text.replace(old, new))
    env = dict(os.environ, MILAN_LITEX_PYTHON=str(LITEX_PY))
    r = subprocess.run([sys.executable, "-B", "-c",
                        "import test_builder as t; t.test_commercial_timing_grade()"],
                       cwd=root / "sw/builder", env=env, capture_output=True, text=True, timeout=600)
    outcome = "KILLED" if r.returncode else "SURVIVED"
    if "SKIP" in r.stdout:
        outcome += "+SKIP"
    err = r.stderr.strip().splitlines()
    where = next((l.strip() for l in reversed(err) if l.strip().startswith('File "')), "")
    where = where.replace(str(root), "<mutant>")
    tail = (err or [""])[-1][:150].replace(str(root), "<mutant>")
    return name, expect, outcome, f"{where[:110]} | {tail}" if err else ""


with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(run, MUTANTS))
bad = 0
for name, expect, outcome, tail in results:
    ok = ((expect == "kill" and outcome == "KILLED") or (expect == "survive" and outcome == "SURVIVED")
          or (expect == "report" and outcome in ("KILLED", "SURVIVED")))
    bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {name:38s} expect={expect:7s} {outcome:9s} {tail}")
print(f"MUTATION SUMMARY: {len(results)} mutants, {bad} unexpected")
sys.exit(1 if bad else 0)

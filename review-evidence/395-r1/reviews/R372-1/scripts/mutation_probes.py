#!/usr/bin/env python3
"""Plant faults in disposable copies of the PR's timing-grade files and run its test.

Usage: mutation_probes.py <clone> <scratch-dir> <litex-python>
Each probe is a fresh `git archive HEAD` extraction; the clone is never edited.
A probe is KILLED when the test exits non-zero, SURVIVED when it passes.
"""

import subprocess
import sys
import tarfile
import io
from pathlib import Path

CLONE, SCRATCH, LITEX_PY = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
TCL = "sw/litex/timing_grade.tcl"
DECL = "sw/litex/platforms/ax7101_timing.py"
PLAT = "sw/litex/platforms/alinx_ax7101.py"

# (label, file, old, new, expectation) - expectation is what a sound test must do.
MUTANTS = [
    ("control-none", None, None, None, "SURVIVE"),
    ("decl-max-100C", DECL, '"junction_max_c": 85', '"junction_max_c": 100', "KILL"),
    ("decl-grade-industrial", DECL, '"grade": "commercial"', '"grade": "industrial"', "KILL"),
    ("decl-part-speed-1", DECL, '"part": "xc7a100t-fgg484-2"', '"part": "xc7a100t-fgg484-1"', "KILL"),
    ("check-skip-grade-compare", TCL, "$grade ne [dict get $spec grade] ||", "", "KILL"),
    ("check-skip-temp-compare", TCL, "$temp != [dict get $spec max_c]", "0", "KILL"),
    ("check-corner-one-yes", TCL, '"^ *$corner +Yes +Yes *$"', '"^ *$corner +Yes"', "KILL"),
    ("configure-skip-part-check", TCL, 'if {$expected eq "" || $actual ne $expected} {', "if {0} {", "KILL"),
    ("configure-no-min-max", TCL,
     "        config_timing_corners -corner $corner -delay_type min_max\n    }\n}",
     "        config_timing_corners -corner $corner -delay_type max\n    }\n}", "KILL"),
    ("reports-no-leading-check", TCL, "proc kl_timing_grade_reports {prefix} {\n    kl_timing_grade_check",
     "proc kl_timing_grade_reports {prefix} {", "KILL"),
    ("reports-no-other-corner-off", TCL, "-corner $other -delay_type none", "-corner $other -delay_type min_max", "KILL"),
    ("reports-no-finally-restore", TCL,
     "    } finally {\n        set_operating_conditions -junction_temp [dict get $spec max_c]",
     "    } finally {\n        # restore removed", "KILL"),
    ("reports-single-endpoint", TCL, "foreach temp [list [dict get $spec min_c] [dict get $spec max_c]]",
     "foreach temp [list [dict get $spec max_c] [dict get $spec max_c]]", "KILL"),
    ("reports-drop-negative", TCL, "report_timing -delay_type min_max -slack_lesser_than 0", "list -delay_type min_max -slack_lesser_than 0", "KILL"),
    ("reports-drop-cdc", TCL, "report_cdc -details", "list -details", "KILL"),
    # Report-content faults: item 2 requires WHS/THS and unconstrained paths per corner.
    ("reports-corner-setup-only", TCL,
     "report_timing_summary -delay_type min_max -report_unconstrained \\\n                    -max_paths 5",
     "report_timing_summary -delay_type max -report_unconstrained \\\n                    -max_paths 5", "KILL"),
    ("reports-corner-no-unconstrained", TCL,
     "report_timing_summary -delay_type min_max -report_unconstrained \\\n                    -max_paths 5",
     "report_timing_summary -delay_type min_max \\\n                    -max_paths 5", "KILL"),
    ("reports-all-no-check-verbose", TCL, "-check_timing_verbose ", "", "KILL"),
    ("reports-clock-interaction-setup-only", TCL, "report_clock_interaction -delay_type min_max",
     "report_clock_interaction -delay_type max", "KILL"),
    ("platform-no-preplacement", PLAT, "            self.toolchain.pre_placement_commands.append(",
     "            (lambda c: None)(", "KILL"),
    ("platform-no-signoff-report", PLAT, '            "kl_timing_grade_reports {build_name}_signoff",\n', "", "KILL"),
    ("platform-literal-part-1", PLAT, 'Xilinx7SeriesPlatform.__init__(self, TIMING_GRADE["part"]',
     'Xilinx7SeriesPlatform.__init__(self, "xc7a100t-fgg484-1"', "KILL"),
]


def extract(dest: Path) -> None:
    data = subprocess.run(["git", "-C", str(CLONE), "archive", "HEAD", "sw/litex",
                           "sw/builder/test_timing_grade.py"], check=True, capture_output=True).stdout
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        tar.extractall(dest, filter="data")


def main() -> int:
    bad = 0
    for label, rel, old, new, expect in MUTANTS:
        dest = SCRATCH / label
        subprocess.run(["rm", "-rf", str(dest)], check=True)
        dest.mkdir(parents=True)
        extract(dest)
        if rel is not None:
            path = dest / rel
            text = path.read_text(encoding="utf-8")
            count = text.count(old)
            if count != 1:
                print(f"{label}: PLANT-FAILED (pattern count {count})")
                bad += 1
                continue
            path.write_text(text.replace(old, new), encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", "sw/builder/test_timing_grade.py", LITEX_PY],
                                cwd=dest, capture_output=True, text=True, timeout=300, check=False)
        outcome = "KILL" if result.returncode != 0 else "SURVIVE"
        verdict = "as-expected" if outcome == expect else "UNEXPECTED"
        if outcome != expect:
            bad += 1
        tail = (result.stderr.strip().splitlines() or [""])[-1][:160]
        print(f"{label}: rc={result.returncode} {outcome} expected={expect} {verdict} | {tail}")
    print(f"unexpected={bad}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

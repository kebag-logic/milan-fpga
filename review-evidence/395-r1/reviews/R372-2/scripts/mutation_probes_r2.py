#!/usr/bin/env python3
"""Plant faults in disposable copies of the PR's timing-grade files and run its tests.

Usage: mutation_probes_r2.py <clone> <scratch-dir> <litex-python> <submodule-copies>

Round-2 rerun of the R372-1 campaign (scripts/mutation_probes.py in the
R372-1 packet): the same 22 plants, unchanged, plus plants for the round-2
changes. Each probe is a fresh `git archive HEAD` extraction; the clone is
never edited. Every plant is run through two entries:
  focused - `sw/builder/test_timing_grade.py <litex-python>` (the file's own main)
  builder - `test_builder.test_commercial_timing_grade()`, the function the
            full builder bank runs first (its exception ends the bank non-zero)
A probe is KILLED when the entry exits non-zero, SURVIVED when it passes.
At most 8 probes run at once.
"""

import concurrent.futures
import io
import os
import subprocess
import sys
import tarfile
from pathlib import Path

CLONE, SCRATCH, LITEX_PY = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
# Extracted copies (`git -C <sub> archive HEAD`) of the clone's pinned submodules.
SUBMODS = Path(sys.argv[4])
SUBMODULES = ("protocol-processor", "gptp-processor", "third_party/verilog-axis")
TCL = "sw/litex/timing_grade.tcl"
DECL = "sw/litex/platforms/ax7101_timing.py"
PLAT = "sw/litex/platforms/alinx_ax7101.py"
SOC = "sw/litex/milan_soc.py"

K, S = "KILL", "SURVIVE"
# (label, file, old, new, expected focused, expected builder)
MUTANTS = [
    ("control-none", None, None, None, S, S),
    # --- R372-1 campaign, unchanged patterns ---
    ("decl-max-100C", DECL, '"junction_max_c": 85', '"junction_max_c": 100', K, K),
    ("decl-grade-industrial", DECL, '"grade": "commercial"', '"grade": "industrial"', K, K),
    ("decl-part-speed-1", DECL, '"part": "xc7a100t-fgg484-2"', '"part": "xc7a100t-fgg484-1"', K, K),
    ("check-skip-grade-compare", TCL, "$grade ne [dict get $spec grade] ||", "", K, K),
    ("check-skip-temp-compare", TCL, "$temp != [dict get $spec max_c]", "0", K, K),
    ("check-corner-one-yes", TCL, '"^ *$corner +Yes +Yes *$"', '"^ *$corner +Yes"', K, K),
    ("configure-skip-part-check", TCL, 'if {$expected eq "" || $actual ne $expected} {', "if {0} {", K, K),
    ("configure-no-min-max", TCL,
     "        config_timing_corners -corner $corner -delay_type min_max\n    }\n}",
     "        config_timing_corners -corner $corner -delay_type max\n    }\n}", K, K),
    ("reports-no-leading-check", TCL, "proc kl_timing_grade_reports {prefix} {\n    kl_timing_grade_check",
     "proc kl_timing_grade_reports {prefix} {", K, K),
    ("reports-no-other-corner-off", TCL, "-corner $other -delay_type none", "-corner $other -delay_type min_max", K, K),
    ("reports-no-finally-restore", TCL,
     "    } finally {\n        set_operating_conditions -junction_temp [dict get $spec max_c]",
     "    } finally {\n        # restore removed", K, K),
    ("reports-single-endpoint", TCL, "foreach temp [list [dict get $spec min_c] [dict get $spec max_c]]",
     "foreach temp [list [dict get $spec max_c] [dict get $spec max_c]]", K, K),
    ("reports-drop-negative", TCL, "report_timing -delay_type min_max -slack_lesser_than 0", "list -delay_type min_max -slack_lesser_than 0", K, K),
    ("reports-drop-cdc", TCL, "report_cdc -details", "list -details", K, K),
    ("reports-corner-setup-only", TCL,
     "report_timing_summary -delay_type min_max -report_unconstrained \\\n                    -max_paths 5",
     "report_timing_summary -delay_type max -report_unconstrained \\\n                    -max_paths 5", K, K),
    ("reports-corner-no-unconstrained", TCL,
     "report_timing_summary -delay_type min_max -report_unconstrained \\\n                    -max_paths 5",
     "report_timing_summary -delay_type min_max \\\n                    -max_paths 5", K, K),
    ("reports-all-no-check-verbose", TCL, "-check_timing_verbose ", "", K, K),
    ("reports-clock-interaction-setup-only", TCL, "report_clock_interaction -delay_type min_max",
     "report_clock_interaction -delay_type max", K, K),
    ("platform-no-preplacement", PLAT, "            self.toolchain.pre_placement_commands.append(",
     "            (lambda c: None)(", K, K),
    ("platform-no-signoff-report", PLAT, '            "kl_timing_grade_reports {build_name}_signoff",\n', "", K, K),
    ("platform-literal-part-1", PLAT, 'Xilinx7SeriesPlatform.__init__(self, TIMING_GRADE["part"]',
     'Xilinx7SeriesPlatform.__init__(self, "xc7a100t-fgg484-1"', K, K),
    # --- round-2 additions ---
    # The PLL literal the round removed. Only the builder entry runs test_pll_grade;
    # the focused file's own main does not, so that entry is expected to miss it.
    ("pll-literal-restored", SOC, 'S7PLL(speedgrade=-int(platform.device.rsplit("-", 1)[1]))',
     "S7PLL(speedgrade=-2)", S, K),
    ("reports-all-setup-only", TCL,
     "report_timing_summary -delay_type min_max -report_unconstrained \\\n        -check_timing_verbose",
     "report_timing_summary -delay_type max -report_unconstrained \\\n        -check_timing_verbose", K, K),
    ("reports-all-no-unconstrained", TCL,
     "report_timing_summary -delay_type min_max -report_unconstrained \\\n        -check_timing_verbose",
     "report_timing_summary -delay_type min_max \\\n        -check_timing_verbose", K, K),
    ("reports-cdc-no-details", TCL, "report_cdc -details", "report_cdc", K, K),
    ("reports-check-timing-no-verbose", TCL, "check_timing -verbose", "check_timing", K, K),
    ("reports-negative-setup-only", TCL, "report_timing -delay_type min_max -slack_lesser_than 0",
     "report_timing -delay_type max -slack_lesser_than 0", K, K),
    ("reports-negative-no-slack-filter", TCL, "report_timing -delay_type min_max -slack_lesser_than 0 \\",
     "report_timing -delay_type min_max \\", K, K),
    ("reports-write-before-check", TCL, "proc kl_timing_grade_reports {prefix} {\n    kl_timing_grade_check",
     "proc kl_timing_grade_reports {prefix} {\n    close [open ${prefix}_early.txt w]\n    kl_timing_grade_check", K, K),
]

ARCHIVE = subprocess.run(["git", "-C", str(CLONE), "archive", "HEAD"], check=True,
                         capture_output=True).stdout

BUILDER = ("import sys; sys.path.insert(0, 'sw/builder'); import test_builder; "
           "test_builder.test_commercial_timing_grade(); "
           "assert not test_builder.SKIPPED, test_builder.SKIPPED")


def run_one(mutant):
    label, rel, old, new, want_focused, want_builder = mutant
    dest = SCRATCH / label
    subprocess.run(["rm", "-rf", str(dest)], check=True)
    dest.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(ARCHIVE)) as tar:
        tar.extractall(dest, filter="data")
    # git archive omits submodule contents; the builder entry imports the SoC,
    # which needs them. Link read-only copies of the pinned gitlink trees.
    for sub in SUBMODULES:
        link = dest / sub
        if link.is_dir():
            link.rmdir()
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(SUBMODS / sub, target_is_directory=True)
    if rel is not None:
        path = dest / rel
        text = path.read_text(encoding="utf-8")
        count = text.count(old)
        if count != 1:
            return [f"{label}: PLANT-FAILED (pattern count {count}) UNEXPECTED"], 1
    if rel is not None:
        path.write_text(text.replace(old, new), encoding="utf-8")
    env = dict(os.environ, MILAN_LITEX_PYTHON=LITEX_PY)
    lines, bad = [], 0
    for entry, argv, want in (
        ("focused", [sys.executable, "-B", "sw/builder/test_timing_grade.py", LITEX_PY], want_focused),
        ("builder", [sys.executable, "-B", "-c", BUILDER], want_builder),
    ):
        result = subprocess.run(argv, cwd=dest, capture_output=True, text=True, timeout=600,
                                check=False, env=env)
        outcome = K if result.returncode != 0 else S
        verdict = "as-expected" if outcome == want else "UNEXPECTED"
        bad += outcome != want
        if outcome == K:
            tail = (result.stderr.strip().splitlines() or [""])[-1][:170]
        else:
            tail = " / ".join(line.strip()[:60] for line in result.stdout.splitlines()
                              if "[timing grade]" in line)
        lines.append(f"{label} [{entry}]: rc={result.returncode} {outcome} expected={want} {verdict} | {tail}")
    return lines, bad


def main() -> int:
    total = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for lines, bad in pool.map(run_one, MUTANTS):
            total += bad
            for line in lines:
                print(line, flush=True)
    print(f"plants={len(MUTANTS)} entries={2 * len(MUTANTS)} unexpected={total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

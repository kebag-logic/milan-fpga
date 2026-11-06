#!/usr/bin/env python3
"""Reviewer-planted mutants for PR #846, each applied to its own disposable
copy of the exact head, then the checks that should catch it are run.

usage: mutants.py <scratch-dir> <log-dir> <verilator> <mutant-id>
  ids: MR1 MR2 MR3 MR4 MR6

Each mutant replaces exactly one occurrence of a literal (refused otherwise),
runs its checks and writes <log-dir>/<id>-<check>.log and .rc. A mutant is
CAUGHT when every listed check exits non-zero and its log names the failing
check.
"""
import pathlib
import subprocess
import sys

scratch, logs, V, mid = (pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]),
                         sys.argv[3], sys.argv[4])
logs.mkdir(parents=True, exist_ok=True)

GATES = ("test_gptp_dataset_matches_engine_announce,"
         "test_gptp_clock_accuracy_per_board")
MUTANTS = {
    # builder passes 0x22 whatever the config says
    "MR1": ("run-b", "sw/builder/endstation_builder.py",
            "\"--clock-accuracy\", f\"0x{cfg['gptp']['clock_accuracy']:02X}\"]",
            "\"--clock-accuracy\", \"0x22\"]",
            [("gate26", ["python3", "sw/builder/test_builder.py", "--gates", GATES]),
             ("gptp-lat", ["make", "-C", "tb/verilator/milan_dp", "gptp-lat",
                           f"VERILATOR={V}", "VERILATOR_JOBS=4"])],
            "gate 26c|\\[CA\\]|FAIL"),
    # builder ignores the config key: every board resolves to 0xFE
    "MR2": ("run-a", "sw/builder/endstation_builder.py",
            "v = int(gp_raw.get(\"clock_accuracy\", GPTP_CLOCK_ACCURACY_UNKNOWN))",
            "v = GPTP_CLOCK_ACCURACY_UNKNOWN",
            [("gate26", ["python3", "sw/builder/test_builder.py", "--gates", GATES]),
             ("gptp", ["make", "-C", "tb/verilator/milan_dp", "gptp",
                       f"VERILATOR={V}", "VERILATOR_JOBS=4"])],
            "gate 26b|gate 26c|\\[CA\\]|FAIL"),
    # gptp_shadow keeps dev's stale clockQuality constant
    "MR3": ("mut-3", "tb/verilator/gptp_shadow/Makefile",
            "-DOUR_CQ_TB=$(OUR_CQ)\"", "-DOUR_CQ_TB=0xF8FE436A\"",
            [("gptp_shadow", ["make", "-C", "tb/verilator/gptp_shadow", "run",
                              f"VERILATOR={V}", "VERILATOR_JOBS=2"])],
            "clockQuality|FAIL"),
    # gptp_plane image announces 0xFE while OUR_CQ is still the generator's
    "MR4": ("mut-4", "tb/verilator/gptp_plane/Makefile",
            "python3 $< --clk-hz 2000000 -o $@",
            "python3 $< --clk-hz 2000000 --clock-accuracy 0xFE -o $@",
            [("gptp_plane", ["make", "-C", "tb/verilator/gptp_plane", "run",
                             f"VERILATOR={V}"])],
            "clockQuality|FAIL"),
    # the descriptor ignores the resolved clockAccuracy
    "MR6": ("mut-6", "avdecc/aem_descriptors.py",
            "b += bytes([int(gp.get(\"clock_accuracy\", 0x21)),",
            "b += bytes([0xFE,",
            [("gate26", ["python3", "sw/builder/test_builder.py", "--gates", GATES])],
            "gate 26b|gate 26c|FAIL|AssertionError"),
}

copy, rel, old, new, checks, pattern = MUTANTS[mid]
root = scratch / copy
target = root / rel
text = target.read_text()
if text.count(old) != 1:
    sys.exit(f"{mid}: literal occurs {text.count(old)} times in {rel}, refusing")
target.write_text(text.replace(old, new))
if mid == "MR4":
    (root / "tb/verilator/gptp_plane/gptp_ucode.hex").unlink(missing_ok=True)
caught = True
for name, argv in checks:
    log = logs / f"{mid}-{name}.log"
    with open(log, "w") as f:
        rc = subprocess.run(argv, cwd=root, stdout=f, stderr=subprocess.STDOUT,
                            env={**__import__("os").environ,
                                 "PYTHONUNBUFFERED": "1"}).returncode
    (logs / f"{mid}-{name}.rc").write_text(f"{rc}\n")
    caught &= rc != 0
    print(f"{mid} {name}: rc {rc}")
# restore the copy's file so the copy can be reused
target.write_text(text)
print(f"{mid}: {'CAUGHT' if caught else 'SURVIVED'}")

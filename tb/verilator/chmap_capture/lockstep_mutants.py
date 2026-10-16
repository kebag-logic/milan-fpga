#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Mutation arm for the chmap_capture lockstep leg (#640 M6): prove its source-table and skid checks can fail.

sim_lockstep.cpp runs the shipping KL_chan_map_capture beside the pre-change
reference and grades the two structures #640 M6 changed with their own
oracles: the flat source table ([ST], every channel entry class resolved by
value) and the commit skid with its beat bank ([SK], back-to-back loopback
beats replayed once each, in order, by value). Each defect below is one those
structures invite: a row decode that drops the half bit, a beat bank whose
write slot never advances (a later beat overwrites one still referenced),
and a commit form that names the wrong sample. The real crossbar is mutated
one defect at a time, the SAME harness is rebuilt through the Makefile's own
recipe (`make lockstep-build` with LS_SRC and LS_MDIR overridden) at both
shapes (4 and 32 pair slots), and both binaries run. Each mutant must make
the harness FAIL by its OWN verdict (a `[FAIL]` line or a tally with
failures, read by scripts/suite_tally.py), and the named check must be among
the failures; a crash or an abort is not a catch. The positive control is
the clean pair `make lockstep` just built (obj_ls1, obj_ls8), re-run here; a
binary older than any input of its recipe is stale and is rebuilt instead of
graded.

What bounds a run. This driver sets no host-time deadline (rule 8's
wall-clock ratchet, scripts/test_evidence.budget item 4). The harness is
cycle-bounded by construction: every case steps a fixed number of cycles and
no loop waits on a DUT output, so a mutant ends at the same cycle as the
clean harness. The host-time bound is the sweep's per-suite guard in
scripts/run_all_suites.sh; the SIGTERM handler turns that kill into an exit
that removes the temporary directory.

Usage: make -C tb/verilator/chmap_capture   (or python3 lockstep_mutants.py from there)
Exit 0 = every mutant was caught and the clean harness still passes.
"""

import signal
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RTL = HERE / "../../../hdl/ieee1722/aaf/KL_chan_map_capture.sv"
CLEAN_MDIR = HERE / "obj_ls"
#: every input of the clean recipe (the Makefile's LSSRCS and the harness,
#: and the Makefile itself): a clean binary older than any of them is stale
CLEAN_INPUTS = [RTL, HERE / "reference/KL_chan_map_capture_ref.sv",
                HERE / "chmap_lockstep_wrap.sv", HERE / "sim_lockstep.cpp",
                HERE / "Makefile"]
EXE_NAME = "Vchmap_lockstep"
SHAPES = ("1", "8")
sys.path.insert(0, str(HERE / "../../../scripts"))
from suite_tally import log_reports_failure  # noqa: E402

# (name, the ONE text it replaces, its replacement, the check it must fail)
MUTATIONS = [
    ("wrong row decode: a TDM entry ignores its half",
     "        SRC_TDM_C : source_row = (32'(idx_f) < N_TDM_PAIRS_C)\n"
     "                                 ? CANDW_C'(CAND_TDM_C + 2 * 32'(idx_f)\n"
     "                                            + 32'(half_f))",
     "        SRC_TDM_C : source_row = (32'(idx_f) < N_TDM_PAIRS_C)\n"
     "                                 ? CANDW_C'(CAND_TDM_C + 2 * 32'(idx_f))",
     "[ST] every channel entry resolves to its own source sample"),
    ("beat slot reused: the beat bank's write slot never advances",
     "        beat_wp_r               <= beat_wp_r + 2'd1;",
     "        beat_wp_r               <= beat_wp_r;",
     "[SK] mono wire, two commits per beat: every event replayed once, in order"),
    ("commit form swapped: a lone even channel commits the beat's first sample",
     "  wire [1:0] cm1_form_w = lb_pair01_w ? CF_SMP0_SMP1_C : CF_SMP1_ZERO_C;",
     "  wire [1:0] cm1_form_w = lb_pair01_w ? CF_SMP0_SMP1_C : CF_SMP0_ZERO_C;",
     "[SK] three-channel wire, stashed and lone channels: every event replayed once, in order"),
]


def build(rtl_path: Path, mdir: Path) -> list[Path] | None:
    """Build the harness at both shapes against `rtl_path` through the suite's
    own recipe; the executables, or None when the recipe failed or left none."""
    out = subprocess.run(
        ["make", "-s", "-C", str(HERE), "lockstep-build", f"LS_SRC={rtl_path}",
         f"LS_MDIR={mdir}"],
        capture_output=True, text=True, check=False)
    exes = [Path(f"{mdir}{shape}") / EXE_NAME for shape in SHAPES]
    if out.returncode != 0 or not all(exe.is_file() for exe in exes):
        sys.stdout.write(out.stdout[-2000:])
        sys.stdout.write(out.stderr[-2000:])
        return None
    return exes


def is_fresh(exes: list[Path]) -> bool:
    """True when every executable exists and is no older than any recipe input."""
    return all(exe.is_file() and all(exe.stat().st_mtime >= src.stat().st_mtime
                                     for src in CLEAN_INPUTS) for exe in exes)


def run_harness(exes: list[Path]) -> tuple[int, str]:
    """(worst rc, joined stdout) of one run of each shape, with no host
    deadline: the harness is cycle-bounded (module docstring)."""
    rcs, outs = [], []
    for exe in exes:
        out = subprocess.run([str(exe)], cwd=str(HERE), capture_output=True,
                             text=True, check=False)
        rcs.append(out.returncode)
        outs.append(out.stdout + out.stderr)
    worst = next((rc for rc in rcs if rc != 0), 0)
    return worst, "\n".join(outs)


def failed_checks(out: str) -> list[str]:
    """The names of the checks the harness printed as failed, in order."""
    return [line.strip()[len("[FAIL]"):].split(" got=")[0].strip()
            for line in out.splitlines() if line.strip().startswith("[FAIL]")]


def verdict(rc: int, out: str, must_fail: str | None) -> str:
    """'pass', 'caught', or why the run is not evidence."""
    reason, failed = log_reports_failure(out)
    if rc == 0 and not failed:
        return "pass"
    if rc == 0 and failed:
        return f"exited 0 but {reason} - a masked verdict is not evidence"
    if failed:
        if must_fail and not any(line.strip().startswith("[FAIL]") and must_fail in line
                                 for line in out.splitlines()):
            return f"failed, but not the named check ({must_fail!r})"
        return "caught"
    if rc < 0:
        return f"died by signal {-rc} with no harness verdict - a crash is not a catch"
    return f"exited {rc} with no harness verdict - a DUT abort is not a catch"


def run_mutant(src: str, mutation: tuple[str, str, str, str], work: Path) -> bool:
    """Plant one mutation, build and run the harness; True when it was caught."""
    name, pattern, replacement, breaks = mutation
    if src.count(pattern) != 1:
        print(f"[FAIL] mutation {name!r}: its pattern appears {src.count(pattern)} "
              f"time(s) in {RTL.name}, expected exactly 1. The RTL moved and this "
              f"mutant is no longer mutating anything - fix the pattern, do not delete the arm.")
        return False
    tag = name.split(":")[0].replace(" ", "_")
    mpath = work / f"KL_chan_map_capture_{tag}.sv"
    mpath.write_text(src.replace(pattern, replacement))
    exes = build(mpath, work / f"obj_{tag}")
    if exes is None:
        print(f"[FAIL] mutation {name!r} did not compile; a mutant that cannot build "
              f"proves nothing about the harness")
        return False
    rc, out = run_harness(exes)
    answer = verdict(rc, out, breaks)
    if answer == "caught":
        broke = failed_checks(out)
        print(f"[PASS] mutant caught: {name} - breaks \"{breaks}\"")
        print(f"    it broke {len(broke)} check(s): {'; '.join(broke)}")
        return True
    if answer == "pass":
        print(f"[FAIL] mutant SURVIVED: {name}. The harness does not prove \"{breaks}\".")
    else:
        print(f"[FAIL] mutant {name!r} {answer}")
    return False


def main() -> int:
    """Run the positive control and every mutant; 1 if any mutant survived."""
    def on_sigterm(*_: object) -> None:
        """Exit on a kill so the temporary directory is removed."""
        sys.exit(143)

    signal.signal(signal.SIGTERM, on_sigterm)
    src = RTL.read_text()
    passes = 0
    fails = 0
    with tempfile.TemporaryDirectory(prefix="chmap-lockstep-mutants-") as td:
        work = Path(td)
        exes: list[Path] | None = [Path(f"{CLEAN_MDIR}{shape}") / EXE_NAME for shape in SHAPES]
        if not is_fresh(exes):
            print(f"[INFO] {CLEAN_MDIR.name}1/{CLEAN_MDIR.name}8 are missing or older than "
                  f"their sources: the positive control is rebuilt")
            exes = build(RTL, work / "obj_clean")
        answer = verdict(*run_harness(exes), None) if exes else "did not compile"
        if answer == "pass":
            passes += 1
            print("[PASS] the unmutated crossbar still passes the lockstep harness")
        else:
            fails += 1
            print(f"[FAIL] the unmutated crossbar does NOT pass ({answer}) - every "
                  f"mutant result is meaningless")
        for mutation in MUTATIONS:
            if run_mutant(src, mutation, work):
                passes += 1
            else:
                fails += 1
    print(f"\n{passes + fails} checks: {passes} PASS, {fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())

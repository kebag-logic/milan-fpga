#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Drive syn/yosys/ooc.sh's refusals, automatically, on planted failures.

That script's exit status is the gate (#245): a top that fails sv2v or yosys,
a ROM generator that fails or emits an empty, truncated, one-word, malformed
or WRONG-CONTENT image (sha256 against the pin-keyed rom_digests.tsv), a
staging or publication step that fails, a report phase that cannot produce a
real row, and a requested top that matches nothing must each leave a
non-zero exit - and one failed top stays failed however many later tops
pass. Three review rounds shaped this file; each one's counterexamples are
arms below, named for what they plant.

WHAT IT RUNS IS THE REAL ooc.sh, not a copy of its logic. The plants ride
seams the script already has: it resolves `sv2v`, `yosys`, `awk` and
`python3` through PATH after prepending `$HOME/.local/bin`, so each arm runs
it with HOME pointing at a scratch directory whose `.local/bin` carries the
planted tool (the same directory is also put first on PATH directly). The
ROM generators, the geometry packages and scripts/pp_srcs.py run for real
through a dispatching `python3` stub, so the generation path the positive
arms prove is the shipping one.

THE STUBS ARE MODELS WITH TEETH, not silence:

  - the sv2v model RECORDS every argument it is handed, and the positive
    `KL_pp_shadow` arm requires the source set to EQUAL the authoritative
    population (pp_srcs.py's own answer plus the parent's named files) - so
    a recipe whose processor list stops being derived cannot stay green;
  - the yosys model refuses to run anywhere but an exclusive per-top
    `*.run.*` directory under `$OOC_TMP` (the shared `$OOC_TMP` itself is a
    refusal too, [R0] round four), refuses a run directory that is still
    WRITABLE (rename authority is directory write permission, [R0] round
    five), refuses a missing or WRITABLE canonical
    `ucode.hex`/`ltn_rom.hex`/`gptp_ucode.hex` regular file in its cwd, and
    asserts each
    image's sha256 against the pin's ledger row - the exact-byte oracle the
    round-four review required, so consuming unvouched bytes is a red arm
    even if every ooc.sh-side re-hash were deleted;
  - a transient-swap model performs [R0] round five's exact exploit (move
    the reviewed image aside, feed different bytes, restore before the
    post-run hash) and reports whether the rename was POSSIBLE - blocked
    on the shipping script, demonstrated to price wrong bytes on the
    mutant that forgets the directory lock;
  - the ledger pin is the SUPERPROJECT gitlink, and a planted stale
    submodule HEAD (a dispatching git stub) must refuse in normal AND
    record modes ([R0] round five);
  - its mapped stat block carries EVERY cell class the parser reports
    (LUT, LUTRAM via RAM32M, FF, RAMB36, RAMB18, DSP, CARRY4), and the
    clean arm compares EVERY column of the printed row, so a zeroed
    accumulator in any column is caught;
  - stat blocks appear only when the -p command carries their source,
    mapped cells only from `synth_xilinx`, JSON only from `write_json`, and
    an empty JSON artifact is its own arm;
  - the yosys and sv2v models can RECORD the LD_PRELOAD they ran under, so
    the allocator preload (#290) is proved to reach yosys and not the front
    end, and `YOSYS_MALLOC=none` to clear an inherited one for yosys only -
    with libc as the fixture library, so no compiler and no jemalloc are
    needed, and a mutant that exports the preload once for every child is
    caught.

Mutation copies of ooc.sh itself (report-phase deletions, the population
replaced by a hand list, `cd "$TMP"` -> `cd "$R"`, the digest ledger
detached, the geometry source swapped for planted packages) prove each
detector can fail. Real synthesis is NOT run here; the real-toolchain run is
recorded on the PR that lands a change.

    python3 syn/yosys/ooc_selftest.py

Runs in .github/workflows/rtl-fast.yml beside syn/ooc/ooc_tcl_selftest.py;
the invocation AND its step keys are pinned by scripts/ci_events.py. Needs
both processor submodules; it does not need yosys or sv2v.
"""
import os
import sys

from ooc_arms import ARMS, run_all
from ooc_harness import Suite


def selftest() -> tuple[list[str], int]:
    """What the arms failed to prove, and how many of them ran.

    The ran count is returned, not just printed, because the arm total is
    itself an assertion: a suite that quietly stops running arms exits green,
    and a planted failure nobody drives is a defense that has rotted.
    """
    suite = Suite()
    problems = suite.problems
    run_all(suite)
    if suite.ran != ARMS:
        problems.append("SELF-TEST FAILED [arm-count]: ran %d arm(s), this "
                        "file declares %d." % (suite.ran, ARMS))
    return problems, suite.ran


def main() -> int:
    """The gate's exit status: 0 only when every declared arm proved its refusal.

    Running as root is its own refusal rather than a run, because the custody
    oracles below are mode bits and root bypasses every one of them.
    """
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        print("ooc.sh refusal self-test: REFUSED - this suite's custody "
              "oracles are mode bits (`test -w`, rename in a u-w directory), "
              "and root bypasses every one of them: the locked run directory "
              "reads as writable and the transient swap succeeds, so the "
              "arms would invert rather than fail. Run it unprivileged.",
              file=sys.stderr)
        return 2
    try:
        bad, ran = selftest()
    except AssertionError as e:
        print("ooc.sh refusal self-test: SETUP REFUSED - %s" % e,
              file=sys.stderr)
        return 2
    for b in bad:
        print("  -", b, file=sys.stderr)
    if bad:
        return 2
    print("ooc.sh refusal self-test: %d arm(s) passed" % ran)
    return 0


if __name__ == "__main__":
    sys.exit(main())

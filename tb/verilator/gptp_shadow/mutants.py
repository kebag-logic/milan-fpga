#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The defect controls the plane-slice suite owns.

WHY THIS EXISTS. A green suite and a suite that cannot go red look the same
from the outside. Each control below plants ONE defect the design is
supposed to refuse, requires this suite to notice, and writes only private
source/build copies. Caller sources are never modified, even under KILL. A control that leaves the suite
green is a finding about the suite, and is reported as one.

WHAT IS HERE AND WHAT IS NOT. The plane's own laws: what a ledger entry is
and when it may be resolved, what a barrier destroys, what discharges a
recovery demand, and which measured terms the egress reconstruction is made
of. The defects that need the SHIPPING MAC and the two real seams - the
observation point itself and the register stages between the launch and the
capture - live with `tb/verilator/gptp_txts`, which pays for a converted MAC
to carry them.

Each control names the check it must break, and the run prints whether that
check really failed rather than only that something did.

Usage:
    python3 mutants.py            # every control
    python3 mutants.py --list     # name them and change nothing

Exit 0 = every control was caught and private work was cleaned; 1 = a control
was not caught; 2 = input or cleanup refusal; 130/143 = handled INT/TERM.
KILL can leave private scratch/children, but cannot modify caller source.
"""

import argparse
import re
import tempfile
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from owned_process import Cancelled, OwnedProcesses  # noqa: E402
from private_inputs import InputRefused, copy_inputs  # noqa: E402

PLANE = REPO / "hdl" / "ieee8021as" / "gptp_plane"
RET = PLANE / "KL_gptp_txret.sv"
OBS = PLANE / "KL_gptp_gmii_launch.sv"
TIC = PLANE / "KL_gptp_txticket.sv"

#: (name, file, old text, new text, the check this must break)
MUTATIONS = [
    (
        "abort_counts_as_completion",
        RET,
        "if (epi_done_i && epi_cover_r) begin",
        "if ((epi_done_i || !epi_busy_i) && epi_cover_r) begin",
        "aborted episode: the demand survives it",
    ),
    (
        #: The WHOLE predicate, because its two terms are not separately
        #: observable: `gen_r` is 1..max by construction, so dropping the
        #: `!= 0` term alone still refuses generation zero. That term
        #: guards against a generation this design never produces, and it
        #: is kept as exactly that.
        "no_generation_check",
        RET,
        "assign gen_ok_w     = (cap_gen_r != '0) && (cap_gen_r == gen_r);",
        "assign gen_ok_w     = 1'b1;",
        "generation zero: the ledger refused it and raised a barrier",
    ),
    (
        "no_tag_check",
        RET,
        "  assign tag_ok_w     = cap_abort_r\n"
        "                     || ((cap_type_r == led_type_r[led_head_r]) &&\n"
        "                         (cap_seq_r  == led_seq_r [led_head_r]));",
        "  assign tag_ok_w     = 1'b1;",
        "foreign tag: the ledger refused it and raised a barrier",
    ),
    (
        #: THE EXPIRY ITSELF. Retiring the head on age cannot be written as
        #: a local edit that compiles - `age_hit_w` is declared after the
        #: ledger block that would have to read it - so the control here is
        #: the expiry NOT BEING NOTICED, which is the same machinery seen
        #: from the other side. That an expiry is not a retirement is
        #: carried by the phase below and, structurally, by the
        #: `push_res_w` line `scripts/check_gptp_docs.py` pins.
        "age_never_expires",
        RET,
        "  assign age_hit_w = (n_led_r != OCC_W_C'(0)) &&",
        "  assign age_hit_w = 1'b0 && (n_led_r != OCC_W_C'(0)) &&",
        "aged head: the age expired and was counted",
    ),
    (
        "observer_latency_off_by_one",
        RET,
        "parameter int unsigned OBS_LAT_E_CYC_P  = 2,",
        "parameter int unsigned OBS_LAT_E_CYC_P  = 1,",
        "launch: the reconstruction is the launch instant",
    ),
    (
        "crossing_latency_off_by_one",
        RET,
        "parameter int unsigned CDC_LAT_D_CYC_P  = 2,",
        "parameter int unsigned CDC_LAT_D_CYC_P  = 3,",
        "launch: the reconstruction is the launch instant",
    ),
    (
        "no_fence",
        RET,
        "        egress_hold_o <= 1'b1;\n        n_pre_v_r     <= 1'b0;",
        "        egress_hold_o <= 1'b0;\n        n_pre_v_r     <= 1'b0;",
        "torn frame: a frame was mid-egress when the fence closed",
    ),
    (
        "unseal_without_echo",
        RET,
        "n_pre_v_r & echo_ok_r;",
        "n_pre_v_r;",
        "echo: the seal outlasts it",
    ),
    (
        "credit_never_withheld",
        TIC,
        "assign tx_credit_o = ~credit_hold_i &",
        "assign tx_credit_o = 1'b1 | ~credit_hold_i &",
        "credit: the engine is held off at the reserve",
    ),
]


#: DEFECTS THIS SUITE CANNOT SEE, and why. Every one of them is a real
#: change to a real line, and every one of them leaves this suite green -
#: which is a fact about the suite and about the design, recorded here
#: rather than hidden by deleting the control. Each names where the law it
#: defends IS carried. `--list` prints them, and `main()` refuses a stale
#: entry: the anchor has to still be in the source, or the reason below has
#: stopped describing anything.
NOT_SEPARATELY_OBSERVABLE = [
    (
        "abort_outranks_completion",
        RET,
        "      if (!epi_busy_i && !epi_done_i)     epi_cover_r <= 1'b0;",
        "the two arms it reorders never apply on the same edge: the guard's "
        "`epi_busy_o` is already high on the cycle its start pulse is "
        "published, so the ordering is defence against an edge this guard "
        "cannot produce. The LAW - an aborted episode is not a completion - "
        "is carried by `abort_counts_as_completion` above.",
    ),
    (
        "no_departure_predicate",
        RET,
        "have_entry_w & departed_w & tag_ok_w;",
        "a record cannot reach the ledger before its frame is on the wire, "
        "so removing the predicate changes only WHEN an entry resolves "
        "relative to the departure it is already behind, and no interface "
        "here observes that order. Pinned structurally in "
        "scripts/check_gptp_docs.py, on the USE in `resolve_w` and not only "
        "on the declaration: until #360 round three the pin was the first "
        "line of that expression and the term is on the second, so the "
        "sentence above was true of a token that did not hold it.",
    ),
    (
        "no_position_check",
        RET,
        "assign oidx_ok_w    = (cap_oidx_r == exp_oidx_r);",
        "the position and the tag are two independent cross-checks on one "
        "fact, and every single-record anomaly this bench can produce - a "
        "lost record, a reset observer, a corrupted field - trips the tag "
        "as well, so the position cannot be isolated behaviourally. Pinned "
        "structurally in scripts/check_gptp_docs.py.",
    ),
    (
        "delta_forced_not_measured",
        OBS,
        "(delta_r != TXTS_DELTA_W_P'(TXTS_DELTA_EXP_P))};",
        "this slice's framer emits only whole frames, so the measured "
        "distance is always the expected one. CARRIED, with a fragment "
        "injected on the wire, by tb/verilator/gptp_txts/mutants.py.",
    ),
    (
        "eof_acceptance_unqualified",
        TIC,
        "assign alloc_w = beat_w & tx_eof_i;",
        "the allocation seam is the ENGINE's byte face into the plane, and "
        "this bench can stall the plane's egress lane but not that face "
        "independently, so an offered-but-unaccepted EOF beat cannot be "
        "produced here. Pinned structurally in scripts/check_gptp_docs.py.",
    ),
    (
        "cancellation_frees_the_entry",
        RET,
        "        for (int unsigned li = 0; li < TXTS_CAP_N_P; li++) "
        "led_live_r[li] <= 1'b0;",
        "every barrier this bench can raise has an empty pre-fence prefix "
        "at the fence, so forgetting the entries and marking them not-live "
        "lead to the same observable close. Pinned structurally in "
        "scripts/check_gptp_docs.py.",
    ),
]

#: This suite counts in its own shape - `N checks: X PASS, Y FAIL`, with one
#: `FAIL <label> got ... exp ...` line per broken check - so this driver
#: reads THAT, and the process status beside it. A driver that grepped for
#: another suite's tally would report every control as uncaught.
TALLY_RE = re.compile(r"^\d+ checks: \d+ PASS, (\d+) FAIL", re.M)


def run_suite(here: Path, owner: OwnedProcesses) -> tuple[int, str]:
    """Build in private scratch, then stop/reap all owned build descendants."""
    return owner.run(["make", "-s", "run"], cwd=here)


def suite_failed(status: int, output: str) -> bool:
    """Did the suite report a failure, rather than merely not finish?

    A non-zero status alone is not it: a build that did not compile also
    exits non-zero and proves nothing about the check the control aims at.
    A tally with a non-zero FAIL count is the suite noticing.
    """
    tally = TALLY_RE.search(output)
    if tally is not None:
        return int(tally.group(1)) != 0
    return False


def apply_control(path: Path, old: str, new: str) -> bool:
    """Plant one defect. False when its anchor is no longer in the source,
    which is a finding about this file and not a passing control."""
    text = path.read_text(encoding="utf-8")
    if old not in text:
        return False
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def main() -> int:
    """Run every control, or list them."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--list", action="store_true",
                        help="name the controls and change nothing")
    args = parser.parse_args()

    if args.list:
        for name, path, _old, _new, expect in MUTATIONS:
            print(f"{name:34s} {path.relative_to(REPO)}  -> {expect}")
        for name, path, _old, why in NOT_SEPARATELY_OBSERVABLE:
            print(f"{name:34s} {path.relative_to(REPO)}  -> NOT SEEN HERE: "
                  f"{why}")
        return 0

    try:
        with OwnedProcesses() as owner:
            with tempfile.TemporaryDirectory(prefix="gptp-shadow-mutants-") as scratch:
                private = Path(scratch)
                copy_inputs(REPO, private, owner)
                failures = campaign(private, owner)
            owner.checkpoint()
        print(f"controls: {len(MUTATIONS)}   failures: {failures}")
        print(f"RESULT: {'PASS' if failures == 0 else 'FAIL'}")
        return 1 if failures else 0
    except Cancelled as exc:
        print(f"CANCELLED: signal {exc.signum}; no mutation verdict", file=sys.stderr)
        return 128 + exc.signum
    except (InputRefused, OSError, RuntimeError) as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2


def campaign(private: Path, owner: OwnedProcesses) -> int:
    """Run the original mutation population against private source bytes."""
    failures = 0
    for name, original, old, new, expect in MUTATIONS:
        owner.checkpoint()
        path = private / original.relative_to(REPO)
        pristine = path.read_bytes()
        if not apply_control(path, old, new):
            print(f"[FAIL] {name}: its anchor is no longer in "
                  f"{original.relative_to(REPO)}")
            failures += 1
            continue
        status, output = run_suite(private / HERE.relative_to(REPO), owner)
        path.write_bytes(pristine)
        caught = suite_failed(status, output)
        named = any(line.startswith("FAIL " + expect)
                    for line in output.splitlines())
        #: the checks this control really broke, so the expectation above is
        #: readable evidence rather than a claim
        broke = [line[len("FAIL "):].split(" got ")[0].strip()
                 for line in output.splitlines() if line.startswith("FAIL ")]
        if caught and named:
            print(f"[ ok ] {name}: caught by \"{expect}\"")
        elif caught:
            print(f"[ ok ] {name}: caught, though not by \"{expect}\"; "
                  f"broke {sorted(set(broke))[:3]}")
        else:
            reason = "the suite stayed green" if TALLY_RE.search(output) else "no completed suite tally"
            print(f"[FAIL] {name}: {reason} (make exit {status})")
            failures += 1

    #: A RECORDED REASON HAS TO STILL DESCRIBE SOMETHING. Each defect this
    #: suite cannot see is still a line in the source; if the line has gone,
    #: the reason has gone with it and the entry is a stale claim.
    for name, original, old, _why in NOT_SEPARATELY_OBSERVABLE:
        path = private / original.relative_to(REPO)
        if old not in path.read_text(encoding="utf-8"):
            print(f"[FAIL] {name}: recorded as not separately observable, "
                  f"but its anchor is no longer in {original.relative_to(REPO)}")
            failures += 1
        else:
            print(f"[note] {name}: not separately observable here")

    return failures


if __name__ == "__main__":
    sys.exit(main())

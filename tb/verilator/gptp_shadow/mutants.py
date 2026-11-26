#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""The defect controls the plane-slice suite owns.

WHY THIS EXISTS. A green suite and a suite that cannot go red look the same
from the outside. Each control below plants ONE defect the design is
supposed to refuse, requires this suite to notice, and writes only private
copies of the files the build reads (`make print-inputs`). Caller sources are
never modified, even under KILL.
A control that leaves the suite green is a finding about the suite, and is
reported as one.

WHAT IS HERE AND WHAT IS NOT. The plane's own laws: what a ledger entry is
and when it may be resolved, what a barrier destroys, what discharges a
recovery demand, and which measured terms the egress reconstruction is made
of. The defects that need the SHIPPING MAC and the two real seams - the
observation point itself and the register stages between the launch and the
capture - live with `tb/verilator/gptp_txts`, which pays for a converted MAC
to carry them. Two more restore defects of the pinned engine the parent
adopted a repair for: the first master Announce waiting for a beat
(FPGA-gPTP #106), and a mastership keeping a settled slave's rate (#107).
A third drops the Announce leg's transmit-credit gate. One more is planted
in this suite's own harness: its lane, held across the race, delivers the
master Announce only after the re-election. It shows the race check grades
that order, not only that the Announce exists.

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
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
sys.path.insert(0, str(REPO / "scripts"))
from owned_process import Cancelled, OwnedProcesses  # noqa: E402
from private_inputs import InputRefused, copy_inputs  # noqa: E402
import mutant_stage  # noqa: E402

PLANE = REPO / "hdl" / "ieee8021as" / "gptp_plane"
RET = PLANE / "KL_gptp_txret.sv"
OBS = PLANE / "KL_gptp_gmii_launch.sv"
TIC = PLANE / "KL_gptp_txticket.sv"
#: The pinned engine and its micro-code generator. The two controls on them
#: restore the defects FPGA-gPTP #106 and #107 repaired, with the donor's
#: own anchors (its p106_mutants.py and p107_mutants.py), so this platform
#: suite is shown to notice the adopted behaviour, not only the donor's.
ENGINE = REPO / "gptp-processor" / "hdl" / "top" / "KL_gptp_engine.sv"
GENERATOR = REPO / "gptp-processor" / "hdl" / "ucode" / "gen_gptp_ucode.py"
#: SELF's tail, which continues into ANNTX since #106
SELF_TAIL = ("    p.emit(\"COMMIT\")\n"
             "    p.emit(\"BR\", label=LB[\"ANNTX\"])\n")
#: BECOME's Sync arm, behind which the old engine also armed the Announce beat
BECOME_SYNC = ("    p.emit(\"WRST\", ra=RT, imm=RG_TMR | 1, fmt=FMT_Q)"
               "  # sync now\n")
#: ANNTX's gates, whose credit gate the third control drops
ANNTX_GATES = ("    e_flag_gate(p, FL_ASCAP_C, FL_ASCAP_C, \"ac\", \"skip\")\n"
               "    e_credit_gate(p, \"skip\")\n"
               "    p.emit(\"RDST\", rd=RA, imm=RG_SCR | S_ASEQ, fmt=FMT_Q)\n")
#: this suite's own harness, and the race arm's queued Announce in it
HARNESS = HERE / "sim_main.cpp"
RACE_ANNOUNCE = ("        run_to(t0 + a1_after);\n"
                 "        announce(tk_seq++, 100, GMID, PEER_CID, 0x00);\n")
#: the engine's PHC word-3 rate write
WORD3 = ("                phc_addend_we_o <= 1'b1;\n"
         "                phc_addend_o    <= st_wdata_w[31:0];\n"
         "                phc_slew_left_r   <= 2'd0;\n")

#: (name, file, old text, new text, the check this must break). A control
#: that edits two places gives a tuple of old texts and one of new texts.
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
        "                     || ((cap_type_r == led_head_type_w) &&\n"
        "                         (cap_seq_r  == led_head_seq_w));",
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
    (
        #: #106's defect: the first master Announce waits 2 ms for a beat,
        #: so an Announce queued at the receipt timeout instant re-elects
        #: first and disarms it
        "first_master_announce_waits_for_a_beat",
        GENERATOR,
        (SELF_TAIL, BECOME_SYNC),
        ("    p.emit(\"COMMIT\")\n    p.emit(\"END\")\n",
         BECOME_SYNC + "    p.emit(\"MOVE\", rd=RT, ra=0, imm=2)\n"
                       "    p.emit(\"WRST\", ra=RT, imm=RG_TMR | 3, fmt=FMT_Q)\n"),
        "#106 race: one master Announce reaches the lane before the re-election",
    ),
    (
        #: #107's defect: word 3 applies only while a slew is active, so a
        #: settled slave's trim outlives its mastership
        "word3_applies_only_during_a_slew",
        ENGINE,
        WORD3,
        "                if (phc_slew_active_o) begin\n"
        "                  phc_addend_we_o <= 1'b1;\n"
        "                  phc_addend_o    <= st_wdata_w[31:0];\n"
        "                end\n"
        "                phc_slew_left_r   <= 2'd0;\n",
        "#107 settled +100 ppm: the mastership's PHC rate is this oscillator's, 0",
    ),
    (
        #: the Announce leg without its credit gate: with the credit
        #: withheld by the ticket reserve, which no fence backs, the first
        #: master Announce then reaches the lane
        "announce_leg_ignores_the_credit",
        GENERATOR,
        ANNTX_GATES,
        ANNTX_GATES.replace("    e_credit_gate(p, \"skip\")\n", ""),
        "#106 reserve: no master Announce reaches the lane without credit",
    ),
    (
        #: the bench's lane held from before the takeover until the queued
        #: Announce is sent: the master Announce still leaves, but its last
        #: beat follows the re-election
        "master_announce_reaches_the_lane_after_the_re_election",
        HARNESS,
        RACE_ANNOUNCE,
        "        dut->tx_tready_i = 0;\n" + RACE_ANNOUNCE +
        "        dut->tx_tready_i = 1;\n",
        "#106 race: one master Announce reaches the lane before the re-election",
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


def planted(text: str, old: str | tuple[str, ...],
            new: str | tuple[str, ...]) -> str | None:
    """The text with one control's edits made, each anchor's first
    occurrence; None when an anchor is no longer in it."""
    pairs = zip(old, new, strict=True) if isinstance(old, tuple) else [(old, new)]
    for anchor, replacement in pairs:
        if anchor not in text:
            return None
        text = text.replace(anchor, replacement, 1)
    return text


def apply_control(path: Path, old: str | tuple[str, ...],
                  new: str | tuple[str, ...]) -> bool:
    """Plant one defect. False when an anchor is no longer in the source,
    which is a finding about this file and not a passing control."""
    text = planted(path.read_text(encoding="utf-8"), old, new)
    if text is None:
        return False
    path.write_text(text, encoding="utf-8")
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
            with mutant_stage.directory("gptp-shadow-mutants-") as scratch:
                private = Path(scratch)
                targets = {row[1] for row in MUTATIONS + NOT_SEPARATELY_OBSERVABLE}
                copy_inputs(REPO, HERE, private, owner, targets)
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

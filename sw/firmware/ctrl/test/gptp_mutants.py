#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gptp_mutants.py - planted defects of the firmware gPTP end station port, each caught by its test (#665 F6, #884).

Each defect replaces one exact text of gptp/gptp.c or gptp/gptp.h in a scratch copy of the port, builds its arm
on that copy (gptp_arms.arm_gptp, or arm_gptp_ubsan for undefined behaviour) and requires each named test to fail
with its named words on a [FAIL] line. A defect whose text is not found exactly once, or that builds and passes,
or that fails only elsewhere, fails the campaign. The unplanted copy must pass first, so a broken baseline is never
read as a kill.

usage: gptp_mutants.py [--build-dir DIR] [--jobs N]
"""

from __future__ import annotations

import argparse
import shutil
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parents[1] / "gtest")]

import fw_gtest  # noqa: E402
import gptp_arms  # noqa: E402
from ctrl_build import CTRL, Refusal, Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402

C = "gptp/gptp.c"
H = "gptp/gptp.h"
ARM = "gptp"
#: The arms a planted defect is graded on, by the name its Mutant gives: the unplanted port passes every one.
ARMS = {"gptp": gptp_arms.arm_gptp, "gptp_ubsan": gptp_arms.arm_gptp_ubsan}

MUTANTS = (
    Mutant("ascap-after-one", H, "#define GPTP_ASCAP_UP 2u", "#define GPTP_ASCAP_UP 1u", ARM,
           "Scripted.AsCapableNeedsTwoGoodInARow", "asCapable after one good exchange with a rate"),
    Mutant("lost-clears-at-fourth", C, "if (p->pd.lost <= GPTP_LOST_ALLOWED)", "if (p->pd.lost < GPTP_LOST_ALLOWED)",
           ARM, "Scripted.FifthLostResponseClearsAsCapable", "asCapable fell at the fourth lost response"),
    Mutant("npd-threshold-exclusive", C, "p->pd.delay_ns > GPTP_NPD_HI_NS", "p->pd.delay_ns >= GPTP_NPD_HI_NS", ARM,
           "Scripted.DelayOverThresholdIsNotAsCapable", "800 ns is at the threshold, inside it"),
    Mutant("late-bound-exclusive", C, "p->pd.t4 - p->pd.t1 > GPTP_PD_LATE_NS", "p->pd.t4 - p->pd.t1 >= GPTP_PD_LATE_NS",
           ARM, "Scripted.LateResponseIsLost", "a response at the bound was refused"),
    Mutant("nrr-inverted", C, "fast = s3 >= s4;", "fast = s3 < s4;", ARM,
           "Scripted.RateRatioAndDelayWithAFastNeighbor", "neighborRateRatio"),
    Mutant("delay-without-nrr", C, "d = (int64_t)rtt + (((int64_t)rtt * p->pd.nrr_q32) >> 32) - (int64_t)turn;",
           "d = (int64_t)rtt - (int64_t)turn;", ARM,
           "Scripted.RateRatioAndDelayWithAFastNeighbor", "the delay ignores the neighbor's rate"),
    Mutant("cease-one-late", C, "if (++p->pd.multi_run >= GPTP_CEASE_N) {", "if (++p->pd.multi_run > GPTP_CEASE_N) {",
           ARM, "Scripted.MultipleRespondersCeaseAndALinkToggleResumes", "Pdelay_Req still sent during the cease"),
    Mutant("cease-survives-link-toggle", C, "\tp->pd.ceased = false;     // each link edge", "\t// each link edge", ARM,
           "Scripted.MultipleRespondersCeaseAndALinkToggleResumes", "the link toggle did not end the cease"),
    Mutant("bmca-inverted", C, "if (p->ann.valid && vector_cmp(&p->ann.v, &own) < 0) {",
           "if (p->ann.valid && vector_cmp(&p->ann.v, &own) > 0) {", ARM,
           "Scripted.BetterAnnounceMakesASlave", "10.3.5: priority1 100 is better than 248"),
    Mutant("path-loop-kept", C, "if (id == p->cfg.clock_id) {", "if (0) {", ARM,
           "Scripted.LoopedPathAndStepsRemoved255AreDiscarded", "a path holding thisClock was used"),
    Mutant("sync-timeout-500", H, "#define GPTP_SYNC_RTO_MS 375u", "#define GPTP_SYNC_RTO_MS 500u", ARM,
           "Scripted.SyncReceiptTimeoutAgesTheGrandmaster", "no pair for 375 ms did not age the grandmaster"),
    Mutant("sync-any-source", C,
           "if (p->role != GPTP_ROLE_SLAVE || memcmp(f + F_SRC, p->ann.v.src, 10))\n\t\treturn;   // Sync only",
           "if (p->role != GPTP_ROLE_SLAVE)\n\t\treturn;   // Sync only", ARM,
           "Scripted.SyncFromAnotherPortIsIgnored", "another port's Sync displaced the master's pending Sync"),
    Mutant("linkup-threshold-lost", C, "p->srv.linkup ? GPTP_STEP_LINKUP_NS : GPTP_STEP_LOCKED_NS",
           "GPTP_STEP_LOCKED_NS", ARM,
           "Scripted.FirstPairStepsAtTheLinkUpThreshold", "an offset over 20 us at link-up did not step"),
    Mutant("step-sign", C, "int64_t delta = (int64_t)(0u - (uint64_t)offset);", "int64_t delta = offset;", ARM,
           "Scripted.FirstPairStepsAtTheLinkUpThreshold", "the step is not the offset, negated"),
    Mutant("p-term-sign", C, "clamp64((p->srv.integ - kp * offset) >> 16, lim)",
           "clamp64((p->srv.integ + kp * offset) >> 16, lim)", ARM,
           "Scripted.LockedThresholdSlewsUnder100us", "local ahead: the trim must slow it"),
    Mutant("trim-unclamped", C, "clamp64((p->srv.integ - kp * offset) >> 16, lim)",
           "clamp64((p->srv.integ - kp * offset) >> 16, 4 * lim)", ARM,
           "Scripted.TrimNeverLeavesTheEnvelope", "the trim left the 200 ppm envelope"),
    Mutant("slow-loop", C, "#define GKP_Q16 41943", "#define GKP_Q16 10486", ARM,
           "Net.LockTimeHoldsTheFabricBench", "the 24th pair's offset is not under 150 ns"),
    Mutant("follow-up-origin-zero", C, "send_follow_up(p, seq, ns);", "send_follow_up(p, seq, 0);", ARM,
           "Scripted.BecomesGrandmasterAndSendsSyncFollowUpAnnounce",
           "preciseOriginTimestamp is not the Sync's egress stamp"),
    Mutant("resp-t2-zero", C, "gptp_ts_put(p->tx + F_BODY, p->rsp.t2);", "gptp_ts_put(p->tx + F_BODY, 0);", ARM,
           "Scripted.ResponderAnswersWithBothTimestamps", "requestReceiptTimestamp is not the ingress stamp"),
    Mutant("announce-before-ascapable", C, "if (!p->link || !p->pd.as_capable) {\n\t\tbecome(p, GPTP_ROLE_DISABLED);",
           "if (!p->link) {\n\t\tbecome(p, GPTP_ROLE_DISABLED);", ARM,
           "Scripted.NoAnnounceOrSyncBeforeAsCapable", "Announce before asCapable"),
    Mutant("sync-250ms", H, "#define GPTP_SYNC_MS 125u", "#define GPTP_SYNC_MS 250u", ARM,
           "Scripted.BecomesGrandmasterAndSendsSyncFollowUpAnnounce", "Milan v1.2 Table 4.1: Sync each 125 ms"),
    Mutant("late-stamp-unpaired", C, "} else if (msg_type == GPTP_MSG_PDELAY_REQ && p->rsp.resp_owed",
           "} else if (0 && msg_type == GPTP_MSG_PDELAY_REQ && p->rsp.resp_owed", ARM,
           "Scripted.ResponderTakesAStampThatComesAfterItsFrame", "a stamp read after its frame was never paired"),
    Mutant("slave-timer-stale", C, "\t\tp->slv.last_ms = p->now_ms;   // the sync receipt timer starts",
           "\t\tp->slv.last_ms = p->slv.last_ms;   // the sync receipt timer starts",
           ARM, "Net.SlaveLocksToTheGrandmaster", "not inside 100 ns of the grandmaster by 15 s"),
    Mutant("own-frames-used", C, "if (from_self(p, frame))\n\t\treturn;", "if (from_self(p, frame) && 0)\n\t\treturn;",
           ARM,
           "Scripted.OwnResponseIsIgnored", "asCapable from its own responses"),
    Mutant("sync-alone-renews-deadline", C, "\tp->slv.rx_ms = p->now_ms;     // a Sync alone renews",
           "\tp->slv.rx_ms = p->slv.last_ms = p->now_ms;     // a Sync alone renews", ARM,
           "Scripted.SyncWithoutItsFollowUpLetsTheGrandmasterAge", "720 ms of Sync without Follow_Up kept the master",
           also=((ARM, "Scripted.SyncWithoutItsFollowUpClearsTheVerdictOfAPortThatIsNeverGrandmaster",
                  "720 ms of Sync without Follow_Up kept the verdict"),
                 (ARM, "Scripted.SyncAndAnnounceWithoutFollowUpNeverHoldTheVerdict",
                  "kept a slave with the verdict past the timeout"))),
    Mutant("follow-up-timeout-500", H, "#define GPTP_FU_RTO_MS 125u", "#define GPTP_FU_RTO_MS 500u", ARM,
           "Scripted.AFollowUpPastItsReceiptTimeoutIsNoPair", "a Sync waited past its followUpReceiptTimeout"),
    Mutant("pair-renews-no-deadline", C, "\tp->slv.last_ms = p->now_ms;\n\tservo_pair(", "\tservo_pair(", ARM,
           "Scripted.AnnounceReceiptTimeoutAgesTheMaster", "aged before 3 s"),
    Mutant("follow-up-without-tlv-used", C, "\tif (!tlv_ok) {", "\tif (plen < LEN_FU - 32u) {", ARM,
           "Scripted.FollowUpWithoutItsInformationTlvIsNoPair", "information TLV is absent was used",
           also=((ARM, "Scripted.FollowUpWithoutItsInformationTlvIsNoPair",
                  "a refused Follow_Up renewed the sync receipt deadline"),)),
    Mutant("follow-up-tlv-fields-unchecked", C, "return plen >= LEN_FU && get16(tlv) == 0x0003u",
           "return plen >= LEN_FU && (get16(tlv) == 0x0003u || 1)", ARM,
           "Scripted.FollowUpWithoutItsInformationTlvIsNoPair", "information TLV is of another type was used"),
    Mutant("late-second-responder-ignored", C, "\t\t\tpd_multi(p, f + F_SRC, p->pd.done_responder);\n",
           "\t\t\t(void)f;\n", ARM,
           "Scripted.ASecondResponderAfterTheFirstsFollowUpStillCeases", "the second late, did not cease"),
    Mutant("run-survives-a-clean-request", C, "\tif (!p->pd.ex_multi)\n\t\tp->pd.multi_run = 0;\n", "", ARM,
           "Scripted.ARequestAnsweredByOneClockEndsTheRun",
           "requests answered by one clock or by none did not end the run"),
    Mutant("one-clock-twice-ceases", C, "if (p->pd.ex_multi || !memcmp(src, first, 8))",
           "if (p->pd.ex_multi || (!memcmp(src, first, 8) && 0))", ARM,
           "Scripted.OneClockAnsweringTwiceIsNotAsCapableButDoesNotCease", "one clock answering twice ceased"),
    Mutant("cease-never-ends", C, "if (p->pd.ceased && due(now_ms, p->pd.cease_end_ms))", "if (p->pd.ceased && 0)",
           ARM, "Scripted.TheCeaseEndsAfterFiveMinutes", "Pdelay_Req did not resume after 5 minutes"),
    # the envelope guards against a peer that stamps on a stepped PHC; this port's own peers run the LocalClock
    Mutant("rate-envelope-dropped", C, "if (s4 == 0 || mag > (s4 >> GPTP_NRR_ENVELOPE_SHIFT)) {", "if (s4 == 0) {",
           ARM, "Scripted.AResponderThatStepsItsClockReachesNoRate",
           "a responder's step reached the delay through the rate"),
    Mutant("turnaround-unbounded", C, "\tif (turn > rtt + (rtt >> GPTP_NRR_ENVELOPE_SHIFT))\n\t\treturn;\n", "", ARM,
           "Scripted.ATurnaroundLongerThanTheRoundTripIsNoMeasurement",
           "a turnaround over the round trip reached the delay"),
    Mutant("own-step-keeps-the-exchange", C, "\tp->pd.in_flight = false;\n\tp->rsp.resp_owed = false;",
           "\tp->rsp.resp_owed = false;",
           ARM, "Scripted.AnOwnStepVoidsTheExchangeInFlightAndMovesNoRate",
           "the exchange straddling the step was used"),
    # Pdelay on the PHC itself, steps and all: a step reaches this port's rate window and a peer's turnaround
    Mutant("steps-left-on-the-local-clock", C, "\treturn phc_ns - p->local_off;", "\t(void)p;\n\treturn phc_ns;", ARM,
           "Scripted.AnOwnStepVoidsTheExchangeInFlightAndMovesNoRate",
           "the rate across the step reached the delay",
           also=tuple((ARM, f"Net.{test}", "the grandmaster's port fell from asCapable across the slave's step")
                      for test in ("AForwardStepOf300usKeepsAsCapableAt10msTurnaround",
                                   "AForwardStepOf400usKeepsAsCapableAt10msTurnaround",
                                   "ABackwardStepOf300usKeepsAsCapableAt10msTurnaround",
                                   "ABackwardStepOf400usKeepsAsCapableAt10msTurnaround",
                                   "ABackwardStepOf475usKeepsAsCapableAt5msTurnaround"))),
    # the second response cleared only at the exchange's completion, which a missing Follow_Up never brings
    Mutant("multiple-responses-cleared-at-completion", C,
           "\tp->pd.multi = true;\n\tp->pd.good = 0;\n\tas_capable_set(p, false);\n", "\tp->pd.multi = true;\n",
           ARM,
           "Scripted.MultipleResponsesWithoutFollowUpClearAsCapableAtOnce",
           "multiple responses without Follow_Up kept asCapable",
           also=((ARM, "Scripted.ASecondResponseClearsAsCapableBeforeItsExchangeCompletes",
                  "a second response in flight kept asCapable until a Follow_Up"),
                 (ARM, "Scripted.OneClockAnsweringTwiceClearsAsCapableAtOnceAndDoesNotCease",
                  "one clock answering twice kept asCapable"),
                 (ARM, "Scripted.ALateSecondResponderClearsTheAsCapableOfACompletedExchange",
                  "a second responder after completion kept asCapable"))),
    Mutant("own-step-completes-the-response", C,
           "\tp->rsp.resp_owed = false;\n\tp->rsp.fu_owed = false;\n}\n\nstatic void servo_pair",
           "}\n\nstatic void servo_pair", ARM,
           "Scripted.AnOwnStepCompletesNoResponseOwed", "a Pdelay_Resp_Follow_Up across this port's step was sent"),
    Mutant("null-path-compared", C, "(n == 0 || !memcmp(p->pub.path, path, n * sizeof *path))",
           "!memcmp(p->pub.path, path, n * sizeof *path)", "gptp_ubsan",
           "Scripted.LinkUpSendsOnePdelayReqAtOnce", "undefined behaviour"),
    Mutant("link-loss-keeps-ascap", C, "\tp->pd.as_capable = false;        // a link loss", "\t// a link loss", ARM,
           "Scripted.LinkDownClearsAsCapableAtOnce", "asCapable came back with the link before any exchange"),
)


def planted_tree(base: Path, mutant: Mutant | None) -> Path:
    """A copy of the port's directory under base/ctrl, with the defect planted."""
    src = base / "ctrl"
    shutil.copytree(CTRL / "gptp", src / "gptp")
    if mutant is not None:
        path = src / mutant.path
        text = path.read_text()
        if text.count(mutant.old) != 1:
            raise Refusal(f"{mutant.name}: its text is in {mutant.path} {text.count(mutant.old)} times, not once")
        path.write_text(text.replace(mutant.old, mutant.new))
    return src


def run_one(out: Path, mutant: Mutant | None) -> tuple[str, bool, str]:
    """Its arms under out/<name>: the unplanted port must pass every arm; a planted one must fail each test it
    names with its words. Returns the name, whether it did, and the line that says so."""
    name = mutant.name if mutant else "baseline"
    base = out / name
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    try:
        src = planted_tree(base, mutant)
        tree = Tree(src, base / "build", base / "reuse", fw_gtest.Build(jobs=1))
        outcomes = [ARMS[arm](tree) for arm in (ARMS if mutant is None else {k[0] for k in mutant.kills()})]
    except Refusal as exc:
        return name, False, f"REFUSED {exc}"
    if mutant is None:
        return name, all(o.rc == 0 for o in outcomes), "\n".join(o.log for o in outcomes)
    log = "\n".join(o.log for o in outcomes)
    marks = [ln for ln in log.splitlines() if ln.lstrip().startswith("[FAIL]")]
    missed = [(test, words) for _arm, test, words in mutant.kills()
              if not any(f"[FAIL] {test}:" in ln and words in ln for ln in marks)]
    if all(o.rc == 0 for o in outcomes):
        return name, False, "SURVIVED: the arm passed"
    if missed:
        return name, False, ("MISSED: failed, but not " + "; ".join(f"{t} with {w!r}" for t, w in missed) + ":\n" +
                             "\n".join(marks[:6]))
    hit = next(ln for ln in marks if f"[FAIL] {mutant.test}:" in ln and mutant.needle in ln)
    return name, True, f"KILLED by {mutant.test}: {hit.strip()}"


def main() -> int:
    """The baseline, then every planted defect in parallel; any survivor, miss or refusal fails the campaign."""
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--build-dir", type=Path)
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()
    out = args.build_dir or Path(tempfile.mkdtemp(prefix="gptp-mutants-"))
    name, ok, log = run_one(out, None)
    print(f"baseline: {'PASS' if ok else 'FAIL'}")
    if not ok:
        print(log)
        return 2
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as pool:
        results = list(pool.map(lambda m: run_one(out, m), MUTANTS))
    failed = 0
    for name, ok, log in results:
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: {log.splitlines()[0] if log else ''}")
        if not ok:
            failed += 1
            print("\n".join("      " + ln for ln in log.splitlines()[1:8]))
    print(f"== ctrl gPTP planted defects: checks: {len(MUTANTS)}   failures: {failed} ==")
    print("RESULT: " + ("PASS" if failed == 0 else "FAIL"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

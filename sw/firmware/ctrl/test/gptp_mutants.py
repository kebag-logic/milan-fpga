#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""gptp_mutants.py - planted defects of the firmware gPTP end station port, each caught by its test (#665 F6, #884).

Each defect replaces one exact text of gptp/gptp.c or gptp/gptp.h in a scratch copy of the port, builds the gptp
arm (gptp_arms.arm_gptp) on that copy and requires the named test to fail with the named words on its [FAIL]
line. A defect whose text is not found exactly once, or that builds and passes, or that fails only elsewhere, fails
the campaign. The unplanted copy must pass first, so a broken baseline is never read as a kill.

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

MUTANTS = (
    Mutant("ascap-after-one", H, "#define GPTP_ASCAP_UP 2u", "#define GPTP_ASCAP_UP 1u", ARM,
           "Scripted.AsCapableNeedsTwoGoodInARow", "asCapable after one good exchange with a rate"),
    Mutant("lost-clears-at-fourth", C, "if (p->pd.lost <= GPTP_LOST_ALLOWED)", "if (p->pd.lost < GPTP_LOST_ALLOWED)",
           ARM, "Scripted.FifthLostResponseClearsAsCapable", "asCapable fell at the fourth lost response"),
    Mutant("npd-threshold-exclusive", C, "p->pd.delay_ns > GPTP_NPD_HI_NS", "p->pd.delay_ns >= GPTP_NPD_HI_NS", ARM,
           "Scripted.DelayOverThresholdIsNotAsCapable", "800 ns is at the threshold, inside it"),
    Mutant("late-bound-exclusive", C, "p->pd.t4 - p->pd.t1 > GPTP_PD_LATE_NS", "p->pd.t4 - p->pd.t1 >= GPTP_PD_LATE_NS",
           ARM, "Scripted.LateResponseIsLost", "a response at the bound was refused"),
    Mutant("nrr-inverted", C, "int64_t q = ((d3 - d4) * (int64_t)(1ll << 32)) / d4;",
           "int64_t q = ((d4 - d3) * (int64_t)(1ll << 32)) / d4;", ARM,
           "Scripted.RateRatioAndDelayWithAFastNeighbor", "neighborRateRatio"),
    Mutant("delay-without-nrr", C, "d = (int64_t)rtt + (((int64_t)rtt * p->pd.nrr_q32) >> 32) - (int64_t)turn;",
           "d = (int64_t)rtt - (int64_t)turn;", ARM,
           "Scripted.RateRatioAndDelayWithAFastNeighbor", "the delay ignores the neighbor's rate"),
    Mutant("cease-one-late", C, "if (++p->pd.multi_run >= GPTP_CEASE_N) {\n\t\t\tp->pd.ceased = true;\n\t\t\tp->pd.cease_end_ms = p->now_ms + GPTP_CEASE_MS;\n\t\t}\n\t\treturn;",
           "if (++p->pd.multi_run > GPTP_CEASE_N) {\n\t\t\tp->pd.ceased = true;\n\t\t\tp->pd.cease_end_ms = p->now_ms + GPTP_CEASE_MS;\n\t\t}\n\t\treturn;",
           ARM, "Scripted.MultipleRespondersCeaseAndALinkToggleResumes", "Pdelay_Req still sent during the cease"),
    Mutant("cease-survives-link-toggle", C, "\tp->pd.ceased = false;     // each link edge", "\t// each link edge", ARM,
           "Scripted.MultipleRespondersCeaseAndALinkToggleResumes", "the link toggle did not end the cease"),
    Mutant("bmca-inverted", C, "if (p->ann.valid && vector_cmp(&p->ann.v, &own) < 0) {",
           "if (p->ann.valid && vector_cmp(&p->ann.v, &own) > 0) {", ARM,
           "Scripted.BetterAnnounceMakesASlave", "10.3.5: priority1 100 is better than 248"),
    Mutant("path-loop-kept", C, "if (id == p->cfg.clock_id) {", "if (0) {", ARM,
           "Scripted.LoopedPathAndStepsRemoved255AreDiscarded", "a path holding thisClock was used"),
    Mutant("sync-timeout-500", H, "#define GPTP_SYNC_RTO_MS 375u", "#define GPTP_SYNC_RTO_MS 500u", ARM,
           "Scripted.SyncReceiptTimeoutAgesTheGrandmaster", "no Sync for 375 ms did not age the grandmaster"),
    Mutant("sync-any-source", C, "if (p->role != GPTP_ROLE_SLAVE || memcmp(f + F_SRC, p->ann.v.src, 10))\n\t\treturn;   // Sync only",
           "if (p->role != GPTP_ROLE_SLAVE)\n\t\treturn;   // Sync only", ARM,
           "Scripted.SyncFromAnotherPortIsIgnored", "another port's Sync displaced the master's pending Sync"),
    Mutant("linkup-threshold-lost", C, "p->srv.linkup ? GPTP_STEP_LINKUP_NS : GPTP_STEP_LOCKED_NS",
           "GPTP_STEP_LOCKED_NS", ARM,
           "Scripted.FirstPairStepsAtTheLinkUpThreshold", "an offset over 20 us at link-up did not step"),
    Mutant("step-sign", C, "p->hal.phc_step(p->hal.ctx, p->index, -offset);",
           "p->hal.phc_step(p->hal.ctx, p->index, offset);", ARM,
           "Scripted.FirstPairStepsAtTheLinkUpThreshold", "the step is not the offset, negated"),
    Mutant("p-term-sign", C, "clamp64((p->srv.integ - kp * offset) / 65536, lim)",
           "clamp64((p->srv.integ + kp * offset) / 65536, lim)", ARM,
           "Scripted.LockedThresholdSlewsUnder100us", "local ahead: the trim must slow it"),
    Mutant("trim-unclamped", C, "clamp64((p->srv.integ - kp * offset) / 65536, lim)",
           "clamp64((p->srv.integ - kp * offset) / 65536, 4 * lim)", ARM,
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
    Mutant("slave-timer-stale", C, "\t\tp->slv.last_ms = p->now_ms;   // the sync receipt timer starts", "\t\tp->slv.last_ms = p->slv.last_ms;   // the sync receipt timer starts",
           ARM, "Net.SlaveLocksToTheGrandmaster", "not inside 100 ns of the grandmaster by 15 s"),
    Mutant("own-frames-used", C, "if (from_self(p, frame))\n\t\treturn;", "if (from_self(p, frame) && 0)\n\t\treturn;", ARM,
           "Scripted.OwnResponseIsIgnored", "asCapable from its own responses"),
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
    name = mutant.name if mutant else "baseline"
    base = out / name
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True)
    try:
        src = planted_tree(base, mutant)
        tree = Tree(src, base / "build", base / "reuse", fw_gtest.Build(jobs=1))
        outcome = gptp_arms.arm_gptp(tree)
    except Refusal as exc:
        return name, False, f"REFUSED {exc}"
    if mutant is None:
        return name, outcome.rc == 0, outcome.log
    marks = [ln for ln in outcome.log.splitlines() if ln.lstrip().startswith("[FAIL]")]
    hit = [ln for ln in marks if f"[FAIL] {mutant.test}:" in ln and mutant.needle in ln]
    if outcome.rc == 0:
        return name, False, "SURVIVED: the arm passed"
    if not hit:
        return name, False, "MISSED: failed, but not " + mutant.test + " with its words:\n" + "\n".join(marks[:6])
    return name, True, f"KILLED by {mutant.test}: {hit[0].strip()}"


def main() -> int:
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

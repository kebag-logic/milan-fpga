#!/usr/bin/env python3
"""Reviewer plants for #925 round 3 at the exact head, run from the clone's own harness modules.

plants.py ROOT OUT IFS JOBS SET
  SET reviewer: the prior internal round's five plants through srp_mutants.campaign, its
      r849-unknown-withdraws re-selected against the test that replaced the removed one.
  SET author:   a spot-check subset of srp_kind_mutants.py's table through srp_mutants.campaign.
  SET explore:  this round's own plants; each is planted in a copy and the SrpTalkerKinds and
      Srp.HeldRegistrations tests of srp_mbx.cpp and SrpFeedback of test_acmp_mbx.cpp are run whole,
      reporting every failing test (a control run with no plant comes first).
  SET whole:NAME: the control and the explore plant NAME, with srp_mbx.cpp and test_acmp_mbx.cpp run whole.
Nothing in ROOT is written: every edit happens in a copy under OUT.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

mode_root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(mode_root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(mode_root / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
import srp_mutants  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from srp_arms import arm_srp  # noqa: E402

D = srp_mutants.Defect
KINDS = "SrpTalkerKinds."
PRIOR = (
    D("r849-bind-copy-same-destination", KINDS + "ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream",
      "                replacement.latest_kind = r->latest_kind;\n",
      "                if (memcmp(r->dest_mac,dest_mac,6) == 0) { replacement.latest_kind = r->latest_kind; }\n",
      "a later binding takes the latest registration"),
    D("r849-walk-kinds-swapped", KINDS + "AnAdvertiseNewReplacesARegisteredFailedWithinAJoinTime",
      "sink->registered_kinds |= status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u;",
      "sink->registered_kinds |= status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED ? 2u : 1u;",
      "a first registration declares within a JoinTime"),
    # re-selected: the removed ABindingThatSawNeitherRegistrationTakesFailedFirst became AFullHeldTableHoldsNothingMore
    D("r849-unknown-withdraws", KINDS + "AFullHeldTableHoldsNothingMore",
      "return (kinds & 1u) != 0u ? 1u : kinds;", "return kinds == 3u ? 0u : kinds;",
      "no latest known: Failed"),
    D("r849-renew-not-recorded", KINDS + "AFailedNewReplacesARegisteredAdvertiseWithinAJoinTime",
      "s->latest_kind = registered ? kind : s->latest_kind;",
      "s->latest_kind = registered && (held & kind) == 0u ? kind : s->latest_kind;",
      "a Failed New replaces the registered Advertise",
      also=(("s->registered_kinds &= (uint8_t)~kind;",
             "const uint8_t held = s->registered_kinds; s->registered_kinds &= (uint8_t)~kind;"),)),
    D("r849-bind-copy-skipped-for-self", KINDS + "ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream",
      "                replacement.latest_kind = r->latest_kind;\n",
      "                replacement.latest_kind = k == sink ? replacement.latest_kind : r->latest_kind;\n",
      "a later binding takes the latest registration"),
)
AUTHOR = ("feedback-latest-filter-holds-nothing", "feedback-latest-filter-holds-nothing-acmp",
          "feedback-latest-not-held", "feedback-latest-held-past-a-leave", "feedback-latest-held-past-a-reset",
          "feedback-latest-renew-not-recorded", "feedback-latest-unknown-withdraws", "held-latest-any-interface",
          "held-latest-reset-any-interface", "feedback-latest-not-carried-in-place")

# (name, path, old, new): this round's exploratory plants
EXPLORE = (
    ("control-no-plant", None, None, None),
    # the filter owes only a declaration that becomes non-zero: a withdrawal its copy makes waits
    ("r849-2-filter-holds-no-withdrawal", "srp/srp_mbx.c",
     "        if (s->desired != previous) {\n            hold(i);\n",
     "        if (s->desired != previous && s->desired != 0u) {\n            hold(i);\n"),
    # the StreamID's kinds counted only for the binding's own destination and VID
    ("r849-2-stream-kinds-own-destination", "srp/srp_mbx.c",
     "                sink->stream_kinds |= status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u;\n"
     "                if (same(sink->dest_mac,v->dest_mac,6) && sink->vid == v->vlan_id) {\n",
     "                if (same(sink->dest_mac,v->dest_mac,6) && sink->vid == v->vlan_id) {\n"
     "                sink->stream_kinds |= status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u;\n"),
    # a reset releases its interface's entries walking forward, skipping the entry moved into a released place
    ("r849-2-reset-walks-forward", "srp/srp_mbx.c",
     "    for (unsigned n = m->held_count; n-- != 0u;) {\n",
     "    for (unsigned n = 0; n < m->held_count; ++n) {\n"),
    # a binding that takes a held entry does not claim both kinds until the next walk
    ("r849-2-take-without-kinds", "srp/srp_mbx.c",
     "            replacement.stream_kinds = 3u;\n", ""),
    # a final unbinding holds the StreamID whatever its latest, also with none known
    ("r849-2-held-latest-dropped", "srp/srp_mbx.c",
     "(struct srp_held){old.stream_id,(uint8_t)interface,old.latest_kind}",
     "(struct srp_held){old.stream_id,(uint8_t)interface,0u}"),
)


def campaign(out: Path, interfaces: int, jobs: int, defects) -> int:
    srp_mutants.DEFECTS = tuple(defects)
    failed = srp_mutants.campaign(out, mode_root / "third_party/lwSRP", jobs, interfaces)
    print(f"campaign interfaces={interfaces}: {'ESCAPED' if failed else 'all caught'}", flush=True)
    return 1 if failed else 0


def explore(out: Path, interfaces: int, jobs: int, only: str | None = None, whole: bool = False) -> int:
    bad = 0
    for name, path, old, new in EXPLORE:
        if only and name not in ("control-no-plant", only):
            continue
        work = out / name
        if work.exists():
            shutil.rmtree(work)
        src = work / "ctrl"
        shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        if path:
            target = src / path
            text = target.read_text()
            assert text.count(old) == 1, name
            target.write_text(text.replace(old, new))
        for suite, selected in ((("srp_mbx.cpp", "*"), ("test_acmp_mbx.cpp", "*")) if whole else
                                (("srp_mbx.cpp", "SrpTalkerKinds.*:Srp.HeldRegistrations*"),
                                 ("test_acmp_mbx.cpp", "SrpFeedback.*"))):
            r = arm_srp(Tree(src, work / "build", work / "reuse", fw_gtest.Build(jobs=jobs)),
                        mode_root / "third_party/lwSRP", interfaces, test=(suite, selected))
            (out / f"{name}-{suite}.log").write_text(r.log)
            fails = sorted({ln.split("]", 1)[1].strip().split(" ")[0] for ln in r.log.splitlines()
                            if ln.startswith("[  FAILED  ]") and "," not in ln.split("]", 1)[1][:2]})
            passed = [ln for ln in r.log.splitlines() if ln.startswith("[  PASSED  ]")]
            print(f"{name} if{interfaces} {suite}: rc={r.rc} {passed[-1] if passed else ''} "
                  f"failed={fails}", flush=True)
            if name == "control-no-plant" and r.rc:
                bad = 1
        shutil.rmtree(work / "build", ignore_errors=True)
    return bad


if __name__ == "__main__":
    out, ifs, jobs, what = Path(sys.argv[2]).resolve(), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    out.mkdir(parents=True, exist_ok=True)
    if what == "reviewer":
        sys.exit(campaign(out, ifs, jobs, PRIOR))
    if what == "author":
        chosen = [d for d in srp_mutants.DEFECTS if d.name in AUTHOR and (ifs == 2 or d.name.startswith("feedback-"))]
        print(f"author plants selected: {[d.name for d in chosen]}", flush=True)
        sys.exit(campaign(out, ifs, jobs, chosen))
    if what.startswith("whole:"):
        # SET whole:<plant>: the control and that one plant, with srp_mbx.cpp and test_acmp_mbx.cpp run whole
        sys.exit(explore(out, ifs, jobs, only=what.split(":", 1)[1], whole=True))
    sys.exit(explore(out, ifs, jobs))

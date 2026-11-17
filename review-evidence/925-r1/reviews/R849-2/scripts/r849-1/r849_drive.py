"""Reviewer drivers for #925 at the exact head, run from the clone's own harness modules.

probes ROOT OUT IFS [PLANT]: copy sw/firmware/ctrl to OUT/ctrl, append scripts/r849_probe_tests.cpp to its
  srp_mbx.cpp, optionally apply the named planted defect, and run R849Probe.* and SrpTalkerKinds.* at IFS.
mutants ROOT OUT IFS JOBS: run the SRP defects of this change (the feedback-latest- table and failed-listener-ready)
  plus the reviewer's own plants through srp_mutants.campaign at IFS interfaces.
Nothing in ROOT is written: every edit happens in a copy under OUT.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

root = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
import srp_mutants  # noqa: E402
from ctrl_build import CTRL, Tree  # noqa: E402
from srp_arms import arm_srp  # noqa: E402

HERE = Path(__file__).resolve().parent
D = srp_mutants.Defect
KINDS = "SrpTalkerKinds."
REVIEWER = (
    # a later binding copies the latest only from a binding of its own destination
    D("r849-bind-copy-same-destination", KINDS + "ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream",
      "                replacement.latest_kind = r->latest_kind;\n",
      "                if (memcmp(r->dest_mac,dest_mac,6) == 0) { replacement.latest_kind = r->latest_kind; }\n",
      "a later binding takes the latest registration"),
    # the walk's kinds swapped: a registered Advertise copied as Failed and the reverse
    D("r849-walk-kinds-swapped", KINDS + "AnAdvertiseNewReplacesARegisteredFailedWithinAJoinTime",
      "sink->registered_kinds |= status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED ? 1u : 2u;",
      "sink->registered_kinds |= status->attr_type == MSRP_ATTR_TYPE_TALKER_FAILED ? 2u : 1u;",
      "a first registration declares within a JoinTime"),
    # both registered and no latest known: nothing declared instead of Failed
    D("r849-unknown-withdraws", KINDS + "ABindingThatSawNeitherRegistrationTakesFailedFirst",
      "return (kinds & 1u) != 0u ? 1u : kinds;", "return kinds == 3u ? 0u : kinds;",
      "neither registration seen: Failed first"),
    # a New of a kind this binding already holds (a talker flapping back) is not recorded as the latest
    D("r849-renew-not-recorded", KINDS + "AFailedNewReplacesARegisteredAdvertiseWithinAJoinTime",
      "s->latest_kind = registered ? kind : s->latest_kind;",
      "s->latest_kind = registered && (held & kind) == 0u ? kind : s->latest_kind;",
      "a Failed New replaces the registered Advertise",
      also=(("s->registered_kinds &= (uint8_t)~kind;",
             "const uint8_t held = s->registered_kinds; s->registered_kinds &= (uint8_t)~kind;"),)),
    # the bind copies the latest of the binding being replaced only when it is unbound (never)
    D("r849-bind-copy-skipped-for-self", KINDS + "ABindingMadeLaterTakesTheLatestFromAnyBindingOfTheStream",
      "                replacement.latest_kind = r->latest_kind;\n",
      "                replacement.latest_kind = k == sink ? replacement.latest_kind : r->latest_kind;\n",
      "a later binding takes the latest registration"),
)


def probes(out: Path, interfaces: int, plant: str | None) -> int:
    src = out / "ctrl"
    if src.exists():
        shutil.rmtree(src)
    shutil.copytree(CTRL, src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    test = src / "test/srp_mbx.cpp"
    test.write_text(test.read_text() + "\n" + (HERE / "r849_probe_tests.cpp").read_text())
    if plant:
        d = next(d for d in srp_mutants.DEFECTS + REVIEWER if d.name == plant)
        target = src / d.path
        text = target.read_text()
        for old, new in ((d.old, d.new), *d.also):
            assert text.count(old) == 1, plant
            text = text.replace(old, new)
        target.write_text(text)
    lwsrp = root / "third_party/lwSRP"
    import srp_arms
    srp_arms.HERE = src / "test"   # arm_srp compiles its test file from HERE: point it at the probe copy
    result = arm_srp(Tree(src, out / "build", out / "reuse", fw_gtest.Build(jobs=4)), lwsrp, interfaces,
                     test=("srp_mbx.cpp", "R849Probe.*:SrpTalkerKinds.*"))
    print(result.log)
    print(f"probe rc={result.rc} interfaces={interfaces} plant={plant}")
    return result.rc


def mutants(out: Path, interfaces: int, jobs: int) -> int:
    mine = tuple(d for d in srp_mutants.DEFECTS
                 if d.name.startswith("feedback-latest-") or d.name == "failed-listener-ready")
    print(f"author plants selected: {len(mine)}; reviewer plants: {len(REVIEWER)}")
    srp_mutants.DEFECTS = mine + REVIEWER
    failed = srp_mutants.campaign(out, root / "third_party/lwSRP", jobs, interfaces)
    print(f"campaign interfaces={interfaces}: {'ESCAPED' if failed else 'all caught'}")
    return 1 if failed else 0


if __name__ == "__main__":
    mode, out, ifs = sys.argv[1], Path(sys.argv[3]).resolve(), int(sys.argv[4])
    if mode == "probes":
        sys.exit(probes(out, ifs, sys.argv[5] if len(sys.argv) > 5 else None))
    sys.exit(mutants(out, ifs, int(sys.argv[5])))

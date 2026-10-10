#!/usr/bin/env python3
"""Reviewer probes of the SRP cancelled-LINK test and its event-poster hold (PR #704, head 25bbe4d9).

Usage: probe_link_hold.py <source-tree> <lwsrp-checkout> <work-dir> [interfaces] [head|parent|nohold|make-nohold]

make-nohold edits <source-tree> IN PLACE (use a disposable export of the head):
it removes the hold and its assertion from the test, giving the tree the
"nohold" mode expects. The SRP arm compiles the test from <source-tree> and only
the firmware and the model from each probe's copy, so test edits cannot be
per-probe edits.

Each probe copies <source-tree>/sw/firmware/ctrl, applies its edits (each old
string must occur exactly once), builds the SRP arm with only
Srp.CancelledLinkRecordRecoversFromLevelAndFencesOldReceive selected, and
compares the outcome with the expectation: "pass" (rc 0) or a needle that must
appear in that test's failure block. Prints one verdict line per probe; exits 1
when any probe misses its expectation.
"""
import shutil
import sys
from pathlib import Path

TREE, LWSRP, WORK = (Path(a).resolve() for a in sys.argv[1:4])
IFS = int(sys.argv[4]) if len(sys.argv) > 4 else 2
MODE = sys.argv[5] if len(sys.argv) > 5 else "head"
sys.path[:0] = [str(TREE / "sw/firmware/ctrl/test"), str(TREE / "sw/firmware/gtest")]
import fw_gtest  # noqa: E402
from ctrl_build import Tree  # noqa: E402
from srp_arms import arm_srp  # noqa: E402
from srp_mutants import caught  # noqa: E402

TEST = "Srp.CancelledLinkRecordRecoversFromLevelAndFencesOldReceive"
PAUSE_ON = "        mbx_model_evt_pause(&model,true);\n"
PAUSE_CHECK = ('        ASSERT_TRUE(model.posted_up[i])<<"the DOWN record stayed held";\n'
               "        mbx_model_evt_pause(&model,false);\n")
# the hold and its assertion removed from the test (make-nohold)
NO_PAUSE = [("test/srp_mbx.cpp", PAUSE_ON, ""), ("test/srp_mbx.cpp", PAUSE_CHECK, "")]
PLANT = [("srp/srp_mbx.c", "if (i->link != link)", "if (i->link && !link)")]
HOLD_IGNORED = [("host/mbx_model.c", "if (m->evt_paused || free_words < MBX_EV_WORDS",
                 "if (free_words < MBX_EV_WORDS")]
# every publication write made a no-op in the driver: the firmware's mailbox
# traffic in the reset window is then what it was on the base
NO_PUB = [("mbx/mbx.c", "// Register `reg` of interface i's publication block, and of its sink k.\n",
           "#define mbx_hal_write32(a, v) ((void)(a), (void)(v))\n"
           "// Register `reg` of interface i's publication block, and of its sink k.\n"),
          ("mbx/mbx.c", "uint16_t mbx_filter_mismatch(void)\n", "#undef mbx_hal_write32\nuint16_t mbx_filter_mismatch(void)\n")]

PROBES = [
    ("control-head", [], "pass"),
    ("hold-with-plant", PLANT, "adapter.ifs[i].link"),
    ("hold-ignored", HOLD_IGNORED, "the DOWN record stayed held"),
]

# Run on a head export whose test already lacks the hold (the arm compiles the
# test from <source-tree>, firmware and model from the probe's copy).
PROBES_NOHOLD = [
    ("nohold-control", [], "pass"),
    ("nohold-plant", PLANT, "pass"),
    ("nohold-plant-no-publication", PLANT + NO_PUB, "adapter.ifs[i].link"),
]

# At the parent 9b73a8c6 (no hold in the model or the test): the author reports
# the plant escaping there; "pass" records an escape.
PROBES_PARENT = [
    ("parent-control", [], "pass"),
    ("parent-plant", PLANT, "pass"),
]


def main() -> int:
    if MODE == "make-nohold":
        for rel, old, new in NO_PAUSE:
            path = TREE / "sw/firmware/ctrl" / rel
            text = path.read_text()
            if text.count(old) != 1:
                print(f"[REFUSED] make-nohold: {rel} has {text.count(old)} sites")
                return 1
            path.write_text(text.replace(old, new))
        print("make-nohold: the test's hold and its assertion removed")
        return 0
    build = fw_gtest.Build(jobs=2)
    bad = 0
    for name, edits, expect in (PROBES_PARENT if MODE == "parent" else PROBES_NOHOLD if MODE == "nohold" else PROBES):
        out = WORK / name
        shutil.rmtree(out, ignore_errors=True)
        src = out / "ctrl"
        shutil.copytree(TREE / "sw/firmware/ctrl", src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        for rel, old, new in edits:
            path = src / rel
            text = path.read_text()
            if text.count(old) != 1:
                print(f"[REFUSED] {name}: {rel} has {text.count(old)} sites for {old[:50]!r}")
                bad += 1
                break
            path.write_text(text.replace(old, new))
        else:
            result = arm_srp(Tree(src, out / "build", out / "reuse", build), LWSRP, IFS, test=("srp_mbx.cpp", TEST))
            (WORK / f"{name}.log").write_text(result.log)
            ok = result.rc == 0 if expect == "pass" else caught(TEST, expect, result)
            got = "pass" if result.rc == 0 else f"rc {result.rc}"
            print(f"[{'as expected' if ok else 'UNEXPECTED'}] {name}: expected {expect!r}, got {got}", flush=True)
            bad += not ok
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

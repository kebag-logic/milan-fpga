#!/usr/bin/env python3
"""Reviewer probe: plant the delta's four declared defects plus reviewer-chosen
extra defects into disposable copies of the firmware tree, using the
repository's own planting and grading functions, and report caught/escaped.

usage: probe_mutants.py <checkout> <work-dir> <control|aecp|baseline>
The checkout is never written: each campaign copies the firmware tree into
<work-dir> first.
"""
from __future__ import annotations

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
work = Path(sys.argv[2]).resolve()
which = sys.argv[3]
sys.path[:0] = [str(repo / "sw/firmware/ctrl/test"), str(repo / "sw/firmware/gtest")]

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import Outcome, Refusal, Tree, stack_pin, STACK  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from gptp_driver_mutants import MUTANTS as DECLARED_DRIVER  # noqa: E402

TS = "DriverUnit.TimestampEventDecodesFlagsAndBothTimeWordsAcrossWrap"
PUB = "DriverUnit.GptpPublicationCommitsAfterItsIdentityWords"
EXTRA_DRIVER = (
    Mutant("x-ts-egress-read-from-ok-bit", "mbx/mbx.c",
           "ev->ts_egress = mbx_field(w1, MBX_EV_TIMESTAMP_W1_EGRESS_LSB,",
           "ev->ts_egress = mbx_field(w1, MBX_EV_TIMESTAMP_W1_OK_LSB,", "unit", TS, ""),
    Mutant("x-ts-low-word-dropped", "mbx/mbx.c", "MBX_EV_TIMESTAMP_W3_NS_HI_WIDTH) << 32) |",
           "MBX_EV_TIMESTAMP_W3_NS_HI_WIDTH) << 32) &", "unit", TS, ""),
    Mutant("x-ts-msg-type-narrowed", "mbx/mbx.c",
           "MBX_EV_TIMESTAMP_W1_MSG_TYPE_LSB, MBX_EV_TIMESTAMP_W1_MSG_TYPE_WIDTH)",
           "MBX_EV_TIMESTAMP_W1_MSG_TYPE_LSB, 2u)", "unit", TS, ""),
    Mutant("x-pub-gptp-accepts-one-past", "mbx/mbx.c",
           "/ 4u;\n\tunsigned k;\n\tif (interface >= MBX_N_IF) {",
           "/ 4u;\n\tunsigned k;\n\tif (interface > MBX_N_IF) {", "unit", PUB, ""),
    Mutant("x-pub-gptp-every-interface-block-0", "mbx/mbx.c",
           "mbx_bus_write32(pub_reg(interface, MBX_PUB_REG_GPTP_STATE), words[state]);",
           "mbx_bus_write32(pub_reg(0u, MBX_PUB_REG_GPTP_STATE), words[state]);", "unit", PUB, ""),
)


def control() -> int:
    arms = {"unit": ctrl_arms.arm_unit}
    build = fw_gtest.Build(jobs=4)
    reuse = work / "reuse"
    escaped = 0
    for m in DECLARED_DRIVER + EXTRA_DRIVER:
        root = work / m.name
        copy, stack = ctrl_mutants.plant(m, root)
        tree = Tree(copy, root / "work" / "build", reuse, build, stack)
        for arm, test, needle in m.kills():
            try:
                outcome = arms[arm](tree)
            except Refusal as exc:
                outcome = Outcome(arm, 2, f"refused: {exc}")
            ok = ctrl_mutants.caught(test, needle, outcome)
            (work / f"{m.name}.log").write_text(outcome.log)
            fails = [ln.strip() for ln in outcome.log.splitlines() if "[FAIL]" in ln]
            print(f"[{'caught' if ok else 'ESCAPED'}] {m.name}: {test} needle={needle!r} rc={outcome.rc} "
                  f"fails={len(fails)} first={fails[0] if fails else '-'}", flush=True)
            escaped += 0 if ok else 1
    return escaped


AVB = "Face.SoftwareGptpAvbKeepsTheDatapathsLinkAndClass"
PATH = "Face.SoftwareGptpPathForwardsCapacityAndRefusalWithoutAWindowRead"


def aecp() -> int:
    import aecp_face_mutants
    import aecp_mutants
    declared = tuple(aecp_mutants.defect(*row) for row in aecp_face_mutants.ROWS[:2])
    extra = (
        aecp_mutants.defect("x-face-datapath-capable-bit-kept", "aecp_face.c",
                            "(uint8_t)((out->flags & ~1u) | (as_capable ? 1u : 0u));",
                            "(uint8_t)(out->flags | (as_capable ? 1u : 0u));", (AVB, "")),
        aecp_mutants.defect("x-face-avb-asks-interface-0", "aecp_face.c",
                            "f->gptp.avb(f->gptp.ctx, interface,", "f->gptp.avb(f->gptp.ctx, 0u,", (AVB, "")),
        aecp_mutants.defect("x-face-path-asks-interface-0", "aecp_face.c",
                            "return f->gptp.path(f->gptp.ctx, interface,", "return f->gptp.path(f->gptp.ctx, 0u,",
                            (PATH, "")),
        aecp_mutants.defect("x-face-path-not-forwarded", "aecp_face.c",
                            "if (f->gptp.path != NULL) {", "if (false) {", (PATH, "")),
        aecp_mutants.defect("x-face-avb-delay-not-taken", "aecp_face.c",
                            "&out->gm_id, &out->propagation_delay,", "&out->gm_id, &(uint32_t){0},", (AVB, "")),
    )
    aecp_mutants.DEFECTS = declared + extra
    aecp_mutants.controls = lambda: None   # the full-table drift control does not apply to a sub-table
    print(f"tsn-c-stack at {stack_pin(STACK.resolve())}", flush=True)
    return int(aecp_mutants.campaign(work, stack=STACK.resolve()))


def baseline() -> int:
    """The unplanted arms: the new tests run and pass at the head."""
    import aecp_arms
    from ctrl_build import CTRL, ROOT
    import shutil
    build = fw_gtest.Build(jobs=4)
    copy = work / "ctrl"
    shutil.copytree(CTRL, copy, ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(CTRL.parent / "ctrl_nvm", work / "ctrl_nvm", ignore=shutil.ignore_patterns("test", "__pycache__"))
    tree = Tree(copy, work / "build", work / "reuse", build, STACK.resolve())
    u = ctrl_arms.arm_unit(tree)
    (work / "unit.log").write_text(u.log)
    a = aecp_arms.core_arm(tree, ROOT / "configs/endstation_ax7101_1x1_tdm8.yaml", 2, "app", AVB + ":" + PATH)
    (work / "app.log").write_text(a.log)
    bad = 0
    for name, out, tests in (("unit", u, (TS, PUB)), ("app", a, (AVB, PATH))):
        for t in tests:
            ran = f"[ RUN      ] {t}" in out.log or t in out.log
            failed = f"[FAIL] {t}" in out.log or f"[  FAILED  ] {t}" in out.log
            print(f"baseline {name}: rc={out.rc} {t}: named={ran} failed={failed}", flush=True)
            bad += int(not ran or failed or out.rc != 0)
    return bad


if __name__ == "__main__":
    work.mkdir(parents=True, exist_ok=True)
    raise SystemExit({"control": control, "aecp": aecp, "baseline": baseline}[which]())

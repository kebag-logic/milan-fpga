#!/usr/bin/env python3
"""Reviewer probe: plant the round-2 host-model twins of ctrl_mutants.py (and
reviewer-added model arms) into scratch copies of sw/firmware/ctrl and run the
`model` arm (the mbx suite on the host model) on each; record every [FAIL].

usage: model_arms.py <exported-tree-root> <work-dir>
"""
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

tree_root = Path(sys.argv[1]).resolve(); work = Path(sys.argv[2]).resolve(); work.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(tree_root / "sw/firmware/ctrl/test"))
import ctrl_arms, ctrl_mutants as cm
from ctrl_build import CTRL, Tree

ROUND2 = ("model-msg-type-off-by-one", "model-tuple-msg-type-ignored", "model-msg-type-refusal-uncounted",
          "model-defend-any-unicast")
arms = [m for m in cm.MUTANTS if m.name in ROUND2]
assert len(arms) == 4, [m.name for m in arms]
G = cm.MODEL_GROUP + "MaapDefendToOwnUnicast"
arms += [
    # the model's frame ending at byte 14 read past its end for the message type (reads byte 15 regardless)
    cm.Mutant("rev-model-msg-past-end", "host/mbx_model.c",
              "return len > MBX_MSG_TYPE_BYTE ? frame[MBX_MSG_TYPE_BYTE] & 0x0Fu : 0u;",
              "return len > MBX_MSG_TYPE_BYTE ? frame[MBX_MSG_TYPE_BYTE] & 0x0Fu : (len == MBX_MSG_TYPE_BYTE ? 2u : 0u);", "model", G, "Q11"),
    # the DEFEND tuple's own-MAC compare dropped on the model (any destination)
    cm.Mutant("rev-model-own-any-dst", "host/mbx_model.c", "&& dst == mac &&",
              "&& (dst == mac || tuple_msg_mask[j] != 0xFFFFu) &&", "model", G, "Q11"),
]

def one(m):
    copy = cm.plant(m, work)
    tree = Tree(copy, work / m.name / "build", work / m.name / "reuse")
    try:
        out = ctrl_arms.arm_model(tree)
    except Exception as exc:  # a build refusal is an escape, never a catch
        return m, 2, False, [], f"REFUSED: {exc}"
    fails = [ln for ln in out.log.splitlines() if "[FAIL]" in ln]
    return m, out.rc, cm.caught(m.test, m.needle, out), fails, out.log

ctl = ctrl_arms.arm_model(Tree(CTRL, work / "control" / "build", work / "control" / "reuse"))
print(f"control (model arm, unplanted): rc={ctl.rc}; tail: {ctl.log.strip().splitlines()[-1:]}")
with ThreadPoolExecutor(max_workers=6) as pool:
    res = list(pool.map(one, arms))
for m, rc, ok, fails, log in res:
    print(f"[{'caught' if ok else 'ESCAPED'}] {m.name}: rc={rc}, {len(fails)} [FAIL] line(s); needle '{m.needle}'")
    if rc not in (0, 1):
        print("   ", log.strip().splitlines()[-5:])
    for f in fails[:8]: print("     ", f.strip())

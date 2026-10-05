#!/usr/bin/env python3
"""Reviewer-owned firmware defect probes for the control-plane firmware (R496-2).

Usage: reviewer_fw_probes.py TREE SCRATCH

Plants defects NOT in the lane's ctrl_mutants.py table into a copy of
TREE/sw/firmware/ctrl with the lane's own plant helper, runs the named arm,
and reports which checks fail (any [FAIL] with exit 1 counts as caught).
"""
import sys
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
root = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(tree / "sw/firmware/ctrl/test"))
import ctrl_arms  # noqa: E402
import ctrl_mutants as cm  # noqa: E402
from ctrl_build import Outcome, Refusal, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

M = cm.Mutant
PROBES = (
    M("p-step-sleeps-when-only-owed", "loop/ctrl_loop.c", "\tif (ctrl_loop_service(l) == 0u) {",
      "\tif (ctrl_loop_service(l) <= 1u) {", "adp", ""),
    M("p-poll-owes-departing-only", "adp/adp.c", "\treturn a->pending != ADP_PENDING_NONE;",
      "\treturn a->pending == ADP_PENDING_DEPARTING;", "adp", ""),
    M("p-seq-stamped-zero", "mbx/mbx.c",
      "mbx_place(tx_seq, MBX_TXREC_W1_SEQ_LSB, MBX_TXREC_W1_SEQ_WIDTH)",
      "mbx_place(0u, MBX_TXREC_W1_SEQ_LSB, MBX_TXREC_W1_SEQ_WIDTH)", "port", ""),
    M("p-carried-ticks-overwritten", "loop/ctrl_loop.c", "\t\t\tl->ticks_owed += ev.tick_count;",
      "\t\t\tl->ticks_owed = ev.tick_count;", "port", ""),
    M("p-carried-ticks-overwritten-adp", "loop/ctrl_loop.c", "\t\t\tl->ticks_owed += ev.tick_count;",
      "\t\t\tl->ticks_owed = ev.tick_count;", "adp", ""),
    M("p-carry-not-dispatched-first", "loop/ctrl_loop.c",
      "\tuint32_t ticked = dispatch_ticks(l, CTRL_LOOP_TICKS_PER_PASS);",
      "\tuint32_t ticked = 0;", "port", ""),
    M("p-carry-not-dispatched-first-adp", "loop/ctrl_loop.c",
      "\tuint32_t ticked = dispatch_ticks(l, CTRL_LOOP_TICKS_PER_PASS);",
      "\tuint32_t ticked = 0;", "adp", ""),
    M("p-bad-record-ends-rx-stage", "loop/ctrl_loop.c", "\t\t\tl->stats.rx_bad++;\n\t\t\tcontinue;",
      "\t\t\tl->stats.rx_bad++;\n\t\t\tbreak;", "port", ""),
    M("p-departing-index-plus-one", "adp/adp.c", "(void)send(a, ADP_MSG_ENTITY_DEPARTING, index);",
      "(void)send(a, ADP_MSG_ENTITY_DEPARTING, index + 1u);", "adp", ""),
)


def main() -> int:
    root.mkdir(parents=True, exist_ok=True)
    reuse = root / "reuse"
    cut_reuse(reuse)
    arms = {"port": ctrl_arms.arm_port, "adp": ctrl_arms.arm_adp, "walk": ctrl_arms.arm_walk,
            "model": ctrl_arms.arm_model}
    caught_n = 0
    for m in PROBES:
        t = Tree(cm.plant(m, root), root / m.name / "build", reuse)
        try:
            out = arms[m.arm](t)
        except Refusal as exc:
            out = Outcome(m.arm, 2, f"refused: {exc}")
        fails = [ln.strip() for ln in out.log.splitlines() if "[FAIL]" in ln]
        caught = out.rc == 1 and bool(fails)
        caught_n += caught
        first = fails[0] if fails else (out.log.strip().splitlines() or ["no output"])[-1]
        print(f"[{'caught' if caught else 'ESCAPED'}] {m.name} ({m.arm}, rc {out.rc}): {len(fails)} [FAIL]; first: {first}")
    print(f"reviewer firmware probes: {caught_n} of {len(PROBES)} caught")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""R530-2 reviewer-planted firmware defects for lane F3 round 2 (the admit
port, the driver's bound-talker writes, the AVTP version check, TMR_NO_RESP
held for an owed probe, the 32-bit wrap, the slot bound, the D3 roll-back).

Reuses only the lane's build machinery (ctrl_build.Tree, ctrl_arms.arm_*,
ctrl_mutants.plant) from the tree under test; the substitutions are the
reviewer's own.  A probe is CAUGHT when at least one of the arms it runs
completes with rc 1 and a [FAIL] line.  Copies and builds go under --out.

Usage: python3 r530_2_fw_probes.py --tree <clone> --out <scratch dir> [--only a,b]
"""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--tree", type=Path, required=True)
ap.add_argument("--out", type=Path, required=True)
ap.add_argument("--only", default="")
args = ap.parse_args()
sys.path.insert(0, str(args.tree / "sw" / "firmware" / "ctrl" / "test"))

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
from ctrl_build import CTRL, Outcome, Refusal, Tree  # noqa: E402
from ctrl_mutant import Mutant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

ARMS = {"acmp": ctrl_arms.arm_acmp, "acmpif2": ctrl_arms.arm_acmpif2, "acmpnvm": ctrl_arms.arm_acmpnvm,
        "unit": ctrl_arms.arm_unit, "model": ctrl_arms.arm_model}

# (name, path, old, new, arms to run)
PROBES = (
    ("FW1-rebind-to-another-talker-not-admitted", "acmp/acmp.c",
     "if (s->bound != s->admitted || (s->bound && talker != s->admitted_talker)) {",
     "if (s->bound != s->admitted) {", ("acmp",)),
    ("FW2-admit-port-on-interface-0", "acmp/acmp_mbx.c",
     "(void)mbx_filter_set_bound_talker(interface, sink, bound, talker_entity_id);",
     "(void)interface;\n\t(void)mbx_filter_set_bound_talker(0u, sink, bound, talker_entity_id);", ("acmp", "acmpif2")),
    ("FW3-driver-entry-off-by-one", "mbx/mbx.c",
     "MBX_BND_ENTRY_STRIDE * (uint32_t)entry + reg;", "MBX_BND_ENTRY_STRIDE * (uint32_t)(entry + 1u) + reg;",
     ("unit", "acmp")),
    ("FW4-driver-eid-halves-swapped", "mbx/mbx.c",
     "mbx_place((uint32_t)talker_entity_id, MBX_BOUND_EID_LO_EID_LSB, MBX_BOUND_EID_LO_EID_WIDTH));",
     "mbx_place((uint32_t)(talker_entity_id >> 32), MBX_BOUND_EID_LO_EID_LSB, MBX_BOUND_EID_LO_EID_WIDTH));",
     ("unit", "acmp")),
    ("FW5-admit-without-first-clearing-en", "mbx/mbx.c",
     "\tmbx_hal_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EN), 0u);\n\tif (bound) {",
     "\tif (!bound) {\n\t\tmbx_hal_write32(bnd_reg(interface, entry, MBX_BND_REG_BOUND_EN), 0u);\n\t}\n\tif (bound) {",
     ("unit",)),
    ("FW6-probe-left-ignores-sequence-id", "acmp/acmp.c",
     "if (s->timer_held && wire_be16(o->frame + O_SEQ) == s->probe_seq) {", "if (s->timer_held) {", ("acmp",)),
    ("FW7-stop-keeps-the-hold", "acmp/acmp.c",
     "\ts->timer = ACMP_TIMER_NONE;\n\ts->timer_held = false;\n}", "\ts->timer = ACMP_TIMER_NONE;\n}", ("acmp",)),
    ("FW8-held-timer-counted-for-the-earliest", "acmp/acmp.c",
     "earliest(&any, &at, sm_running(s), s->timer_deadline);",
     "earliest(&any, &at, s->timer != ACMP_TIMER_NONE, s->timer_deadline);", ("acmp",)),
    ("FW9-due-unsigned-compare", "acmp/acmp.c", "return (int32_t)(deadline - at) <= 0;", "return deadline <= at;",
     ("acmp",)),
    ("FW10-earliest-unsigned-compare", "acmp/acmp.c", "(int32_t)(deadline - *at) < 0)", "deadline < *at)",
     ("acmp",)),
    ("FW11-slot-bound-off-by-one", "acmp/acmp_mbx.c", "if (first_slot > MBX_N_TIMERS - MBX_N_IF ||",
     "if (first_slot >= MBX_N_TIMERS - MBX_N_IF ||", ("acmp", "acmpif2")),
    ("FW12-slot-bound-summed", "acmp/acmp_mbx.c", "if (first_slot > MBX_N_TIMERS - MBX_N_IF ||",
     "if (first_slot + MBX_N_IF > MBX_N_TIMERS ||", ("acmp", "acmpif2")),
    ("FW13-d3-rollback-drops-bindings", "acmp/acmp_nvm.c",
     "\tif (walk != NVM_W_BIND) {\n\t\treturn n->others->rollback(n->others->ctx, walk);\n\t}",
     "\tif (walk != NVM_W_BIND) {\n\t\tacmp_restore_rollback(n->acmp);\n"
     "\t\treturn n->others->rollback(n->others->ctx, walk);\n\t}", ("acmpnvm", "acmp")),
    ("FW14-adp-version-only-bit-4", "acmp/acmp.c",
     "#define AVTP_VERSION(frame) (((frame)[O_MSG] >> 4) & 0x07u)",
     "#define AVTP_VERSION(frame) (((frame)[O_MSG] >> 4) & 0x01u)", ("acmp",)),
    ("FW15-version-checked-after-the-sink-match", "acmp/acmp.c",
     "\t    frame[PDU] != ACMP_ADP_SUBTYPE || AVTP_VERSION(frame) != ACMP_AVTP_VERSION ||",
     "\t    frame[PDU] != ACMP_ADP_SUBTYPE || (AVTP_VERSION(frame) != ACMP_AVTP_VERSION && a->cfg.n_sinks == 0u) ||",
     ("acmp",)),
    ("FW16-restored-bindings-not-admitted-at-open", "acmp/acmp.c",
     "void acmp_open(struct acmp *a)\n{\n\tif (!enter(a)) {\n\t\treturn;\n\t}\n\tfinish(a);\n}",
     "void acmp_open(struct acmp *a)\n{\n\t(void)a;\n}", ("acmp", "acmpnvm")),
    ("FW17-one-slot-for-every-interface", "acmp/acmp_mbx.c", "m->ifs[k].slot = (uint8_t)(first_slot + k);",
     "m->ifs[k].slot = (uint8_t)first_slot;", ("acmp", "acmpif2")),
    ("FW18-flag-bits-swapped-both-sides", "acmp/acmp.c", "#define BIND_STARTED 0x02u\n#define BIND_STREAMING_WAIT 0x04u",
     "#define BIND_STARTED 0x04u\n#define BIND_STREAMING_WAIT 0x02u", ("acmp", "acmpnvm")),
    ("FW19-longer-record-applied", "acmp/acmp.c", "if (sink >= a->cfg.n_sinks || len != ACMP_BINDING_BYTES) {\n\t\treturn ACMP_RESTORE_REFUSED;",
     "if (sink >= a->cfg.n_sinks || len < ACMP_BINDING_BYTES) {\n\t\treturn ACMP_RESTORE_REFUSED;", ("acmp", "acmpnvm")),
)

out = args.out.resolve()
out.mkdir(parents=True, exist_ok=True)
base = Tree(CTRL, out / "checkout", out / "reuse")
cut_reuse(base.reuse)
bad = 0
sel = [p for p in PROBES if not args.only or p[0] in args.only.split(",")]
for name, path, old, new, arms in sel:
    m = Mutant(name, path, old, new, arms[0], "", "")
    try:
        copy = ctrl_mutants.plant(m, out / "probes")
    except Refusal as exc:
        print(f"[FIXTURE] {name}: {exc}")
        bad += 1
        continue
    tree = Tree(copy, out / "probes" / name / "build", base.reuse, base.build)
    results = []
    for arm in arms:
        try:
            o = ARMS[arm](tree)
        except Refusal as exc:
            o = Outcome(arm, 2, f"refused: {exc}")
        fails = [ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln]
        results.append((arm, o.rc, fails))
    caught = any(rc == 1 and f for _a, rc, f in results)
    bad += not caught
    summary = "; ".join(f"{a} rc={rc} fails={len(f)}" for a, rc, f in results)
    first = next((f[0] for _a, _rc, f in results if f), "none")
    print(f"[{'CAUGHT' if caught else 'ESCAPED'}] {name}: {summary}\n    first: {first[:300]}")
    shutil.rmtree(out / "probes" / name, ignore_errors=True)
print(f"r530-2 firmware probes: {len(sel) - bad} of {len(sel)} caught")
sys.exit(1 if bad else 0)

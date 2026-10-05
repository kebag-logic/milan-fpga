# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""ctrl_mutants.py - planted defects the control-plane firmware's host test must catch.

Each mutant is one substitution in a COPY of sw/firmware/ctrl (never the
checkout), the arm that must catch it, and a fragment of the name of the check
that must fail. A mutant is caught only when that arm exits 1 AND a `[FAIL]`
line names the check: a build that breaks, or a different check failing, is
reported as an escape, because neither proves the check can see the defect.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path

import ctrl_arms
from ctrl_build import CTRL, Outcome, Refusal, Tree


@dataclass(frozen=True)
class Mutant:
    """One planted defect."""

    name: str
    path: str
    old: str
    new: str
    arm: str
    needle: str


MUTANTS = (
    Mutant("departing-keeps-index", "adp/adp.c",
           "\ta->available_index = 0;                                         // 6.2.2.15",
           "\t// 6.2.2.15", "walk", "available_index"),
    Mutant("down-answers-discover", "adp/adp.c", "if (!a->enabled || a->state != ADP_STATE_WAITING) {",
           "if (!a->enabled) {", "walk", "RCV_ADP_DISCOVER(eid 0) x DOWN"),
    Mutant("link-down-departs", "adp/adp.c", "\t\ttimer_stop(a);                                          // 5.6.3.5.6",
           "\t\t(void)send(a, ADP_MSG_ENTITY_DEPARTING, a->available_index);\n\t\ttimer_stop(a); // 5.6.3.5.6",
           "walk", "LINK_DOWN x WAITING: frames committed"),
    Mutant("gm-change-ignored", "adp/adp.c", "\t\tenter_delay(a, ADP_DRAW_DELAY);                         // 5.6.3.5.7",
           "\t\t(void)0;", "walk", "GM_CHANGE x WAITING"),
    Mutant("delay-ignores-link-down", "adp/adp.c", "\tif (a->state != ADP_STATE_DOWN) {\n\t\ttimer_stop(a);",
           "\tif (a->state == ADP_STATE_WAITING) {\n\t\ttimer_stop(a);", "walk", "LINK_DOWN x DELAY"),
    Mutant("shutdown-in-down-departs", "adp/adp.c",
           "\tif (a->state == ADP_STATE_DOWN) {\n\t\treturn;\n\t}\n\ttimer_stop(a);",
           "\ttimer_stop(a);", "walk", "SHUTDOWN x DOWN"),
    Mutant("draw-kinds-merged", "adp/adp.c", "kind == ADP_DRAW_STARTUP ? ADP_DELAY_STARTUP_MAX_MS : ADP_DELAY_MAX_MS",
           "ADP_DELAY_MAX_MS", "adp", "A9 every startup draw"),
    Mutant("foreign-discover-answered", "adp/adp.c", "if (target != 0u && target != a->entity->entity_id) {",
           "if (target == 1u) {", "adp", "A4 a foreign DISCOVER"),
    Mutant("frame-misses-config-index", "adp/adp.c", "wire_put_be(pdu + 50, a->current_configuration_index, 2);",
           "wire_put_be(pdu + 50, 0u, 2);", "walk", "P11"),
    Mutant("stale-tag-accepted", "adp/adp_mbx.c", "if (!i->armed || ev->timer_tag != i->tag) {",
           "if (!i->armed) {", "adp", "B1 an expiry of the arm a GM_CHANGE replaced"),
    Mutant("latency-extra-read", "adp/adp_mbx.c", "\tmbx_timer_arm(i->slot, i->tag, mbx_now_ms() + delay_ms);",
           "\t(void)mbx_link_up(0);\n\tmbx_timer_arm(i->slot, i->tag, mbx_now_ms() + delay_ms);", "adp",
           "C0 LINK_UP -> TMR_DELAY armed"),
    Mutant("pool-free-leaks", "port/ctrl_pool.c", "\t\tbin->free_head = ptr;\n\t\tbin->free_count++;",
           "\t\tbin->free_count++;", "port", "P2 a released block"),
    Mutant("calloc-overflow-unchecked", "port/ctrl_pool.c", "if (nmemb != 0u && bytes > SIZE_MAX / nmemb) {",
           "if (nmemb == 0u) {", "port", "P3 calloc refuses"),
    Mutant("pool-double-free-accepted", "port/ctrl_pool.c",
           "if (offset % bin->stride != 0u || bin->used[index] == 0u) {",
           "if (offset % bin->stride != 0u) {", "port", "P2 a double free"),
    Mutant("debug-truncation-uncounted", "port/ctrl_debug.c", "\t\ttruncated++;\n", "", "port", "S2 the truncation"),
    Mutant("tick-count-ignored", "loop/ctrl_loop.c", "for (uint32_t k = 0; k < count; ++k) {",
           "for (uint32_t k = 0; k < (count != 0u ? 1u : 0u); ++k) {", "port", "L4 every centisecond"),
    Mutant("rx-pass-unbounded", "loop/ctrl_loop.c", "for (unsigned k = 0; k < CTRL_LOOP_RX_PER_PASS; ++k) {",
           "for (unsigned k = 0; k < 64u; ++k) {", "port", "L2 a pass takes at most"),
    Mutant("filter-opened-before-eid", "loop/ctrl_loop.c", "\tmbx_filter_set_own_eid(entity_id);\n",
           "\tmbx_filter_open(open);\n\tmbx_filter_set_own_eid(entity_id);\n", "port", "L1 OWN_EID is written before"),
    Mutant("rx-no-resync", "mbx/mbx.c",
           "\trx_tail[ch] = head;\n\tmbx_hal_write32(ch_reg(ch, MBX_CH_REG_RX_TAIL), head);",
           "\t(void)ch;\n\t(void)head;", "port",
           "D1 and the ring is resynchronised"),
    Mutant("tx-overfills", "mbx/mbx.c", "record > tx_words[ch] - used", "record > tx_words[ch] - used + 23u", "port",
           "D3 a held merge fills the ring"),
    Mutant("lanes-big-endian", "mbx/mbx_wire.h", "\t\tword |= (uint32_t)p[i] << (8u * i);",
           "\t\tword |= (uint32_t)p[i] << (8u * (3u - i));", "model", "F1 frame byte k is ring word"),
    Mutant("model-rate-unlimited", "host/mbx_model.c", "\tif (ch->tokens == 0u) {",
           "\tif (ch->tokens == 0u && false) {",
           "model", "T0 the frames past it count in RATE_DROP"),
    Mutant("model-gm-hi-live", "host/mbx_model.c", "\t\treturn m->gm_hi_snap[i];",
           "\t\treturn (uint32_t)(m->gm_id[i] >> 32);", "model", "G0 GM_HI reads the snapshot"),
)


def plant(m: Mutant, root: Path) -> Path:
    """A copy of the firmware tree with the mutant written into it."""
    copy = root / m.name / "ctrl"
    if copy.exists():
        shutil.rmtree(copy)
    shutil.copytree(CTRL, copy, ignore=shutil.ignore_patterns("__pycache__"))
    target = copy / m.path
    text = target.read_text(encoding="utf-8")
    if text.count(m.old) != 1:
        raise Refusal(f"mutant {m.name}: its fixture occurs {text.count(m.old)} times in {m.path}")
    target.write_text(text.replace(m.old, m.new), encoding="utf-8")
    return copy


def caught(m: Mutant, outcome: Outcome) -> bool:
    """The named check of the named arm failed in a completed run."""
    return outcome.rc == 1 and any("[FAIL]" in ln and m.needle in ln for ln in outcome.log.splitlines())


def campaign(root: Path, reuse: Path) -> bool:
    """Plant every mutant; True when one escaped."""
    arms = {"model": ctrl_arms.arm_model, "port": ctrl_arms.arm_port, "adp": ctrl_arms.arm_adp,
            "walk": ctrl_arms.arm_walk}
    escaped = 0
    for m in MUTANTS:
        tree = Tree(plant(m, root), root / m.name / "build", reuse)
        try:
            outcome = arms[m.arm](tree)
        except Refusal as exc:
            outcome = Outcome(m.arm, 2, f"refused: {exc}")
        ok = caught(m, outcome)
        fails = [ln.strip() for ln in outcome.log.splitlines() if "[FAIL]" in ln]
        print(f"[{'ok' if ok else 'ESCAPED'}] mutant {m.name} ({m.arm}): {len(fails)} check(s) failed"
              f"{'' if ok else ', none named ' + repr(m.needle)}")
        if fails:
            print(f"    first: {fails[0]}")
        escaped += 0 if ok else 1
    print(f"mutants: {len(MUTANTS) - escaped} of {len(MUTANTS)} caught")
    return escaped != 0

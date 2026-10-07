#!/usr/bin/env python3
"""Reviewer-planted defects for PR #687 (round R528-1).

Each defect is planted into a scratch copy of sw/firmware/ctrl through the
repository's own plant() helper; the named arms are then built and run.
A defect counts as caught only when its arm completes with rc 1 and at least
one named [FAIL] line (a build failure is rc 2 and is reported as NOT caught).
Every [FAIL] line is printed so the catching test is visible.

Usage: r528_mutants.py REPO OUT [NAME ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
only = set(sys.argv[3:])
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(repo / "sw/firmware/gtest"))

import ctrl_arms  # noqa: E402
import ctrl_mutants  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import Outcome, Refusal, Tree  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

C = "maap/maap.c"
A = "maap/maap_mbx.c"
S = "maap/maap_csr.c"
P = "app/ctrl_app.c"

# name, path, old, new, arms
DEFECTS = [
    # core: Table B.7 cells
    ("r-probe-state-defends", C, "type == MAAP_MSG_PROBE && m->state == MAAP_DEFEND",
     "type == MAAP_MSG_PROBE && m->state == MAAP_PROBE", ("maap",)),
    ("r-probe-state-compare-mac-on-defend", C, "(m->state == MAAP_PROBE && type != MAAP_MSG_PROBE) ||",
     "false ||", ("maap",)),
    ("r-compare-mac-always-loses", C, "reverse_mac(m->mac) >= reverse_mac(peer)", "true", ("maap",)),
    ("r-compare-mac-strict", C, "reverse_mac(m->mac) >= reverse_mac(peer)",
     "reverse_mac(m->mac) > reverse_mac(peer)", ("maap",)),
    ("r-reverse-five-octets", C, "for (unsigned i = 0; i < 6u; ++i) {", "for (unsigned i = 0; i < 5u; ++i) {",
     ("maap",)),
    # core: timers, draws, PDUs
    ("r-probe-uses-announce-interval", C, "start_timer(m, false);\n\t\trequest(m, MAAP_MSG_PROBE);",
     "start_timer(m, true);\n\t\trequest(m, MAAP_MSG_PROBE);", ("maap",)),
    ("r-no-jitter-allowance", C, "base + MAAP_SERVICE_MS + 1u + draw(m, variation - 2u * MAAP_SERVICE_MS - 1u)",
     "base + draw(m, variation)", ("maap",)),
    ("r-seed-mac-ignored", C, "(uint32_t)m->mac + m->ports->clock", "0u + m->ports->clock", ("maap",)),
    ("r-generate-past-pool-end", C, "draw(m, MAAP_POOL_SIZE - m->count + 1u)",
     "draw(m, MAAP_POOL_SIZE - m->count + 2u)", ("maap",)),
    ("r-conflict-count-to-own-end", C, "(uint16_t)(last - overlap)", "(uint16_t)(ours_end - overlap)", ("maap",)),
    ("r-own-range-one-address", C, "uint64_t ours_end = m->base + m->count;", "uint64_t ours_end = m->base + 1u;",
     ("maap",)),
    ("r-conflict-start-nonzero-in-request", C, "enqueue(m, type, MAAP_MULTICAST, m->base, m->count, 0, 0);",
     "enqueue(m, type, MAAP_MULTICAST, m->base, m->count, m->base, 0);", ("maap",)),
    # core: lifecycle
    ("r-release-keeps-timer", C, "static void withdraw(struct maap *m)\n{\n\tstop_timer(m);",
     "static void withdraw(struct maap *m)\n{\n\t(void)0;", ("maap",)),
    ("r-link-down-keeps-claim", C, "\t\t} else {\n\t\t\twithdraw(m);\n\t\t}", "\t\t} else {\n\t\t\t(void)0;\n\t\t}",
     ("maap",)),
    ("r-restart-keeps-queue", C, "\tm->queued = 0; // old allocation", "\tm->queued += 0; // old allocation", ("maap",)),
    ("r-restart-reuses-range", C, "\tm->state = MAAP_INITIAL;\n\treserve(m, 0);",
     "\tm->state = MAAP_INITIAL;\n\treserve(m, m->base);", ("maap",)),
    ("r-unicast-defend-any-destination", C, "(f[15] == MAAP_MSG_DEFEND && dst == m->mac)",
     "(f[15] == MAAP_MSG_DEFEND)", ("maap",)),
    ("r-in-call-left-set-after-poll", C, "\tbool owed = pump(m);\n\tm->in_call = false;",
     "\tbool owed = pump(m);\n\tm->in_call = m->queued != 0u;", ("maap",)),
    # adapter
    ("r-arm-half-delay", A, "mbx_now_ms() + delay_ms);", "mbx_now_ms() + delay_ms / 2u);", ("maap",)),
    ("r-cancel-keeps-armed", A, "\ti->armed = false;\n\tmbx_timer_cancel", "\tmbx_timer_cancel", ("maap",)),
    ("r-link-level-not-recorded", A, "\t\t\ti->link = ev->link_up;\n", "", ("maap",)),
    ("r-envelope-own-interface-only", A,
     "uint16_t n = k == interface ? count : (core->state == MAAP_INITIAL ? 0u : core->count);",
     "uint16_t n = k == interface ? count : 0u;", ("maap_if2",)),
    ("r-poll-first-interface-only", A, "for (unsigned k = 0; k < MBX_N_IF; ++k) {\n\t\towed = maap_poll",
     "for (unsigned k = 0; k < 1u; ++k) {\n\t\towed = maap_poll", ("maap_if2",)),
    ("r-timer-slot-shared", A, "m->ifs[k].slot = (uint8_t)(first_slot + k);",
     "m->ifs[k].slot = (uint8_t)(first_slot);", ("maap_if2",)),
    # corrected fixtures (the first spellings broke the build under -Werror)
    ("r-compare-mac-always-loses-v2", C, "reverse_mac(m->mac) >= reverse_mac(peer)",
     "(reverse_mac(m->mac) >= reverse_mac(peer) || true)", ("maap",)),
    ("r-compare-mac-lsb-only", C, "reverse_mac(m->mac) >= reverse_mac(peer)",
     "(reverse_mac(m->mac) >> 40) >= (reverse_mac(peer) >> 40)", ("maap",)),
    ("r-conflict-count-to-own-end-v2", C, "(uint16_t)(last - overlap)",
     "(uint16_t)(ours_end - overlap + 0u * last)", ("maap",)),
    ("r-unicast-defend-any-destination-v2", C, "(f[15] == MAAP_MSG_DEFEND && dst == m->mac)",
     "(f[15] == MAAP_MSG_DEFEND && (dst == m->mac || true))", ("maap",)),
    # CSR output
    ("r-csr-enable-before-programming", S,
     "\tif (c->aaf_outputs != 0u) {\n\t\taddress(c, interface, AAF_DMLO",
     "\twrite_word(c, interface, AAF_CTRL, c->aaf_control);\n"
     "\twrite_word(c, interface, CRFT_CTRL, c->crf_control);\n"
     "\tif (c->aaf_outputs != 0u) {\n\t\taddress(c, interface, AAF_DMLO", ("maap",)),
    ("r-csr-loss-keeps-aaf", S, "write_word(c, interface, AAF_CTRL, c->aaf_control & ~1u);",
     "write_word(c, interface, AAF_CTRL, c->aaf_control);", ("maap",)),
    ("r-csr-high-word-unshifted", S, "(uint32_t)(mac >> 32)", "(uint32_t)(mac >> 31)", ("maap",)),
    ("r-csr-select-listener", S, "STRM_SEL, 0x100u | k);", "STRM_SEL, k);", ("maap",)),
    # composition
    ("r-app-shares-adp-slots", P, "count, MBX_N_IF, allocation, ctx)", "count, 0u, allocation, ctx)", ("maap",)),
]


def main() -> int:
    out.mkdir(parents=True, exist_ok=True)
    tree0 = Tree(ctrl_mutants.CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
    cut_reuse(tree0.reuse)
    arms = {"maap": ctrl_arms.arm_maap, "maap_if2": ctrl_arms.arm_maap_if2}
    escaped = 0
    for name, path, old, new, use in DEFECTS:
        if only and name not in only:
            continue
        m = ctrl_mutants.Mutant(name, path, old, new, use[0], "", "")
        try:
            copy = ctrl_mutants.plant(m, out / "planted")
        except Refusal as exc:
            print(f"[FIXTURE] {name}: {exc}", flush=True)
            escaped += 1
            continue
        tree = Tree(copy, out / "planted" / name / "build", tree0.reuse, tree0.build)
        result = []
        for arm in use:
            try:
                outcome = arms[arm](tree)
            except Refusal as exc:
                outcome = Outcome(arm, 2, f"refused: {exc}")
            fails = sorted({ln.strip().split(":", 1)[0] for ln in outcome.log.splitlines() if "[FAIL]" in ln})
            ok = ctrl_mutants.caught("", "", outcome)
            result.append((arm, outcome.rc, ok, fails))
        caught = any(r[2] for r in result)
        escaped += 0 if caught else 1
        print(f"[{'caught' if caught else 'ESCAPED'}] {name}", flush=True)
        for arm, rc, ok, fails in result:
            print(f"    arm={arm} rc={rc} named-fail={ok} failing: {fails[:6]}", flush=True)
    print(f"reviewer defects escaped: {escaped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

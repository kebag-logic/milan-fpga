#!/usr/bin/env python3
"""Reviewer-planted defects for PR #687 round R528-2 (exact head 938497af).

Mode "reviewer": plant each reviewer defect below into a scratch copy of
sw/firmware/ctrl through the repository's own plant() helper, run the named
arms, and print every failing test. Caught means rc 1 with a [FAIL] line in a
completed arm run (a build failure is rc 2 and is NOT caught).

Mode "repo": run the repository's own named defects (by name) and grade them
with the repository's caught(test, words), on their declared arm and, where
asked, on extra arms as well.

Usage: r528_2_mutants.py REPO OUT reviewer [NAME ...]
       r528_2_mutants.py REPO OUT repo NAME[@arm,arm] ...
"""
from __future__ import annotations

import sys
from pathlib import Path

repo = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
mode = sys.argv[3]
only = sys.argv[4:]
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
IRQ = ("\tmbx_irq_enable(mbx_place(channels, MBX_IRQ_ENABLE_RX_LSB, MBX_IRQ_ENABLE_RX_WIDTH) |\n"
       "\t\t       mbx_place(1u, MBX_IRQ_ENABLE_EVT_LSB, MBX_IRQ_ENABLE_EVT_WIDTH));\n")

# name, path, old, new, arms
DEFECTS = [
    # R528-1 escapes, re-run unchanged (F3, F4, F5)
    ("r-reverse-five-octets", C, "for (unsigned i = 0; i < 6u; ++i) {", "for (unsigned i = 0; i < 5u; ++i) {",
     ("maap",)),
    ("r-compare-mac-lsb-only", C, "reverse_mac(m->mac) >= reverse_mac(peer)",
     "(reverse_mac(m->mac) >> 40) >= (reverse_mac(peer) >> 40)", ("maap",)),
    ("r-restart-reuses-range", C, "\tm->state = MAAP_INITIAL;\n\treserve(m, 0);",
     "\tm->state = MAAP_INITIAL;\n\treserve(m, m->base);", ("maap",)),
    ("r-csr-enable-before-programming", S,
     "\tif (c->aaf_outputs != 0u) {\n\t\taddress(c, interface, AAF_DMLO",
     "\twrite_word(c, interface, AAF_CTRL, c->aaf_control);\n"
     "\twrite_word(c, interface, CRFT_CTRL, c->crf_control);\n"
     "\tif (c->aaf_outputs != 0u) {\n\t\taddress(c, interface, AAF_DMLO", ("maap",)),
    ("r-csr-select-listener", S, "STRM_SEL, 0x100u | k);", "STRM_SEL, k);", ("maap",)),
    ("r-poll-first-interface-only", A, "for (unsigned k = 0; k < MBX_N_IF; ++k) {\n\t\towed = maap_poll",
     "for (unsigned k = 0; k < 1u; ++k) {\n\t\towed = maap_poll", ("maap_if2",)),
    # R529-1-F1: the app's interrupt enable, own spellings, one and two interfaces
    ("r2-irq-adp-only", P, "mbx_irq_enable(mbx_place(channels,", "mbx_irq_enable(mbx_place(1u << MBX_CH_ADP,",
     ("maap", "maap_if2")),
    ("r2-irq-no-enable-write", P, IRQ, "", ("maap", "maap_if2")),
    ("r2-irq-maap-only", P, "mbx_irq_enable(mbx_place(channels,", "mbx_irq_enable(mbx_place(1u << MBX_CH_MAAP,",
     ("maap", "maap_if2")),
    ("r2-irq-no-event", P, IRQ, IRQ.replace(" |\n\t\t       mbx_place(1u, MBX_IRQ_ENABLE_EVT_LSB, "
                                            "MBX_IRQ_ENABLE_EVT_WIDTH));", ");"), ("maap", "maap_if2")),
    # R528-1-F1: Begin! before PortOperational! (Table B.7 note a)
    ("r2-up-ignores-saved-range", C, "\t\t\tif (m->preferred != 0u) {", "\t\t\tif (false && m->preferred != 0u) {",
     ("maap",)),
    ("r2-saved-range-never-consumed", C, "\tm->preferred = 0; // Table B.7 note a", "\t(void)0; // Table B.7 note a",
     ("maap", "maap_if2")),
    ("r2-saved-range-reused-on-conflict", C, "\tm->state = MAAP_INITIAL;\n\treserve(m, 0);",
     "\tm->state = MAAP_INITIAL;\n\treserve(m, m->preferred);", ("maap",)),
    ("r2-up-saved-range-no-send", C, "\t\t\t\treserve(m, m->preferred); // Begin!",
     "\t\t\t\tm->base = m->preferred; m->state = MAAP_PROBE; // Begin!", ("maap",)),
    # R528-1-F3: priority comparison variants
    ("r2-forward-octet-order", C, "reverse_mac(m->mac) >= reverse_mac(peer)", "m->mac >= peer", ("maap",)),
    ("r2-first-octet-ignored", C, "reverse_mac(m->mac) >= reverse_mac(peer)",
     "(reverse_mac(m->mac) >> 8) >= (reverse_mac(peer) >> 8)", ("maap",)),
    ("r2-last-octet-ignored", C, "reverse_mac(m->mac) >= reverse_mac(peer)",
     "(reverse_mac(m->mac) & 0xffffffffffULL) >= (reverse_mac(peer) & 0xffffffffffULL)", ("maap",)),
    # R528-1-F4: CSR order variants
    ("r2-csr-crf-enable-before-crf-address", S, "\tif (c->crf_output) {\n\t\taddress(c, interface, CRFT_DMLO",
     "\twrite_word(c, interface, CRFT_CTRL, c->crf_control);\n"
     "\tif (c->crf_output) {\n\t\taddress(c, interface, CRFT_DMLO", ("maap",)),
    ("r2-csr-aaf-enable-before-window", S, "\tuint32_t selection = c->port.read32",
     "\twrite_word(c, interface, AAF_CTRL, c->aaf_control);\n\tuint32_t selection = c->port.read32", ("maap",)),
    ("r2-csr-selection-not-restored", S, "\twrite_word(c, interface, STRM_SEL, selection);\n", "", ("maap",)),
    # corrected fixtures (the first spellings broke the build under -Werror: rc 2, not caught)
    ("r2-forward-octet-order-v2", C, "reverse_mac(m->mac) >= reverse_mac(peer)",
     "(0u * reverse_mac(m->mac) + m->mac) >= (0u * reverse_mac(peer) + peer)", ("maap",)),
    ("r2-csr-selection-not-restored-v2", S, "\twrite_word(c, interface, STRM_SEL, selection);\n", "\t(void)selection;\n",
     ("maap",)),
]


def run_arms(name: str, copy: Path, tree0: Tree, use: tuple[str, ...], grade=None) -> bool:
    arms = {"maap": ctrl_arms.arm_maap, "maap_if2": ctrl_arms.arm_maap_if2,
            "maap_debug": ctrl_arms.arm_maap_debug}
    tree = Tree(copy, out / "planted" / name / "build", tree0.reuse, tree0.build)
    result = []
    for arm in use:
        try:
            outcome = arms[arm](tree)
        except Refusal as exc:
            outcome = Outcome(arm, 2, f"refused: {exc}")
        fails = sorted({ln.strip().split(":", 1)[0] for ln in outcome.log.splitlines() if "[FAIL]" in ln})
        ok = grade(outcome) if grade else ctrl_mutants.caught("", "", outcome)
        result.append((arm, outcome.rc, ok, fails))
    for arm, rc, ok, fails in result:
        print(f"    arm={arm} rc={rc} caught={ok} failing: {fails[:8]}", flush=True)
    return result


def main() -> int:
    out.mkdir(parents=True, exist_ok=True)
    tree0 = Tree(ctrl_mutants.CTRL, out / "checkout", out / "reuse", fw_gtest.Build(jobs=4))
    cut_reuse(tree0.reuse)
    escaped = 0
    total = 0
    if mode == "reviewer":
        for name, path, old, new, use in DEFECTS:
            if only and name not in only:
                continue
            total += 1
            m = ctrl_mutants.Mutant(name, path, old, new, use[0], "", "")
            try:
                copy = ctrl_mutants.plant(m, out / "planted")
            except Refusal as exc:
                print(f"[FIXTURE] {name}: {exc}", flush=True)
                escaped += 1
                continue
            print(f"[run] {name}", flush=True)
            result = run_arms(name, copy, tree0, use)
            per_arm = all(r[2] for r in result)
            any_arm = any(r[2] for r in result)
            tag = "caught-all-arms" if per_arm else ("caught-some-arm" if any_arm else "ESCAPED")
            escaped += 0 if any_arm else 1
            print(f"[{tag}] {name}", flush=True)
    else:
        by_name = {m.name: m for m in ctrl_mutants.MUTANTS}
        for spec in only:
            name, _, extra = spec.partition("@")
            m = by_name[name]
            total += 1
            copy = ctrl_mutants.plant(m, out / "planted")
            arms = tuple(dict.fromkeys((m.arm, *(extra.split(",") if extra else ()))))
            print(f"[run] {name} declared ({m.arm}, {m.test!r}, {m.needle!r})", flush=True)
            result = run_arms(name, copy, tree0, arms,
                              grade=lambda o: ctrl_mutants.caught(m.test, m.needle, o))
            ok = all(r[2] for r in result)
            escaped += 0 if ok else 1
            print(f"[{'named-caught' if ok else 'NOT-NAMED'}] {name} arms={','.join(arms)}", flush=True)
    print(f"defects: {total}, escaped: {escaped}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

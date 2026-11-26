#!/usr/bin/env python3
"""draw_plants.py - reviewer-owned plant campaign for the ADP draw (#970).

Plants the author's draw table (adp_first_mutants.MUTANTS plus the core's
seed-left-at-zero plant) and the reviewer's own falsification plants into
disposable copies, through the repository's own campaign driver, and reports
each plant's verdict. Also reports whether the full plant table leaves any
host test unnamed.

usage: python3 -B draw_plants.py <repo-root> <work-dir> [--jobs N]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("repo", type=Path)
    ap.add_argument("work", type=Path)
    ap.add_argument("--jobs", type=int, default=4)
    args = ap.parse_args()
    test_dir = args.repo.resolve() / "sw/firmware/ctrl/test"
    sys.path.insert(0, str(test_dir))
    sys.path.insert(0, str(args.repo.resolve() / "sw/firmware/gtest"))
    import adp_first_mutants
    import ctrl_mutants
    import fw_gtest
    from ctrl_build import Tree
    from ctrl_mutant import ADP_C, Mutant
    from ctrl_reuse import cut_reuse

    full_unnamed = ctrl_mutants.unnamed_tests()
    print(f"full table: {len(ctrl_mutants.MUTANTS)} plants; {len(full_unnamed)} host test(s) named by no plant")
    for t in full_unnamed:
        print(f"  unnamed: {t}")

    adp_mbx = "adp/adp_mbx.c"
    clock = "clock_fn != NULL ? clock_fn(clock_ctx) : mbx_now_ms();"
    plat_clock = "\treturn (uint32_t)p->env->flash->now_us(p->env->flash->ctx);\n"
    rise = "\t\t\tleave_down(a, ADP_DRAW_DELAY);  "
    enable_read = "\ta->enabled = true;\n\tport_active = true;\n"
    own = (
        # the adapter reads the clock twice per sample: H9 counts one read per qualified rise
        Mutant("r-clock-read-twice", adp_mbx, clock,
               "clock_fn != NULL ? (clock_fn(clock_ctx), clock_fn(clock_ctx)) : mbx_now_ms();", "adp",
               adp_first_mutants.H9, "H9 each qualified LINK_UP reads the clock once through the adapter"),
        # the base pin's behaviour: a sample at the enable whatever the link, none at a LINK_UP
        Mutant("r-base-pin-semantics", ADP_C, enable_read,
               "\ta->enabled = true;\n\ta->rng ^= a->ports->seed(a->ports->ctx);\n\tport_active = true;\n",
               "adp", adp_first_mutants.H9, "H9 a start with the link down reads no clock",
               also=(("adp", adp_first_mutants.H10, "H10 boots apart only at the LINK_UP draw apart"),)),
        Mutant("r-base-pin-link-up", ADP_C, rise, "\t\t\tenter_delay(a, ADP_DRAW_DELAY);  ", "adp",
               adp_first_mutants.H10, "H10 boots apart only at the LINK_UP draw apart",
               also=(("platboot1", adp_first_mutants.B27, "B27 boots apart only in the clock at the LINK_UP"),
                     ("platboot2", adp_first_mutants.B27, "B27 boots apart only in the clock at the LINK_UP"))),
        # the platform hands the clock's high word: a constant over a boot
        Mutant("r-plat-clock-high-word", "plat/ctrl_plat.c", plat_clock,
               "\treturn (uint32_t)(p->env->flash->now_us(p->env->flash->ctx) >> 32);\n", "platboot1",
               adp_first_mutants.B25, adp_first_mutants.B25_WORDS,
               also=(("platboot1", adp_first_mutants.B27, "B27 boots apart only in the clock at the LINK_UP"),)),
        # the platform clock read once and cached: a LINK_UP after ready reads the boot's value
        Mutant("r-plat-clock-cached", "plat/ctrl_plat.c", plat_clock,
               "\tstatic uint32_t once;\n\tstatic bool have;\n\tif (!have) {\n\t\thave = true;\n"
               "\t\tonce = (uint32_t)p->env->flash->now_us(p->env->flash->ctx);\n\t}\n\treturn once;\n",
               "platboot1", adp_first_mutants.B27, "B27 boots apart only in the clock at the LINK_UP"),
    )
    seed_zero = tuple(m for m in ctrl_mutants.MUTANTS if m.name == "seed-left-at-zero")
    table = tuple(adp_first_mutants.MUTANTS) + seed_zero + own
    print(f"campaign: {len(adp_first_mutants.MUTANTS)} draw-table plants + {len(seed_zero)} core plant + "
          f"{len(own)} reviewer plants")
    ctrl_mutants.MUTANTS = table
    ctrl_mutants.unnamed_tests = lambda: []
    work = args.work.resolve()
    tree = Tree(test_dir.parent, work / "checkout", work / "reuse", fw_gtest.Build(jobs=args.jobs))
    cut_reuse(tree.reuse)
    escaped = ctrl_mutants.campaign(work / "mutants", tree.reuse, args.jobs)
    print(f"draw_plants: {'ESCAPED' if escaped else 'ALL CAUGHT'}")
    return 1 if escaped else 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Plant the reviewed head's ADP draw defects, and the reviewer's own probes, with the
repository's own planting and arms (sw/firmware/ctrl/test/ctrl_mutants.py plant/caught).

  table : adp_first_mutants.MUTANTS plus ctrl_mutants' latency-extra-read, each required
          caught by its own test's words (the author's claim of 19 of 19);
  probes: reviewer plants; for each, every listed arm is run and the [FAIL] lines are
          recorded, so an ESCAPE (no check fails anywhere) is visible.

Usage: python3 -B adp_probe.py <clone> <work root> [--jobs N]
Writes nothing inside <clone>: plant() copies the firmware tree under <work root>/work.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("clone", type=Path)
    ap.add_argument("root", type=Path)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--only", choices=("table", "probes", "both"), default="both")
    ap.add_argument("--reuse", type=Path, help="a reuse directory the gate prepared (the walk arm needs it)")
    ap.add_argument("--names", nargs="*", help="only these table plants")
    args = ap.parse_args()
    sys.path.insert(0, str(args.clone / "sw/firmware/ctrl/test"))
    sys.path.insert(0, str(args.clone / "sw/firmware/gtest"))
    import ctrl_mutants as cm
    import adp_first_mutants
    import fw_gtest
    from ctrl_build import Outcome, Refusal, Tree
    from ctrl_mutant import Mutant

    table = list(adp_first_mutants.MUTANTS) + [m for m in cm.MUTANTS if m.name == "latency-extra-read"]
    adp_clock = "\treturn (uint32_t)p->env->flash->now_us(p->env->flash->ctx);\n"
    probes = [
        # the platform's clock read at millisecond resolution: the change's "microsecond clock" lost
        (Mutant("r-plat-clock-in-ms", "plat/ctrl_plat.c", adp_clock,
                "\treturn (uint32_t)(p->env->flash->now_us(p->env->flash->ctx) / 1000u);\n",
                "platboot1", "", ""), ("platboot1", "platboot2", "plat")),
        # the platform's clock read at a 1,024 us granule
        (Mutant("r-plat-clock-1024us-granule", "plat/ctrl_plat.c", adp_clock,
                "\treturn (uint32_t)p->env->flash->now_us(p->env->flash->ctx) & ~0x3FFu;\n",
                "platboot1", "", ""), ("platboot1", "platboot2")),
        # the interface never recorded: every interface seeded as interface 0
        (Mutant("r-seed-interface-not-set", "adp/adp_mbx.c", "\t\tseed_interface = k;\n", "",
                "platboot2", "", ""), ("platboot2", "adp")),
        # the sample's low ten bits dropped in the adapter
        (Mutant("r-seed-sample-low-bits-dropped", "adp/adp_mbx.c",
                "\tuint32_t sum = (uint32_t)e->mac + sample;\n",
                "\tuint32_t sum = (uint32_t)e->mac + (sample >> 10);\n", "adp", "", ""), ("adp",)),
        # the clock wired only after ADP's release (step 9): the seed falls back to NOW_MS
        (Mutant("r-plat-clock-wired-after-release", "plat/ctrl_plat.c",
                "\tctrl_app_release_adp(&p->app);\n",
                "\tctrl_app_release_adp(&p->app);\n\tadp_mbx_set_clock(adp_clock, p);\n",
                "platboot1", "", ""), ("platboot1",)),
    ]
    # the last probe also removes the original wiring
    arms = {"adp": cm.ctrl_arms.arm_adp, "walk": cm.ctrl_arms.arm_walk,
            "platboot1": lambda tree: cm.plat_arms.arm_platboot(tree, 1),
            "platboot2": lambda tree: cm.plat_arms.arm_platboot(tree, 2),
            "plat": cm.plat_arms.arm_plat}
    build = fw_gtest.Build(jobs=args.jobs)
    reuse = args.reuse or args.root / "reuse"
    reuse.mkdir(parents=True, exist_ok=True)
    rc = 0

    def run(m, arm_names):
        ctrl, stack = cm.plant(m, args.root)
        if m.name == "r-plat-clock-wired-after-release":
            f = ctrl / "plat/ctrl_plat.c"
            t = f.read_text(encoding="utf-8")
            first = "\tadp_mbx_set_clock(adp_clock, p);\n\t// The console's poll"
            assert t.count(first) == 1
            f.write_text(t.replace(first, "\t// The console's poll"), encoding="utf-8")
        tree = Tree(ctrl, args.root / "work" / "build", reuse, build, stack)
        res = {}
        for arm in arm_names:
            try:
                res[arm] = arms[arm](tree)
            except Refusal as exc:
                res[arm] = Outcome(arm, 2, f"refused: {exc}")
        return res

    if args.only in ("table", "both"):
        caught_n = 0
        for m in [t for t in table if not args.names or t.name in args.names]:
            res = run(m, [k[0] for k in m.kills()])
            missed = [f"{a}: {t} on {n!r}" for a, t, n in m.kills() if not cm.caught(t, n, res[a])]
            fails = [ln.strip() for o in res.values() for ln in o.log.splitlines() if "[FAIL]" in ln]
            ok = not missed
            caught_n += ok
            print(f"[{'ok' if ok else 'ESCAPED'}] table {m.name}: {len(fails)} failed check(s)"
                  f"{'' if ok else '; missed ' + '; '.join(missed)}")
            if fails:
                print(f"    first: {fails[0][:220]}")
            rc |= 0 if ok else 1
        print(f"TABLE: {caught_n} of {len([t for t in table if not args.names or t.name in args.names])} caught by their own test's words")
    if args.only in ("probes", "both"):
        for m, arm_names in probes:
            res = run(m, arm_names)
            fails = [ln.strip() for o in res.values() for ln in o.log.splitlines() if "[FAIL]" in ln]
            rcs = ", ".join(f"{a} rc={o.rc}" for a, o in res.items())
            verdict = "CAUGHT" if fails else "ESCAPED"
            print(f"[{verdict}] probe {m.name} ({rcs}): {len(fails)} failed check(s)")
            for ln in fails[:3]:
                print(f"    {ln[:220]}")
            for a, o in res.items():
                if o.rc == 2:
                    print(f"    {a}: {o.log[:300]}")
    shutil.rmtree(args.root / "work", ignore_errors=True)
    print("RESULT:", "PASS" if rc == 0 else "FAIL")
    return rc


if __name__ == "__main__":
    sys.exit(main())

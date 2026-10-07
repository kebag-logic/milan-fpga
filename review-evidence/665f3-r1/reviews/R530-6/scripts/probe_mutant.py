#!/usr/bin/env python3
"""Plant one defect into a COPY of the ctrl firmware tree and run EVERY arm,
recording each arm's rc and every [FAIL] line, so a defect's full set of
failing checks is visible (not only the one its campaign row names).

Usage: probe_mutant.py <clone-root> <scratch-root> <name> [--jobs N]
<name> is a row of the clone's campaign table or one of the reviewer probes
below. Writes <scratch-root>/<name>.json and prints a summary.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("clone", type=Path)
    ap.add_argument("scratch", type=Path)
    ap.add_argument("name")
    ap.add_argument("--jobs", type=int, default=1)
    a = ap.parse_args()
    test_dir = a.clone.resolve() / "sw/firmware/ctrl/test"
    sys.path.insert(0, str(test_dir))
    import ctrl_build  # noqa: F401
    import ctrl_arms
    import ctrl_mutants
    import fw_gtest
    from ctrl_build import Refusal, Tree, Outcome
    from ctrl_mutant import Mutant
    from ctrl_reuse import cut_reuse

    reviewer = {
        "rp-null": Mutant("rp-null", "app/ctrl_app.c", "\t\tmac[k] = cfg->entity->mac;\n",
                          "\t\tmac[k] = cfg->entity->mac;\n", "", "", ""),
        "rp-maap-mac-plus-one": Mutant("rp-maap-mac-plus-one", "app/ctrl_app.c", "\t\tmac[k] = cfg->entity->mac;\n",
                                       "\t\tmac[k] = cfg->entity->mac + 1u;\n", "", "", ""),
        "rp-maap-pass-event-7": Mutant("rp-maap-pass-event-7", "maap/maap_mbx.h",
                                       "CTRL_LOOP_EVENTS_PER_PASS * (6u + MAAP_MBX_EVENT_MAX)",
                                       "CTRL_LOOP_EVENTS_PER_PASS * (7u + MAAP_MBX_EVENT_MAX)", "", "", ""),
        "rp-share-rx-record-plus-one": Mutant("rp-share-rx-record-plus-one", "app/ctrl_app.h",
                                              "MBX_CH_MAAP_MAX_FRAME_BYTES / 4u)\n",
                                              "MBX_CH_MAAP_MAX_FRAME_BYTES / 4u + 1u)\n", "", "", ""),
    }
    table = {m.name: m for m in ctrl_mutants.MUTANTS}
    m = reviewer.get(a.name) or table[a.name]
    root = a.scratch.resolve() / a.name
    reuse = root / "reuse"
    cut_reuse(reuse)
    arms = {"model": ctrl_arms.arm_model, "port": ctrl_arms.arm_port, "adp": ctrl_arms.arm_adp,
            "unit": ctrl_arms.arm_unit, "walk": ctrl_arms.arm_walk, "acmp": ctrl_arms.arm_acmp,
            "acmpwalk": ctrl_arms.arm_acmpwalk, "acmpnvm": ctrl_arms.arm_acmpnvm, "acmpif2": ctrl_arms.arm_acmpif2,
            "entity": ctrl_arms.arm_entity, "maap": ctrl_arms.arm_maap, "maap_debug": ctrl_arms.arm_maap_debug,
            "maap_if2": ctrl_arms.arm_maap_if2, "rv32": lambda tree: ctrl_arms.arm_rv32(tree, True),
            "reentry_debug": ctrl_arms.arm_reentry_debug, "reentry_release": ctrl_arms.arm_reentry_release}
    tree = Tree(ctrl_mutants.plant(m, root), root / "build", reuse, fw_gtest.Build(jobs=a.jobs))
    result = {"name": m.name, "path": m.path, "old": m.old, "new": m.new, "expected": list(map(list, m.kills())),
              "arms": {}}
    for arm, fn in arms.items():
        try:
            o = fn(tree)
        except Refusal as exc:
            o = Outcome(arm, 2, f"refused: {exc}")
        fails = [ln.strip() for ln in o.log.splitlines() if "[FAIL]" in ln]
        tally = [ln.strip() for ln in o.log.splitlines() if ln.strip().startswith("==")]
        result["arms"][arm] = {"rc": o.rc, "fails": fails, "tally": tally}
        print(f"{m.name} {arm}: rc={o.rc} fails={len(fails)}", flush=True)
        for f in fails:
            print(f"    {f}", flush=True)
    out = a.scratch.resolve() / f"{a.name}.json"
    out.write_text(json.dumps(result, indent=1) + "\n")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

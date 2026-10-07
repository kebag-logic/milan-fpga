#!/usr/bin/env python3
"""r530_author_sample.py - a reviewer-chosen sample of the AUTHOR's planted defects
(acmp_mutants.py), each planted with the campaign's plant() and graded with its
caught(): the named test must fail on the named words in every arm it lists.

Usage: PYTHONDONTWRITEBYTECODE=1 python3 r530_author_sample.py <clone> <scratch> [K/N]
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
scratch = Path(sys.argv[2]).resolve()
part = sys.argv[3] if len(sys.argv) > 3 else "1/1"
sys.path.insert(0, str(clone / "sw/firmware/ctrl/test"))

import ctrl_arms  # noqa: E402
import fw_gtest  # noqa: E402
from ctrl_build import Outcome, Refusal, Tree  # noqa: E402
from ctrl_mutants import MUTANTS, caught, plant  # noqa: E402
from ctrl_reuse import cut_reuse  # noqa: E402

SAMPLE = (
    # listener cells
    "acmp-probe-before-response", "acmp-not-authorized-is-13", "acmp-lock-refuses-the-holder",
    "acmp-rebind-same-reprobes", "acmp-guard-reads-the-binding", "acmp-duplicate-takes-a-new-sequence-id",
    "acmp-retry-zeroes-the-status", "acmp-reprobe-ignores-discovery", "acmp-unbind-echoes-the-talker",
    # talker
    "acmp-disconnect-always-succeeds", "acmp-probe-tx-any-interface", "acmp-get-tx-connection-supported",
    # discovery
    "acmp-restart-on-a-smaller-index-only", "acmp-restart-mismatch-keeps-aging", "acmp-departing-interface-unchecked",
    "acmp-valid-time-in-seconds",
    # adapter, ordering, latency
    "acmp-stale-tag-taken", "acmp-tap-takes-discover", "acmp-change-not-held-for-its-response",
    "acmp-response-passes-an-owed-frame", "acmp-bind-reads-the-clock-twice", "acmp-adp-ring-bound-understated",
    # store
    "acmp-record-flags-swapped", "acmp-restore-starts-no-discovery", "acmp-nvm-d3-roll-back-kept",
    "acmp-nvm-refusal-applied",
)


def main() -> int:
    k, n = (int(x) for x in part.split("/"))
    by_name = {m.name: m for m in MUTANTS}
    missing = [s for s in SAMPLE if s not in by_name]
    if missing:
        print(f"[REFUSED] not in the table: {missing}")
        return 2
    size = -(-len(SAMPLE) // n)
    table = [by_name[s] for s in SAMPLE[(k - 1) * size:k * size]]
    arms = {"model": ctrl_arms.arm_model, "port": ctrl_arms.arm_port, "adp": ctrl_arms.arm_adp,
            "unit": ctrl_arms.arm_unit, "walk": ctrl_arms.arm_walk, "acmp": ctrl_arms.arm_acmp,
            "acmpwalk": ctrl_arms.arm_acmpwalk, "acmpnvm": ctrl_arms.arm_acmpnvm}
    root = scratch / f"author-{k}"
    root.mkdir(parents=True, exist_ok=True)
    reuse = root / "reuse"
    cut_reuse(reuse)
    build = fw_gtest.Build()
    escaped = 0
    for m in table:
        tree = Tree(plant(m, root), root / m.name / "build", reuse, build)
        missed = []
        first = ""
        for arm, test, needle in m.kills():
            try:
                out = arms[arm](tree)
            except Refusal as exc:
                out = Outcome(arm, 2, f"refused: {exc}")
            hits = [ln.strip() for ln in out.log.splitlines() if "[FAIL]" in ln and test in ln]
            first = first or (hits[0] if hits else "")
            if not caught(test, needle, out):
                missed.append(f"{arm}:{test} on {needle!r} (rc {out.rc})")
        escaped += 1 if missed else 0
        print(f"[{'CAUGHT' if not missed else 'ESCAPED'}] {m.name}: named {', '.join(t for _, t, _ in m.kills())}"
              f"{'' if not missed else '; missed ' + '; '.join(missed)}")
        if first:
            print(f"    {first[:220]}")
        shutil.rmtree(root / m.name, ignore_errors=True)
    print(f"author sample slice {k}/{n}: {len(table) - escaped} of {len(table)} caught by their named test")
    return 1 if escaped else 0


if __name__ == "__main__":
    sys.exit(main())

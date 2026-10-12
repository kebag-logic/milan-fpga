#!/usr/bin/env python3
"""Run the in-tree pin controls that need no build (the basic clone arms, the
inherited-environment arms of ctrl_pin_env.py and the store/configuration arms
of ctrl_pin_store.py) against the checkout given, the way ctrl_pin.pin_controls
drives them, and print one verdict line per arm plus a tally.

usage: python3 -I pin_arms.py <superproject-root> <work-dir>
The superproject must have third_party/tsn-c-stack initialised at its gitlink.
"""
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
work.mkdir(parents=True, exist_ok=True)

import ctrl_pin  # noqa: E402
from ctrl_build import UNLISTED, stack_gitlink  # noqa: E402
from ctrl_pin_env import inherited_arms  # noqa: E402
from ctrl_pin_store import store_arms  # noqa: E402

pin = stack_gitlink()
clone = ctrl_pin.Clone(work, pin)
edited = f"differs from the pinned {pin[:8]}: "
arms = [("the pinned clone, unmodified", lambda: None, clone.direct, ""),
        ("a core source edited", lambda: clone.append("src/adp.c"), clone.direct, edited + "src/adp.c"),
        ("pinned src/ tree replaced", clone.replaced_tree, clone.direct, edited + "src/adp.c"),
        ("pinned commit replaced", clone.replaced_commit, clone.direct, edited + "src/adp.c"),
        ("graft file", clone.grafted, clone.direct, edited + "src/adp.c"),
        ("clean filter via attributes", clone.filtered, clone.direct, UNLISTED + "filter.pin-control.clean (local)")]
texts = {p.relative_to(ctrl_pin.ROOT).as_posix(): p.read_text(encoding="utf-8") for p in ctrl_pin.PROOF}
arms += inherited_arms(clone.path, pin, work, lambda stack, env: ctrl_pin.proof_run(texts, stack, env))
arms += store_arms(clone.path, pin, work, edited)
bad = 0
for what, spoil, check, needle in arms:
    clone.fresh()
    try:
        spoil()
        accepted, detail = check()
    except Exception as exc:  # a setup refusal is a misbehaving control
        accepted, detail = (bool(needle), f"SETUP FAILED: {type(exc).__name__}: {exc}")
    ok = accepted if not needle else (not accepted and needle in detail)
    print(f"[{'ok' if ok else 'ESCAPED'}] {what}: {detail}", flush=True)
    bad += not ok
print(f"TALLY: {len(arms)} arms, {bad} misbehaved")
sys.exit(1 if bad else 0)

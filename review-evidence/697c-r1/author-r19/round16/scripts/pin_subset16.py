"""Scratch: run a tree's configuration-relevant pin controls as ctrl_pin.pin_controls runs them: the clean clone,
the clean-filter control (ctrl_pin.Clone.filtered), the inherited-environment controls and the object-store and
configuration controls (ctrl_pin_store.store_arms), each after a fresh clone.

usage: pin_subset16.py <tree root> <work dir>
"""
import shutil
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_pin  # noqa: E402
from ctrl_build import UNLISTED  # noqa: E402
from ctrl_pin_env import inherited_arms  # noqa: E402
from ctrl_pin_store import store_arms  # noqa: E402

if work.exists():
    shutil.rmtree(work)
work.mkdir(parents=True)
pin = ctrl_pin.stack_gitlink()
clone = ctrl_pin.Clone(work, pin)
edited = f"differs from the pinned {pin[:8]}: "
texts = {p.relative_to(ctrl_pin.ROOT).as_posix(): p.read_text(encoding="utf-8") for p in ctrl_pin.PROOF}
arms = [("the pinned clone, unmodified", lambda: None, clone.direct, ""),
        ("a source edited, a clean filter given through attributes turning it back into the pinned blob",
         clone.filtered, clone.direct, UNLISTED + "filter.pin-control.clean (local)")]
arms += inherited_arms(clone.path, pin, work, lambda stack, env: ctrl_pin.proof_run(texts, stack, env))
arms += store_arms(clone.path, pin, work, edited)
bad = 0
for what, spoil, check, needle in arms:
    clone.fresh()
    spoil()
    accepted, detail = check()
    ok = accepted if not needle else (not accepted and needle in detail)
    print(f"[{'ok' if ok else 'ESCAPED'}] tsn-c-stack pin control, {what}: {detail}", flush=True)
    bad += not ok
print(f"{bad} of {len(arms)} misbehaved")
sys.exit(1 if bad else 0)

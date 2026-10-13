"""Scratch: run a subset of the pin controls (the inherited-environment arms, chosen hook plants, the clean
proof) as ctrl_pin.pin_controls runs them. usage: pin_subset.py <checkout> <work> [hook|env|all]"""
import sys
from pathlib import Path

root, work, which = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "all"
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(root / "sw/firmware/gtest"))
import ctrl_pin  # noqa: E402
from ctrl_build import stack_gitlink  # noqa: E402

work.mkdir(parents=True, exist_ok=True)
pin = stack_gitlink()
clone = ctrl_pin.Clone(work, pin)
texts = {p.relative_to(ctrl_pin.ROOT).as_posix(): p.read_text(encoding="utf-8") for p in ctrl_pin.PROOF}
arms = []
if which in ("hook", "all"):
    arms.append(("the pin proof as the checkout holds it, under its audit hook", lambda: None, ctrl_pin.unplanted, ""))
    arms += [a for a in ctrl_pin.census_arms() if any(w in a[0] for w in sys.argv[4:])] if len(sys.argv) > 4 \
        else ctrl_pin.census_arms()
if which in ("env", "all"):
    arms += ctrl_pin.inherited_arms(clone.path, pin, work, lambda s, e: ctrl_pin.proof_run(texts, s, e))
bad = 0
for what, spoil, check, needle in arms:
    clone.fresh()
    spoil()
    accepted, detail = check()
    ok = accepted if not needle else (not accepted and needle in detail)
    print(f"[{'ok' if ok else 'ESCAPED'}] {what}: {detail}", flush=True)
    bad += not ok
print(f"controls {len(arms)}, misbehaved {bad}")
sys.exit(1 if bad else 0)

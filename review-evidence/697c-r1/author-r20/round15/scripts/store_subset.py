"""Run a tree's object-store controls (ctrl_pin_store.store_arms) and its inherited-environment controls the way
ctrl_pin.pin_controls runs them, optionally from a stack whose store borrows from another (--reference).

usage: store_subset.py <tree root> <work dir> [--reference]
"""
import shutil
import subprocess
import sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path[:0] = [str(root / "sw/firmware/ctrl/test"), str(root / "sw/firmware/gtest")]
import ctrl_pin  # noqa: E402
from ctrl_pin_env import inherited_arms  # noqa: E402

if work.exists():
    shutil.rmtree(work)
work.mkdir(parents=True)
pin = ctrl_pin.stack_gitlink()
if "--reference" in sys.argv:
    borrowed = work / "borrowing-stack"
    subprocess.run(["git", "clone", "--quiet", "--reference", str(ctrl_pin.STACK), str(ctrl_pin.STACK), str(borrowed)],
                   check=True)
    subprocess.run(["git", "-C", str(borrowed), "-c", "advice.detachedHead=false", "checkout", "--quiet", pin],
                   check=True)
    print("source stack's alternates:", (borrowed / ".git/objects/info/alternates").read_text().strip())
    ctrl_pin.STACK = borrowed
clone = ctrl_pin.Clone(work, pin)
edited = f"differs from the pinned {pin[:8]}: "
texts = {p.relative_to(ctrl_pin.ROOT).as_posix(): p.read_text(encoding="utf-8") for p in ctrl_pin.PROOF}
arms = inherited_arms(clone.path, pin, work, lambda stack, env: ctrl_pin.proof_run(texts, stack, env))
try:
    from ctrl_pin_store import store_arms  # noqa: E402
    arms += store_arms(clone.path, pin, work, edited)
except ImportError:
    print("this tree has no ctrl_pin_store.py")
bad = 0
for what, spoil, check, needle in arms:
    clone.fresh()
    if what.startswith("the inherited environment, GIT_ALTERNATE"):
        print("clone's alternates file before the control:", (clone.path / ".git/objects/info/alternates").exists())
    spoil()
    accepted, detail = check()
    ok = accepted if not needle else (not accepted and needle in detail)
    print(f"[{'ok' if ok else 'ESCAPED'}] tsn-c-stack pin control, {what}: {detail}", flush=True)
    bad += not ok
print(f"{bad} of {len(arms)} misbehaved")

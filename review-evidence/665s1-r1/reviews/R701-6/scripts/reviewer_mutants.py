#!/usr/bin/env python3
"""Reviewer mutants on the round-6 delta: each plants one defect in a disposable copy
of sw/firmware/ctrl and requires the named test to fail (app arm, two interfaces).
Usage: reviewer_mutants.py CHECKOUT SCRATCH"""
import json, re, shutil, sys
from pathlib import Path
checkout, root = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(checkout / "sw/firmware/ctrl/test"))
import aecp_arms, ctrl_build, fw_gtest  # noqa: E402
T_EXP = "Core.AnExpiredLockHoldsByItsOwnerUntilThePlatformAppliedItsRelease"
T_SID = "Core.ASystemIdChangeWhileOneWaitsIsRefusedAsEveryChangeIs"
M = [
 ("rx-refusal-old-owner-form", "aecp/aecp.c",
  "if (status == AECP_ENTITY_LOCKED && a->refusing && !aecp_other_lock(a)) {",
  "if (status == AECP_ENTITY_LOCKED && a->refusing && (!a->locked || a->lock_owner == a->requester)) {", [T_EXP]),
 ("available-owner-zero-while-unlocked", "aecp/aecp_commands.c",
  "wire_put_be(out + 12, a->lock_owner, 8);", "wire_put_be(out + 12, a->locked ? a->lock_owner : 0u, 8);", [T_EXP]),
 ("acmp-owner-zero-while-unlocked", "aecp/aecp.c",
  "*owner = a->lock_owner;", "*owner = a->locked ? a->lock_owner : 0u;", [T_EXP]),
 ("lock-refusal-locked-id-zero-while-unlocked", "aecp/aecp_commands.c",
  "wire_put_be(out + 4, a->lock_owner, 8);", "wire_put_be(out + 4, a->locked ? a->lock_owner : 0u, 8);", [T_EXP]),
 ("mvu-refusal-only-while-waiting", "aecp/aecp.c",
  "if (set && a->refusing) {", "if (set && a->waiting) {", [T_SID]),
 ("mvu-ignores-other-lock", "aecp/aecp.c",
  "if (cmd == 2u || (set && !aecp_other_lock(a))) {", "if (cmd == 2u || set) {", [T_SID]),
 ("mvu-refusal-before-other-lock", "aecp/aecp.c",
  "if (cmd == 2u || (set && !aecp_other_lock(a))) {",
  "if (cmd == 2u || (set && (a->refusing || !aecp_other_lock(a)))) {", [T_SID]),
 ("owner-changes-while-unlocked", "aecp/aecp_commands.c",
  "return a->refusing || aecp_other_lock(a);", "return (a->refusing && !a->unlocked) || aecp_other_lock(a);", [T_EXP]),
]
src = root / "ctrl"
shutil.copytree(checkout / "sw/firmware/ctrl", src, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
shutil.copytree(checkout / "sw/firmware/ctrl_nvm", src.parent / "ctrl_nvm",
                ignore=shutil.ignore_patterns("test", "__pycache__", "*.pyc"))
tree = ctrl_build.Tree(src, root / "build", root / "reuse", fw_gtest.Build(jobs=4), ctrl_build.STACK)
cfg = checkout / "configs/endstation_ax7101_1x1_tdm8.yaml"
out, escaped = [], 0
for name, path, old, new, tests in M:
    target = src / path
    original = target.read_text()
    assert original.count(old) == 1, (name, original.count(old))
    target.write_text(original.replace(old, new))
    try:
        r = aecp_arms.core_arm(tree, cfg, 2, "app", ":".join(tests))
        failed = [t for t in tests if re.search(r"\[  FAILED  \] " + re.escape(t) + r" \(", r.log)]
        caught = r.rc == 1 and failed == tests
        (root / f"{name}.log").write_text(r.log)
    except ctrl_build.Refusal as e:
        caught = False
        (root / f"{name}.log").write_text(str(e))
    finally:
        target.write_text(original)
    escaped += not caught
    out.append({"name": name, "path": path, "old": old, "new": new, "tests": tests, "caught": caught})
    print(f"[{'CAUGHT' if caught else 'ESCAPED'}] {name}", flush=True)
(root / "results.json").write_text(json.dumps(out, indent=2) + "\n")
print(f"escaped {escaped} of {len(M)}")
raise SystemExit(1 if escaped else 0)

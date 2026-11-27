#!/usr/bin/env python3
"""Reviewer mutation probe: plant one text substitution in a disposable tree copy, run the port loop suite and the SRP
mailbox suite at 1x1/1if and 8x8/1if, report each arm's verdict, and restore the file byte for byte.

usage: run_mutant.py <probe-tree> <pinned lwSRP checkout> <out dir> <file relative to sw/firmware/ctrl> <old> <new>
"""
import sys
from pathlib import Path

tree_root, lwsrp, out, rel, old, new = (Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), sys.argv[4],
                                         sys.argv[5], sys.argv[6])
sys.path.insert(0, str(tree_root / "sw/firmware/ctrl/test"))
sys.path.insert(0, str(tree_root / "sw/firmware/gtest"))
import fw_gtest  # noqa: E402
from ctrl_build import Tree  # noqa: E402
import ctrl_arms  # noqa: E402
import srp_arms  # noqa: E402

target = tree_root / "sw/firmware/ctrl" / rel
original = target.read_bytes()
text = original.decode()
if text.count(old) != 1:
    sys.exit(f"the anchor occurs {text.count(old)} times in {rel}")
target.write_text(text.replace(old, new), encoding="utf-8")
try:
    out.mkdir(parents=True, exist_ok=True)
    tree = Tree(src=tree_root / "sw/firmware/ctrl", out=out, reuse=out / "reuse", build=fw_gtest.Build(jobs=4))
    results = [ctrl_arms.arm_port(tree)]
    for cfg in ("configs/endstation_ax7101_1x1_tdm8.yaml", "configs/endstation_ax7101_8x8.yaml"):
        results.append(srp_arms.arm_srp(tree, lwsrp, 1, test=("srp_mbx.cpp", "-Srp.ReviewProbe*"),
                                        config=tree_root / cfg))
finally:
    target.write_bytes(original)
for r in results:
    fails = [ln for ln in r.log.splitlines() if "[FAIL]" in ln or "checks:" in ln]
    print(f"ARM {r.arm} rc={r.rc}")
    for ln in fails[:8]:
        print("   ", ln)
print("CAUGHT" if any(r.rc for r in results) else "ESCAPED")

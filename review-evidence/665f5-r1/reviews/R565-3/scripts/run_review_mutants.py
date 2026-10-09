#!/usr/bin/env python3
"""Reviewer-planted AECP defects in a disposable copy; record every failing test.

Usage: run_review_mutants.py <exact-head-tree> <packet>
Each plant edits one exact site in a copy of sw/firmware/ctrl, runs the complete
composed AECP suite (app arm, two interfaces, all tests) and restores the copy.
"""
import json, re, shutil, sys
from pathlib import Path
root, packet = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(root / "sw/firmware/ctrl/test"))
import aecp_arms, fw_gtest  # noqa: E401,E402
from ctrl_build import Tree, CTRL, Refusal  # noqa: E402
PLANTS = [
    ("nosub-applies-request-latency", "aecp/aecp_commands.c",
     "\t\tif ((requested & 0x20000000u) == 0u) {\n",
     "\t\tif ((requested & 0x20000000u) == 0u) {\n\t\t\ta->cfg.latency[index] = (uint32_t)wire_be32(in + 24); aecp_override(a, d, 2u);\n"),
    ("nosub-reports-request-latency", "aecp/aecp_commands.c",
     "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n",
     "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4); memcpy(out + 24, in + 24, 4u);\n"),
    ("saved-state-refused", "aecp/aecp_commands.c",
     "(requested & 0xdaf80000u) != 0u", "(requested & 0xdaf80004u) != 0u"),
    ("unavailable-event-dropped", "aecp/aecp.c",
     "\t\t\te->retry_pending |= (uint8_t)(1u << bit);\n",
     "\t\t\te->pending &= (uint8_t)~(1u << bit);\n"),
    ("init-guard-after-memset", "aecp/aecp.c",
     "\tif (!aecp_enter(NULL)) return false;\n\tmemset(a, 0, sizeof *a);\n",
     "\tmemset(a, 0, sizeof *a);\n\tif (!aecp_enter(NULL)) return false;\n"),
]
out = packet / "scratch" / "review-mutants"
src = out / "work/ctrl"
shutil.copytree(CTRL, src, dirs_exist_ok=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
tree = Tree(src, out / "work/build", out / "work/reuse", fw_gtest.Build(jobs=4))
config = root / "configs/endstation_ax7101_1x1_tdm8.yaml"
results = []
for name, path, old, new in PLANTS:
    target = src / path
    original = target.read_text()
    assert original.count(old) == 1, (name, original.count(old))
    target.write_text(original.replace(old, new))
    try:
        result = aecp_arms.core_arm(tree, config, 2, "app", "*")
        failed = sorted(set(re.findall(r"\[  FAILED  \] (\S+) \(", result.log)))
        rc, log = result.rc, result.log
    except Refusal as error:
        failed, rc, log = ["BUILD-REFUSED"], 2, str(error)
    finally:
        target.write_text(original)
    (out / (name + ".log")).write_text(log)
    results.append({"plant": name, "rc": rc, "failing_tests": failed})
    print(name, "rc", rc, "failing:", failed, flush=True)
(out / "results.json").write_text(json.dumps(results, indent=2) + "\n")

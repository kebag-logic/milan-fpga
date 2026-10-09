#!/usr/bin/env python3
"""R564-4 reviewer probe: run the AECP application arm on a disposable copy,
optionally with one planted core defect, and grade named-test diagnostics.

Usage: r564_4_plant.py --repo CLONE --out DIR --interfaces {1,2} [--plant NAME] [--jobs N]
The clone is never written; the plant is applied to DIR/ctrl only.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

# name -> (file, old, new, [(test, diagnostic words), ...])
PLANTS = {
    # Exact text of the round-3 reviewer plants as carried by the mutation table.
    "X8-nosub-bypasses-running-only": (
        "aecp/aecp_commands.c",
        "\t\tif (info.running) {\n",
        "\t\tif ((wire_be32(in + 4) & 0xfaf80000u) == 0u && !aecp_foreign_lock(a)) {\n"
        "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n"
        "\t\t\treturn AECP_SUCCESS;\n"
        "\t\t}\n"
        "\t\tif (info.running) {\n",
        [("Core.S1_NoSubcommandSetOnRunningOutputIsRefused", "STREAM_IS_RUNNING for a no-sub-command SET")]),
    "X9-nosub-bypasses-input-refusal": (
        "aecp/aecp_commands.c",
        "\t\tif (type == 5u) {\n\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n",
        "\t\tif (type == 5u && (wire_be32(in + 4) & 0xfaf80000u) != 0u) {\n"
        "\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n",
        [("Core.S2_NoSubcommandSetOnInputIsNotSupported",
          "NOT_SUPPORTED for a no-sub-command SET to a STREAM_INPUT")]),
    # Reviewer-own variants: narrow the bypass to one ignored-flag value, so a
    # test iterating only some flag values would let it escape.
    "V1-running-bypass-streaming-wait-only": (
        "aecp/aecp_commands.c",
        "\t\tif (info.running) {\n",
        "\t\tif ((uint32_t)wire_be32(in + 4) == 8u) {\n"
        "\t\t\twire_put_be(out + 4, flags & ~0x20000000u, 4);\n"
        "\t\t\treturn AECP_SUCCESS;\n"
        "\t\t}\n"
        "\t\tif (info.running) {\n",
        [("Core.S1_NoSubcommandSetOnRunningOutputIsRefused", "STREAM_IS_RUNNING for a no-sub-command SET")]),
    "V2-input-bypass-flags12-only": (
        "aecp/aecp_commands.c",
        "\t\tif (type == 5u) {\n\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n",
        "\t\tif (type == 5u && (uint32_t)wire_be32(in + 4) != 12u) {\n"
        "\t\t\treturn AECP_NOT_SUPPORTED;\n\t\t}\n",
        [("Core.S2_NoSubcommandSetOnInputIsNotSupported",
          "NOT_SUPPORTED for a no-sub-command SET to a STREAM_INPUT")]),
    # Reviewer-own: the running refusal keeps its status but leaks the request.
    "V3-running-refusal-stores-latency": (
        "aecp/aecp_commands.c",
        "\t\tif (info.running) {\n",
        "\t\tif (info.running && ((uint32_t)wire_be32(in + 4) & 0x20000000u) == 0u) {\n"
        "\t\t\ta->cfg.latency[index] = (uint32_t)wire_be32(in + 24);\n"
        "\t\t}\n"
        "\t\tif (info.running) {\n",
        [("Core.S1_NoSubcommandSetOnRunningOutputIsRefused", "refusal preserves stored latency")]),
    "V4-running-refusal-echoes-latency": (
        "aecp/aecp_commands.c",
        "\t\tif (info.running) {\n",
        "\t\tif (info.running && ((uint32_t)wire_be32(in + 4) & 0x20000000u) == 0u) {\n"
        "\t\t\tmemcpy(out + 24, in + 24, 4u);\n"
        "\t\t}\n"
        "\t\tif (info.running) {\n",
        [("Core.S1_NoSubcommandSetOnRunningOutputIsRefused", "refusal reports current latency")]),
}


def failure_block(log: str, test: str) -> str | None:
    m = re.search(r"\[ RUN      \] " + re.escape(test) + r"\n(.*?)\[  FAILED  \] " +
                  re.escape(test) + r" \(", log, re.S)
    return None if m is None else m[1]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--interfaces", type=int, choices=(1, 2), required=True)
    ap.add_argument("--plant", choices=sorted(PLANTS))
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--filter", default="*")
    a = ap.parse_args()
    repo = a.repo.resolve()
    out = a.out.resolve()
    out.mkdir(parents=True, exist_ok=True)
    test_dir = repo / "sw/firmware/ctrl/test"
    sys.path.insert(0, str(test_dir))
    import aecp_arms
    import fw_gtest
    from ctrl_build import Tree, Refusal
    src = out / "ctrl"
    shutil.copytree(repo / "sw/firmware/ctrl", src, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    receipt = {"plant": a.plant, "interfaces": a.interfaces, "filter": a.filter}
    if a.plant:
        path, old, new, checks = PLANTS[a.plant]
        target = src / path
        text = target.read_text()
        if text.count(old) != 1:
            raise SystemExit(f"plant site count {text.count(old)} for {a.plant}")
        target.write_text(text.replace(old, new))
        receipt["site"] = path
    else:
        checks = []
    tree = Tree(src, out / "build", out / "reuse", fw_gtest.Build(jobs=a.jobs))
    config = repo / "configs/endstation_ax7101_1x1_tdm8.yaml"
    try:
        result = aecp_arms.core_arm(tree, config, a.interfaces, "app", a.filter)
        receipt["compiled"] = True
        receipt["rc"] = result.rc
        log = result.log
    except Refusal as error:
        receipt["compiled"] = False
        receipt["rc"] = 2
        log = "REFUSED (compile/link): " + str(error)
    (out / "run.log").write_text(log)
    receipt["failed_tests"] = sorted(set(re.findall(r"^\[  FAILED  \] (\S+) \(", log, re.M)))
    receipt["passed_line"] = next(iter(re.findall(r"^\[  PASSED  \] .*$", log, re.M)), None)
    receipt["verdict_line"] = next(iter(re.findall(r"verdict: .*$", log, re.M)), None)
    receipt["checks"] = []
    for test, words in checks:
        block = failure_block(log, test)
        receipt["checks"].append({"test": test, "words": words, "test_failed": block is not None,
                                  "diagnostic_present": block is not None and words in block})
    receipt["killed"] = bool(checks) and receipt["compiled"] and receipt["rc"] == 1 and \
        all(c["diagnostic_present"] for c in receipt["checks"])
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    if a.plant:
        return 0 if receipt["killed"] else 1
    return result.rc if receipt["compiled"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

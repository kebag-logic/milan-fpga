#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check a gate 1b compiler audit (R227-2, issue #504 / PR #521).

compiled mode: every selector invocation is mapped at argv[0] only, the
argument tail and the recorded return code are preserved, every census
assembly declares the same rv32 arch, and no host/alternate compiler
compiled firmware. absent mode: every cross candidate is hidden and no
firmware compile happened.

Usage: audit_check.py compiled|absent <audit.jsonl> [<sdk-prefix>]
"""

import collections
import json
import sys
from pathlib import Path


def main() -> int:
    mode, path = sys.argv[1], Path(sys.argv[2])
    records = [json.loads(line) for line in path.read_text().splitlines()]
    selector_suffix = "/br-milan-rv32/host/bin/riscv32-linux-gcc"
    tally = collections.Counter()
    arches = collections.Counter()
    problems = []
    for record in records:
        requested, actual = record["requested_argv"], record.get("actual_argv")
        head = requested[0]
        if head.endswith(selector_suffix):
            tally["selector"] += 1
            if mode == "compiled":
                sdk = sys.argv[3] + "/bin/riscv32-linux-gcc"
                if actual is None or actual[0] != sdk or actual[1:] != requested[1:]:
                    problems.append(f"mapping not argv[0]-only: {record}")
                if "-std=gnu99" in requested:
                    tally["firmware-compiles"] += 1
                    if "assembly_arch" in record:
                        arches[record["assembly_arch"]] += 1
            else:
                if actual is not None or record.get("result") != "deliberately absent":
                    problems.append(f"selector not hidden: {record}")
        elif head in ("riscv64-elf-gcc", "riscv32-unknown-elf-gcc"):
            tally["alternate"] += 1
            if mode == "absent" and record.get("result") != "deliberately absent":
                problems.append(f"alternate not hidden: {record}")
            if mode == "compiled" and "-std=gnu99" in requested:
                problems.append(f"alternate compiled firmware: {record}")
        else:
            tally["host"] += 1
            if "-std=gnu99" in requested:
                problems.append(f"host compiled firmware: {record}")
    if mode == "compiled":
        if tally["firmware-compiles"] == 0:
            problems.append("no firmware compile recorded")
        if len(arches) != 1 or not next(iter(arches)).startswith("rv32"):
            problems.append(f"census arch not one rv32 value: {dict(arches)}")
    else:
        if tally["firmware-compiles"]:
            problems.append("absent mode compiled firmware")
    print(json.dumps({"mode": mode, "records": len(records), "tally": tally,
                      "assembly_arch": arches, "problems": len(problems)},
                     sort_keys=True))
    for problem in problems[:20]:
        print("PROBLEM " + problem[:300])
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

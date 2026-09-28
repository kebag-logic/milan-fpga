#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Reviewer probe (R377-2): copy a processor tree and add the reviewer's
directed probe include(s) to tb/acmp_talker/sim_main.cpp in the COPY.
Usage: apply_probe.py SRC_TREE DST_TREE HPP [HPP ...]
Each HPP must define struct <Name> { int& checks; int& fails; void run_all(); };
the struct name is read from the file."""

import re
import shutil
import sys
from pathlib import Path


def main() -> int:
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    hpps = [Path(p) for p in sys.argv[3:]]
    if dst.exists():
        shutil.rmtree(dst)
    for sub in ("hdl", "tb/acmp_talker", "tb/common"):
        shutil.copytree(src / sub, dst / sub,
                        ignore=shutil.ignore_patterns("obj_dir", "__pycache__"))
    cpp = dst / "tb/acmp_talker/sim_main.cpp"
    text = cpp.read_text()
    anchor_inc = '#include "retry_cases.hpp"\n'
    anchor_run = "  check_retry_cases();\n  return report();\n"
    if text.count(anchor_inc) != 1 or text.count(anchor_run) != 1:
        raise SystemExit("probe anchors not unique")
    incs, calls = "", ""
    for hpp in hpps:
        shutil.copy(hpp, dst / "tb/acmp_talker" / hpp.name)
        body = hpp.read_text()
        incs += f'#include "{hpp.name}"\n'
        if "void run_all()" not in body:
            continue                      # helper include only
        name = re.search(r"^struct (\w+) \{", body, re.M).group(1)
        calls += f"  {{ {name} probe{{checks, fails}}; probe.run_all(); }}\n"
    text = text.replace(anchor_inc, anchor_inc + incs)
    text = text.replace(anchor_run, "  check_retry_cases();\n" + calls + "  return report();\n")
    cpp.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

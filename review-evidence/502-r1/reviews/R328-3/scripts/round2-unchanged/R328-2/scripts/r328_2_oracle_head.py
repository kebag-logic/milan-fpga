#!/usr/bin/env python3
"""R328-2 re-anchored run of the unchanged round-1 oracle_probe.py on the head harness.

Usage: r328_2_oracle_head.py <oracle_probe.py> <repo-root> <scratch>

Loads oracle_probe.py unchanged (hash printed). Two of its four anchors moved:
  * pending_post_edge's early return now tests `pending.watching`; the oracle
    call is inserted before it and gated on the same `watching` flag, so the
    control-face preloads that precede the first command form the baseline
    (they are outside #502 and raise no pending by design);
  * the "K12 zero records" report lost one indentation level; the inserted
    refused-record block is kept byte for byte.
The other two anchors and every inserted body are unchanged.
"""
import hashlib
import runpy
import sys
from pathlib import Path

OLD_POST = ("    void pending_post_edge() {\n"
            "        if (!pending.armed || !pending.unsaved || !dut->axis_resetn) return;")
HEAD_POST = ("    void pending_post_edge() {\n"
             "        if (!pending.armed || !pending.watching || !dut->axis_resetn) return;")
NEW_POST = ("    void pending_post_edge() {\n"
            "        if (pending.armed && pending.watching && dut->axis_resetn) oracle_edge();\n"
            "        if (!pending.armed || !pending.watching || !dut->axis_resetn) return;")
OLD_ZERO = '            pending_report("K12 zero records", 0, 0, 0);\n'
HEAD_ZERO = '        pending_report("K12 zero records", 0, 0, 0);\n'


def main():
    script = Path(sys.argv[1]).resolve()
    print(f"script {script.name} sha256 {hashlib.sha256(script.read_bytes()).hexdigest()}")
    ns = runpy.run_path(str(script))
    patches = ns["PATCHES"]
    for i, (old, new) in enumerate(patches):
        if old == OLD_POST:
            patches[i] = (HEAD_POST, NEW_POST)
            print("rebound: pending_post_edge anchor (oracle gated on watching)")
        elif old == OLD_ZERO:
            assert new.startswith(OLD_ZERO)
            patches[i] = (HEAD_ZERO, HEAD_ZERO + new[len(OLD_ZERO):])
            print("rebound: K12 zero records anchor (body unchanged)")
    sys.argv = [str(script)] + sys.argv[2:] + ["shipping"]
    ns["main"]()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""make_arm_patches.py <tree>: write tb/srp_top/mutations/<arm>.patch for the round's new arms, each one exact text
replacement in hdl/srp/KL_srp_encoder.sv, as a three-line-context unified diff. Refuses an edit that does not match
exactly once."""
import difflib
import sys
from pathlib import Path

ENC = "hdl/srp/KL_srp_encoder.sv"
ARMS = {
    "push-on-prepared-start": (
        "                     ? (start0_w || ((st_r == E_COLLECT) && go0_w)\n",
        "                     ? (start0_w\n"),
    "push-taken-in-alloc": (
        "assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT)\n",
        "assign busy_app_w  = (st_r != E_IDLE) && (st_r != E_COLLECT) && (st_r != E_ALLOC)\n"),
}


def main() -> int:
    tree = Path(sys.argv[1])
    src = (tree / ENC).read_text()
    for arm, (old, new) in ARMS.items():
        assert src.count(old) == 1, (arm, src.count(old))
        lines = difflib.unified_diff(src.splitlines(keepends=True),
                                     src.replace(old, new).splitlines(keepends=True),
                                     fromfile="a/" + ENC, tofile="b/" + ENC, n=3)
        (tree / "tb/srp_top/mutations" / (arm + ".patch")).write_text("".join(lines))
        print(arm)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

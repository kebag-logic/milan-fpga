#!/usr/bin/env python3
"""Write the reviewer's disposable probe patches against hdl/maap/KL_pp_maap.sv.

Usage: make_probe_patches.py <processor checkout at the exact head> <output dir>
Each probe is one exact text replacement; the script refuses a probe whose
anchor is not found exactly once.
"""
import difflib
import sys
from pathlib import Path

REL = "hdl/maap/KL_pp_maap.sv"
PROBES = {
    # W_POST no longer sees a live fall itself; only the TX-state latch runs it
    "post-ignores-live-fall": (
        "          if (!eng_w || rel_pend_r) begin\n",
        "          if (rel_pend_r) begin\n",
    ),
    # the TX-state latch no longer withdraws the claim at the fall
    "latch-keeps-claim": (
        "        pstate_r   <= P_INITIAL;\n        rel_pend_r <= 1'b1;\n",
        "        rel_pend_r <= 1'b1;\n",
    ),
    # the TX-state latch withdraws the claim but does not remember the Release!
    "latch-forgets-release": (
        "        pstate_r   <= P_INITIAL;\n        rel_pend_r <= 1'b1;\n",
        "        pstate_r   <= P_INITIAL;\n",
    ),
}


def main() -> int:
    root, out = Path(sys.argv[1]), Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    text = (root / REL).read_text()
    for name, (old, new) in PROBES.items():
        if text.count(old) != 1:
            print(f"{name}: anchor found {text.count(old)} times, refused")
            return 1
        mutated = text.replace(old, new)
        diff = difflib.unified_diff(text.splitlines(keepends=True),
                                    mutated.splitlines(keepends=True),
                                    fromfile="a/" + REL, tofile="b/" + REL)
        (out / f"{name}.patch").write_text("".join(diff))
        print(f"{name}: written")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

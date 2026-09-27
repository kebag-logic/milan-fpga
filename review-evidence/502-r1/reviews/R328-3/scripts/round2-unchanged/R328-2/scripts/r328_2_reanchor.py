#!/usr/bin/env python3
"""R328-2 re-anchoring runner for an unchanged round-1 mutant script.

Usage: r328_2_reanchor.py <mutant-script> <repo-root> <scratch> [mutant ...]

Loads the round-1 script unchanged (byte hash printed), and for every mutant
whose anchor is the round-1 map/name trigger text `LIVE`, rebinds ONLY the
anchor to the head's trigger text. Every replacement body is kept byte for
byte. The head anchor must occur exactly once in the shipping shadow and the
old anchor must be absent; otherwise the runner refuses. Then the script's own
main() runs with its own build, verdict and hash-guard logic.
"""
import hashlib
import runpy
import sys
from pathlib import Path

HEAD_LIVE = ("  assign aecp_live_wr_w = aecp_name_wr_w\n"
             "                        | amap_live_wr_i;")


def main():
    script = Path(sys.argv[1]).resolve()
    root = Path(sys.argv[2]).resolve()
    print(f"script {script.name} sha256 {hashlib.sha256(script.read_bytes()).hexdigest()}")
    shadow = (root / "hdl/milan/KL_pp_shadow.sv").read_text()
    ns = runpy.run_path(str(script))
    old = ns["LIVE"]
    if shadow.count(old) != 0 or shadow.count(HEAD_LIVE) != 1:
        sys.exit(f"REFUSED: old anchor {shadow.count(old)}, head anchor {shadow.count(HEAD_LIVE)}")
    rebound = []
    for name, spec in ns["MUTANTS"].items():
        if spec is None:
            continue
        anchor, body = spec
        if anchor == old:
            ns["MUTANTS"][name] = (HEAD_LIVE, body)  # same dict object main() reads
            rebound.append(name)
    print("rebound anchors only: " + " ".join(rebound))
    sys.argv = [str(script)] + sys.argv[2:]
    ns["main"]()


if __name__ == "__main__":
    main()

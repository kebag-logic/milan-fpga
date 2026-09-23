#!/usr/bin/env python3
"""Write a compact, publishable digest of each harness run log.

usage: digest.py OUTDIR LOG...
Each OUTDIR/<log name>.digest.txt keeps: the full log's sha256 and line count, the
header (leg, datapath/harness/crf_rx sha256, build status), every [FAIL] line, every
[CTRS-CRF], [NOTIFY-CRF] and [PROBE] line, the "CRF row pushes" info line, the
harness tally and the run status. Full logs stay with the reviewer.
"""
import hashlib
import os
import sys

KEEP = ("[FAIL]", "[CTRS-CRF]", "[NOTIFY-CRF]", "[PROBE]", "CRF row pushes",
        "checks:", "RESULT:")
HEAD = ("leg=", "datapath_sha256=", "harness_sha256=", "crf_rx_sha256=", "build_exit=",
        "run_exit=")


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for log in sys.argv[2:]:
        raw = open(log, "rb").read()
        lines = raw.decode(errors="replace").splitlines()
        keep = [f"full_log={os.path.basename(log)}",
                f"full_log_sha256={hashlib.sha256(raw).hexdigest()}",
                f"full_log_lines={len(lines)}"]
        for n, ln in enumerate(lines, 1):
            s = ln.strip()
            if s.startswith(HEAD) or any(k in ln for k in KEEP):
                keep.append(f"{n}: {ln.rstrip()}")
        with open(os.path.join(out, os.path.basename(log) + ".digest.txt"), "w") as f:
            f.write("\n".join(keep) + "\n")


if __name__ == "__main__":
    main()

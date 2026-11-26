#!/usr/bin/env python3
"""Copy probe logs into receipts/ with host paths replaced by placeholders.

Usage: python3 -I publish_receipts.py <packet-dir>
"""
import re
import sys
from pathlib import Path

PKT = Path(sys.argv[1])
SCRATCH = PKT / "scratch"
OUT = PKT / "receipts"
PROBES = ["p0_instr", "p1_stale_bank", "p2_unsent", "p3_oldgen",
          "p4_stale_on_negative", "p5_wrong_sign", "p6_used_as_zero"]


def scrub(text: str) -> str:
    text = text.replace(str(SCRATCH / "probes3"), "<PROBES>")
    text = text.replace(str(PKT), "<PACKET>")
    text = re.sub(r"/home/[^/\s]+/\S*", "<TOOLROOT>", text)
    text = re.sub(r"/srv/\S*", "<HOSTPATH>", text)
    text = re.sub(r"/data/\S*", "<TOOLPATH>", text)
    return text


def main() -> int:
    OUT.mkdir(exist_ok=True)
    summary = []
    for p in PROBES:
        log = (SCRATCH / f"{p}.v3.log").read_text(errors="replace")
        rc = (SCRATCH / f"{p}.v3.rc").read_text().strip()
        (OUT / f"probe_{p}.log").write_text(scrub(log) + f"\n# make run exit status: {rc}\n")
        tally = [l for l in log.splitlines() if re.match(r"^\d+ checks:", l)]
        named = [l for l in log.splitlines() if l.startswith(("FAIL #109", "PROBE #109"))]
        summary.append(f"== {p} rc={rc} {tally[0] if tally else 'NO TALLY'}")
        summary.extend("   " + l[:150] for l in named)
    (OUT / "probe_summary.txt").write_text("\n".join(summary) + "\n")
    print("\n".join(summary[:3]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

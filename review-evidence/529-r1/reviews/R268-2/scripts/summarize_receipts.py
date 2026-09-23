#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Tabulate every mutant receipt of this round.

usage: summarize_receipts.py <packet root>
Reads receipts/{mutants,prior_mutants,extra_mutants}/*.txt and writes
receipts/MUTATION-SUMMARY.tsv plus a per-campaign verdict count on stdout.
"""
import collections
import pathlib
import re
import sys


def field(txt: str, key: str) -> str:
    m = re.search(rf"(?:^|\s){key}=(\S*)", txt, re.M)
    return m.group(1) if m else ""


def main() -> int:
    root = pathlib.Path(sys.argv[1])
    rows, tally = [], collections.Counter()
    for sub in ("mutants", "prior_mutants", "extra_mutants"):
        for r in sorted((root / "receipts" / sub).glob("*.txt")):
            t = r.read_text()
            camp, mid = r.stem.split("__", 1)
            v = field(t, "verdict")
            rows.append("\t".join([sub, camp, field(t, "leg"), mid, field(t, "mutant_sha256")[:12],
                                   field(t, "harness_sha256")[:12], field(t, "build_exit"),
                                   field(t, "checks"), field(t, "failures"), v]))
            tally[(sub, camp, v)] += 1
    hdr = "set\tcampaign\tleg\tmutant\tmutant_sha256\tharness_sha256\tbuild_exit\tchecks\tfailures\tverdict"
    (root / "receipts" / "MUTATION-SUMMARY.tsv").write_text(hdr + "\n" + "\n".join(rows) + "\n")
    for (sub, camp, v), n in sorted(tally.items()):
        print(f"{sub}\t{camp}\t{v}\t{n}")
    print(f"TOTAL receipts: {len(rows)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

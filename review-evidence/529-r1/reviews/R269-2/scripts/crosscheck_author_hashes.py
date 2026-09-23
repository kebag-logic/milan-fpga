#!/usr/bin/env python3
"""Compare this round's pairwise-exchange mutants with the author's published set.

usage: crosscheck_author_hashes.py AUTHOR_MUTATION_RESULTS_MD MUTDIR
The author's table names each exchange `nxn8_pw_<a>_<b>` and records the first eight
hex digits of the mutated datapath's sha256. This round's mutants are named
`vx-<port a>-<port b>` (port order as in the KL_crf_rx instance). Prints one line per
exchange and the totals.
"""
import hashlib
import os
import re
import sys

SHORT = {"pdu_count": "pdu", "fmt_err": "fmt", "seq_err": "seq", "mr_cnt": "mr",
         "tu_cnt": "tu", "late_cnt": "late", "early_cnt": "early", "cnt_locked": "lock",
         "cnt_unlocked": "unlock", "cnt_intr": "intr"}


def main():
    table, mutdir = sys.argv[1:3]
    author = {}
    for ln in open(table):
        m = re.match(r"\| nxn8_pw_(\w+?) \| nxn8 \| \w+ \| (\w{8}) \|.*\| (RED|green) \|", ln)
        if m:
            author[m.group(1)] = (m.group(2), m.group(3))
    same = diff = 0
    for mid in sorted(os.listdir(mutdir)):
        if not mid.startswith("vx-"):
            continue
        rest = mid[3:]
        key = None
        for a in SHORT:
            if rest.startswith(a + "-") and rest[len(a) + 1:] in SHORT:
                key = f"{SHORT[a]}_{SHORT[rest[len(a) + 1:]]}"
        h = hashlib.sha256(open(os.path.join(mutdir, mid, "milan_datapath.sv"), "rb").read()).hexdigest()[:8]
        ah, verdict = author.get(key, ("-", "-"))
        ok = ah == h
        same += ok
        diff += not ok
        print(f"{mid}\tauthor:{key}\tours:{h}\tauthor:{ah}\tauthor_nxn8:{verdict}\t{'SAME' if ok else 'DIFFERENT'}")
    print(f"byte-identical (8-hex prefix): {same}; different or absent: {diff}")


if __name__ == "__main__":
    main()

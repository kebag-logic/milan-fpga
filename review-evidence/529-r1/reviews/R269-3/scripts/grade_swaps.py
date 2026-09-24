#!/usr/bin/env python3
"""R269-3: for each binding exchange, require BOTH exchanged quadlets red in the
event arm ("[CTRS-CRF] events, all ten: @<4q> <SYM>").

usage: grade_swaps.py <SWAPS.tsv> <logs dir> <leg>
Prints one line per exchange and a final tally; exit 1 if any exchange fails
to turn both of its quadlets red.
"""
import pathlib
import sys


def main():
    tsv, logs, leg = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]
    rows = [l.split("\t") for l in tsv.read_text().splitlines()[1:]]
    both = 0
    for name, _wa, qa, sa, _wb, qb, sb in rows:
        log = (logs / f"{name}__{leg}.run.log").read_text()
        red = []
        for q, s in ((qa, sa), (qb, sb)):
            tag = f"[CTRS-CRF] events, all ten: @{int(q) * 4} {s}"
            hit = [l for l in log.splitlines() if tag in l]
            red.append(len(hit) == 1 and "[FAIL]" in hit[0])
        fails = sum(1 for l in log.splitlines() if "[FAIL]" in l)
        ok = all(red)
        both += ok
        print(f"{name}\t@{int(qa)*4} {'RED' if red[0] else 'green'}\t"
              f"@{int(qb)*4} {'RED' if red[1] else 'green'}\t{fails} FAIL lines")
    print(f"TOTAL {both}/{len(rows)} exchanges turn both exchanged quadlets red on {leg}")
    return 0 if both == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())

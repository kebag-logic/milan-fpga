#!/usr/bin/env python3
"""Reviewer probe (R461-3): the order of the two sides, without the second walk.

The index + 1 first, then the repeat of the index.

usage: r461_3_order_probe.py --tree EXPORTED_HEAD_TREE --work SCRATCH_DIR --out RECEIPT_DIR [--jobs N]

Rewrites check_noted_index so that the AVAILABLE one above the index is sent
first, straight from the cell's end state, and the repeat second, with no
second walk; runs it on the head RTL and under q1 and q3 of r461_probes.py.
Uses one() of r461_3_probes.py (same copy, anchor and record rules).
"""
import argparse
import concurrent.futures as cf
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r461_3_probes as p  # noqa: E402

SIM = p.SIM
HEAD_BODY = """  const size_t e1 = evts.size();
  load_remote(0, tk, noted, d->gm_id_i, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, tk, 10, 0, now)),
        "%s: the AVAILABLE repeating index %u consumed", tag, noted);
  idle(20);
  const size_t n_rep = evts.size() - e1;
  CHECK(n_rep == 2 && evts[e1].departed && evts[e1].sink == s
            && !evts[e1 + 1].departed && evts[e1 + 1].sink == s,
        "%s: the noted index is at least %u (Milan 5.6.4.5.2 step 3): an AVAILABLE "
        "repeating it is EVT_TK_DEPARTED then EVT_TK_DISCOVERED (step 2), got %zu events",
        tag, noted, n_rep);
  goto_disc(col, s);
  apply_disc(col, row, s);
  idle(20);
  const size_t e2 = evts.size();
  load_remote(0, tk, noted + 1, d->gm_id_i, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, tk, 10, 0, now)),
        "%s: the AVAILABLE at index %u consumed", tag, noted + 1);
  idle(20);
  const size_t n_up = evts.size() - e2;
"""
UPPER_FIRST = """  (void)row; (void)col;
  const size_t e2 = evts.size();
  load_remote(0, tk, noted + 1, d->gm_id_i, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, tk, 10, 0, now)),
        "%s: the AVAILABLE at index %u consumed", tag, noted + 1);
  idle(20);
  const size_t n_up = evts.size() - e2;
  const size_t e1 = evts.size();
  load_remote(0, tk, noted, d->gm_id_i, DOM0, 0, 10, MSG_AVAIL);
  CHECK(send_txn(adp_txn(MSG_AVAIL, tk, 10, 0, now)),
        "%s: the AVAILABLE repeating index %u consumed", tag, noted);
  idle(20);
  const size_t n_rep = evts.size() - e1;
  CHECK(n_rep == 2 && evts[e1].departed && evts[e1].sink == s
            && !evts[e1 + 1].departed && evts[e1 + 1].sink == s,
        "%s: ORDER PROBE the repeat of %u after it: restart pair, got %zu events",
        tag, noted, n_rep);
"""
ORDER = (SIM, HEAD_BODY, UPPER_FIRST)
Q3 = (p.ENG, p.FRESH, "            rec_wr_en_w = gm_dom_ok_w;\n")

PROBES = [
    ("o0-upper-first-control", [ORDER], "TB: one above first, then its repeat, no second walk; head RTL"),
    ("o1-upper-first-q1", [ORDER, p.Q1], "same TB, RTL: q1"),
    ("o3-upper-first-q3", [ORDER, Q3], "same TB, RTL: q3 (fresh branch notes only on a GM match)"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tree", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--jobs", type=int, default=3)
    args = ap.parse_args()
    Path(args.out).mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(args.jobs) as ex:
        results = list(ex.map(lambda q: p.one(args, q), PROBES))
    for name, what, rc, tally, fails in results:
        print(f"{name}: rc={rc} {tally} | {what}")
        for f in fails:
            print(f"    {f}")


if __name__ == "__main__":
    main()

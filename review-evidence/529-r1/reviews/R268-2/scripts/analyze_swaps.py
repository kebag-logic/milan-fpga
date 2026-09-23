#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Summarise the pairwise-exchange receipts of one campaign.

usage: analyze_swaps.py <receipts dir> <campaign tag>

For every swap_<a>__<b> receipt it reports the verdict, whether the event
arm ("[CTRS-CRF] events, all ten") failed on BOTH exchanged quadlets, and
which other check families failed. Prints one line per mutant and a summary.
"""
import pathlib
import re
import sys

Q = {  # KL_crf_rx port -> Table 7-157 quadlet label printed by the harness
    "cnt_locked_o": "@0 MEDIA_LOCKED", "cnt_unlocked_o": "@4 MEDIA_UNLOCKED",
    "cnt_intr_o": "@8 STREAM_INTERRUPTED", "seq_err_o": "@12 SEQ_NUM_MISMATCH",
    "mr_cnt_o": "@16 MEDIA_RESET", "tu_cnt_o": "@20 TIMESTAMP_UNCERTAIN",
    "fmt_err_o": "@32 UNSUPPORTED_FORMAT", "late_cnt_o": "@36 LATE_TIMESTAMP",
    "early_cnt_o": "@40 EARLY_TIMESTAMP", "pdu_count_o": "@44 FRAMES_RX",
}


def family(line: str) -> str:
    m = re.match(r"\s*\[FAIL\] (\[[A-Z0-9-]+\])?\s*([^:]*)", line)
    tag = m.group(1) or ""
    head = (m.group(2) or "").split(":")[0]
    if tag == "[CTRS-CRF]":
        return "CTRS-CRF " + ("events" if head.startswith("events") else head.split(" ")[0])
    return (tag or head[:30]).strip()


def main() -> int:
    d, tag = pathlib.Path(sys.argv[1]), sys.argv[2]
    n = both = killed = only_events = 0
    for r in sorted(d.glob(f"{tag}__swap_*.txt")):
        a, b = r.stem.split("__swap_")[1].split("__")
        txt = r.read_text()
        verdict = re.search(r"^verdict=(\w+)", txt, re.M).group(1)
        fails = [ln for ln in txt.splitlines() if ln.startswith("  [FAIL]")]
        ev = [ln for ln in fails if "[CTRS-CRF] events, all ten:" in ln]
        hit = all(any(Q[p] in ln for ln in ev) for p in (a, b))
        fams = sorted({family(ln) for ln in fails if "events, all ten:" not in ln})
        n += 1
        killed += verdict == "KILLED"
        both += hit
        only_events += verdict == "KILLED" and not fams
        print(f"{r.stem}\t{verdict}\tevents_both_quadlets={'yes' if hit else 'NO'}"
              f"\tother_failing_families={','.join(fams) or '-'}")
    print(f"SUMMARY {tag}: {n} exchanges, {killed} KILLED, {both} with both quadlets red in the "
          f"event arm, {only_events} killed by the event arm alone")
    return 0


if __name__ == "__main__":
    sys.exit(main())

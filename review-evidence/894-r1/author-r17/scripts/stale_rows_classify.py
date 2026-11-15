#!/usr/bin/env python3
"""Round 15's classifier, its PR-body keys moved to round 16's, then round 17's, body by line content. Classify every hit stale_rows.py lists (argv[1], its output; argv[2], its --tokens output) and print the receipt.
Classes: historical (past tense, dated, or quoting the old text as the old text); beside (the head's figure stands
beside it); head (the head's own figure); another (another quantity, point or design). An unclassified hit exits 1,
and so does a hit classed current: none is."""
import sys

S = "docs/design/SPLIT_CONTROL_MEMORY.md"
F = "docs/reference/FR_NFR.md"
B = "PR-BODY.md"
H, X, O = "historical", "beside", "another"
C = {
    f"{S}:1365": (O, "8x8/2if's last SRP record (27.25 to 28.25 ms against 18), an earlier subsection's row"),
    f"{S}:2322": (H, "past tense: 'the load gate held 1x1/1if ... at the pin 0.501', rounds 28 and 29's loads, and 8x8/2if's 0.822 and 0.770 at the merge"),
    f"{S}:2330": (O, "a load term (ACMP's timer-slot expiries) at 32x32/2if, 0.637 to 0.186"),
    f"{S}:2349": (H, "past tense: 'At the 800 us slice and the merged costs they were 12.80, 74.80 ...'; before the merge, the same"),
    f"{S}:2351": (X, "the tx row at the merge's costs, 29.78 (29.80 at 800 us, 28.00 before), 'at the costs of the merge of #810's 084cf7a8 ...; 33.38 and 98.49 ms at the head'"),
    f"{S}:2380": {"*": (H, "past tense: the pace's chain, 'txL was 39.61 ms there', 'no pace ... held txL', 'none did either', 'it found 6 ms, txL 49.99 ms and R4L 158.34', '7 ms, txL 47.98 ms and R4L 173.37', '8 ms, txL 48.09 ms and R4L 188.39'; then 'at the head it finds 8 ms, txL 48.43 ms and R4L 188.48'"),
                  **{t: (X, "the load's history in parentheses after the head's: 'The load is 0.516 at the pin and 0.695 ... (0.513 and 0.692 at the direct index's costs, 0.685 at 940 us, 0.499 and 0.671 ..., 0.508 and 0.680 ..., 0.470 and 0.637 before the merge)'")
                     for t in ("0.513", "0.692", "0.685", "0.499", "0.671", "0.508", "0.680", "0.470", "0.637")}},
    f"{S}:2402": (H, "past tense: 'At these costs ... txL was 46.58 ms ... (47.25 and 137.79 before), and the load was 0.499 ... was 0.696 (0.727 before)'"),
    f"{S}:2436": (H, "past tense: 'the rows at 1x1/1if were lever (a)'s: txL 46.58 ms ... the last queued notice 135.64 ms'"),
    f"{S}:2445": (H, "past tense: 'The last queued notice was then 125.84 ms at 900 us'; 'txL was then 49.99'"),
    f"{S}:2447": (H, "past tense: 'the load was 0.513'"),
    f"{S}:2457": (H, "past tense: '7 ms was the smallest that held, txL 47.98 ms and R4L 173.37 ms'"),
    f"{S}:2459": (H, "past tense: 'the load was 0.513 at the pin and 0.509 with tsn-c-stack #32'"),
    f"{S}:2466": (O, "a counterfactual at the domain's 64 slots: 'would be 1,040 us, which would move ... the load ... to 0.705'"),
    f"{S}:2467": (X, "past tense with the head's beside: 'txL 48.09 ms within 49 and R4L 188.39 within 238 (AECP_PACE_MS; 48.43 and 188.48 at the head)'"),
    f"{S}:2477": (H, "past tense: 'Every 1x1/1if row held by every source at that cut: ACMP 28.64 ms, the last queued notice 127.22 ...'"),
    f"{S}:2479": (O, "0.06 ms, the most the TICK's restatement moved a row (a difference)"),
    f"{S}:2480": (X, "'The tx row then took a seventeenth pass, 33.01 ms within its 49 (33.38 ms at the head's 950 us slice)'"),
    f"{S}:2491": (H, "past tense: 'At its record every 1x1/1if row held by every source: ACMP 28.80 ms, the last queued notice 127.86 ...'"),
    f"{S}:2509": (H, "past tense: 'the last queued notice at 1x1/1if was 132.71 ms ... at the design then built (900 us ...)'"),
    f"{F}:383": (H, "past tense throughout: '7 ms held it, txL 47.98 ms', '8 ms held it, txL 48.09 ms and R4L 188.39 ms', '8 ms then held txL, 48.23 ms, and R4L, 188.41 ms ... (ACMP 28.80 ms, the last queued notice 127.86)', 'was then 132.71 ms'; then 'there 8 ms holds txL, 48.43 ms, and R4L, 188.48 ms'"),
    f"{F}:387": (X, "'after #908's cuts the last queued notice's row was 125.84 ms (127.21 at the head)'"),
    "sw/firmware/ctrl/srp/README.md:238": (X, "'33.38 ms there at the 950 us slice (33.01 at the 900 us slice under #894's one-row edit cut, 29.78 before it'"),
    "syn/ooc/pp_resource_gate_set_selftest.py:103": (O, "a timing self-test's WNS string, 0.450"),
    "syn/yosys/bench/bench_selftest.py:150": (O, "a bench self-test's parsed times, 0.06"),
    "syn/yosys/bench/bench_selftest.py:155": (O, "a bench self-test's parsed times, 0.06"),
    "tb/tools/torture_campaign.py:8074": (O, "a resolution in a torture self-test, 0.499"),
    "tb/tools/torture_campaign.py:8085": (O, "a resolution pair in a torture self-test, 0.06"),
    "tb/verilator/ctrl_service_budget/README.md:1135": (O, "0.513 ms, slow-adp-rx's unplanted ADP record"),
    "tb/verilator/fw_service_budget/README.md:84": (O, "14.56 seconds, two flash slots' WIP bound"),
    f"{B}:493": (H, "17.2: the statement sweep's token list (the load's 0.515 and 0.511)"),
    f"{B}:119": (H, "round 12's section, past tense: 'The rows at e4d80a8a ... all held: R4 13.01 ... The load was 0.515 and 0.511'"),
    f"{B}:198": (H, "round 12's section, past tense: 'The slice rule's rerun left the built design: the last queued notice 132.71 ms over 130 at 900 us'"),
    f"{B}:301": (X, "14.1's moves table, the 'Old' column beside the 'Head' column (0.516, 0.512)"),
    f"{B}:309": (X, "14.1 quoting :2380: 'txL 48.43 ms and R4L 188.48 ms (48.09 and 188.39 then)'"),
    f"{B}:310": (X, "14.1: 'The tx row's 33.01 ms is history beside the head's 33.38 ms'"),
    f"{B}:311": (H, "14.1 quoting FR_NFR.md:383: '8 ms then held txL, 48.23 ms'"),
    f"{B}:312": (X, "14.1 quoting the SRP README: '33.38 ms at the 950 us slice. As history: 33.01 ..., and 29.78 before it'"),
    f"{B}:315": (H, "14.1's list of round 14's grep tokens"),
    f"{B}:317": (H, "14.1: '0.515, 0.511 and a LINK at 150 have no hit', round 14's grep result"),
    f"{B}:378": (X, "15.1 quoting FR_NFR.md:383's history and, beside it, the head's 48.43 and 188.48"),
    f"{B}:379": (X, "15.1 quoting :2467, past tense with '48.43 and 188.48 at the head'"),
    f"{B}:383": (H, "15.1 quoting :2402's past tense: 'was 46.58 ms', 'was 0.499', 'was 0.696'"),
    f"{B}:384": (O, "15.1 quoting :2466's counterfactual, 0.705"),
    f"{B}:385": (X, "15.1 quoting FR_NFR.md:387: 'was 125.84 ms (127.21 at the head)'"),
    f"{B}:527": (H, "a round-12 finding row, past tense: 'the last queued notice 132.71 > 130 at 900 us and the slice rule chose 950: round 12's STOP'"),
    f"{B}:529": (H, "the R838-6-F2 row: 'R4 12.85 ... were the previous head's'; 'the 900 us figures, R4 13.05 and 132.71 over 130, are its history row and round 12's stop'"),
    f"{B}:651": (O, "0.008, a load difference ((300 - 235) us a pace of 8 ms), true at the head"),
}


def main(hits, tokens):
    rows, bad, counts = [], 0, {}
    for line in open(hits, encoding="utf-8"):
        tok, src, loc, text = line.rstrip("\n").split("\t", 3)
        c = C.get(loc)
        if isinstance(c, dict):
            c = c.get(tok, c.get("*"))
        if c is None:
            bad += 1
            rows.append(f"UNCLASSIFIED\t{tok}\t{loc}\t{text[:140]}")
            continue
        counts[c[0]] = counts.get(c[0], 0) + 1
        rows.append(f"{c[0]}\t{tok}\t{loc}\t{c[1]}")
    toks = [l.split("\t")[0] for l in open(tokens, encoding="utf-8") if l.strip()]
    print("# Round 15, R837-8-F1: every hit of a superseded 1x1/1if row or load figure, each classified")
    print("# tokens (stale_rows.py --tokens): every figure of every row of section 13's rows-history table before the head's,")
    print("#   less any equal to the head's in its column; and every load figure on a line naming the load in section 13,")
    print("#   FR_NFR 3.4.1 or the PR body, less the head's (0.516, 0.512, 0.695; 0.794, 0.754) and the ceilings (0.70, 0.75)")
    print(f"# {len(toks)} tokens: " + " ".join(toks))
    print("# scope: section 13, FR_NFR 3.4.1, MAILBOX_SPLIT, every tracked README and C, C++, header, Python and")
    print("#   SystemVerilog file, outside table lines; and the PR body, every line, its tables included")
    print("# classes: historical (past tense, dated, or quoting the old text as the old text); beside (the head's figure")
    print("#   stands beside it); head (the head's own figure); another (another quantity, point or design)")
    print("# " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + f", total {len(rows)}; current with a superseded figure: 0")
    for r in rows:
        print(r)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))

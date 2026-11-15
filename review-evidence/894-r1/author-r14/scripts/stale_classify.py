#!/usr/bin/env python3
"""Classify every hit stale_grep.py lists (argv[1], its tab-separated output) and print the receipt.

Every hit must have a class; an unclassified one fails the run (exit 1)."""
import sys

S = "docs/design/SPLIT_CONTROL_MEMORY.md"
H = "historical"
U = "unrelated"
C = {
    f"{S}:1215": (U, "an earlier rows table in section 13 (### The rows), owed-row ms such as 65.13, not a timer slot"),
    f"{S}:1277": (U, "a later rows table of the same kind, owed-row ms"),
    f"{S}:1357": (U, "a later rows table of the same kind, owed-row ms"),
    f"{S}:1444": (U, "a later rows table of the same kind, owed-row ms"),
    f"{S}:1579": (U, "a later rows table of the same kind, owed-row ms"),
    f"{S}:1704": (U, "a later rows table of the same kind, owed-row ms"),
    f"{S}:1899": (U, "a later rows table of the same kind, owed-row ms"),
    f"{S}:2194": (U, "an 8x8/2if THE SHARE sum (1,215 a build of one there), not 1x1/1if's AECP timer slot"),
    f"{S}:2224": (H, "the polls-by-source table of #665's round-22 ruling (its base 155 is superseded too, 205 at :2285 and :2340); poll_grade.STATED_US holds 280 at the head"),
    f"{S}:2246": (U, "ms figures (65.86 ms) and a record count (50 records), #665's rules"),
    f"{S}:2292": (H, "#665 round 26's SRP record cut: '250 at 1x1/1if (250 before)'"),
    f"{S}:2310": (H, "#665's re-grade on the composed image, restatements written 'from X to Y'"),
    f"{S}:2312": (H, "#665 round 30's re-grade, restatements 'from X to Y' ('AECP's timer slot 60 to 65')"),
    f"{S}:2340": (H, "#810's merge raising an SRP record 'to 280 us (250)': the old value in parentheses"),
    f"{S}:2342": (H, "'the rule picked 900 us' then, and 'at the costs restated under the SET_CONFIGURATION cut it picks 950 us'; '50 us grid' is the first sweep's step"),
    f"{S}:2351": (H, "explicitly 'at the costs of the merge of #810's 084cf7a8' (29.78 ms at 900 us); '50 ms' is a bound"),
    f"{S}:2364": (H, "the rows-history table, the contingent moves' row (19 cs, 6 ms, 900 us)"),
    f"{S}:2365": (H, "the rows-history table, 'And a build of one at 725 us' row"),
    f"{S}:2368": (H, "the rows-history table, the one-row edit cut's row (a TICK at 50 us, tx 33.01)"),
    f"{S}:2370": (H, "the rows-history table, the final pass's restatements' row at the 900 us design (R4 13.05, last 132.71); the head's row is the next"),
    f"{S}:2373": (H, "past tense: 'it held every row, and tier_grid.py held 6 of the 420, choosing the built design at 900 us'"),
    f"{S}:2443": (H, "past tense: 'then followed the slice ruling's rule ... 900 us ... (950 us since #894's ruling of 2026-11-15)'"),
    f"{S}:2444": (H, "past tense: 'A 900 us slice held', 'By the rule it was 725 us ... 735 us since the SET_CONFIGURATION cut'"),
    f"{S}:2445": (H, "past tense: 'The last queued notice was then 125.84 ms at 900 us'"),
    f"{S}:2457": (H, "past tense: the pace at the 975 us record, 'The slice rule still gave 900 us'"),
    f"{S}:2467": (H, "past tense: item 4's re-measure, 'the slice rule still gave 900 us'"),
    f"{S}:2479": (H, "'A TICK at 1x1/1if was then stated at 50 us ... it is 55 us since the SRP drain's record cost moved'; the cut's full arm's '50 us by the rule' is that arm's measurement"),
    f"{S}:2480": (H, "'The tx row then took a seventeenth pass, 33.01 ms ... (33.38 ms at the head's 950 us slice)'; 'over the 50 stated' is ACMP's owed frame then"),
    f"{S}:2489": (H, "'within event.TICK's 50 and 40 us then (55 at 1x1/1if since)'"),
    f"{S}:2498": (H, "past tense: 'ctrl_loop.h stated CTRL_LOOP_SRP_UNIT_US ... at 250 us', the SRP drain's move"),
    f"{S}:2509": (H, "past tense: 'the last queued notice at 1x1/1if was 132.71 ms ... at the design then built (900 us ...)'"),
    "docs/reference/FR_NFR.md:383": (H, "'a TICK at 50 us ... 8 ms then held txL', 'was then 132.71 ms ... at the 900 us slice, and the slice rule chose 950 us, which the built slice now is'"),
    "hdl/common/csr/milan_csr.sv:1490": (U, "725 Mb/s, the idleSlopes' sum"),
    "hdl/common/ethernet_packet_pkg.sv:268": (U, "725 Mb/s, the idleSlopes' sum"),
    "sw/firmware/ctrl/srp/README.md:238": (H, "'33.38 ms there at the 950 us slice (33.01 at the 900 us slice under #894's one-row edit cut, 29.78 before it'"),
    "sw/firmware/ctrl/test/test_aecp.cpp:1881": (U, "test clock step, ms+=250"),
    "sw/firmware/ctrl/test/test_aecp.cpp:1882": (U, "test clock step, ms+=250"),
    "sw/firmware/ctrl/test/test_aecp.cpp:2255": (U, "test clock step, ms+=250"),
    "sw/firmware/ctrl/test/test_aecp.cpp:2912": (U, "default_count=65, a map count bound"),
    "sw/trace/trace_selftest.c:255": (U, "a trace self-test's parsed count, 900u + rnd()"),
    "sw/trace/trace_selftest.c:318": (U, "a trace self-test's parsed count, 900u + rnd()"),
    "tb/verilator/csr/milan_csr_ref.sv:1470": (U, "725 Mb/s, the idleSlopes' sum"),
    "tb/verilator/csr/sim_main.cpp:432": (U, "725 Mb/s, the idleSlopes' sum"),
    "tb/verilator/ctrl_service_budget/load_grade.py:126": (H, "restatement history: 'under #894's edit cut a TICK at 1x1/1if 45 to 50 us'"),
    "tb/verilator/ctrl_service_budget/load_grade.py:134": (H, "restatement history: 'a TICK at 1x1/1if 50 to 55'; the table holds 55"),
    "tb/verilator/ctrl_service_budget/load_grade.py:149": (U, "item.aecp.response 65 at 8x8/2if, a head figure, not the timer slot"),
    "tb/verilator/ctrl_service_budget/load_grade.py:155": (U, "item.aecp.response 65 at 32x32/2if, a head figure"),
    "tb/verilator/ctrl_service_budget/load_grade.py:171": (H, "restatement history: 'at 1,010 and 725 us ... under #894's ... 735'; the table holds 735"),
    "tb/verilator/ctrl_service_budget/load_grade.py:183": (U, "item.aecp.response 65 at 8x8/2if (donor table), a head figure"),
    "tb/verilator/ctrl_service_budget/load_grade.py:190": (U, "item.aecp.response 65 at 32x32/2if (donor table), a head figure"),
    "tb/verilator/ctrl_service_budget/load_grade.py:570": (H, "the planted control: it writes the old 250 us limit into a copy of the header so --check must refuse it"),
    "tb/verilator/ctrl_service_budget/rows_tiers.py:73": (U, "'under 65 us each', the room the walk (35) and reclaim (25) leave, true at the head"),
    "tb/verilator/ctrl_split_boot/README.md:91": (U, "65.026 ms to ready, a boot time"),
    "tb/verilator/milan_dp/README.md:989": (U, "a mutant row number"),
    "tb/verilator/milan_dp/README.md:1431": (U, "byte offset 65 in a twin-compare example"),
    "tb/verilator/milan_dp/twin_compare.py:73": (U, "byte offset 65 in a twin-compare example"),
}


def main(path):
    rows, bad = [], 0
    for line in open(path, encoding="utf-8"):
        tok, loc, text = line.rstrip("\n").split("\t", 2)
        cls = C.get(loc)
        if cls is None:
            bad += 1
            rows.append(f"UNCLASSIFIED\t{tok}\t{loc}\t{text[:120]}")
            continue
        rows.append(f"{cls[0]}\t{tok}\t{loc}\t{cls[1]}")
    counts = {}
    for r in rows:
        counts[r.split("\t")[0]] = counts.get(r.split("\t")[0], 0) + 1
    print("# Round 14, R837-7-F1: every hit of the stale-figure tokens, each classified")
    print("# tokens: 725, 33.01, 900 us, 0.515, 0.511, 13.05, 132.71, 50 (lines naming TICK), 65 (lines naming AECP, a timer or a slot),")
    print("#         150 (lines naming LINK), 250 (lines naming SRP or the drain)")
    print("# scope: SPLIT_CONTROL_MEMORY.md section 13, FR_NFR.md 3.4.1, every tracked README, every tracked .c .h .cpp .hpp .py .sv .svh .v .yml")
    print("# classes: historical = stated as then or as an old value beside the head's; unrelated = another quantity")
    print("# head figure = none left in current tense with an old value")
    print("# " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + f", total {len(rows)}")
    print("# 0.515, 0.511 and 150 (LINK): no hit")
    for r in rows:
        print(r)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

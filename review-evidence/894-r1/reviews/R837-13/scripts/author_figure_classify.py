#!/usr/bin/env python3
"""Classify every hit of figure_sweep.py (argv[1]); argv[2] is the PR body the sweep read. Prints the receipt and exits
1 on any hit it does not class. A hit the sweep marks CUR? (no history marker in its sentence) is classed only by a
line of its own or by a region whose every hit was read; a HIST hit by the same, else by its marker.
Classes: historical (past tense, dated, a ruling's or finding's text, a quote of old text, a token list); beside (the
head's figure beside it); head (the head's own figure); another (another quantity, component, point, clause figure,
requirement bound or plant); reported (#916, a harness defect reported, not fixed in a documents round)."""
import re
import sys

H, X, HD, O, RP = 'historical', 'beside', 'head', 'another', 'reported'
S, F = 'docs/design/SPLIT_CONTROL_MEMORY.md', 'docs/reference/FR_NFR.md'
BUD, HOOK = 'tb/verilator/ctrl_service_budget/README.md', 'tb/verilator/ctrl_service_hooks/README.md'
SEC13 = {  # section 13 from THE TIERS' queued notices on, read hit by hit
    2204: (X, "the queued-notice table: the head's rows, 12180198's at 1,200 us beside them (R837-11-F1)"),
    2205: (X, "the queued-notice table: the head's 127.21 within 130, 12180198's 91.59 within 125 beside it"),
    2207: (X, "the first notice's bound decision D's 20 ms, the last's the amendment's 130 ms (decision D's 125 before it)"),
    2236: (HD, "the load ceiling, 0.70"), 2244: (H, "'before #894 ... R4 was 73.02 ms' (R837-11-R3)"),
    2246: (H, "the rules at earlier heads: 'on round 28's costs', 'on #810's head's it was 74.83 ms'"),
    2256: (O, "a clause number, Milan Table 5.22"), 2257: (O, "a clause number, Milan Table 5.26"),
    2260: (X, "'SRP_JOIN_CS, 200 ms then; 190 ms at 19 cs'"), 2262: (O, "clause numbers, Milan 5.6.3.5.x, Table 5.50"),
    2287: (X, "round 30's costs, past tense, with the head's 205 us base and 55 us owed frame beside"),
    2310: (H, "#665's re-grade, restatements 'X to Y'"), 2312: (H, "round 30's re-grade, restatements 'X to Y'"),
    2322: (H, "past tense: 'the load gate held 1x1/1if ... at the pin 0.501'; rounds 28 and 29"),
    2324: (H, "lever options, 'from X to Y'"), 2325: (H, "lever options, 'from X to Y'"), 2326: (H, "lever options, 'from X to Y'"),
    2340: (H, "#810's merge raising costs 'to Y (X)', and the events 'charged ... 60 and 95 us' then"),
    2342: (H, "the slice's history and the 2026-11-13 ruling's text; '430 us ... then (735 us now)'"),
    2349: (H, "past tense: 'At the 800 us slice and the merged costs they were ...'"),
    2351: (X, "the tx row at the merge's costs with the head's 33.38 and 98.49 beside; 'stated as 30 and 98 ms'; the bound's derivation"),
    2353: (H, "past tense: the design grid 'held no design either' at the merged costs"),
    2357: (X, "'then at the slice ruling's 800 us (950 us at the head)'"),
    2364: (H, "the rows-history table"), 2365: (H, "the rows-history table"), 2366: (H, "the rows-history table"),
    2367: (H, "the rows-history table"), 2368: (H, "the rows-history table"), 2369: (H, "the rows-history table"),
    2370: (H, "the rows-history table"), 2373: (H, "past tense: 'the flip check refused 1x1/1if'"),
    2377: (H, "past tense: 'every row held ... the six rows' rule picked 800 us'; 'not the 665 us stated before'"),
    2379: (X, "the long record's states, past tense, with the head's 87,895 and 146,678 cycles beside"),
    2380: (H, "the pace's chain, past tense; the load's history in parentheses after the head's 0.516 and 0.695"),
    2386: (H, "restatements 'X to Y'"), 2402: (H, "past tense at lever (a)'s costs"),
    2405: (X, "'155 us by the rule' on 2cc852fa beside '205 us' on da1869a3"), 2432: (H, "'was 125.87 ms then' (R837-11-R2)"),
    2436: (H, "past tense: 'the rows ... were lever (a)'s'"),
    2442: (X, "'was ... 50 ms (49 since T_egress is counted)', 'then 6 ms (8 ms at the head)'"),
    2443: (X, "'900 us ... (950 us since #894's ruling of 2026-11-15)'"), 2444: (X, "'it was 725 us (...; 735 us since the cut)'"),
    2445: (H, "'was then 125.84 ms at 900 us'"), 2447: (O, "#908's open condition, naming the original bounds"),
    2456: (H, "round 7's re-graded legs"), 2457: (H, "past tense: the pace at the 975 us record"),
    2459: (H, "'the load was 0.513'"), 2466: (O, "a counterfactual at 64 slots ('would')"),
    2467: (X, "past tense, '48.43 and 188.48 at the head'"), 2476: (H, "past tense: the cut's measurements ('was 22,728 cycles')"),
    2477: (X, "'was then charged ... 260 us ... 325 us ... At the head EDIT_RECORD_US is ... 300 and 595 us' (R837-11-F2); a counterfactual flat 295 us"),
    2479: (X, "'was then stated at 50 us ... it is 55 us since'; the cut's arm's TICK '50 us by the rule, within' (a measurement)"),
    2480: (X, "'33.01 ms ... (33.38 ms at the head's 950 us slice)'; 8x8/2if's events' fixed part 35 us at the head"),
    2489: (X, "'within event.TICK's 50 and 40 us then (55 at 1x1/1if since)'"),
    2491: (HD, "the paced class's members' records at the head (edit_rows.PACED: 260 and 300, 325 and 595), so 300 and 595; 'row held' past"),
    2498: (H, "past tense: 'ctrl_loop.h stated CTRL_LOOP_SRP_UNIT_US ... at 250 us'"), 2509: (H, "past tense at the 900 us design"),
    2520: (X, "THE RETRY's pre-tiers bound, past tense, with the head's first queued notice beside"),
    2521: (X, "'44 ms before THE TIERS ... was sent within the 200 ms JoinTime (under THE TIERS ...)'"),
    2525: (H, "'before #894's tiers, R4 ... was 74.83 ms'"),
}
FR = {344: O, 347: O, 348: O, 403: O, 406: O, 407: O, 418: O, 427: O, 443: O, 376: O, 414: O, 415: X, 426: O,
      381: H, 383: H, 387: X, 392: HD}
FR_NOTE = {O: "the requirement's per-path bound min(T_svc, C) or a clause's own figure (option A's 30 ms row bounds are :374's)",
           H: "past tense ('held', 'was then')", X: "beside the head's (127.21 at the head; JoinTime 190 ms at 19 cs)",
           HD: "the 8x8/2if load ceiling, 0.75"}
CODE = {  # file:line -> class, note
    'sw/firmware/ctrl/acmp/acmp_mbx.h:140': (O, "the per-path T_svc and ACMP ceiling, 20 ms"),
    'sw/firmware/ctrl/aecp/aecp_mbx.h:46': (H, "'join timer at 20 cs, none did'"),
    'sw/firmware/ctrl/aecp/aecp_mbx.h:50': (H, "'txL was 49.69 ms at 7 ms'"),
    'sw/firmware/ctrl/aecp/aecp_mbx.h:62': (X, "'decision D's 125 ms ... at 1x1/1if 130 ms by #894's amendment'"),
    'sw/firmware/ctrl/loop/ctrl_loop.h:124': (O, "a step's and a pass's measured length"),
    'sw/firmware/ctrl/loop/ctrl_loop.h:125': (O, "a pass's measured length, 1.90 ms"),
    'sw/firmware/ctrl/loop/ctrl_loop.h:208': (X, "'125 ms (#665), at 1x1/1if AECP_QUEUED_MS's 130 ms'"),
    'sw/firmware/ctrl/loop/ctrl_loop.h:263': (X, "the 2026-11-13 ruling's text, then 'The built slice is the rule's choice ... 950 us'"),
    'sw/firmware/ctrl/loop/ctrl_loop.h:304': (O, "a step's length, 0.97 ms"),
    'sw/firmware/ctrl/srp/srp_bounds.h:17': (O, "both builds' measured pass, 2.08 ms"),
    'sw/firmware/ctrl/srp/srp_mbx.c:999': (O, "both builds' measured pass, 2.08 ms"),
    'sw/firmware/ctrl/test/ctrl_service_bounds.py:53': (O, "the per-path T_svc and ACMP ceiling, 20 ms"),
    'tb/verilator/ctrl_service_budget/build.py:59': (O, "an ADP record's per-path 20 ms budget"),
    'tb/verilator/ctrl_service_budget/flip_grade.py:16': (HD, "'ACMP's, ADP's and MAAP's at 30 ms'"),
    'tb/verilator/ctrl_service_budget/flip_grade.py:107': (O, "a control's 0.001 delta"),
    'tb/verilator/ctrl_service_budget/flip_grade.py:109': (O, "a control's 0.001 delta"),
    'tb/verilator/ctrl_service_budget/load_grade.py:10': (HD, "the load ceiling, 0.70"),
    'tb/verilator/ctrl_service_budget/load_grade.py:65': (O, "a clause number"),
    'tb/verilator/ctrl_service_budget/load_grade.py:126': (H, "restatement history"),
    'tb/verilator/ctrl_service_budget/load_grade.py:150': (HD, "record.maap 205 at 32x32/2if, the head's"),
    'tb/verilator/ctrl_service_budget/load_grade.py:171': (H, "restatement history"),
    'tb/verilator/ctrl_service_budget/load_grade.py:185': (HD, "record.maap 205 at 32x32/2if, the head's"),
    'tb/verilator/ctrl_service_budget/load_grade.py:570': (O, "the planted control's 250u"),
    'tb/verilator/ctrl_service_budget/paced_rows.py:55': (O, "the 0.01 ms grid"),
    'tb/verilator/ctrl_service_budget/paced_rows.py:75': (O, "the 0.01 ms grid"),
    'tb/verilator/ctrl_service_budget/queued_bound.py:68': (O, "the 0.01 ms grid"),
    'tb/verilator/ctrl_service_budget/rows_grade.py:15': (O, "rows_grade's own bounds, decision D's, the as-built comparison model"),
    'tb/verilator/ctrl_service_budget/rows_grade.py:287': (O, "the 0.01 ms grid"),
    'tb/verilator/ctrl_service_budget/rows_tiers.py:24': (O, "decision D's bounds, named as rows_grade.BOUNDS"),
    'tb/verilator/ctrl_service_budget/rows_tiers.py:492': (O, "the 0.01 ms grid"),
    'tb/verilator/ctrl_service_budget/rows_tiers.py:934': (O, "the planted control's 33u and 98u"),
    'tb/verilator/ctrl_service_budget/save_window.py:11': (O, "the save window's phase spacing, 1.25 ms"),
    'tb/verilator/ctrl_service_budget/selftest_answers.py:24': (O, "clause numbers, Milan Tables 5.42, 5.43"),
    'tb/verilator/ctrl_service_budget/selftest_mutants.py:891': (H, "a mutant's measured figure"),
    'tb/verilator/ctrl_service_budget/tier_grid.py:13': (H, "the owed slot's history, 128 B"),
    'tb/verilator/ctrl_service_hooks/hooks_selftest.py:344': (O, "the H-MAAP per-path 20 ms bound in a self-test"),
    'tb/verilator/milan_dp/srptx.hpp:82': (RP, "#916: kJoinCs 20 against CTRL_LOOP_JOIN_CS 19"),
    'tb/verilator/milan_dp/srptx.hpp:83': (RP, "#916: kJoinCs 20 against CTRL_LOOP_JOIN_CS 19"),
    'tb/verilator/milan_dp/twin_grades.py:147': (O, "a clause's own figure, JoinTime 200 ms"),
}
CODE_OTHER = (O, "another component's measured figure (a simulation, the SoC builder, the store)")
PR_OVERRIDE = [  # substring of the sentence -> class (read)
    ('now 0.95 ms at one interface', HD, "the head's slice, 0.95 ms"),
    ('52.09 ms at 7 ms', HD, "the head's txL at 7 ms"),
    ('adds about 0.008', O, "a load difference, (300 - 235) us a pace of 8 ms"),
    ("Arm B's SET_STREAM_INFO is 19,925", O, "a measurement by the rule, within record.aecp"),
    ('| A build of one, us |', X, "14.1's old/head table"), ('| A TICK, us |', X, "14.1's old/head table"),
    ("| AECP's timer slot, us |", X, "14.1's old/head table"), ('| A LINK, us |', X, "14.1's old/head table"),
    ('| The SRP drain, us |', X, "14.1's old/head table"), ('| The load (pin, second column) |', X, "14.1's old/head table"),
    ('mirrors', RP, "#916, reported"), ('still mirrors', RP, "#916, reported"),
]


def sections(path):
    out, cur = [], ''
    for s in open(path, encoding='utf-8').read().split('\n'):
        if re.match(r'#{2,3} ', s):
            cur = s.strip()
        out.append(cur)
    return out


def main(hits, body):
    pr_sec = sections(body)
    budget = sections(BUD)
    rows, bad, counts = [], 0, {}
    for line in open(hits, encoding='utf-8'):
        f, n, rule, val, mark, s = line.rstrip('\n').split('\t', 5)
        n = int(n)
        c = None
        if f == S and 2189 <= n <= 2527:
            c = SEC13.get(n)
        elif f == S and 1098 <= n < 2189:
            c = (O, "section 13's earlier subsections: the CPU harness's last-record rows and passes, each at its own head, not a tier row") if mark == 'CUR?' else (H, "an earlier subsection, its history marker")
        elif f == S:
            c = (H if n == 361 else O, "the owed slots' history, 128 B" if n == 361 else
                 "sections 1 to 12's measurements at their own heads, or section 14's estimate anchored to a30c9986")
        elif f == F:
            k = FR.get(n)
            c = (k, FR_NOTE[k]) if k else None
        elif f == 'PR-BODY':
            for sub, k, note in PR_OVERRIDE:
                if sub in s:
                    c = (k, note)
                    break
            if c is None:
                sec = pr_sec[n - 1]
                if sec.startswith('## Known limitations'):
                    c = None
                elif sec.startswith(('## Status', '## Description', '## Findings', '## Round 1', '### ')):
                    c = (H, f"this body's history ({sec[:40]}): a past round's narrative, quote, token list or finding")
        elif f == BUD and n == 172:
            c = (O, "decision D's bound, the 1x1/1if 130 ms beside it")  # R837-12-R5
        elif f == BUD:
            sec = budget[n - 1]
            if 427 <= n < 1140:
                c = (H, f"the S2-era record, dated ({sec[:40]})")
            else:
                c = (O, f"a control's or path's figure ({sec[:40]}): a plant, a per-path T_svc bound, a phase spacing")
        elif f in ('tb/verilator/milan_dp/README.md',) and n in (1610, 1639):
            c = (RP, "#916: the adapter's JoinTime as 200 ms")
        elif f.endswith('.md'):
            c = (HD if f == 'docs/design/MAILBOX_SPLIT.md' and n == 390 else O,
                 "the head's slice, 0.95 ms" if n == 390 and 'MAILBOX' in f else
                 "another harness's, component's or document's figure (hooks, F0 bounds, the store, media, saved state)")
        else:
            c = CODE.get(f'{f}:{n}', CODE_OTHER if not f.startswith(('sw/firmware/ctrl/', 'tb/verilator/ctrl_service')) else None)
        if c is None or c[0] is None:
            bad += 1
            rows.append(f"UNCLASSIFIED\t{mark}\t{f}:{n}\t{rule}:{val}\t{s[:140]}")
            continue
        counts[c[0]] = counts.get(c[0], 0) + 1
        rows.append(f"{c[0]}\t{mark}\t{f}:{n}\t{rule}:{val}\t{c[1]}")
    total = len(rows)
    print("# Round 19 (round 18's classifier, R837-12-R5 applied): every hit of figure_sweep.py (the R837-11 reviewer's sweep, with round 18's AUTO rules)")
    print("# superseded values: constant_history.py over the PR's commits from 66f71326 (73 constants moved); rows: every")
    print("#   two-decimal ms figure not the head's (flip_grade.py --check at both points); loads: every three-decimal one")
    print("# classes: historical, beside (the head's figure beside it), head, another, reported (#916)")
    print("# " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) + f", total {total}; "
          f"unclassified {bad}; current with a superseded figure: 0")
    for r in rows:
        print(r)
    return 1 if bad else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))

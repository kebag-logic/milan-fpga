#!/usr/bin/env python3
"""Classify every hit statement_sweep.py lists (argv[1]) and print the receipt. A location's class may differ by its
sentence (the sweep's sentence index) or by the hit's label. An unclassified hit exits 1.
Classes: historical (past tense, dated, a ruling's or a finding's text, a quoted old text, or a token list); beside
(the head's figure stands beside it); another (another quantity, component or clause's own figure); reported (it
names a defect found here and reported for its own Issue, not fixed in a documents round)."""
import sys

S, F, B = "docs/design/SPLIT_CONTROL_MEMORY.md", "docs/reference/FR_NFR.md", "PR-BODY.md"
H, X, O, RP = "historical", "beside", "another", "reported"
MDP = "tb/verilator/milan_dp"
C = {
    f"{S}:2004": (H, "'30 + 7 x 2 = 44 ms (before THE TIERS; ... 34 and 99 ms at the head)'; 'was then within 2 x MBX_N_IF x 44 = 176 ms ... inside the 200 ms JoinTime'; then what governs under THE TIERS (R837-10-F1)"),
    f"{S}:2197": (X, "'735 us at 1x1/1if (430 before #894's round 7, below)'"),
    f"{S}:2211": (O, "800 us, the polls' heaviest measured instance at 8x8/2if (round 21), not a slice"),
    f"{S}:2260": (X, "'(SRP_JOIN_CS, 200 ms then; 190 ms at 19 cs since #908's contingent moves)'"),
    f"{S}:2310": (H, "#665's re-grade: restatements written 'from X to Y'"),
    f"{S}:2312": (H, "#665 round 30's re-grade: restatements written 'X to Y'"),
    f"{S}:2340": (H, "#810's merge raising costs 'to Y (X)': the old value in parentheses"),
    f"{S}:2342": {0: (H, "past tense: 'The slice at 1x1/1if was first ... 1,200 us'"),
                  1: (H, "the slice ruling of 2026-11-13's text: it 'sets it to 800 us'"),
                  2: (H, "the ruling's text ('may take the rule's choice instead of 800 us') and past tense ('with ... the pace at 6 ms ... every row held and the rule picked 900 us')"),
                  4: (X, "'which stated 1x1/1if's 430 us for every one-interface shape then (735 us now)'")},
    f"{S}:2349": (H, "past tense: 'At the 800 us slice and the merged costs they were ...'"),
    f"{S}:2351": {0: (X, "the tx row 'at the 900 us slice (29.80 at 800 us) ... at the costs of the merge ...; 33.38 and 98.49 ms at the head), which CTRL_LOOP_TX_MS stated as 30 and 98 ms'"),
                  5: (X, "the bound's derivation: 'At the 200 ms default that is 40 ms ... with the join timer at 19 cs, 190 ms, it is 50 ms, and with the fabric's T_egress counted, 49 ms'")},
    f"{S}:2357": (X, "'The built design is the option's, then at the slice ruling's 800 us (950 us at the head)'"),
    f"{S}:2359": (X, "the rows table's header: 'MRPDU (40; 50 at 19 cs; 49 with T_egress)'"),
    f"{S}:2364": (H, "the rows-history table: the contingent moves' row (a 6 ms pace, 900 us)"),
    f"{S}:2365": (H, "the rows-history table: 'And a build of one at 725 us' row"),
    f"{S}:2366": (H, "the rows-history table: the egress row (a 7 ms pace)"),
    f"{S}:2368": (H, "the rows-history table: the one-row edit's row (a TICK at 50 us)"),
    f"{S}:2373": (H, "past tense: 'the join timer at 20 cs and the 800 us slice, the flip check refused 1x1/1if'; 'choosing the built design at 900 us'"),
    f"{S}:2377": (H, "past tense: 'every row held ... and the six rows' rule picked 800 us'"),
    f"{S}:2380": (H, "past tense: 'no pace ... held txL: 47.96 ms at 7 ms'; 'With the join timer at 19 cs and txL's bound at 50 ms it found 6 ms'"),
    f"{S}:2436": (H, "past tense: 'the rows ... were lever (a)'s: ... over 40 at every pace'"),
    f"{S}:2442": {0: (H, "past tense: 'txL was over 40 ms at every pace that holds R4L within 240 ms'; the clause cited, Milan Table 4.3's 180 to 240 ms, holds 19 cs's 190 ms"),
                  1: (X, "'THE TRANSMIT's MRPDU bound was 240 ms less it, 50 ms ... (CTRL_LOOP_TX_BOUND_MS; 49 ms since T_egress is counted)'"),
                  2: (X, "'The pace stayed the smallest that held, then 6 ms (AECP_PACE_MS; 8 ms at the head)'")},
    f"{S}:2443": (X, "'900 us at 1x1/1if (CTRL_LOOP_SLICE_US; 950 us since #894's ruling of 2026-11-15)'"),
    f"{S}:2444": (X, "past tense: 'over the 430 us stated', 'A 900 us slice held', 'By the rule it was 725 us (...; 735 us since the SET_CONFIGURATION cut)'"),
    f"{S}:2445": (H, "past tense: 'was then 125.84 ms at 900 us', 'txL was then 49.99 of 50 ms'"),
    f"{S}:2447": (O, "#908's open condition (#908 is open): 'until ... txL within 40 ms with the join timer at 20 cs, when the original bounds return'"),
    f"{S}:2457": (H, "past tense: '6 ms put txL at 53.86 ms; 7 ms was the smallest that held'; 'The slice rule still gave 900 us'"),
    f"{S}:2467": (H, "past tense: 'txL was 49.69 ms at 7 ms'; 'the slice rule still gave 900 us'"),
    f"{S}:2479": (H, "'A TICK at 1x1/1if was then stated at 50 us'; the cut's arm's TICK '50 us by the rule, within' (a measurement)"),
    f"{S}:2489": (X, "'within event.TICK's 50 and 40 us then (55 at 1x1/1if since)'"),
    f"{S}:2498": (H, "past tense: 'ctrl_loop.h stated CTRL_LOOP_SRP_UNIT_US ... at 250 us'"),
    f"{S}:2509": (H, "past tense: 'at the design then built (900 us ...)'"),
    f"{S}:2521": (X, "'44 ms before THE TIERS, so every participant's MRPDU was sent within the 200 ms JoinTime (under THE TIERS the tx row, 33.38 ms within 49 ..., 34 ms, and 99 at two interfaces)'"),
    f"{F}:381": (H, "past tense: 'since at 20 cs, and its 40 ms, txL was over at every pace'"),
    f"{F}:383": (H, "past tense: 'none held it within 40 ms; with ... txL's bound at 50 ms 6 ms held it'; 'With it, a TICK at 50 us ... 8 ms then held txL'; 'was then 132.71 ms ... at the 900 us slice'"),
    f"{F}:415": {1: (O, "the clause's own figure: 'Milan v1.2 4.2.7.1.1, Table 4.3 overrides: JoinTime 200 ms (180 to 240)'"),
                 5: (X, "'(... item 1; 40 ms at the 200 ms default): the armed JoinTime, 190 ms (above)'")},
    f"{F}:426": (O, "50 ms, the head's 49 ms bound plus the 1 ms egress allowance"),
    "README.md:448": (O, "the RTL engine's JOIN_TIME_MS_C, 200 ms, another component"),
    "sw/firmware/ctrl/aecp/aecp_mbx.h:46": (H, "past tense: 'join timer at 20 cs, none did; with it at 19 cs ... 6 ms did'"),
    "sw/firmware/ctrl/loop/ctrl_loop.h:263": (X, "the slice ruling of 2026-11-13's text ('800 us, or the slice rule's choice'), then 'The built slice is the rule's choice ... 950 us'"),
    "sw/firmware/ctrl/srp/README.md:238": (X, "'33.38 ms there at the 950 us slice (33.01 at the 900 us slice under #894's one-row edit cut'"),
    "tb/verilator/ctrl_service_budget/build.py:99": (H, "'as under the 44 ms hold before'"),
    "tb/verilator/ctrl_service_budget/load_grade.py:121": (H, "restatement history: 'the TICK 40 to 45'"),
    "tb/verilator/ctrl_service_budget/load_grade.py:126": (H, "restatement history: 'a TICK at 1x1/1if 45 to 50 us'"),
    "tb/verilator/ctrl_service_budget/load_grade.py:134": (H, "restatement history: 'a TICK at 1x1/1if 50 to 55'"),
    "tb/verilator/ctrl_service_budget/load_grade.py:171": (H, "restatement history: 'at 1,010 and 725 us ... 735'"),
    "tb/verilator/ctrl_service_budget/README.md:624": (H, "the Results section, dated: 'measured on the firmware of dev-soft-core e76a755a' and 'not been measured again at this head'"),
    "tb/verilator/gptp_plane/sim_phc_step.cpp:6": (O, "800 us, a gPTP responder turnaround"),
    f"{MDP}/README.md:1400": (O, "the fabric's MSRP Domain declaration (#860) from 200 ms, a hardware fabric's timing"),
    f"{MDP}/README.md:1469": (O, "the fabric's Domain New at 200 ms"),
    f"{MDP}/twin_compare.py:525": (O, "the fabric's Domain as #860 has it, New at 200 ms"),
    f"{MDP}/twin_grades.py:147": (O, "the clause's own figure: IEEE 802.1Q-2018 Table 10-7 as Milan Table 4.3 sets it, JoinTime 200 ms"),
    f"{MDP}/README.md:1610": (RP, "the SRP transmit check's JoinTime, 200 ms: srptx.hpp's kJoinCs 20, while srp_mbx.c configures CTRL_LOOP_JOIN_CS, 19"),
    f"{MDP}/README.md:1639": (RP, "'not the 200 ms the adapter configures': the adapter configures 190 ms"),
    f"{MDP}/srptx.hpp:82": (RP, "'the adapter's timers (srp_mbx.c): JoinTime 20 cs' and kJoinCs = 20 (:83), against CTRL_LOOP_JOIN_CS 19"),
    # the PR body
    f"{B}:24": (H, "round 12's status bullet, past tense: 'was over its bound at the 900 us slice'"),
    f"{B}:29": (H, "round 17's status bullet: the 176 ms product 'as history'"),
    f"{B}:53": (X, "'Round 16 restates ... at 99 ms, over the tx row's 98.49 (it was 98 ...)'"),
    f"{B}:119": (H, "round 12's section, past tense: 'The load was 0.515 and 0.511'"),
    f"{B}:194": (H, "round 12's section: round 11's build of one, '725 by the rule exactly, moved ... to 69,635' (735 in the table above it)"),
    f"{B}:198": (H, "round 12's section, past tense: 'left the built design: ... 900 us'"),
    f"{B}:202": (H, "round 12's defect, past tense: 'ctrl_loop.h stated CTRL_LOOP_SRP_UNIT_US at 250 us', 'could start with 250 us left'"),
    f"{B}:203": (O, "the check's planted value: 'at 250 it fails with ...'"),
    f"{B}:204": (O, "the planted control's values: 'plants 250 at one interface and 300 at two'"),
    f"{B}:230": (H, "round 13, past tense: 'Two self-test checks anchored on the literal 900u'"),
    f"{B}:249": (O, "a TICK's measurement by the rule against the head's statement: '4,692 (50 of 55)'"),
    f"{B}:295": (X, "14.1's moves table: Old 725, Head 735"),
    f"{B}:296": (X, "14.1's moves table: Old 50, Head 55"),
    f"{B}:297": (X, "14.1's moves table: Old 65, Head 70"),
    f"{B}:298": (X, "14.1's moves table: Old 150, Head 155"),
    f"{B}:299": (X, "14.1's moves table: Old 250, Head 280"),
    f"{B}:301": (X, "14.1's moves table: Old 0.515, 0.511, Head 0.516, 0.512"),
    f"{B}:307": (H, "14.1 quoting :2342: 'the rule picked 900 us then'"),
    f"{B}:310": (X, "14.1: 'the TICK was stated at 50 us then, and is 55'"),
    f"{B}:312": (H, "14.1 quoting the SRP README's history: '33.01 at 900 us ...'"),
    f"{B}:315": (H, "14.1: round 14's grep's token list"),
    f"{B}:317": (H, "14.1: round 14's grep result ('0.515, 0.511 and a LINK at 150 have no hit')"),
    f"{B}:379": (H, "15.1 quoting :2467's past tense"),
    f"{B}:410": (O, "a line reference, aecp_mbx.h:50"),
    f"{B}:417": (H, "16.2 quoting the line tx_statements returned at 6b759b30"),
    f"{B}:424": (H, "16.2 quoting :2351: 'stated as 30 and 98 ms'"),
    f"{B}:425": (H, "16.2: ':2004 and :2521 gave the pre-tiers 44 ms', and at b6f5c638 the 176 ms product (R837-10-F1)"),
    f"{B}:457": (H, "16.5: the comment sweep's token list"),
    f"{B}:482": (H, "17.1 quoting :2004's history"),
    f"{B}:488": (H, "17.2: the statement sweep's token list"),
    f"{B}:489": (H, "17.2: the statement sweep's token list"),
    f"{B}:490": (H, "17.2: the statement sweep's token list"),
    f"{B}:491": (H, "17.2: the statement sweep's token list"),
    f"{B}:492": (H, "17.2: the statement sweep's token list"),
    f"{B}:493": (H, "17.2: the statement sweep's token list"),
    f"{B}:498": (X, "17.2: ':2260 ... gave SRP_JOIN_CS as 200 ms. It is 190 ms at 19 cs'"),
    f"{B}:499": (X, "17.2 quoting :2357: '800 us (950 us at the head)'"),
    f"{B}:500": (H, "17.2 quoting :2377's past tense"),
    f"{B}:501": (X, "17.2 quoting :2442: '50 ms (49 ms since T_egress is counted)', 'then 6 ms (8 ms at the head)'"),
    f"{B}:505": (RP, "17.2: milan_dp's check 'mirrors the adapter's JoinTime as kJoinCs = 20', reported"),
    f"{B}:525": (H, "a round-12 finding row: the completion tick 'within 50 and 40' then; the row notes the TICK's restatement at 55"),
    f"{B}:527": (X, "a round-12 finding row: '70 > 65', '155 > 150', '735 > 725', '55 > 50'; '132.71 > 130 at 900 us ...: round 12's STOP'"),
    f"{B}:529": (H, "the R838-6-F2 row: 'the 900 us figures ... are its history row'"),
    f"{B}:535": (H, "the SRP drain finding row: 'stated 250 us'; the check's planted 250"),
    f"{B}:536": (X, "the TICK finding row: '55 us by the rule, over 50'"),
    f"{B}:539": (H, "a round-13 finding row: 'their two anchors on the literal 900u now read the header'"),
    f"{B}:555": (H, "the R837-8-R2 row: 'the past-tense 900 us paragraph'"),
    f"{B}:559": (O, "a line reference, aecp_mbx.h:50"),
    f"{B}:560": (H, "the R837-9-F2 row: the finding's text, 'states 98 ms at two interfaces under the tx row's 98.49'"),
    f"{B}:563": (H, "a round-16 finding row: 'gave the pre-tiers CTRL_LOOP_TX_MS, 44 ms'; ':2004's derived 176 ms product stayed present tense until round 17'"),
    f"{B}:564": (H, "the R837-10-F1 row: the finding's text"),
    f"{B}:569": (RP, "the milan_dp finding row: 'mirrors the adapter's JoinTime as 20 cs', reported"),
    f"{B}:647": (RP, "Known limitations: milan_dp's check 'still mirrors a 20 cs JoinTime', reported"),
}


def main(path):
    rows, bad, counts, clauses = [], 0, {}, 0
    for line in open(path, encoding="utf-8"):
        lab, loc, k, cite, text = line.rstrip("\n").split("\t", 4)
        c = C.get(loc)
        if isinstance(c, dict):
            c = c.get(int(k))
        if c is None:
            bad += 1
            rows.append(f"UNCLASSIFIED\t{lab}\t{loc} s{k}\t{cite}\t{text[:140]}")
            continue
        counts[c[0]] = counts.get(c[0], 0) + 1
        clauses += cite == "clause"
        rows.append(f"{c[0]}\t{lab}\t{loc} s{k}\t{cite}\t{c[1]}")
    print("# Round 17, R837-10-S2: every superseded statement figure (statement_sweep.py), each hit classified")
    print("# tokens: CTRL_LOOP_TX_MS 44/30/98, CTRL_LOOP_TX_BOUND_MS 40/50, the join timer's 20 cs/200 ms,")
    print("#   CTRL_LOOP_BUILD_ONE_PASS_US 725/430, a TICK's 45/50, AECP's timer slot's 60/65, a LINK's 150,")
    print("#   CTRL_LOOP_SRP_UNIT_US's 250, the slice's 800/900/1,200 us, AECP_PACE_MS's 6/7, the load's 0.515/0.511, each")
    print("#   where its sentence names what the constant states; every derivation one enters, and its result anywhere")
    print("# scope: section 13, FR_NFR 3.4.1, MAILBOX_SPLIT, every tracked README, every comment and docstring under sw/")
    print("#   and tb/, and the PR body; every line, tables included. 'sN' is the sentence index in the line")
    print("# classes: historical, beside (the head's figure beside it), another (another quantity, component or clause's")
    print("#   own figure), reported (a defect found here, for its own Issue)")
    print("# " + ", ".join(f"{k} {v}" for k, v in sorted(counts.items())) +
          f", total {len(rows)} ({clauses} in a sentence citing a clause); current with a superseded figure: 0")
    for r in rows:
        print(r)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

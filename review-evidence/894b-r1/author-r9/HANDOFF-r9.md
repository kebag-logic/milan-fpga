# HANDOFF — lane 894b (8x8/1if follow-up of #894), round 9, [A781]

Status: STOP to the maintainer at `cd7d92ad` (comment text `STOP-COMMENT.md`, posted once on #894 as issuecomment-6917926838): item 3's group
measures costs over their statements at both points, which restated by the rule fail the flip check at both. PR text
`PR-BODY.md`. Nothing pushed; no PR created or edited.

- Start head: acfa5601 (round 8's STOP, #894 issuecomment-6914891355), tree clean, 12:19 CET. Only the session's
  own unit running.
- Assignment: the manager's ruling on round 8's STOP, #894 issuecomment-6914952893 (read in full; saved at the
  scratch's r8/ruling-r9.md), and #665 issuecomment-6907491626 (the dev sync's LeaveAll finding, read with the STOP it
  answers, 6903515775). Items: (1) the six held-egress ledger figures moved to the rule's at the composed measurement,
  service.aecp.last kept at 61.94, the ledger file naming the ruling; (2) R4 by every source at 8x8/1if (20.96 of 20)
  reported, owed to #872, not a STOP; (3) a harness group declaring Talkers beside a Listener Ready at 1x1/1if and
  8x8/1if, a LeaveAll during its held load at 8x8/1if, every row at its bound, statements restated only upward by the
  rule; (4) the CTRL_LOOP_TX_MS keying stands. Then the final gates round 8's STOP left, on a clean clone of the final
  head; one REVIEW READY, or one STOP if a gate fails. Push nothing.

## Items

1. The ledger. — DONE `24753b96`: `egress_ledger.py` states both measurements (`MERGED`, `COMPOSED`) and derives each
   figure from the larger (`MEASURED`), naming #894's ruling of 2026-11-16 on the composition with #901, item 1:
   63.86, 64.10, 64.36, 64.61, 64.86, 62.62 and 61.94 ms, the tool's own output. Section 13's table has both
   measurements; a new self-test check holds them, and a 14th mutant (a figure at the merged image's measurement where
   the composed one is larger) is caught. Round 8's legs graded with the moved ledger: PASS, every row within
   (gate_r8.py).
2. R4. — reported in the PR body and the comment, owed to #872.
3. The group. — `edbd04fe`: `talker_window.held`, `srp-talker-held` in the valid-destinations arm: talker_window's
   declared() (every source's PROBE_TX, its Talker Advertise), then a bridge's Listener Ready for each source's stream
   (a row each), then `save_window.loaded`'s held save (a prelude stands in for its boot), whose held load at 8x8/1if
   spans a LeaveAll run-out as save-held's does (mrpdu_grade's leaveall row); `cd7d92ad` its README. Measured at
   both points (R9-H1, R9-H8 on a clean clone of edbd04fe, the valid-destinations arm, the group alone):
   - 1x1/1if: rc 0, 0 misses, both sources licensed (LICENCE 0x3), the build at most 45,323 cycles (90,000); no
     LeaveAll under its held load at this MAC's phase. By the rule (costs_r5.sh): record.srp 290 and the record's
     apply 285 against 280 (raw within, so no STATED line).
   - 8x8/1if: 0 misses, every row within (SRP's held 10.799 of 20, MRPDU periodic 3.241 and leaveall 1.177 of 49,
     the Talker declarations 189.426 of 220); LICENCE 0x1ff; the build at most 121,848 (147,500); rc 1 on 23 STATED
     lines. The survey: record.srp 42,663 (450 against 365), the record's apply 42,449 (450 against 345), the walk
     11,179 (120 against 55), the base 26,255 (280 against 250), the reclaim 3,292 (35 against 30).
   - The trial restatement (not committed; receipts/model/trial-restatement*): those figures, the SRP unit following
     record.srp (450 and 290, the drain ruling): 8x8/1if's load 0.783 at the pin (FAIL against 0.75), 1x1/1if's last
     queued notice 157.09 ms (FAIL against 140; 136.65 with record.srp at 280).
4. The keying. — stands; no change.
5. The final gates. — NOT RUN, by the STOP; their scripts ready (mkqueueR9.sh, lane_gates_r9.sh, vshard.sh). Quick
   checks on a clean clone of cd7d92ad pass 18 of 18 (receipts/gates/quick-checks-cd7d92ad.txt).
6. STOP posted once on #894.

## Run history (CET)

- 12:19 resume; head acfa5601, tree clean; the ruling and the #665 thread read.
- 12:2x item 1 (egress_ledger.py, section 13, the harness README, FR_NFR); self-test 36 controls x 2, 14 mutants;
  round 8's legs pass at the moved ledger. Item 3's group (talker_window.py, save_window.py, run.py); a dry run builds
  it at 8x8/1if (9 declarations, 9 Listener Readies, the held save of the 13,584 B container). Commits 24753b96,
  edbd04fe.
- 12:26 the group's legs on a clean clone of edbd04fe (launchM.py): R9-H8 at 8x8-1if, R9-H1 at 1x1, the
  valid-destinations variant, the group alone.
- 12:3x the final gates' scripts: lane_gates_r9.sh (round 7's, the diff check against acfa5601 and the comment scan
  over acfa5601..HEAD added), vshard.sh (rtl.yml's verilator shard step run directly: round 6's not_run.json marks its
  suite steps not run, the sweep having stood for them), mkqueueR9.sh.
- 13:19 R9-H1 (1x1) ended rc 0; the licence writes checked (0x1, 0x3). 13:3x the 1x1 receipt; gate_r9.py.
- 14:26 R9-H8 (8x8-1if) ended rc 1, 23 STATED lines; 14:2x its survey (12 statements exceeded, five costs); the
  trial restatement on the working tree: load 0.783 at 8x8/1if (flip FAIL); 1x1/1if's costs (costs_r5.sh: record.srp
  290, apply 285 by the rule), trialled with the SRP unit at 290: 1x1/1if's last queued notice 157.09 ms (flip FAIL),
  136.65 with record.srp at 280. The trial recorded as a patch and its outputs, then the tree restored (clean at
  edbd04fe).
- 14:2x-14:3x the receipts; the full 8x8/1if gate (round 8's legs and R9-H8): FAIL on the group's STATED lines alone;
  quick checks at edbd04fe 18/18; the harness README for the group, commit cd7d92ad; quick checks at cd7d92ad 18/18.
- 14:3x STOP-COMMENT.md, PR-BODY.md, the index; the STOP posted once on #894.
- 14:3x the STOP posted once on #894 (issuecomment-6917926838); the posted text equals the file but for one trailing
  blank line. Nothing pushed; no PR created or edited.

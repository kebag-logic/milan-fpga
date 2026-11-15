[A781] REVIEW READY
Commit: af2c4d7a (lane 894b, PR #914; rounds 5 and 6 on round 4's 98c0b62b: the merges of #902's 234bc149 and 4ae887a1 and nine commits)

Changed:
- **Sync (rounds 5 and 6).** #902's 234bc149 (647d5c4a) and 4ae887a1 (5aadbc8c) are merged.
  - #902's interface-keyed one-interface figures (slice 950, build of one 735, SRP limit 280 us) go to THE SHAPES' 1x1/1if block. 8x8/1if keeps its own slice and builds (1,475 / 1,795 / 1,475 us), which its measurement holds.
  - #902's drain check is read at each point's shape.
- **8x8/1if's own figures, by the rule:**
  - the SRP drain limit, 365 us, the load gate's record.srp there (b2737ba5);
  - its AECP records held at its own statements: the paced class 635 us (an accepted SET_CONFIGURATION, 60,027 cycles) and the largest legal command 1,510 us (1a0fedad);
  - the walk at 55 us and the notice item at 145 (d09494c4).
- **Round 6, item 2 (6bf90e0d).** egress_ledger.py derives the held-egress ledger: the scenario's 60 ms hold, read from scenario.py, plus the service behind it at the merged image's measurement plus 5 %, rounded up to 0.01 ms.
  - The tool's figures: 63.40, 63.64, 63.93, 64.16, 64.41, 62.30, 61.94 ms.
  - Section 13 shows the 716a8ae7 measurement and the merged image's, and attributes the growth to #902's merged code: the bare merge 647d5c4a gives the same figures to the microsecond.
  - A new or larger miss still fails the leg.
- **Round 6, item 4 (f8ea6d72).** 8x8/1if states its own ADP record, 130 us by the rule (12,210 cycles), where 8x8/2if's tsn-c-stack#32 column states 125; 8x8/2if's table is untouched. The load is 0.711 at the pin and 0.673 with tsn-c-stack#32.
- **af2c4d7a.** Four new source-comment lines named a review round, which the final pass's comment scans caught; they now name #894's ledger ruling by its subject and items, and section 13 links it.
- **Round 4's reviews.** RES1 and R844-2-R1 are fixed in wording (a15345f7), and R843-2-S1 is taken (25c782a4: a results directory's run refusals fail the ledger).

Validation (clean clones; receipts and their index in the round 6 packet):
- **Images.** All eight at the head are byte-identical by ELF and loadable sha256 to 5aadbc8c's, which are round 5's measured a15345f7 images, so the 8x8/1if measurement carries. The six fixed images (1x1/1if, 1x1/2if, 8x8/2if) are identical to #902's 4ae887a1's.
- **The 8x8/1if measurement** (a15345f7's image): 114 groups, 1,717 instances, every leg rc 0, no STATED line, no refusal. The transmit-aged control is caught in 8 of 8.
  - The worst measured rows: AECP 4.860, ACMP 7.231, ADP 6.014, MAAP 6.255, SRP 10.474, MRPDU 4.114, the first queued notice 2.812, the last 26.636, the largest command 2.547 ms. Each is within its bound.
  - Joins are 187.397 to 190.147 ms. THE RETRY's 2,453,084 rounds are none over their statement. The slices fit 147,500 cycles.
- **Regraded at the head:** the gate PASS. The seven held-egress rows are under their derived figures by 0.094 to 0.219 ms. The stated-table survey finds 0 statements exceeded, and the record classes PASS at 8x8/1if's statements.
- **Controls:**
  - egress_ledger --selftest: 35 controls in process and as a process, 13 of 13 mutants. One cycle over each restated figure exits 1 naming the row; a new miss exits 1; a figure without its 5 % and a hold not the scenario's are refused.
  - load gate 28 of 28: the own ADP record left out, or stated at 125, is refused by name.
  - record classes 13 of 13.
  - gate_r5 21 of 21.
- **The final pass at af2c4d7a** (each job on its own clean clone):
  - lane gates 65 of 65 as required (both source-comment scans and R844-1's audit 0 lines), each part's clone clean;
  - every hosted job step of rtl-fast, rtl, elaborate and docs: 139 run rc 0, 226 not run with a stated reason, 0 bad;
  - the firmware campaigns: 716 control, 302 AECP and 345 SRP mutants caught, 0 escaped; boundary and firmware-verilator PASS, aecp_wire --every exit 0;
  - the four-shard sweep, each shard on its own picked range: exit 0 each, 65 suites (15, 17, 17, 16), 2,713,040 checks, 0 failures, 0 SKIPPED;
  - counters-f5 rc 0 at both shapes; plat_ledger --self-test PASS at its four points, 7 of 7 controls, 8x8/1if 56 of 56 RAMB36. No image is past its ledger entry, so item 6 has nothing to report.
- **Two restarts in the pass.**
  - The first pass, at f8ea6d72, stopped when lane part a's comment scans found four new source-comment lines naming a review round. af2c4d7a fixes them, and the pass ran again from fresh clones.
  - Its first sweep exited 1: another lane's shared tool directory, first on the sweep's PATH, was absent, so Verilator refused its root. No other job reads that directory. The sweep ran again from a private copy whose files are byte-identical.

Acceptance criteria (the round-6 ruling, issuecomment-6892938049): items 1 to 4 and 6 are met, and item 5's sync, image carry, controls and final pass are done, as the PR body's finding-by-finding table records. Item 5's two delta reviews are the reviewers'. No STOP condition:
- no measured CPU-decided row is over its bound, and the load is 0.711;
- no held-egress row is over its restated figure, and there is no new miss;
- no 1x1 or 8x8/2if image changed;
- the joins, slices and retry rounds are within their statements;
- no donor changed.

Open risks/questions:
- The rows by every source at 8x8/1if stay reported, owed to #872 (round 6, item 1).
- valid-destinations is #895's arm and is not in this tree.
- Mailbox.ARoundFillsWhatItsPassHasLeft at 8x8/1if, and 1x1/1if's SRP record figure, stay for new Issues.
- Two delta reviews from round 4's head 98c0b62b are due (round 6, item 5).
- #902 has posted REVIEW READY at 26898c05 and 41ca9f87 since 4ae887a1; 894-tiers is at 41ca9f87. Its three new commits change comments, docstrings and documents only (aecp_mbx.h's comments, rows_grade.py's docstring, section 13, FR_NFR and the harness README), so no image can move. They are not merged here, as the sync was to 4ae887a1. A merge conflicts in FR_NFR.md and in aecp_mbx.h's comments, so the next sync resolves them.

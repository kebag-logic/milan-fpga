# #977 round 10d handoff

**Status (2026-11-27 19:55 CET): REVIEW READY** at milan-fpga `25ff0632`. The stack is unchanged: tsn-c-stack `5a07d9b7`, lwSRP `e27b34c9`. Nothing is pushed or posted.

- Ruling 7216582862 items 1-4 are committed.
- Item 5 is one droppable commit (`70468e2a`), behind the owner's answer. `git revert 70468e2a` applies cleanly.
- Every group of every arm at both points passes (578 runs, plus 4 pairs) on images byte-identical to the head's.
- Both routes, the firmware gate (4 shards), coverage, the memory gates, the harness self-tests and the docs workflow pass at the head.
- Open for the owner and the reviewers:
  - item 5;
  - whether the post-swap delivering passes are a load term (+0.0136 at the registration rate over the median base, about 0.780 at 8x8/1if);
  - the 8x8/1if platform ledger at 61.0 under the owner's rule of 2026-11-15.

**ETA:** done. The packet is REVIEW-READY.md, PR-BODY.md and receipts/INDEX.md. PR-BODY-tsn.md is unchanged, since the stack did not move.

## Plan

1. Item 1: the alone-record pass statement, per shape, by the rule.
2. Item 2: the 8x8/1if base restated: polls base 350 us, walk 150 us.
3. Item 3: THE SETTLE as a row term, one per opening record.
4. Item 4: a record's pass makes no binding change. This comes with a test, a plant and the new group.
5. Item 5: THE TRANSMIT 77 -> 80 ms at 8x8/1if, behind the owner's decision, with ELF identity checked.
6. The final relearn, then every arm and group at both points, the routes, the gates, flip_grade and load_grade.

## Log
- 12:21 d8e12c16, 7e7f59af, 55bd7f41: items 1-4 committed (alone-record pass per shape: 730 us at 1x1/1if from 69,384 cycles, 1,840 us at 8x8/1if from 174,819; THE SETTLE row term 105 / 415 us; 8x8/1if base 350 us and walk 150 us; deliver() makes no binding change in a pass that carries a record alone, test D6 and plant deliver-binds-in-a-records-pass, 8 of 8 delivery plants refused at 1x1/1if; new group srp-register-both-owed). Model before the relearn: 8x8/1if tx 79.48 ms; 1x1/1if ACMP 29.51, txL 48.08, last 133.91; rows_tiers 1055 of 1055 controls refused.
- 12:21 70468e2a: item 5, CTRL_LOOP_TX_MS 77 -> 80 at 8x8/1if, one droppable commit behind the owner's answer; flip_grade --check --point 8x8/1if passes at 80 against 79.48.
- 12:21 rm (logged before it runs): r10/id/oA, r10/id/oB, r10/id/oC (round 10's pin-identity images, 13.2 GB; the hashes stay in receipts/pins/elf-identity.txt) and r10/maps11 (e62e1936's relearn images, superseded, 4.4 GB), for room on /data (20 GB free).
- 12:23 rm (logged before it runs): r10d/hb and r10d/maps, a build attempt outside the build environment (migen not importable), partial; relaunched under unit5.sh.
  (nothing was there to remove: neither directory had been created)
- 12:34 relearn windows: backlog cut 206,393 PCs (anchor bus 267,563,658); backlog-adp's trace from 267.0M ran out of PCs before its window (anchor 272,796,649, 86,326 PCs), so it runs again from 272.4M into r10d/tr2 (no rm).
- 12:45 c63e9d58: hot list relearned at 70468e2a's 1x1/1if default arm (windows 206,393 / 274,149 / 900,000 / 900,000 PCs; 295 learned, the same five dropped, 290 listed; 72 of 72 maps clean).
- 12:46 started: identity builds elf10d-80 (cF, c63e9d58) and elf10d-77 (c77, c63e9d58 with 70468e2a reverted in the scratch clone); firmware gate shards 0 and 1 (cF); routes10d (both routes at c63e9d58, clean clone r10d/rt).
- 13:00 plat_ledger at c63e9d58: 8x8/1if platform image 147,712 B of rom, 61 RAMB36 over its 60.5 entry (LINK refused); re-ledgered at 61.0 by the owner's rule of 2026-11-15 in 4352900b (sw/litex/ctrl_memory.py is in the harness's firmware trees, so the measurement images are rebuilt there). TX 80 identity at c63e9d58: 80 of 80 hashed ELFs identical, but the 8x8/1if platform ELF was not linked at either, so the identity pair is rebuilt at 4352900b. rm (logged before it runs): r10d/oF and r10d/o77 (the c63e9d58 builds, 8.8 GB; hashes in receipts/r10d/tx80-elf-identity.txt).
- 13:01 firmware gate shard 0 at c63e9d58 FAIL: SrpBinding.D6 at 1x1/2if (CTRL_LOOP_SETTLE_ALONE 0 there: no pass carries a record alone, so the guard does not apply and the test must hold each branch at its shape). Stopped my units elf10d-G and elf10d-77b (the test edit moves tree:firmware again); their partial outputs r10d/oG and r10d/o77b to be removed (logged here before the rm).
- 13:02 e59cf6ea: D6 held per shape (mbx1, mbx2, mbx8 pass; the plant refused at 1x1/1if). Started at e59cf6ea: elfset cH -> oH (80) and c77c -> o77c (77, 70468e2a reverted in the scratch clone); firmware gate shards 0-3 (fwH-*). Stopped fw10d-1 (c63e9d58, superseded).
- 13:15 shard 3 at e59cf6ea REFUSED: binding-refusal-dropped had 0 planting sites. Five SRP plants (binding-refusal-dropped, binding-owed-retry-dropped, r10-transient-refusal-forgotten, feedback-withdrawal-missing, feedback-withdrawal-sink-crossed, binding-park-keeps-old: six names, three needles) planted at lines f6b44e99 (round 10c's delivery bound) rewrote; re-pointed at those lines in 2e466ae9; all 443 SRP defects at one site. Stopped fwH-0..2 (e59cf6ea, superseded).
- 13:16 rm (logged before it runs): r10/maps (ec9dc4be's relearn maps, 4.4 GB), r10/b (ec9dc4be's builds, 2.9 GB), r9 (round 9's scratch, 16 GB; its receipts are in round9/receipts) for room on /data (19 GB free; the pools write about 5 GB). Pools pool10d-pA (32-47) and -pB (48-63), 16 workers each, started on e59cf6ea's images (oH, clone cH) at both points.
- 13:51 gates at 2e466ae9: coverage FAIL (ctrl_app_srp.c lines 142/143, branches 139/140 against the recorded 89/89 and 72/72); test_ctrl_memory FAIL on the ledger's expected 60.5, now fixed in the tree (61.0; passes); ctrl_hot, plat_ledger --self-test, twin pass. Shards 0 and 2 pass. Routes: 1x1/1if at c63e9d58 0 routing errors, WNS +0.159 ns, WHS +0.036 ns, 82 BRAM tiles; 8x8/1if at e59cf6ea 0 routing errors, 100.5 BRAM tiles. Coverage rerun with --keep (cov10d) to find the line.
- 13:53 registering groups (40 of 40 rc 0) on e59cf6ea's images: dearest Talker 17,578 (1x1/1if) and 17,921 (8x8/1if) cycles -> REGISTRATION_US 185 and 190 us; THE SETTLE at most 8,663 and 40,049 cycles -> 1x1/1if keeps the ruling's 105, 8x8/1if 425 by the rule (tx row 79.49 ms); one-record passes 82,462 (1x1/1if, 870 us by the rule, under its 950 us slice) and 171,622 (8x8/1if, within 1,840); load 0.524 and 0.766; post-swap delivering passes at the registration rate +0.0019 over the dearest base before the record, +0.0136 over the median. Committed 4e595c85 (memory gate cases at 61.0) and 25824442 (restatements).
- 14:08 coverage's gap: ctrl_app_srp.c line 169 (bind = n, both owed after a binding change; e62e1936's alternation, never tested). Shard 3 at 2e466ae9: srp-977-deliver-binds-in-a-records-pass escaped at two interfaces (renamed into the one-interface campaigns, 8c30e241) and feedback-withdrawal-missing did not compile (lose unused; planted as false && lose). D7 and plant deliver-both-owed-binds-after-a-change added (8765bfd5f7); 8 of 8 two-interface and 7 of 7 re-pointed one-interface plants refused; mbx1/mbx2/mbx8 pass. Stopped fwI-1 (superseded). Pool pC (0-15) added.
- 14:54 at 8765bfd5: firmware gate shards 0-3 PASS; coverage PASS (40 files); test_ctrl_memory PASS; ctrl_hot --check/--self-test, plat_ledger --self-test, twin PASS. Docs workflow at 235a48c8: 99 of 100 steps, the Python idiom gate's one long line (srp_deliver_mutants.py's docstring) wrapped in dfda4df4. Pools: 58 of 578 groups, all rc 0.
- 15:05 rm RAN BEFORE ITS LOG LINE (a slip, recorded here at once): receipts/r10d/routes/route-8x8-1if-c63e9d58.txt, a copy made a minute earlier into the packet of the c63e9d58 8x8 route's receipt, the route that failed at once for want of its image (plat_ledger refused the link at 60.5). The scratch original r10d/routes/route-8x8-1if-c63e9d58.txt is untouched. Routes: 1x1/1if at c63e9d58 WNS +0.159 ns, WHS +0.036 ns, 0 routing errors, 82 BRAM tiles; 8x8/1if at e59cf6ea WNS +0.092 ns, WHS +0.036 ns, 0 routing errors, 45,672 LUT, 100.5 BRAM tiles; both meet the #818 floor at every corner.
- 15:12 harness self-tests at 8765bfd5 PASS (run.py --self-test 0 failures, kept_grade 33, load_grade 28/28 and --check, flip_grade 628/628 and --check at both points, shape_costs 25/25 and --check). Pool pD (16-31) added: 64 workers.
- 15:13 rm (logged before it runs): r10d/o77c (the 77 build at e59cf6ea, 4.4 GB; its hashes in receipts/r10d/tx80-elf-identity-e59cf6ea.txt).
- 15:23 srp-bound alone refused by kept_grade in its 4 arms (it is graded with srp-kept on one image): the pair runs together per arm into r10d/pair (none and answering-ports at both points).
- 15:34 dcd1dc58: the design paragraph states the tx row (79.49 ms; 79.48 at the ruling's 415 us SETTLE) apart from the figure. git revert 70468e2a applies cleanly at dcd1dc58 in a scratch clone (3 files: ctrl_loop.h, FR_NFR.md, SPLIT_CONTROL_MEMORY.md), so item 5 stays one droppable commit.
- 17:51 rm (logged before it runs): r10d/maps (the relearn's 72 link maps at 70468e2a, 4.4 GB; the filter's result in receipts/r10d/hot/filter-c63e9d58.txt), for room on /data (21 GB free, the pools still writing).
- 18:46 pools DONE: 578 of 578 group runs at both points (289 each), every one rc 0 but srp-kept and srp-bound alone (kept_grade's pairing refusal, 8 runs); the 4 pairs (srp-kept with srp-bound, none and answering-ports at both points) rc 0. Over-statements 0. Longest pass 1.557 ms (1x1/1if, answering-every-port notice-burst-5) and 1.930 ms (8x8/1if, none srp-register-both, 3.5 % under THE SHARE). Heaviest base 19,847/22,500 and 33,565/35,000; walk 3,260/3,500 and 14,108/15,000. One-record passes over every log: 87,826 (1x1/1if, 925 us by the rule, restated in 25ff0632) and 171,622 (8x8/1if, within 1,840). THE SETTLE over every log: 8,663 and 40,049 cycles (95 and 425 us).
- 18:46 rm (logged before it runs): r8 (round 8's scratch, 5.5 GB, superseded; its receipts are in round8/), for room on /data (21 GB free, the final identity build adds 4.4 GB).
- 19:47 at 25ff0632: firmware gate shards 0-3 PASS; coverage PASS (40 files); test_ctrl_memory, plat_ledger --self-test, ctrl_hot --check/--self-test, twin PASS; harness self-tests PASS (run.py --self-test 0 failures; load_grade 28/28, flip_grade 628/628, shape_costs 25/25, kept_grade 33; --check at both points); py and cpp idiom PASS. The head's 80 product ELFs are byte-identical to e59cf6ea's measured images, and plat_ledger PASSes there (8x8/1if 61.0). Docs workflow 100/100 at 25ff0632.
- 19:55 packet written: REVIEW-READY.md, PR-BODY.md, receipts/r10d/*, receipts/INDEX.md (91 files, none over 200 KB, no host paths).

REVIEW READY 25ff0632c4ed312d57cad78783474308c92dd21f stack 5a07d9b7d87298f04b15aa28f0304ec88b0aef81

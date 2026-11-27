# #977 round 11 handoff

**Status (2026-11-27 23:35 CET): REVIEW READY** at milan-fpga `3181a3ec` (round 11b), stack unchanged. Round 11's status follows.
- Round 11b removed `srp_binding.hpp`'s blank line at EOF. It was the builder's step 43 failure and the only `git diff --check` hit over the PR delta.
- Every step of the manager's builder exits 0 at `3181a3ec`. Step 47 leaves gate 11 not run, as on the candidate.
- The 80 product ELFs are byte-identical to `25ff0632`'s.
- `9976b94f` stays the one droppable commit.

**Status (2026-11-27 22:30 CET): REVIEW READY** at milan-fpga `9976b94f`; stack unchanged (tsn-c-stack `5a07d9b7`, lwSRP `e27b34c9`). Nothing is pushed or posted.

- Fixed:
  - R957-2-F1 (option (a): the sourced `deliveries` load term at the median ordinary base);
  - S1 (D8-D10 with 4 plants);
  - R958-2-F1 (the 61.5 threshold);
  - every residue in both reports.
- The 8x8/1if load at the pin is 0.77864, so the 0.78 ceiling is the one droppable commit, `9976b94f`, owner decision pending.
- Every product ELF is byte-identical to `25ff0632`'s (80 of 80), so no arm was re-run.
- At the head:
  - load and flip at both points, the harness self-tests, the idiom gates and the docs workflow pass;
  - the firmware gate (4 shards), coverage and the memory gates pass too.

**ETA:** done. The packet is REVIEW-READY.md, PR-BODY.md and receipts/INDEX.md.

## Log
- 21:07 resumed at 25ff0632 (tree clean, no units running). Read PR #993 comments 7226275798 (R957-2 NEGATIVE) and 7226304210 (R958-2 NEGATIVE).
- 21:11 deliveries measured (tools' deliv11.py over every registering log of both arms at both points, on e59cf6ea's images, whose 80 ELFs equal 25ff0632's). Over the median ordinary base: 11,573 cycles a sink at 8x8/1if (answering-ports swap), 125 us by the rule; 18,076 at 1x1/1if, 190 us. Over the dearest base before the record: 7,236 and 11,930 cycles, 80 and 130 us. Load at the pin: 8x8/1if 0.77864 (0.76614 without the term, 0.77414 at the dearest-before cost); 1x1/1if 0.5321. load_grade --selftest 32 of 32.
- 21:19 committed: 71503e5a (deliveries term), bdf8c0cc (D8-D10 and 4 plants: 3 at two interfaces, 1 in the one-interface campaigns, every one caught), 0acbb717 (61.5 threshold), 8ffdea83 (residues: citations named, 79.49, owner link, B prefixes, review IDs out of the load text), e8618e0c + 9976b94f (the ceiling commit made again without a review label; 9976b94f is the one droppable commit). Started at 9976b94f: elf11 (identity build), gates11, firmware gate shards 0 and 1.
- 21:32 at 9976b94f: 80 of 80 product ELFs byte-identical to 25ff0632's; plat_ledger PASS.
- 22:23 at 9976b94f: firmware gate shards 0-3 PASS; coverage PASS (40 files); test_ctrl_memory, plat_ledger --self-test, ctrl_hot --check/--self-test, twin PASS; harness self-tests PASS (load_grade 32/32, flip_grade 628/628, shape_costs 25/25, kept_grade 33, run.py --self-test 0 failures); idiom gates PASS; docs workflow 100/100. Plants: the 3 deliver-* at 1x1/2if and srp-977-deliver-loss-in-a-records-pass at 1x1/1if and 8x8/1if all caught; 448 SRP defects at one site each.
- 22:30 packet written: REVIEW-READY.md, PR-BODY.md, receipts/ (38 files, none over 200 KB, no host paths); a dated supersession note appended to round10/receipts/INDEX.md (its other bytes kept). No rm this round.

- 22:26 round 11b: the builder's whitespace gate (git diff --check) found srp_binding.hpp's blank line at EOF, the only hit over the PR delta against the merge base 71bad8c0 and against the dev-soft-core tip 0b594023; fixed in 3181a3ec, after the ceiling commit (9976b94f still reverts by git revert alone). Started: every manager-builder.json step in a clean clone at 3181a3ec (builder11, step 43 at this head, step 47 with its record in scratch), and the ELF identity build (elf11b).
- 23:03 builder steps 0-48 at 3181a3ec in a unit with a scratch HOME: every step rc 0, but step 32 (xvlog) SKIPPED and step 47 left 17 gate arms NOT RUN (no xvlog / litex under that HOME); both rerun with the real HOME. rm (logged before it runs): r11/builder-sdk-argv.jsonl (step 47's own record, which it refuses to start over).
- 23:31 steps 32 and 47 again with the real HOME: xvlog gate PASS (through vivado-slot.sh); step 47 "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11's calibration report not on disk, as on the candidate). The ELF identity at 3181a3ec: 80 of 80 identical to 25ff0632's; plat_ledger PASS.
- 23:35 packet refreshed: REVIEW-READY.md, PR-BODY.md, receipts/r11b/ (whitespace, builder steps, step 32/47 logs, identity), receipts/INDEX.md (44 files).

REVIEW READY 3181a3ec372b6473175cc1c842ada8133a96b127 stack 5a07d9b7d87298f04b15aa28f0304ec88b0aef81

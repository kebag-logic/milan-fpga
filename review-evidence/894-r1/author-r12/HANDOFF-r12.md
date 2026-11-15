# HANDOFF — #894 round 12 ([A773], PR #902, branch 894-tiers)

Assignment: #894 issuecomment-6883864236 (round-12 ruling). Round 11's cut, class split (paced edits 260 us at
1x1/1if, 325 at 8x8/2if; every other AECP record 235) and TICK stand. Authority: 6878230332, 6878532871,
6876349104; bounds 6858269025, 6862465874, 6867990126; direct-index ruling 6870437042.

Start: 2026-11-14 21:39 CET, HEAD 9606b3a9 (clean). Round 11 REVIEW READY: issuecomment-6883768027.

## Status

- [x] 1 ATTRIBUTE arm B aecp-fanout SET_CONFIGURATION record + completion tick, 1x1/1if and 8x8/2if, one pass
- [x] 2 CUT once: publish a stream entry only when its index value changes; running() reads only the GSI word it uses
- [x] 3 (paced) record <= 235 at 1x1/1if -> ordinary; else accepted SET_CONFIGURATION stamps the pace (+ planted control)
- [x] 4 completion tick vs event.TICK (restate only by the rule)
- [x] 5 record_classes.py holds arm B SET_CONFIGURATION + SET_STREAM_INFO by class; refuses a pass lacking them
- [x] 6 final pass -> STOP;; section 13, FR_NFR 3.4.1, PR-BODY.md; REVIEW READY or STOP text
- [ ] R837-6 / R838-6 findings (relayed 21:55; PR #902 issuecomment-6884063444 R837-6 NEGATIVE, -6884009601 R838-6
      NEGATIVE; copies in scratch r12/an/R83*.md):
  - [ ] R837-6-F1 MINOR: compare EVERY stated table by the rule over the answering-every-port arm's 1x1/1if legs
        (H-L1N, ...) as well as arm A at the final head; receipt with leg prefixes; restate/rows/pace/slice rule
  - [ ] R838-6-F1 MINOR + R837-6-R2: per-image rom growth (fixture +224, 8x8/2if platform +208 at round 11), no
        universal "220 B"; restate for round 12's images
  - [ ] R838-6-F2 MINOR: section 13 current tier summary R4 (12.85 -> head's) and PR validation load line = head's
  - [ ] R838-6-R1 / R837-6-R1: no round/lane words in source comments (edit_rows.py:3,29; record_classes.py:4-5,72;
        load_grade.py:126,130; poll_grade.py:86,89; new ones); commit IDs (round 9's head = 5b264bf2)
  - [ ] R838-6-R2 / R837-5-R1: SPLIT_CONTROL_MEMORY.md:2493 "The margins at this head" -> "The margins in round 30's
        measurements"; :2484 drop "at this head"
  - [ ] R838-6-R3: PR body/RR "none changes a compiled firmware file" -> "none changes the compiled firmware output,
        as the image/object identity receipts show"
  - [ ] R837-6-S2 (take): record_classes names a record by a response within its own span, else unanswered; control
  - [ ] R837-6-S1 (take): index the packet after sanitizing; indexer fails on a mismatch

## 1. Attribution (done 21:50; receipts/attribution)

Traced on round 11's final-pass arm B builds H-B1F / H-B8F (bc971054 firmware; images identical to 9606b3a9 by
round 11's 332-file identity), aecp-fanout, BUDGET_TRACE_AFTER 83517000 / 97091000. Trace sha256 b1 714a0e32...,
b8 4bd723f9... (scratch r12/trace, 5.8 MB each). Tool: round12/scripts/calltree.py (inclusive call tree), budget.py.

1x1/1if frame 33,724 (6,322 commits / 16,131 short / 8,823 fetch / 2,448 data):
- aecp_command 23,456 incl: aecp_note 8,376 (face changed -> publish 6,696: write_stream 2,020, current() 2,019,
  write_settings/commit ~600, nvm_changed 484), running x4 6,618 (aecp_stream_read -> ctrl_app_aecp:stream:
  acmp_view 1,993, b_stream 689, memsets ~1,700, aecp_find 361), self 6,198 (any_running + ENTITY scans over every
  descriptor), aecp_keep 1,182 (memcpy), lock/override/put ~900.
- rest of the frame: aecp_rx 3,828 self, transmit 2,119 (the SUCCESS response, in the frame), arm 1,158, header 888,
  applied 708, owe 563.
8x8/2if frame 78,332 (17,729 / 37,812 / 7,322 / 15,469): aecp_note 27,666 (publish 25,243: write_stream 12,929,
current() 4,323, interface_of 2,653), running 22,704 (acmp_view 6,917, b_stream 2,861, memsets 4,896), self ~18,700.

KEY FACTS:
- arm B's stream port is the harness's b_stream (build.py VARIANTS answering-ports: memset, return true): NO GSI
  window read is in the measured record. The product's running() reads 6 GSI words a stream (aecp_face.c stream).
- The completion: in arm B the accepted SET_CONFIGURATION never waits at either point: the face commit is
  acknowledged inside the port, the frame answers SUCCESS (1x1: in the frame; 8x8: in the next poll), no
  IN_PROGRESS on the wire. The poll after the frame fans out the notice: 1x1 aecp_mbx:poll 20,631 (owed_drain ->
  fan_out 16 recipients 17,894), deliver 4,124 (nvm mark 1,885, publish_store 1,421, face_poll 212: nothing owed);
  8x8 poll 28,308 (response + 32 recipients 24,871), deliver 5,140, then a centisecond dispatch_ticks 6,941 (SRP
  timer tick, unrelated). No republication occurs after the frame in arm B.

## 2. Cut (done 22:00, f275b619; measured once on r12/cut-wt, arm B aecp-fanout)

| point | SET_CONFIGURATION before | after the cut | rule | SET_STREAM_INFO after |
|---|---:|---:|---:|---:|
| 1x1/1if | 33,724 | 28,509 | 300 us (> 235) | 20,068 |
| 8x8/2if | 78,332 | 55,377 | 585 us | 18,373 |
Arm B's records are b_stream's (no window read), so the one-word running check moves arm B by layout only; the
product's check reads 1 GSI word a stream instead of 6. -> step 3: accepted SET_CONFIGURATION stamps THE PACE
(fe0cef5b). Images (r12/scripts/qall.sh): every image +216 B rom vs 9606b3a9 (1x1/1if fixture +224), within caps;
8x8/2if platform 130,920 of 131,072 (152 B spare), fixture 1x1/1if 111,024 (41.0).

## Commits (round 12)
1. f275b619 firmware cut + 4 tests (Core.TheRunningCheckObservesEveryStreamBriefly,
   Core.AConfigurationChangeNamesWhetherItsIndexMoved, Face.TheRunningCheckReadsOneWindowWordAStream,
   Face.OnlyAMovedConfigurationIndexWritesTheStreamEntries)
2. fe0cef5b pace stamp (aecp_commands.c configuration(), accepted branch) + Mailbox.AnAcceptedConfigurationHolds-
   TheNextRecordForThePace + receive()/latency tests given the pace after an accepted SET_CONFIGURATION + rows
3. 1c8c071b rows moved to aecp_configuration_mutants.py (py idiom long module 11 > 10 at fe0cef5b)
4. 30a01422 graders' comments: no round/lane words (R838-6-R1 / R837-6-R1)
FIRMWARE FROZEN at fe0cef5b. DO NOT edit sw/firmware/** (except test tables) after it, or the final-pass builds
are stale.

## Final pass (started 22:25 at 30a01422, clone r12/fp-wt)
- arm A: r12-A-p1 (64-71, picked), r12-A-p2 (72-79, picked), build r12/gates-out/builds/A
- every-port arm 1x1 all 16 groups: r12-E1 (104-111; 88-95 collided with 894b's H-L1O, stopped and moved)
- 12 legs r12/gates-out/queue-legs.txt via r12-dispatch on 112-127 MAX 4 (H-B1F now aecp-fanout,aecp,
  aecp-largest-notice)

## Model at e4d80a8a (paced class 300 / 595)
- edit_rows.PACED {1x1: edit 260, SET_CONFIGURATION 300; 8x8: 325, 595}; EDIT_RECORD_US = max; control 2 "an unpaced
  SET_CONFIGURATION charged as ordinary" (class = edits' alone -> 'an accepted SET_CONFIGURATION charged below its
  record', ACMP row shortens). rows_tiers selftest 1033/1033, load 25/25, flip 585/585, record classes 11/11.
- 1x1/1if rows: R4 13.01 R5 73.80 R6 69.60 first 14.59 last 127.86 R4L 188.41 ACMP 28.80 ADP 27.17 MAAP 27.29
  tx 33.21 (<= CTRL_LOOP_TX_MS 34) txL 48.23; load 0.515/0.511; tier_grid CHOSEN built (900, aecp-first, srp-first,
  queue, cap 2, +0.0157); pace choice 8.
- 8x8/2if reported: R4 44.24 R5 206.45 R6 196.31 first 20.93 last 806.60 R4L 195.76 ACMP 67.94 ADP 68.08 MAAP 69.13
  tx 98.49 txL 459.40, load 0.794/0.754.
- Completion tick (step 4): arm B never waits (commit acked in the port); window TICK precedes the command: 1x1
  2,159 (25 us), 8x8 2,404 (30 us) <= event.TICK 50/40: no restatement. The late-ack completion (owed -> whole
  republish) is staged by no arm: open risk.
- record_classes on H-B1F/H-B8F: SET_CONFIGURATION paced 28,376 (300/300), 56,474 (595/595); SET_STREAM_INFO held
  other 19,925 (210/235), 19,080 (205/265).

## Final pass state (23:15)
- 12 legs done 23:05: B1F B8F L8A L8N L8L L8O C-R1 rc 0; 81L 81A 81N J8 J81 rc 1 = round 11's (8x8-1if STATED/40-notice
  RuntimeError; #910 build of one at 8x8 srp).
- 8x8/2if compare (r12/an/final/compare-8x8.txt; point-aware round12/scripts/aecp_records.py, AECP_RECORDS_POINT):
  only #910 build_one 145,595 (1,530 vs 1,215), the largest legal notice 61,749 (650, held to LONG_NOTICE_US 655),
  and the paced SET_CONFIGURATION 56,474 (595 vs 265; held at the paced class 595).
- fw_coverage --check PASS at e4d80a8a (r12-cov, clone r12/cov-wt).
- 94e828ed docs commit (section 13 subsection "SET_CONFIGURATION's record", rows, images per image, R2/F2 fixes,
  FR_NFR, READMEs). docs_check 0, em_dash 0.
- Early gates at 94e828ed (firmware jobs, rtl-a/b, elab, lane b/c): r12-dispatch-early on 112-127 MAX 3,
  r12/gates-out/queue-early.txt, wf dir r12/gates-out/wf-94e828ed, lane dir lane-94e828ed. They read neither the
  budget harness's tables nor docs, so they carry to a later head that changes only those (state it).
- Pending: arm A (~00:30), E1, then finish.sh (1x1 compare over A + E1 + B1F), restate if over, regrade on fp-wt with
  the later tb/ diff, record_classes over every leg, lane-a + rtl-fast + docs jobs + sweep at the final head.

## R837-6-F1 result so far (23:20)
- E1 (every-port arm, 16 groups, 1x1/1if, rc 0; joins 188.071-189.937) + B1F compare (r12/an/pre1): event.AECP
  (AECP's timer slot) 6,206 cycles = 70 us by the rule > 65 stated, in 7 of 16 groups (notice-burst-5..7,
  notice-every-5..7); notice-every-0 (round 11's only H-L1N group) < 5,500. At 9606b3a9 (r12/builds/E1-head, clone
  r12/img-wt): notice-every-5 5,329, notice-burst-5 5,753 (65). Traced: same work (1,024 vs 1,030 commits), fetch
  stalls +479 -> layout of the cut's code. RESTATE event.AECP 1x1/1if 65 -> 70 both columns (load_grade.py, edited,
  NOT yet committed). Rows then: R4 13.04 R5 73.91 R6 69.72 first 14.60 last 127.98 R4L 188.42 ACMP 28.88 ADP 27.23
  MAAP 27.35 tx 33.30 txL 48.35; load 0.515/0.511; pace 8; tier_grid built chosen, 14 of 420 hold (+0.0133).
- Sweep: no pick range freed 23:43-23:53 -> after arm A: 64-71, 72-79 (arm A's) + 112-127 (when its 3 jobs end).
  Early queue rest moved to r12-dispatch-early2 on 96-111 MAX 2 (queue-early-rest.txt).

## Final pass 1 result (00:57-01:30) and the STOP it found (NOT posted)
- Arm A (fw fe0cef5b, clone fp-wt 30a01422): 96 groups, 0 refusals, 7 held-egress misses, 0 of 140,035 over share,
  joins 187.994-190.021. E1 16 groups rc 0. 12 legs as round 11. Merge regraded at 30a01422 (rc 0).
- 1x1 compare (A1/A2/E1/B1F) at the tree's statements: over by the rule: event.AECP 6,206 (70 > 65, E1),
  event.LINK 14,715 (155 > 150, A2/fixture; 13,956 at round 11), build_one 69,635 (735 > 725, A2/srp; 68,972 at
  round 11). Restated in 21aeb997 (ctrl_loop.h CTRL_LOOP_BUILD_ONE_PASS_US 735 (static assert only; 332/332 images
  identical 30a01422/94e828ed/21aeb997), load_grade donor build_one/item.mrpdu 735, poll_grade mrpdu 735,
  rows_grade ROW_COSTS LINK 155, load_grade event.AECP 70 both columns).
- => last queued notice 132.64 > 130 (70 passes; 127.98 without the build-one restatement); tier_grid chooses slice
  950 (12 of 420 hold) = STOP (ruling's STOP 1 + R837-6-F1's slice rule). STOP-COMMENT.md drafted, NOT POSTED.
- Early gates at 94e828ed: 53 wf steps rc 0 (AECP campaign 299/299, fw-unit coverage PASS), lane b/c rc 0.
  Sweep at 94e828ed stopped at 01:3x (firmware changes below; it does not count).

## NEW ITEM (relay #894 issuecomment-6886633874; #895 issuecomment-6886630886 item 8), 01:32
- ctrl_loop.h CTRL_LOOP_SRP_UNIT_US 250 -> 280 at 1if (365 at 2if unchanged) (1c0ca94b): the SRP drain limit
  (ctrl_loop.c:322 start + SLICE - SRP_UNIT) at load_grade's record.srp (max of both columns). load_grade.srp_unit()
  in findings (--check refuses: '1x1/1if: ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US 250 us, not the load gate's
  record.srp 280 us', shown at 250), control "the SRP drain's record cost not the load gate's" (plants 250 at 1if
  and 300 at 2if; srp_unit_controls(), a47cd3f2 after the long-function ratchet refused controls()). load 26/26.
  Loop arm 51 tests pass (L23 symbolic). loop_step_mutants 'drain-past-its-time' text unchanged.
- Images: only the 4 1if images' ctrl_loop.o/ELF/bin differ (sizes equal); 2if images identical -> 8x8/2if legs
  carry. FINAL PASS 2 at a47cd3f2 (clone r12/fp2-wt, builds r12/gates-out/builds2): r12-A2-p1 96-103, r12-A2-p2
  104-111, r12-E2 112-119, r12-dispatch-legs2 120-127 (B1F, C-R1, 81L, 81A, 81N, J81). Sweep via
  r12-sweep-launch (waits for 4 free 8-ranges, 3 h limit) at a47cd3f2, out r12/gates-out/sweep2.
- TODO after: compare 1x1 (finish over builds2), restate by the rule, rows/pace/grid; fw jobs at a47cd3f2;
  lane a + rtl-fast + docs at the final head; section 13 + PR-BODY rows for this item; STOP or REVIEW READY.

## FINAL (05:2x): STOP, head 783b1596d4acb431698c6e5da9d3f4506cfc091e (12 commits on 9606b3a9; nothing pushed)
- Pass 2 at a47cd3f2 (firmware final): arm A 96 groups, 0 refusals, 7 held-egress misses, 0 of 139,988 over share;
  E1(E2) 16 groups rc 0; B1F/C-R1 rc 0; 81L/81A/81N/J81 rc 1 (round 11's); 8x8/2if legs carried (2if images
  identical). Fw jobs 22 steps rc 0 (AECP 299/299, control 716/716, coverage PASS). Sweep (r12b shards on picked
  0-7, 8-15, 32-39, 40-47) rc 0 each.
- NOTE: the srp group's log is byte-identical at fe0cef5b and a47cd3f2: build of one 69,635 stands (an early read of
  41,913 was a partial log; nowhere in the packet).
- Compare at a47cd3f2 statements: the TICK 4,784 (55 > 50) new -> restated 3909588f. At 3909588f's statements only
  class lines remain (receipts/final2/compare/compare-1x1-at-99626ee4-statements.txt).
- Rows at 3909588f: R4 13.05 R5 74.02 R6 69.81 first 14.61 LAST 132.71 (>130, 70 passes) R4L 188.43 ACMP 28.90
  ADP 27.25 MAAP 27.37 tx 33.33 txL 48.38; load 0.516/0.512; pace 8; tier_grid 10 of 420, CHOSEN 950 (+0.0116).
  Counterfactuals: build_one 725 + TICK 55 -> 132.65; build_one 735 + TICK 50 -> 132.64; both old -> 127.98.
- Docs 99626ee4 + 783b1596 (section 13 rows/history row/subsections "The SRP drain's record cost", "The final
  pass's restatements"; FR_NFR 3.4.1). docs_check 0, em_dash 0.
- Self-tests at 3909588f: rows_tiers 1032/1033, flip 584/585 (consistency controls the over row defeats), load
  26/26, record classes 11/11.
- STOP POSTED 2026-11-15 05:3x CET: #894 issuecomment-6888749411 (exactly one [A773] comment this round; body =
  STOP-COMMENT.md). Nothing pushed.
- Outputs: STOP-COMMENT.md (posted), PR-BODY.md, receipts/ (attribution, images, model, classes,
  final (pass 1 + 8x8), final2 (pass 2), cut, e1-9606b3a9), INDEX.md.

## Changes (file:line, reason)

## New checks (planted mutant, failing words)

13 rows (aecp_configuration_mutants.py), all caught by name (r12/rows1, rows2), + face-write-after-response re-anchored
(new text keeps `every` referenced: the first version escaped on an unused-variable build refusal):
| row | plant | test | words |
|---|---|---|---|
| running-reads-every-word | sel < 7 | Face.TheRunningCheckReadsOneWindowWordAStream | one word a stream, selector 0 |
| running-reads-no-word | brief reads 0 | same + Face.StreamAvbAndFormat... | status for command 6 / 8 |
| running-reads-another-word | brief reads sel 2 | same | one word a stream, selector 0 |
| running-check-blind-to-the-licence | !brief && licensed | same + StreamAvb... | status for command 6 / 8 |
| running-check-reads-whole | .brief = false | Core.TheRunningCheckObserves... + Face | SET_CONFIGURATION observes every stream, briefly |
| stream-read-brief | aecp_stream_read sets brief | Core + Face | GET_STREAM_INFO reads the stream whole / its six |
| configuration-streams-every-time | every = CONFIGURATION | Face.OnlyAMoved... | the index in force writes no stream entry |
| configuration-streams-never | every = false | Face.OnlyAMoved... | a moved index writes the stream entries |
| configuration-move-unnamed | note(.., 0, 0) | Core.AConfigurationChange... + Face | Changed(AECP_CHANGE_CONFIGURATION,0,1) |
| configuration-move-always-named | note(.., 0, 1u) | Core + Face | Changed(AECP_CHANGE_CONFIGURATION,0,0) |
| configuration-moved-by-its-override | moved = !overridden | Core + Face | Changed(AECP_CHANGE_CONFIGURATION,0,0) |
| configuration-unpaced | stamp removed | Mailbox.AnAcceptedConfiguration... | held 1 ms after the accepted SET_CONFIGURATION |
| configuration-paced-when-refused | stamp before any_running | Mailbox.AnAcceptedConfiguration... | a refused SET_CONFIGURATION holds nothing |

## Gate table

## Notes for a successor

- Scratch: $SCRATCH/r12/

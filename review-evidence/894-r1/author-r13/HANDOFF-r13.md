# HANDOFF — #894 round 13 ([A773], PR #902, branch 894-tiers)

Assignment: #894 issuecomment-6888782796 (ruling on round 12's STOP issuecomment-6888749411). Overrides round 12's
stop list. Start 2026-11-15 04:50 CET at local head 783b1596 (clean, not pushed; 12 commits on 9606b3a9).
The manager pushes; I do not. End: one REVIEW READY (short commit IDs only) or a STOP per the ruling's list.

## Items
- [x] 1 slice = the slice rule's choice within 650-1,100 us at one interface (950 now), own commit, ctrl_loop.h
      states the rule, held by the self-tests (no hand-picked number); CTRL_LOOP_BUILD_MOST at 950 stated
- [x] 3 reruns on rebuilt images: every 1if leg (arm A, every-port, answering-ports, 8x8/1if legs), compare, pace and
      slice rules, firmware jobs, sweep, every gate on a clean clone of the final head (incl. round 12's leftovers)
- [x] 4 carries: 8x8/2if legs by 2if image hashes; anything else only with an input-identity proof
- [x] 5 (shown, not staged) a late-acknowledged SET_CONFIGURATION's completion staged in one group at each point, held by the rule
- [x] PR-BODY.md (rounds 12 and 13, finding table), receipts, INDEX after sanitizing; REVIEW READY or STOP

STOP (maintainer): a 1x1/1if row over its bound or load > 0.70 at the rule's slice; the rule's choice moving again on a
rebuilt image; no pace up to 11 ms; a join outside 181-239; an image over its cap; item 5's cost putting a row over.

## Log
- 04:5x c274b9f5 slice 950 (ctrl_loop.h states the rule: ruled() = the slice rule's choice in 650-1,100 us at one
  interface; rows_tiers control and selftest_round now read the header / ruled(), no 900 literal). Model at 950 with
  round 12's costs: R4 13.10 R5 74.07 R6 69.86 first 14.66 last 127.21 R4L 188.48 ACMP 28.95 ADP 27.30 MAAP 27.42
  tx 33.38 txL 48.43; load 0.516/0.512; tier_grid CHOSEN 950 = built (10 of 420, +0.0116); pace 8.
  CTRL_LOOP_BUILD_MOST stays 1 (950 < CTRL_LOOP_BUILD_PASS_US 1,010): no row change from it.
  Self-tests rows_tiers 1033/1033, flip 585/585, load 26/26, classes 11/11, slice_checks 10/10; loop arm 51, AECP
  mailbox arm 124. Images: only the 4 1if images' ctrl_loop.o/ELF/bin differ, sizes equal; 2if identical.
- Item 5: shown, not staged: receipts/item5-no-late-completion.md (contract 64 cycles; KL_mbx_cdc takes on the
  pulse unconditionally; sim_split [FACE] 2 polls; mbx_face_commit outwaits; no owed; applied true; no wait).
- 04:56 reruns at c274b9f5 (clone r13/fp-wt, builds r13/gates-out/builds): arm A in 4 quarters r13-A-q1..q4 on
  0-7/8-15/16-23/24-31; r13-E1 32-39; r13-dispatch-legs 40-47 (B1F, C-R1, 81L, 81A, 81N, J81); r13-dispatch-fw
  48-63 (W-fw-*, wf dir r13/gates-out/wf-c274b9f5; early check, rerun at the final head).
- 06:14 arm A at c274b9f5: q1-q4 96 groups, 0 refusals, 7 misses (q4), 0 of 140,032 over share; E1 rc 0; B1F, C-R1
  rc 0; 81L/81A/81N/J81 rc 1 (8x8/1if states 1x1/1if's costs: build-one 92-94k vs 73,500, polls base 20,580 vs
  20,500; the 40-notice RuntimeError); 8x8/2if legs rerun: B8F L8A L8N L8L L8O rc 0, J8 rc 1 (#910). 8x8/2if harness
  ELFs identical to round 12's (receipts/images/harness-elf-sha256.txt). Joins arm A 187.994-190.021, all 185.486-190.147.
- 1x1 compare (A1..A4, E1, B1F) at the head's statements: only class lines; NO restatement. TICK 4,692 (50 <= 55).
- Fw jobs at c274b9f5: 22 steps rc 0, AECP 299/299, control 716/716, coverage PASS.
- ed0df35b docs (section 13 rows + history + ruling text, FR_NFR, MAILBOX_SPLIT 0.95 ms, harness/SRP READMEs).
  FINAL HEAD ed0df35b; only 5 .md files after c274b9f5.
- Model at ed0df35b: flip 1x1 rc 0 (R4 13.10 R5 74.07 R6 69.86 first 14.66 last 127.21 R4L 188.48 ACMP 28.95
  ADP 27.30 MAAP 27.42 tx 33.38 txL 48.43), load 0.516/0.512, grid 950 = built, pace 8, self-tests 1033/585/26/11.
  record_classes over every r13 leg PASS. 8x8 compare: #910 + class lines.
- 06:23 final gate pass at ed0df35b: sweep r13 shards 0-7/8-15/16-23/24-31; r13f-dispatch-a 32-63 and -b 64-95
  (MAX 4 each) over queue-final (lane a/b/c, every W-* job), dispatch log r13/gates-out/dispatch-final.txt.
- 06:47 lane a at ed0df35b: hooks_selftest 27/28 ('the plants apply': hooks.py:204 anchored on the publish line round
  12's cut rewrote). Fixed 234bc149 (anchor = new line; replacement keeps `every` referenced). hooks self-test 28/28,
  96/96. No workflow/sweep reads ctrl_service_hooks (grep): carry the ed0df35b jobs by input identity.
- Gate pass: lane a at 234bc149 48 gates (4 by design); lane b/c at ed0df35b rc 0; verify_wf combined over
  ed0df35b (fw/RTL/elab) + 234bc149 (rtl-fast others, boundary, docs): 139 ran rc 0, 226 not run, 0 bad; AECP
  299/299, control 716/716, coverage PASS; sweep at ed0df35b 4 shards (0-7, 8-15, 16-23, 24-31) rc 0; milan_dp
  [FACE] 2 polls. FINAL HEAD 234bc149 (15 commits on 9606b3a9; not pushed).
- Outputs: PR-BODY.md (rounds 12+13, finding table), REVIEW-READY-COMMENT.md (short IDs only), receipts/, scripts/,
  INDEX.md. REVIEW READY: to post once on #894.
- REVIEW READY POSTED: #894 issuecomment-6890460677 (exactly one [A773] comment in round 13; body = REVIEW-READY-COMMENT.md).

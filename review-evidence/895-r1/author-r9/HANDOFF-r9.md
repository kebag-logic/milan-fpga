# HANDOFF — lane 895 ([A775]), round 9

**Status (20:2x CET 2026-11-15): REVIEW READY at `056d619d` (local, not pushed), posted once on #895 as issuecomment-6899637516 (REVIEW-READY-COMMENT.md; the posted body checked identical but a trailing blank line).** The full pass at the final head is green; #902 merged into `dev-soft-core` (`659d7687`, its tree `07ed787e`'s, which `056d619d` contains) during the round.

Assignment: #895 issuecomment-6895331865 (the ruling on round 8's STOP, issuecomment-6895274375), read in full, and the
manager's relay notes. Start: `f93317cb`, clean.

## Items

| Ruling item | What | Status | Commit | Receipt |
|---|---|---|---|---|
| 1, 2, 4 | `CTRL_LOOP_TX_MS` at two interfaces 99 -> 105, `SRP_REDECLARE_CS` there 2,029 -> 2,030 cs; own commit with FR_NFR 3.4.1, section 13, the SRP README; #902 keeps 99 | done | `845364b6` | graders/g-item1 |
| 5 | by hash: no one-interface image changes; the two-interface images differ only in that constant | done: 0 one-interface files differ; 12 two-interface files (6 images' `srp_mbx.o` and ELF), each one instruction `li a3,2029` -> `li a3,2030`, 0 other differing lines (`objdump -d`, `objdump -s`) | | identity/compare-merge-head.txt |
| 5 | rerun the two-interface Talker arms | done: srp_talker if2 8x8 11, if1 1x1 11, SrpGate 8x8/2if 7, srp-acmp if2 1x1 76; all PASS | | arms/ |
| 5 | rerun the 8x8/2if valid-destinations leg | done: R9-W8 rc 0, 2 groups, 0 refusals, 0 misses, 0 of 3,052 over the share, 49 joins 185.605 to 190.228; both groups' measured logs byte-identical to R8-W8's | | legs/ |
| 5 | sync onto #902's current head, image identity | done twice: `41ca9f87` (3 conflict hunks in section 13, word-merged; 552 of 552 image files identical to 73388996's, the legs' image) and, as #902 moved during the round, `07ed787e` (docs only, sections 5 and 13; 2 hunks: one by hand, this branch's own sizes where #902 states its head's, one word-merged); the final head's 552 image files identical to 449d29d2's | `663b519b`, `056d619d` | identity/, merge/ |
| 5 | one full pass on a clean clone | pass 1 at `c772b1e5` found one failure, the harness self-test (2 checks pinning the queued bound at 130 ms, stale since round 8's `2b7f8428`); fixed in `249a3823`; **pass 2 at the final head `056d619d`: green** (hosted steps 139 ran / 226 reasoned / 0 bad; campaigns 716/716, AECP 299, SRP 415 rows (70 talker-), 0 escaped; fw_coverage PASS; lane gates rc 0 but the two flip checks by design, harness_selftest 0 failures; sweep 65 suites 0 failed, 2,713,040 checks, field 164 + 675; graders: flip 1x1 PASS, rows_tiers 1033/1033, tier_grid 6 of 420 CHOSEN 900, load 0.517/0.514; plat_ledger rc 0, images 552/552 = 449d29d2's) | `249a3823` | pass1-c772b1e5/, gates/, sweep/, graders/g-final, ledger-final |
| relay | the 1x1/1if per-pass headroom and every row's margin | done: 260 us now, holds to 278, fails at 279 (last 141.36, txL 49.02) | | graders/per-pass-threshold.txt |

Found on the way (own lane's defect, fixed): `plat_ledger.py` refused `ctrl_plat` at 8x8 with one interface since round
7B's cut `f14e56a9` (18,240 B in the image, 18,176 in `ctrl_memory_ledger.PLAT_8X8_1`): the cut's `gate_seen` and
`gate_base` add 64 B there and take the padding at the other three points. Rounds 7B and 8 reported the sizes but not
that FAIL; round 8's PR-BODY.md said "plat_ledger.py PASS", which was wrong. `449d29d2` records 18,240; plat_ledger.py
rc 0 at the head (ledger-head), `test_ctrl_memory.py` PASS. No image changes (only test_ctrl_memory.py and
plat_ledger.py read the record).

## Commits (on `f93317cb`)

| Commit | What |
|---|---|
| `663b519b` | Merge #902's `41ca9f87` (#894 round 20: section 13's history in the past, `aecp_mbx.h` comments, `rows_grade.py`'s docstring, FR_NFR, harness README). Section 13's three conflict hunks resolved word by word against the base: #902's changes applied wherever this branch left those words unchanged (round9/scripts/merge_words.py; replay byte-identical to the commit). |
| `845364b6` | Item 1: `ctrl_loop.h` `CTRL_LOOP_TX_MS (34u : 105u)` and its comment; `flip_grade.py` and `rows_tiers.py` self-test controls' literals (the figure 105, the plants 33/104 under each row); `srp_talker.cpp` comment (20,300 ms at two); FR_NFR 3.4.1 (415), section 13 (the tx paragraph, the round-8 bullet in the past, the closing line, the new subsection "THE TRANSMIT's figure at two interfaces (#895)"), SRP README (the hold-off's terms with both figures), harness README (188). |
| `449d29d2` | `ctrl_memory_ledger.PLAT_8X8_1` 18,176 -> 18,240; section 3's ctrl_plat sentence. |
| `c772b1e5` | Section 13: the images by hash, the sync's, the Talker arms, the rows and the ledger. |
| `249a3823` | `selftest_notice.py`: the queued bound's pin (140, 62) and its over-bound probe 141 ms (was 130 and 131); `ctrl_loop.h`'s comment of the bound (130 -> 140), lines kept. |
| `056d619d` | Merge #902's `07ed787e` (#894 round 20: sections 5 and 13's image sizes as its head's), docs only. |

## Run history

- 14:53 relay read; ruling 6895331865 fetched (round9/ruling-6895331865.md). HEAD f93317cb, clean, no units.
- 14:5x fetch: origin/894-tiers 41ca9f87 (6 commits since b6f5c638; code files: aecp_mbx.h comment, rows_grade.py
  docstring). Merge: section 13 conflicted in 3 hunks; word-merged; `663b519b`.
- 15:0x item 1 edits (round9/scripts/item1_r9.py; its final anchor assert failed first, the section inserted at the
  unique anchor after). Worktree: flip 1x1 PASS, rows_tiers self-test 1033/1033, flip self-test 585/585, docs and
  idiom checks rc 0; tx_statements []. `845364b6`.
- 15:0x the plat_ledger finding traced to 7B's cut (round7/receipts/7B/ledger-merge PASS, ledger-cut FAIL); `449d29d2`.
- 15:05 clean clones r9/M (663b519b) and r9/L (449d29d2); ledger units (48-55 and the pool): rc 0 both;
  plat_ledger rc 1 at the merge (the finding), rc 0 at the head.
- 15:09 leg R9-W8 started with point `8x8/2if`: run.py takes `8x8` (rc 2 at once, incident/); restarted 15:12 on 48-55.
- 15:1x image_sha.py and compare_images.py: r8's 73388996 = merge (0 differ); merge -> head 12 two-interface files,
  each one instruction.
- 15:13 arms-talker on 56-63: PASS. Per-pass threshold on an export of the head: as round 8.
- 15:14 `c772b1e5`. Pre-check of the 27 check_*.py scripts the workflows name: rc 0 (em-dash with the gate venv).
- 15:17 the gate queue (18 units, gate_queue.sh) started via disp_once.py, at most 4 at once.
- 15:34 the sweep's per-shard starter (sweep_shard.py): its first two starts failed at once (the runner path one
  directory off; sweep/failed-start); fixed; shard 0 on 32-39 at 15:46.
- 15:2x removed round 5's sweep clones $LANES/895r5sweep-shard{0..3} (9.7 GB).
- 15:3x-17:40 pass 1 at `c772b1e5`: hosted steps 139 ran, 226 not run with a reason, 0 bad; campaigns control 716/716,
  AECP 299 rows ok, SRP 415 rows ok (70 talker-), 0 escaped; firmware coverage PASS; sweep 65 suites (15 + 17 + 17 +
  16), 0 failed, 2,713,040 checks, tsn_fuzz's field campaigns 164 and 675 pass (TSN_GEN_ROOT in the spec's env; the
  two TEST_RESULTS.md date stamps restored in shard 3's clone); lane gates all rc 0 but flip_check and flip_check_8x8
  (by design) and **harness_selftest rc 1: 2 failures**, `selftest_notice.queue_checks` pinning the bound at (130,
  62) and its 131 ms probe a miss, stale since round 8's bound commit (round 8 ran no gate).
- 16:3x R9-W8 rc 0, identical to R8-W8's measured logs.
- 17:0x a release hold (894c) collecting CPUs: pick8 none by design; lane-a, W-docs-a and lane-c on the session pool,
  at most two (pool_start.py).
- 17:4x `249a3823` (the self-test fix); #902 had moved to `07ed787e` (docs only): merged, `056d619d`, the final head.
  ledger-final at it: plat_ledger rc 0; 552 of 552 image files identical to 449d29d2's.
- 17:44 pass 2 started at `056d619d` (fresh queue, fresh clones, the sweep's shard clones reset by sweep_shard.py).
  lane-a: harness_selftest 0 failures; every gate rc 0 but the two flip checks by design.
- 18:1x CPUs 0-95 held by other lanes; the firmware campaign jobs allowed on the session pool too.
- 18:2x-20:0x pass 2 on the pool and pick8 ranges as they freed: every unit and shard done, all green (the table).
- 20:0x #902 found merged into dev-soft-core (17:35, `659d7687`; 894-tiers deleted): its tree is 07ed787e's, and
  HEAD..dev-soft-core is that merge commit alone, so the candidate merge has this head's tree. Graders on clone H.
- 20:1x receipts collected; INDEX.md (index.py: 670 files, scrub idempotent, no host path left, none over 200 KB);
  PR-BODY.md; REVIEW-READY-COMMENT.md; REVIEW READY posted once (issuecomment-6899637516).

## For the manager

- Push `895-talker-redeclare` at `056d619d` (rounds 6 to 9 on the pushed `62298ab5`); replace PR #901's body with
  round9/PR-BODY.md (rounds 6 to 9, finding by finding, both of this round's own findings). Act and the hosted
  exact-head contexts follow the push. PR #901's base `dev-soft-core` now carries #902 (`659d7687`); the PR's diff is
  this branch's own commits.
- Round 8's PR-BODY.md said "plat_ledger.py PASS"; that line was wrong (FAIL at 8x8/1if since 7B's cut), corrected
  here and fixed in `449d29d2`.
- The ruling's two delta reviews run from round 5's `62298ab5`.
- Scratch kept: r9/L (449d29d2), r9/H (the final head), the R9-W8 build, the R8-* builds (the legs that carry), the
  sweep shard clones $LANES/895r9sweep-shard{0..3}. Removed: see the run history's last line.
- 20:2x removed r9/M (the merge's clone), r9/P (the threshold's export) and pass 1's job clones r9/pass1/gates (receipts kept): the lane's scratch 21 GB -> 16 GB. No unit of this lane runs.

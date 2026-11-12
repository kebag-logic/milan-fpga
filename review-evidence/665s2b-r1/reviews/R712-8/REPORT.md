[R712] NEGATIVE - exact head b2d39235ab9bba85d7e560b5f5f78fb4be528960

# R712-8: external review of PR #810 (#665 Mark II split, stage S2b), round 29's delta

Head `b2d39235ab9bba85d7e560b5f5f78fb4be528960`, tree `bb7493020c15f2b84678ff000edb7e024b8b3146`. Delta reviewed: `66f71326..b2d39235`, which is the merge `e96b9120` of the pin move's head `bfe7a9d6` (PR #892, reviewed there) plus seven commits.

**Verdict: NEGATIVE, on two MINOR findings.** Both need a maintainer disposition, and the author has already disclosed both.

- **F1.** The composed tree's own ledger refuses its target platform's 8x8/2if image. The image plans 59.5 RAMB36 and the ledger holds 59.0. The owner's decision of 2026-11-12 14:26 (#665 issuecomment-6824896581) allows 60.0, with a cap of 60.5.
- **F2.** The `srp-compared-by-memcmp` cost control escapes on the composed image. The README still requires it to be caught.

Everything the brief asked me to check otherwise holds at this head:
- My round-7 findings, and R711-7's, are closed.
- The merge composes both sides.
- R4, R5 and R6 re-derive exactly.
- The fan-out refusal/loss and `fan_end` fixes are correct, and their tests fail under each planted defect.
- The load gate passes at 1x1/1if in both columns, and its binding control is real.
- The ACMP item is carried consistently.

## How this round was reviewed

- **Context.** I read AGENTS.md's review rules, then the issue's authority for this round:
  - the ruling on round 28 (issuecomment-6813183455, items 1-5);
  - its addendum (6813599829, items 6-8);
  - the owner decision (6824896581);
  - the REVIEW READY (6827605854).
- **Diff.** I read `git show --remerge-diff e96b9120` (the merge's eight hand-resolved files) and `git diff e96b9120..b2d39235` (23 files), together with the code each change depends on:
  - `aecp.c` `fan_out`;
  - `aecp_mbx.c`;
  - `mbx.c` `mbx_tx_begin` and `mbx_tx_commit`;
  - `srp_mbx.c`'s retained retry (`retry_spent`, `tick`);
  - `rows_grade.py` whole;
  - `load_grade.py`'s columns and controls;
  - `poll_grade.py`.
- **Order.** I read prior public findings (R711-7, R712-7) only after my own pass over the diff.
- **Evidence packet.** `review-evidence/665s2b-r1/author-r29`, archive `27dedc0a`:
  - The archive's `MANIFEST.json` covers 777 files: 0 bad, 0 unlisted.
  - The packet's own `receipts/INDEX.md` has 823 rows. 47 name helper scripts and tools that were not published. 5 are path-redacted logs whose index hash is the manifest's `original_sha256`.
  - The archive commit carries no signature (`%G?` = `N`), so I treated the manifest as the integrity claim (`receipts/verify_packet.txt`).
- **Probes.** I ran these myself, as disposable copies or in-process plants. Nothing was edited in the clone.
  - the load gate, flip check and poll gate, with their self-tests;
  - 12 arrival-rule plants;
  - 6 column-binding plants;
  - 14 fan-out runs (two baselines and twelve plants), including two of the author's new rows and eight of my own, through the AECP app arm (core and mailbox adapter, 2 interfaces) and the unit arm;
  - a reconciliation of round 7's R4 figures.
- **Restore.** The clone is byte-exact at the head (`receipts/restore.txt`):
  - index modes, blobs and paths equal the HEAD tree (1,588 entries);
  - no worktree or index change;
  - the gitlinks are as committed (tsn-c-stack `715589c`, lwSRP `08ee86e`);
  - the four `__pycache__` directories my runs wrote were removed.

## The six questions

### (1) Round-7 findings at this head

| Finding | At this head | Evidence |
|---|---|---|
| R712-7 F1 = R711-7 F1 (MINOR): retained retry once a pass; SRP's R4 window cut by AECP's whole work | **Closed** | `rows_grade.py:200-203` `retained_retries` = min(passes, floor(W/10)+2), the firmware's rule: `retry_spent` is cleared only in `tick()` (`srp_mbx.c:86`) and set once per retry (`:1031`). `:206-209` and `:237` count SRP's arrivals over W less the row's record alone. My required "state whether the hold is in scope" is met: the docstring `:54-59` takes it out of R5/R6 and charges no retry there (`:264`), which is the second option my finding offered. The flip check's rule controls refuse the two earlier rules (`flip_grade.py` `rule_controls`). §13 (`SPLIT_CONTROL_MEMORY.md:2120`) states the corrected figures. |
| R712-7 F2 (MINOR): `fan_end` keeps a completion for a walk left owed | **Closed** | `aecp.c:661` passes `!owed` as `whole`. `aecp_mbx.c:36-38` keeps no completion for a walk that is not whole. The comment at `aecp_mbx.c:11-12` is true at the code. T6 (`test_mbx_dma_driver.cpp`) and the core tests' `kept == 1` assert none after a mid-walk loss and exactly one after the resumed walk. Both plants are caught (my runs: `notice-completion-kept-for-a-walk-left-owed`, which fails both core fan tests, and the T6 plant, which fails `MbxDma.T6AWalkLeftOwedKeepsNoCompletion`). |
| R711-7 F2 (MINOR): no test tells REFUSED from LOST | **Closed** | `Core.ARefusedFrameIsSentToItsRecipientAndNoOneElseAgain` covers a ring full at frame 2 and a completion queue full. Each recipient gets the notice once, in order, at its own sequence_id, with one completion. Both of R711-7's plants are now caught by name (`receipts/fan_probe_failures.txt`). |
| R712-7 S1 (index after redaction) | Taken by the author | The author's index was generated after their scrub. In the published archive, 5 rows again carry pre-redaction hashes because the manager redacted after indexing. The manifest's `original_sha256` matches each of them (S6). |
| R712-7 S2 (column binding control) | Taken | `load_grade.py:494-496`. I falsified it (below). |
| R712-7 S3 (notice-round charge in `item.aecp`) | Moved to #894 by the addendum | Not re-judged. |
| R711-7 RES-1 (name #894 in the PR) | Fixed in the packet's PR body, **not in the live PR body** | See RES-1. |

My round-7 figure was one retry short. Under round 28's costs, the corrected rules give R4 = 59.19 ms. My 58.94 is the same costs with one retry fewer over the whole W, and R711-7's 58.18 is one retry fewer over W less the record. I reproduce all three in-process (`receipts/reconcile_r28.txt`), which confirms the author's reconciliation.

### (2) The merge `e96b9120`

- **No hidden change.** The remerge diff shows exactly the eight files the ruling named, each resolved from the composed tree. No other file differs from git's automatic merge. The whole delta changes nothing under `sw/mailbox` or `hdl` and no `.sv`, `.v` or `.yaml` file. There is no protocol or mailbox-contract change.
- **`ctrl_plat` at the four points.**
  - 8x8/2if, 20,288 B: the build's own refusal log reads it from the image (`receipts/merge/plat-merge/8x8-if2.log`, "this image carries ... ctrl_plat 20288").
  - 17,472 / 19,008 / 18,112 B: from the images table built at `2cc852fa` (`receipts/images/table.md`). No firmware file changed after `2cc852fa` except `test_aecp.cpp`.
  - These agree with each image's member sizes plus the struct's other fields (+188 B at one interface, +244 B at two at 1x1). They only feed refusal cases (`ctrl_memory_ledger.py:56-62`).
- **Size fixture at 58.0.** 123,112 B of `rom` in 124,928, 1,816 B under the granule (`receipts/images/fixture-8x8-if2.size.json`), so it is true of the composed image.
- **The ACMP expiry plant.**
  - It takes the composed anchor (with `dirty_if`, from #892) and round 28's kill test (`AcmpCore.TimerPortBudgets`). It is killed, with 7 checks failing (`receipts/merge/plant-acmp-expiry-reads-the-clock-twice.log`).
  - #892's kill test `AcmpMailbox.C5ToC9...` is still named by three other rows (`acmp_mutants.py:832`, `:838`, `:848`).
- **Docs.**
  - `MAILBOX_SPLIT.md` keeps round 28's removal of the T_svc column, which the merge base had, together with #892's new bounds (8,262 / 30,294 / 60,588 / 24,786) and the redelivery's RX_HEAD read.
  - The firmware README's SRP access counts (`sw/firmware/ctrl/README.md:444`) compose additively: base 3,523 / 4,429; #892 +1,724; round 28 3,116 / 3,256; composed 4,840 / 4,980.
- **Coverage ratchet.** Regenerated through `fw_coverage.py --write` (`receipts/merge/fw_coverage-write-at-the-merge.log`, 39 files).
- **Hot list.** `__lshrdi3` was dropped from `ctrl_split_hot.txt` and `ctrl_split.ld`, and `plat_arms.py` now refuses the helper.
- **Not true of the composed image:** the platform's 8x8/2if ledger. See F1.

### (3) R4, R5 and R6 at 1x1/1if

`rows_grade.rows` at the head gives R4 66.12, R5 35.95, R6 28.67. At 8x8/2if it gives R4 346.15, R5 144.15, R6 135.80 (`receipts/rows_at_head.txt`). These match the REVIEW READY to the hundredth.

I re-derived R4 by hand from the header constants and the stated costs:
- `CTRL_LOOP_DRAIN_US` 1300, `RX_PER_PASS` 2, `TICK_US` 430; srp (32, 2 ms), aecp (16, 5 ms), tick 10 ms.
- ticks: 7 × (40 + 430) = 3.29 ms.
- aecp: 16 × 205 = 3.28 ms.
- srp: (32 + floor((66.12 − 0.205)/2) = 64) × 260 = 16.64 ms.
- passes: 34 = 15 + 1 + 18 drained, × 180 = 6.12 ms.
- retained: min(34, floor(6.612) + 2 = 8) × 260 = 2.08 ms.
- others: 29 × 280 + 14 × 105 + 11 × 90 = 10.58 ms.
- item.aecp: 34 × 210 = 7.14 ms.
- item.acmp: 34 × 120 = 4.08 ms.
- item.reclaim: 1.70; timers: 3.075; steps: 2.925; rounds: 3.23; builds: 0.90; item.mrpdu: 0.81; item.walk: 0.16; gm: 0.105.
- The sum is 66.115 ms, which is ≤ 66.12.

Charged twice or missed:
- **Nothing is charged twice in a way that understates the row.** The retained retries (2.08 ms) and the 64 SRP records are both charged, although the firmware takes no other SRP record while one is retained (`rx_ready`). In time the two are exclusive, so this is a conservative overcount (S4).
- **Missed, and stated:** the four datapath change records in `EXCLUDED` (`rows_grade.py:107`, docstring `:61-67`). AMAP_LIVE_WRITE can arrive up to once per AECP record (29 in R4's window) and has no stated cost. The PR states this and defers it to #894. Because R4 is already over its bound and the rows are not the merge gate, no verdict moves (S3).
- **Can the controls tell a wrong charge from the right one?** Mostly yes (`receipts/rule_probes.txt`). `rule_findings` refuses these:
  - one retry fewer (R4 65.86) or one more (66.64);
  - once a pass (78.16);
  - no retries (59.81);
  - SRP over the whole W (66.38);
  - SRP cut by AECP's burst (65.86);
  - retries in R5;
  - a dropped or a doubled event type.
- **Two plants escape:**
  - "retries not capped by passes" is equivalent: passes always exceed floor(W/10)+2 in R4.
  - "SRP window less two records" escapes. Every `RULE_WINDOWS` entry is a multiple of SRP's 2 ms refill, so any shortening under 2 ms gives the same floor. It moves no figure at this head at either point (S1).
- The flip self-test refuses 131 of 131 controls and the load self-test 25 of 25 (my runs: `receipts/flip_grade.py_--selftest.log`, `receipts/load_grade.py_--selftest.log`).

### (4) The fan-out refusal/loss distinction and `fan_end` completion

`fan_out` (`aecp.c:609-677`) is correct against `mbx_tx_begin`/`mbx_tx_commit` (`mbx.c:515-590`):
- `mbx_tx_begin` commits the record before it first, so after a mid-walk FULL or LOST nothing is moving.
- REFUSED resumes at the refused frame's own recipient (whose sequence_id was not spent), or past the last recipient for a full completion queue.
- LOST resumes at the held recipient with its sequence_id given back.
- The cookie is stable until `sent_frame`, which runs once per notice, so one completion is kept per notice (IEEE 1722.1-2021 7.5.2 sequence_id; Milan v1.2 5.4.5.1, 5.4.5.2).
- No notice is sent twice or lost on any path I traced.

Plants, all run on disposable copies (`receipts/fan_probe_failures.txt`, `receipts/fan_probes_*.txt`):

| Plant | Caught by |
|---|---|
| baseline, AECP app arm | 125 pass |
| baseline, unit arm | all pass |
| author `fan-end-refused-taken-as-lost` | `Core.ARefusedFrame...` |
| author `refused-mid-fan-after-a-taken-frame-taken-as-lost` | `Core.ARefusedFrame...` |
| author `notice-completion-kept-for-a-walk-left-owed` | both core fan tests |
| author T6 row `(void)whole` | `MbxDma.T6AWalkLeftOwedKeepsNoCompletion` |
| reviewer: `whole` = `!lost` | `Core.ARefusedFrame...` |
| reviewer: a completion REFUSED taken as done | `Core.ARefusedFrame...`, `Mailbox.ANoticeWithNoRoomStaysOwed` |
| reviewer: the lost resend keeps the spent sequence_id | `Core.ANoticeWhoseFrameWasLost...` |
| reviewer: the lost frame not resumed | `Core.ANoticeWhoseFrameWasLost...` |
| reviewer: a walk left owed not committed | escapes both arms; **equivalent**, since `mbx_tx_begin` already committed |
| reviewer: the completion queue checked before the commit | **escapes both arms**; head code correct (S2) |

### (5) The load gate

- `load_grade.py --check` passes: 1x1/1if 0.486 at the pin and 0.483 with tsn-c-stack#32, both at most 0.70. The self-test refuses 25 of 25 controls.
- **The COLUMNS binding refusal is real** (`receipts/columns_probe.txt`). `controls()` refuses each of these:
  - the tables swapped;
  - the names swapped;
  - the pin's table twice;
  - the donor column dropped;
  - an equal copy that is not the same table object.

  It runs in `--selftest` and the harness self-test, not in `--check` (S5).

### (6) The ACMP item

- 11,359 cycles (`backlog-owed`, `receipts/costs/G1/costs.txt`) at 100 MHz is 113.59 µs. Plus 5 % and rounded up to 5 µs, that is 120 µs.
- It is carried as `poll_grade.STATED_US[1]['acmp']` = 120, and the donor column's 1x1/1if `item.acmp` = 120.
- The load term is 0.037: 120 µs × (200 + 100 + 8) /s.
- In R4 it is 34 × 120 µs = 4.08 ms.
- The values are consistent between the load gate and the rows.

## Findings

### R712-8-F1 - MINOR - Conformance, Tests, Docs - `sw/litex/ctrl_memory.py:217-218`, `sw/litex/ctrl_memory_ledger.py:40`, `:42`, `:55`, `docs/design/SPLIT_CONTROL_MEMORY.md:221`, `:255`, `:281` - the composed tree refuses its own target platform's 8x8/2if image

**Authority and evidence**
- The owner decision of 2026-11-12 14:26 (#665 issuecomment-6824896581): "The platform image may plan 60.0 RAMB36, with a cap of 60.5." It supersedes, for the flip, §5's "56 RAMB36 or fewer at every point", and "That document's next revision states it."
- At this head `LEDGERED["platform-8x8-two-interfaces"]` is 59.0 with the correct key (`ctrl_plat` 20,288).
- The composed image plans 59.5: `rom` 128,264 B against the 126,976 that 59.0 holds. The author's receipt `receipts/images/platform-8x8-if2.log` shows rc 2: "REFUSED: allocation over budget: 59.5 RAMB36 ... exceeds the 59-RAMB36 budget". Round 28's head (127,664 B) and round 27's (127,544 B) were refused the same way, hidden behind the stale key.
- No gate links the platform image with its override (the author's `PLATFORM-LEDGER-FINDING.md`, and §5 `:281`), which is why the overrun went unseen for two rounds of this PR.
- §5 `:281` says "The ledger stays 59.0 until a ruling names another". The owner decision names 60.0 / 60.5 about ten minutes before the head was committed, and `:221` and `:255` still state the superseded 56 criterion.

**Impact**
- At merge, the tree's ledger refuses the target platform's 8x8/2if image that the owner decision allows.
- The ledger, its tests (`ctrl_memory_ledger.py`) and §5 state a plan the decision has replaced.
- No executable check would catch the next stale key or tile overrun of this image.

**Required outcome**
- The platform's 8x8/2if image is not refused by the tree's own ledger: its entry and the ledger tests are set at the owner decision's 60.0 with the 60.5 cap and cite it, or a maintainer rules another disposition.
- §5 states the decision (lines 221, 255 and 281).
- A check plans the platform image at its ledgered point with its override, or reads its measured plan, and fails on a stale key or a tile overrun.

**Verification**
- `ctrl_plat_image.py --ledgered-point platform-8x8-two-interfaces` at 8x8/2if links and plans at most 60.0. Its refusal at 60.5 is a ledger arm.
- `test_ctrl_memory.py` passes.

### R712-8-F2 - MINOR - Tests, Docs - `tb/verilator/ctrl_service_budget/poll_items.py:122`, `tb/verilator/ctrl_service_budget/README.md:1413`, `docs/design/SPLIT_CONTROL_MEMORY.md:2168` - the SRP comparison cut's cost control escapes on the composed image

**Authority and evidence**
- README `:1413` requires: "Each must print its `STATED` line ... `CONTROL srp-compared-by-memcmp caught`." §13 `:2168` says each cut's plant "must print `STATED`".
- At this head the control escapes. The author's receipt `receipts/controls/ctl-srp-compared-by-memcmp.log` reads "CONTROL srp-compared-by-memcmp ESCAPED", rc 1.
  - With the old comparisons, the record costs 35,908 cycles, under the 36,500 that 8x8/2if's stated 365 µs allows.
  - Unplanted, it costs 32,866 cycles (`receipts/controls/srp-record-plant-against-unplanted.txt`).
  - At round 28's head the same plant (37,494) was caught. The merge's composed image caused the escape.
- §13 `:2184` discloses it, and the REVIEW READY asks for a ruling. The tree still carries a documented control that cannot fail for the defect it exists to catch.

**Impact**
- A return of the per-byte StreamID/MAC comparisons is caught by no check at 8x8/2if.
- The README's stated expectation is false at the head.
- The stated cost remains a true upper bound, so no load or row figure is understated.

**Required outcome**
- A maintainer ruling, then a tree in which this control is caught, or in which its expectation is restated with the ruling cited. For example, restate 8x8/2if's SRP record and retry from the composed image's measurement (34,509 cycles is 345 µs under the table's rule), or re-target the control's limit.

**Verification**
- `run.py --point 8x8 --variant answering-every-port --mutation srp-compared-by-memcmp` prints `CONTROL srp-compared-by-memcmp caught`, or README `:1413` states the ruled expectation.

### Suggestions (optional, do not affect coverage)

- **S1. `rows_grade.py:339`.** Every `RULE_WINDOWS` entry is a multiple of SRP's 2 ms refill, so an `srp_window` that is short by less than 2 ms (for example W less two records) passes `rule_findings`. Add windows off that grid, such as each solved row's W or 5.3 ms.
- **S2. `aecp_mbx.c:36-45`.** No test holds the adapter to "REFUSED means the last frame was delivered". A plant that checks the completion queue before committing escapes both the app arm and the unit arm. A driver test with a full completion queue should assert that the last frame is committed before the REFUSED.
- **S3. For #894.** The `EXCLUDED` datapath records (`rows_grade.py:107`) are missing terms of the rows, and possibly of the long-window load. AMAP_LIVE_WRITE can arrive once per AECP record. #894's term table should carry each with an arrival bound and a cost.
- **S4. For #894.** R4 charges both the retained retries and every SRP arrival, though a retained record stops other SRP records being taken. This is conservative; state it in #894's itemisation.
- **S5. `load_grade.py:494-496`.** The binding check runs only in the self-test. `--check` with swapped columns prints PASS with mislabelled HELD lines. Neither the load gate nor the harness self-test is wired into any workflow, so they rely on the manual merge-gate run.
- **S6. Publication, for the manager.** In archive `27dedc0a`:
  - 5 `INDEX.md` rows carry pre-redaction hashes because redaction ran after indexing.
  - 47 rows name helper scripts and tools that were not published (for example the receipts' generator and the ACMP item tool), so a reviewer cannot re-run them.
- **S7. `acmp_mutants.py:780-783`.** The merged expiry row could also name #892's `AcmpMailbox.C5ToC9...` kill through `also`, so the merge keeps both sides' kill claims.

### Residue (wording only)

- **RES-1 (live PR #810 body).** The published PR body is still round 28's:
  - It states "73.02 ms against 20" (line 184).
  - It has no 66.12 and no round-29 section.
  - It differs from the packet's `author-r29/PR-BODY.md`, which states the round-29 figures and names #894 in R711-7 RES-1's places.

  **Exact fix:** publish `review-evidence/665s2b-r1/author-r29/PR-BODY.md` (archive `27dedc0a`) as the PR body.
- **Comment rule.** No added source line in the delta carries a lane label, round label, reviewer ID or issue-comment ID.
  - The A17/A19/E1-E3 strings are #653 test IDs.
  - `ctrl_memory.py:214-216` carries "lane S14" and two ruling IDs on a line the delta edited. That text was there before (tracked by #746), so it is not a new instance.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | owner decision 6824896581 against `ctrl_memory.py:217-218` and `receipts/images/platform-8x8-if2.log`; `srp_mbx.c:86`, `:1031` against `rows_grade.py:200-209`, `:237`, `:264`; `aecp.c:609-677` and `aecp_mbx.c:28-45` against IEEE 1722.1-2021 7.5.2 and Milan v1.2 5.4.5.1/5.4.5.2; `load_grade.py --check` (0.486/0.483 ≤ 0.70) | R712-8 | `b2d39235` |
| RTL | CLEAN | no RTL or contract change in `66f71326..b2d39235` (`sw/mailbox`, `hdl`, `*.sv`, `*.v`, `*.yaml` diff empty); the remerge diff's 8 files; fan-out state across `aecp.c:609-677`, `aecp_mbx.c:28-45` and `mbx.c:515-590` (commit-before-begin, the cookie, the sequence_id give-back, the `held_r` NULL path only on REFUSED); the RAMB36 plans measured and understood (`receipts/images/table.md`) | R712-8 | `b2d39235` |
| Robustness | CLEAN | REFUSED/LOST/completion-full/resume paths traced and probed: 8 reviewer plants, 2 equivalent (`receipts/fan_probe_failures.txt`); no notice twice or lost; the retained retry's centisecond rule at `srp_mbx.c:1031` against the rows | R712-8 | `b2d39235` |
| Tests | UNCLEAN (F1, F2) | the new core test and T6: 4 author plants caught, 4 of 6 reviewer plants caught, 1 equivalent, 1 gap (S2); `rule_findings`: 12 plants, 10 refused, 1 equivalent, 1 blind spot (S1); COLUMNS: 5 of 5 wrong bindings refused; flip 131/131, load 25/25 (my runs); `ctl-srp-compared-by-memcmp` rc 1 (F2); no platform-image ledger gate (F1) | R712-8 | `b2d39235` |
| Docs | UNCLEAN (F1, F2) | `SPLIT_CONTROL_MEMORY.md:221`, `:255`, `:278-281`, `:2120`, `:2168`, `:2184`; `MAILBOX_SPLIT.md` remerge; `sw/firmware/ctrl/README.md:444`; `aecp/README.md:126-127`; `ctrl_service_budget/README.md:1413`; live PR body (RES-1) | R712-8 | `b2d39235` |

## Real limits

- **Not run:** full parent, PP, gPTP, Yosys or builder banks; the full control (696), AECP (227) and SRP (340) campaigns; the harness legs; the four-shard sweep; the workflows. Their results here are the author's receipts.
- **Not independently built:**
  - the platform and fixture images, and the three non-keyed `ctrl_plat` totals: author receipts, checked for internal consistency only;
  - the 11,359-cycle measurement: the author's leg.
- **The hooks harness** cannot build at this head or at round 28's (provisional image, no flash map). H-ACMP's re-anchored plants are shown to apply (self-test 28 of 28), not caught by a run.
- **No hosted run at the exact head:** 0 check runs, 0 statuses, 0 workflow runs for `b2d39235`.
- **No manager source bank** exists at this head, and I infer none.
- **Physical calibration was not run.** Field skips are not hardware proof.
- **The archive commit is unsigned.** Integrity rests on `MANIFEST.json`.

## Pending manager duties

- Disposition of F1 under the owner decision and of F2 by ruling. Then re-review of the commit that answers them.
- Publish the round-29 PR body (RES-1).
- Open the author's proposed issues: the platform-image ledger gate, if not folded into F1's fix, and the hooks harness build.
- Exact-head `rtl-fast` after any new head, and `verilator-suites` and `yosys-portability` once marked ready.
- The current-dev candidate merge (source base `a68536fa`, live dev `fa6c094b`) and its builder and native banks. Live `dev-soft-core` reports conflicts in seven paths (author's `receipts/checks/merge-tree-against-live-dev-soft-core.txt`).
- The second positive review and the completion bar.

## Publishable files

Listed in `MANIFEST.sha256`:
- `scripts/`: `verify_packet.py`, `rule_probes.py`, `columns_probe.py`, `fan_probes.py`, `reconcile_r28.py`;
- `receipts/`: the packet check, the gate and self-test logs with their rc files, the rule, column and fan-out probe outputs, the round-28 reconciliation, and the restore record.

R712-8 FINISHED

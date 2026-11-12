[R712] NEGATIVE - exact head 66f713267f201d1a00d7f711e04b3a996d804dee

# R712-7: external review of PR #810 (#665 Mark II split, stage S2b), round 28's delta

- **Head:** `66f713267f201d1a00d7f711e04b3a996d804dee`, tree `3f30ac591059d9dd6f77dcbb908e43e6416a30fb`.
- **Delta:** `e7e2b744..66f71326`, five commits, 31 files. No HDL is in the delta: only firmware, the CPU-budget harness and docs.
- **Authority:** the round 28 ruling (#665 issuecomment-6805157674, maintainer-delegated) and the owner decisions it quotes (option D, option B tiers, #890's 0.75 for 8x8/2if). I also read the round 29 ruling (issuecomment-6813183455), which sends the tier rows to #894 "with the model first" and folds early findings into round 29.

**Verdict: NEGATIVE, on two MINOR findings.**
- **F1.** `rows_grade.py` charges SRP's retained retry once a pass. `srp_mbx.c` allows at most one a centisecond, and the harness's own load gate and section 13 both state that rule. So 1x1/1if's R4 by every source is too high: 73.02 ms, where my independent re-derivation gives 58.94 ms. The "retained retries 9.00 ms" term, which the round 29 ruling cites in its #894 reasoning, is about 7.5 ms too high. Also, one SRP term is counted over a window shortened by AECP's own work. The R4 miss itself stands at either figure; it is the model that is wrong.
- **F2.** After a mid-walk lost frame, `fan_end` keeps a completion for a notice that is still owed. I proved this with a probe.

Every round 28 item is otherwise met and verified against code and receipts: the merge gate at the pin, record commits, #890's deferral, the flip check, portable C, docs and residue, and the gates.

## How this round was reviewed

1. I read AGENTS.md (CONTRIBUTING.md through it), the PR body and the round 28 and 29 rulings.
2. I read the full firmware and harness delta, then `ctrl_loop.h` (THE PASS, THE DRAIN, THE TICK, THE RETRY, THE TRANSMIT, THE STEP), `srp_mbx.c`'s retained retry, `aecp.c`'s `fan_out` and `aecp_mbx.c`'s fan port.
3. I re-ran the graders and wrote my own probes: the load columns, an independent rows solver, an object-identity build with a positive control, the changed firmware arms, the round's 13 plants, the clean AECP tests and one probe test.
4. I verified the author packet `review-evidence/665s2b-r1/author-r28` at archive `ac5d8de2` against its `receipts/INDEX.md`.
5. Prior findings (R711-6, R712-6) were read only after my verdict draft was written (`scratch/verdict-draft.md`, 03:27 UTC, unpublished).

All my runs were foreground, inside this clone or the packet's `scratch/`. The clone was restored and verified afterwards (`receipts/restore_check.txt`).

## The six questions

### (1) Round-6 findings at this head

| Prior finding (at `e7e2b744`) | At this head | Evidence |
|---|---|---|
| R712-6-F1 = R711-6 F1: the merge gate held 1x1/1if on the tsn-c-stack#32 column only | **Closed.** | `load_grade.py:165-168` `COLUMNS`; `:347-358` (each column, named). `--check` prints `HELD 1x1/1if at the pin: 0.463` and `HELD ... with tsn-c-stack#32: 0.450`, `RESULT: PASS` (`receipts/load_grade_check.log`). The pin-only control is at `:420-429`. My probe: a pin-only rise is refused naming the pin only; a donor-only rise is refused naming the donor only; the 0.70 boundary is exact (0.69961 passes, 0.70011 is refused); the old donor-only gate lets the new control escape (`receipts/probe_load_columns.log`). Section 13's margins name both columns. |
| R712-6-F2: a record's commit inherited an earlier ERR; a failed move was reported against the next recipient; `fan_end` discarded its result | **Closed** for the three rules ruled. One new consequence is recorded as F2 below. | `mbx.c:82-85` (`TX_MOVED`, static-asserted above 2 + 379 words), `:526` (only a moved record waits on the mover), `:547-548` (`MBX_STATUS_LOST`, nothing started), `:577`, `:584`; `mbx.h:180-198`; `aecp_mbx.c:20-40`; `aecp.c:634-672`. Tests T2, T4 and T5 and `Core.ANoticeWhoseFrameWasLostSendsItToItsRecipientAgain` pass (`receipts/fw_arms.log`, `receipts/aecp_clean.log`). All 9 plants are caught by their test's words, and the changed retry plant too (`receipts/fw_ctrl_plants.log`, `receipts/fw_aecp_plants.log`). |
| R712-6-F3: the not-committed cut's ROM growth was attributed to the wrong image | **Closed.** | `SPLIT_CONTROL_MEMORY.md` §13 now reads "152 B at the pin and 160 B with tsn-c-stack #32, which takes arm A's image with tsn-c-stack #32 over the 8x8/2if ledger (122,936 B in 122,880)". |
| R712-6 RESIDUE-1 and R711-6 RES-1: issue-comment IDs and round labels in harness comments | **Closed.** | 0 matches for `issuecomment-NNN` or "round N ruling" in `load_grade.py`, `flip_grade.py`, `poll_grade.py`, `poll_items.py`, `selftest_polls.py`, `rows_grade.py` and `answers.py`. No new instance in any added source line of the delta. |
| R712-6 RESIDUE-2: the round 26 load table described as "this head" | **Closed.** | The round 26 section has moved to the round histories. The PR's "load at this head" table (PR body line 67) is under Round 28 and matches `--check`. |
| R711-6 RES-2: "the flip-gate issue" and "its own issue" | **Closed.** | #890 and #891 are named; `answers.py:104-105` cites #891. |
| R711-6 F2: round 16's margin at 8x8/2if | **Disposed** by the ruling (item 3: deferred to #890). | §13 cites #890 and the 0.75 decision; 1x1/1if keeps the margin (160,618 cycles, 39,382 under). |
| R711-6 F3: decision D's tier bounds not held | **Closed** as ruled (item 4): the flip check holds them. | Open on the model's correctness: see F1. |
| R711-6 F4: GNU attributes in the protocol and port code | **Closed.** | See (5). |
| R712-6 S1: a plant for the pool's link | **Taken.** | `pool-link-unwritten` and `portable-fallback-link-unwritten` are caught by `Pool.P10` (`receipts/fw_ctrl_plants.log`). |

### (2) Record commits: can a record be lost, duplicated, reordered or reported with the wrong status?

I traced the driver and the fan-out at their code.

**Lost.** No.
- A failed moved record is not committed (`mbx.c:526-528`): `moving` is cleared at `:522` and the head is not advanced.
- The next `mbx_tx_begin` returns LOST and starts nothing (`:547-548`; T2 asserts that 3 starts stay 3 and TX_HEAD is unchanged).
- `fan_out` sets `k = held` and gives back `held_r`'s sequence_id (`aecp.c:667-671`). `held` and `held_r` are only set after a TAKEN, and a LOST always names the record started just before it, because every walk ends with `fan_end`'s commit. So `held_r` cannot be NULL on a LOST: the first `fan` of a walk commits nothing.
- A lost last frame is reported by `fan_end` (`aecp_mbx.c:31-33`), and the walk resumes there.

**Duplicated.** No.
- The lost record's slot is reused at the same head (T2, T5: "the lost frame uncommitted").
- `--held_r->sequence` restores exactly the sequence_id the lost frame carried (IEEE 1722.1-2021 9.2.1.1 sequence_id, 7.5.2 unsolicited notification to each registered controller).
- The core test checks each recipient once, in order, with its own sequence (plants `sequence-spent`, `resumed-at-the-next` and `frame-skipped` are caught).

**Reordered.** No.
- The resumed walk starts at the lost recipient, and nothing after it was started (`break` precedes `++r->sequence`).
- `mbx_tx_send` still commits its own record (`:591`). The begin/commit contract (`mbx.h:186-198`) forbids any other channel or window access between the halves, and that is what keeps the mover's single ERR attributable. `fan_out` is the only split caller.

**Wrong status.** One case: F2.
- `fan_out` calls `fan_end` after a mid-walk LOST (`aecp.c:657-662`). `fan_end` commits nothing there (`moving` is 0), returns TAKEN and keeps a completion for cookie `tx_cookie` while the notice is still owed.
- My probe shows `fan_end` returning `0` (TAKEN) with `completions kept 1` (`receipts/probe_fan_end_after_loss.log`).

**Plants.** All 13 of the round's plants were caught by their tests' words (my subset runs). Each is meaningful: for example, `mover-move-not-held-its-own` fails 15 checks, starting with T1.

### (3) The load gate

- `load_grade.py --check` holds 1x1/1if in both columns at 0.70: 0.463 at the pin and 0.450 with tsn-c-stack#32, rc 0. `--selftest` gives 24 of 24 (11 controls and 13 periods).
- Refusals carry the column's name.
- The new control is real: my mutant restoring the old donor-only gate makes exactly `a rise at the pin alone` escape.
- One gap, S2: swapping which table each column name binds is not caught by any control (the HELD lines then print swapped values). The merge property is unaffected, because both tables are still held.

### (4) The rows, re-derived at 1x1/1if

**Method.**
- `scripts/rederive_rows.py` writes every count itself. It takes only the stated costs (`load_grade.stated` at the pin, `poll_grade.stated_us`, `ROW_COSTS`), the contract rates from `mailbox.yaml` and the header constants, which I checked by hand: `CTRL_LOOP_DRAIN_US` 1300, `RX_PER_PASS` 2, `RX_PER_TICK_PASS` 1, `TICK_US` 430, `STEP_AGE` 2, `STEP_PASS_US` 975, `BUILD` 900/405, `AECP_NOTICE_US` 255, `ROUND_COLD` 85, `PACE` 2, `YIELDS` 0, `FIRM` 12, `NOTICES_MOST` 12.
- With the model's own rules (V0) it reproduces `rows_grade.py` exactly: R4 73.02, R5 37.19, R6 32.69 ms. So the arithmetic is right, and the question is the rules.

**R4 item by item** (the AECP channel's last record of its 16-record burst, beside the composed burst, every notice queued, against THE DRAIN as built):

| Term | Model, ms | Against the firmware as built | Verdict |
|---|---:|---|---|
| own: 16 × `record.aecp` 205 | 3.28 | The row's record and the 15 ahead of it in its ring. | right |
| srp: (32 + ⌊(W − 3.28)/2⌋) × 250 | 16.50 | SRP's records precede in every pass (THE DRAIN first). Every SRP arrival before the row's record is taken precedes it, including those arriving while AECP's earlier records are being taken. `rows_grade.py:199-200` subtracts all of AECP's own 3.28 ms from SRP's arrival window. Over the whole W it is 17.00. | **too low** (−0.50 ms; F1) |
| others: ACMP, ADP, MAAP arrivals over W, capped at passes × 2 | 10.96 | Round-robin start, so any of them can be ahead. Every arrival is counted (the cap does not bind). | right (conservative) |
| item.retained: min(passes, SRP arrivals) × 250 | 9.00 | 36 retries. `srp_mbx.c:1025-1033` retries at most once a centisecond (`retry_spent`, reset in `tick()` at `:79-86`), and no other SRP record is taken while one waits. In this window that is at most ⌊W/10⌋ + 1 = 8 retries (2.00 ms at W = 73). This is round 24's superseded rule, which §13 (line 2112) records as replaced. The load gate's own control `a retry every pass` (`load_grade.py:446`) refuses this very rule. | **too high** (~7.0 ms before the fixed point; F1) |
| item.aecp: min(passes, 30 + 16) × 210 | 7.56 | AECP records behind the row's cannot owe a frame ahead of it, so the sources are 16 + 16 probes. Here passes (36, then 32) caps it either way. | right at 1x1/1if (conservative; 8x8/2if moves: V3) |
| passes: 36 × (25 + 155) | 6.48 | Ticks are counted as passes with no AECP progress, though a tick pass takes 1 record. Drain passes are `⌈work/1300⌉`, an upper bound since a drain pass spends at least 1300. | right (conservative) |
| ticks: 8 × (40 + max(125, 430)) | 3.76 | | right |
| rounds: 2 rounds, 12 notices (7 + 5) | 3.23 | The 12 queued notices. Notices that the 15 AECP records ahead cause are charged in `item.aecp` at 210 us one a pass, but THE RETRY sends notices only in rounds, at `AECP_NOTICE_US` 255 + 85 cold. | right for its stated scope; see S3 |
| timers 3.19, steps 2.92, item.acmp 2.34, item.reclaim 1.80, builds 0.90, item.mrpdu 0.81, item.walk 0.18, gm 0.10 | | Each re-derived from its stated rule. | right |

**Result.**

| Variant (1x1/1if) | R4 | R5 | R6 |
|---|---:|---:|---:|
| V0 the model as stated | 73.02 | 37.19 | 32.69 |
| V1 SRP arrivals over the whole W | 73.52 | 37.19 | 32.69 |
| V2 V1 + the retained retry at one a centisecond | **58.94** | 34.94 | 28.55 |
| V3 V2 + AECP owed frames only from the records ahead | 58.94 | 34.94 | 28.55 |
| V4 V3 + each record ahead queueing a notice for THE RETRY (sensitivity only) | 67.10 | 34.94 | 28.55 |

- At 8x8/2if, V2 gives R4 344.74 (model 489.97), R5 154.43 and R6 144.12 (`receipts/rederive_rows.log`).
- **So 73.02 ms is too high**, by about 14 ms at 1x1/1if. The model charges the retained retry at the passes' rate, where the firmware allows the TICK's.
- The retry also cannot run at full rate beside SRP's full drain, since no other SRP record is taken while one waits. Even V2 still sums both.
- **One term is undercounted** (SRP's window, −0.50 ms).
- **One hold is missing from R5 and R6, or `item.retained` is out of scope.** A retained record holds SRP's channel for up to `SRP_RX_RETRY_MS` (1000 ms). If storage refusal is inside the rows' every-source scope, R5 and R6 do not count that hold. If it is outside, `item.retained` should not be charged at all.
- The R4 miss against tier 1's 20 ms stands under every variant. That miss is the accepted finding for #894; the wrong term is F1.

### (5) Portable C keeps the images byte-identical

- `scripts/objects_identical.sh` compiled every firmware C file outside `test/`, at `e7e2b744` and at `24ea9c04`, with the split flags (`-march=rv32im -mabi=ilp32 -Os -std=c11 -DNDEBUG`, `CTRL_MBX_DMA_BASE`, function and data sections) and the pinned GCC 14.3.0.
- It dumped each object's disassembly, sections and symbols and compared them: **26 identical, 0 different**. These include `srp/srp_mbx.c`, `port/ctrl_pool.c`, `aecp/aecp.c`, `aecp/aecp_mbx.c` and `mbx/mbx.c`.
- 5 units need generated SoC headers and were not compiled: `ctrl_plat.c`, `ctrl_plat_main.c`, `ctrl_app_aecp.c`, `aecp_nvm.c`, `ctrl_debug.c`.
- Positive control: the same comparison across `71e905fb` flags exactly `mbx.c`, `aecp.c` and `aecp_mbx.c` (`receipts/objects_identical_control.log`).
- This agrees with the author's image-level sha256s (`5b2317d8...`, `be42e7c9...`, `57b60044...`).
- `git grep __attribute__ -- sw/firmware/ctrl ':!*/test/*'` shows only `plat/ctrl_cc.h:31-32`. No `__builtin_`, `asm`, `typeof` or `#pragma GCC` remains outside `test/`.
- The `portable` arm passes with `CTRL_CC_GNU=0` (48 tests, scan 0 findings), and its 3 plants are caught.

### (6) The disclosed deviations

| Deviation | Honest? | Evidence |
|---|---|---|
| The 8x8/2if column with the donor (tsn-c-stack#32) is not re-measured: 58 vs 57.5 RAMB36 | Yes | `receipts/rom/D8-image.log:1`: `REFUSED: allocation over budget: 58 RAMB36 (rom 122896 bytes in 124928 ...) exceeds the 57.5-RAMB36 budget ledgered for 8x8, two interfaces`. The column keeps its committed costs. Round 29 sets 58.0 and re-measures. |
| The shared session pool | Yes | The sweep shards give 17 + 17 + 15 + 16 = 65 suites passed, 0 failed, 0 timed out. The only effect seen is the timeout below. |
| `elaborate-gates-1` run twice | Yes. The first run hides no failure. | `first-elaborate-gates-1/..._gate_19.log:25-28`: `TIMEOUT test_soc_timing_cuts (900s wall clock - result UNKNOWN, not a failure)`, 7 of 8 passed, rc 92. The rerun gives 8 of 8 passed, rc 0, and the published final log is the rerun's byte for byte. Both runs are kept. |
| Fresh rebuilds for the harness re-grade | Yes | `receipts/head/head-G*.log`: `REFUSED reused build is stale: tree:firmware changed` (rc 1, kept). Then `headS-G*-compare.txt`: each image `objcopy -O binary identical` to the leg's (for example 8x8/2if arm A 122,440 B, `6f18ddb0...`), a sample log byte-identical, rc 0. The only firmware change after the legs' `71e905fb` is `coverage.ratchet`. |

**Packet integrity.**
- 660 of 666 receipts match `INDEX.md` byte for byte.
- The 6 that do not are exactly the 6 workflow logs containing a `<home-path>` redaction marker, each 8 bytes shorter than indexed. That is consistent with privacy redaction after indexing, and none of them is a grading input (S1).
- The archive commit is unsigned (`%G?` = N). It is identified by its id `ac5d8de2`.

## Findings

### R712-7-F1 - MINOR - Tests, Conformance, Docs - `tb/verilator/ctrl_service_budget/rows_grade.py:227`, `:41`, `:199-200` - the rows by every source charge SRP's retained retry once a pass, against the firmware's once a centisecond

**Authority and evidence**
- `srp_mbx.c:1025-1033`: "at most one retry a centisecond (tick), so the retries come at THE TICK's rate, not the passes'". `retry_spent` is reset only in `tick()` (`:79-86`).
- `SPLIT_CONTROL_MEMORY.md:2112` records the once-a-pass rule as round 24's, replaced.
- The load gate refuses that rule as a planted defect (`load_grade.py:446`, `a retry every pass`).
- `rows_grade.py:227` charges `min(passes, srp_in)` retries, 36 in 1x1/1if's R4 (9.00 ms). The firmware allows at most 8 there.
- `rows_grade.py:199-200` also counts SRP's arrivals over W minus all of AECP's own work, which undercounts by 2 records at 1x1/1if.
- My independent re-derivation (`scripts/rederive_rows.py`, `receipts/rederive_rows.log`) reproduces 73.02 under the model's rules and gives 58.94 ms with both terms corrected (R5 34.94, R6 28.55; 8x8/2if R4 344.74, R5 154.43, R6 144.12).
- None of the 129 flip controls can catch a wrong rate. "Each source left out shortens W" holds for any rate.

**Impact**
- The flip check's figures, §13 (line 2085) and the PR body (item 4, the decisions list) publish R4 = 73.02 ms and "the retained retries (9.00 ms)" as by-every-source terms.
- The round 29 ruling uses that 9.00 ms term to reason that tiers cannot close R4.
- #894 is to itemise "every term at both points" from this model, so a wrong term misdirects its design.
- The 1x1/1if R4 miss itself stands (58.94 > 20).

**Required outcome**
- `item.retained` is charged at the retry's own rule: at most one a centisecond in W, and no more than SRP's records.
- The rows state whether a retained record's hold on SRP's channel is in scope. If storage refusal is in scope, R5 and R6 count that hold (no other SRP record is taken while one waits, up to `SRP_RX_RETRY_MS`). If not, `item.retained` is not charged.
- R4's SRP term counts every SRP arrival before the row's record is taken.
- A flip self-test control plants the once-a-pass retry, or the shortened SRP window, and must see the row lengthen.
- §13 and the PR state the corrected figures.

Per the round 29 ruling ("no change to `rows_grade.py`" in round 29; findings that arrive in time fold into it), the manager decides whether this lands in round 29 or, unchanged as a defect, in #894's model-first itemisation. Moving it does not resolve it.

**Verification:** `flip_grade.py --check --point 1x1/1if` prints R4 within 0.01 ms of an independent re-derivation (mine: 58.94 ms with these two corrections), and the new control is refused.

### R712-7-F2 - MINOR - Robustness, Conformance, Tests - `sw/firmware/ctrl/aecp/aecp.c:657-666`, `sw/firmware/ctrl/aecp/aecp_mbx.c:11`, `:27-40` - after a mid-walk lost frame, `fan_end` keeps a completion for a notice still owed

**Authority and evidence**
- `aecp_mbx.c:11` states "A completion is kept for a notice's last frame alone (fan_end)".
- When `fan` reports a frame LOST mid-walk, `fan_out` still calls `fan_end` (`aecp.c:660`). `mbx_tx_commit` then has nothing to commit and returns true, and `fan_end` keeps `{cookie, TX_HEAD}` and returns TAKEN.
- The notice stays owed (`owed` from the loop) and resumes later at the lost recipient, with the same `tx_cookie`, since `sent_frame` has not run.
- My probe (`scripts/probe_fan_end_after_loss.cpp.txt`, `receipts/probe_fan_end_after_loss.log`): `fan_end after a mid-walk loss: 0 (TAKEN), completions kept 1`.
- `aecp_tx_complete` matches a completion by cookie (`aecp.c:547-560`). If the resumed walk ends and `sent_frame` assigns that cookie to a counter notice before the transmit tail passes the partial walk's head, the stale completion matches first. It stamps `counter_at` from the partial walk's departure, before the resumed frames depart (Milan v1.2 5.4.5.2, the counters' notice rate).
- The same path existed before this delta for a mid-walk REFUSED (ring full). The LOST route is new here.
- Neither T5 nor the core test asserts the completions after a mid-walk loss: the core test's `FanModel::end` mirrors the behaviour without checking it.

**Impact**
- A counter notice's rate-limit clock can start early, by the time between the partial walk's departure and the resumed walk's.
- A completion slot is spent on a notice that is not delivered, which can make a later `fan_end` REFUSED.
- This is narrow (fault and ring-full paths only), but it is a status reported for a notice before its frames are delivered.

**Required outcome**
- `fan_end` keeps a completion only for a walk that reached its last recipient, so none is kept for a walk that ends owed at a recipient (LOST, and the REFUSED route that shares the cause).
- The comment at `aecp_mbx.c:11` is true at the code.
- A test asserts no completion after a mid-walk loss and exactly one after the resumed walk ends, with a plant that restores the current behaviour.

**Verification:** the new test passes and its plant is caught. My probe prints `completions kept 0`.

### Suggestions (optional, do not affect coverage)

- **S1. Packet index after redaction.** `receipts/INDEX.md` was generated before 6 workflow logs were redacted (`<home-path>`), so 6 rows do not match (`elaborate-gates-0/1` `gate_15_*`, the first-run and rerun copies, `docs-gates-1/2` `gate_25_*`). Regenerate the index after redaction, so every row verifies.
- **S2. A control for the column binding.** No load control fails if `COLUMNS` binds the pin's name to the donor's table (`receipts/probe_load_columns.log`, the swapped mutant). Add one assert, for example that `COLUMNS[0][1] is STATED_US`.
- **S3. For #894's itemisation.** Notices that the AECP records ahead of R4's record cause are charged in `item.aecp` at 210 us one a pass. THE RETRY sends notices only in rounds, at `AECP_NOTICE_US` 255 + `AECP_ROUND_COLD_US`, and `rounds_us` never replenishes the queue past `AECP_NOTICES_MOST`. My V4 sensitivity moves R4 from 58.94 to 67.10 ms. State which rule holds.
- **S4.** At this head the PR's evidence names no exact-head hosted run: the head has 0 check runs and 0 statuses (base `dev-soft-core`). That is for the manager's merge-turn record, not a defect of the lane.

### Residue (wording only)

None new in this delta. No added source line carries a lane label, round label, reviewer ID or issue-comment ID.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | the round 28 ruling items 1-7 against `load_grade.py:165-168,347-358,420-429`; `mbx.c:515-592`; `mbx.h:180-200`; `aecp.c:598-676`; `aecp_mbx.c:11-40`; `rows_grade.py`; `flip_grade.py --check`/`--point`; `srp_mbx.c:79-86,1015-1033`; IEEE 1722.1-2021 7.5.2/9.2.1.1, Milan v1.2 5.4.5.1/5.4.5.2 | R712-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |
| RTL | CLEAN | No HDL in the delta (`git diff --name-only e7e2b744..66f71326`: firmware, harness, docs only). Driver architecture: `mbx.c:80-85` (TX_MOVED bit above 381 words, static-asserted), `:530` (head arithmetic masks the flag), the single-mover begin/commit contract `mbx.h:186-198`, `plat/mbx_dma.h:16-18,64-71` (ERR until the next accepted start); object identity of the portable change (`receipts/objects_identical.log`) | R712-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |
| Robustness | UNCLEAN (F2) | the failure paths of `mbx_tx_commit`/`mbx_tx_begin`/`mbx_tx_send`; `fan_out`'s LOST resume (`held` and `held_r` invariants, first-frame NULL impossibility); `fan_end` after a mid-walk loss (probe); the 0.70 boundary of the load gate (probe) | R712-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |
| Tests | UNCLEAN (F1, F2) | `test_mbx_dma_driver.cpp` T2/T4/T5, `test_aecp.cpp` `ANoticeWhoseFrameWasLost...`, `test_port_loop.cpp` P10, run clean (`receipts/fw_arms.log`, `receipts/aecp_clean.log`); 13 plants (`receipts/fw_ctrl_plants.log`, `receipts/fw_aecp_plants.log`); load selftest 24/24 and my column mutants; flip selftest 129/129 and its controls' power over rates (none) | R712-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |
| Docs | UNCLEAN (F1) | `SPLIT_CONTROL_MEMORY.md` §13 (lines 2085, 2112, 2138-2180), `tb/verilator/ctrl_service_budget/README.md`, `sw/firmware/ctrl/README.md`, `aecp/README.md`, `plat/README.md`, `mbx.h`; PR body Round 28 items 1-7 and decisions 1-4; prior residue (closed) | R712-7 | `66f713267f201d1a00d7f711e04b3a996d804dee` |

## Real limits

- No manager source bank runs at this head, and I claim none. Source-head execution evidence is the author's published gate receipts, verified as above.
- I did not run the full gates or full campaigns. I ran the changed arms (`unit`, `port`, `portable`), the round's 13 plants and 5 AECP tests, on this host's toolchain (GCC 16.2.1, GoogleTest 1.18.0). The CI pins may differ.
- The object identity covers 26 of 31 firmware units. The 5 that need generated SoC headers rest on the author's image sha256s.
- The rows re-derivation takes the stated costs as given. It re-derives counts, windows and rules, not measurements.
- Physical calibration NOT RUN. Field skips are not hardware proof. Docker/act and hosted runs were not used. The head has no hosted contexts.

## Pending manager duties

- Rule F1's landing (round 29, or #894's model-first itemisation) and F2's.
- The current-dev merge candidate (source base `a68536fa`, live dev `fa6c094b`): the builder and native banks, and hosted/act acceptance at the merge turn.
- Carry S1-S4 to the residue and suggestion checklist.

## Publishable files

`REPORT.md` and the files listed in `MANIFEST.sha256`: `scripts/` (the probes and drivers) and `receipts/` (each run's log and rc).

R712-7 FINISHED

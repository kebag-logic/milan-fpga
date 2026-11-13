# 894-a773: #894 round 7, HANDOFF

**Status: REVIEW READY at the final head `8a3791e44533d6b1cc26d486d0b18e7d83470dc1`**, posted 00:20 CET 2026-11-14 as #894 issuecomment-6867318907 (text: `REVIEW-READY-COMMENT.md`). The full pass at the head is clean (section 6). 1x1/1if holds every row by every source under the contingent ruling and its amendment. 8x8/1if is a STOP on its per-point slice, which by ruling item 6 does not hold back 1x1/1if.

- Start head `ccb47e39a534f4c8d02af826fa50fcd6578a38de`: the manager's merge of dev-soft-core `cec88385` (#810 merged) into round 6's STOP head `eebc37a3`. 20 commits on it.
- Nothing pushed, rebased or forced. **One local commit was amended:** `4d0168a4` became `f02457a6` to take in its README rows, minutes after it was made and before any pass or publication. Every other commit is as made.
- **Authority:**
  - the ruling issuecomment-6857835707 (`A10-RULING.md`);
  - the contingent ruling issuecomment-6858269025 (`A10-RULING-contingent.md`; `A10-RULING-2.md` is the same text);
  - its amendment issuecomment-6862465874 (`A10-RULING-amendment.md`).
- Also read: #908, round 6's handoff and its STOP (issuecomment-6857656161).
- `STOP-COMMENT.md` is the superseded STOP-era draft, kept as a record and not posted. The contingent ruling says "with no STOP and no extra round".
- dev-soft-core was still `cec88385` at 21:44, and there were no new comments on #894 or #908 since the amendment.

## 0. Exit

**1x1/1if** (`flip_grade.py --check --point 1x1/1if`: RESULT: PASS; receipt `receipts/model/rows-1x1-final.txt`):

| Row | W, ms | Original bound | Bound now | Moved by |
|---|---:|---:|---:|---|
| R4 | 12.82 | 20 | 20 | |
| R4L (paced) | 158.34 | 240 | 240 | |
| ACMP | 28.35 | 30 | 30 | |
| ADP | 26.76 | 30 | 30 | |
| MAAP | 26.88 | 30 | 30 | |
| first queued notice | 14.50 | 20 | 20 | |
| R5 | 72.71 | 90 | 90 | |
| R6 | 68.62 | 90 | 90 | |
| last queued notice | 125.84 | 125, over | 130 | the amendment |
| tx | 29.78 | 40 | 50 | contingent item 3 |
| txL | 49.99 | 40, over | 50 | contingent item 3 |

- **Load:** 0.513 at the pin and 0.509 with tsn-c-stack#32, against 0.70.
- **Settings:** the slice is 900 us (`rows_tiers.ruled` = `slice_choice`, least relative margin +0.0002, txL binding), P = 6 (`paced_rows.choice`), the join timer 19 cs.
- **No back-to-owner trigger:**
  - last 125.84, within 140;
  - txL 49.99, within 50 at 19 cs;
  - no lwSRP change;
  - every other row, the loads and the caps hold (section 6);
  - every join interval measured is in 180 to 240 (section 4).
- **The order of events.** The first moves (19 cs, P = 6, 900 us) gave last 117.19 and txL 49.70. The `srp` group's leg, run for the join gate, then refuted the stated build of one: 68,951 cycles against 430 us, refused at `ccb47e39` too. Restating it by the +5 % rule (725 us), and an owed MRPDU with it, put the last queued notice at 125.84, so the amendment moved its bound to 130.
- **Owed:**
  - the bench capture of the join intervals (contingent item 4); no bench access this round;
  - 8x8/2if's build of one, refuted (147,613 cycles, 1,550 us by the rule) and not restatable within the 1,300 us slice (`ctrl_loop.c:201`); an owner decision and a new Issue.
- **8x8/1if: STOP** on "the per-point slice built". The derived load is 0.698 (0.75) and the platform image is in section 6. The derived rows are in `receipts/model/rows-8x8-1if-final.txt`.

## 1. STEP 0 (ruling item 3)

Posted 16:49 CET as issuecomment-6857903645 (text: `STEP0-COMMENT.md`; receipt `receipts/model/step0-ccb47e39.txt`).
- 10 of 36 combinations held txL and the last queued notice: base 155 or 180 with ACMP 35, at P 8 to 11; base 155 with ACMP 80, at P 10 and 11.
- I continued without waiting.

## 2. The changes, with file:line and their reasons

### Lever (a), itemise: `5dc3fb35`

- **What:** ACMP's poll item is its send, with THE KEPT COMMAND's nested offers taken out. A declined offer is held to its own cost (20 us). The kept record's accepted re-offer is held to `record.acmp`.
- **Occurrence bound:** 2 a send + 1.
  - `acmp_mbx.c:111-128`: a declined record is kept, and the ring is not taken while it is.
  - `:157-175`: the redelivery offers the kept record first.
  - `:186-187`: each re-offer follows its own send.
  - tsn-c-stack `acmp.c:1309-1318`: the owed count drops only on a committed send.
- **Measured (M1):** the send at most 4,744 and 6,134 cycles (50 and 65 us); a decline 1,589 and 1,550 (20 us). Receipt `receipts/harness/m1-backlog-owed.txt`.
- **Files:**
  - `poll_items.py`, `poll_grade.py` (DECLINED/KEPT/OFFERS/DECLINES, `offers`, `offered`, `record_us`, `held`, STATED_US), `run.py` (`stated_misses`);
  - `rows_grade.py` (`acmp_items`, `rule_findings`; item 4's allowance), `rows_tiers.py`, `load_grade.py`, `flip_grade.py`;
  - `selftest_polls.offer_checks`, `selftest_mutants.py`.

### Lever (b), attribute: `fda4ef56` (docs)

- The register read accounts for 2 cycles and the hot list without `nvm_any` for 203.
- About 4,400 cycles are data-cache stalls on unchanged instructions: KLJ3's `nvm` grew from 296 to 552 B, and its 9 lines alias SRP's state's first 9 sets.
- Receipts are in `receipts/attribution/`.

### Lever (c), cut: `77a2da0b`, reverted by `5013dbc1`; the findings in `bbeb9299`

| Placement | Base, cycles | Rejected because |
|---|---:|---|
| V7: SRP's, then the store's | 14,514 | THE RETRY's rounds and AECP's item over their stated costs (`m2e-placement-v7-rounds.txt`) |
| V5: the store's alone | 14,545 | AECP's item over its stated cost |
| V10: no object moved | 17,878 | |

The loop schedules by `AECP_ROUND_COLD_US` and `AECP_NOTICE_US` (`aecp_mbx.c:202`, `:228`), so restating those costs would be a behaviour change.

### Move: the join timer at 19 cs, `158265c2` (contingent item 3)

- **`ctrl_loop.h`:**
  - `:333` `#define CTRL_LOOP_JOIN_CS 19u`;
  - `:348` `#define CTRL_LOOP_TX_BOUND_MS (240u - 10u * CTRL_LOOP_JOIN_CS)`, which was a typed 40.
- **`srp_mbx.c:29`:** `#define SRP_JOIN_CS CTRL_LOOP_JOIN_CS`. lwSRP is configured from it (`mrp_port_configure`, `srp_mbx.c:347-348`), so the donor is unchanged.
- **`srp_mbx.cpp:1524`:** the loop derived from `CTRL_LOOP_JOIN_CS`.
- **The model:** `rows_tiers.TX_BUDGET_MS` (`:115`) and `tier1_rows.join_cs`/`built_value`.
- **Controls:** `rows_tiers.py:935` (a typed 90u) and `flip_grade.py:181` (`TX_BUDGET_MS != 50`).
- **FR_NFR 3.4.1:** the bound paragraph.

### Gate: join intervals, `3d3afc17`, corrected by `0ab4e574` (contingent item 4)

- **`join_grade.py`** (new) has `released` and `intervals`. An interval is a participant's consecutive commits A < B, where B is a frame that a join timer's run-out E released (A < E < B, `mrpdu_grade.released`) and no periodic or LeaveAll timer ran out between them.
- **`mrpdu_grade.py`:** `released(log, entry)`, split out of `commits`.
- **`run.py`:** `print_joins` and the `stated_misses` words. **`grade.py`:** `passes['joins']`.
- **Why the correction.** lwSRP arms the join timer at a commit alone (`mrp_mad.c:1540`); `on_join_timer` only clears `join_wait` (`:850-855`). After a run-out with nothing pending (its builds send nothing), a later request sends at once.
  - The first definition counted that as a 715 ms interval at 1x1 and 720 to 783 at 8x8 (`receipts/harness/srp-join-definition-cc758286.txt`).
  - Under the corrected definition those logs give 188.09 to 190.03 ms (1x1) and 185.67 to 190.02 (8x8).

### Move: THE PACE at 6 ms, `1560e4f4`

`aecp_mbx.h:48` `AECP_PACE_MS 6u` (was 8u), with its comment, and FR_NFR 3.4.1's pace sentence. `paced_rows.choice` gives 6.

### The slice at 900 us, `dec9f1d7` (the slice ruling's rule)

- **`ctrl_loop.h:276`:** `CTRL_LOOP_SLICE_US (MBX_N_IF == 1u ? 900u : 1300u)`. The static asserts hold (`ctrl_loop.c:200-201`).
- **Checks:** the control text at `rows_tiers.py:881`; `selftest_round.py:108` [900, 1300].
- **Docs:** the srp README `:237-238`, the harness README `:127`, `:182` and `:1368`.

### The build of one restated, `7290f0f3`

- **`ctrl_loop.h:322`:** `CTRL_LOOP_BUILD_ONE_PASS_US (MBX_N_IF == 1u ? 725u : 1215u)` (was 430u), with its comment.
  - The `srp` group's build after its Listener Ready is 68,951 cycles at 1x1, and 725 us is that plus 5 %, rounded up to 5 us.
  - The firmware reads it only in a static assert (`ctrl_loop.c:201`), so the change is behaviour-neutral.
- **`poll_grade.py:87`:** mrpdu=725 (an owed MRPDU "stated at that pass's cost", `:71`).
- **`load_grade.py:169`:** the donor column's `item.mrpdu` and `build_one`, 725.
- **Evidence:**
  - the start head `ccb47e39` refuses the same pass (`receipts/harness/srp-1x1-start-head-ccb47e39.txt`), so it predates this round;
  - 8x8/2if measured 147,613 cycles, which would be 1,550 us, over the 1,300 us slice, so it is kept at 1,215 and reported refuted.

### Move: the last queued notice at 130 ms, `8cf7e2b7` (the amendment)

- **`aecp_mbx.h:64`:** `AECP_QUEUED_MS (MBX_N_IF == 1u ? 130u : 62u)`, with its comment.
  - Only the tests (`test_aecp.cpp:3081`, `:3094`) and the harness read it, so the change is behaviour-neutral.
- **`queued_bound.py`** (new):
  - `ruled(w)`: 125 while the row holds it, else 5 x ceil(w / 5); None past 140.
  - `stated`, `statements`, and `controls` (three plants).
- **`rows_tiers.py:200-203`:** `bounds_at` takes `AECP_QUEUED_MS` as the last row's bound at one interface. `rows_grade.BOUNDS` is untouched.
- **`flip_grade.py`:** `row_findings` adds `queued_bound.statements`, the controls run with the flip self-test, and `:244` derives the control text.
- **`selftest_notice.py:84-88`** expects (130, 62), with its over-the-bound case at 131. **`notice_window.py:59-61`:** the docstring.
- **FR_NFR 3.4.1:** the queued-notice paragraph, citing the amendment.

### Tests, twin and docs

- **`18e14164`:** `srp_mbx.cpp:294`, `:310`, `:1698-1701`; `srp_walk.cpp:74`, `:90`; `srp_latency.cpp:88-90`. These derive the JoinTime from `CTRL_LOOP_JOIN_CS`; they had expected 200/400 ms and failed at 19 cs (the firmware-unit job at `cc758286`). Each check stays an exact equality, or a bound at the armed time.
- **`f02457a6` (amended from `4d0168a4`):** `twin_compare.py` PLANT_WORDS for `table-10-3` (200 → 190), `mvrp-join-in` (212 → 200) and `mvrp-received-join` (31012 → 31010), and the milan_dp README table. Each plant is refused by the same finding (`receipts/twin/twin-plants-19cs.txt`).
- **`cc758286`:** `selftest_polls.named_checks`, split out of `polls_checks` (101 lines) for the long-function ratchet.
- **`5cbebb80`:** two SRP tests timed from the armed JoinTime, so their planted defects fail them by their own words at 19 cs. The first full pass, at `11c586a8`, had them escape.
  - `srp_mbx.cpp:735-747` (`SharedBindingsRetainTheListenerAndVlanUntilTheLastUnbind`) filters on `unbound=model.now_ms`, not a literal 1000 ms. Under `unbind-shared-listener` the Leave goes out at the 950 ms join opportunity, so the literal missed it.
  - `srp_rx_retry.cpp:385-389` (`OversizedValidRecordExpiresOnceAndReleasesOtherInterfaceAndBinding`) offers its record at `advance(2u*10u*CTRL_LOOP_JOIN_CS)`, 380 ms, not 400. Its 1000 ms expiry then falls on the second join count's end after the periodic MRPDU, the build that `build-reclaim-left-to-the-next-slice` breaks. The literal 400 aligned with it only at 20 cs: on scratch clones the mutant is caught at 20 cs and escapes with only the slice moved back to 800 us.
  - Receipt: `receipts/harness/pass1-failures-and-fixes.txt`.
- **`8a3791e4`:** `ctrl_configs.py` OUTSIDE names `queued_bound.py`. The first pass's TSN stack boundary step refused it: it names `aecp_mbx.h` and compiles nothing.
- **`64a19f03`, `2953091e`, `11c586a8`:** SPLIT_CONTROL_MEMORY section 13 (the THE TIERS table, the 1x1/1if table against both bounds, THE PACE bullet, "The contingent moves (#908)"), FR_NFR 3.4.1, the model's docstrings, and the srp and harness READMEs.

## 3. New checks, planted mutants and failing words

| Check | Plant | Failing words |
|---|---|---|
| ACMP's item is its send | `polls: an ACMP item carries the redelivery's offers (earlier rule)` | "an ACMP item is its send: the kept record's re-offer and the records the redelivery hands to their handler are subtracted from it and from the base" |
| A decline is told by its successor | `polls: no offer is the kept record's re-offer, so none is told declined` | "an offer the kept record's re-offer follows is declined and held to its own cost, ..." |
| A declined offer and the kept re-offer are held to their costs | `polls: no declined ACMP offer is held to its cost`; `polls: no kept command's accepted offer is held to its cost`; `polls: a kept command's accepted offer held to the send's cost, not the record's` | "a declined ACMP offer over its stated cost, and a kept command's accepted offer over the ACMP record's, are named, ..." |
| The declines' bound | `polls: the declined offers held to no bound`; `polls: the declined offers held to three a send` | "declined ACMP offers over two a sent owed frame and one are refused, named with the sends" |
| The declines' bound in a run | firmware plant `acmp-redelivered-every-poll` | "backlog-owed: 316 declined ACMP offers, over their bound of two a sent owed frame and one (12 sent)" |
| The rows count 2 a send + 1 | flip rule control | "declined ACMP offers at ... not the rule's ... (two an owed frame sent and one)" |
| A join interval, 180 and 240 hold | `joins: the range from the armed 190 ms` | "a join interval is two MRPDUs of one participant, the second one a join timer released: 180 and 240 ms hold" |
| Outside the range is named | `joins: no join interval held to its range`; `joins: the participants' applications not told apart`; `joins: any two MRPDUs, with no join timer between` | "a join interval under 180.0 ms or over 240.0 ms is named with its participant" |
| Periodic or LeaveAll MRPDUs, or no join timer, give none | `joins: a periodic or LeaveAll timer's MRPDU taken for a join's`; `joins: an MRPDU a join timer did not release taken for a join's` | "a participant's join intervals are its own, and two MRPDUs with a periodic or LeaveAll timer, or no join timer, between them are none" |
| An idle run-out releases nothing | `joins: an MRPDU a join timer did not release taken for a join's` | "a join timer that runs out with nothing to send, its build sending no frame, releases nothing, and the MRPDU a later request sends ends no join interval" |
| An interval outside fails the run | (verdict) | "a join interval outside its range fails a run whatever findings it records" |
| The MRPDU bound is derived | `#define CTRL_LOOP_TX_BOUND_MS 90u`; `TX_BUDGET_MS != 50` | "CTRL_LOOP_TX_BOUND_MS states 90 ms, not the timer budget's 50" |
| The slice is the rule's | `850u` | "the built design's slice not the rule's" |
| The pace is the model's | P plus or minus 1 | "aecp_mbx.h states AECP_PACE_MS P ms, not the model's 6 ms" |
| The last bound is the amendment's | `ruled` off its grid; `AECP_QUEUED_MS` at 125 or 135; a row at 140.01 | "the last queued notice's bound not the amendment's rule"; "aecp_mbx.h states AECP_QUEUED_MS 125 ms, not the 130 ms its row 125.84 ms rules"; "... past the amendment's 140 ms: the owner's" |
| The harness's queued bound | (selftest_notice) | "a queued notice's bound is the constants', the last queued notice's 130 ms at one interface ..." |

- **Self-tests at the final head:** the harness 0 failures, with 239 mutants caught and 0 escaped (226 at the start: 7 polls and 6 joins added); rows_tiers 969 of 969; flip 555 of 555; load 25 of 25.
- **The firmware suite** passes (68 arms).

## 4. 1x1/1if gate (ruling item 5, by every source)

| Requirement | Result | Evidence |
|---|---|---|
| txL ≤ its bound at the smallest P with R4L ≤ 240 | 49.99 ≤ 50 (19 cs), at P = 6; R4L 158.34 | `receipts/model/rows-1x1-final.txt` |
| The last queued notice ≤ its bound | 125.84 ≤ 130 (the amendment; over 125) | the same |
| Every other row in bound | section 0 | the same |
| Load ≤ 0.70 | 0.513 / 0.509 | `load_grade.py --check` |
| Every image within its cap | section 6 | the image gates |
| Join intervals, 180.0 to 240.0 ms, in the harness | 1x1 at the head's pre-check: 188.094 to 190.025 ms; the full pass's `srp` legs in section 6 | `receipts/harness/srp-1x1-11c586a8-precheck.txt`, `receipts/gates/harness-head-builds.txt` |
| The same on the wire (bench capture) | **owed**: no bench access this round | |

## 5. 8x8/1if gate (ruling item 6): STOP

- **Held:**
  - the derived load, 0.698 against 0.75 (0.971 with every AECP command the largest legal one, reported);
  - the platform image (section 6).
- **STOP: the per-point slice (1,070 to 1,300 us, build costs per shape) is not built.** `ctrl_loop.h` states the slice and the build costs by `MBX_N_IF` alone, and `rows_grade.py`, closed this round, reads them that way.
- **Reported only:**
  - the derived rows by every source (`receipts/model/rows-8x8-1if-final.txt`): R4 19.12, R5 143.96, R6 137.82, first 16.82, last 395.65, R4L 162.35, ACMP 48.80, ADP 48.02, MAAP 48.72, tx 67.86, txL 199.96;
  - the 8x8-1if harness legs (section 6);
  - the stated 1,590 us record, which is in the ledger.

## 6. Gate table

The final full pass is at `8a3791e44533d6b1cc26d486d0b18e7d83470dc1`, each part on its own clean clone and never piped (receipts `receipts/gates/`). The first pass, at `11c586a8`, is kept in `receipts/gates-11c586a8/`; it failed the two steps in section 2.

| Gate | Result | Receipt |
|---|---|---|
| The sweep, 4 shards (`native-shards.py`, label 894-r7g, CPUs 0-7, 8-15, 16-23, 24-31) | exit 0 each; 65 suites, 2,713,040 checks, 0 failures | `sweep-shard{0..3}.txt` |
| Every hosted job step of rtl-fast, rtl, elaborate and docs (`run_wf.py`; `verify_wf.py ... --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4`) | 139 run, 0 bad; 226 not run with a reason | `workflows-verify.md` |
| The firmware jobs (unit, control, AECP and SRP mutation campaigns, boundary, Verilator) | every step 0; SRP campaign 0 escaped | the same |
| Lane gates, part a | 37 at 0; 4 at their expected 1 (8x8/2if reported): `rows_tiers --terms`, `flip --check`, `--point 8x8/2if`, `--design as-built` | `lane-summary.txt`, `lane-*.txt` |
| The harness self-test | 0 failures; 239 mutants caught, 0 escaped | `lane-harness_selftest.summary.txt` |
| `flip_grade.py --check --point 1x1/1if` | PASS | `lane-flip_check_1x1.txt` |
| `tier_grid.py --point 1x1/1if` | exit 0, the built design at 900 us | `lane-tier_grid.txt` |
| rows_tiers, flip and load self-tests; `load_grade.py --check` | 969/969, 555/555, 25/25; 0.513 and 0.509 | `lane-*.txt` |
| em-dash, idioms, docs, diff-checks (9 bases), `ctrl_hot` | 0 | `lane-*.txt` |
| BDD | 511 scenarios passed | `lane-behave.summary.txt` |
| `make twin`, `make twin-plants` | 0 findings; every plant refused | `lane-twin*.summary.txt` |
| Lane parts b and c (builder tests, NVM self-test, boot 1x1, 8x8, native and plants) | 0 | `lane-*.summary.txt` |
| Harness legs at 1x1 (`datapath-events`, `notice-every-0`, `aecp-largest-notice`, `backlog-owed`, `srp`) | exit 0; the plant control `acmp-redelivered-every-poll` caught | `harness-head-builds.txt` |
| Harness legs at 8x8/2if | four groups exit 0; `srp` exits 1 on the refuted build of one (reported) | the same |
| Harness legs at 8x8-1if | exit 1, reported (8x8/1if STOP): build-one over its one-interface statement; the answering arm refuses to build, as in round 6 | the same |
| Join intervals, every leg | 52 in 14 group runs, 185.668 to 190.025 ms | the same |
| Every image (`qall.sh` at `11c586a8`; no firmware source change since) | 1x1/1if 40.5 and 42.5; 8x8/1if platform 56.0 (cap 56); 8x8/2if 59.0 and 60.0 | `receipts/images/every-image-final.txt` |
| The model at the head | `receipts/model/rows-1x1-final.txt`, `rows-8x8-1if-final.txt` | |

## 7. Run history

- 16:47 CET: start. 16:49: STEP 0 posted.
- 16:53-19:58: the levers. 20:02: a full pass at `bbeb9299` (the STOP plan), stopped as obsolete once the contingent ruling applied; it is not evidence.
- 20:38-20:48: the moves (`158265c2` to `2953091e`).
- 20:47: pre-checks at `cc758286`:
  - the harness self-test passed;
  - the firmware-unit job failed on the SRP tests' 200 ms JoinTime, fixed in `18e14164` (all 68 arms then pass);
  - the `srp` legs at 1x1 and 8x8 showed the first join definition's 715 to 783 ms "intervals" and the build-one overrun.
- 21:02-21:31:
  - the start head's `srp` leg (`ccb47e39`) also refuses the build of one;
  - the twin passes, but three twin plants escaped on their 20 cs timestamps;
  - fixed: `0ab4e574`, `7290f0f3`, `8cf7e2b7`, `f02457a6` and `11c586a8`.
- 21:35-21:43: pre-checks at `11c586a8`: the harness self-test (0 failures), the firmware suite (PASS) and the 1x1 `srp` leg (exit 0, JOINS 188.094 to 190.025) all passed.
- 21:44-22:54: **the first full pass, at `11c586a8`.** The sweep's four shards exited 0, and every lane gate and harness leg had its expected exit. The step verifier found 139 steps run, 226 not run with a reason, and 2 bad:
  - the TSN stack boundary (`queued_bound.py` unlisted);
  - the SRP mutation campaign (two mutants escaping their words at 19 cs).
  - Its receipts are kept in `receipts/gates-11c586a8/`.
- 22:55-23:00: fixed in `5cbebb80` and `8a3791e4`; the two mutants were re-run alone at both join times.
- 23:00: **the second full pass, at `8a3791e4`.** The sweep's shards run on 0-7, 8-15, 16-23 and 24-31, and the dispatcher's 33 units on 32-95, at most 12 at once.
- 21:44: the full pass at `11c586a8`, on CPUs picked by `cpu_ranges.py`.
- 00:13: the second pass completes. The sweep's four shards exit 0; 139 steps run, 0 bad; every lane gate and leg is at its expected exit. Collected by `scripts/collect.sh`.
- 00:19: re-checked before posting: dev-soft-core still `cec88385`, no new comments on #894 or #908, the tree clean at `8a3791e4`. 00:20: REVIEW READY posted (issuecomment-6867318907), the round's second and last comment.

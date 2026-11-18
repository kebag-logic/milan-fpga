# HANDOFF r1: [A794] flip-train composition, steps 1-7 (#665)

Status: **STOP** posted on #665 (issuecomment-6942842392): step 7, #931 `d06ded5a`, and step 5, #933 `1a1e6665`,
require opposite behaviour of the product SoC build past 56 RAMB36 (`own_point` against `product_point`), each pinned by
its memory test, under one ruling (#923's of 2026-11-16) that does not settle which (section 6, F2). After the STOP,
#914's head moved to its frozen `e1ecce20` and the branch was recomposed on it: steps 1 to 6 are in `flip-train-1117`
at `7431b6ba` (the first composition is kept under `refs/ref/compose-on-914-8883d499`). Step 7's decision-independent
files are resolved in scratch. Local only; nothing pushed.

**Found after the STOP (not posted; STOP-ADDENDUM.md): a second STOP condition, provisional.** On a probe of step 7,
the composed image's largest legal command record is 99,468 CPU cycles, 1,045 us by the rule, over `LONG_RECORD_US`'s
975 us at 1x1/1if (#931 measured 92,714 on its own head, 975 by the rule), and the statement survey finds `event.AECP`
(80 against 75), `event.MAAP` (170 against 165) and two datapath events (40 against 35) under the composed measurement.
Restated by the rule, three 1x1/1if rows by every source pass their bounds: the last queued notice 142.44 ms (past
140), ACMP 32.89 ms (30), txL 49.66 ms (49); the load 0.523 holds (section 3.1, F3).

**Also found after the STOP (not posted; STOP-ADDENDUM.md): a third STOP condition.** #938 makes the store step every
pass while a save is in flight, and #933's PHY client runs a PHY frame only in a call whose store took no save step, so
the composed platform polls no PHY during a save. #933's `Phy.B12StepCarriesTheStoresSaveOrAPhyFrame` fails on the
composed tip, if1 and if2 (F4).

TAKEN: #665 issuecomment-6939741872.

## 0. Lane

- Branch `flip-train-1117`, from dev-soft-core `cb96336d` (verified equal to origin/dev-soft-core at start; submodules initialised, `git submodule status` clean).
- Owner rules: #665 issuecomment-6939460730 (option B, one train candidate), issuecomment-6939574513 (freeze; compose once; one composition review; one merge).
- Dry plan: the manager's train plan (step 1 conflicts on 18 paths; per-PR conflict lists for later steps).
- The #881 lane's partial sync onto `cb96336d` (its local branch, fetched into a private ref of this lane, `59fe35b5` plus its ledger commit `c4860141`) is used only as a reference for how its conflicts were resolved.
- Commits carry one-line subjects and no trailers (CONTRIBUTING 2.2); the git identity is the lane's own.

## 1. Steps

The branch now holds the **recomposition on #914's new head** (section 9); the first composition, on #914's
`8883d499`, is kept under `refs/ref/compose-on-914-8883d499` (`47f77284`).

| Step | PR | Frozen head | GitHub head checked | Merge (fix) | Conflicted files | Quick checks |
|---|---|---|---|---|---|---|
| 1 | #881 | `d3e61e37` | equal, before the merge | `43b954e6` | 18 (the plan's 18) | all pass; the all-points flip check fails only on 8x8/2if, the base's same eleven findings; firmware suites rc 0; control campaign (run at the first composition's step 2, identical platform files) rc 0 |
| 2' | #914 | `e1ecce20` | equal, before the merge | `877c99e4` | 12 | all pass: harness self-test 0 failures, record classes 20/20, `shape_costs` 25/25, `egress_ledger` 15 mutants, 1x1/1if flip PASS, 8x8/1if `tx_held` HELD (75 against 74.26); firmware suites and SRP campaign rc 0 |
| 3' | #918 | `394612c5` | equal, before the merge | `9c0e1974` (`6fef44b8`) | 7 | light gates at `6fef44b8` pass; the all-points flip findings are the base's; 8x8/1if `tx_held` HELD |
| 4' | #935 | `37255683` | equal, before the merge | `22a82038` | 2 | light gates pass; flip findings the base's |
| 5' | #933 | `1a1e6665` | equal, before the merge | `2078c438` | 13 | light gates and `fw_coverage --check` pass; coverage ratchet regenerated, identical to step 5's |
| 6' | #938 | `81c9a1a0` | equal, before the merge | `7c28f53f` (`7431b6ba`) | 5 | on the identical tree `fd050aec`: every gate passes, the harness self-test 0 failures (with the split mutant table), the idiom gate rc 0; at the tip: the four firmware shards (running) |
| 7 | #931 | `d06ded5a` | equal at the dry run | not merged: **STOP** | 15 | decision-independent files resolved in scratch |

First composition (on `8883d499`), for the record: `43b954e6`, `136e64ce`, `874bd403` (`d7941d4d`), `d21f7aab`,
`89eea108`, `13da58de` (`47f77284`); every check listed in RESOLUTIONS passed there.

Not composed this round (round 2, on the manager's heads): #934, #932, #936.

Each step's resolution rows: RESOLUTIONS.md.

## 2. Commits after the merges (composition fixes, regenerations)

| Commit | File:line | Change | Reason |
|---|---|---|---|
| `7431b6ba` (recomposition; replaces `47f77284`) | `tb/verilator/ctrl_service_budget/grade.py`, `run.py`, `selftest_round.py` x3; `sw/firmware/ctrl/test/aecp_mutants.py:688`; new `tb/verilator/ctrl_service_budget/selftest_mutants_burst.py` | `grade.grade`'s `interfaces` and `shape` folded into `at`; one comment rewrapped; #938's five burst mutants and their helper moved to their own module, spread back into `MUTANTS` first | as `47f77284`, and #914's round 13 added 13 lines to `selftest_mutants.py`, so the union (1,018) needs more than layout; the mutant table's keys, order and values are AST-identical (272) |
| `6fef44b8` (recomposition) | as `d7941d4d` | the same patch | as `d7941d4d` |
| `47f77284` (first composition) | `tb/verilator/ctrl_service_budget/grade.py:943-948`, `run.py:598`, `selftest_round.py:75,140,204`; `sw/firmware/ctrl/test/aecp_mutants.py:688`; `tb/verilator/ctrl_service_budget/selftest_mutants.py` (five dict entries) | `grade.grade`'s `interfaces` and `shape` folded into `at` (its callers pass `shape or interfaces`); one comment rewrapped; five entries joined onto one line each | #914's `shape` and #938's `journal` gave `grade.grade` seven parameters (`MAX_PARAMETERS` 6, ratchet full at 7); each side left the two modules within 1,000 lines and the union was over; both modules' ASTs are unchanged |
| `d7941d4d` | `tb/verilator/ctrl_service_budget/build.py:390,640,877`, `grade.py:220` | three comment blocks rewrapped to 120 columns, one comment moved onto its `elif` line; words and AST unchanged | each side left `build.py` at the idiom gate's 1,000-line module limit and `grade.parse` at 100 and 98 of its 100-line function limit; the union broke `check_py_idiom.py` (long module 11 > 10, long function 10 > 9); a ratchet may not be raised |

## 3. Composed figures

Owed after step 7: the CPU service-budget harness at 1x1/1if and 8x8/1if, the record classes, the in-tree statement
survey, the ROM ledger at every point, the release image identity, and both split routes (the composed gateware
differs from every PR's own head: #881 moves `milan_datapath.sv` and `milan_soc.py`, #918 `KL_mbx_rx.sv`, #933 and
#931 `milan_soc.py`).

### 3.1 CPU service-budget harness

Provisional, 1x1/1if only: a probe tree (step 7 merged in a throwaway worktree, the undecided ledger hunks taken from
#931, nothing of it in the branch) measured with the formal legs: arm A in 8 parts, the answering-every-port arm in
2, the valid-destinations arm's `srp-talker`, `srp-talker-loss` and `srp-talker-held`, the answering-ports arm's `aecp`,
`aecp-fanout`, `aecp-largest-notice` and `aecp-reboot`. It shows early whether the composed costs force restatements or
break a bound. It is not the composed measurement: the harness hashes the firmware tree, the coverage ratchet and
`ctrl_memory.py` into each build, so the final figures need a run at the final head. 8x8/1if waits for #914's new head
(R844-4-F1 moves that image).

Probe at `9f5a305f` (throwaway; not in the branch), 1x1/1if, built at 10:22:

| Leg | Groups | Result |
|---|---:|---|
| arm A, 8 parts | 99 | 0 refusals; 7 budget misses, all `backlog-owed`'s held-egress rows (61.8 to 63.7 ms, the ruled recorded misses); 0 `STATED`; 0 passes over the share |
| answering-every-port, 2 parts | 16 | 0 refusals, 0 misses (280 probe instances), 0 over the share; the longest queued notice 23.37 ms against 140 |
| answering-ports (`aecp`, `aecp-fanout`, `aecp-largest-notice`, `aecp-reboot`), 2 parts | 4 | 0 refusals, 0 misses, 0 over the share |
| valid-destinations (`srp-talker`, `-loss`, `-held`), 3 parts | 3 | `-loss` and `-held` 0 refusals, 0 misses; `srp-talker` too: 0 refusals, 0 misses |
| saves | 4 | durable within their stated worst cases (save-held 1,096.5 of 4,070 ms; save-second 6,030.4 of 6,070) |
| record classes | | FAIL: the largest legal command's record 1,045 us by the rule over 975 (F3); every other class within |
| tier model with that record restated (1,045) | | txL 49.31 ms over 49 (F3); every other 1x1/1if row within |
| statement survey (all 15 legs) | | 5 statements under the measurement by the rule: `event.AECP` 80 against 75 (both columns), `event.MAAP` 170 against 165, `AS_PATH_CHANGED` and `AVB_INFO_CHANGED` 40 against 35; everything else within |
| tier model with every restatement | | last 142.44 ms over 140 (the amendment's ceiling), ACMP 32.89 over 30, txL 49.66 over 49; R4 13.50, R5 77.02, R6 74.50, first 14.78, R4L 203.70, ADP 28.32, MAAP 28.41, tx 34.54 within; load 0.523 within 0.70 |

### 3.2 Record classes, statement survey

### 3.3 ROM ledger

### 3.4 Release image identity

At step 5 (`89eea108`, which carries #881's and #933's SoC changes) against `cb96336d`, each the AX7101 1x1 all-fabric
export without Vivado (the launcher's dry run and its `milan_soc.py` command without `--build`):
`software/bios/bios.bin` and `aem_desc.bin` byte-identical; `bios.elf` identical with debug sections stripped, and its
disassembly identical; every gateware file equal after path normalisation but the top Verilog, which is equal outside
its comments (a date stamp and the hierarchy listing). Repeated at the final head.

### 3.5 Routes

## 4. Gate table

There is no final head this round (STOP at step 7). These ran at the recomposed tip `7431b6ba` (steps 1 to 6), on a
clean clone or on the identical tree `fd050aec`:

| Gate | Command | Result | Receipt |
|---|---|---|---|
| docs gates | `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `gen_toc.py --selftest`, `check_em_dash.py --base cb96336d` | pass | receipts/steps/s6b/ |
| idioms, hygiene | `check_py_idiom.py`, `check_cpp_idiom.py`, `check_hygiene.py --check` | pass (with the fixes) | receipts/steps/s6b/ |
| harness self-test | `run.py --self-test` | 0 failures | receipts/steps/s6b/ |
| harness model and self-tests | `rows_tiers --selftest` 1033/1033, `record_classes --selftest` 20/20, `load_grade --check` and `--selftest` 28/28, `flip_grade --check --point 1x1/1if` PASS, `--selftest` 612/612, `shape_costs --check` and `--selftest` 25/25, `egress_ledger --selftest` 15 mutants | pass | receipts/steps/s6b/ |
| all-points flip check | `flip_grade.py --check` | FAIL on the base's same eleven 8x8/2if findings only; 8x8/1if `tx_held` HELD (75 against 74.26) | receipts/steps/s6b/flip_check.log |
| ledger test | `test_ctrl_memory.py` | PASS | receipts/steps/s6b/ |
| firmware suites | `test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4` | **FAIL**: platboot `Phy.B12...` at if1 and if2 (F4) | receipts/firmware/tip-fw0.log |
| control campaign | shard 1/4 | **FAIL**: 792 of 793 caught; the escape, `plat-phy-store-owed-dropped`, plants into the B12 test that already fails at the baseline (F4) | receipts/firmware/tip-fw1.log |
| AECP campaign | shard 2/4 | PASS | receipts/firmware/tip-fw2.log |
| SRP campaigns | shard 3/4 | PASS | receipts/firmware/tip-fw3.log |
| coverage | `fw_coverage.py --check` | PASS at step 5' (`2078c438`) | receipts/steps/ |
| release image | the AX7101 1x1 export against `cb96336d` | identical (first composition's step 5) | receipts/release/ |
| CPU budget harness, 1x1/1if | the formal legs on a step-7 probe | see section 3.1; F3 | receipts/legs/, receipts/budget/, receipts/survey/ |

Not run, owed to the final head: every workflow job end to end (`run_wf.py`/`verify_wf.py`), the elaborate legs, the
twin and twin-plants, the 4-shard verilator sweep, the 8x8/1if harness, the ROM ledger (`plat_ledger.py`) at every
point, both split routes.

## 5. New checks (planted mutant, failing words)

None so far: the composition added no check of its own. Step 2 added a constant, `record_classes.REBOOT_PATH_POINT`,
naming the one point (1x1/1if) where the train's REBOOT and GET_AS_PATH completeness checks apply inside #914's
per-point loop; the self-test's existing controls cover both sides (20 of 20).

## 6. Findings reported (not fixed)

- **F4 (firmware, a design decision).** THE STEP: #938's store steps once a pass during a save (#920) and #933's PHY
  client yields its frame to any save step (#919), so the PHY starves for a save's length (about 1.1 s typically, up to
  6 s at 1x1/1if, 22 s at 8x8 by the stated worst cases). `test_plat_boot.cpp`'s
  `Phy.B12StepCarriesTheStoresSaveOrAPhyFrame` fails at the tip `7431b6ba` (receipts/firmware/tip-fw0.log). The
  first composition never ran the firmware suites at step 6, my omission; the step-5 tree passed them.

- **F3 (bounds, provisional; after the STOP).** The composed image's `aecp-largest-notice` record: 99,468 CPU cycles
  (arm A) and 99,397 (arm B), 1,045 us by the rule, against `rows_tiers.LONG_RECORD_US` 975 us at 1x1/1if; the record
  classes refuse it. The survey adds `event.AECP` 80 (75), `event.MAAP` 170 (165), `AS_PATH_CHANGED` and
  `AVB_INFO_CHANGED` 40 (35). Restated by the rule, the 1x1/1if rows by every source: last 142.44 ms against 140, ACMP
  32.89 against 30, txL 49.66 against 49 (`flip_grade.py --check --point 1x1/1if` on scratch copies; receipts/survey/). Not fixed: a bound and the
  rule may not move here, and a cut in the AECP record path would be a change of a PR's own behaviour.

- **F2 (the STOP).** #933's `ctrl_memory.product_point` (only `product`-flagged entries planned by
  `milan_soc.add_ctrl_memory`) and #931's `ctrl_memory.own_point` (every `LEDGERED` entry) differ on a product build of
  the size fixture's and the platform's 8x8 two-interface images: refused by #933, planned at 59.5 and 61.0 by #931.
  #933's `test_ctrl_memory.py` requires the refusals (and two planted ledgers on the flag); #931's requires the builds.
  Both cite #923's ruling of 2026-11-16. Decision asked: (a) #931's reading (recommended, the ruling's sentence as
  written) or (b) #933's.

- **F1 (test hygiene, pre-existing).** `test_ctrl_firmware.py --self-test --shard 0/4` and `3/4` write
  `dispatch-build/keys/keys-16x4.yaml` and `keys-16x32.yaml` into the checkout, untracked and not ignored (found on
  clean clones at steps 2 and 4, so before #935). Not the composition's.

## 7. Not done, and why

- **Step 7 (#931)**: STOP, a decision is owed (F2). Its decision-independent files are resolved in scratch
  (RESOLUTIONS, step 7).
- **The composed measurement and the final gates**: there is no final head. Three bound-level findings (F3, F4) also
  need decisions before the figures can be restated. The 1x1/1if harness ran on a probe only.
- **The figures two PRs restate** (sizes in the ROM ledger, the paced and other stated costs) are still the
  provisional larger values; they are restated from the composed image once it exists.

- PR-BODY.md: the round's instructions name both "Closes #665" and "Relates to #665". #665 is the flip issue, which
  the flip PR closes, and the train must not, so the body carries "Relates to #665" only (with #871 and #894), and
  "Closes" for #917, #929, #919, #920, #923, #924 and #930, each the issue its PR closes. Change if the manager wants.

- Step 2 was merged before step 1's control campaign (shard 1/4) finished; its suites (shard 0/4) had passed. The
  restart cut that campaign; it was run instead at step 2, whose platform files are identical to step 1's (`git diff
  43b954e6 136e64ce` over them is empty), rc 0.

## 9. #914's head moves: the recomposition

- Both reviews of #914 at `8883d499` are NEGATIVE (R843-5, R844-4). The instructions say its head then moves and the
  composition restarts from step 2. At 08:20 its GitHub head was still `8883d499`.
- Until the new head arrives, steps 3 to 7 are composed on the current step 2, so their resolutions are done once:
  `git rerere` is enabled in the lane and holds every resolution (step 2's recorded in a throwaway worktree from
  `136e64ce`); each step's hand resolutions are also kept as files in scratch.
- 10:2x: #914's head moved to `d0a2a160` (round 13: 8x8/1if's `CTRL_LOOP_TX_MS` 75 ms, the hold-off 2,027 cs there,
  8x8/1if's rows derived in-tree; 11 files). R844-5 POSITIVE and R843-6 NEGATIVE at that head (10:38, 10:39 UTC), so
  it is not frozen and may move again; the recomposition waits for a frozen head. `d0a2a160` changes `ctrl_loop.h`,
  `srp_mbx.c` and the harness's `flip_grade.py`, `load_grade.py`, `rows_grade.py`, `rows_tiers.py`, which the
  composition also touched, so its recorded resolutions will be replayed and rechecked there.
- 11:2x: #914 moved again, to `e1ecce20` (FR_NFR's 8x8/1if hold-off at 2,027 cs; a control that `flip_grade.py --check`
  reports tx_held's refusal at 8x8/1if). R843-7 POSITIVE at `e1ecce20` (11:49 UTC) and R844-5 POSITIVE at its ancestor
  `d0a2a160`, whose later delta R843-7 covers: two positives by the owner's rule, so the recomposition starts on it.
- On the new head: keep this composition under a backup ref, reset the branch to step 1 (`43b954e6`), merge the new
  #914 head, then steps 3 to 7 again, each conflict checked against its recorded resolution and the quick checks rerun.
  The measurement after step 7 carries only where the composed images are byte-identical.

## 8. Environment notes

- CPUs 0-95 were fully booked by other lanes at the start (`cpu_ranges.py show`: 128 busy), so every unit of this lane
  runs on the session pool 96-127; host load average about 140 on 128 CPUs.
- The host was shut down at 07:25 and back at 08:00 with 96 CPUs (session pool 64-95; bookings from 0-63). Every unit
  without a recorded rc was treated as cut: its half-written output moved to `logs/cut-by-restart/` and the check rerun.
- A firmware campaign leaves two untracked files in its checkout, `dispatch-build/keys/keys-16x{4,32}.yaml` (seen at
  steps 2 and 4); pre-existing, reported in section 6, not fixed.
- A check runner backgrounded from a tool call (not in a unit) lost its harness self-test without an exit status; the
  self-test was rerun in its own unit. Long checks now run only in units.

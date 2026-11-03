[R711] NEGATIVE - exact head a3f23bbabdd9800177224432361fcd41b53bf882

# R711-4: internal review of PR #810 (#665 S2b), round 14

- Head `a3f23bbabdd9800177224432361fcd41b53bf882`, tree `677a44180c838c11ce0852c618cee0b09a63b2be`.
- Base `dev-soft-core` `a68536fa`. Delta judged: `4f58214f..a3f23bba`, 11 commits, 43 files.
- Judged against the round 14 assignment (#665 issuecomment-6589337173) and my round 13 findings (R711-3).
- Authorities: AGENTS.md sections 6 and 7; #665's body and its owner decisions of 2026-10-31; the owner's 0.5 s save (#823 issuecomment-6545894131 and -6545924397); `ctrl_loop.h` (THE BOUND, THE SHARE, THE STEP); `nvm_store.h`; `SPLIT_CONTROL_MEMORY.md` sections 13 and 14.
- Role: internal reviewer, cleared context. All five lenses were applied.

## Verdict in one paragraph

The age limit is a correct mechanism, and it bounds a save's progress.

- With the limit, the starved save is durable within its stated bound at both points.
- Without it, the save never completes, and the named control catches that.
- The SRP orientation fix, the step-pass figures and the verify-phase guard each resolve their round 13 finding at its cause.

The verdict is NEGATIVE on two new MAJOR findings, one for each of the two shared deliverables:

- **F1.** "No aged step lands among a window's records" holds only for windows that open from idle. Under the PR's own starved input, an aged step does land among a composed window's records, in 23 of 39 probe windows. The published least margin of 0.77 ms becomes 0.16 ms (17.84 ms against 18). No probe row went over its bound, but item 1 says to measure this, not assume it, and the case is not staged.
- **F2.** The stated worst case, 12,110 ms at 8x8/2if, does not hold for a change made while a save is in flight. That change waits for the save in flight, then for its own. A probe at 1x1 measures it at 5,609 ms against the stated 4,070 ms. The same derivation gives about 22.1 s at 8x8/2if.

Three RESIDUEs and three suggestions follow.

## Method

**Context, in order:**
- AGENTS.md;
- #665's body and the round 14 assignment;
- #823's decisions;
- the diff `4f58214f..HEAD`, with `ctrl_loop.c` and `nvm_store.c` read whole at the step and the store's phases;
- the author's public packet `review-evidence/665s2b-r1/author-r14` at evidence commit `73deb391c6b81dfa26040c565dcf988cb3519e1a`.

I read the prior public findings (R711-3, R712-3) only after my own pass over the diff.

**Evidence integrity:**
- The evidence commit is unsigned (GitHub verification: unsigned). Its integrity rests on `MANIFEST.json` (sha256 `aacae9c7150bcd20445edf7624c05b8be7e8586f1ca030f9d0be5672af5dceed`).
- The 24 receipts I relied on all match their `published_sha256`: 0 bad, 0 missing (`receipts/evidence-manifest-check.txt`).
- The live PR body equals the packet's `PR-BODY.md` except for one trailing newline.

**Recomputed:**
- The bound arithmetic (`receipts/bound-recompute.txt`), from the containers 13,256 B and 3,336 B (`nvm_stage` less its 8-byte look-ahead):
  - 8x8: S = 1 + 3 + 52 + 2 + 104 + 104 + 104 = 370, so T = 12,110 ms;
  - 1x1: S = 102, so T = 4,070 ms.
  - These match `save_window.bound_ms` and the doc.
- The gate tables against the measured legs, by blob hash:
  - `gates/harness/G-A8/table.md` = `measure/N-A8/table.md` (`378e4600…`);
  - `G-A1` = `N-A1` (`77674b27…`).
- Section 14's S column, from arm A's 1x1 figures: for example, the last AECP record is 15.93 + 24 × (13.66 − 10.04) / 7 = 28.3.

**Probes:** all were run in disposable copies of the head, at 8x8/2if, arm A, without the drafts, CPU on `sys` at 100 MHz, unless stated otherwise.

- **Probe images.**
  - The 8x8 probe image `ctrl_app.elf` is byte-identical to the author's measured `N-A8` image (`a7d77f31…`, `receipts/probe-images.sha256`).
  - The unmodified control window `backlog-adp@blank-0` reproduces the published last SRP record exactly: 17.23372 ms, 1,723,372 cycles.
- **P1, P1b and P1c (F1):** `scripts/plant_aged_window.py`, then the edits in `receipts/p1-probe-tree.diff`.
  - Each probe is backlog-adp's composed save window, opened after a grandmaster-change flood (`flood gm`, the same input `save-starved` uses). The flood stops before `scenario.OPEN_WINDOW`, so the window's population is unchanged and the step's age is not zero when it opens.
  - The phases sampled:
    - P1: the blank phase, F = 30 to 57 ms after its lead-in;
    - P1b: the program and verify phases, F = 45 to 59 ms;
    - P1c: blank-0's exact opening instant, with the flood inside its 30 ms lead-in, I = 19 to 29 ms.
  - Analysis: `scripts/analyse_aged_window.py`. Receipts: `receipts/p1*-analysis.txt`, `p1*-table.md` and `p1*-run.log`.
- **P2 (F2):** `scripts/plant_second_change.py`, at 1x1. It is `save-starved`'s flood with a second SET_NAME of the entity, to another value, 1,500 ms after the first.
  - Analysis: `scripts/analyse_second_change.py`. Receipts: `receipts/p2-*`.
- **Hosted checks:** the exact-head check runs were snapshotted (`receipts/hosted-checks-snapshot.tsv`).

**After the probes:** the review clone is at `a3f23bba`, tree `677a4418…`. Its worktree and index match HEAD, and the six submodule gitlinks are unchanged.

## Findings

### R711-4-F1 - MAJOR - Conformance, RTL (architecture), Robustness, Tests, Docs - an aged step does land among a window's records; the stated reason for N = 2 and the least margin are not what the head does

**Where:**
- `sw/firmware/ctrl/loop/ctrl_loop.h:146-150`: "Two: in every window the budget stages … no aged step lands among a window's records, the least of whose margins (0.77 ms) is below a step".
- `docs/design/SPLIT_CONTROL_MEMORY.md:1440-1444` ("Why two") and `:1589`, where the least margin is given as 0.77 ms.
- The PR body: row 1 of the acceptance table, `:128` and `:354`.
- The REVIEW READY's acceptance 1.

**Authority:**
- Round 14 item 1: "keep every row and every pass within its bound. The least margin, 0.71 ms, is below the longest step, 0.954 ms, so measure this; do not assume it."
- THE BOUND (`ctrl_loop.h:33`): "it costs the input one step's time".

**Evidence:**
- The author's argument comes from windows staged from idle. There the step's age is 0 when the window opens, and at most two centiseconds pass before the next step (`analysis/stepgaps-*`).
- The age counts the centiseconds dispatched since the step last ran. Before a window, input that leaves no pass empty raises it to 2. The PR's own `save-starved` is such input: "an event source the contract coalesces but does not rate" (`:1459`, harness README `:97`).
- The composed burst's buckets refill during that flood, because the flood is events, not records. So a full composed window can open with the step's age at 2, and its first dispatched centisecond then admits an aged step among its records.
- **Measured.** In 23 of 39 probe windows an aged pass ran before the last SRP record was answered. It is identified by a pass whose cycles are the store's plus about 400: for example 76,860 against 76,455, or 77,736 against 77,331.
  - Verify phase, all 8 windows, a 0.78 ms read-back taken aged:

    | Window | F45 | F47 | F49 | F51 | F53 | F55 | F57 | F59 |
    |---|---:|---:|---:|---:|---:|---:|---:|---:|
    | Last SRP record, ms | 17.69 | **17.84** | 17.41 | 17.55 | 17.71 | 17.64 | 17.04 | 17.14 |

    The verify phase's idle-start windows give 16.46 to 17.02 ms (`N-A8/table.md`).
  - Blank phase, the 5 of 10 P1 windows where a 0.77 ms read-back was taken aged: 17.12 to 17.37 ms.
  - Program phase, all 8 windows: the aged steps were page-program waits of 0.06 ms, at 16.34 to 16.84 ms.
  - P1c, 2 of 11 windows: 16.97 and 17.29 ms.
- **What the measurements show.**
  - No row was over its bound: 0 budget misses and 0 passes over the share in all four runs.
  - The least margin is **0.16 ms**, not 0.77 ms, and it is below a read-back step (0.77 ms).
  - The sentence "no aged step lands among a window's records" is false at the head.
  - The heaviest compositions are unmeasured, because the probes sample, not sweep. Two are open:
    - an aged step at the worst idle-start phase, `blank-0` at 17.23 ms, plus a 0.77 ms step;
    - an aged page-program issue (0.97 ms) in a program window.

**Impact:**
- The acceptance's "every row within its bound" rests on a reason the head does not have.
- The published least margin overstates the room by 0.61 ms.
- The harness stages no window opened with the step aged, so a regression that moved the last SRP record past 18 ms in that case would pass every gate.

**Required outcome:**
- Stage the composed windows with the step's age at `CTRL_LOOP_STEP_AGE` as they open, in every flash phase and at the tick phases the windows already sweep. The program phase needs an aged page issue among them.
- Report the rows and the least margin from those windows. If a row is over its bound, take another N, change the mechanism, or STOP with the residual.
- Restate `ctrl_loop.h:146-150`, the doc's "Why two", `:1589` and the PR text from what is measured. The point to keep: an aged step can land in a window, and the rows fit with it.

**Verification:**
- The new groups at 8x8/2if in both arms, with every row within its bound and the least margin stated.
- A plant that makes the aged step heavier, or that lowers N to 1 with the opening age forced, is caught by a named row.

### R711-4-F2 - MAJOR - Conformance, RTL (architecture), Robustness, Tests, Docs - the stated worst case is not a change's worst case when a save is in flight

**Where:**
- `sw/firmware/ctrl_nvm/nvm_store.h:16-28`: "a save is durable at most MILAN_NVM_DEBOUNCE_MS after its first change, plus…".
- `docs/design/SPLIT_CONTROL_MEMORY.md:1447-1453`: "under any input, so a save is durable at most T ≤ 1,000 ms + S × 3 × 10 ms + 10 ms after its change".
- `tb/verilator/ctrl_service_budget/save_window.py` `bound_ms` and the harness README `:98`.
- The PR body `:18` ("A SET_NAME of the entity is durable at most 12,110 ms") and row 2 of its acceptance table.

**Authority:** round 14 item 2: "State the worst case of a save from the change to durable at 8x8/2if, derived from N, the step count and the tick". #823 states the save bound as "from the change to durable in flash, worst case".

**Evidence:**
- **Code.**
  - `nvm_mark` (`nvm_store.c:819-833`) takes a change into the running save only while the capture has yet to reach its record. Any other change opens a first-dirty window of its own.
  - `nvm_idle` alone begins a capture (`nvm_store.c:737`, `:482-485`), and only from `NVM_P_IDLE`.
  - So a change marked after the capture of a save in flight waits for that save's remaining steps, and then for its own S steps.
  - The bound counts only the second wait. It assumes the first step after the window starts the change's capture.
- **Probe P2, 1x1, under `save-starved`'s flood** (`receipts/p2-second-change-analysis.txt`):
  - The first SET_NAME is durable 4,048.957 ms after it, within 4,070. The harness's own `SAVE` line agrees.
  - The second SET_NAME, 1,500 ms later, is written by the second save (erase at 7,293.2 ms). It is durable **5,608.954 ms** after it, **over the stated 4,070 ms by 1,538.954 ms**.
  - No refusal, no failure, and no pass over the share.
- **Derived worst case.** A change marked just after the capture of a save in flight waits (S − 4) × 30 + S × 30 + 10 ms:
  - about **22,090 ms at 8x8/2if**, against the stated 12,110;
  - about 6,010 ms at 1x1, against 4,070 (`receipts/bound-recompute.txt`).

**Impact:**
- The figure the round delivers as "the worst case of a save from the change to durable" is low by about 10 s at 8x8/2if.
- Anything that inherits it, such as the restated `T-NVM-COMMIT-TIMEOUT` #823 names, or the append-only writer's budget through this step, would be sized from a number an ordinary second change exceeds.
- No group stages a change during a save in flight, so no gate can see it.

**Required outcome:**
- State the worst case for a change, including one marked while a save is in flight after its capture has passed the record, derived from N, S and the tick.
- Or change the store so that such a change is bounded by the stated figure.
- Correct `nvm_store.h`, the doc's T, the harness README, `save_window.bound_ms` and the PR text to match.

**Verification:** a harness group with a second change after the first save's capture, timed from that change against the restated bound at both points, with a plant that leaves the in-flight wait out of the bound caught.

### RESIDUE-1 - wording only - `docs/design/SPLIT_CONTROL_MEMORY.md:1609` - section 14's S paragraph says the same thing twice

Both round 13 exact fixes were applied. Each states that the slope is arm A's at both ends, and "The 8x8/1if point is a labelled scratch arm, not on this branch." sits between them. No figure changes.

**Exact fix:** replace the bullet's text after "which holds the interfaces at one." with: "Its slope uses arm A at both ends, since the 8x8/1if point ran in arm A only: section 13's arm A 1x1/1if figures (the last AECP record's 10.04 ms), not the worst-of-arms 1x1/1if column below. The 8x8/1if point is a labelled scratch arm, not on this branch."

### RESIDUE-2 - wording only - `sw/firmware/ctrl_nvm/test/test_nvm_more.cpp:17-19` - the new test-list line splits another entry

The line `change_by_record_id  a change named by its record id` was inserted between `change_unknown_record`'s two lines. As a result, `change_unknown_record` loses its "marks nothing;", and `change_by_record_id` reads "a change named by its record id marks nothing", which is the opposite of what the test checks. This is a comment only.

**Exact fix:**

```
//   change_unknown_record      a change to a record the shape does not have
//                              marks nothing;
//   change_by_record_id        a change named by its record id marks that
//                              record;
```

### RESIDUE-3 - wording only - `sw/firmware/ctrl_nvm/nvm_store.h:88`, `sw/firmware/ctrl/loop/ctrl_loop.h:150` - the longest step rounded two ways

The same measurement, 96,579 cycles, is given as 0.97 ms in three places (`ctrl_loop.h:88`, the doc `:1487`, `ctrl_nvm/README.md:268`) and as 0.96 ms in two. No figure changes.

**Exact fix:**
- `nvm_store.h:88`: "measured at up to 0.97 ms at 8x8/2if";
- `ctrl_loop.h:150`: "(0.97 ms)".

### Suggestions (optional)

- **S1. The step's room.** Carried from R711-3 S3 and R712-3 SUGGESTION-1. The longest step is 0.966 ms of the 1.0 ms that `NVM_STEP_US` admits, a room of 0.034 ms, and no gate holds it; the author discloses this. A harness check that the longest measured store step is within `NVM_STEP_US` would make a slower flash port a refusal.
- **S2. A real part's figure.** The doc gives a part's erase as "about its erase time" added to the bound. With the datasheet maximum `SAVED_STATE_FASTCONNECT.md` uses (a 3,000 ms erase), state the resulting figure, about 15.1 s at 8x8/2if before F2's correction.
- **S3. The sweep shard tooling.** See judgement 5. Open an Issue, if none tracks it, for `capture_coherence`'s mutant driver sizing its pool to the CPU affinity under `run_all_suites.sh` shards (`tb/verilator/capture_coherence/mutants.py:723`). Rounds 12 and 13 already peaked at 10 GB with swap in that shard (`journal-shard2-peaks.txt`). R711-3 S4 (naming #756 beside #833) was not taken; the PR body names only #833.

## The judgements requested

1. **The shared MAJOR, mechanism (b).**
   - The mechanism is right. `ctrl_loop.c:158-168` runs an aged step as the whole pass, with the deadline read at the start, and returns 1. `step_age` counts dispatched centiseconds (`:111`) and resets when a step runs or owes nothing (`:182`).
   - `Loop.L13AnAgedStepIsAPassOfItsOwn` and its 10 plants cover each clause. I read the test and the mutants; the published firmware self-test catches all of them.
   - N = 2 was chosen by measurement of the idle-start windows only. That is F1. The "least margin 0.77 ms" does not hold under the starved input: 0.16 ms was measured, with every row still within its bound.
   - The contract-rate harness group exists. `save_window.arrivals` uses each channel's `refill_ms` and admission `at_once`, and `save_grade.held_load` refuses a load not committed whole.
   - With the age limit removed, `save-starved`'s save is not durable 12,618.4 ms after its change, and `CONTROL store-step-ageless caught` is printed (`measure/AGE-A8/run.log`, manifest-verified). The control catches by the run's end, not by a late completion, and that is sufficient here.
2. **The worst case, 12,110 ms.**
   - The bound is derived, not fitted. It is the debounce, plus S × (N + 1) ticks from the store's phase structure, plus 10 ms of stated slack. The measured 12,087.0 to 12,088.0 ms is inside it even without the slack: 12,100 ms.
   - The derivation holds for a save started from idle at every point and arm the author ran, and in my P2 for the first save (4,048.957 against 4,070).
   - It does not hold for a change made while a save is in flight (F2).
   - **On the owner's 0.5 s.** The PR does not claim it. The PR body (`:158`, `:351`), the doc (`:1455`) and the REVIEW READY all say that 0.5 s applies to the append-only writer through this same step and is not met by this image, whose stated worst case is 12.1 s, about 24 times 0.5 s.
   - One observation for the manager's scope decision: DR2a's 1,000 ms first-dirty window alone is twice 0.5 s. At this pace each further step of an inheriting writer costs up to 30 ms under the starved input.
3. **The round 13 MINORs.** Each is resolved at its cause.
   - **One build a pass, both orientations (R711-3-F2).** `turn_builds` reads the turn interface's state before any visit (`srp_mbx.c:840-845`, `:852-858`). The rule `!i->msrp && (built || (n != turn && turn_due))` defers in both orientations. `Srp.JointLinkChangeBuildsInterfaceOneBesideAWithdrawal` mirrors round 13's probe. The plant `build-turn-read-after-its-visit` restores the old reading and is caught (firmware self-test shards 2 and 3). The other plants were re-anchored without losing their meaning.
   - **The step-pass maximum (R711-3-F3 = R712-3-F2).** Every pass that enters `nvm_store_service` is now printed, quiet or work (`sim_main.cpp` `STEPPASS`, `step=1`). The maximum is stated on one basis at both points: 1.22 / 1.23 ms at 1x1 and 1.29 / 1.27 ms at 8x8, above the 1.26 ms floor. My probes' longest step-carrying pass, 1.220 ms, is consistent with it.
   - **The verify phase's end (R711-3-F4).** `grade.save_phase` refuses a verify window opened after the read-backs cover the image (`checked < save.image`), and `selftest_share` has its case and mutant.
4. **Residues.**
   - R712-3 RESIDUE-2 is applied verbatim (`nvm_store.h:79-82`).
   - R711-3 RESIDUE-1 and R712-3 RESIDUE-1 are both applied verbatim, which produced this round's RESIDUE-1.
   - R711-3 S1 (exactly `NVM_STEP_US` left) is taken on the model port, with the reason the LiteSPI port is excluded. S2 (the step-kind table) is taken.
   - Comment rule: the delta's added C, H, C++ and Python lines carry no bench lane label, lane name, review round, reviewer ID or issue-comment ID. No new comment-rule RESIDUE.
5. **The author's disclosed deviations.**
   - **Sweep shard 2.** This is not a defect of this PR.
     - `capture_coherence` and its sources are untouched by `a68536fa..HEAD`. The only HDL in the PR is the mailbox's record mover, which that suite does not build.
     - The OOM kills follow from its mutant driver sizing its thread pool to the CPU affinity when `--jobs` is not given (`mutants.py:723`). The shard runner does not pass `--jobs`.
     - The same shard peaked at 10 GB, with swap, in rounds 12 and 13.
     - Run alone on four CPUs at `a3f23bba`, shard 2 passed: `results.json` exit 0, 5,723.8 s.
     - This is shard tooling and suite resource behaviour (S3).
   - **The 8x8 harness gate through the 11-03 host incident.** I accept it as evidence. Its `run.log` gives HEAD `a3f23bba`, DIRTY 0, rc 0, 44 groups, 0 refusals, 0 of 88,204 passes over. The table is byte-identical to the measured leg's (blob `378e4600…`). The simulation is deterministic: my control window reproduced a published row to the cycle. Its 10,907 s, against the leg's 5,771 s, is the incident's slowdown.
   - The `results.json.gz` receipts archived only by sha256 were not needed: I relied on the tables and logs, which are manifest-verified.

## Prior findings at this head

| Finding | State at `a3f23bba` | Evidence |
|---|---|---|
| R711-3-F1 = R712-3-F1, a save's progress unbounded | **Resolved** at its cause: the age limit bounds it, and the ageless plant is caught. What the round states about the bound is F1 and F2 | Judgements 1 and 2 |
| R711-3-F2, one build a pass in one orientation | **Resolved** | Judgement 3 |
| R711-3-F3 = R712-3-F2, the step-carrying pass maximum | **Resolved** | Judgement 3 |
| R711-3-F4, the verify phase's end | **Resolved** | Judgement 3 |
| R711-3 RESIDUE-1 and R712-3 RESIDUE-1 | Applied; their overlap is RESIDUE-1 | `SPLIT_CONTROL_MEMORY.md:1609` |
| R712-3 RESIDUE-2 | **Resolved** | `nvm_store.h:79-82` |
| R711-3 S1 / S2 / S3 / S4 | Taken / taken / not taken (S1 here) / not taken (S3 here) | Judgement 4 |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | Round 14 items 1-6 against `ctrl_loop.h:29-150`, `ctrl_loop.c:100-186`, `nvm_store.h:9-29,77-90`, `nvm_store.c:480-485,564-815,819-848`, `save_window.py:24-240`, `save_grade.py`; #823's 0.5 s against the PR body `:18,:39,:158,:351` and doc `:1440-1455`; bound recomputed; P1, P1b, P1c, P2 | R711-4 | a3f23bbabdd9800177224432361fcd41b53bf882 |
| RTL (and architecture) | UNCLEAN (F1, F2) | No HDL in the delta. The loop's scheduling contract (THE BOUND, THE STEP's age limit), the store's phase machine and its change-marking contract (`nvm_mark`, `nvm_idle`), SRP's build-turn rule (`srp_mbx.c:836-880`), the walk-free id helpers (`nvm_klj2.c:187-202`) | R711-4 | a3f23bbabdd9800177224432361fcd41b53bf882 |
| Robustness | UNCLEAN (F1, F2) | A window opened after sustained input (P1, P1b, P1c); a second change during a save in flight (P2); the aged step's deadline and room (`nvm_store_step` under an aged pass); deferral keeping age (L13); ids outside the shape (`nvm_rec_id_known`, `change_unknown_record`); SRP turn with a link change in the same poll | R711-4 | a3f23bbabdd9800177224432361fcd41b53bf882 |
| Tests | UNCLEAN (F1, F2) | `test_port_loop.cpp` L13 and `loop_step_mutants.py` (18 plants); `srp_app.cpp` mirrored test and `srp_reopen_mutants.py`; `test_nvm_codec.cpp`, `test_nvm_more.cpp`, `test_nvm_write.cpp`, `nvm_mutants.py`; `build.py` `store-step-ageless`, `run.py` verdict, `selftest_share.py`; the published gate receipts (manifest-verified); no group stages F1's or F2's case | R711-4 | a3f23bbabdd9800177224432361fcd41b53bf882 |
| Docs | UNCLEAN (F1, F2); RESIDUE-1, -2, -3 | `SPLIT_CONTROL_MEMORY.md` `:1346-1349,1424-1590` and section 14 `:1596-1700`; `MAILBOX_SPLIT.md:326-335`; the `ctrl`, `srp`, `ctrl_nvm`, `gtest`, harness and boot READMEs; `ctrl_loop.h` and `nvm_store.h` comments; the live PR body and the REVIEW READY; comment-rule scan of the added source lines | R711-4 | a3f23bbabdd9800177224432361fcd41b53bf882 |

## Real limits

- Physical calibration was NOT RUN. Simulation is not hardware proof, and the harness's flash model has no busy time.
- The probes ran at 8x8/2if, arm A, without the drafts (F1), and at 1x1 (F2). F1's windows sample the age and tick phases; they are not exhaustive. F2's 8x8 figure is derived, not run, because a 22 s starved simulation did not fit this round.
- I did not re-run the host firmware and store gates. This host's interpreter lacks the YAML module the contract generator imports, and GoogleTest. Their results are the author's published, manifest-verified receipts.
- No manager source bank ran at this head, and none is claimed or inferred.
- Hosted checks at this exact head were still running when read. The snapshot showed 14 succeeded, 1 skipped (Physical gPTP, nightly and manual), 20 in progress and 14 queued. I claim no hosted verdict.
- I read the author's HANDOFF only where the PR body and the REVIEW READY cite it.

## Pending manager duties

- Publish this packet.
- Route F1 and F2 to the author:
  - F1: stage aged-step windows, restate the least margin and the reason for N;
  - F2: restate the bound for a change during a save in flight, or change the store.
- Carry RESIDUE-1, -2 and -3 to the residue checklist.
- Decide on S3, a tooling Issue for shard 2's memory.
- Record the scope position on #823's 0.5 s against this image's stated worst case (judgement 2). The PR records it as not met and does not claim it.
- At the merge turn, build and validate the current-dev merge candidate (source base `a68536fa`, live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`), and own hosted and act acceptance.

R711-4 FINISHED

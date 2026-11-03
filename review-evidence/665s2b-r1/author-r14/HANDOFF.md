# [A683q] #665 lane S2b, round 14 (HANDOFF)

**Status: REVIEW READY at `a3f23bbabdd9800177224432361fcd41b53bf882`** (started 2026-11-02 22:51 CET; cut by a host reset at about 09:50 on 2026-11-03 and resumed at 17:00 with no change to the tree). Start head `4f58214f457e963243a1fe6b86c6af161e97f26f` on `665-s2b-cycles`; commits are added on top, no rebase, no force, no merge. PR target `dev-soft-core` (`a68536fa`, not moved). Nothing pushed by this lane.

- Remote `https://github.com/kebag-logic/milan-fpga.git` (checked); the head contains `origin/dev-soft-core` `a68536fa` (checked); the live `dev` tip `e61a4afa` is not in it.
- Authority: the round 14 assignment (issuecomment-6589337173); the round 13 reviews R711-3 (PR #810 issuecomment-6589042666) and R712-3 (issuecomment-6589327842); earlier assignments and the owner decisions of 2026-10-31.
- TAKEN: issuecomment-6589414923 (`TAKEN-COMMENT.md`). REVIEW READY: issuecomment-6608999389 (`REVIEW-READY-COMMENT.md`), posted 2026-11-03.
- Outputs here: this file; `PR-BODY.md` (round 13's body with a round 14 section; `PR-BODY.round13.md` is round 13's, kept for the diff); `receipts/` with `receipts/INDEX.md` generated from the files present (`scripts/make_index.py`); `scripts/`, the lane's own drivers and analyses.

## Contents

1. Outcome against the assignment
2. Changes (file:line, reason)
3. New checks, planted mutants and failing words
4. Method
5. Measurement
6. Gates
7. Findings, decisions for the manager
8. Run history

## 1. Outcome against the assignment

A save's progress is bounded by a mechanism, the share is not amended, and every measured row the CPU decides and every pass fits at 100 MHz, at both points, in both arms, with the two drafts staged and without them, a save under every receive channel at its refill rate with and without a pass that takes nothing included. So this is REVIEW READY, not STOP.

| Item | Outcome | Where |
|---|---|---|
| 1. The mechanism | Met. THE STEP's age limit: an owed step not run for more than two centiseconds (`CTRL_LOOP_STEP_AGE`) is the next pass's alone, before any input; the input it held off is taken by the next pass. N chosen by measurement: in every window of every leg at most two TICK records were posted between two step-carrying passes (one at 1x1), so at N = 2 no aged step is taken among a window's records, at N = 1 it would be at 8x8. Every row and every pass within its bound (section 5); the least margin 0.77 ms (8x8 last SRP record, 17.23 ms, arm A, a save's window) | `ctrl_loop.c:160-168`, `ctrl_loop.h:99-106`, `:146-151`; `Loop.L13...` |
| 2. The bound | Met. T ≤ 1,000 ms + S × 3 ticks + 10 ms; a SET_NAME of the entity marks two records: S = 370 and 12,110 ms at 8x8/2if, S = 102 and 4,070 ms at 1x1, no flash busy time. `save-held` and `save-starved` at both points, both arms, with and without the drafts: every save within, 0 passes over the share, each channel's longest record within its bound; at 8x8 `save-starved` 12,087.0 to 12,088.0 ms. The plant with the age limit removed: `CONTROL store-step-ageless caught`, the save not durable 12,618.4 ms after its change. `SPLIT_CONTROL_MEMORY.md:1435` replaced | `nvm_store.h:16-28`, `save_window.bound_ms`, `save_grade.save_time`; section 13 "A save's worst case, and one build a pass either way" |
| 3. One build a pass either way | Met. `turn_builds` read before the poll's visits; `Srp.JointLinkChangeBuildsInterfaceOneBesideAWithdrawal`, plant `build-turn-read-after-its-visit` caught | `srp_mbx.c:835-878` |
| 4. The step-carrying pass maximum | Met. Every step-carrying pass printed by the harness (`STEPPASS`, `step=1`): over every group, 1.22 / 1.23 ms at 1x1 and 1.29 / 1.27 ms at 8x8 (arm A / arm B, without the drafts); the lone save's per-kind table at both points; round 13's sentence restated on one basis (1.21 and 1.26 ms) | section 13 |
| 5. The phase guard | Met. `save_phase` refuses a verify window that opens after the read-backs read back every programmed byte; self-test case and mutant | `grade.py:830-852` |
| 6. Residue | Met. R712-3 RESIDUE-1 and R711-3's RESIDUE (both texts, the figure this head's 10.04 ms), R712-3 RESIDUE-2 (exact text); S1 taken (`step_room` at exactly `NVM_STEP_US`, on the model port); R712-3 SUGGESTION-2 taken (1.116 ms) | section 14; `nvm_store.h:79-84`; `test_nvm_write.cpp` |
| Exit | Every row and pass fits; no share amendment; no STOP | section 5 |

## 2. Changes

Commits on `4f58214f` (one-line subjects, no body, no trailers):

| Commit | Subject (short) |
|---|---|
| `77f407cd` | THE STEP's age limit: an owed step not run for more than two centiseconds is the next pass's alone, before any input; `ctrl_plat` ledgered 8 bytes more |
| `db113e77` | SRP reads whether the interface with the turn builds before the poll visits either |
| `1a71c631` | The store's header states a save's worst case for a SET_NAME of the entity (370 steps, 12.11 s at 8x8/2if) |
| `3fed27b3` | The harness times a save to durable against its stated worst case under the held load and the starved load, prints every step-carrying pass, bounds the verify phase, plants the age limit's removal |
| `10851da1` | The store's room rule held at exactly `NVM_STEP_US` left (R711-3 S1), on the model port, and its `<=` plant |
| `d4930b76` | The held load started one AECP refill period after the change (superseded by `21d0e0f6`) |
| `22fc99f7` | A changed record marked by its id without walking the records (`nvm_rec_id_of`, `nvm_rec_id_known`, `nvm_store_changed_id`); AECP marks so; the coverage ratchet through its generator |
| `21d0e0f6` | The held channels burst at the change but AECP, whose first burst waits one refill period |
| `ecb8db10` | The step's measured cost, the heaviest pass and the age limit's basis restated in the loop's and the store's comments (comments only) |
| `f711714b` | The documentation: the age limit, a save's worst case, every step-carrying pass, one build a pass either way, the bounded verify phase, the rows at this head, the restated 32x32 estimate |
| `a3f23bba` | The SRP poll's extra-read plant re-anchored at the link reads the poll now makes before its visits |

| file:line | Change | Reason |
|---|---|---|
| `sw/firmware/ctrl/loop/ctrl_loop.c:111` | `dispatch_ticks` adds each dispatched centisecond to `step_age` | The age is counted in the centiseconds the store's consumer is called for, so it is time, not passes |
| `sw/firmware/ctrl/loop/ctrl_loop.c:160-168` | A pass that starts with `step_age > CTRL_LOOP_STEP_AGE` resets the age, calls the step with the deadline read as it starts, counts `aged_passes` and returns 1, taking nothing else | Item 1: input that leaves no pass empty held the step off for good (R711-3-F1 = R712-3-F1); the step alone keeps the pass within the share, and the input it holds off is taken by the next pass, one step later |
| `sw/firmware/ctrl/loop/ctrl_loop.c:179-184` | A step called in a pass that took no input resets the age when it ran or owed nothing (returned false); a step it had no room for keeps its age | A deferral must not restart the wait the limit bounds |
| `sw/firmware/ctrl/loop/ctrl_loop.h:28-33` (THE BOUND), `:80-82` (THE SHARE), `:99-106` (THE STEP), `:146-151` (`CTRL_LOOP_STEP_AGE` 2u), `:197`, `:214`, `:228-230` | The age limit in the loop's contract; the constant and why two; `aged_passes`, `step_age`; the return value | Item 1 |
| `sw/firmware/ctrl/test/test_port_loop.cpp:848-910` | `Loop.L13AnAgedStepIsAPassOfItsOwn` | Item 1: the boundary at N, the pass taken whole, nothing else taken, the deadline, the count, the input taken next, the age reset by a step and kept by a deferral |
| `sw/firmware/ctrl/test/loop_step_mutants.py` (new), `ctrl_mutants.py` | THE STEP's 19 planted defects moved out of `ctrl_mutants.py` (L10 to L13), 10 of them new | `ctrl_mutants.py` would have passed the idiom gate's 1,000-line module limit; the file names no firmware tree path, so the boundary gate needs no entry |
| `sw/litex/ctrl_memory.py:217`, `ctrl_memory_ledger.py:26` | `ctrl_plat` 19,968 B, and 17,168 / 18,672 / 17,816 at the other points | The loop's two new fields; measured by `scripts/fit.py` (section 5) |
| `sw/firmware/ctrl_nvm/nvm_store.h:9-28`, `:79-84`, `:85-91` | The step's age limit; A SAVE'S WORST CASE; R712-3 RESIDUE-2's exact text; `NVM_STEP_US`'s measured basis (0.96 ms, 0.77 ms) | Items 2 and 6 |
| `sw/firmware/ctrl_nvm/nvm_store.c:47-51` | The step's age limit in the store's header | Item 1 |
| `sw/firmware/ctrl_nvm/nvm_store.c:819-848`, `nvm_store.h:167-170` | `nvm_mark` sets the record's dirty bit by its id; `nvm_store_changed` finds the id by `nvm_rec_id_of`; `nvm_store_changed_id` marks an id the shape knows | Item 1 requires every pass within its bound: AECP's mark of a SET_NAME walked the records twice (22,088 cycles) in the pass that drained the held load's first bursts, 2.135 ms at 8x8 (section 7) |
| `sw/firmware/ctrl_nvm/nvm_klj2.c:187-202`, `nvm_klj2.h:77-82` | `nvm_rec_id_of` (a group's base plus the index, or -1), `nvm_rec_id_known` (an id inside a group's range) | The same: an id with no walk |
| `sw/firmware/ctrl/aecp/aecp_nvm.c:126-131`, `:167` | AECP's mark by group and index, and its scan of the record bitmap, mark by id | The same |
| `sw/firmware/ctrl_nvm/test/test_nvm_codec.cpp:144-158`, `test_nvm_more.cpp:88-110`, `nvm_rig.cpp:561` | `NvmCodec.codec_ids_without_the_walk`, `NvmModel.change_by_record_id`, an unknown id in `change_unknown_record`, the rig's `--change-id` | The new functions against the walking ones over every group, index and id |
| `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:684-690` | `step_room` at exactly `NVM_STEP_US` left, on the model port | R711-3 S1; the LiteSPI port's timer moves between the rig's read and the store's |
| `sw/firmware/ctrl_nvm/test/nvm_mutants.py`, `sw/firmware/ctrl/test/aecp_mutants.py:182-186` | Five store plants new; five re-anchored on `nvm_mark`; `nvm-scan-word-index-dropped` re-anchored on `nvm_store_changed_id` | Each new path planted; each moved site still planted once |
| `sw/firmware/gtest/coverage.ratchet`, `sw/firmware/gtest/README.md` | The ratchet rewritten by `fw_coverage.py --write`; its exemption text | The store's and the codec's line counts moved |
| `sw/firmware/ctrl/test/srp_mutants.py` | `srp-poll-extra-read` anchored at `links[n] = mbx_link_up(n);` | The link reads moved before the visits (item 3), and the old anchor had no site: shard 3 of the firmware self-test refused at `f711714b` with "has 0 planting sites" |
| `sw/firmware/ctrl/srp/srp_mbx.c:835-860`, `:878` | `turn_builds`: whether the interface with the turn builds, read before the poll visits any interface; every link level read once as the poll starts | Item 3 (R711-3-F2): visited first, a withdrawing turn interface had spent its withdrawal before the other was examined, so interface 1 waited three passes |
| `sw/firmware/ctrl/test/srp_app.cpp:412-430` | `Srp.JointLinkChangeBuildsInterfaceOneBesideAWithdrawal` | Item 3: the mirrored orientation |
| `sw/firmware/ctrl/test/srp_reopen_mutants.py` | `build-turn-read-after-its-visit` new; `joint-reset-builds-both`, `build-turn-ignored`, `build-waits-beside-a-withdrawal` re-anchored | Item 3; with the turn read first, `built` alone never defers at two interfaces, so the builds-both plant now removes the deferral |
| `sw/firmware/ctrl/srp/srp_bounds.h:20-21`, `srp/README.md:157-158` | The rule holds whichever index has the turn | Item 3 |
| `tb/verilator/ctrl_service_budget/sim_main.cpp:234-262`, `:265-276` | `FLASHOP` with address and bytes, `FLASHPOLL`, `FLASHRD` runs of journal reads (overlapping word reads merged) | A save's read-backs run in passes that write nothing to the mailbox; their reads time the save and bound the verify phase |
| `sim_main.cpp:366-377`, `:535-539` | `flood gm 1|0`: a grandmaster change as every pass starts | Item 2: the event sources are coalesced but not rated by the contract, the only input that leaves no pass empty |
| `sim_main.cpp:381-398`, `:410` | `STEPPASS` for every idle pass that enters `nvm_store_service`, `step=1 store=` on a work pass | Item 4: every pass that carries a step on one basis, at both points, in every leg |
| `sim_main.cpp:456-488` | `queue_reply` extracted | `run_script` would have passed the C++ idiom gate's 100-line function limit |
| `tb/verilator/fw_service_budget/flash.hpp:107-111` | `command()`, `address()`, `cursor()` read-only accessors | The observer reads the closing command; no behaviour changes |
| `tb/verilator/ctrl_service_budget/save_window.py:52-98` | `CHANGED` 2, `container`, `step_age`, `steps`, `bound_ms` | Item 2: the worst case from N, the step count and the tick |
| `save_window.py:155-227` | `maap_conflict`, `arrivals`, `loaded`, `windows`, `groups(p, build)`; `save-held`, `save-starved` | Item 2: every channel at its contract refill rate with its bursts through a whole save, and the same with no pass that takes nothing |
| `tb/verilator/ctrl_service_budget/save_grade.py` (new) | `first_save`, `merged_reads`, `save_time`, `held_load`, `held`, `step_figures` | Items 2, 4, 5; moved out of `grade.py`, which would have passed 1,000 lines |
| `tb/verilator/ctrl_service_budget/grade.py:225-226`, `:830-852`, `:906-907` | `STEPPASS` parsed; `save_phase` bounds the verify by its read-backs; `grade` reports the save, the held rows, the step figures | Items 4 and 5 (R711-3-F4) |
| `tb/verilator/ctrl_service_budget/run.py:142-195`, `:412-420`, `:503-516` | Saves and steps tables, `SAVE` and `STEPS` lines, a late save fails the run, the `SAVE_CONTROLS` verdict | Item 2 |
| `tb/verilator/ctrl_service_budget/build.py:46-53`, `:80-89`, `:437-440` | `STEP_SPAN` re-anchored; `store-step-ageless`; `STEP_SYMBOL`, `STORE_MODULES` | Item 2's plant; item 4's observation |
| `tb/verilator/ctrl_service_budget/selftest_share.py`, `selftest_mutants.py`, `selftest.py` | Phase, bound, save-time, held-load, held-rate and step checks; 15 grader mutants | Each new check |
| `tb/verilator/ctrl_service_budget/README.md` | A save under load and its stated worst case; the checks; the mutants; the control | Items 2, 4, 5 |
| `docs/design/MAILBOX_SPLIT.md:326-332`, `sw/firmware/ctrl_nvm/README.md`, `sw/firmware/ctrl/README.md:480` | The age limit; a save's worst case | Items 1 and 2 |

## 3. New checks, planted mutants and failing words

| Check | Planted | Failing words |
|---|---|---|
| `Loop.L13AnAgedStepIsAPassOfItsOwn` | `step-age-uncounted`, `step-age-ignored` | "L13 the next pass takes the step though input waits" |
| | `step-age-at-the-limit` | "L13 the pass that dispatches one more takes its input, not the step" |
| | `step-aged-pass-takes-input` | "L13 and takes nothing else: no event, no record, no poll" |
| | `step-aged-pass-sleeps` | "L13 the step's pass asks for the next pass at once" |
| | `step-aged-deadline-not-read` | "L13 with the deadline read as it starts" |
| | `step-aged-pass-uncounted` | "L13 the pass is counted as an aged step's" |
| | `step-age-kept-by-its-pass` | "L13 the next pass takes the input it held off" |
| | `step-age-kept-after-a-step` | "L13 a step run in a pass that takes nothing starts its age again" |
| | `step-age-reset-on-deferral` | "L13 a step it had no room for keeps its age" |
| `Srp.JointLinkChangeBuildsInterfaceOneBesideAWithdrawal` | `build-turn-read-after-its-visit` | "interface 1, due beside interface 0 still withdrawing with the turn, is built at once" |
| `Srp.JointLinkChangeBuildsOneInterfaceAPass` (re-anchored) | `joint-reset-builds-both` | "a pass builds one interface at most" |
| Harness: a save's window refused outside its phase, the verify ending at its read-backs | `save: a verify window is graded after its read-backs read back the container` | The check's name |
| Harness: a save's stated worst case, restated | `save: the bound counts one tick a step, not the age limit's`; `save: the bound leaves out the verify's read-backs` | The check's name |
| Harness: a save timed to the read-back that completes its verify | `save: durable at the verify's first read-back, not the one that completes it`; `save: a save never durable in the run is within its bound` | The check's name |
| Harness: a late save fails the run | `save: a save over its stated worst case is no finding` | The check's name |
| Harness: the age limit's plant caught by save-starved's late save | `save: the age limit's plant is judged as a budget control` | The check's name |
| Harness: a held group commits every offered record | `save: a held group that commits fewer records than it offered is graded` | The check's name |
| Harness: every receive channel at its refill rate with its bursts | `save: a channel left out of the held load`; `save: the held load a burst once, then nothing` | The check's name |
| Harness: save-starved alone has the grandmaster flood | `save: the starved save without its grandmaster flood` | The check's name |
| Harness: every step-carrying pass counted | `steps: a pass that carries a step and writes nothing to the mailbox is left out`; `steps: a work pass that carries a step is left out` | The check's name |
| Native control `--mutation store-step-ageless` | the age limit removed (`step_age > CTRL_LOOP_STEP_AGE + step_age`) | `CONTROL store-step-ageless caught` (section 5) |
| `NvmCodec.codec_ids_without_the_walk` | `id_of_one_past_a_group` (`index > count`), `id_known_one_past_a_group` (`<= count`) | "a record's id by its group and index is nvm_rec_of's, and -1 where it has none"; "an id is known exactly where nvm_rec_by_id finds its record" |
| `NvmModel.change_by_record_id` | `change_id_ignored` (the id dropped), `change_id_of_no_record` (an unknown id marks `id & 0xFF`) | "a change by a record's id marks it, and one by an id the shape has not marks nothing" |
| `NvmModel.change_unknown_record` (an unknown id added) | `change_id_of_no_record`; `change_of_no_record` re-anchored on `nvm_mark` | "changes to records the shape does not have" |
| `NvmBoth.step_room` (exactly `NVM_STEP_US`, model port) | `step_needs_room_past_its_cost` (`<=` for `<`) | "a pass with exactly NVM_STEP_US left takes the owed step" |
| The store's DR2a and budget cases (unchanged tests) | `taken_off_by_one`, `taken_while_capturing`, `taken_after_last_latch`, `budget_rearmed_by_change` re-anchored in `nvm_mark` | Their tests' existing words (`debounce`, `capture_window_edges`, `dr2c_unchanged_set`) |
| `Nvm.EmptyAndNonDefaultMapsSurviveTheRealStorePowerCycle` (unchanged) | `nvm-scan-word-index-dropped` re-anchored on `nvm_store_changed_id` | "the empty set is a framed record, not an erased one" |
| `Srp.PollTermsAreMeasuredSeparatelyThroughRealCallbacks` (unchanged) | `srp-poll-extra-read` re-anchored at `links[n] = mbx_link_up(n);` | "one link read per interface" |

## 4. Method

- **Legs.** `tb/verilator/ctrl_service_budget/run.py` on clean clones of the code head `21d0e0f6` (`scripts/clone.sh`, `scripts/drafts.sh` for the two drafts staged in the clone only, lwSRP `fc06e7c0` and tsn-c-stack `6532c3b0`, `receipts/drafts-staged.patch`), each a build, its groups, `--record-budget-findings --record-share-findings`, the CPU on `sys` at 100 MHz (`scripts/leg.sh`, `scripts/queues2.sh`):
  - arm A, every group, at both points (`N-A1`, `N-A8`);
  - arm B (`--variant answering-ports`), and both drafts staged in each arm, on the four backlog rows, a save's 24 windows, the lone save, `save-held` and `save-starved` (`N-B1`, `N-B8`, `DA1`, `D-B1`, `D-A8`, `D-B8`);
  - the two native controls at 8x8, arm A: `--mutation store-step-unbounded` on the 24 windows (`CTL-A8`), `--mutation store-step-ageless` on `save-starved` (`AGE-A8`);
  - section 14's labelled 8x8/1if point (`P81-A8`, `receipts/point-8x8-1if.patch`) and the round 12 review's probe groups (`X-A8`, `X-B8`, `receipts/probe-groups.patch`, adapted to `save_window.groups(p, build)`).
- **Heads.** Every leg started at `21d0e0f6`. The final head `a3f23bba` adds comments in `ctrl_loop.h` and `nvm_store.h`, documentation and one re-anchored plant in a mutant table; its images are rebuilt through the harness's own `build.firmware()` and compared with the legs' (section 6). `sim_main.cpp`, `flash.hpp` and every harness Python file are unchanged since `21d0e0f6`. Arm A's every group ran again at both points on a clean clone of the final head as the harness gate (`G-A1`, `G-A8`, section 6).
- **The first legs** started at `3fed27b3` and were stopped once the held groups' first runs found the AECP token and the mark's walk (section 7); only `N-A1` finished there, kept as a whole-pipeline pre-check (`receipts/first-runs/`).
- **Analyses.** `scripts/rows14.py` builds every row, share, save and step table from the legs' `results.json` (`receipts/tables/section13.md`); `scripts/estimate14.py` restates section 14 (`receipts/tables/section14.md`); `scripts/stepgaps.py` the longest gap between step-carrying passes and the centiseconds posted between them, per window (`receipts/analysis/stepgaps-*.txt`); `scripts/stepkinds.py` each step kind's cost in the lone save (`receipts/analysis/stepkinds-*.txt`); `scripts/fit.py` the fit table.
- **The boot simulation** ran at both shapes at `21d0e0f6` (`receipts/precheck/boot-C2-*.log`) and again in the lane gates at the final head.

## 5. Measurement

Every leg at `21d0e0f6`, the CPU on `sys` at 100 MHz; receipts under `receipts/measure/<leg>/` (`label.txt`, `run.log` with the head, `build.json`, `image.txt`, `results.json.gz`, `table.md`). Each leg's `run.log` ends with rc 0.

| Leg | Point, arm | Groups | Result (its `run.log`) |
|---|---|---|---|
| `N-A1` | 1x1/1if, A | every group, 45 | 0 refusals, 6 egress-held misses, 0 of 66,819 over; saves 2,019.2 / 2,019.0 / 4,049.0 ms (alone / held / starved) |
| `N-B1` | 1x1/1if, B | backlog, 24 windows, three saves | 0 refusals, 0 of 57,520 over; starved 4,048.1 ms |
| `DA1`, `D-B1` | 1x1/1if, A and B, drafts | the same | 0 refusals, 0 of 56,068 and 0 of 57,576 over; starved 4,047.9 and 4,048.0 ms |
| `N-A8` | 8x8/2if, A | every group, 44 | 0 refusals, 6 egress-held misses, 0 of 88,204 over; saves 4,697.4 / 4,696.9 / 12,087.0 ms |
| `N-B8` | 8x8/2if, B | backlog, 24 windows, three saves | 0 refusals, 0 of 74,225 over; starved 12,087.0 ms |
| `D-A8`, `D-B8` | 8x8/2if, A and B, drafts | the same | 0 refusals, 0 of 80,929 and 0 of 76,066 over; starved 12,087.1 and 12,088.0 ms |
| `CTL-A8` | 8x8/2if, A, store-step-unbounded | 24 windows | `CONTROL store-step-unbounded caught`: 5 windows over the share with every row in bound, 8 with a row over as well, 3 with a row over and no pass over; 13 of 18,918 over, the longest 2.718 ms |
| `AGE-A8` | 8x8/2if, A, store-step-ageless | save-starved | `CONTROL store-step-ageless caught`: not durable 12,618.4 ms after its change (worst case 12,110), 0 of 53,678 over |
| `P81-A8` | 8x8/1if, A | backlog | 0 refusals, 0 of 1,277 over |
| `X-A8`, `X-B8` | 8x8/2if, A; B | probe groups; link groups | 0 refusals, 0 over; x-save 1.640, y-save 1.977, y-links 1.741 / 1.809, x-links-same 1.531 / 1.556 ms |

Figures (tables in `receipts/tables/`):

- **The bound.** 12,110 ms at 8x8/2if (S = 370), 4,070 ms at 1x1 (S = 102), for a SET_NAME of the entity, no flash busy time. Every save within it in every leg; starved 12,087.0 to 12,088.0 ms at 8x8, the longest gap between flash steps 31.25 to 31.48 ms.
- **N.** The most centiseconds posted between two step-carrying passes in any window: 2 at 8x8 (verify windows' longest gap 26.36 / 26.40 ms), 1 at 1x1, so no aged step in any window at N = 2.
- **The share.** 0 passes over in every group of every leg but the planted control; the longest 1.97 ms (8x8, arm A, `backlog-adp`), carrying no step.
- **The rows.** Every row the CPU decides fits; the least margin 0.77 ms, 8x8 last SRP record 17.23 ms in a save's window, arm A (16.91 arm B); backlog windows 16.35 / 15.90 ms. Held groups: each channel's longest record within its bound, SRP at most 14.81 ms at 8x8.
- **The step-carrying pass maximum** over every group: 1.218 / 1.231 ms at 1x1, 1.292 / 1.266 ms at 8x8 (arm A / arm B), 1.182 / 1.177 and 1.246 / 1.249 ms with the drafts. The longest step's own time 96,579 cycles, 0.966 ms (`DA1`).
- **The step kinds**, lone save, arm A, own / pass cycles at 1x1 and 8x8: program issue 95,184 / 102,986 and 95,525 / 126,870; blank check 76,495 / 120,202 and 75,869 / 121,069; verify 76,048 / 83,867 and 76,917 / 122,059; capture or seal 35,645 and 34,700.
- **The boot**: 25.477 and 64.584 ms to ready at 1x1 and 8x8 (25.515 and 64.885 at `4f58214f`).
- **Fit**: platform 58.5 tiles and fixture 57.0 at 8x8 with two interfaces, within 59.0 and 57.5; the 1x1 two-interface platform image 41.5 (41.0); `ctrl_plat` 19,968 B.
- **32x32**: the last SRP record 31.0 / 35.8 / 65.4 ms under S / L / U, the last AECP record 28.3 / 35.0 / 63.7 ms, the longest pass 3.6 / 4.9 / 7.9 ms.

## 6. Gates

Every gate on a clean clone of the final head `a3f23bbabdd9800177224432361fcd41b53bf882` (`scripts/clone.sh`; the sweep's clones by `native-shards.py`), never piped, one log and rc each; receipts under `receipts/gates/`. The environment is `scripts/env.sh` with the pinned Verilator 5.050, sv2v and make 4.3 first on `PATH` (`scripts/lane_gates.sh`).

| Gate | Command (from the clone's root) | rc | Result (its log) | Receipt |
|---|---|---:|---|---|
| docs.yml | every `run:` step of `.github/workflows/docs.yml`, each job on its fresh clone (`scripts/docsrun.sh`, `run_docs_yml.py`, `verify_docs_yml.py`) | 0 | six jobs rc 0; "64 steps ran, 31 not run with a reason, 0 bad" | `gates/docs/` |
| The full sweep | `bash scripts/run_all_suites.sh <logs> --wait --shard k/4`, k = 0 to 3, four `native-shards.py` units, `MAKEFLAGS=-j4 --no-print-directory`; shard 2's result from its run alone on four CPUs (below) | 0 ×4 | 65 of 65 suites passed, 0 failed, 0 timed out, 2,613,655 checks, 0 in-suite failures: shard 0 15 suites, 360,921 checks; shard 1 17, 1,946,931; shard 2 17, 284,228; shard 3 16, 21,575 (each shard's `spec/01.log`, `complete.json` "exit_code": 0) | `gates/sweep/`, `gates/sweep-first-attempt/`, `gates/sweep-shard2-killed/` |
| Firmware self-test | `python3 -B sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --lwsrp third_party/lwSRP --jobs 4 --shard k/4`, k = 0 to 3 | 0 ×4 | `test_ctrl_firmware: PASS` in each; 1,160 live invocations in exactly one shard (67 / 623 / 169 / 301); shard 1 "mutants: 622 of 622 caught"; the AECP campaign's plants `[ok]` in shard 2 and the SRP campaign's in shard 3, `srp-poll-extra-read` among them; no `ESCAPED` or `REFUSED` verdict in any shard | `gates/firmware/fwshard-k.log` |
| The store's gate | `python3 -B sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py --require-rv32 --self-test --jobs 4` | 0 | "OK across 5 shape(s), 455 tests, and all 121 planted defects reddened" | `gates/lane/nvm_selftest.log` |
| Coverage | `python3 sw/firmware/gtest/fw_coverage.py --check --lwsrp third_party/lwSRP --jobs 8` | 0 | "firmware coverage: PASS (38 files)" | `gates/lane/fw_coverage.log` |
| RV32 self-test | `python3 sw/firmware/gtest/fw_rv32_selftest.py --require-rv32` | 0 | "25 checks PASS" | `gates/lane/fw_rv32_selftest.log` |
| Harness self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | 0 | "self-test: 0 failures"; 124 grader mutants caught, 0 escaped; the control verdict's escaping inputs print `ESCAPED` by design | `gates/lane/harness_selftest.log` |
| Harness, 1x1 | `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <b> --record-budget-findings --record-share-findings --jobs 8` (`scripts/leg.sh`, `G-A1`) | 0 | 45 groups, 0 refusals, 6 egress-held misses, 0 of 66,819 over; saves 2,019.2 / 2,019.0 / 4,049.0 ms (alone / held / starved), worst case 4,070; the longest step-carrying pass 1.218 ms; the figures `N-A1`'s | `gates/harness/G-A1/` |
| Harness, 8x8 | the same at `--point 8x8` (`G-A8`) | 0 | 44 groups, 0 refusals, 6 egress-held misses, 0 of 88,204 over; saves 4,697.4 / 4,696.9 / 12,087.0 ms (alone / held / starved), worst case 12,110; the longest step-carrying pass 1.292 ms, the longest step 0.962 ms; the figures `N-A8`'s | `gates/harness/G-A8/` |
| Image identity | `scripts/imgcheck.sh`: the six measured images rebuilt at the head through the harness's `build.firmware()` | 0 | "6 of 6 images the same" (`N-A1`, `N-B1`, `N-A8`, `N-B8`, `CTL-A8`, `AGE-A8`) | `gates/image-identity.log` |
| Builder | `python3 sw/builder/test_builder.py --require-rv32` | 0 | "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 1b's make, gate 11's mf48 build tree; as before) | `gates/lane/test_builder.log` |
| behave | `cd tests && behave --no-capture -f plain` | 0 | 508 scenarios passed, 0 failed | `gates/lane/behave.log` |
| Boot | `python3 -B tb/verilator/ctrl_split_boot/run.py --build-dir <b>` at 1x1, `--shape endstation_ax7101_8x8`, `--native-controls`, `--self-test` | 0 ×4 | ready 25.477 and 64.584 ms; native controls 6 of 6; 3 of 3 plants caught | `gates/lane/boot_*.log` |
| Idiom | `python3 -B scripts/check_py_idiom.py`; `python3 -B scripts/check_cpp_idiom.py` | 0, 0 | every count within its ratchet | `gates/lane/py_idiom.log`, `cpp_idiom.log` |
| Mailbox, census | `python3 sw/mailbox/gen_mailbox.py --check --crosscheck`; `--selftest`; `python3 sw/mailbox/publication_census.py --check --selftest --jobs 8` | 0 ×3 | 0 findings; 0 arms failed; 0 of 43 rules no arm proves | `gates/lane/gen_mailbox*.log`, `census.log` |
| RTL lint | `python3 scripts/lint_rtl.py --check` | 0 | PASS, 89 within the ratchet 89 | `gates/lane/lint_rtl.log` |
| SoC, memory | `python3 sw/builder/test_soc_options.py`; `python3 sw/litex/test_ctrl_memory.py` | 0, 0 | PASS, PASS | `gates/lane/soc_options.log`, `ctrl_memory.log` |
| Boundary | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator`; `--only verilator` | 0, 0 | PASS, PASS | `gates/lane/boundary_*.log` |
| `git diff --check` | `git diff --check a68536fa4cf8ce65c513874722de2e3ba83c2d00 HEAD` (the merge base); also against round 13's base `f4c9ad4f` | 0, 0 | clean | `gates/lane/diffcheck_*.log` |
| Tree after | `git status --short` in the lane gates' clone | | empty | `gates/lane/tree-after.txt` |

**The sweep's attempts**, all at `a3f23bba` with the same command, each kept:

| Attempt | Units | Result | Receipt |
|---|---|---|---|
| 1 (05:25) | four `native-shards.py` units, 10 GB each | every shard rc 1 in its preflight, `test_suite_cancellation.py` (#833): shards 0, 1 and 2 "CLEANUP FAILED: owned descendants remain" after the `unsafe-command-SIGTERM` case; shard 3 "timed out after 12 seconds" in the `cancel-lock-wait-SIGTERM` case, then "ABORTING: sweep cancellation controls failed." | `gates/sweep-first-attempt/` |
| 2 (05:27), the one re-run #833 allows | four `native-shards.py` units, 10 GB each | shards 0, 1 and 3 rc 0 (06:31, 06:26, 06:23); shard 2 killed by the kernel OOM killer at its unit's 10 GB (05:48) in `capture_coherence`, "41 builds on 8 worker(s)", its four suites before it passed | `gates/sweep/shard-{0,1,3}/`, `gates/sweep-shard2-killed/8cpu-10G/` |
| 3 (07:29) | shard 2 alone, its own unit on its cleaned clone, 16 CPUs, the 24 GB cap | killed by the OOM killer at 24 GB (08:07) in `capture_coherence`, "41 builds on 16 worker(s)", while it compiled `Vmilan_datapath.o` | `gates/sweep-shard2-killed/16cpu-24G/` |
| 4 (08:09 to 09:44) | shard 2 alone, its own unit on its cleaned clone, four CPUs, the 24 GB cap | rc 0, 17 of 17 suites, 284,228 checks, "41 builds on 4 worker(s)" | `gates/sweep/shard-2/` |

Attempts 2 to 4's shard 2 is a memory failure of the host's unit, not a suite failure: `tb/verilator/capture_coherence/mutants.py` takes one build worker per CPU of its affinity (`len(os.sched_getaffinity(0))`), each a Verilator datapath build. No suite this PR touches is involved, and nothing in the tree was changed between the attempts. The unit accounting is in `gates/sweep-shard2-killed/units.txt` and `journal-shard2-peaks.txt`. Attempt 4's own unit lines were not kept, because the journal on disk ends at 08:05 and the host was reset at about 09:50. Its worker count is in its log. Each shard's suite and check counts equal round 13's at `4f58214f` (its `receipts/gates/sweep/shard-k/01.log`), shard 2 included.

**Gates at `f711714b`**, stopped once shard 3 refused (section 8), are kept outside the receipts; nothing in this table comes from them.

## 7. Findings, decisions for the manager

- **Found and fixed: a persisted change beside a full burst was over the share.** The first held runs (at `3fed27b3`) put one 8x8 pass at 2.135 ms (arm A) and 2.085 ms (arm B), 1 ms after the change, in both held groups: AECP's mark of the SET_NAME's two names walked the store's records twice, 22,088 cycles of `nvm_klj2`, in the pass that drained the first bursts. No defined window staged it: the save windows' SET_NAME comes 1.1 s into the MAAP wait. `22fc99f7` marks by id without the walk; that pass is 1.711 ms at this head. This is a store change beyond the assignment's items, made because item 1 requires every pass within its bound; it is disclosed in the PR body.
- **Found and fixed in the harness**: the held load's SET_NAME took one of AECP's tokens (the channel's first burst lost a record), and the copied MAAP PROBEs went to the bridge's MAC once the entity had answered with a DEFEND (7 of 231 committed in the working-tree pre-check). AECP's bursts now start one refill period after the change, the copy goes to the MAAP group address, and a held group that commits fewer records than it offered is refused.
- **N = 2 rests on a 3.6 ms margin.** The heaviest window holds a step off for at most 26.4 ms, two centiseconds in the gap; a third, about 30 ms after a step taken just after its tick, would put an aged step among the window's records, where the least margin (0.77 ms) is below a step (0.96 ms at 8x8). A change that lengthens that drain must measure it again. N = 3 would add 3.7 s to the worst case (15.81 s).
- **The step's room is 0.034 ms.** The longest step's own time is 0.966 ms of the 1.0 ms `NVM_STEP_US`. The harness now reports every step's own time (S3 / R712-3 SUGGESTION-1), but no gate holds the figure; not taken as a gate this round.
- **The worst case is this image's.** 12,110 ms at 8x8/2if on a flash with no busy time; a part's erase time adds to it. #823's 0.5 s is the append-only design's writer's through this same step, and this image does not meet it; no owner decision is asked here.
- **Not taken:** R711-3 S5 (the platform image's hot list, still disclosed), R712-3 SUGGESTION-3 (the boot export's ISA-string order; outside this PR, for a new Issue, which this lane may not open: the lane's runs set `PYTHONHASHSEED=0`).
- **Diagnostic only:** a `FLASHRD` run spans one read-back step's reads, or two steps' within a millisecond of each other (a step held off past a tick, then the next); the save's time to durable counts bytes and is exact, the count of flash steps then reads one short.
- **The sweep's shard 2 needs its CPU range bounded.** `capture_coherence/mutants.py` takes one build worker per CPU of its affinity, each a Verilator `-j 0` build of the datapath, so the shard's memory grows with the CPUs it is given: past 10 GB on 8, past 24 GB on 16. Round 13's shard 2 peaked at 6 GB in one run and at 10 GB with 4.7 GB of swap in another, and round 12's at 10 GB with 5 GB and 4.5 GB of swap (`gates/sweep-shard2-killed/journal-shard2-peaks.txt`). This lane's passing run used four CPUs. Whether `native-shards.py` should bound it is for the manager; nothing in this PR touches the suite.
- **Not run:** any hardware or bench step (none assigned); a Vivado route (none needed). docs.yml's hosted-only steps are listed with their reasons in `receipts/gates/docs/verify.md`.

## 8. Run history

- 2026-11-02 22:51 CET start; remote and head checked; the assignment, both reviews and A683p's handoff read. 22:58 TAKEN.
- 23:05 to 23:30 THE STEP's age limit, L13 and its plants; the SRP turn read first, its mirrored test and plants; the firmware suite on the working tree (rc 0); `ctrl_plat` measured 19,968 B by `scripts/fit.py`.
- 23:31 the new plants' pre-check: 15 of 15 loop plants caught; `joint-reset-builds-both` escaped, equivalent at two interfaces with the turn read first; re-planted as the deferral removed, caught (23:36).
- 23:36 the 1x1 pre-check of the new groups on the working tree (`PRE-A1`): the starved save durable 4,048.0 ms after its change, steps 30.9 ms apart at most; the held save 2,018.2 ms, as the lone save; 0 of 46,048 passes over the share. Found: the SET_NAME marks both of the entity's names, so a save's steps are 370 at 8x8, not 369; and the copied MAAP PROBEs went to the bridge's MAC after the first DEFEND, so 7 of 231 committed: the copy now goes to the MAAP group address with no conflict range, and a held group that commits fewer records than it offered is refused.
- 23:50 coverage on the working tree: PASS, 38 files. Idiom gates: three modules past 1,000 lines and `run_script` past 100, split (`save_grade.py`, `loop_step_mutants.py`, `queue_reply`).
- 00:07 code head `3fed27b3`; 00:09 thirteen legs start in five queues on clean clones (section 4).
- 00:35 the store's room rule at exactly `NVM_STEP_US` (S1): on the LiteSPI port the timer moves between the rig's read and the store's, so the case holds on the model port; the store suite and three room plants pass (`10851da1`).
- 01:03 `CTL-A8` at `3fed27b3`: `CONTROL store-step-unbounded caught`.
- 01:10 the first 8x8 starved save, arm A: durable 12,087.8 ms after its change, within 12,110; but the held-load check refused it (AECP committed 2,528 of 2,529: the SET_NAME took a token of the channel's first burst), and one pass was over the share, 2.135 ms, 1 ms after the change, in arm A and arm B at 8x8 without the drafts. Its cause: AECP's mark of the SET_NAME's two names walked the records twice, 22,088 cycles of `nvm_klj2` in the pass that drained the first bursts. The held load's start fixed (`d4930b76`), then the mark made walk-free in the store and in AECP (`22fc99f7`), the store suite, nine store plants, two AECP plants, the firmware suite and coverage on the working tree, rc 0, the ratchet rewritten by its generator; the held channels but AECP burst at the change again, so the marks fall among their first bursts (`21d0e0f6`). Every leg started at `3fed27b3` measured an image this replaces: they were stopped (`N-A1` kept as a whole-pipeline pre-check: only the two held refusals, MAAP 231 of 231 committed, 0 of 20,016 passes over).
- 01:47 thirteen legs again, at `21d0e0f6`, five queues, clean clones `C2`, `CD2` (drafts), `CP2` (8x8/1if), `CX2` (probe groups); the last finished by 05:09, every one rc 0.
- 05:07 the comments (`ecb8db10`) and the documentation (`f711714b`) committed; the images rebuilt at `f711714b` equal the legs' (6 of 6). The gates started on clean clones of `f711714b`.
- 05:15 firmware self-test shard 3 at `f711714b`, rc 2: "REFUSED: SRP defect srp-poll-extra-read has 0 planting sites", its anchor the link read the poll now makes before its visits. Every gate stopped (outputs kept apart); every mutant table scanned for an anchor with no site, none other; the plant re-anchored and caught in a pre-check on the working tree ("[ok] srp-poll-extra-read: ... one link read per interface"); committed `a3f23bba` (05:24).
- 05:25 every gate restarted on clean clones of `a3f23bba`, the harness at both points (`G-A1`, `G-A8`) among them. The sweep's first attempt stopped at 05:26 in every shard's preflight, `test_suite_cancellation.py` (#833): "CLEANUP FAILED: owned descendants remain" after its `unsafe-command-SIGTERM` case in shards 0 to 2, a 12-second timeout in its `cancel-lock-wait-SIGTERM` case in shard 3; re-run once at 05:27 as instructed, both kept.
- 05:32 to 07:28 at `a3f23bba`: firmware shards 0 to 3, the lane gates (22), docs.yml (six jobs and the verifier) and the image check (6 of 6 the same), every one rc 0; `G-A1` rc 0, its figures `N-A1`'s; sweep shards 0, 1 and 3 rc 0.
- 05:48 sweep shard 2 (8 CPUs) killed by the kernel OOM killer at `native-shards.py`'s 10 GB unit limit, in `capture_coherence` (its four suites before it passed). 07:29 shard 2 alone in its own unit on its cleaned clone, 16 CPUs, the 24 GB unit cap: killed again by the OOM killer at 24 GB (08:07), in `capture_coherence`, while it compiled `Vmilan_datapath.o`. The cause, read from the suite: `tb/verilator/capture_coherence/mutants.py` runs one build per CPU in its affinity (`len(os.sched_getaffinity(0))`), each a Verilator `--build -j 0`, so its memory grows with the CPU range the unit is given. 08:09 shard 2 alone on four CPUs (the sweep's `-j4`), the 24 GB cap, its clone cleaned again.
- 07:52 to 08:06 **host incident**: soft lockups on CPUs in every range (this lane's shard 2 compiles and `G-A8` simulations among the tasks named), swap exhausted (70 MB of 37 GB free at 08:10), load average to about 146; at about 08:06 the root filesystem was remounted read-only by the kernel (`emergency_ro`), while `/data` stayed writable. The 24 GB shard 2 unit was running through it and its peak coincides; a cause is not established from the logs here. From 08:10 the output directory could not be written: this file and every later output were kept in a copy of the output directory on `/data` (identical to it at 08:10) until it can be written again. `G-A8`'s simulations ran through the incident. Its `table.md` is byte for byte `N-A8`'s, and its image's sha256 is `N-A8`'s.
- 08:27 `G-A8` rc 0 (elapsed 10,907 s); `G-A1`'s `table.md` is likewise byte for byte `N-A1`'s. 09:44 sweep shard 2 (attempt 4) rc 0, 17 of 17. The host was reset at about 09:50, ending the session (not a gate failure).
- 2026-11-03 17:00 resumed: the lane's tree clean at `a3f23bba` (no uncommitted edits), `dev-soft-core` still `a68536fa`, no new comment on #665 or PR #810 since TAKEN; the output directory writable again, the copy on `/data` brought back (identical after); every gate's rc read from its own file; the receipts collected (`scripts/collect_gates.sh`); the sweep's shard 2 attempts and the earlier rounds' shard 2 peaks recorded from the previous boot's journal; this table, `PR-BODY.md` and the index completed. No commit since `a3f23bba`, so no gate was re-run.

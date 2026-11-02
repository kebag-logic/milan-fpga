[R711] NEGATIVE - exact head 4f58214f457e963243a1fe6b86c6af161e97f26f

# R711-3: internal review of PR #810 (#665 S2b), round 13

- Head `4f58214f457e963243a1fe6b86c6af161e97f26f`, tree `3313634dcaa3d25448d03004b40de2b7cedb7ff1`.
- Base `dev-soft-core` `a68536fa`. Delta judged: `c954b8a9..4f58214f`, 23 commits.
- Authorities:
  - the frozen acceptance (#665 issuecomment-6414297191, items 3 and 6);
  - the round 13 assignment (#665 issuecomment-6573625213);
  - the owner decisions of 2026-10-29 (T_svc 20 ms) and 2026-10-30 (100 MHz on `sys`);
  - the owner's 0.5 s save (#823 issuecomment-6545894131 and -6545924397);
  - AGENTS.md sections 6 and 7;
  - my round 12 findings (R711-2) and R712-2's.

## Verdict in one paragraph

Round 12's three named defects are fixed at their cause, and each fix is measured.

- **The save's store step.** At the head, THE STEP holds every pass of a save to the share. I recomputed it from the published receipts:
  - x-save 1.628 ms and y-save 1.978 ms, against 2.388 and 2.716 ms reproduced at `c954b8a9`;
  - 0 of 99,289 passes over the share across the 24 save windows;
  - the planted store step is caught.
- **Both links at once.** One interface is built a pass, and the plant fails its named check.
- **The boot simulation.** It now runs on the product's uncached flash window, and its plant is caught.
- **Images.** The two arm-A images I rebuilt at the head are byte-identical to the measured legs' images.

The verdict is still NEGATIVE, for one MAJOR and three MINOR findings:

- **F1 (MAJOR).** The fix makes a save's progress depend on passes that take no input, and the author records that nothing bounds the wait. Round 13 item 1 requires "a save's own progress stays bounded and stated", and the round reports item 1 as Met. At `c954b8a9` progress was bounded: one store step every centisecond, whatever the input.
- **F2 (MINOR).** The one-build-a-pass rule holds in one orientation only. A probe shows interface 1 waiting three passes, built after interface 0, where the documents say neither interface waits more than one pass.
- **F3 (MINOR).** The published "a pass carrying a step is at most 1.02 ms at 8x8" is wider than its evidence. The lone save at 8x8 measures 1.264 ms.
- **F4 (MINOR).** The phase guard does not bound the end of the verify phase, while the design page says it refuses any window outside its phase.

There is also one RESIDUE and some suggestions.

## Method (what was run, and what was only read)

**Context.** I reconstructed the task in this order:

1. AGENTS.md and CONTRIBUTING.md;
2. #665's body and its S2b decisions (D4, 2026-10-29, 2026-10-30);
3. the round 13 assignment;
4. #823's 0.5 s decisions;
5. the diff `c954b8a9..HEAD`, and then `83709d3f..HEAD`, which confirms that no firmware C or H code changed after the first measured leg, only comments, the grader and the docs.

I read the prior public findings only after my own pass over the diff.

**The evidence packet.** This is `review-evidence/665s2b-r1` at `b7d1afef`, author-r13 directory.

- Every file matches `MANIFEST.json`'s `published_sha256`: 509 listed, 509 on disk, 0 bad, 42 path-redacted (`receipts/manifest_author_r13.txt`).
- The packet commit carries no cryptographic signature. Integrity here means the manifest's hashes.

**Recomputed from text receipts** (`receipts/figures_checked.txt`). The `results.json.gz` files are not in the packet, so these come from the legs' `save-windows.txt`, `step-waits.txt`, `save-alone.txt`, `run.log` and the sweep's `01.log`/`complete.json`:

| Quantity | Value |
|---|---|
| x-save / y-save / y-links / x-links-same, longest pass at the head | 1.628 / 1.978 / 1.761 / 1.543 ms |
| x-save / y-save / y-links at `c954b8a9` | 2.388 / 2.716 / 2.081 ms (equal to my round 12 probe) |
| Longest wait for a step (R-W8) | 16.95 ms |
| Longest pass carrying a step, 24 windows, 8x8, arm A | 101,796 cycles |
| Longest pass carrying a step, lone save | 126,436 cycles at 8x8, 120,515 at 1x1 |
| Durable after the change | +4,697.4 ms at 8x8, +2,018.4 ms at 1x1 |
| Sweep, all four shards at the exact head | 65 of 65 suites, 2,613,655 checks, 0 failures |
| Boot to ready | 25.515 and 64.885 ms |

**Further recomputes:**
- Section 14's gPTP additions all recompute: 0.45, 8.0 and 1.6 ms, and the margins 0.26, 0.39 over, 7.29 over, and 3.58 ms.
- Section 14's U, L and S columns recompute too. S does so only with arm A's 1x1 figures; see RESIDUE-1 (`receipts/estimate32_recompute.txt`).

**Probes run** (disposable copies under the packet's `scratch/`; the review clone was never modified):

- `scripts/rebuild_image.py`: the harness's own `build.firmware()` at the head, from a shared clone with the submodules at their gitlinks.
  - 8x8/2if arm A gives `2c6779345a95e820…`, equal to `N-A8`, `R-A8` and `X-A8`'s image.
  - 1x1/1if arm A gives `0e8e15278be90547…`, equal to `N-A1` and `R-A1`'s.
  - Receipts: `receipts/rebuild_N-A8.log`, `receipts/rebuild_N-A1.log`.
- `scripts/probe_srp_mirror.py`: the two-interface `srp_app.cpp` arm with one added mirrored test (F2). Receipt: `receipts/probe_srp_mirror.log`.
- `scripts/contract_buckets.py`: the contract's per-channel admission buckets (F1). Receipt: `receipts/contract_buckets.txt`.

**After the probes** (`receipts/clone_integrity.txt`):
- the clone's HEAD and tree are exact;
- status, index and worktree are clean;
- all six gitlinks are as recorded;
- every submodule worktree is clean.

## Findings

### R711-3-F1 - MAJOR - Conformance, Robustness, RTL (architecture) - a save's progress is unbounded under input, against round 13 item 1

**Where:**
- `sw/firmware/ctrl/loop/ctrl_loop.c:170` (`if (l->step != NULL && work == 0u)`);
- `sw/firmware/ctrl_nvm/nvm_store.c:789-808` (`nvm_store_tick` owes one step, and `nvm_store_step` takes it);
- `sw/firmware/ctrl/plat/ctrl_plat.c:260-261`;
- `docs/design/SPLIT_CONTROL_MEMORY.md:1435`;
- the PR body's acceptance row 1 and "A save's progress" paragraph;
- HANDOFF section 7, bullet 3.

**Authority:** the round 13 assignment, item 1, first sub-bullet: "A save's own progress stays bounded and stated, at 8x8, from the change to durable." The exit says: "STOP with the residual if a store phase cannot fit the share without an amendment."

**Evidence:**
- The store steps only in a pass that took no event and no record, and the lane's own test pins it: `Loop.L12StepOnlyInAPassThatTakesNoInput`, "L12 a pass that takes a record does not take the step". So any input sequence that leaves no pass empty never takes the store's step.
- At `c954b8a9` the store was a centisecond consumer (`ctrl_plat.c:258`, `ctrl_loop_add_tick(..., nvm_store_service)`). It stepped on every dispatched centisecond whatever the input, so its progress was bounded. This delta removed that bound.
- The author states the gap in three places: "Nothing here bounds that wait under input that never leaves a pass empty" (doc :1435; PR body; HANDOFF section 7). The same round still reports item 1 as **Met**, and the REVIEW READY repeats that.
- The doc's reason, "the contract's rings and buckets bound what a pass takes, not how often one takes nothing", is not established either way. The buckets are per channel (`KL_mbx_rx.sv:194-195`), and their sustained admitted rate is finite: about 1.05 records a ms over all five channels (`receipts/contract_buckets.txt`). So a bound may be derivable from the contract, the measured per-record costs and the event sources. None is derived, stated or tested.
- The one measured wait is 16.95 ms (`R-W8/step-waits.txt`). It comes from a burst window that drains, not from sustained input.

**On the owner's 0.5 s:**
- This does not break a requirement this image claims. The image's save takes 4,697 ms with no load. The 0.5 s is the append-only design's (#823), as the docs and PR body say, and no NFR for it is in this tree (`docs/reference/FR_NFR.md` at the head has none).
- It is still not correctly "left". #823's decision says "The same bound applies to the firmware writer (#665 F1)", and that writer would run through this loop's step. A step whose admission has no bound gives no worst case for any writer to meet.
- The round 13 assignment made the bound part of this round. The author neither met it nor STOPped for a decision.

**Impact:** under sustained admitted control traffic a persisted change can stay undurable for an unbounded time, and a power cut loses it. The design meant to meet the 0.5 s worst case inherits an unbounded admission rule. The acceptance report says Met for an unmet sub-bullet.

**Required outcome:** one of the following, with the acceptance row and the PR body saying which.

- **(a) A stated bound, tested.** State a worst-case bound on a save's progress at 8x8/2if, from the change to durable. Derive it from the contract's per-channel bursts and refills, every event source the loop takes, and the measured per-record and per-pass costs. Check it with a harness group that holds every channel at its refill rate, with its bursts, through a save, and grades the save's completion against the stated bound.
- **(b) A mechanism.** Bound the wait by mechanism, for example an age past which an owed step is admitted to a pass with room even if that pass took input. Every row must still fit and every pass the share. Note that the least margin, 0.71 ms, is below the longest step, 0.954 ms, so this needs measuring, not assuming.
- **(c) A recorded decision.** The manager or owner records the unbounded progress as accepted for this image under round 13 item 1, and item 1 stops being reported as Met without it.

**Verification:**
- For (a), the new group's verdict at both points and both arms, with its plant (for example, the step taken only after N empty passes) caught.
- For (b), the save windows and backlog rows re-measured, with every row within its bound.
- For (c), the decision's link in the PR body and in the docs line `SPLIT_CONTROL_MEMORY.md:1435`.

### R711-3-F2 - MINOR - RTL (architecture), Robustness, Tests, Docs - the one-build-a-pass rule holds in one orientation only

**Where:**
- `sw/firmware/ctrl/srp/srp_mbx.c:837-841` (`builds_first`), `:867` and `:877`;
- the documents: `srp_bounds.h:16-19`, `sw/firmware/ctrl/srp/README.md:152-154`, `docs/design/SPLIT_CONTROL_MEMORY.md:1383`;
- the test: `sw/firmware/ctrl/test/srp_app.cpp:404-409`.

**What the documents say:**
- `srp_bounds.h`: "the interface whose build waited goes first after that, so an interface whose build keeps failing delays the other's by one pass at most".
- The SRP README: "so neither waits more than one pass for the other".
- The test: "an interface due beside one still withdrawing is built at once".

**The cause.** `builds_first(m, n)` reads the turn interface's `reopen_polls` during the same poll loop that decrements it. When the turn interface is 0 and its LINK event withdrew it in this pass, its iteration has already set `reopen_polls` to 0 by the time interface 1 is examined. Interface 1 then sees a turn interface with no participants and no pending withdrawal, and defers. `build_turn` moves only when an interface is built, so on the next pass interface 0 (the turn) builds first and interface 1 is deferred again behind it.

**Evidence** (`receipts/probe_srp_mirror.log`, two-interface `srp_app.cpp` arm at the head):
- The lane's `JointLinkChangeBuildsOneInterfaceAPass` passes. It covers only the orientation in which the waiting interface is index 0.
- The added mirror, `ProbeMirrorJointLinkChange`, has interface 0 with the turn, interface 1 due, then interface 0 withdrawing. It fails at "an interface due beside one still withdrawing is built at once".
- It then prints "interface 1 built after 3 pass(es) from interface 0's withdrawal; interface 0 built 1". The interface whose build waited goes second, not first.

**Impact:**
- No pass exceeds the share: a deferral only shortens a pass.
- With link 1 changing and then link 0 one pass later, interface 1, and SRP's receive (which waits until both interfaces are built), wait two passes more than the stated rule allows.
- The module contract in `srp_bounds.h` and the README is false for interface 1.
- The test and the four new mutants cannot see it.

**Required outcome:**
- A rule that behaves the same in both orientations, for example the turn interface's withdrawal taken from state captured before the loop over interfaces. Or a documented bound that is true for both.
- A test of the mirrored orientation, and a mutant that test kills.

**Verification:** the mirrored case, as in the probe, passes at the corrected head, and the existing case still does.

### R711-3-F3 - MINOR - Docs - "a pass carrying a step is at most 1.02 ms at 8x8" is wider than its evidence

**Where:** `docs/design/SPLIT_CONTROL_MEMORY.md:1349`; the PR body's acceptance row 1; the REVIEW READY comment ("a pass carrying a step is at most 1.02 ms at 8x8").

**Evidence:**
- The 1.02 ms is `R-W8`: arm A, without drafts, the 24 windows only, with the read-back build. It measured 101,796 cycles.
- At the same point, the lone save in `R-A8` has a pass carrying a page program's issue of 126,436 cycles, 1.264 ms. Its read-backs reach 120,731 cycles, 1.207 ms (`R-A8/save-alone.txt`).
- No step-carrying pass was measured in arm B or with the drafts.
- The 1.22 ms at 1x1 is the longest of all passes in the 1x1 windows. That makes it an upper bound, not a measured step-carrying pass.

**Impact:** a published figure understates the longest step-carrying pass at 8x8 by about 0.25 ms. The margin it implies under the share is larger than the measured one: 0.74 ms is left, not 0.98.

**Required outcome:** scope each figure to its leg, or give the largest measured figure: 1.26 ms at 8x8, in the lone save. Say that arm B and the drafted windows are bounded only by their longest pass.

**Verification:** the sentence and the PR row against `R-W8/step-waits.txt`, `R-A8/save-alone.txt` and `R-A1/save-alone.txt`.

### R711-3-F4 - MINOR - Tests, Docs - the phase guard does not bound the verify phase's end

**Where:**
- `tb/verilator/ctrl_service_budget/grade.py:819-821`, where `'verify'` is defined as at least 30 ms after the last page, with no later page and no upper bound;
- `selftest_share.py` `phase_checks`, which has no case for a window opened after the verify ends;
- `docs/design/SPLIT_CONTROL_MEMORY.md:1347`: "`grade.save_phase` refuses a window that did not open inside it".

**Evidence:** an earlier version of this guard required a read after the window's start. Commit `5688b627` removed that, because read-backs run in passes the log prints only as a run's longest. Since then, a verify window that opens after the save is durable is accepted. Today's windows are inside: they open 40 to 48.75 ms after the last page, and the verify lasts 270 ms at 1x1 and 1.04 s at 8x8.

**Impact:** the guard exists so that a window's passes are its phase's. A smaller image, a faster read-back or a changed `save_window.PHASES` offset would put "verify" windows after the save with no refusal. The design page claims more than the code checks. No current figure changes.

**Required outcome:** bound the verify's end from something the grader can see, for example `NVM_IMG_LEN / NVM_READ_BYTES` ticks after the last page, or a log line that marks durability. Add a self-test case refused for a window that opens after the verify. Alternatively, narrow the doc's claim to what is checked.

**Verification:** `phase_checks` with the new case; the save windows regraded with 0 refusals.

### RESIDUE-1 - wording only - `docs/design/SPLIT_CONTROL_MEMORY.md:1451` - S's slope uses arm A at both ends, which the text does not say

The table's 1x1/1if column is the worst of the two arms (for example, the last AECP record is 10.17 ms, arm B). S recomputes from arm A's 1x1 figures (9.68 ms), not from that column: 28.1 ms against 26.4 ms from the printed column (`receipts/estimate32_recompute.txt`). This follows R712-2's SUGGESTION-1 in substance. No figure changes.

**Exact fix:** after "which holds the interfaces at one." add: "Its slope uses arm A at both ends, since the 8x8/1if point is arm A only: arm A's 1x1/1if figures (the last AECP record's 9.68 ms), not the worst-of-arms column below."

### Suggestions (optional)

- **S1 - `test_nvm_write.cpp` `step_room`.** The room gate is tested at `NVM_STEP_US - 1` and `NVM_STEP_US + 100`. A `<` to `<=` mutant, or `+ 1` to `+ 99` in the planted `step_needs_more_room`, would survive. Add the case with exactly `NVM_STEP_US` left.
- **S2 - the step-cost table** (`SPLIT_CONTROL_MEMORY.md:1325-1334`, `ctrl_nvm/README.md`, `nvm_store.h:68-73`). The table lists only the flash-port steps, yet the text says "the program's issue is the longest step". Capture and seal steps are not given; `N-A8/save-alone.txt` shows their passes at up to 108,517 cycles. State their store cost, so the claim covers every step kind `NVM_STEP_US` admits.
- **S3 - the step's 0.046 ms room.** The room is held by a measurement, and no gate holds it: `step_room` holds the rule, not the figure. A harness check that the longest measured store step is within `NVM_STEP_US` would turn "a slower flash port must restate the constant" into a refusal.
- **S4 - the sweep's first attempt.** Its preflight stop ("CLEANUP FAILED: owned descendants remain" in `test_suite_cancellation.py`'s SIGINT case) is the class tracked by #756 as well as #833. Name both in the PR text.
- **S5 - carried from R711-2 S3.** The platform image's hot-list check is still removed, and that is disclosed. An exclusion list would keep the guard on the product image.
- **S6 - HANDOFF section 4.** It says legs whose grader changed were regraded. `N-A1` and `N-A8` started at `83709d3f` and have no `regrade.log`. Their windows' fixed offsets mean the older phase guard accepted only windows the newer one accepts, and `pass_share` did not change after `5a1b5eee`, so their figures stand. Say so.

## The six judgements requested

1. **R711-2's MAJOR (a save's store step in a composed window).** Fixed at its cause for the share.
   - THE STEP: a step only in a pass that took no input, only while 1.0 ms of the share is left, and owed once (`ctrl_loop.c:158`, `:170`; `nvm_store.c:798-808`).
   - x-save and y-save reproduce at `c954b8a9`, 2.388 and 2.716 ms (`P0-A8`, identical to my round 12 probe), and fit at the head, 1.628 and 1.978 ms (`X-A8`).
   - Each flash phase is staged at 8 tick phases, at both points, both arms, with and without the drafts: 0 of 99,289 passes over the share.
   - The step costs are measured at both points (`R-A1`, `R-A8`), on images I rebuilt byte-identical at the head.
   - `CONTROL store-step-unbounded caught` (`CTL-A8`): 5 windows over the share with every row in bound.
   - The bound that fix gave up is F1.
2. **The joint link change.** One interface is built a pass (`srp_mbx.c:867-877`). `y-links` is 1.761 / 1.817 ms and `x-links-same` 1.543 / 1.560 ms, with 0 over. The plant `joint-reset-builds-both` fails `Srp.JointLinkChangeBuildsOneInterfaceAPass`. The mirrored orientation is F2.
3. **The boot simulation's flash window.** Holds. `boot_soc.py:93` calls `milan_soc.ctrl_uncached_flash`, and `:112-115` refuses any flash window that is not `['r']`; mode `r` carries neither cache nor execute, as `build.json`'s region list shows. `PLANT flash-window-cached: caught` (`gates/lane/boot_plants.log:18`). The README's 25.515 and 64.885 ms equal the gate logs.
4. **Stale statements and residue.** All resolved; see the table below.
5. **The author's own risks:**
   - Least margin 0.71 ms (17.29 against 18, arm B, in a save's window): measured and recorded. The doc says gPTP's mean leaves 0.26 ms and its bound does not fit. Not a finding.
   - Heaviest 8x8 pass 1.98 of 2.0 ms: fits, carries no step, recorded. Not a finding.
   - A save's progress not bounded: it does not break the 0.5 s requirement as this image claims it (see F1). It is **not** correctly recorded as left, because round 13 item 1 required it bounded and stated. That is F1.
   - The step's 0.046 ms room: held by measurement only, on identical images; see S3.
6. **The sweep.** The first attempt stopped in every shard's cancellation preflight, a known host-load class (#756, #833; see S4). The delta touches no sweep or cancellation script. The second attempt passed 65 of 65 suites at the exact head; I recomputed it from the four shards.

## Prior findings, at this head

| Finding | Status | Evidence |
|---|---|---|
| R711-2-F1 = R712-2-F1, save step in a composed window, share | **Resolved** for the share; its replacement's unbounded progress is R711-3-F1 | Judgement 1 |
| R711-2-F2, joint link change 2.08 ms | **Resolved**; the residual orientation is R711-3-F2 | Judgement 2 |
| R711-2-F3, boot flash window | **Resolved** | Judgement 3 |
| R711-2-F4, three stale lines | **Resolved** | `srp/README.md:221` gives "share of 2.0 ms"; `aecp/README.md:310` gives "20 ms local service bound"; `ctrl_nvm/README.md` gives the cadence as one step owed a dispatched centisecond, taken by THE STEP |
| R711-2-R1, save time in absolute terms | **Resolved** | `SPLIT_CONTROL_MEMORY.md:1304-1305`; PR body "Saved-state read-back" row |
| R711-2-R2, boot README caches | **Resolved** | `ctrl_split_boot/README.md:42` |
| R711-2-S1, `listener_present` | **Taken** | `srp_mbx.c:791`; `Srp.InterfaceResetClearsListenerPresent`; mutant `reset-keeps-listener-present` |
| R711-2-S2 = R712-2-F2, gPTP additions from their units | **Resolved** | Section 14's table, mean or bound per row, 8x8/2if margins; recomputed |
| R711-2-S3, hot list | Retained as S5 | Disclosed in "What is left" |
| R712-2 RESIDUE-1, harness README arm B | **Resolved** | The exact fix text is at `ctrl_service_budget/README.md:119` |
| R712-2 SUGGESTION-1, S slope across arms | Taken in substance, unstated | RESIDUE-1 |
| R712-2 SUGGESTION-2, absolute read-back time | **Taken** | `ctrl_nvm/README.md`, `SPLIT_CONTROL_MEMORY.md:1304` |

**Comment rule.** Of the delta's added C, H, C++ and Python lines, only one matched a label pattern: `B10`, the test's own step label in `plat_mutants.py`. That is not a bench lane. No new comment carries a lane name, review round, reviewer ID or issue-comment ID. No new RESIDUE of that kind.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | Round 13 assignment items 1-5 and exit against `ctrl_loop.h:62-97`, `ctrl_loop.c:158-171`, `nvm_store.c:789-815`, `srp_mbx.c:837-878`, `boot_soc.py:93,112-115`; the packet's legs P0-A8, X-A8/B8, N-*, D-*, CTL-A8, R-*; section 14 recomputed; FR_NFR.md and #823 for the 0.5 s | R711-3 | 4f58214f457e963243a1fe6b86c6af161e97f26f |
| RTL (and architecture) | UNCLEAN (F1, F2) | No HDL in the delta. `boot_soc.py` and `milan_soc.py:3228-3247` (`ctrl_uncached_flash`, unchanged), `build.json` regions; the loop's scheduling contract (`ctrl_loop.c/.h`) and SRP's build contract (`srp_mbx.c`, `srp_bounds.h`); `KL_mbx_rx.sv:194-195`, `:597-625` for the buckets; mirrored probe | R711-3 | 4f58214f457e963243a1fe6b86c6af161e97f26f |
| Robustness | UNCLEAN (F1, F2) | Sustained input against THE STEP; owed-step coalescing and the late busy-poll path (`nvm_store.c:640-650` checks done before the timeout, so a late poll is not a false timeout); deadline wrap (`nvm_store.c:802`, L11's wrap case); SRP alternation under failing builds and mirrored withdrawals | R711-3 | 4f58214f457e963243a1fe6b86c6af161e97f26f |
| Tests | UNCLEAN (F2, F4) | `test_port_loop.cpp` L10-L12 with their 8 mutants; `test_nvm_write.cpp` `step_room` with 6 plants; `srp_app.cpp`/`srp_mbx.cpp` new cases with 5 mutants; `selftest_share.py`, `selftest_mutants.py`; `build.py` `store-step-unbounded`; `run.py` verdict; boot `SOC_PLANT`; published gate receipts; two image rebuilds; SRP probe | R711-3 | 4f58214f457e963243a1fe6b86c6af161e97f26f |
| Docs | UNCLEAN (F2, F3, F4); RESIDUE-1 | `SPLIT_CONTROL_MEMORY.md` 13 (`:1291-1437`) and 14; `MAILBOX_SPLIT.md`; the `ctrl`, `srp`, `aecp`, `plat`, `ctrl_nvm`, harness and boot READMEs; `ctrl_loop.h` and `nvm_store.h` comments; the live PR body (it equals the packet's `PR-BODY.md` but for a trailing newline); comment-rule scan | R711-3 | 4f58214f457e963243a1fe6b86c6af161e97f26f |

Coverage this round: all five lenses were applied at the exact head, and none is clean. Round 12's RTL-clean (R711-2, `c954b8a9`) covered the HDL and SoC scope, which this delta does not touch. This round's RTL findings come from the architecture half of the lens: the firmware's loop and SRP module contracts. If the author believes a lens is misfiled, AGENTS.md section 3 applies.

## Real limits

- **No manager source bank at this head.** Source-head execution evidence is the author's published gate receipts. I did not rerun the sweep, the firmware or store campaigns, the harness legs, docs.yml, the builder bank or behave.
  - My own execution was limited to the two image rebuilds, the SRP mirror probe, the manifest check, the bucket table and the recomputes listed above.
- **Hosted checks at the exact head**, as I saw them at review time:
  - completed: `wire-accountability`, `docs-check-no-git` and `full-ci-gate` succeeded; `Physical gPTP` was skipped;
  - still running or queued: the 19 Verilator shards, pinned Yosys, the docs and elaborate gates, and `bdd-conformance`.
  - None of these is used as evidence here.
- **Not in the packet:** the `results.json.gz` files. Figures were recomputed from the text receipts, whose hashes match the manifest.
- **Not shown by any of this:**
  - physical calibration (NOT RUN), hardware, or a routed image;
  - real flash busy time (the harness's flash model has none);
  - the drafts beyond the scratch staging.
- **The live dev merge candidate** (`e61a4afaa54a598ceec08b7b5879285256cc60b6`) was not built or validated here.

## Pending manager duties

- Publish this report.
- Carry RESIDUE-1 to the residue checklist.
- Rule on F1's route: a bound, a mechanism, or a recorded decision.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn.
- Own hosted and local-replica acceptance at the final head.
- Re-file lenses if the author disputes them under AGENTS.md section 3.

R711-3 FINISHED

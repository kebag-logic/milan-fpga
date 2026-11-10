[R805] NEGATIVE - exact head 7c97e99f53ab0efc3e05e4617ee652dbab6e1b14

# R805-5: internal cleared-context review of PR #863 (#823 round 5)

- **Head:** `7c97e99f53ab0efc3e05e4617ee652dbab6e1b14`, tree `ffccc6f5afbb06998e37343419d4d722dcd03054`. Source base `a9d69c77`. Live `dev` is `45c0b56c`; the PR's base `dev-soft-core` is `1d6bf555`.
- **Delta judged:** `30ca4b21..7c97e99f`, four commits: `b6a60fbd`, `d01c66ad`, `a9c6391f`, `7c97e99f`. That is 48 files, all under `sw/firmware/ctrl_nvm`, `sw/firmware/ctrl/test`, `scripts/` (the page gate and the reference), `sw/builder` (two comments) and five design or integration pages.
- **Authorities:**
  - the round 5 ruling (issuecomment-6754858510);
  - decisions 3, 4, 5 and 7 of the round 2 ruling (issuecomment-6730773797), scoped to the split by the round 3 ruling (issuecomment-6730985093), items 2 to 4;
  - `docs/design/SAVED_STATE_FORMAT_32X32.md` section 4;
  - FASTCONNECT sections 5 and 7;
  - AGENTS.md sections 6 to 8.
- **Evidence read:**
  - the author's packet `review-evidence/823-r1/author-r5` at `19491031`. All 1,193 files match the published digests in `MANIFEST.json`, with none missing and none unlisted (my check);
  - REVIEW READY (issuecomment-6764816430);
  - the prior public findings of R805-4 and R806-4, read after my own pass.
- **Earlier verdicts** stand for code this delta does not touch: the codec's framing, layout 3, the builder, the flash map and the legacy rule.

## Verdict

**NEGATIVE.** Three MAJOR findings and one MINOR finding are open.

- The append path, the boot replay, the suspend and the bound are built as ruled and well tested. The four prior MINOR or RESIDUE items and the three suggestions are all met.
- **F1 (MAJOR):** the compaction copies the old slot's deltas from one read that nothing checks. One silent misread during that copy loses a save the store reported durable, once the old slot is erased. A probe reproduces it.
- **F2 (MAJOR):** item (4)'s "never half-applied" fails in two starts the shipped sweep does not exercise: a first base on blank media, and a compaction over a torn log. A cut just after the authority moves boots a state that is neither the old values nor the new ones. My run of the store's own sweep reproduces it on both ports.
- **F3 (MAJOR):** ruling item 6 (area under #818) is not met, and the ledgered 8x8 two-interface point is over its owner-set 57.5 RAMB36. The author reports both and asks for a decision.
- **F4 (MINOR):** the page's 32x32 worst case leaves out the store's own per-step cost. The host suite measures 325.19 ms against the page's 304.71 ms. The bound also depends on how often the event loop runs, and no assumption states that.

## What I ran at this head

The clone was restored and verified after every probe: index tree = head tree `ffccc6f5`, worktree identical to HEAD, gitlinks unchanged (`receipts/restore_check.txt`).

| Run | Result | Receipt |
|---|---|---|
| `test_ctrl_nvm.py --require-rv32 --self-test --jobs 12` (pinned RV32 SDK, Buildroot 2026.05 gcc 14.3.0) | rc 0. `OK across 5 shape(s), 728 tests, and all 191 planted defects reddened`. The bound printed `321274 us during the erase, 325187 us during a compaction (bound 500 ms)` and `append ... 175187 us; twice it 350374 us, the deadline 500 ms`. Wall time 1:26:40 on a host at load 85 to 100. | `receipts/ctrl_nvm_selftest.log` |
| `check_nvm_format_32x32.py` and its `--self-test`; `check_nvm_klj3.py` and its `--self-test` | Each rc 0. `0 finding(s)`. The range, list, unquoted, `line N` and `#L` plants are each caught. `self-test: PASS`. `all 9 planted defects caught` | `receipts/drift_klj3.log` |
| `ctrl_boundary.py --require-rv32 --selftest --without verilator` | Under its capture: `fw_rv32_selftest` exit 0, `test_ctrl_firmware.py --require-rv32` exit 0 (775 s), `test_ctrl_nvm.py --require-rv32` exit 0 (310 s), `fw_coverage.py --build-only` exit 0. It then **refused** (rc 2) at `sw/litex/test_ctrl_memory.py`, because this host has no `migen`. That is an environment limit, not a tree finding. The boundary verdict rests on the author's receipt (`ctrl_boundary: PASS`) and the hosted job. | `receipts/ctrl_boundary.log` |
| Three disposable probes on a copy of the tree (below) | F1 and F2 reproduced | `receipts/probes/`, `scripts/run_probes.sh` |
| Hosted checks at this head | A snapshot: 5 completed success, 20 queued or in progress. The manager owns their acceptance. | `receipts/hosted_checks_snapshot.tsv` |

## Findings

### F1 - MAJOR - Robustness, Conformance, Tests - `sw/firmware/ctrl_nvm/nvm_store.c:1302-1311`, `:1445-1464`, `:1064-1089` - the compaction copies the old slot's deltas from one unchecked read

- **Authority:**
  - The ruling's item 1 (round 3 ruling item 2): "the authority moves only after the base verifies and the deltas taken meanwhile are copied".
  - Format page section 4, rule 4: "Authority moves only then, and both slots hold every value a save reported".
  - `nvm_store.c:71-73`: "at every instant one slot holds every value a save reported".
  - The store's own fault model, `nvm_store.c:336-344` (#665 decision 2). A read can go wrong without the port saying so, which is why every boot verdict except OK stands only on two reads that agree.
- **Evidence (code):**
  - `NVM_K_COPY`'s assemble step reads one page of the old slot into `nvm_page` (`:1304`) and programs it.
  - The verify step (`:1472-1482`) compares the new slot's readback with that same `nvm_page`, so a page misread on the way in is programmed and "verified" as misread.
  - Nothing then walks the copied log, or compares it with a second read, before `nvm_cmp_next` calls `nvm_move` (`:1463`).
  - `nvm_move` prepares the old slot (`:1087`), so its intact log is erased.
- **Evidence (probe `probe_copy_misread`, `receipts/probes/probe_tests.diff`):**
  - The setup is the shipped `compaction_copy_read` scenario, with `read-flip-at:1:1:<journal_b+log_start+8>` instead of `read-fail-at`. That is one silent bit flip in the copy's read of the old slot's delta.
  - At `endstation_arty_current` the run reports the save durable: `appends 1, failed 0, ok 2, seq 6, pending 0, stale 0`.
  - A boot of the slots it leaves gives `seq_a 5, torn 1, deltas 0, seq_b 0`. Slot B is erased, and record `0xfa` has lost its saved value (`receipts/probes/probe_1x1_arty_current.log`, `probe_1x1_copy_misread_status.txt`).
  - At `endstation_ax7101_8x8` the boot is also `seq 5, torn 1` after a reported `seq 6` (`probe_8x8_ax7101.log`). The state check passes there only because that record was ahead of the base's front, so the base already carried it.
- **Test gap:**
  - `compaction_copy_read` (`test_nvm_journal.cpp:314`) and the planted defect `copy_read_fail_ignored` cover only a read the port reports failed.
  - `torn_compaction` cuts the power and never misreads.
  - No test or planted defect can see an unchecked copy.
- **Impact:** a value the store published as durable is lost at the next boot. The trigger is one transient misread in a window that every compaction with a concurrent save opens. The boot path already treats that fault as real.
- **Required outcome:**
  - Before the authority moves, the copied log in the new slot is proven, with the same strength the boot applies, to reach the old slot's sequence and end. Otherwise the move does not happen and the compaction fails or retries.
  - A test plants a silent misread on the copy and requires that no reported value is lost.
  - A planted defect that removes the proof is caught.
- **Verification:**
  - `probe_copy_misread` (or the author's equivalent) passes at both shapes.
  - The new planted defect is reddened by `--self-test`.

### F2 - MAJOR - Conformance, Robustness, Tests - `nvm_store.c:948-951`, `:972-974`, `:1064-1089`, `:1286-1295`; `test_nvm_journal.cpp:293`; `nvm_rig.cpp:387-483` - a cut just after the move boots a half-applied capture when no delta could go during the compaction

- **Authority:**
  - The round 5 focus item 4, from the ruling's decision 3 rules: "a cut at every write step leaves a state the boot accepts (completed or abandoned, never half-applied), shown by a cut campaign".
  - `nvm_store.c:71-73`: "a power cut at any step boots the old content or the new one, never a mix".
  - The rig's own oracle, `nvm_rig.cpp:460`. It accepts only `states[1]`, or `states[0]` when the save was not reported.
- **Mechanism:**
  - During a compaction, a capture marks a record below the front as `behind` (`:972-974`).
  - A record above the front goes into the base at its new value from the stage (`nvm_base_fill`, `:1293`).
  - When no delta can go (`nvm_can_append()` false, `:948-951`), the capture's records stay in flight. That happens with no authoritative slot, a torn log or a full log.
  - At the move, the new slot is the authority at the old sequence S. With no old slot it is alone. With a torn or full old slot at S it ties, and slot A wins.
  - Until the follow-up delta lands, it holds the capture's later records new and its earlier ones old.
- **Evidence (probes, which run the store's own `--powercut-compaction` sweep from two other starts, `receipts/probes/probe_8x8_ax7101.log`):**
  - `--blank` at `endstation_ax7101_8x8`, model and LiteSPI ports: `effects 55 cases 220 old 216 new 0 reported 0 bad 4`. Every bad case is `effect=55` at fractions 0, 1, 128 and 255, the first program after the base's 54 pages and the move. Since old + new = 216 of 220, the four boot a state that is neither.
  - A torn old slot (`torn_pad` in slot B), both ports: `effects 56 cases 224 old 216 new 4 reported 4 bad 4`. Again every bad case is at `effect=55`.
  - At `endstation_arty_current` both starts are clean (`bad 0`). There the 150 ms window closes after the front has passed both records. So the defect depends on the shape, and the shipping 1x1 sweep cannot show it.
- **Test gap:**
  - `torn_compaction` loads only a healthy old slot (`golden@5`). There the save appends to the old slot and that slot stays newer until the move.
  - `powercut` in `test_nvm_write.cpp:807` captures before any compaction starts.
  - Rule 3 makes the torn-log start the ordinary path after any failed delta. Item 4 asks for a campaign over every write step.
- **Impact:** after a failed delta, or on the first save to blank media, a power cut in the window between the move and the next delta restores some of one save's values and not others. For example, a map and the names saved with it.
- **Required outcome:**
  - A cut at every effect boots exactly the old or the new state from these starts too: blank media, a torn log and a full log, at a shape where the window splits the base.
  - The cut campaign covers those starts.
  - The page's rules 4 and 5 and the store comment state the guarantee that holds.
- **Verification:**
  - `probe_powercut_first_base` and `probe_powercut_torn_old`, or the author's campaign over the same starts, report `bad 0` at 8x8 on both ports.
  - A planted defect for the fix is caught.

### F3 - MAJOR - Conformance, RTL - the round 5 ruling item 6; `docs/design/SPLIT_CONTROL_MEMORY.md:230-245`; author receipt `memory/at-7c97e99f/8x8-if2.log` - the split's area is not run under #818, and the ledgered 8x8 two-interface point is over budget

- **Authority:**
  - Ruling item 6: "Area for the split placement under #818's gate against `dev-soft-core`, now that the save path lands". The ruling's done means "items 1 to 6 committed and gated".
  - The owner's 57.5 RAMB36 ledger for 8x8 with two interfaces, which the page cites (rulings 6412739248 and 6425357821).
  - AGENTS section 2: a conflict is published and decided, not chosen privately.
- **Evidence:**
  - REVIEW READY marks item 6 "**not met as ruled**" (#818's routed gate needs Vivado, and this round runs none).
  - Its linked memory plan, at this head, prints `REFUSED: allocation over budget: 59.5 RAMB36 (rom 125824 bytes in 126976, sram 114832 bytes in 116736) exceeds the 57.5-RAMB36 budget ledgered for 8x8, two interfaces` (rc 2). `30ca4b21` plans the same point at 57.5.
  - The append path adds 5,280 B of `rom` and 800 to 1,248 B of `sram` at every point.
  - I did not re-link. The claim runs against the author's own interest, and I verified the receipt's digest.
  - No CI gate plans the linked image, so nothing goes red.
- **Impact:** the PR would land a split image that does not fit the resource budget the owner ledgered for its largest point, with the ruled area gate not run.
- **Required outcome:**
  - An owner decision on the ledger is recorded: raise it, or shrink the store or another tenant.
  - Item 6 is run under #818's gate, or waived by ruling.
  - The memory page and the plan agree at the merge head.
- **Verification:**
  - `ctrl_srp_image.py --ledgered-point 8x8-two-interfaces` passes at the ruled ledger.
  - The #818 receipt (or the waiver) is linked on the PR.

### F4 - MINOR - Conformance, Docs - `docs/design/SAVED_STATE_FORMAT_32X32.md:296-299,313,339-341`; `test_nvm_bound.cpp`; `sw/firmware/ctrl_nvm/README.md:161` - the 32x32 worst case leaves out the store's per-step cost and the event-loop rate it depends on

- **Authority:**
  - The ruling's item 1: "the 32x32 worst case, from the model, against 500 ms".
  - Round 2 decision 4: "Each assumption gets a gate or a stated source".
- **Evidence:**
  - The page gives "Worst case, split **304.71 ms** + suspend", as 150 + 5.335 + 149.37 ms.
  - The store measures, in its own suite at the same datasheet maxima, `325187 us during a compaction` and `321274 us during the erase`. Without the compaction page, the arithmetic for the erase case is 299.39 ms.
  - The page and README give neither measured figure. Both runs (author and mine) print them.
  - The difference, about 20.5 ms, is the store's service calls at the suite's 100 us event loop. Each record of the capture and each phase of each page takes one call: about 205 calls.
  - So the bound also holds only while the event loop's pass time stays under about 0.95 ms (or about 0.46 ms to keep the page's 95.29 ms suspend room).
  - A1 to A3 do not state that rate, and no source or gate fixes it. The README says only that F0's loop calls the service once per pass.
- **Impact:**
  - The page's worst case is lower than the store's own measured worst case.
  - A loop slower than about 1 ms per pass breaks the 500 ms bound with every A1 to A3 assumption met.
  - The suspend room and its 6,352x margin stay conservative for the split, whose measured room is about 174.8 ms.
- **Required outcome:**
  - The page states the measured worst cases and the loop period they assume.
  - The page adds the event-loop pass time as a stated assumption with a source or gate, or counts the per-step cost in its arithmetic.
  - The margins are restated to match.
- **Verification:** the drift gate holds the new figures. If it is a gate, a plant at a slower loop is refused.

### RESIDUE (wording only)

- **RS-d - `sw/firmware/ctrl_nvm/test/nvm_rig.hpp:18` and `nvm_suite.hpp:9`.** Both name `scripts/nvm_klj2.py` as the fixture's source, in files this delta edits. The author found this and did not change it. **Exact fix:** say `scripts/nvm_klj3.py` in both. Leave `nvm_rig.cpp:247`, which describes the payload rule, and `test_nvm_boot.cpp:12`, which names the all-fabric KLJ2 container, as they are.
- **Comment rule:**
  - No new comment in the delta shows a lane label, review round, reviewer ID or comment ID.
  - `nvm_store.c:339` "(#665 issue comment 5999350068)" is a reflow of an existing line, tracked by #746.
  - The new `Anchor("F1 store", ...)` strings in `scripts/nvm_format_32x32_tables.py` are table labels that the page prints, not comments.

### SUGGESTION

- **SG-a (Tests):** `test_nvm_journal.cpp` `compaction_copy_read` and the probe above show that a state check against `golden@5+one3@6` cannot see a loss at a shape where the changed record was ahead of the base's front. Requiring the boot's `seq`, `deltas` and `torn` too would make such checks shape-independent.
- **SG-b (Robustness):** `nvm_delta_begin` (`nvm_store.c:898-908`) stops at the first in-flight record that does not fit and leaves smaller later ones for the next delta. That is correct and bounded. One line in the README saying so would spare the next reviewer the check.

## The ruling's items, at their cause

| Item | Result | Evidence at this head |
|---|---|---|
| 1. Append-only save path | **Built, with F1 and F2 open** | Rule by rule, each with the test its planted defect reddens in my self-test run: <br>• **a save appends only changed records as one delta and never erases:** `nvm_capture_end` and `nvm_delta_begin`, `nvm_store.c:926-954` and `:890-923`; `replay_skipped` caught by `append_order, change_commit_bytes`; `erase_authoritative` caught by `change_commit_bytes, powercut`; `seg_cap_ignored` caught by `burst_deltas`; `full_drops_save` caught by `reserve_exhausted`. <br>• **a torn or failed delta forces a compaction:** `nvm_fail` `:1005-1006` and `nvm_cmp_wanted` `:1125`; `torn_appends` caught by `torn_delta, media_failures`; `torn_without_program` caught by `suspend_slow, suspend_master_stall`. <br>• **the compaction writes the other slot page by page and yields to saves:** `nvm_cmp_next` `:1449-1453` and the idle order `:1241-1246`; `compaction_never_yields` caught by `compaction_yields`. <br>• **a record cut by a page boundary is carried whole:** `nvm_carry_step` `:1324-1345`; `carry_dropped` caught by `compaction_carry`. <br>• **the authority moves only after the base verifies and the deltas are copied:** `move_before_base_closes` caught by `torn_compaction, compaction_bytes`; `move_before_copy` caught by `compaction_yields, torn_compaction`; `base_seq_above_old` caught. **F1: the copy itself is unchecked.** <br>• **boot replays the chosen slot's deltas:** `nvm_restage_once` `:552-567`; `deltas_applied_out_of_order`, `replay_past_judged_end` and `log_walk_unconfirmed` each caught. <br>• **STOP condition:** does not apply. `git diff 30ca4b21..7c97e99f -- hdl protocol-processor gptp-processor sw/firmware/milan_baremetal` is empty, the gitlinks are unchanged, and the store reaches the flash only through `plat/nvm_flash_litespi.c` (`LS_CMD_PES 0x75`, `LS_CMD_PER 0x7a`). |
| 2. Suspend, replay, 32x32 against 500 ms | **Met, with F4 open** | The model's suspend is 15 us typical (`host/nvm_fmodel.c:15-17`). Every suspend is timed (`nvm_suspend_wait`, `nvm_store.c:1407-1422`), and the slow ones are counted against `NVM_SUSPEND_ROOM_US 95290u`; `slow_suspend_not_counted`, `suspend_untimed`, `late_suspend_kept`, `erase_deadline_counts_suspend`, `no_resume` and `save_waits_for_erase` are each caught. The worst case is 325.19 ms against 500 ms; F4 is about the page's statement of it. |
| N1 | **Resolved** | `SPLIT_CONTROL_MEMORY.md:144` reads "3,344 against 13,264 bytes", as at `a9d69c77`, and line 146 points to section 5 for the KLJ3 sizes. |
| N2 | **Resolved** | `QSPI_FLASHBOOT.md:58-68` lists the readers and writers of each range, as FASTCONNECT section 5's table does (lines 541-545, 553-559). The "nothing writes or reads" and "blank-flash responder" text is gone. |
| RS5, RS6 | **Resolved** | FASTCONNECT lines 101 and 118. |
| RS-a | **Resolved** | `nvm_klj2.c:3`, `nvm_klj2.h:4` and `nvm_shape.h:4` read "(#665, the split placement's saved-state store)". No "(#665, the F1 store)" is left in `sw/firmware/ctrl_nvm`. The older "#665 lane F1" headers are #746's. |
| RS-b | **Resolved** | `test_nvm_write.cpp:17,73,82,96,113,775` name `nvm_klj3.py`. `nvm_rig.cpp:247` and `test_nvm_boot.cpp:12` are unchanged, as ruled. The two remaining names are RS-d. |
| SG3 = S-a | **Met** | `check_nvm_format_32x32.py:57-58`. The range, list, unquoted, `line N` and `#L` forms each have a plant, all caught. |
| SG4 = S-b | **Met** | `test_ctrl_nvm.py` `AT_WIDTH = (..., 255)` must compile. `mapin_width_off_by_one` (`>= 255u`) is caught by `over_width`. |
| S-c | **Met** | `nvm_shape.h:191-193` `#error` outside `NVM_HOST_SHAPE`. `doctored_error_removed` is caught by `doctored_outside`. |
| 4. Power-cut safety by campaign | **Not met (F2)** | `powercut` (3 starts) and `torn_compaction` pass in my run. My run of the same sweep from blank media and from a torn log fails. |
| 5. Area under #818 | **Not met (F3)** | As F3. |
| RS-c = SG5 | **Residue, tracked by #495** | Not this round, as ruled. |
| Prior R805-1 F1-F6 and R806-1 F1-F7 | Resolved at round 4 | They are not reopened by this delta, which does not touch their artifacts beyond the documented moves. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | **UNCLEAN** (F1, F2, F3, F4) | The round 5 ruling items 1 to 6 against `nvm_store.c:1-1595`, `nvm_store.h:86-94`, `nvm_shape.h:135-200`, `SAVED_STATE_FORMAT_32X32.md:255-364`; the round 2 decisions 3, 4, 5 and 7; the STOP diff (empty) | R805-5 | `7c97e99f53ab0efc3e05e4617ee652dbab6e1b14` |
| RTL | **UNCLEAN** (F3) | The store's FSM `nvm_store.c:800-1554` (every phase, failure, suspend and resume path); widths in `nvm_seg_read` `:385-459` and `nvm_delta_begin`; the step bound (`step_max == step_bound` in `service_bound`); the RV32 build sizes in `receipts/ctrl_nvm_selftest.log`; the memory plan receipt for F3. No HDL or processor gitlink changed. | R805-5 | `7c97e99f53ab0efc3e05e4617ee652dbab6e1b14` |
| Robustness | **UNCLEAN** (F1, F2) | Misread, torn, stale and refused deltas, the prep and erase failures, suspend faults and deadlines (`test_nvm_journal.cpp`, `test_nvm_write.cpp:230-460`); probes `receipts/probes/*` | R805-5 | `7c97e99f53ab0efc3e05e4617ee652dbab6e1b14` |
| Tests | **UNCLEAN** (F1, F2) | `receipts/ctrl_nvm_selftest.log` (728 tests, 191 of 191 planted defects reddened); the 56 new planted defects in `nvm_mutants.py` mapped to their tests (table above); `nvm_rig.cpp:356-483` sweeps; `test_nvm_bound.cpp`; `receipts/drift_klj3.log` | R805-5 | `7c97e99f53ab0efc3e05e4617ee652dbab6e1b14` |
| Docs | **UNCLEAN** (F4) | `SAVED_STATE_FORMAT_32X32.md` section 4 and the test plan; `SPLIT_CONTROL_MEMORY.md:140-146,227-245`; `QSPI_FLASHBOOT.md:56-68`; FASTCONNECT lines 101, 118 and 535-559; `sw/firmware/ctrl_nvm/README.md` (the journal, boot and port sections); REVIEW READY. N1 and N2 are resolved; RS-d is residue. | R805-5 | `7c97e99f53ab0efc3e05e4617ee652dbab6e1b14` |

## Real limits

- **Probes.** All three are disposable tests on a copy of the tree, driven through the store's own rig and fault knobs. They are not proposed tests.
- **F2's shape dependence.** F2 shows at the 8x8 shape. I did not run it at the 32x32 bound shape or the other three shapes.
- **Area.** I did not re-link the split image (F3 rests on the author's digest-checked receipt). No Vivado, no #818 route.
- **Boundary gate.** My `ctrl_boundary` run stopped at `test_ctrl_memory.py` for want of `migen` on this host. Every firmware builder before it exited 0.
- **What I did not run here:** the control mutants (570), the AECP and SRP campaigns, `behave`, the twin and `twin-plants`, the LiteX simulations and the full sweep. The author's receipts cover them, and none reads the store's save path beyond what the boundary capture ran.
- **No hardware.** The real N25Q128 suspend latency, LiteSPI timing and real power cuts are unproven. Physical calibration was NOT RUN.

## Pending manager duties

- The owner's decision on the 8x8 two-interface ledger, and the #818 area gate or its waiver (F3).
- Hosted acceptance at this head. The snapshot shows the run in progress.
- The current-dev merge candidate (builder and native banks) at the merge turn.
- RS-d to the residue checklist. RS-c = SG5 is already on #495.

R805-5 FINISHED

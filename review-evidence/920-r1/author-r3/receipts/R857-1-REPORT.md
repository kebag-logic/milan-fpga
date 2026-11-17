[R857] NEGATIVE - exact head bd252db1d73511307c0ecb78470f0d15d0c3ea9b

# R857-1: internal cleared-context review of PR #938 (issue #920)

- **Head:** `bd252db1d73511307c0ecb78470f0d15d0c3ea9b`, tree `2cc90eb47ddd00d5bd7d1d5edb6c7ec0937b509a`, on `dev-soft-core` `70f4056f` (merge `d66b4045`). Source base `659d7687`.
- **Verdict:** NEGATIVE. Two MINOR findings are open:
  - F-1 (Tests, Robustness): the resets of the two new state flags are not tested. Removing either one gets past every store check, and each removal is a real defect.
  - F-2 (Conformance, Docs): the frozen 8x8 load criterion (0.75) has no figure and no ruling behind it. At this head the only 8x8 load is over it.
- **The fix itself checks out:**
  - The cause was proven at the base.
  - Only the ruling's three mechanisms are used.
  - The termination argument holds.
  - The 1x1/1if target reproduces exactly.
- **Prior public review findings:** none. Before this round the PR held only the two review-start comments (R857-1, R858-1). No other review or finding comment exists, so nothing is carried, resolved or retained.

## Reconstruction

The task was rebuilt from these sources:
- AGENTS.md, CONTRIBUTING.md and docs/README.md.
- Issue #920: its body, the TAKEN comment, the STOP and the ruling issuecomment-6910219988.
- #665: finding 13 (issuecomment-6899519003) and ruling issuecomment-6899740728, item 1 (target; allowed and refused mechanisms) and item 4.
- Milan v1.2 5.3.13.
- DR2a (the SAVED_STATE_MATERIALIZATION.md register row; SAVED_STATE_FASTCONNECT.md 9.x).
- The owner decision of 2026-11-11 setting the 8x8/2if flip ceiling at 0.75, recorded on #665.
- `git diff 659d7687..bd252db1` and the PR's own delta `70f4056f..bd252db1` (28 files, no `hdl/`, `syn/`, mailbox-contract or `ctrl_loop.c` change).
- The commit history `945a1217..bd252db1`.
- The author packets `author-r1` and `author-r2` at archive `4a3e37f8`.

## Checks against the brief

1. **The cause, proven at the base. Confirmed independently.**
   - At `659d7687` the PR's unit test runs on the base's own `aecp_nvm.c`. The test is inserted less its `pending_count` line, which the base lacks.
   - Result: 34 of 39 marks reach the store, and names 34 to 38 come back as defaults after the real store's power cycle: AUDIO_CLUSTER 22/23/24, CONTROL 0 and CLOCK_DOMAIN 0.
   - At `945a1217` the same test passes.
   - Receipts: `receipts/cause/run-659d7687.log`, `run-945a1217.log`, `scripts/base_cause_probe.sh`.
   - The harness control `store-names-past-256-lost` re-plants the base's lost mark at 1x1/1if. It is caught: names 34 to 38 are never durable and 5 names are missing at the cut (`receipts/runs/ctl-names256-1x1.log`).
   - The 8x8/1if trap and the board's console bits are the author's receipts. The console shows `backed=1 dirty=0 pend=0 verdict=0` before the cut, and the defect predicts exactly that. They were read, not re-run.
2. **Only the ruling's three mechanisms are used, and no refused one.**
   - The PR's delta changes none of these: `NVM_STEP_US`, `CTRL_LOOP_STEP_AGE`, `MILAN_NVM_DEBOUNCE_MS`, the tiers, the pace, the two-slot sequence, the blank check, the verify, `nvm_klj2.c`, `nvm_shape.h`, `nvm_layout3.h` or `ctrl_loop.c`.
   - The join is at `nvm_store.c:636-675` and `:943-949`.
   - The next save at the first idle step is at `:548-558`, `:950-953` and `:896-901`.
   - The step a pass is at `:912-925`. The loop calls it only in a pass with `work == 0` (`ctrl_loop.c:336-339`), one service per call, and only with `NVM_STEP_US` left.
   - A first change still arms DR2a's window (`:954-957`).
3. **Store and AECP state stay consistent across a power cut.**
   - The join and the walk again change only the RAM stage before the seal, and the seal's CRC covers the final stage.
   - Flash effects and their order are unchanged, so a cut at any step boots the old container or the new one. The `powercut` case is unchanged and green.
   - Termination of the walk again was checked against the walk:
     - `nvm_rec_id_known`/`nvm_rec_id_of` (`nvm_klj2.c:199-214`) accept exactly the ids that `nvm_rec_first/next` visit (`:143-170`).
     - A walk again happens only when some record is dirty and not in flight. That walk takes such a record, which moves it in flight, and nothing clears in-flight records during a capture. So each capture takes each record at most once and ends.
   - The AECP side's `pending_count` follows its bits. `mark` counts only a clear bit, `poll` uncounts the bit it clears, and `init` zeroes both.
   - `_Static_assert` (`aecp_nvm.c:135`) and `AECP_NVM_WORDS` = 36 cover id space 1,129.
4. **The target.**
   - 1x1/1if was reproduced at this head with byte-identical firmware: `ctrl_app.elf` sha256 `e6ce5e91…`, equal to the author's `fixture-1x1-1if` on `d66b4045`. Results:
     - `save-burst`: 1,107.785 ms, 1 save, the cut at sequence 1, 0 missing.
     - `save-flight`: 165.045 ms, 19 steps (want 19).
     - `save` 1,081.825, `save-held` 1,097.164, `save-starved` 4,049.108 of 4,070, `save-second` 6,030.340 of 6,070.
     - 6 groups, 0 refusals, 0 budget misses, 0 of 75,219 work passes over the share, rc 0 (`receipts/runs/save-1x1.log`, `receipts/harness-1x1/`).
   - 8x8/1if was **not re-run** (see limits). Its firmware image matches the author's byte for byte: sha256 `898c2860…` = `fixture-8x8-1if` on `d66b4045`.
   - The author's receipts give 1,370.301 ms (6 saves, 0 missing) and 663.104 ms (59 of 59 steps), with 0 refusals and 0 of 6,322 over the share.
5. **Tests.**
   - Store suite: OK across 5 shapes, 546 tests, all 152 planted defects caught (`receipts/runs/store-suite.log`, rc 0).
   - Harness self-test: 0 failures, 251 mutants caught (`harness-selftest.log`, rc 0).
   - AECP `Nvm.*`: 9 of 9 pass.
   - AECP mutation campaign, shard 2/4: PASS, 302 mutants caught. That includes `nvm-ids-past-256-dropped`, `nvm-pending-counted-twice` and `nvm-pending-count-kept` (`aecp-campaign.log`).
   - `fw_coverage --check`: PASS. `aecp_nvm.c` and `nvm_store.c` are at 100 % lines and branches under the ratchet.
   - Controls `store-names-past-256-lost` and `store-next-save-waits` are caught by name at 1x1/1if (the latter shows 111 steps, want 19). `store-step-only-owed` at 8x8/1if is the author's receipt (8,021 ms, OVER).
   - Removing the join control (`339d0224`) is justified in substance. The removed plant escaped at 8x8/1if (7 saves, every name at the cut, author's receipt). The store units catch a dropped join: `join_never_walks_again` is caught by `capture_joins` and `capture_window_edges`, and my `probe_joined_behind_any_dirty` is caught too. The wording of that justification is R-2.
   - The gap: see F-1.
6. **CPU budget.**
   - At my 1x1/1if save groups: no refusal and no pass over the share.
   - Load: `load_grade.py --check` rc 0, 1x1/1if 0.517 (0.514 with #32) of 0.70. This is identical to `70f4056f` (`gate-load_grade-check*.log`). The PR changes no load term.
   - The 8x8 load: see F-2.
   - The memory ledger (`test_ctrl_memory.py`) passes, rc 0.
   - ROM: my 1x1 image's plan is 112,728 B of rom, 55,264 B of sram and 41.5 tiles, equal to the author's merge table.
   - The seven held-egress rows and the 8x8/1if stated-cost lines are the author's full-point receipts. The stated-cost lines are ruled as #914's.
7. **The merge's four resolutions.** The merge was replayed (`54280c94` + `70f4056f`), and the conflicts are exactly `SPLIT_CONTROL_MEMORY.md`, `aecp_nvm.h`, `ctrl_memory.py` and `ctrl_memory_ledger.py`.
   - `aecp_nvm.h` keeps #901's `aecp_name_run` and `names`/`name_runs` together with #920's `AECP_NVM_WORDS`, `pending[]` and `pending_count`.
   - Both ledger files keep #895's 60.5 reason and add #920's "within it" text. The `ctrl_plat` sizes of 17,664, 19,200, 18,304 and 20,480 B are re-measured, not either side's.
   - The doc conflict keeps both sides. Both sides are kept.
8. **Gates at this head.**
   - `docs_check.py`: 0 findings. `check_doc_style.py`: OK. `check_doc_paths.py`: OK. `check_py_idiom.py`: rc 0.
   - The 65-suite sweep (65 of 65, 2,713,040 checks) is the author's receipt. The four shard totals add up to the claim. Not re-run.
   - The firmware, elaborate and docs workflow receipts are the author's.
   - Hosted runs at this exact head: 50 check runs, 9 success, 1 skipped (Physical gPTP, nightly and manual), 40 queued or in progress, 0 failed (`receipts/hosted-check-runs-bd252db1.json`). The manager owns these.

## Findings

### F-1 MINOR: the resets of the store's new state flags are not tested

- **Lenses:** Tests, Robustness.
- **Where:**
  - `sw/firmware/ctrl_nvm/nvm_store.c:536` (`nvm.rewound = 0;`) and `:540` (`nvm.next_now = 0;`), both in `nvm_capture_begin`.
  - Their tests: `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:164` (`capture_joins`) and `:239` (`busy_steps`), and `sw/firmware/ctrl_nvm/test/nvm_mutants.py:371-394` (#920's mutants).
- **Authority and evidence:**
  - AGENTS.md section 5 asks for reset, ordering and failure paths to be tested. Section 6 (Tests) asks that each test can fail for the defect it claims to detect.
  - The ruling (#665 issuecomment-6899740728, item 1) refuses "a shorter first-dirty window for a first change".
  - Probe round 1 (`receipts/runs/store-probes-round1.log`, `scripts/store_probes.py`) planted seven defects through the suite's own self-test at its shape, each against all 19 write-path checks. Three left every check green:
    - `probe_next_now_kept`: line 540 removed.
    - `probe_rewound_kept`: line 536 removed.
    - `probe_rewound_walk_refuses_join`: on the walk again, no change joins.
  - Probe round 2 (`receipts/runs/store-probes2.log`, `scripts/store_probe_tests.py`) added three reviewer tests. All three pass on the head's code: the boot and write paths binary ran 112 tests with 0 failures.
    - `probe_first_change_after_flight` **catches** `probe_next_now_kept`.
    - `probe_retry_after_rewind` **catches** `probe_rewound_kept`.
- **Impact:** each surviving reset defect is a real regression that no gate would see.
  - With `next_now` left set, every later first change after a save that a change in flight left starts at the first idle step without its 1,000 ms window. That is the refused mechanism. The loop also takes an idle step in every empty pass for good.
  - With `rewound` left set after any capture that walked again, a later failed attempt's retry skips a record in flight that was changed in its backoff. The save then commits without it, and with no window or `next_now` pending, that acknowledged change is never written. It is lost at the next power cut. Milan v1.2 5.3.13 is the requirement at stake.
  - `capture_joins` case 4 (`test_nvm_write.cpp:191`) claims "on the walk again a record no capture holds joins". It passes even when joins are refused on the walk again, because the record it marks lies ahead of the rewound cursor and that walk takes it anyway. My own variant has the same blind spot.
- **Required outcome:**
  - Self-checking store tests, and named entries in `nvm_mutants.py`, that fail when either reset is removed:
    - a first change after a save that a change in flight left waits its DR2a window;
    - a retry after a capture that walked again takes the record in flight changed in its backoff, and the change is durable.
  - Either a case-4 variant that marks a record behind the rewound cursor, so that a refused join is distinguished from the next save, or the case's claim narrowed to what it shows.
- **Verification:** the store suite's self-test catches each new plant by name, and the suite stays green.

### F-2 MINOR: the frozen 8x8 load criterion has no figure and no disposition

- **Lenses:** Conformance, Docs.
- **Where:** issue #920 acceptance item 3 ("the load within 0.70 (1x1) and 0.75 (8x8)") and ruling item 1, Budget ("the load within 0.70 and 0.75"). Against them, REVIEW READY issuecomment-6932870595 ("Load gate: 1x1/1if at 0.517 of 0.70", "Acceptance criteria: met") and the PR body.
- **Evidence:**
  - At this head `load_grade.py --check` reports 8x8/2if at 0.798 at the pin and 0.756 with tsn-c-stack #32. Both are over 0.75, the ceiling the owner set for 8x8/2if on 2026-11-11.
  - Both figures equal `70f4056f`'s (`receipts/runs/gate-load_grade-check.log`, `gate-load_grade-check-base70f4056f.log`).
  - No gate computes an 8x8/1if load.
  - Neither the REVIEW READY nor the PR body states an 8x8 load or a disposition. The PR's own changes move no load term, so the figure is the base's.
- **Impact:**
  - A frozen acceptance criterion is reported met with no evidence, and the only 8x8 figure at this head contradicts it.
  - A cold reviewer cannot tell whether the criterion is owed elsewhere or not met.
  - AGENTS.md section 2 asks for such a conflict to be published as needing a decision.
- **Required outcome:** the PR and issue state the 8x8 load at this head against 0.75, for the point the ruling means. Then either show it within, or carry a recorded maintainer decision that it is the base's and owed elsewhere (for example the owner decision's closing path, #890). The acceptance line is amended to match.
- **Verification:** the figure and its disposition can be found on the PR or issue, with the decision linked.

### R-1 RESIDUE: issue-comment IDs in new source comments (owner rule 2026-10-15)

- **Where:**
  - `sw/firmware/ctrl_nvm/test/test_nvm_write.cpp:155`: `// #920 (#665, the ruling of issuecomment-6899740728, item 1)`.
  - `tb/verilator/ctrl_service_budget/save_burst.py:5`, docstring: `THE TARGET (#665, the ruling of issuecomment-6899740728, item 1)`.
  - Related: the printed table heading string at `tb/verilator/ctrl_service_budget/run.py:373-374`.
- **Exact fix:** write "#665's ruling on finding 13, item 1" and drop `issuecomment-6899740728` from each. These are comments and an output label only, and change no behaviour.

### R-2 RESIDUE: the stated reason for having no join control describes a different defect from the one measured

- **Where:** `tb/verilator/ctrl_service_budget/save_window.py:70-73` and `tb/verilator/ctrl_service_budget/README.md:129`.
- **The problem:**
  - Both say "left out, that change is the next save's, which starts at the first idle step … (7 saves where the join makes 6 at 8x8/1if …)".
  - The 7-save figure is the removed plant's (`if (0 && nvm_joined_behind())`, `339d0224`). Under that plant, a change behind the cursor opens no window and sets no `next_now`. It is written only because a later change in flight starts a next save.
- **Exact fix:** say the figures are the removed plant's, and that under it the left-out change is written by the next save that a later change starts. The reason itself stands: the store's units hold the join.

### S-1 SUGGESTION: the step a pass relies on the image never sleeping

- **Where:** `sw/firmware/ctrl_nvm/nvm_store.c:912-925` and `ctrl_loop.c:336-355`.
- **The point:** a busy step that is not owed returns false. So on a platform built with `CTRL_MBX_WFI`, a pass that only stepped would sleep in `mbx_hal_wait()`, and the save would fall back to a step a centisecond.
- **No effect now:** the split image defines no WFI (`mbx_plat_mmio.c:16-20`), and `nvm_store.c:905-911` says it relies on that.
- **Optional:** state the dependency in THE STEP (`ctrl_loop.h`) as well.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F-2) | Issue #920 acceptance; ruling 6899740728 item 1; ruling 6910219988; `nvm_store.c:548-559,636-675,896-959` against the allowed and refused mechanisms; DR2a register row; `load_grade.py --check` here and at `70f4056f`; the cause probe at `659d7687` | R857-1 | `bd252db1d73511307c0ecb78470f0d15d0c3ea9b` |
| RTL | CLEAN | `nvm_store.c` state machine (join, walk again, `next_now`, `nvm_busy`, `nvm_store_step`); termination against `nvm_klj2.c:143-214`; `aecp_nvm.c:134-191` and `aecp_nvm.h:8-33` widths, `_Static_assert` and count; `ctrl_loop.c:259-356` unchanged; delta has no `hdl/`, `syn/` or mailbox file; merge resolution of `aecp_nvm.h` | R857-1 | `bd252db1d73511307c0ecb78470f0d15d0c3ea9b` |
| Robustness | UNCLEAN (F-1) | Retry and backoff (`nvm_fail`, `nvm_idle`), DR2b and DR2c paths after a join, HELD writer, no-room passes, failed-attempt `next_now`; probes `store-probes-round1.log` and `store-probes2.log` | R857-1 | `bd252db1d73511307c0ecb78470f0d15d0c3ea9b` |
| Tests | UNCLEAN (F-1) | `test_nvm_write.cpp:140-280`, `test_nvm_more.cpp:112-138`, `nvm_mutants.py:352-394`, `test_aecp.cpp:347-372`, `aecp_mutants.py:452-472`, `save_burst.py`, `selftest_burst.py`; store suite 546/152; harness self-test 251; AECP shard 2/4 (302); `fw_coverage --check`; 1x1 controls | R857-1 | `bd252db1d73511307c0ecb78470f0d15d0c3ea9b` |
| Docs | UNCLEAN (F-2) | `SPLIT_CONTROL_MEMORY.md` section 3 (line 147) and "A burst of names and a change in flight (#920)" (line 2726); `ctrl_nvm/README.md`; `nvm_store.h:11-40`; `ctrl_loop.h:120-145`; `ARCHITECTURE_HW_SW_SPLIT.md:171`; `nvm_split_target/README.md:158`; the harness README; PR body and REVIEW READY; docs, style, paths and idiom gates | R857-1 | `bd252db1d73511307c0ecb78470f0d15d0c3ea9b` |

The docs figures I could check match my receipts:
- save-burst and save-flight at 1x1/1if: 2,916 and 3,131 work passes, 0 over the share;
- 1,107.8, 165.0 and 1,081.8 ms;
- the ROM plan.

The residues are wording only.

## Limits of this round

- **8x8/1if harness not re-run.** Its CPU netlist (`VexiiRiscvLitex_38b7c320…`) is not in the shared LiteX cache. Generating it would write into the shared install and the user's sbt caches, which this round may not touch.
  - For 8x8/1if (`save-burst`, `save-flight`, the `store-step-only-owed` control, the stated-cost lines), the figures are the author's receipts.
  - What I did check: the image is byte-identical to the author's.
- **Not run:**
  - the full 98- and 97-group points (backlog-owed's seven held-egress rows);
  - the 65-suite sweep;
  - elaborate;
  - the control and SRP mutation campaigns, and the AECP campaign's other three shards;
  - the 8x8 ROM builds other than the 1x1 and 8x8/1if fixture images;
  - any route.
- **Bench:** physical calibration NOT RUN. No hardware was touched, and field skips are not hardware proof.
- **Hosted runs:** read, not accepted. Most were still queued.

## Pending manager duties

- Validate the current-dev merge candidate (source base `659d7687`, live dev `6b66f66d`) with builder and native banks, and link the receipts.
- Hosted and act acceptance at the exact head.
- The sync onto #919's review head (ruling item 4).
- Carry R-1 and R-2 to the residue checklist.
- The bench persistence scenario at both shapes, three runs each (issue acceptance).

## Run index

- Commands: `scripts/env.sh` (`REPO`, `TOOLS`), with the PR's own validation commands.
- Probes: `scripts/base_cause_probe.sh`, `scripts/store_probes.py`, `scripts/store_probe_tests.py`.
- Every receipt listed in `MANIFEST.sha256`.
- After the probes, the clone was verified: HEAD and tree are exact, index entries equal the tree (`git ls-files -s` digest equals `git ls-tree -r HEAD`), the worktree is clean, and every submodule gitlink equals its index and checkout (`receipts/clone-integrity.txt`). One untracked directory left by the AECP campaign was removed.

R857-1 FINISHED

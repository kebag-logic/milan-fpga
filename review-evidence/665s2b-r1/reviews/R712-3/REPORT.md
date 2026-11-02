[R712] NEGATIVE - exact head 4f58214f457e963243a1fe6b86c6af161e97f26f

# R712-3: external review of issue #665 lane S2b, PR #810, round 13

- **Head:** `4f58214f457e963243a1fe6b86c6af161e97f26f`, tree `3313634dcaa3d25448d03004b40de2b7cedb7ff1`.
- **Base:** `dev-soft-core` `a68536fa`.
- **Delta judged:** `c954b8a9..4f58214f`, 23 commits, 48 files, against the round 13 assignment (#665 issuecomment-6573625213) and the round 12 findings of R711-2 and R712-2.
- **Role:** external, cleared-context reviewer.
- **Verdict:** NEGATIVE, on one MAJOR and one MINOR.
  - Every round 12 finding is resolved at its cause.
  - The one-build-a-pass link change, the boot simulation's flash window and the gPTP restatement are correct, and I reproduced or recomputed them.
  - **The MAJOR:** round 13's frozen item 1 requires that "a save's own progress stays bounded and stated, at 8x8, from the change to durable". The fix for the share (THE STEP) makes a save's progress depend on passes that take no input. The author's own documents say that nothing bounds it. The REVIEW READY still marks item 1 "Met".

## Authority read (in this order)

1. AGENTS.md and CONTRIBUTING.md (via AGENTS.md's contract), then docs/README.
2. Issue #665's body: the owner decisions of 2026-10-31 and the original scope.
3. The round 13 assignment (issuecomment-6573625213): items 1 to 5 and the exit.
4. The owner's save bound on #823, 2026-10-31 (comments 6545894131 and 6545924397): "A save is bounded by 0.5 s worst case, from the change to durable in flash, at 32x32 ... The same bound applies to the firmware writer (#665 F1)".
5. The ingress contract's token buckets (`sw/mailbox/mailbox.yaml:1139,1158,1173,1195,1210`) and their RTL (`hdl/milan/mailbox/KL_mbx_rx.sv:597-619`, one bucket per channel).
6. `git diff c954b8a9..4f58214f` and its history.
7. The author's REVIEW READY (#665 issuecomment-6588508497).
8. The evidence commit `b7d1afef`, `review-evidence/665s2b-r1/author-r13/`, with its HANDOFF, PR-BODY, receipts and INDEX.
9. Exact-head hosted check runs.

Prior public findings (R711-2 and R712-2 reports in the same evidence commit) were read only after my own pass over the diff.

## Findings

### R712-3-F1 - MAJOR - Conformance, RTL (architecture), Robustness, Docs - a save's progress is not bounded under input, against round 13 item 1

**Where:**
- `sw/firmware/ctrl/loop/ctrl_loop.c:169-172`: the step is called only when `work == 0u`, that is, only in a pass that took no event and no record.
- `sw/firmware/ctrl_nvm/nvm_store.c:789-808`: `nvm_store_tick` only marks a step owed, once. `nvm_store_step` is the only path to `nvm_store_service`.
- `docs/design/SPLIT_CONTROL_MEMORY.md:1435` ("What is left"): "Nothing here bounds that wait under input that never leaves a pass empty: the contract's rings and buckets bound what a pass takes, not how often one takes nothing."
- The PR body draft (`author-r13/PR-BODY.md:60` and `:250`).
- HANDOFF section 7.
- The REVIEW READY: "1. **Met.**", with "A save's progress is not bounded" listed under open risks.

**Authority:**
- Round 13 assignment, item 1, second bullet: "A save's own progress stays bounded and stated, at 8x8, from the change to durable."
- Exit: "STOP with the residual if a store phase cannot fit the share without an amendment."
- The owner's #823 bound, which "applies to the firmware writer (#665 F1)".
- AGENTS.md section 2: a conflict with a requirement is published as a decision, not chosen privately.

**Evidence:**
- **Before the delta,** the store's step ran as a centisecond consumer on every TICK (`ctrl_plat.c` at `c954b8a9`). So a save advanced one step per tick, whatever the input.
- **At the head,** a step runs only in a pass with `work == 0`. A TICK is itself an event, so the pass that takes it never steps. Any stream of records that keeps a record pending at every pass start defers the step indefinitely. The ticks meanwhile "owe it once", so the time lost is never recovered.
- **What the author measured:** one wait of at most 16.95 ms per window (`R-W8/step-waits.txt`), and the lone save with no other load: 4,697.4 ms at 8x8 and 2,018.4 ms at 1x1 (`R-A8`, `R-A1` `save-alone.txt`). Neither is a bound under input, and the documents say so.
- **My reviewer plant confirms the rule is enforced as written.** Removing `&& work == 0u` fails `Loop.L12StepOnlyInAPassThatTakesNoInput` (`receipts/plant_step_beside_input.log`). So the starvation is the designed behaviour, not a slip.
- **The documents' stated reason is not established.** The contract's token buckets bound the admitted record rate, not only what a pass takes:
  - one bucket per channel, shared by both interfaces (`KL_mbx_rx.sv:600-609`);
  - at most 100 + 200 + 200 + 50 + 500 = 1,050 records a second, after bursts of 8 + 16 + 16 + 8 + 32 = 80 (`mailbox.yaml` rates);
  - together with the measured per-record costs (a full composed load drains in about 17 ms at 8x8), that is the input a worst-case busy period can be derived from;
  - so whether a pass that takes nothing must recur, and how soon, is a computable question this round did not answer.
- **Against #823's 0.5 s.** The whole-image design already takes about 4.7 s at 8x8 with no flash busy time (and #823 places the 0.5 s on the append-only design), so not claiming 0.5 s for this image is correct, as R711-2 judged. But THE STEP is the scheduling the firmware writer will carry into #823's design. A step whose wait has no bound makes any worst-case save bound for the firmware writer, 0.5 s included, unstatable. This is therefore not only "left": it conflicts with an owner bound that is stated to apply to F1.

**Impact:**
- A frozen acceptance criterion is marked Met while the author's own text says it is not.
- Under sustained admitted input, a persisted change (a bind, a SET_NAME) may never become durable, and no figure in the tree says how long it may take.
- The owner's decision that a save is bounded in the worst case cannot be met by the firmware writer as scheduled. HANDOFF section 7 records "no owner decision is asked here".

**Required outcome:** one of the following.
1. **Derive and state a worst-case bound** on a step's wait, and so on a save from the change to durable at 8x8. Derive it from the contract's admitted input: the buckets' rates and bursts, the event sources, the ticks, and the measured per-record and per-pass costs. Stage the input that realises it in the harness during a save. Correct `SPLIT_CONTROL_MEMORY.md:1435`'s reason.
2. **Or bound the wait by mechanism**, keeping every row and every pass within its bound. For example, a step owed for more than N ticks is taken in the next pass with `NVM_STEP_US` of room even if that pass took input, with N chosen so the rows still fit. Then state the bound.
3. **Or STOP**, as the exit requires, and obtain a public owner decision that accepts an unbounded save under sustained input for this image. That decision must name what replaces item 1's bound and how #823's firmware writer will meet 0.5 s. Item 1 then stays "not met" until it is decided.

In every case, the REVIEW READY's item 1 and the PR body must not say "Met" while the bound is absent.

**Verification:**
- A harness group at 8x8/2if, in both arms, that holds input at the contract's admitted rates (or at the derived worst case) across a whole save. It reports the save's time from change to durable within the stated bound, 0 passes over the share, and its rows.
- A plant that defers the step without limit (for example, the age limit removed under option 2) fails a named check.
- For option 3: the owner's comment, linked from `SPLIT_CONTROL_MEMORY.md` "What is left" and from the PR body.

### R712-3-F2 - MINOR - Docs - "a pass that carries a step is at most 1.02 ms at 8x8" is contradicted by the author's own lone-save receipt

**Where:**
- `docs/design/SPLIT_CONTROL_MEMORY.md:1349`: "A pass that carries a step is at most 1.22 ms at 1x1 and 1.02 ms at 8x8".
- The PR body draft's item 1 row (`author-r13/PR-BODY.md:38`).
- HANDOFF section 5, "The share".

**Evidence:**
- `receipts/measure/R-A8/save-alone.txt`, 8x8/2if, at the image the head builds:
  - a pass carrying a page-program issue reaches 126,436 CPU cycles (1.26 ms);
  - a pass carrying a read-back step reaches 120,731 cycles (blank check) and 121,756 cycles (verify).
- The 1.02 ms figure is `R-W8/step-waits.txt`'s maximum, 101,796 cycles. That maximum is taken only over steps "that waited inside the window".
- The 1x1 figure, 1.22 ms, is a whole-save figure (R-A1: 120,515 cycles).
- So the sentence puts figures on two different bases side by side, and the 8x8 one understates the measured maximum by 0.24 ms.
- The share verdict is unaffected: 1.26 ms is within 2.0 ms, and the room rule bounds such a pass at about 1.0 ms plus the step's cost.

**Impact:** a published measurement that a reader would use to judge the step's headroom is wrong at 8x8.

**Required outcome:** the sentence, the PR body and the HANDOFF either give each point's maximum over every pass that carries a step (at least 1.26 ms at 8x8 per R-A8), or scope each figure to what it measures, on the same basis at both points.

**Verification:** each figure traces to a named receipt line on the stated basis.

### RESIDUE-1 (wording only; no verdict effect) - `docs/design/SPLIT_CONTROL_MEMORY.md:1451` - S's slope is arm A's, not the printed column's

- S at this head uses arm A's 1x1/1if figure (section 13's table) as the slope's 1x1 end. That is the arm the 8x8/1if point ran in, so R712-2's SUGGESTION-1 is adopted in substance.
- But the 1x1/1if column section 14 prints is the worst of the arms.
- So a reader who recomputes S from the printed table gets, for the last AECP record, 26.4 ms instead of the printed 28.1 ms (`receipts/estimate-check.txt`, where every S cell recomputes from arm A to within rounding).
- Exact fix: append to `:1451`: "The slope is arm A's at both ends, from section 13's arm A 1x1/1if figure, since the 8x8/1if point ran in arm A only; the 1x1/1if column below is the worst of the arms."

### RESIDUE-2 (wording only; no verdict effect) - `sw/firmware/ctrl_nvm/nvm_store.h:64-66` - the read-back's cost in the comment R712-2-F1 asked to correct

- The comment says "half a page takes 0.70 ms". The `NVM_STEP_US` comment four lines below gives a read-back step as 0.77 ms.
- The measured 8x8 steps are 0.73 ms (blank check) and 0.77 ms (verify) (`SPLIT_CONTROL_MEMORY.md:1329-1331`).
- Exact fix: "... so half a page takes about 0.70 ms to read, and a read-back step 0.73 to 0.77 ms at 8x8/2if with the store's own work (NVM_STEP_US below), of the 2.0 ms a pass may take (#665, the share in ctrl_loop.h)."

### SUGGESTION-1 - nothing checks that the measured step cost stays within `NVM_STEP_US`

- `nvm_store.h:68-74` makes "no pass that carries one exceeds the share" depend on the step's cost staying within the 1.0 ms constant. The longest step today is 0.954 ms, which leaves 0.046 ms.
- `NvmBoth.step_room` holds the rule, not the figure. The harness's share check would not see a 1.1 ms step, because the empty pass before it is about 0.16 ms.
- Suggest a harness check that the largest per-step cost of each step kind (flash port and store, as `R-A8` prints) is at most `NVM_STEP_US`, with a plant. That way a slower flash port fails by name.

### SUGGESTION-2 - `docs/design/SPLIT_CONTROL_MEMORY.md:1536` - carry the unrounded unit count

- "At the top of its range, 1.1 ms, puts it 0.39 ms over" uses the rounded 1.1.
- From the table's units it is 62 × 0.018 × 1.0 ms = 1.116 ms, so 0.41 ms over (`receipts/estimate-check.txt`).
- The conclusion is unchanged.

### SUGGESTION-3 (outside this PR; for a new Issue) - the boot simulation's export comparison is not deterministic

- `tb/verilator/ctrl_split_boot/run.py:233` refuses a build whose second export's `csr.csv` differs from the provisional one.
- The VexiiRiscv ISA string's extension order varies between processes: `zicsr_zifencei` against `zifencei_zicsr`, from `get_arch` iterating `isa_map`.
- So my first `--self-test` at the head stopped with `REFUSED` at its second plant, after `flash-window-cached` was caught (`receipts/boot_1x1.log`, rc 2).
- The same self-test with a fixed hash seed passed 3 of 3 (`receipts/boot_selftest_seed0.log`).
- The check comes from `6380c8cd78`, which is in the base, so this is not this PR's defect. It fails closed, so it produced no false evidence.
- Suggest an Issue: compare the CSV with that constant normalised, or pin the seed in the export's child process.

### Retained from round 12

- **R711-2-S3** (the platform image's hot list names fixture callbacks only). Still disclosed at `SPLIT_CONTROL_MEMORY.md:1436`. It stays a suggestion.

## Round 12 findings at this head (read after my own pass)

| Finding | State | Evidence at `4f58214f` |
|---|---|---|
| R711-2-F1 MAJOR / R712-2-F1 MINOR: the store step in a composed window | **Resolved at its cause** for the share | THE STEP (`ctrl_loop.c:157-172`, `nvm_store.c:798-808`); THE SHARE names it (`ctrl_loop.h:80-81`). At `c954b8a9` x-save and y-save reproduce exactly: 238,763 and 271,599 cycles, 2.388 and 2.716 ms (`P0-A8/table.md`). At the head's image (`2c677934`, which my 8x8 build reproduces byte for byte) they take 1.628 and 1.978 ms (`X-A8/table.md`). The 24 save windows at both points, both arms, with and without drafts: 0 of 99,289 passes over. My own exact-head 8x8 run of `blank-7`, `program-3`, `verify-1`, `backlog-adp` and `save`: 0 of 3,199 passes over and no idle run over; `backlog-adp` longest 1.963 ms; SRP last 16.23 to 16.85 ms in the save windows and 16.556 ms in `backlog-adp` (doc: 16.56) (`receipts/h8-table.md`). The planted store step is caught at CTL-A8: 5 windows over the share with every row in bound. The **new** progress defect introduced by the fix is F1 above. |
| R711-2-F2: joint link change | **Resolved** | `srp_mbx.c:837-878`: one build a pass, with turn order. `y-links` 1.761 / 1.817 ms and `x-links-same` 1.543 / 1.560 ms (`X-A8`, `X-B8` tables). My plant removing the deferral fails `Srp.JointLinkChangeBuildsOneInterfaceAPass` ("a pass builds one interface at most", "receive waits until both are built", "the interface whose turn it is is built first") (`receipts/plant_both_builds.log`). |
| R711-2-F3: boot flash window | **Resolved** | `boot_soc.py:93,112-115`. My run: 25.515 ms to ready at 1x1, as the README says. Self-test 3 of 3 plants caught, `flash-window-cached` included (`receipts/boot_1x1.log`, `boot_selftest_seed0.log`; see SUGGESTION-3). |
| R711-2-F4: three stale lines | **Resolved** | `srp/README.md:221` (2.0 ms), `aecp/README.md:310` (20 ms bound), `ctrl_nvm/README.md:128-133` (one step per centisecond dispatched, THE STEP). |
| R712-2-F2: gPTP per-row and per-pass | **Resolved** | Section 14's units table: row mean 1.116 units, 0.446 ms; row bound 20 units, 8.0 ms; pass bound 4 units, 1.6 ms. Each is labelled mean or bound, with the margins 17.736 and 25.29 ms against 18 (`receipts/estimate-check.txt`). Rounding is SUGGESTION-2. |
| R711-2-R1: save time in absolute terms | **Resolved** | `SPLIT_CONTROL_MEMORY.md:1304-1305`, PR body. |
| R711-2-R2: boot README caches | **Resolved** | `ctrl_split_boot/README.md:42`. |
| R712-2 RESIDUE-1: harness README arm B line | **Resolved** | The `answering-ports` line now carries the exact fix. Lines `:344` and `:576` describe earlier runs and are left as history. |
| R712-2 SUGGESTION-1: S crosses arms | **Adopted in substance** | The wording residue is RESIDUE-1. |
| R712-2 SUGGESTION-2: absolute read-back time | **Adopted** | `ctrl_nvm/README.md:257-262`. |
| R711-2-S1: `listener_present` | **Resolved** | `srp_mbx.c:790-791`; `Srp.InterfaceResetClearsListenerPresent` and its plant (author receipts, `fwshard-3.log`). |
| R711-2-S2 | **Resolved** | With R712-2-F2. |
| R711-2-S3 | **Retained** | As a suggestion. |

## The author's open risks (HANDOFF section 7)

- **Margin 0.71 ms, least row.**
  - Correct: 17.29 ms against 18, the 8x8 last SRP record, arm B, in a save window (`SPLIT_CONTROL_MEMORY.md:1363`).
  - My arm A windows give at most 16.85 ms, within the doc's arm A 16.99 ms.
  - It fits, and is correctly recorded. gPTP's assumed bound would not fit, and section 14 says so.
- **Heaviest 8x8 pass, 1.98 of 2.0 ms.**
  - Correct: 1.98 ms is arm B (N-B8); my arm A `backlog-adp` is 1.963 ms (doc 1.96).
  - It fits, is correctly recorded, and carries no step.
- **A save's progress not bounded under input that never leaves a pass empty.**
  - This **does not merely record a left item.** It fails round 13 item 1's frozen "bounded and stated" criterion.
  - It makes the owner's worst-case save bound (0.5 s, which #823 states applies to the firmware writer) unstatable for the firmware writer's scheduling.
  - Its stated reason overlooks that the buckets bound the input rate.
  - This is F1.
- **The step's 0.046 ms room.**
  - Correct (95,386 cycles of 100,000).
  - It is recorded, and the rule is held by `NvmBoth.step_room`. My plant that reduces the room test to the deadline itself fails `step_room` on both ports (`receipts/plant_room_is_deadline.log`).
  - The figure is held by nothing: SUGGESTION-1.
- **The sweep.**
  - The first attempt stopped in every shard's preflight: `test_suite_cancellation.py` SIGINT, "CLEANUP FAILED: owned descendants remain" (the #833 class).
  - The same script passed alone (`sweep-first-attempt/rerun-alone-shard0.log`).
  - The second attempt: shards of 15, 17, 17 and 16 suites, 65 of 65, with checks 360,921 + 1,946,931 + 284,228 + 21,575 = 2,613,655 and 0 failures. Each `results.json` names head `4f58214f` and base `a68536fa`.
  - Accepted as the known preflight class; no gptp_shadow failure.

## Comment rule

- I scanned the added source lines of the delta (`sw`, `tb`, `hdl`, excluding Markdown) for lane labels, round or reviewer IDs, issue-comment IDs and review wording. There are no new instances.
- `B10`, `L10` to `L12` are the suites' existing test-step labels, not bench lane labels.

## Packet and evidence integrity

- `receipts/packet-verify.txt`: all 509 files of `author-r13/` match `MANIFEST.json`'s `published_sha256`. Nothing is unlisted and nothing is missing.
- Five INDEX hashes differ. Each is a `path_redacted` entry whose `original_sha256` equals the INDEX hash.
- 17 `results.json.gz` receipts are hash-only in INDEX (not archived by size), so I did not recompute rows from raw results. I spot-checked their `table.md` and `run.log` lines and reproduced a subset at the exact head instead.
- Legs ran at `83709d3f` to `b49a001d`. The image identity gate (`gates/image-identity.log`, 5 of 5) and my own 8x8 build (ELF sha256 `2c677934...`, equal to N-A8's) tie them to the head's images.
- `D-A8`'s `run.log` shows 8 refusals before its regrade with `5688b627`'s phase guard. The regrade gives 0. The guard's final rule (`grade.py:805-825`: pages alone) is a sound reading of the phases, not a loosening: blank is after the erase with no page; program is within 30 ms of a page; verify is 30 ms or more after the last page, with none later. My exact-head run, graded by it, refused nothing.

## Lens results

| Lens | Result | Artifact examined at `4f58214f` | What was checked, against what |
|---|---|---|---|
| Conformance | UNCLEAN (F1) | assignment items 1-5 and exit; `ctrl_loop.c:157-178`, `nvm_store.c:789-815`, `srp_mbx.c:837-878`, `boot_soc.py:93-115`, `SPLIT_CONTROL_MEMORY.md:1313-1437,1514-1541` | Items 2, 3, 4 and 5 are met. In item 1, the share, the phases and the plant are met; "progress bounded" is not (F1). |
| RTL (architecture) | UNCLEAN (F1) | the loop's pass order and THE STEP (`ctrl_loop.c`, `ctrl_loop.h:62-97,131-156,188-210`), `nvm_store_step`/`_tick`/`_clock` and `ls_now_us` (`nvm_flash_litespi.c:266-286`), the busy-poll timeout order (`nvm_store.c:640-650`), SRP's `builds_first`/`build_turn`, `KL_mbx_rx.sv:597-619` buckets | The wrap-safe deadline is correct. The step is admitted only with ≥1.0 ms left. A late poll cannot false-timeout, because busy is checked first. The one-build turn order is correct with one or two interfaces. The stall is unbounded (F1). |
| Robustness | UNCLEAN (F1) | the same, under sustained admitted input; reset during a link change (`reset_interface` clears `listener_present`); a deferred step across ticks (owed once) | The step is starved by input that keeps passes non-empty (F1). The joint link change and its build failure are bounded (one pass of delay). |
| Tests | CLEAN | `test_port_loop.cpp` L10-L12, `test_nvm_write.cpp` `step_room`, `srp_app.cpp` `JointLinkChangeBuildsOneInterfaceAPass` and `InterfaceResetClearsListenerPresent`, `grade.py:802-838`, `save_window.py`, `run.py:342-354`, `build.py:45-77`, `ctrl_split_boot/run.py` SoC plant; my receipts `fw_gate.log` (PASS), `nvm_gate.log` (445 tests), `harness_selftest.log` (0 failures), the three `plant_*.log` (each caught by its named check), `h8_save.log`, `boot_selftest_seed0.log` (3 of 3) | Each new test failed for the defect it claims: three reviewer plants of my own, beyond the author's 612/612 and 116. The share control is graded per window. Save windows are refused outside their phase. The planted store step is caught at CTL-A8. F1's missing staging is part of F1's required outcome, not a defect in a test that exists. |
| Docs | UNCLEAN (F1, F2) | `SPLIT_CONTROL_MEMORY.md:1304-1305,1313-1437,1439-1541`, `MAILBOX_SPLIT.md` pass order, `ctrl/README.md`, `srp/README.md`, `aecp/README.md`, `plat/README.md`, `ctrl_nvm/README.md:120-262`, `ctrl_split_boot/README.md`, `ctrl_service_budget/README.md`, the PR body draft, the REVIEW READY | The stale lines are fixed and the estimate recomputes (U and L exact; S per RESIDUE-1). There is a "Met" claim against F1, and a misstated 8x8 step-pass figure (F2). Residue: RESIDUE-1, RESIDUE-2. |

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | as in Lens results; F1 open | R712-3 | `4f58214f457e963243a1fe6b86c6af161e97f26f` |
| RTL | UNCLEAN | as in Lens results; F1 open | R712-3 | `4f58214f457e963243a1fe6b86c6af161e97f26f` |
| Robustness | UNCLEAN | as in Lens results; F1 open | R712-3 | `4f58214f457e963243a1fe6b86c6af161e97f26f` |
| Tests | CLEAN | as in Lens results; receipts listed in MANIFEST.sha256 | R712-3 | `4f58214f457e963243a1fe6b86c6af161e97f26f` |
| Docs | UNCLEAN | as in Lens results; F1, F2 open | R712-3 | `4f58214f457e963243a1fe6b86c6af161e97f26f` |

A fix to F1 will touch the loop or the store and the harness, so it un-covers Tests at the new head under AGENTS.md section 7.

## Execution evidence (this round, at the exact head, pinned Verilator 5.050 verified by `--version`)

| Run | Result | Receipt |
|---|---|---|
| Firmware gate, `test_ctrl_firmware.py --require-rv32` | rc 0, `test_ctrl_firmware: PASS` | `receipts/fw_gate.log` |
| Store gate, `test_ctrl_nvm.py --require-rv32` | rc 0, 5 shapes, 445 tests | `receipts/nvm_gate.log` |
| Harness self-test | rc 0, `self-test: 0 failures` | `receipts/harness_selftest.log` |
| Harness 8x8/2if arm A, 5 groups | rc 0; 0 refusals, 0 of 3,199 passes over; image `2c677934...` = N-A8 | `receipts/h8_save.log`, `h8-table.md`, `h8-image.sha256` |
| Boot 1x1 run, then self-test | run PASS 25.515 ms; self-test REFUSED at the second plant by SUGGESTION-3's nondeterminism (rc 2) | `receipts/boot_1x1.log` |
| Boot self-test, fixed hash seed | rc 0; 6 of 6 native controls; 3 of 3 plants caught | `receipts/boot_selftest_seed0.log` |
| Plant `step-beside-input` (`ctrl_loop.c`) | caught: L12 "a pass that takes a record does not take the step", "nor one that takes an event" | `receipts/plant_step_beside_input.log` |
| Plant `both-builds` (`srp_mbx.c`) | caught: `JointLinkChangeBuildsOneInterfaceAPass`, three checks | `receipts/plant_both_builds.log` |
| Plant `room-is-deadline` (`nvm_store.c`) | caught: `NvmBoth.step_room` on the model and LiteSPI ports | `receipts/plant_room_is_deadline.log` |
| Packet verification | 509/509 manifest matches; 17 hash-only receipts | `receipts/packet-verify.txt` |
| Section 14 recomputation | U and L exact; S from arm A; gPTP figures | `receipts/estimate-check.txt` |
| Hosted check runs at the head (read only) | at 22:27 CET: 4 success, 1 skipped, 12 in progress, 27 queued | `receipts/hosted-check-runs.tsv` |
| Checkout integrity after probes | HEAD, tree and index `3313634d...`; no tracked, untracked or ignored change after removing this run's `__pycache__`; six gitlinks as at the head | `receipts/checkout-integrity.txt` |

The plants ran in disposable copies under the packet's `scratch/` directory, which is not published. The clone itself was never edited. The scripts and the exact commands are in `scripts/` (`scripts/README.md`).

## Real limits

- **Not run:** the firmware self-test's full mutant table, the full sweep, docs.yml, the builder bank, behave, coverage, and the 24 windows at both points and both arms. For these I relied on the author's verified receipts, and spot-checked against my exact-head 8x8 subset.
- The 17 `results.json.gz` are hash-only, so no row was recomputed from raw results.
- **No sustained-input starvation was staged.** F1 rests on the frozen criterion, the code's rule (confirmed by plant), the author's own statement, and the contract's arithmetic, not on a measured stall.
- The harness's flash model has no busy time: a real part's erase and program waits add to every save figure.
- Physical calibration NOT RUN. No hardware or bench step was run, and field skips are not hardware proof.
- No manager source bank exists at this head, and none is claimed or inferred.

## Pending manager duties

- Publish this packet; carry RESIDUE-1 and RESIDUE-2 to the residue checklist.
- Hosted exact-head contexts (most queued or in progress when read) and act acceptance.
- The current-dev merge candidate at the merge turn: source base `a68536fa`, live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`, with the builder and native banks, and their receipts linked on the PR.
- Route F1's option 3, if chosen, to the owner. Consider SUGGESTION-3 as a new Issue on the base's boot simulation.

R712-3 FINISHED

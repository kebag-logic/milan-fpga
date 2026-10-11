[R602] NEGATIVE - exact head fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08

# R602-3: internal cleared-context review of PR #715 (issue #671), round 3

- **Head:** `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08`, tree `5df4098eebf77625bd26899bb84cd72ca35e96e4`.
- **Source base:** `e8454e2751d05b02ee8e5a571857589ab358ab86`. Live dev at review start: `ac2c5e77bba1c0ae20ce2f69f711a1d17ead94a5`. That is the manager's merge-turn candidate, which this review does not cover.
- **Diff:** 16 commits, 14 files, +1,591 / -379. No `hdl/`, register-map, generator, record-layout or gitlink change.
- **Role:** internal independent reviewer `[R602]`, round R602-3, in its own detached clone.
- **Lenses:** all five were applied independently at this head: Conformance, RTL, Robustness, Tests and Docs.
- **Order:** I wrote my verdict and ledger to `receipts/VERDICT_FIXED_BEFORE_PRIOR_READ.txt` before reading any prior-round review text. I then resolved the prior findings against this head (section "Prior public findings"). I read no report by the other reviewer for this round.

## Verdict

**NEGATIVE, on two MINOR findings:**

- **F1** (Tests, Robustness, Docs): check 13 cannot fail if the re-stage retry loses its bound.
- **F2** (Docs): the PR body gives the round-2 harness's base-reproduction figure as this head's.

The firmware is correct on every path I read and drove, including the re-stage bound. It applies the #671 rule on both boot paths, the cold boot and the writer restart without a fabric reset:
- one staged read per judgement;
- OK stands on one read;
- any other verdict, blank included, stands only on two byte-identical reads within three;
- the pick is re-staged under its own sequence, and an unread pick offers the other slot;
- no sequence is taken from refused bytes;
- an UNREAD slot holds the writer.

Acceptance 1 to 3 are met, and every round-1 and round-2 finding is resolved at this head. Both new findings concern test strength and evidence text. Neither is in the shipped firmware.

## Reconstruction

I read these in order:
1. AGENTS.md and CONTRIBUTING.md (sections 2, 3 and 6).
2. docs/README.md.
3. The #671 body: Required, and Acceptance 1 to 3.
4. On #671:
   - assignment 6098494890, with its scope (A/B guarantee, record format, register map and boot budget unchanged) and STOP condition;
   - TAKEN 6098611315;
   - the round-2 assignment 6100704879, whose item 1 says "the read-fault check must be able to fail for every mechanism the fix depends on";
   - the round-3 assignment 6103025987 ("The PR body's 'every mechanism' sentence is then true. Keep it true.");
   - the three REVIEW READY comments.
5. FASTCONNECT 6.2 and 7, `sw/firmware/ctrl_nvm/README.md` Boot items 2 to 4 and 9 (the Mark II rule the assignment applies), and MATERIALIZATION 6.3.
6. `hdl/milan/KL_nvm_backend.sv` (CSR words 2 and 3, liveness and loss) and the SoC stage layout (`sw/litex/milan_soc.py:3032`, `:4093-4097`).
7. The full diff `e8454e27..fc0c517c` and its history.
8. The PR body and the hosted check list at this head.

I read no private author material, lane scratchpad or management directory.

## Findings

### F1 - MINOR - Tests, Robustness, Docs - check 13 cannot fail if the re-stage retry loses its bound

**Where.**
- The firmware is correct. `sw/firmware/milan_baremetal/milan_baremetal.c:813-825` is `nvm_restage()`, the picked slot's retry, bounded by `NVM_READ_TRIES`.
- No case reaches the bound. Check 13's fault windows are at `sw/firmware/nvm_hosttest/read_fault_cases.py:114`, `:120` and `:126` (`FAULT_WINDOWS`, `RESTAGE_WINDOWS`, `RESTART_RESTAGE`). Each fault either lasts at most 3 reads, or is the whole-boot window `(0, 64)`. That window starts at read 0, so it also fails the faulted slot's judgement, and an unjudged slot is never re-staged. So no case faults the picked slot after its judgement read for longer than the bound.
- The exact read count is pinned only for one window. `read_fault_cases.py:256-269` (`read_findings`) checks the total bound for every case, but the exact count only for `(0, 64)`.
- The documented bound includes the re-stage count. `docs/integration/BAREMETAL_FIRMWARE.md:2054-2055` gives it as "three judgements and three re-stages per slot".
- Three PR body claims are therefore not true of the re-stage:
  - "Round 2": "Check 13 can now fail for every mechanism the fix depends on";
  - "Round 3": "The round-2 sentence above is now true";
  - "Round 3": "The per-slot read bound is pinned".

**Authority.**
- #671 Required: "The writer retries the read within a bound."
- Assignment 6098494890: "So do a planted unbounded retry". The shipped `unbounded_retry` (`read_fault_cases.py:27-32`) unbounds only the judgement loop.
- Round-2 assignment item 1 and the round-3 assignment, quoted above.
- AGENTS.md section 6. Tests: "Each new test can fail for the defect it claims to detect". Robustness: "backpressure and timeout paths".

**Evidence.** Each plant was applied to the firmware text in memory only, and graded by the head's own checks 13 and 14 in full.

- **Plant `p_restage_unbounded`** changes the `nvm_restage()` loop condition from `n < NVM_READ_TRIES` to `n != 0xffffffffu`.
  - It gives **0 findings** on `endstation_arty_4x4` (`receipts/probes/p_restage_unbounded.endstation_arty_4x4.txt` is empty; `receipts/probes_g3.log`, rc 0).
- **Plant `p_restage_once`** allows one re-stage. It is caught by 28 "one faulty read held" findings. So the bound is pinned from below only.
- **Demonstrator** `scripts/probe_restage_bound.py` (`receipts/restage_bound_arty.log`, `receipts/restage_bound_8x8.log`, rc 0):
  - **Check 13's own cases:** none of the 472 faults more than 3 consecutive reads without also faulting the judgement.
  - **Four extra cases,** graded with the head's own `grade_fault_case()`. Each fault starts just after the picked slot's judgement read and lasts 64 reads:
    - both slots valid, A newer;
    - both slots valid, B newer;
    - A valid, B blank;
    - both slots valid, on a writer restart.
  - **Head:** 0 findings on every case. The writer holds after exactly 7 boot reads, or 6 restart reads, with `read faults=3 unread=1` (`receipts/restage_exact_count.log`).
  - **Unbounded plant:** caught on every case, on arty and 8x8, in the head's own words: "the boot read the flash 68 times, over the bound of 13" and "the writer restart read the flash 67 times, over the bound of 12". The checker can see this defect, but no case drives the firmware there.
  - **Four-try re-stage plant:** 0 findings, even on the extra cases. The per-slot re-stage count is not pinned at all.

**Impact.**
- A regression that removes or raises the re-stage bound would pass every gate. The documentation would still say "three re-stages per slot".
- Such a writer reads without end under a fault that persists after one clean judgement read. Examples are a slot that degrades after its first read, or an address fault on the re-stage. The boot then never reaches the restore walk, and the entity is never enabled.
- No committed change is lost, which is why this is MINOR and not MAJOR.

**Required outcome.**
- Check 13 includes cases whose fault starts after the picked slot's judgement read and lasts past the bound. They cover the cold boot and the writer restart, in both orientations.
- Each such case asserts its exact read count:
  - 7 on a cold boot: the AEM image, one judgement read of each slot, three re-stages of the pick and one of the other;
  - 6 on a restart.
- A named `--self-test` control that unbounds or raises the re-stage loop reddens by its own words on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`.
- The PR body's "every mechanism" and "per-slot read bound is pinned" sentences are then true.

**Verification.**
- At the new head, `python3 <packet>/scripts/probe_plants.py <tree> <out> 8 p_restage_unbounded` reports a non-zero finding count containing "over the bound" or "want exactly".
- The four-try variant in `scripts/probe_restage_bound.py` is caught through check 13's own cases.
- `--self-test` reports the new control "caught by N named finding(s)" on three shapes.

### F2 - MINOR - Docs - the PR body's base-reproduction figure is the round-2 harness's, stated as this head's

**Where.** The PR #715 body, "Description", second paragraph: "The host model reproduces this on the base firmware, graded by this head's checks: 645 findings per product shape, 124 of them 'was lost on the clean reboot'."

**Evidence.**
- This head's checks cannot grade the base firmware as shipped:
  - `test_nvm_firmware.py` appends `writer_restart.host_restart()` to every host build;
  - `host_restart()` refuses any firmware whose statics differ from `WRITER_STATICS` (`writer_restart.py:34-37`);
  - the base firmware lacks `nvm_unread`, `nvm_held` and `nvm_read_faults`.
- My probe narrowed the restart model to the base's statics (`scripts/probe_plants.py`, label `base`). The base firmware's sha256 is `a73ecc25…`, equal to the previous capture receipt's digest.
- With that model, this head's checks 13 and 14 give **743 findings per product shape, 135 of them "was lost on the clean reboot"** (`receipts/probes/base.endstation_ax7101_1x1_tdm8.txt`, `base.endstation_ax7101_8x8.txt` and `receipts/probes_base_*.log`, rc 0).
- The 645 / 124 figure matches the round-2 REVIEW READY (#671 comment 6102799749), which predates the 26 restart cases.
- The reproduction itself is real. Only the figure and its attribution are stale.

**Why not RESIDUE.** The fix changes a stated figure, and the owner's rule excludes any figure change from RESIDUE.

**Impact.** A cold reviewer who follows "graded by this head's checks" gets a harness refusal, not 645. The acceptance-1 reproduction evidence cannot be reconstructed from the PR as written.

**Required outcome.** The PR body gives the reproduction count as this head grades it, and says how the restart model was matched to the base writer's statics. Alternatively, it attributes 645 / 124 explicitly to the round-2 head `9112a0df`.

**Verification.**
- Re-read the PR body.
- To check the count, place the base firmware at `<out>/base_fw.c` (`git show e8454e27:sw/firmware/milan_baremetal/milan_baremetal.c`), then run `scripts/probe_plants.py <tree> <out> 8 base endstation_ax7101_8x8`.

### S1 - SUGGESTION (optional) - Robustness - a held re-attach publishes a sequence derived without the unread slot

- At `milan_baremetal.c:1696-1701`, a held re-attach still calls `nvm_publish(verdict)`.
- Take both slots valid with the newer one unread. The published word 2 then drops to the older slot's sequence, while the window keeps the previous run's state.
- Nothing is mis-persisted:
  - the backend treats word 2 and the verdict as "evidence only" (`KL_nvm_backend.sv:491-494`);
  - `nvm_backed` 0 and the console carry the hold.
- Plant `p_reattach_held_no_publish` gives 0 findings (`receipts/probes/p_reattach_held_no_publish.*.txt`). That matches the documented "publishes and HOLDS", which was pre-#671 behaviour on that path.
- Suggestion: say in the restart bullet what a held re-attach publishes, or leave the previous run's word 2 in place while held. This counts against no lens.

## Prior public findings, resolved or retained at this head

I read these only after my independent pass and after recording the provisional verdict.

| Prior finding | Status at fc0c517c | Evidence at this head |
|---|---|---|
| R603-1-F1 MAJOR / R602-1-S2 (Tests): record-area faults, both-valid layouts, three plants | Resolved | `fault_cases` has the `body` fault and both-valid layouts across the wrap (`read_fault_cases.py:187-219`). `reboot_findings` requires every other saved record to survive (`test_nvm_firmware.py:682-715`). `r_digest_header_only`, `r_fill_from_flash`, `r_restage_fail_offers_none` and `restage_fail_not_unread` are each caught on three shapes (`receipts/host_selftest_head.log`). |
| R603-1-F2 / R602-1-F1 (Docs, RTL / Docs, Robustness): fault worst-case boot understated | Resolved | The PR body's "Boot time" counts 10 slot-length reads and 2 container reads: about 16.4 s (1x1) and 17.1 s (8x8), labelled an estimate. The restart liveness note is under limitations. The read count matches `nvm_judge_slot` / `nvm_restage` (`:781-825`). The per-byte cost is the author's measurement; I did not re-measure it. |
| R603-1-R1 / R602-1-R2: check numbering | Resolved | The README says "fourteen checks" and numbers items 12 to 14. |
| R603-1-S1 / R602-1-S3: wipe while held | Resolved | Stated at `milan_baremetal.c:1576-1578` and in `BAREMETAL_FIRMWARE.md` Boot. Checked by `grade_hold_console` (`test_nvm_firmware.py:827-831`). |
| R603-1-S2: the console names the real retire cause | Resolved | `nvm_held` is set only in `nvm_go_live()` (`:1588`). All four causes are checked (`RETIRE_CAUSES`, `test_nvm_firmware.py:832-837`). My `p_console_unnamed` plant is caught. |
| R603-1-S3: re-stage sequence check | Resolved | `--read-other` and `r_restage_any_seq`, caught on three shapes. |
| R602-1-R1: FASTCONNECT 7 loss mode per store | Resolved | The exact text is in `SAVED_STATE_FASTCONNECT.md` section 7. |
| R602-1-R3, then R602-2-R1: SNAPSHOT_OWNERSHIP 18 wording | Resolved | Section 18 reads "its console report of the writer's hold only; `nvm_capture()`, the backend's capture hold and the census are unchanged." |
| R602-1-R4: all-0xFF sentence | Resolved | README check 13: "A single all-`0xFF` read of the valid slot is walked over SKIP 0 to 5." |
| R602-1-S1: read-fault counter | Resolved | Documented as a floor (`milan_baremetal.c:478-482`). |
| R603-2-F1 MAJOR / R602-2-F1 MINOR (Conformance, Tests, Robustness): the re-attach hold is reached by no gate | Resolved | There are 26 restart cases (`read_fault_cases.py:168-184`, `test_nvm_firmware.py:718-731`). Control `r_reattach_goes_live` is the same one-line revert as R602-2's `p1_reattach_no_hold`. In my run it is caught on three shapes, by 8, 8 and 5 named findings. My `p_hold_both_only` and `p_cold_goes_live` plants are caught too. |
| R603-2-R1: the writer-restart bullet names the hold | Resolved | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:725-729` carries the exact text. |
| R603-2-S1: pin the per-slot judgement bound | Resolved for the judgement | `r_judge_four_tries` is caught on three shapes. The re-stage half was not part of that finding; it is F1 here. |
| R603-2-S2: "re-attached and HELD" | Resolved | `milan_baremetal.c:1700-1701`, and graded (`read_fault_cases.py:300-301`). |
| R602-2-S1: the firmware page states the every-boot hold | Resolved | `BAREMETAL_FIRMWARE.md:2047-2054`. |
| R602-2-S2 / R603-2-OBS-1: the runtime prefill reads flash freshly | Retained, out of scope | Unchanged (`milan_baremetal.c:1245-1255`). The round-3 assignment placed it outside #671, and the PR body names #717. Not a finding against this head. |

**No prior finding stays open.** F1, F2 and S1 are new at this head.

## Answers from evidence

**Sequence derivation is local to the firmware.**
- The diff touches no HDL.
- The sequence enters only through `nvm_read_slot()` on VD_OK (`milan_baremetal.c:757-758`). It flows through `nvm_judge_slot`, `nvm_restage`, `nvm_pick_slot` and `nvm_boot` (`:1648-1675`), and `nvm_commit` uses `nvm_seq + 1` (`:1383`).
- `KL_nvm_backend.sv` stores word 2 and reads it back (`:424`, `:439`, `:490`, `:582`).
- My probe `p_seq_from_flash` re-reads the sequence from flash after the judgement, as the base did. It is caught on arty and 8x8 with 42 findings, 2 of them "was lost on the clean reboot". So deriving the sequence from the judged bytes is load-bearing, and it is graded.

**Acceptance 1, met.**
- `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 8` at this head ends "saved-state writer gate: OK across 5 shape(s), and every planted defect reddened". It took about 3 minutes, with rc 0 and 40 "self-test OK" lines (`receipts/host_selftest_head.log`).
- Check 13 runs 472 cases per shape. Each is followed by a change, its commit and a clean reboot. They cover:
  - both orientations;
  - sequences 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF;
  - both slots valid, at 0x5A5A5 and across the wrap at 0;
  - header, sequence and record-area faults;
  - the cold boot and the writer restart.
- The base firmware loses the change in the same model, with 135 "lost" findings per shape (F2's figures).
- The processor half does not apply, because the processor writer carries no generation.

**Acceptance 2, met.**
- `restart_at_zero` is caught by name on three shapes.
- Ten further plants of my own are each caught by a named finding (`receipts/probes_summary.txt`):

  | Plant | Findings |
  |---|---|
  | `p_cold_goes_live` | 169 |
  | `p_held_heartbeats` | 99 |
  | `p_agree_first_only` | 2 |
  | `p_judge_unread_unmarked` | 202 |
  | `p_judge_keeps_verdict` | 70 |
  | `p_restage_once` | 28 |
  | `p_no_restage` | 542 |
  | `p_blank_one_read` | 30 |
  | `p_hold_both_only` | 210 |
  | `p_seq_from_flash` | 42 |

- `p_console_unnamed` is caught by the console check (1 finding).
- Two plants are not caught: `p_restage_unbounded` (F1) and `p_reattach_held_no_publish` (S1, evidence-only).

**Acceptance 3, met.**
- `nvm_commit`, erase, program, verify, `nvm_capture` and `nvm_prefill_stage` have no hunk in the diff.
- Checks 1 to 12 pass on five shapes, and their five controls redden.
- `make -C tb/verilator/nvm_cosim run` with the pinned Verilator 5.050 gives "465 checks: 465 PASS, 0 FAIL" and "39 of 39 mutant(s) killed by their named check", RESULT PASS, rc 0 (`receipts/nvm_cosim_head.log`). The tool reports "Verilator 5.050 2026-07-01 rev v5.050", and its wrapper's sha256 is `905795b9…`.

**Capture receipt.**
- `python3 scripts/check_nvm_capture.py` gives "PASS: capture census, clocks, both timing arms and receipt agree", and its four controls fire (rc 0, `receipts/check_nvm_capture.log`).
- The firmware source sha256 at this head is `5f174859…`, equal to the receipt.
- The receipt's base `4886f231` has tree `4f92a4db…`, as section 18 says. The firmware has not changed since `1f484c66`.
- I recomputed all six arms from `measurements.json`, and each matches the section 18 table:
  - the 8x8 contract maximum is 13.86328 ms (3.5345x, margin 10.63672 ms);
  - the 1x1 maximum is 3.96548 ms (12.3566x);
  - the 100 MHz non-contract maximum is 10.43406 ms.

**Docs gates,** run at this head in a disposable copy:
- `docs_check.py`: 0 findings across 202 md files and 1,248 scrubbed text files. One check was skipped: inventory parity needs git.
- `check_doc_style.py`: OK.
- `DOC_MAP.gen.py --check`: OK.
- The added lines carry no U+2014.
- `check_em_dash.py` could not run, because the pinned renderer is not installed here (rc 2, `receipts/em_dash.log`).

## Clean-lens evidence

```text
[R602] PASS Conformance - sw/firmware/milan_baremetal/milan_baremetal.c:366,737-825,1581-1591,1648-1675,1696-1701,1383 against #671 Required/Acceptance 1-3, assignments 6098494890/6100704879/6103025987, ctrl_nvm/README.md Boot 3,4,9, FASTCONNECT 6.2 and 7; KL_nvm_backend.sv:424,439,490,582; receipts/host_selftest_head.log, receipts/probes_summary.txt (base 743/135 lost; ten independent plants caught), receipts/nvm_cosim_head.log - one staged read per judgement, OK on one read, refusal/blank on two byte-identical reads within 3, re-stage under the picked sequence with fallback, no sequence from refused bytes, UNREAD holds on the cold boot and the re-attach; the base reproduces the loss; F1/F2 are test-strength and evidence-text defects, not conformance gaps
[R602] PASS RTL - milan_baremetal.c:415 (stage holds a 64 KiB slot) with milan_soc.py:3032,4093-4097 (stage = 64 KiB below the live window), :737-761 (copy bounded by rule-3 length <= NVM_SLOT_BYTES, unsigned indices), :781-825 (judge and re-stage bounded at 3; read counts 7 cold / 6 restart measured, receipts/restage_exact_count.log), :1536-1544 (window filled with NVM_IMG_LEN bytes of the re-staged stage), :1657-1668 (fallback loop ends within two passes), :1084-1085 (retired/held: no heartbeat strobe), KL_nvm_backend.sv:637-701 (loss and recovery: backed returns on the next heartbeat, stale on the next commit); all mutable writer statics (milan_baremetal.c:450-482) named in writer_restart.py:18-23; no hdl/ in the diff; nvm_cosim 465/465 and 39/39
```

Robustness, Tests and Docs are UNCLEAN. What each examined:
- **Robustness** (F1):
  - fault windows, and the hold on both paths;
  - both-valid and wrap layouts, and the other-slot address fault;
  - post-judgement persistent faults: the head is correct, but no gate covers them;
  - heartbeat and liveness while held, and the console and wipe while held;
  - retire causes, and publication on a held re-attach (S1).
- **Tests** (F1):
  - checks 13 and 14;
  - the host fault model: `nvm_host.c` read counting and its three fault modes;
  - `writer_restart.py`;
  - the eleven #671 controls on three shapes, thirteen independent plants, and the demonstrator.
- **Docs** (F1, F2):
  - FASTCONNECT 7;
  - BAREMETAL_FIRMWARE Boot and its host-suite paragraph;
  - the nvm_hosttest README and the nvm_cosim README;
  - SNAPSHOT_OWNERSHIP's writer-restart bullet, and sections 18 and 20 item 6, against `measurements.json` and the code;
  - the PR body, and the docs gates.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #671 body and three assignments; #665 decision 2 via ctrl_nvm README Boot 3, 4 and 9; FASTCONNECT 6.2 and 7; `milan_baremetal.c` read, judge, re-stage, pick, go-live, re-attach and commit; `KL_nvm_backend.sv` word 2; writer gate self-test; base reproduction; independent plants; nvm_cosim | R602-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |
| RTL | CLEAN | `milan_baremetal.c` bounds, loop termination, stage and window sizes, writer state on every boot path, static list; `milan_soc.py` stage layout; `KL_nvm_backend.sv` liveness and loss; no HDL in the diff; nvm_cosim 465/465 and 39/39; measured read counts | R602-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |
| Robustness | UNCLEAN (F1) | fault windows; hold on cold boot and re-attach; both-valid and wrap; other-slot fault; post-judgement persistent fault; held liveness, console and wipe; retire causes; held publication (S1) | R602-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |
| Tests | UNCLEAN (F1) | `test_nvm_firmware.py` checks 13 and 14; `read_fault_cases.py`; `nvm_host.c`; `writer_restart.py`; 11 #671 controls on 3 shapes; 13 independent plants; `probe_restage_bound.py` | R602-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |
| Docs | UNCLEAN (F1, F2) | FASTCONNECT 7; BAREMETAL_FIRMWARE Boot and host suite; nvm_hosttest README; SNAPSHOT_OWNERSHIP writer-restart bullet, 18 and 20.6 against `measurements.json`; nvm_cosim README; PR body; docs gates | R602-3 | fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08 |

## Real limits of this review

**No hardware and no physical calibration (NOT RUN).**
- Every fault I drove is the host model's: a view of wrong bytes per mapped read.
- Not exercised: the real LiteSPI read, the N25Q's fault behaviour, a read during an in-flight erase after a CPU-only restart, and real boot timing.
- Skipped field contexts are not hardware proof.

**The restart model is the co-simulation's.** It resets only the writer statics, so obligation O4 is assumed, as the PR states.

**Not run by me.** No manager source bank ran at this head, and I infer none.
- the builder banks (`--require-rv32`, `--require-elaboration`), including the compiled census over the new 64 KiB stage copy;
- the Mark II power-cut suite and the rtl-fast firmware-unit replica;
- the capture CPU harness, so the receipt was regraded, not re-measured;
- an RV32 build, so the +1,768 B text delta is an author receipt;
- the act replica and the pinned-renderer em-dash gate.

**Probe breadth.**
- Most of my plants ran on `endstation_arty_4x4`.
- Five were repeated on `endstation_ax7101_8x8`, and the base reproduction ran on both product shapes.
- The self-test at this head covered all five shapes.

**Environment.**
- Python here is 3.14.7 (the author's is 3.12.3), and the host gcc is 16.2.1.
- The suites ran in disposable copies. Their submodule gitfiles pointed nowhere, so I rebuilt those directories as local snapshot repositories. The first two attempts failed on this before any test ran, and the successful reruns overwrote their logs.
- `nvm_cosim` ran in the clone, and I removed its ignored build outputs afterwards.
- `receipts/probes_g1.log` (rc 1) records a plant that did not compile (`-Werror`, unused variable). It was respelled and ran in `probes_g3`.

**Hosted checks at this head.** Snapshot taken 2026-10-11T02:33:46Z (`receipts/hosted_checks_snapshot.txt`). Accepting them is the manager's duty.
- Succeeded, 13: changes, docs-check-no-git, verilator-lint, bdd-conformance, wire-accountability, full-ci-gate, elaborate, yosys-elaboration, Yosys shards 0 to 3, and Verilator shard 3/5.
- Pending, 6: docs-check, firmware-unit, and Verilator shards 0, 1, 2 and 4.
- Skipped, 1: Physical gPTP (nightly and manual), which is not hardware proof.

**Clone state.** Restored and verified (`receipts/restore_verify.log`, rc 0):
- HEAD and the index tree equal `fc0c517c` / `5df4098e`;
- all 1,272 tracked files rehash to their index blobs, with matching modes;
- there are no untracked or ignored entries;
- the gitlinks are at their pins and clean: protocol-processor `2ad2f845`, gptp-processor `5dce647a`, third_party/verilog-axis `48ff7a7e`;
- `external` and `third_party/lwSRP` were uninitialised, as at the start.

## Pending manager duties

- Carry F1 and F2 to the lane. S1 is optional.
- Re-review at the head that answers them. Tests, Robustness and Docs must be covered again there, with any lens whose scope that change touches.
- Accept the exact-head hosted contexts and run the act replica.
- Validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks.
- Confirm the external review independently.

## Receipts and scripts (listed in MANIFEST.sha256)

- `receipts/VERDICT_FIXED_BEFORE_PRIOR_READ.txt`: the provisional verdict and ledger, written before reading any prior-round review.
- Scripts:
  - `scripts/run_bg.sh` and `wait_rc.sh`: start a campaign and wait for it;
  - `scripts/probe_plants.py`: the plants and the base grading;
  - `scripts/probe_restage_bound.py`: the F1 demonstrator;
  - `scripts/summarize_probes.py` and `scripts/verify_clone.sh`.
- Suite runs: `receipts/host_selftest_head.log/.rc`, `nvm_cosim_head.log/.rc` and `check_nvm_capture.log/.rc`.
- Probes:
  - `receipts/probes/*.txt`, one finding per line;
  - `receipts/probes_summary.txt`;
  - `receipts/probes_g*.log/.rc` and `receipts/probes_base_*.log/.rc`.
- F1 demonstrator: `receipts/restage_bound_*.log/.rc` and `receipts/restage_exact_count.log`.
- Docs gates: `receipts/docs_focused.log`, `docs_check.log` and `em_dash.log`.
- `receipts/hosted_checks_snapshot.txt` and `receipts/restore_verify.log`.
- Local workspace paths in the receipts are replaced by `<packet>`, `<review-clone>`, `<pinned-verilator-5.050>` and `$HOME`.

R602-3 FINISHED

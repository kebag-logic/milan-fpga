[R602] NEGATIVE - exact head f54dbe3e393e2b1b027f1825c4acb736cf502cda

# R602-1: internal cleared-context review of PR #715 (issue #671)

- Head `f54dbe3e393e2b1b027f1825c4acb736cf502cda`, tree `45b1132b81194df293752b67b27119aea99979dd`, on dev `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Role: internal independent reviewer `[R602]`, round R602-1, in its own detached clone.
- All five lenses were applied: Conformance, RTL, Robustness, Tests, Docs.
- **Verdict: NEGATIVE, on one MINOR (F1).** F1 is the PR's fault worst-case boot figure. It touches no code and no test. The firmware change, its tests and the ticket's acceptance 1 to 3 hold at this head.
- Fixing F1 is a change to the PR body and the REVIEW READY evidence. Re-review can be limited to that change unless something else moves.

## Reconstruction

I read the following in order:
1. AGENTS.md and CONTRIBUTING.md (sections 3 and 6).
2. docs/README.md.
3. The #671 body, plus assignment 6098494890, TAKEN 6098611315 and REVIEW READY 6100491164.
4. #665 decision 2 (5997929153), round 4 item 1 (5999350068) and finding 5997533145.
5. FASTCONNECT sections 6.2 and 7, and `sw/firmware/ctrl_nvm/README.md` Boot items 2 to 4 and 9, plus "What this does not prove".
6. `hdl/milan/KL_nvm_backend.sv`, and the processor's NVM modules at pin `2ad2f845`.
7. The full diff `e8454e27..f54dbe3e` (4 commits, 11 files) and its history.
8. The public evidence at `review-evidence/671-r1` (blob `25ad3f94`), read as data only.

**Prior public findings on PR #715:** none. At review time the PR had two "review started" comments, no reviews and no review comments, so there is nothing to resolve or carry forward.

## Answers to the review focus

**1. Is the author right that only the firmware derives the authoritative sequence? Yes.**
- `KL_nvm_backend.sv` only stores and reads back the sequence as a CSR word:
  - `R_SEQ_C = 5'd2` (line 424);
  - `seq_r` declared at 439, reset at 482, written from `csr_wdata_i` at 490, read back at 582;
  - no other use in `hdl/`.
- The processor's NVM path names no sequence or generation anywhere: `KL_aecp_nvm_writer.sv`, `KL_acmp_nvm_shadow.sv`, `KL_pp_nvm_mgr_arb.sv` and `KL_pp_nvm_port.sv` (searched at pin `2ad2f845`).
- So no processor change or adoption is needed.
- The read path really is a pointer load:
  - `nvm_slot()` (`milan_baremetal.c:493`).
  - The Mark II `ls_read` (`ctrl_nvm/plat/nvm_flash_litespi.c:185-196`) fails only on bounds.
  - So the STOP condition does not apply.

**2. Acceptance 1 to 3: met, with the limit stated.**
- **Acceptance 1, case count.** `fault_cases` (`test_nvm_firmware.py:627`) gives 2 orientations × (4 sequences × 19 windows on the valid slot + 19 on the blank slot + 6 single all-0xFF reads) = **202 cases per shape**. The sequences are 1, 0x5A5A5, 0x80000000 and 0xFFFFFFFF. The writer gate passes at this head across all 5 shapes (receipt `hosttest_selftest_head.log`, rc 0, 349 s).
- **Acceptance 1, the base firmware reproduces the loss.** I ran checks 13 and 14 of the head harness against the base firmware (`e8454e27`, sha256 `a73ecc25`). On each product shape, `grade_read_faults` gives 61 findings, 36 of them "lost on the clean reboot" (`probe_base_repro_*.log`).
- **Acceptance 2, the plants.** I re-applied **all four** plants on both product shapes, 1x1 and 8x8. The author's self-test applies them only to the first shape, arty_4x4. Each is caught by its own words (`probe_plants_*.log`):

  | Plant | Findings carrying its words |
  |---|---|
  | `restart_at_zero` | 10 |
  | `unbounded_retry` | 10 |
  | `generation_from_refused_slot` | 8 |
  | `verdict_only_agreement` | 12 |

- **Acceptance 3, A/B unchanged.** These are byte-identical to base in the diff: `nvm_commit`, `nvm_capture`, `nvm_prefill_stage`, the header writer and seal, erase, program and verify. `nvm_cosim` reproduces at this head: 465/465 checks, 39/39 mutants killed by their named check, rc 0 (`nvm_cosim_run.log`, pinned Verilator 5.050 identity recorded in the log).
- **The stated limit.** A fault that returns the same wrong bytes twice, or reads all `0xFF` twice, is taken as content.
  - This is the Mark II store's accepted rule word for word: #665 round 4 item 1 ("Two reads establish a content refusal only when they return identical bytes"), `ctrl_nvm/README.md` Boot item 3 and "What this does not prove".
  - It is stated in the host-suite README and in FASTCONNECT section 7.
  - No reading of a memory-mapped load can do better.
- **On closing #671.** With this limit stated, I judge acceptance 1 to 3 met. I support the manager closing #671 at merge once F1 is answered.

**3. Held-writer reporting: enough, and nothing is persisted.**
- The issue's scope freezes the register map. Given that, `nvm_backed` 0 is the only register-face signal available, and the console line names the hold.
- This works because `nvm_go_live` (`:1574`) sets `nvm_retired`, and `nvm_heartbeat_tick` returns before the heartbeat strobe.
- Every held case in check 13 (README item 12), and every held case in my both-valid probes, shows the same counters: erases 0, programs 0, acks 0, hb 0 and backed 0, with dirty kept at 1.
- One exception, already present for a retired writer: the operator's explicit `milan_nvm wipe` still erases both slots (S3).

**4. Capture re-measure: PASS, every figure checks.**
- `check_nvm_capture.py` passes at this head, and its controls fire (`check_nvm_capture_head.log`).
- The receipt binds the right inputs:
  - firmware sha256 `3b9468ee…`, which equals the head file;
  - tree `a90192e8`, which equals the tree of `7b714334`;
  - processor pin `2ad2f845`.
- I recomputed all six arms' minima, maxima and 49 ms ratios from `measurements.json`. Each matches the section 18 table and item 6:
  - 8x8 maximum 13.86328 ms, margin 10.63672 ms, 3.5345x;
  - 1x1 maximum 3.96548 ms, 12.3566x.
- Not verified by me:
  - the firmware text delta of +1,680 B, because building the RV32 image is outside what this review may run (author receipt only);
  - the boot-time estimate, which is F1.

**5. No register-map, record-format or A/B change.**
- Confirmed: the diff touches no HDL, no generator and no record layout.
- Docs gates pass at this head:

  | Gate | Result |
  |---|---|
  | `docs_check` | 0 findings |
  | `check_em_dash --base e8454e27` | 0 findings over 139 added lines |
  | `gen_toc --check` | OK |
  | `check_doc_style` | OK |
  | `git diff --check` | clean |

- I did not run the builder banks (not allowed here). Their evidence is the author's receipts, each "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11).
- The act replica was not run, by the author or by me.

## Findings

### F1: MINOR, lenses Docs and Robustness. The fault worst-case boot figure leaves out read faults on the length word

- **Where:**
  - the PR #715 body, "Boot time": "The fault worst case is twelve, an estimated 2.5 s of flash at 8x8";
  - REVIEW READY (#671 comment 6100491164), "Open risks": "twelve at worst (about 2.5 s at 8x8…)".
- **Evidence:**
  - `nvm_read_slot` (`milan_baremetal.c:742-752`) reads as many bytes as the header's `IMG_LEN` names, up to `NVM_SLOT_BYTES` (64 KiB), whenever tests 1 to 3 pass. A read fault on the length word therefore makes one read many containers long.
  - Probe S4 faults byte 17 of a valid slot on three reads. The judgement reads are 65,480 + 65,224 + 64,968 B at 8x8, which is 14.77 containers' worth (receipt `probe_scenarios_endstation_ax7101_8x8.log`).
  - At 1x1 the same probe gives 65,288 + 65,032 + 63,752 B (`probe_scenarios_endstation_ax7101_1x1_tdm8.log`).
  - Re-stage reads take the same path (`nvm_restage`, `:807`). The fault worst case is therefore two OK judgements plus six re-stage reads of up to 65,536 B: about 419,728 B, against 12 × 13,256 = 159,072 B.
  - At the author's own rate of 15.5 µs per byte, that is about 6.5 s of flash, not 2.5 s. Each refusal also adds a second CRC pass for its digest (`:754`).
  - The published HANDOFF does give "about 6 s" for a "pathological header", but it treats that as stored content, not a read fault. Its writer-restart estimate (2.5 to 3 s, item 4) has the same gap.
- **Impact:** the conclusion still holds, and it stays well inside #397's 20 s comparison. But the figure the PR and the REVIEW READY give for the fault worst case is too low by a factor of about 2.6 for a fault class the PR itself models (one wrong byte).
- **Required outcome:** the PR body and the REVIEW READY evidence state the fault worst case including length-word faults: about 6.5 s of flash at 8x8 by the stated rate, plus the refusal digest pass. Alternatively, they keep 2.5 s scoped explicitly to faults that leave `IMG_LEN` intact, with the larger bound beside it. The writer-restart heartbeat note is updated to match.
- **Verification:** re-read the corrected text against `nvm_read_slot` / `nvm_restage`, probe S4 and the arithmetic above.

### RESIDUE (wording only; these do not affect the verdict or any lens)

- **R1, Docs. `docs/design/SAVED_STATE_FASTCONNECT.md:785`.** "the next commit lands in B at sequence 1" is true of the Mark II store (`ctrl_nvm/nvm_store.c:615-620`). The shipping writer targets A when no slot is authoritative (`milan_baremetal.c:1378`), so it overwrites A itself, which is the PR body's own second loss mode. Exact fix: replace lines 785-786 with "If A is then taken as refused, the next commit restarts at sequence 1. The bare-metal store writes it to B, and the next clean boot prefers A at s, so that commit is lost. The shipping writer writes it over A, so the saved state is lost."
- **R2, Docs. Check numbering.** `sw/firmware/nvm_hosttest/README.md:11, 89, 105, 123-124, 177` number the new checks 12 and 13 ("thirteen checks"). `test_nvm_firmware.py:46-54, 628, 651, 744` and the PR body and REVIEW READY number them 13 and 14. Exact fix: in the README list, add the existing startup-rejection check as item 12 and renumber the read-fault check to 13 and the refused-generation check to 14. Then change "thirteen checks" to "fourteen checks", "checks 1 to 11" to "checks 1 to 12", "checks 12 and 13" to "checks 13 and 14", and "Check 12 walks" to "Check 13 walks".
- **R3, Docs. `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1650`.** "The firmware changed in its boot path only" is incomplete: the console commit refusal and the status line changed too (`milan_baremetal.c:1934-1935, 1972-1974`). Exact fix: "The firmware changed in its boot path and its console report of the hold only; …".
- **R4, Docs. `sw/firmware/nvm_hosttest/README.md:93-95`.** This sentence includes "an all-`0xFF` read" among the faults walked at "COUNT 1 to 3, and one window covering the whole boot". The all-0xFF cases are COUNT 1 only (`fault_cases`, `--read-ff {slot}:{skip}:1`). Exact fix: end the sentence after the blank-slot fault, and add "A single all-`0xFF` read of the valid slot is walked over SKIP 0 to 5."

### SUGGESTION (optional)

- **S1, Robustness. `milan_baremetal.c:474-476` and `:777-793`.**
  - The read-fault counter is described as "Boot reads whose bytes differed from every earlier read of the slot".
  - It does not count a refused read followed by an OK read. Probe S3 faults only the first judgement read of a valid A: `faulty_reads=1`, but the boot line says `read faults=0`.
  - The Mark II store counts the same way (`nvm_store.c:240-243`), so this is shared and is not a #671 acceptance item.
  - Suggestion: in both stores, count the earlier read when a later read stands OK, or narrow the comment.
- **S2, Tests. `test_nvm_firmware.py:674, 727`.**
  - In check 13's non-held branch, only the changed record is compared after the reboot.
  - Reviewer plant `restage_fail_not_unread` drops the UNREAD mark on a failed re-stage (`milan_baremetal.c:1650`). The suite still catches it, through the B-valid orientation (2 findings per shape).
  - The A-valid orientation is blind to it: with a re-stage-only fault, the planted writer erases A and commits a container that keeps 0/53 (1x1) and 0/163 (8x8) of the other saved records, and those cases pass (`probe_extra_plants_*.log`).
  - Suggestion: require every other saved record to survive in that branch. Also add both-slots-valid layouts with the newer slot faulted and with its re-stage faulted. I probed those at this head (S1, S2 in `probe_scenarios_*.log`): the writer holds, persists nothing, and the clean reboot restores the newer slot, in both orientations, at sequences 2, 0x80000000, 0xFFFFFFFF and 0 across the wrap. They are not yet standing tests.
- **S3, Docs. `docs/integration/BAREMETAL_FIRMWARE.md:2038`.** "the held writer captures, erases and writes nothing" could add that an explicit `milan_nvm wipe` still erases both slots (`milan_baremetal.c:1981-1992`). That behaviour predates this PR and matches a retired writer.

## Clean-lens evidence

```text
[R602] PASS Conformance - milan_baremetal.c:731-817,1574-1583,1639-1666; KL_nvm_backend.sv:424,439,482,490,582; processor KL_aecp_nvm_writer.sv, KL_acmp_nvm_shadow.sv, KL_pp_nvm_mgr_arb.sv, KL_pp_nvm_port.sv @2ad2f845; probe_base_repro_*.log, probe_plants_*.log - #671 Required and acceptance 1-3 against #665 decision 2 and round 4 item 1: refusals stand on two equal-byte reads within 3, OK on one plus a re-stage under its picked sequence, no sequence from a refused slot, UNREAD holds; base firmware loses the change in the same model; all four plants caught by name on 1x1 and 8x8; the identical-wrong-bytes limit is the accepted Mark II rule
[R602] PASS RTL - milan_baremetal.c:366,407-415,731-817,1530-1538,1611-1761; milan_soc.py:3014-3032 (64 KiB stage below the live window); KL_nvm_backend.sv CSR word 2 - stage bound (NVM_SLOT_BYTES <= MILAN_NVM_IMAGE_MAX, a 64 KiB stage), validate reads stay inside IMG_LEN, an accepted container is exactly NVM_IMG_LEN so the window fill copies only re-staged bytes, the fallback loop ends within two passes, every boot path's writer state (live, held, retired, disabled), no HDL, register or record-format change
```

Robustness and Docs are UNCLEAN because of F1. Their reviewed scope was:
- **Robustness:** fault windows, the hold, both-valid and re-stage fallback probes, wrap sequences, length-word faults, the writer-restart path.
- **Docs:** FASTCONNECT 7, BAREMETAL_FIRMWARE Boot, the host-suite README, SNAPSHOT_OWNERSHIP 18 and 20 item 6, the PR body, REVIEW READY and HANDOFF.

```text
[R602] PASS Tests - test_nvm_firmware.py:149-182,627-790,808-828; nvm_host.c read-fault model; hosttest_selftest_head.log (5 shapes, 9 writer plants plus boot-walk plants reddened); nvm_cosim_run.log 465/465, 39/39; probe_extra_plants_*.log - each new check can fail for its named defect (four plants plus one reviewer plant caught), the bound check is exact (BOOT_READ_BOUND 13 = AEM + 12), run_cases.py names the two new statics; the remaining oracle weakness is S2 (SUGGESTION)
```

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #671 body and assignment; #665 decisions 5997929153 and 5999350068; FASTCONNECT 6.2 and 7; ctrl_nvm README Boot 2-4, 9; `milan_baremetal.c` diff; `KL_nvm_backend.sv`; processor NVM modules @2ad2f845; base-reproduction and plant probes | R602-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |
| RTL | CLEAN | `milan_baremetal.c` boot, read, judge, re-stage, fill, go-live and console paths; SoC stage layout; backend CSR word 2; `nvm_cosim` 465/465 and 39/39 | R602-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |
| Robustness | UNCLEAN (F1) | fault windows and the hold; both-valid probes S1/S2; counter probe S3; length-word probe S4; writer-restart path; `wipe` while held | R602-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |
| Tests | CLEAN | `test_nvm_firmware.py` checks 13/14 and plants; `nvm_host.c` model; `run_cases.py`; writer gate across 5 shapes; four plants on 1x1 and 8x8; reviewer plant | R602-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |
| Docs | UNCLEAN (F1) | FASTCONNECT 7; BAREMETAL_FIRMWARE Boot and host-test paragraph; nvm_hosttest README; SNAPSHOT_OWNERSHIP 18 and 20.6; `measurements.json`; PR body; REVIEW READY; docs gates | R602-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |

## Real limits of this review

- **No hardware and no physical calibration.** The memory-mapped LiteSPI read, its fault behaviour on a real N25Q and real boot timing are unmeasured. The host model plants faults on wrong bytes only.
- **Not run by me:**
  - builder banks, `--require-rv32`, the Mark II power-cut suite and rtl-fast firmware-unit (author receipts only);
  - the act replica and the hosted jobs;
  - an RV32 build, so the +1,680 B text delta is not independently verified;
  - a capture re-measurement in the CPU harness. The receipt was regraded, not re-run.
- **Hosted checks at this head (snapshot taken at review time):**
  - succeeded: changes, docs-check-no-git, verilator-lint, bdd-conformance, wire-accountability, full-ci-gate, Verilator shard 3/5, and Yosys shards 0-3/4;
  - still running: docs-check, elaborate, firmware-unit, yosys-elaboration, and Verilator shards 0, 1, 2 and 4;
  - skipped: Physical gPTP, which is no hardware proof.
  - Acceptance of these belongs to the manager.
- **Clone state.** After the probes it holds exact head bytes: the index tree equals `45b1132b`, worktree bytes rehash to the index blobs, and modes match. The required gitlinks are at their pins: protocol-processor `2ad2f845`, gptp-processor `5dce647a`, third_party/verilog-axis `48ff7a7e` (`restore_verify.log`). `external` and `third_party/lwSRP` were uninitialised from the start; the log's "checkout=" value for those two is the superproject HEAD, not a submodule checkout.

## Pending manager duties

- Carry F1 back to the lane, and R1 to R4 to the residue checklist.
- Run the act replica and accept the exact-head hosted contexts.
- Validate the current-dev merge candidate: base `e8454e27`, live dev `f88df731`, builder and native banks.
- Confirm the external review (R603) independently.
- Close #671 at merge, as the PR body says "Relates", if both reviews are POSITIVE.

R602-1 FINISHED

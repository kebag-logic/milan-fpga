[R603] NEGATIVE - exact head f54dbe3e393e2b1b027f1825c4acb736cf502cda

# R603-1: external review of PR #715 (issue #671)

- Head `f54dbe3e393e2b1b027f1825c4acb736cf502cda`, tree `45b1132b81194df293752b67b27119aea99979dd`. Source base `e8454e2751d05b02ee8e5a571857589ab358ab86`.
- Role: external independent reviewer, cleared context. I read AGENTS.md, CONTRIBUTING.md, docs/README.md, the #671 body and its three public comments (assignment 6098494890, TAKEN 6098611315, REVIEW READY 6100491164), the #665 decisions 5997929153 and 5999350068, the PR body, the full diff `e8454e27..f54dbe3e` and its four commits, and the public evidence tree `25ad3f94:review-evidence/671-r1`.
- No manager source bank ran at this head, and I infer none. The execution evidence at this head is the author's published receipts plus my own focused reruns and probes below.

## Verdict in one paragraph

The firmware change is correct as far as I could drive it. Every slot is judged on one staged read. OK stands on one read. Any other verdict stands only on two byte-identical reads (verdict, count, CRC-32 digest) within a bound of three. The picked slot is re-staged and re-judged under its picked sequence, and an UNREAD slot holds the writer: nothing is captured, erased, programmed or acknowledged, there is no heartbeat, and `nvm_backed` reads 0.

I confirmed the author's sequence-locality finding in the backend and processor sources. The base firmware reproduces the #671 loss in the head's model. The four named plants fail by name, and I re-applied four independently spelled equivalents, all caught. The head stays clean under faults the shipped matrix does not try: record-area bytes, both slots valid, and the sequence wrap.

The verdict is NEGATIVE for one test weakness (F1, MAJOR). Check 13 faults only header bytes 0 and 0x0B, so two load-bearing parts of the fix can regress with the gate green while reproducing the #671 data loss: the whole-container refusal digest, and filling the window from the judged stage. I found one MINOR too (F2): the PR body's boot-time "worst case" figure is understated.

## Findings

### F1 - MAJOR - Tests - check 13 cannot fail for two of the mechanisms the fix depends on

- **Where:** `sw/firmware/nvm_hosttest/test_nvm_firmware.py:638` (every valid-slot fault is byte `0x00` or `0x0B`, both in the 40-byte header) and `:634-646` (one valid slot plus one blank, never two valid). `sw/firmware/nvm_hosttest/README.md:93` states the header-only scope ("its magic byte or its sequence word").
- **Authority:**
  - The PR, the TAKEN comment and `docs/integration/BAREMETAL_FIRMWARE.md:2014-2045` (Boot) state that a refusal stands only when two reads agree "by verdict, length and a CRC-32 digest" of the bytes read, that "the window is filled from the stage, never from a fresh read", and that an unread pick has "the other ... offered".
  - The #671 assignment applies the Mark II rule, and #665 round 4 item 1 (5999350068) made the standing probe for that rule "header and body".
  - AGENTS.md section 6, `Tests`: "Each new test can fail for the defect it claims to detect".
- **Evidence:** my plants were applied to an in-memory copy of the head firmware and graded with the head's own checks 13 and 14 on `endstation_arty_current`. Receipts: `receipts/probe_plants2_current.log`, `receipts/probe_bodyfault_current.log`, `receipts/probe_bodyfault2_current.log` and `receipts/probe_both_valid_current.log`, made by `scripts/probe_read_fault.py` and `scripts/probe_both_valid.py`.

  | plant (one line each) | shipped checks 13/14 | same checks, fault moved to record-area byte 0x40 | both-valid probe |
  |---|---|---|---|
  | `r_digest_header_only`: refusal digest over `KLJ2_HDR` bytes instead of `rd.bytes` (`milan_baremetal.c:754`) | **0 findings** | 28 findings, "the change committed after the faulty boot was lost on the clean reboot" | not run |
  | `r_fill_from_flash`: `nvm_fill_window()` reverted to the base fresh read of the slot (`:1530-1538`) | **0 findings** | 48 findings: the window holds unjudged bytes, every later commit is refused and the change is lost | 36 findings |
  | `r_restage_fail_offers_none`: an unread pick offers nothing instead of the other slot (`:1658`) | **0 findings** | not run | 8 findings, "held with the older slot read cleanly, yet nothing was offered" |
  | unplanted head | 0 | 0 | 0 of 304 cases |

- **Impact:** the head is correct, but the gate that is meant to keep it correct is blind to these regressions. A one-line change to the digest's span, or a revert of the fill to the pre-#671 code, reintroduces silent loss of a committed change, which is #671's own defect. The gate stays green while that happens. The third row is a documented behaviour that no test exercises.
- **Required outcome:**
  - Check 13 also faults at least one record-area byte of the valid slot. A refusal decided after the header must be among the faulted cases.
  - Check 13 adds at least one both-slots-valid arrangement in both orientations, so the "other slot is offered" path is exercised.
  - Each of the three plants above (or equivalents) becomes a named `--self-test` control that reddens.
- **Verification:** at the new head, `test_nvm_firmware.py --self-test` stays OK across 5 shapes, and each new control is reported "caught by N named finding(s)". Reapplying my three plants (`scripts/probe_read_fault.py`, `PLANTS`) to the new head must redden the shipped gate.

### F2 - MINOR - Docs, RTL - the boot-time "worst case" assumes container-length reads

- **Where:** PR #715 body, "Boot time" ("The fault worst case is twelve, an estimated 2.5 s of flash at 8x8 against #397's 20 s comparison"), and the REVIEW READY comment 6100491164 ("twelve at worst (about 2.5 s at 8x8 against #397's 20 s)").
- **Authority:** `milan_baremetal.c:645` admits a header length up to `NVM_SLOT_BYTES` (64 KiB). `nvm_read_slot()` (`:743-754`) then copies that many bytes and CRCs them, once to judge and once more for the digest. Only an OK container is exactly `NVM_IMG_LEN` (13,256 B at 8x8). The author's own published handoff scopes the 2.5 s to "every read of a valid-length container faulty", but the PR body drops that scope. AGENTS.md `RTL` lens: "latency, and resource/timing effects are understood".
- **Impact:** a slot whose header (stored, or as one faulty read returns it) declares a long length costs about 5x a container read on each of up to six judgement reads. On the author's own basis (12 x 13,256 B = 2.5 s), the worst case is about (6 x 65,536 + 6 x 13,256) / (12 x 13,256) x 2.5 s, roughly **7.4 s**, plus the DRAM-side CRC passes. That is still inside the 20 s comparison, so no requirement is broken, but the published "worst case" figure is about 3x low. The writer-restart risk the author discloses (a re-judge longer than T-NVM-WRITER-ALIVE, 2 s) is reached sooner than stated.
- **Required outcome:** the PR body gives the worst case with refused reads up to the 64 KiB slot, or scopes the 2.5 s figure to container-length reads and states the larger bound beside it. It stays labelled an estimate.
- **Verification:** a reviewer re-reads the PR body at the next head. No code change is needed.

### R1 - RESIDUE - check numbering differs between the suite and its README

- `sw/firmware/nvm_hosttest/README.md:11, 89, 105, 124, 177` number the #671 checks 12 and 13 ("thirteen checks per shape").
- `test_nvm_firmware.py:46, 53, 173, 628, 651, 780` number them 13 and 14.
- The offset is inherited from the README's unnumbered "Console tests" item.
- Exact fix: in the README, number the console-rejection item 12 and the #671 items 13 and 14, write "fourteen checks per shape", and change "checks 12 and 13" and "Check 12" to "checks 13 and 14" and "Check 13".
- Wording only: no figure, test or verdict changes.

### Suggestions (optional; not counted against any lens)

- **S1:** `milan_nvm wipe` (`milan_baremetal.c:1981`) still erases both slots while the writer is HELD. That is safe: both slots blank cannot outrank a later commit. But the pages say the held writer "erases ... nothing". Either refuse `wipe` while held, or say the operator wipe is the exception.
- **S2:** `nvm_unread` is set before the boot path is chosen. On the contract-mismatch, no-load-accepted and window-went-live paths, `milan_nvm` therefore prints "writer HELD, a slot unread at boot" and the commit refusal names the unread slot (`:1934`, `:1973`), where the real cause is the retire. Nothing persists either way; only the console's stated cause is wrong.
- **S3:** the re-stage's sequence check (`rd.seq == seq`) is not exercised: plant `r_restage_any_seq` shows 0 findings with header and body faults (`receipts/probe_plants3_current.log`, `receipts/probe_bodyfault2_current.log`). Under the CRC it is reachable only by a fault returning another valid container, such as an address fault returning the other slot. The host model cannot express that fault, so it is defence in depth. A both-valid case whose faulty view returns the other slot's bytes would pin it.

## The focus questions, answered from evidence

1. **The sequence is derived only in the firmware. True.**
   - In `hdl/milan/KL_nvm_backend.sv`, word 2 (`R_SEQ_C`) is a plain register: decode `:424`, declaration `:439`, reset `:482`, write `:490`, readback `:582`. Nothing in the module reads `seq_r` to decide anything.
   - `nvm_backed` is set only by a heartbeat (`:653-655`, `:682-683`), and `ever_backed_r` gates loss (`:648`).
   - `protocol-processor` at `2ad2f845`: `KL_aecp_nvm_writer.sv`, `KL_pp_nvm_port.sv`, `KL_pp_nvm_mgr_arb.sv` and `KL_acmp_nvm_shadow.sv` carry no slot sequence or generation (searched for seq, generation, epoch and slot; the only hits are comments and unrelated ACMP/AECP sequence ids).
   - In the firmware, the sequence comes from `nvm_read_slot()` on VD_OK only (`:751-752`), flows through `nvm_judge_slot()`, `nvm_restage()`, `nvm_pick_slot()` and `nvm_boot()`, and `nvm_commit()` uses `nvm_seq + 1`.
2. **Acceptance 1-3.**
   - *1, met:*
     - My head rerun: "saved-state writer gate: OK across 5 shape(s), and every planted defect reddened" (`receipts/hosttest_selftest.log`, rc 0).
     - The matrix is 2 orientations x (4 sequences x 19 windows + 19 blank-slot windows + 6 all-0xFF) = 202 cases per shape, as claimed.
     - The base firmware graded by the head's checks reproduces the loss: 61 findings under header faults and 138 under body faults (`receipts/probe_plants1_current_partial.log`, `receipts/probe_bodyfault_current.log`). Slot B valid at 0x5A5A5 or 0x80000000 restores the old payload `d4e5f607` instead of the change. Slot A valid and faulted ends with both slots blank.
   - *2, met:* the shipped controls `restart_at_zero`, `unbounded_retry`, `generation_from_refused_slot` and `verdict_only_agreement` are each "caught by N named finding(s)" in my rerun. I re-applied four independently spelled equivalents (`r_restart_at_zero`, `r_retry_over_bound`, `r_generation_from_flash`, `r_agree_without_digest`), and each is caught by the named finding words. I also caught `r_no_second_agreement`, `r_two_tries`, `r_held_heartbeats`, `r_console_commit_while_held` and `r_no_restage`.
   - *3, met:* `nvm_commit()`, `nvm_slot_erase()` and `nvm_slot_program()` have no hunk in the diff. `nvm_cosim` at this head gives "465 checks: 465 PASS, 0 FAIL" and "39 of 39 mutant(s) killed by their named check" (`receipts/nvm_cosim_run.log`, rc 0). No `hdl/`, register-map or `scripts/nvm_klj2.py` change.
   - F1 is a test-strength defect beyond the acceptance minimum. It does not make acceptance 1-3 unmet.
3. **The stated limit.**
   - A fault returning the same wrong bytes twice is the definition #665 round 4 item 1 adopted ("Two reads establish a content refusal only when they return identical bytes"), and `sw/firmware/ctrl_nvm/README.md` Boot item 3 states it the same way.
   - My limit run (`receipts/probe_both_valid_current.log`, `limit_*`) reproduces it: slot B valid at 0x5A5A5 read as all-0xFF twice is taken for blank, the change goes to A at sequence 1, and the clean reboot prefers B.
   - The shipping read is a pointer load with no error report, so no read-based rule can tell that case apart. With the limit stated in FASTCONNECT section 7, both READMEs and the PR, I judge acceptance 1-3 met. The PR body says "Relates to #671". Closing #671 at merge on two POSITIVE reviews is the manager's call, and this round is not one of them (F1, F2).
4. **Held-writer reporting is enough, and nothing persists while held.**
   - Register face: the backend raises `nvm_backed` only on a heartbeat. The held cold boot never strobes one (`nvm_heartbeat_tick()` returns on `nvm_retired`, `:1078`), so the face reads backed 0, stale 0: the existing "no live writer" signal.
   - Console: the boot line carries `unread=`, plus a HELD line and `milan_nvm` "writer HELD".
   - The register map is frozen by the assignment, so a distinct register bit was out of scope. The console line plus backed 0 is enough.
   - Nothing persisted: in every held case of the shipped check, and in my 40 held both-valid cases, erases, programs, acks, heartbeats and backed are all 0. The console commit plant and the heartbeat plant are both caught. The one exception is the operator `wipe` (S1).
5. **Capture re-measure.**
   - `scripts/check_nvm_capture.py` at this head: "PASS: capture census, clocks, both timing arms and receipt agree", with all four controls detected (`receipts/check_nvm_capture.log`). The head firmware sha256 is `3b9468ee...6de6`, equal to the receipt's `product_firmware_sha256`.
   - Nothing under `sw/`, `hdl/`, `scripts/` or the capture harness changed between the measured commit `7b714334` (tree `a90192e8`) and this head.
   - The six maxima in section 18 match `measurements.json` exactly: 8x8 contract maximum 13.86328 ms (margin 10.63672 ms to 24.5 ms, 3.5345x), 1x1 maximum 3.96548 ms (12.3566x). The census is unchanged at 164/13,210 and 54/3,290.
   - Firmware size: my RV32 estimate (host stub headers, `-Os`, not the product build) gives text +1,520 B and bss +8 B (`receipts/fw_size_estimate.txt`), the same order as the author's +1,680/+8 from product headers. That corroborates the figure but is not a reproduction.
   - Boot time: see F2.
6. **Other evidence.**
   - The author did not run the act replica, and I did not run it either (not allowed).
   - Exact-head hosted snapshot at 2026-10-10T18:10:40Z (`receipts/hosted_check_runs_f54dbe3e.tsv`): 11 runs completed success, 8 in progress (Verilator shards 0, 1, 2 and 4 of 5, `firmware-unit`, `yosys-elaboration`, `elaborate`, `docs-check`), and 1 skipped (`Physical gPTP`, nightly/manual: a skipped context, not hardware proof).
   - `scripts/docs_check.py` at this head: 0 findings across 202 md files (`receipts/docs_check.log`).

## Lens coverage at f54dbe3e

```text
[R603] PASS Conformance — milan_baremetal.c:731-819,1574-1583,1639-1666,1969-1977; hdl/milan/KL_nvm_backend.sv:424-490,582,630-684; protocol-processor@2ad2f845 NVM writer/port/arbiter/shadow; #671 body + 6098494890; #665 5997929153/5999350068; ctrl_nvm/README.md Boot 2-4,9 — rule, bound, HELD semantics, sequence locality and acceptance 1-3 checked against the issue, the assignment and the Mark II decisions; head rerun and base reproduction
[R603] MINOR RTL — PR #715 body "Boot time" — F2; otherwise examined milan_baremetal.c:366,407-415 (stage fits a 64 KiB slot),645,731-819 (bounded loops, unsigned indices, digest span),1530-1538,1648-1659 (re-pick loop ends within two passes),1078 (held: no heartbeat); KL_nvm_backend.sv backed/alive/loss logic unchanged; no further finding
[R603] PASS Robustness — receipts/probe_bodyfault_current.log, probe_both_valid_current.log, hosttest_selftest.log — header and record-area faults, one valid plus one blank and both valid, both orientations, SEQ 1/0x5A5A5/0x80000000/0xFFFFFFFF and the 0xFFFFFFFF->0 wrap, single all-0xFF reads, faults lasting the whole boot, read bound 13, console commit while held: head 0 findings; the stated same-bytes limit reproduces as documented
[R603] MAJOR Tests — sw/firmware/nvm_hosttest/test_nvm_firmware.py:634-646 — F1
[R603] MINOR Docs — PR #715 body "Boot time" — F2; R1 RESIDUE recorded; examined docs/design/SAVED_STATE_FASTCONNECT.md:781-800, docs/integration/BAREMETAL_FIRMWARE.md:2014-2045,2148-2155, sw/firmware/nvm_hosttest/README.md, docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md section 18 and section 20 item 6 against measurements.json, PR body
```

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | firmware boot/judge/restage/go-live/console; backend seq and backed logic; processor NVM modules; #671 body and assignment; #665 decisions; ctrl_nvm Boot rule; host gate rerun; base reproduction | R603-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |
| RTL | UNCLEAN (F2) | firmware bounds, widths and loop termination; backend liveness/seq RTL (unchanged); boot latency | R603-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |
| Robustness | CLEAN | header/body/all-0xFF faults, both-valid, wrap, held path, read bound; probes and reruns listed above | R603-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |
| Tests | UNCLEAN (F1) | test_nvm_firmware.py checks 13/14 and plants; nvm_host.c fault model; nvm_cosim; capture gate; 13 reviewer plants | R603-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |
| Docs | UNCLEAN (F2; R1 residue) | FASTCONNECT section 7, BAREMETAL_FIRMWARE Boot and host suite, nvm_hosttest README, SNAPSHOT_OWNERSHIP sections 18 and 20, PR body, REVIEW READY | R603-1 | f54dbe3e393e2b1b027f1825c4acb736cf502cda |

## Prior public review findings on this PR

I read these only after the verdict and ledger above were written, and checked at 2026-10-10T18:14:46Z. PR #715 holds two public issue comments, the R602-1 and R603-1 review-start notices (6100504738, 6100505250). It holds no formal review and no inline comment. #671 holds only the assignment, TAKEN and REVIEW READY. There is **no prior public finding on this PR to resolve or retain**. The sibling-store precedent F1 relies on, #665 round 4 item 1 (R501-3 F1: compare bytes, standing probe "header and body"), is cited as authority, not carried as a finding of this PR.

## Receipts (all listed in MANIFEST.sha256)

- `receipts/identity.txt`: head, base, tool versions, commands.
- `receipts/hosttest_selftest.log` / `.rc`: the writer gate with self-test, 5 shapes, rc 0.
- `receipts/nvm_cosim_run.log` / `.rc`: 465/465, 39/39, rc 0.
- `receipts/check_nvm_capture.log` / `.rc`: PASS, rc 0.
- `receipts/docs_check.log` / `.rc`: 0 findings, rc 0.
- `receipts/probe_plants1_current_partial.log`: base firmware plus four re-applied plants under the head's checks 13/14. This run was cut short when a fifth plant failed to compile under `-Werror`. That plant was re-spelled and rerun in `probe_plants2`.
- `receipts/probe_plants2_current.log`, `receipts/probe_plants3_current.log`: head and the remaining plants, header faults.
- `receipts/probe_bodyfault_current.log`, `receipts/probe_bodyfault2_current.log`: head, base and plants with the valid-slot fault moved to record-area byte 0x40.
- `receipts/probe_both_valid_current.log`: 304 both-valid cases per firmware, plus the stated-limit run.
- `receipts/fw_size_estimate.txt`: RV32 size estimate, base vs head.
- `receipts/hosted_check_runs_f54dbe3e.tsv` and `.snapshot_utc`: exact-head hosted runs at the snapshot time.
- `scripts/probe_read_fault.py` and `scripts/probe_both_valid.py`: run as `python3 -B scripts/probe_read_fault.py REPO REPO/configs/endstation_arty_current.yaml WORK [--head] [--base-fw FILE] [--body-fault 0x40] --plant NAME ...` and `python3 -B scripts/probe_both_valid.py REPO CONFIG WORK --head --plant NAME ...`. They never write the checkout; plants are applied to an in-memory copy.

## Real limits

- Every fault I drove is the host model's: a wrong-bytes view per mapped read. The model has no LiteSPI timing, no address-line fault and no partial-read error. Physical calibration was NOT RUN, and no hardware was used.
- My probes ran on one shape (`endstation_arty_current`); the author's matrix and my head rerun cover all five. The size figure is an estimate on stub headers. The boot-time figure in F2 is an estimate on the author's own basis, not a measurement.
- No processor or builder bank, no act replica and no Yosys run was executed by me. The builder `--require-rv32` and `--require-elaboration` results are the author's receipts only.
- A container does not bind its slot, so an address fault returning the other slot's valid container on a judgement read can be taken for OK on one read. The re-stage's sequence check narrows this for the picked slot only (S3). This is outside #671's stated fault model.
- After my runs, the clone was restored to the exact head and verified: worktree and index match HEAD, no untracked or ignored files, tree `45b1132b`, and gitlinks at the recorded commits (`protocol-processor` `2ad2f845`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, all clean; `external` and `third_party/lwSRP` uninitialised, as at start).

## Pending manager duties

- Hosted acceptance at the exact head: 8 runs were still in progress at the snapshot, and the act replica has not been run.
- The current-dev merge candidate (base `e8454e27`, live dev `f88df731`), with its builder and native banks.
- Carry R1 to the residue checklist.
- Re-review at the head that answers F1 and F2. The Tests, RTL and Docs lenses must be covered again there.

R603-1 FINISHED

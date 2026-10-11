[R603] NEGATIVE - exact head fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08

External independent review R603-3 of issue #671 / PR #715. Head `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08`, tree `5df4098eebf77625bd26899bb84cd72ca35e96e4`, diff from source base `e8454e2751d05b02ee8e5a571857589ab358ab86` (16 commits, 14 files).

**Verdict: NEGATIVE on one MINOR, R603-3-F1 (Tests, Robustness, Docs).** The firmware is correct at this head on every path I read and drove. Acceptance 1 to 3 are met. Every prior finding on this PR is resolved. One mechanism of the fix still has no check that can fail: the re-stage's retry bound.

- With the bound set to 2 tries, 4 tries, or removed, checks 13 and 14 stay green.
- With the bound removed, a judgement-read address fault, a fault mode the PR documents, makes the boot hang forever.
- The PR body still says check 13 "can fail for every mechanism the fix depends on".

My verdict and ledger were recorded in `receipts/verdict_ledger_before_prior_findings.md` (02:49:36Z). That was before I read any prior review report. I did not read the concurrent internal round-3 report.

## Reconstruction

- **Order.** I read AGENTS.md, CONTRIBUTING.md sections 3 and 6, the #671 body, and the manager's assignment and round-2 and round-3 assignments. Then I read the author's TAKEN and REVIEW READY comments 1 to 3, the PR body, the diff and history, and the public evidence tree `review-evidence/671-r1` at `25ad3f94`. That evidence is round-1 author evidence, and I re-ran its gates at this head.
- **Frozen acceptance (issue body).** Acceptance 1: a transient refusal of A, then a change, a commit and a clean reboot, in the shipping path's tests. The change survives or persistence was refused. Both orientations and the sequence boundaries are run. Acceptance 2: a planted restart-at-zero control fails. Acceptance 3: the A/B power-loss guarantees are unchanged.
- **Proof list (manager's assignment).** Planted restart-at-zero, unbounded-retry and generation-from-invalid-slot controls each fail by name. The existing A/B suites pass. Capture is re-measured. Round 2 added: "check 13 must be able to fail for every mechanism the fix depends on". Round 3 added: "The PR body's 'every mechanism' sentence is then true. Keep it true."
- **Scope derived.** The rule applies wherever the shipping path derives the authoritative sequence. I confirmed that this is the firmware alone:
  - `hdl/milan/KL_nvm_backend.sv:424,439,482,490,582`: `seq_r` is a stored and read-back word, and nothing decides on it.
  - `protocol-processor` `2ad2f845` `hdl/aecp/KL_aecp_nvm_writer.sv`: per-record CRC-16 only, with no slot and no generation.
  - So no processor change is needed, and the processor half of acceptance 1 does not apply.

## Findings

### R603-3-F1 - MINOR - Tests, Robustness, Docs - the re-stage's retry bound is reached by no check that can fail

- **Where.**
  - `sw/firmware/milan_baremetal/milan_baremetal.c:813-825` (`nvm_restage`, loop at `:818`): the picked slot is re-read at most `NVM_READ_TRIES` (3) times.
  - `sw/firmware/nvm_hosttest/read_fault_cases.py:256-268` (`read_findings`): only the boot total is bounded (13 reads; 12 on a restart). The exact count is asserted only for a whole-boot fault, which fails the judgement and never reaches a re-stage.
  - `read_fault_cases.py:120,126` (`RESTAGE_WINDOWS`, `RESTART_RESTAGE`): these drive every re-stage read faulty. But `:290` and `test_nvm_firmware.py:758` require the hold only when the boot line reports `unread`, or for the whole-boot window. So a firmware that re-stages a fourth time, succeeds and goes live grades exactly like one that holds.
  - `READ_FAULT_MUTATIONS` has `unbounded_retry` and `r_judge_four_tries` for the judgement loop. It has no control on the re-stage loop.
- **Authority.**
  - #671 Required: "The writer retries the read within a bound."
  - Assignment 6098494890: "So do a planted unbounded retry."
  - Round-2 assignment item 1: "check 13 must be able to fail for every mechanism the fix depends on".
  - Round-3 assignment item 1: "Keep it true."
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
  - The PR body ("Round 3") says check 13 "fails for each of these mechanisms", and the round-3 REVIEW READY says "check 13 can fail for every mechanism the fix depends on".
  - `sw/firmware/nvm_hosttest/README.md:137-138` and the suite docstring `test_nvm_firmware.py:59-60` present "three re-stages per slot" and "the reads the per-slot bound allows" as checked.
- **Evidence** (`scripts/probe_plants.py`, which plants into a copy of the firmware text and grades it with the head's own checks; `receipts/probes/`):
  - `none` (the head, unplanted): 0 findings on `endstation_arty_4x4`, so the probe itself is sound.
  - `p_restage_four_tries`, `p_restage_two_tries` and `p_restage_unbounded` (the loop at `:818` set to 4, 2 or 2^32-1 tries): 0 findings each in checks 13 and 14 on `endstation_arty_4x4`.
  - `p_restage_unbounded` with checks 1 to 14: 0 findings on `endstation_arty_4x4`.
  - `p_restage_unbounded`, checks 13 and 14: 0 findings on `endstation_ax7101_1x1_tdm8` and on `endstation_ax7101_8x8`.
  - No other suite injects a read fault: only `test_nvm_firmware.py`, `read_fault_cases.py` and `writer_restart.py` name `--read-*`, so `nvm_cosim`, boot-walk and disabled-writer cannot see it either.
  - Controls in the same probe run are caught: `p_judge_no_unread` (202 findings), `p_hold_only_both` (210), `p_held_heartbeats` (99), `p_seq_from_flash` (38) and `p_judge_ignores_second` (2). So the gap is specific to the re-stage bound.
- **Impact** (`scripts/probe_restage_hang.py`, `receipts/probes/restage_hang.log`). The scenario: slot A is blank and slot B is valid at 0x5A5A5. A's single judgement read is answered with B's container (`--read-other a:1:1`, the address fault the PR's own limits paragraph describes).
  - **Head:** A is picked on the tie and its three re-stages are refused, so A is UNREAD and B is offered. The writer is HELD after 7 reads, the boot line prints and the walk runs (`walks=1`).
  - **Unbounded re-stage:** no boot line, no restore walk (`walks=0`), and the host stops it at 1,000,001 reads. On hardware the boot never reaches `entity_advertise()`, and the entity stays down while the fault lasts.
  - **Four re-stage tries:** 8 reads. The console still says "in 3 reads".
  - A one-line regression in the re-stage loop can therefore hang the boot, or move the stated bound and the roughly 17.1 s worst-case estimate built on it, with every gate green.
- **Required outcome.**
  - Check 13 asserts that a re-stage refused on all three of its reads holds the writer and opens an exact read count. For example: the existing `--read-other` (3,3) cold case holds after 7 reads, and the (2,3) restart case after 6.
  - A named `--self-test` control that changes the re-stage bound (for example `p_restage_four_tries` or `p_restage_unbounded` above, byte-identical) reddens with a named finding on `endstation_arty_4x4`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`.
  - The PR body's "every mechanism" sentence is then true again, or is narrowed to what is checked.
  - Optional: add the judgement-read address fault above as a standing case.
- **Verification.**
  - `python3 -B scripts/probe_plants.py <root> <empty dir> p_restage_four_tries configs/endstation_arty_4x4.yaml` prints `VERDICT CAUGHT`, and likewise `p_restage_unbounded` on the three shapes.
  - `python3 sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test` reports the new control "caught by N named finding(s)" on three shapes.
  - `probe_restage_hang.py` still shows the head holding after 7 reads.

### R603-3-S1 - SUGGESTION - Robustness - the hold's console line names the wrong cause for a re-stage that never read back

- `milan_baremetal.c:1589-1590`: a slot marked UNREAD by the re-stage loop (`:1657-1659`) was judged OK and only failed to read back, yet the line says it "gave no standing verdict in 3 reads" (`receipts/probes/restage_hang.log`, head).
- The state and the hold are right; only the stated reason is wrong.
- Optional: say "gave no standing verdict or did not read back as judged". The comment at `:470-472` already distinguishes the two.

## Prior public findings, resolved or retained at this head

| Prior finding | State at `fc0c517c` | Evidence |
|---|---|---|
| R603-1-F1 MAJOR (Tests): no record-area or both-valid faults; `r_digest_header_only`, `r_fill_from_flash`, `r_restage_fail_offers_none` green | RESOLVED | `read_fault_cases.py:168-219`. My `--self-test` run catches all three by their own words on three shapes (`receipts/gate_selftest.log:75-83`). |
| R603-1-F2 MINOR (Docs, RTL): worst case assumed container-length reads | RESOLVED | The PR body "Boot time" prices slot-length reads (16.4 s / 17.1 s), labelled an ESTIMATE. The per-read costs are the author's measurement and are not re-run here. |
| R603-1-R1 RESIDUE: check numbering | RESOLVED | README "fourteen checks" matches `test_nvm_firmware.py:40-63`. |
| R603-1-S1 wipe while held / R602-1-S3 | RESOLVED | `milan_baremetal.c:1576-1577`, `BAREMETAL_FIRMWARE.md` Boot. `grade_hold_console` checks it, and it is clean in my run. |
| R603-1-S2 console cause on retire paths | RESOLVED | `nvm_held` is set only in `nvm_go_live()` (`:1588`), and `:1944,1982`. Checked over the four `RETIRE_CAUSES`, clean in my run. |
| R603-1-S3 re-stage sequence check unexercised | RESOLVED | `--read-other` cases and `r_restage_any_seq`, caught on three shapes (`gate_selftest.log:87-89`). |
| R602-1-F1 MINOR (Docs, Robustness): length-word faults | RESOLVED | As R603-1-F2. |
| R602-1-R1 to R4 RESIDUE | RESOLVED | `SAVED_STATE_FASTCONNECT.md:785-787` (loss per store); README checks 12-14; `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1655`; README "A single all-`0xFF` read of the valid slot is walked over SKIP 0 to 5." |
| R602-1-S1 read-fault count is a floor | RESOLVED | Documented at `milan_baremetal.c:478-481`. |
| R602-1-S2 every saved record must survive; both-valid layouts | RESOLVED | `test_nvm_firmware.py:682-715`; both-valid cases in `read_fault_cases.py:187-219`. |
| R603-2-F1 MAJOR (Conformance, Tests): re-attach hold unreachable | RESOLVED | `--restart` (`nvm_host.c`, `writer_restart.py`); 26 restart cases. `r_reattach_goes_live` is caught by "yet the writer re-attached live" on three shapes (`gate_selftest.log:90-92`). The "every mechanism" sentence it asked to be made true is untrue again for a different mechanism: see new F1. This is not a retention of R603-2-F1. |
| R603-2-R1 RESIDUE: writer-restart bullet | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:725-729` carries the exact text. |
| R603-2-S1 pin the per-judgement bound | RESOLVED | Exact counts 6 / 5 (`read_fault_cases.py:266-268`). `r_judge_four_tries` is caught by "want exactly" on three shapes (`gate_selftest.log:93-95`). |
| R603-2-S2 held re-attach wording | RESOLVED | `milan_baremetal.c:1700-1701` "re-attached and HELD", graded at `read_fault_cases.py:300-301`. |
| R603-2 OBS-1 / R602-2-S2 prefill fresh read | OUT OF SCOPE, filed | #717 is OPEN. `nvm_prefill_stage()` is unchanged. |
| R602-2-F1 MINOR (Tests, Robustness): re-attach hold unreachable | RESOLVED | As R603-2-F1. |
| R602-2-S1 every-boot hold undocumented | RESOLVED | `BAREMETAL_FIRMWARE.md:2047-2054`. |
| R602-2-R1 RESIDUE: "the hold" twice | RESOLVED | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1655` carries the exact text. |

## Per-lens results

```text
[R603] PASS Conformance - milan_baremetal.c:737-825,1581-1591,1620-1772,1975-1990; KL_nvm_backend.sv:424-582; protocol-processor hdl/aecp/KL_aecp_nvm_writer.sv; #671 body and assignments; receipts/gate_selftest.log - the sequence is derived only in the firmware. No sequence is taken from a refused read: rd.seq is set on VD_OK only (:757-758), and nvm_seq is 0 with no slot accepted (:1673). A slot with no standing verdict holds the writer on both go-live call sites (:1699, :1736). Acceptance 1: check 13's cold and restart cases, both orientations, SEQ 1/0x5A5A5/0x80000000/0xFFFFFFFF and the wrap, are green on 5 shapes. Acceptance 2: restart_at_zero is caught by "was lost on the clean reboot" on three shapes (gate_selftest.log:63-65). Acceptance 3: the diff leaves nvm_commit, the erase, program and verify path, seal and header untouched, checks 1-12 are green, and nvm_cosim is 465/465 with 39/39 mutants killed.
[R603] PASS RTL - KL_nvm_backend.sv and the processor are unchanged by the diff (no hdl/ file in it). Firmware architecture: milan_baremetal.c:415 (the stage holds a 64 KiB slot) against sw/litex/milan_soc.py:3014-3032 (the stage is one 64 KiB erase block). :737-760: the loop is bounded by NVM_SLOT_BYTES, rd.bytes <= NVM_SLOT_BYTES by :651, and indices are unsigned. :1657-1668: the re-pick loop clears one VD_OK per pass, so it ends in at most two. The heartbeat is gated by nvm_retired (:1084). The register map and PP_NVM_STAT layout are unchanged. The capture receipt binds the head firmware sha256 5f174859, and all 96 captures are cycle-identical to round 2 (receipts/capture_r2_vs_head.txt). check_nvm_capture.py PASS.
[R603] MINOR Robustness - milan_baremetal.c:813-825 / read_fault_cases.py:256-268,290 - R603-3-F1. Otherwise examined: reset during activity (the writer restart with the fabric kept, 26 cases); the retire paths (--boot-backend contract|over|live, refused loads); held-writer liveness (probe p_held_heartbeats caught); the both-unread and blank-image path. All clean.
[R603] MINOR Tests - read_fault_cases.py:20-104,120-130,256-301 / test_nvm_firmware.py:629-880 - R603-3-F1. The head grades clean (probe none: 0 findings), and 40 self-test controls redden (gate rc 0). Five independent plants were caught (receipts/probes/*.log). The three re-stage-bound plants were not.
[R603] MINOR Docs - PR #715 body "Round 3" ("Check 13 fails for each of these mechanisms"); README.md:137-138; test_nvm_firmware.py:59-60 - R603-3-F1's coverage claims. Otherwise examined against the code: SAVED_STATE_FASTCONNECT.md:781-800, BAREMETAL_FIRMWARE.md:2015-2059,2163-2174, SAVED_STATE_SNAPSHOT_OWNERSHIP.md:719-729,1619-1667,1808-1820 (every figure matches measurements.json), nvm_cosim/README.md:69-78, and the host README checks 13 and 14 and its controls table. docs_check 0 findings; TOC gate OK; doc style and doc paths rc 0; no U+2014 added.
```

## Reviewer-owned ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #671 body and assignments; `milan_baremetal.c:737-825,1581-1772,1975-1990`; `KL_nvm_backend.sv:424-582`; `KL_aecp_nvm_writer.sv`; `gate_selftest.log`; `nvm_cosim_run.log` | R603-3 | `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08` |
| RTL | CLEAN | no hdl/ change in the diff; `milan_baremetal.c:415,737-760,1084,1657-1668`; `milan_soc.py:3014-3032`; capture receipt and gate | R603-3 | `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08` |
| Robustness | UNCLEAN (F1) | restart, retire, hold-liveness and both-unread paths; the re-stage bound | R603-3 | `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08` |
| Tests | UNCLEAN (F1) | `read_fault_cases.py`, `test_nvm_firmware.py`, `nvm_host.c`, `writer_restart.py`, `nvm_cosim/run_cases.py`; gate and probe receipts | R603-3 | `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08` |
| Docs | UNCLEAN (F1) | PR body; host README; suite docstring; FASTCONNECT 7; BAREMETAL_FIRMWARE Boot and host suite; SNAPSHOT_OWNERSHIP 719-729, 18, 20; cosim README | R603-3 | `fc0c517cd55111d81a9fc2aeaa2edd3a82c9ee08` |

No RESIDUE is carried by this round. SUGGESTION S1 does not affect coverage.

## Executed at this head (local, this clone; Python 3.14.7 with PyYAML 6.0.3; pinned Verilator 5.050, wrapper sha256 `905795b9...`, reports "5.050 2026-07-01 rev v5.050")

| command | result |
|---|---|
| `python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test --jobs 8` | rc 0. "saved-state writer gate: OK across 5 shape(s), and every planted defect reddened". 40 "self-test OK" lines; the eleven #671 controls are each caught on three shapes. |
| `make -C tb/verilator/nvm_cosim run JOBS=4 POOL=4` (pinned Verilator) | rc 0. "465 checks: 465 PASS, 0 FAIL", "39 of 39 mutant(s) killed by their named check", "RESULT: PASS". |
| `python3 -B scripts/check_nvm_capture.py` | rc 0. "PASS: capture census, clocks, both timing arms and receipt agree". Four controls detected. |
| `scripts/compare_capture_receipts.py . 9112a0df fc0c517c` | 96 captures, 0 rows differing; maxima 13.86328 / 3.96548 / 10.43406 ms; ratios as published. |
| `scripts/docs_check.py`; `scripts/gen_toc.py --check` (pinned Markdown environment) | rc 0, "0 finding(s) across 202 md files"; rc 0, "TOC gate: OK". |
| `check_hygiene.py --check`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_doc_style.py`, `check_doc_paths.py` | rc 0 each. |
| `scripts/probe_plants.py` x 12 runs; `scripts/probe_restage_hang.py` | As in F1. |

**Hosted, read only** (`receipts/hosted_check_runs_fc0c517c.tsv`, fetched during this review):

- 18 contexts completed `success`, including `rtl-fast`, `firmware-unit`, `docs-check`, `full-ci-gate`, Yosys shards 0-3/4 and Verilator shards 0, 3 and 4/5.
- Verilator shards 1/5 and 2/5 were `in_progress`.
- "Physical gPTP (nightly and manual)" was `skipped`. A skipped context is not evidence.

**Restore.** I removed the build outputs and caches my runs created: `tb/verilator/nvm_cosim/{build,runs}`, `__pycache__` in this clone, and one `__pycache__` under `protocol-processor/hdl/aecp/desc` written at 04:41 local by the gate. `receipts/restore_verification.txt` then shows:

- HEAD `fc0c517c...`, tree and index-tree `5df4098e...`;
- 0 status lines including ignored files;
- `ls-files -s` equal to `ls-tree -r HEAD` in mode, blob and path;
- 0 worktree blob re-hash mismatches;
- gitlinks `gptp-processor` `5dce647a`, `protocol-processor` `2ad2f845` and `third_party/verilog-axis` `48ff7a7e`, each at its pin and clean;
- `external` and `third_party/lwSRP` uninitialised, as they were at the start.

## Real limits

- Physical calibration NOT RUN; no hardware, bench or field run. Field skips are not hardware proof.
- I did not re-run these, and rely on the author's published receipts or statements:
  - the builder bank (`test_builder.py --require-rv32` / `--require-elaboration`);
  - the Mark II store suite (`test_ctrl_nvm.py`), whose sources the diff does not touch;
  - `fw_service_budget`;
  - the record-space gate;
  - the six-arm capture re-measurement (I checked only the receipt's consistency and the gate);
  - the firmware size with the pinned SDK;
  - the measured per-read boot costs. The 16.4 s / 17.1 s worst-case boot remains an estimate.
- The host read-fault model counts one read per evaluation of `SPIFLASH_BASE`. A fault returning the same wrong bytes twice, an all-`0xFF` slot read twice, and a judgement read answered with the other slot's valid container stay undetectable by design (the stated limit).
- The restart model resets the writer's statics only (obligation O4 assumed).
- No manager source bank ran at this head, and none is claimed.

## Pending manager duties

- Carry R603-3-F1 to the next round. Optional: R603-3-S1.
- Validate the current-dev merge candidate (source base `e8454e27`, live dev `ac2c5e77`) with the builder and native banks, and link the receipts.
- Hosted acceptance: Verilator shards 1/5 and 2/5 were still running at fetch time. Hosted and act acceptance at the final head.
- Confirm #717 stays tracked for the prefill read.

R603-3 FINISHED

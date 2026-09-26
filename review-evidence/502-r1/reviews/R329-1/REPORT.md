[R329] NEGATIVE - exact head 104c8a54b183cd9215ed1e3a2e1be1634f48d33d

Round R329-1, external independent review of kebag-logic/milan-fpga PR #579 for issue #502.
Head `104c8a54b183cd9215ed1e3a2e1be1634f48d33d`, tree `c1d413a847312074618f45635750252aea21e197`.
Base `831f94f4146cc45ec476f8c8dcf5afac7cd8eacf` (live dev at review time).
Commits reviewed: `87e263fd` (implementation on dev `7eb3b0d4`) and `104c8a54` (merge of dev `831f94f4`).

Lenses applied this round: Conformance, RTL, Robustness, Tests, Docs (all five).
Result: RTL is CLEAN. Conformance, Robustness, Tests and Docs are UNCLEAN because of three MINOR findings of this round (R329-F1..F3) and two retained prior Docs MINORs (R328-F2, R328-F3; see "Prior public findings").
The shipping glue does what the decision needs on the path that matters: no status reads durable over a changed name or map. The findings are these:

- an unchanged duplicate map command now sets pending, which only reset clears;
- two plausible trigger regressions survive the committed K12 suite.

## Reconstruction

1. Read AGENTS.md, CONTRIBUTING.md (section 1 reset rule) and docs/README.md.
2. Read issue #502: the body, and comments 5844866872 (decision/scope), 5845129498, 5846418959 (round-2 assignment) and 5847404798 (merge-dev).
3. Read the authorities:
   - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 6.1 and the section 11 table;
   - `docs/design/SAVED_STATE_MATERIALIZATION.md` section 2;
   - the processor top contract at pin `870ff88a` (`protocol-processor/hdl/top/protocol_processor_top.sv:358-375`, `:647-669`);
   - the parent map owner (`hdl/milan/milan_datapath.sv:4229-4420`).
4. Read diff `831f94f4..104c8a54` and both commits.
5. Read the historical K10/K12 evidence at `a21b165a` (`design-evidence/500-materialization/proposal-evidence/harness/d3_cases.cpp:483-511`, `results.txt:754-770`).

Of the published evidence packet at `dc9d0928`, I examined only its manifest (189 author files). Every claim checked below was re-executed independently.
I read prior public review findings on this PR only after this verdict and ledger were written (see "Prior public findings").

## Verification of the assigned questions

### (1) Pending glue, `hdl/milan/KL_pp_shadow.sv:919-952`

**Trigger.**
- `aecp_live_wr_w = aecp_name_wr_w | (amap_edit_req_o && amap_edit_phase_o == 5)` (:941-942).
- A sync-reset sticky latch holds it (:944-950).
- `nvm_pend_w` ORs both the pulse and the history (:952) into `u_nvm.pend_i` (:1018).
- The name export is connected at :1080.

**Timing.**
- The backend registers `pend_i` into `pend_r` on the same `clk_i` edge (`hdl/milan/KL_nvm_backend.sv:755-790`), so the status reads pending immediately after the accepting edge.
- The harness observer checks this after every edge. Mutant M3 (pulse bypass removed) is killed.

**Clock and reset.**
- `KL_pp_shadow` is instanced with `clk_i(axis_clk)` and `rst_n(axis_resetn)` (`milan_datapath.sv:7420-7421`).
- The processor and backend share `clk_i`/`rst_n` inside the shadow. The statement "All three events and the backend use clk_i and the shared rst_n. No CDC is introduced" is correct.
- The new latch uses a synchronous active-low reset. That is the CONTRIBUTING section 1 rule and matches the backend; the old mark latch was asynchronous.

**Name pulse.**
- `name_wr_o = take_wr_w && st_name_i` is the same enable that writes the name RAM (`protocol-processor/hdl/aecp/KL_aecp_desc_store.sv:457`, `:545`).
- It is combinational to the top (`protocol_processor_top.sv:3470`).
- The processor HDL delta `0922e434..870ff88a` is only this export.

**Map pulse.**
- Phase 5 is the phase in which the parent writes the map store, and only for a record that differs (`milan_datapath.sv:4337-4389`).
- Phase 5 follows only an accepted phase 1 and cannot stall (top contract :358-364).

**Mark.**
- The mark is kept (`unused_aecp_marks_w`, :937-938) and no longer drives pending.
- Its completion meaning is documented. The harness grades the mark group and that the mark follows the first write.

**Unchanged and refused commands.**
- These raise nothing:
  - an unchanged SET_NAME (K10 unchanged, `sim_main.cpp:1390`);
  - a zero-record map command (:1417);
  - a static-output refusal (:1410);
  - a dynamic ADD refused at record validation (reviewer probe P2: status 7, pend 0).
- **Exception:** an unchanged duplicate ADD from a durable baseline does raise sticky pending (probe P3). See R329-F3.

### (2) K10/K12 in `tb/verilator/pp_shadow`

**What the harness does.**
- Real AECP frames run through the shipping datapath.
- Observation is read-only: `public_flat_rd` probes (`pending_probes.vlt`) are sampled before and after each edge in `hi()` (`sim_main.cpp:283-314`, `:518`). No signal is forced.
- It covers:
  - both port directions (STREAM_PORT_INPUT 0xe and STREAM_PORT_OUTPUT 0xf on the dynamic fixture);
  - reset;
  - the durable baseline (`pending_boot`, :1298-1320);
  - a snapshot ARM/ATTEST/ACK.

**My reruns.**
- `make run-pending`: 159 checks, 0 failures (`receipts/run-pending.log`).
- `make -C tb/verilator/pp_shadow`: 520 + 520 + 520 + 159 checks, 0 failures (`receipts/pp_shadow-default.log`).
- `make pending-mutant`: the clean control passes. The late-mark mutant fails both named checks (`receipts/pending-mutant.log`):
  - K10: 0x759 = 1881 falsely-durable cycles;
  - K12: 0xF = 15 falsely-durable cycles per map direction;
  - final line: `PASS: late-mark mutant killed by K10 and K12; clean control passes`.

**Reviewer mutant campaign** (`scripts/r329_mutants.py`, raw results in `receipts/mutants/RESULTS.txt`). Leg "dyn" is `run-pending`; leg "static" is `run-base --pending-only`.

| mutant | dyn | static | verdict |
|---|---|---|---|
| control | PASS 159/0 | PASS 118/0 | - |
| M1 drop map class | FAIL 26 | FAIL 13 | killed |
| M2 drop name class | FAIL 9 | FAIL 9 | killed |
| M3 delay one cycle (no pulse bypass) | FAIL 16 | FAIL 10 | killed (durability + accepting-edge checks) |
| M4 wrong phase (2) | FAIL 4 | FAIL 2 | killed, only by the zero-record control's sticky check |
| M5 early phase (4) | PASS | PASS | **survives** (R329-F2) |
| M6 add-only (ignores REMOVE) | PASS | PASS | **survives** (R329-F1) |
| M7 no sticky history | FAIL 35 | FAIL 22 | killed |
| M8 input ports only | FAIL 13 | PASS | killed by the dyn leg |
| M9 any phase | FAIL 4 | FAIL 4 | killed |
| M10 late mark (lane mutant, re-derived) | FAIL 16 | FAIL 10 | killed |

The shipping source sha256 `6a0090d8...` was identical before and after the campaign.

**Reviewer probe** (`scripts/r329_probe.py`, receipts in `receipts/probe/*.log`).
- It derives a harness copy in the disposable tree and runs it on the dynamic fixture.
- It preloads input port 0 cluster 0 through the firmware channel-map CSR, so the mapping exists while the status reads durable.
- On the shipping head (189 checks, 0 failures):
  - P1 (REMOVE from a durable baseline) passes, with pending from the accepting edge.
  - P2 (refused ADD) passes, with pending clear.
  - P3 observed `duplicate ADD status 0, phase-5 records 1, marks 0, mappings after 1, PP_STAT[11] pend 1, durable 0`.
- Against the surviving mutants:
  - M6 fails P1 with 0x605B = 24667 falsely-durable cycles;
  - M5 fails P2's sticky checks.

### (3) Pin and ROM ledger

**Pin and ledger rows.**
- `protocol-processor` gitlink = `870ff88ad35bbd532244e4c7e6d7661b9f6e1366`; `0922e434` is an ancestor.
- `syn/yosys/rom_digests.tsv:27-28` holds the `870ff88a` rows.
- The `0922e434` rows (:7-8) and the `990f9652` rows are retained.

**Re-record.**
- `syn/yosys/ooc.sh --record-rom-digests`, rerun in a disposable copy, left the ledger byte-identical (`git diff --exit-code` clean; `receipts/rom-record.log`).
- The generated images match the recorded digests: ucode `23605682...`, ltn `23cc67ee...`.

**Diagram and manifest.**
- `docs/diagrams/submodule_boundaries.gen.py` in write mode reproduced the committed `.drawio`, `.svg` and `.png` byte-for-byte (`receipts/diagram-regen.log`, no diff).
- The `PNG_MANIFEST.json` `source_sha256` `255646cb...` equals the drawio's sha256.
- `check_diagram_pngs.py` and `submodule_boundaries.gen.py --check` pass.
- I checked the rendered PNG visually: it shows `pin 870ff88ad35b`.
- `check_submodule_docs.py` passes (4 exact gitlinks).

### (4) Firmware, CSR and area

**No firmware or CSR change.**
- `git diff 831f94f4..104c8a54 -- sw hdl/common/csr configs` is empty, and so is the same diff over `7eb3b0d4..87e263fd`.
- The `sw/firmware/milan_baremetal/milan_baremetal.c` blob is `a4e560fb...` at 7eb3b0d4, 831f94f4 and 104c8a54.
- Its sha256 `0bf43cd4...` equals `product_firmware_sha256` in `tb/verilator/nvm_capture_cpu/measurements.json`.
- `scripts/check_nvm_capture.py` passes (`receipts/check_nvm_capture.log`). No re-measure is required.

**Area** (single-top OOC run `ooc.sh KL_pp_shadow`, Yosys 0.66; `receipts/ooc-{base,head}-KL_pp_shadow.log`):

| tree | LUT | LUTRAM | FF | RAMB36 | RAMB18 | DSP | CARRY4 |
|---|---|---|---|---|---|---|---|
| base `831f94f4` (pin `0922e434`) | 60855 | 6136 | 30187 | 15 | 4 | 6 | 2104 |
| head `104c8a54` | 60766 | 6136 | 30187 | 15 | 4 | 6 | 2104 |

The delta is -89 LUT with every other column identical. This matches the reported figure.

### (5) Merge commit `104c8a54`

**Re-merge.** I re-merged `831f94f4` into `87e263fd` in a disposable clone. It conflicts only in:
- `CHANGELOG.md`;
- `PNG_MANIFEST.json`;
- `submodule_boundaries.{drawio,png,svg}`;
- `SUBMODULES.md`;
- the `protocol-processor` gitlink.

Every auto-merged path is identical to `104c8a54`, including `rom_digests.tsv`, `scripts/act_ci.py`, `docs/testing/CI_WORKFLOWS.md` and `tb/verilator/milan_dp/README.md`.

**Conflict resolutions.**
- CHANGELOG: the #502 entry is byte-identical to `87e263fd`, and dev's entries are intact.
- SUBMODULES.md keeps #567's text and names `870ff88a` as current.
- The gitlink stays at `870ff88a`.
- The diagram set is regenerated, per (3).

The merge introduces no other change.

### (6) Repository gates

All of these exited 0 in a disposable copy at the head (`receipts/gates.log`, `receipts/gates-venv.log`):
- `git diff --check 831f94f4 104c8a54`
- `docs_check.py`
- `check_em_dash.py --base 831f94f4`
- `check_doc_style.py`
- `gen_toc.py --check` and `gen_toc.py --verify-anchors`
- `check_doc_paths.py`
- `docs/traceability/gen_module_matrix.py --check`
- `check_rtl_source_lists.py`
- `check_sv_idiom.py`
- `lint_rtl.py --check`
- `check_cpp_idiom.py`
- `check_py_idiom.py`
- `check_port_contracts.py`
- `measure_naming.py --check`
- `measure_test_evidence.py --check`
- `ci_events.py --check`
- `xvlog_gate.py --check`
- `check_submodule_docs.py`
- `check_diagram_pngs.py`
- `submodule_boundaries.gen.py --check`

Three of them first refused for environmental reasons: em-dash and gen_toc lacked the pinned Markdown renderer, and my module-matrix invocation used the wrong path. I reran them in a private venv built from `tools/markdown/requirements.txt --require-hashes`, and they passed.

## Findings

### R329-F1 MINOR - Tests, Robustness - `tb/verilator/pp_shadow/sim_main.cpp:1429-1431` - K12 REMOVE (and duplicate) legs cannot fail

**Authority/evidence.**
- Issue #502 requires a changed map to be tracked "from their first accepted live write". AGENTS section 6 (Tests) requires that each test can fail for the defect it claims to detect.
- The K12 duplicate and remove reports run in the same boot as the ADD at :1420. By then pending is already sticky, so their `no_durable_claim_over_unsaved` and `pending_from_accepting_edge` checks are vacuous.
- No REMOVE is ever observed from a durable baseline.
- Mutant M6 gates the map trigger on `!amap_edit_remove_o` and passes the whole committed suite (dyn 159/0, static 118/0).
- Reviewer probe P1 (REMOVE of a CSR-preloaded mapping from a durable baseline) kills M6 with 24667 falsely-durable cycles.
- The PR body's testing text and `tb/verilator/pp_shadow/README.md` ("then adds and removes") imply REMOVE coverage.

**Impact.** A regression that drops removals from the pending source would ship green. The status would then read durable over a removed live mapping, which is exactly the defect class of #502.

**Required outcome.** The committed suite contains a REMOVE of a present mapping, started from a durable baseline, whose named durability or accepting-edge check fails when removals do not raise pending.

**Verification.** Run `scripts/r329_mutants.py <tree> <out> M6_add_only`: M6 must be killed by a named K12 check, and the shipping head must still pass.

### R329-F2 MINOR - Tests, Robustness - `tb/verilator/pp_shadow/sim_main.cpp:1405-1418` - no control for a map command refused at record validation

**Authority/evidence.**
- Frozen scope 5844866872 item 2 says to keep the unchanged-command controls. The assigned verification says refused edits raise nothing.
- The only refusal control is "K12 static output refused" (:1410). It is refused before any record phase and runs only in the non-dynamic builds.
- On the dynamic owners, no command is refused at record validation (phase 4).
- Mutant M5 moves the map trigger to phase 4, so it sets pending on records that are then refused. It passes the committed suite (dyn 159/0, static 118/0).
- Reviewer probe P2 (ADD with stream_index 7, status 7) kills M5: the sticky-pending checks read 1 against an expected 0. The shipping head passes P2.
- `SAVED_STATE_MATERIALIZATION.md:235` and the PR body say "Controls cover ... refused output edits". That is true only for the static refusal.

**Impact.** A mis-phased trigger would ship green, and with it a refused command would revoke durability for the rest of the power cycle.

**Required outcome.** A committed control issues a map command to a dynamic owner that is refused at record validation, from a durable baseline, and requires pending to stay clear.

**Verification.** M5 must be killed by the committed suite, and the shipping head must still pass.

### R329-F3 MINOR - Conformance, Tests, Docs - `hdl/milan/KL_pp_shadow.sv:941-942,932` - an unchanged duplicate map command sets pending until reset

**Authority.**
- Issue decision 5844866872 says pending sources "rise on the first accepted live write".
- Scope item 2 says to keep the unchanged-command control.
- `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 6.1 defines bit [11] as "accepted work that no verified slot holds".

**Evidence.**
- Phase 5 is offered for every validated record. The parent writes the map only when the record differs (`milan_datapath.sv:4337-4389`), and the processor emits no class-6 mark for an unchanged record.
- Reviewer probe P3 preloads a mapping (status durable), then sends an ADD of the same mapping. Result: status SUCCESS, one phase-5 record, 0 marks, map unchanged, `PP_STAT[11]=1`, durable 0.
- Because the source is sticky and has no writer, pending then stays set until reset, over a map that did not change.
- At base `831f94f4` this command raised nothing, because no class-6 mark was emitted. This is therefore a new false-pending path. The name group has no equivalent, because unchanged lanes do not pulse.

**Where it is and is not disclosed.**
- The RTL comment (:932), section 6.1 and the materialization page describe the behaviour as "conservative".
- The frozen map "unchanged" control is a zero-record command, which never reaches phase 5. The behaviour is therefore untested from a durable baseline.
- The PR body and the REVIEW READY evidence say "Controls cover unchanged and repeated commands" without stating this exception.
- It was not raised on the issue as an open question or decision (AGENTS section 2).

**Impact.**
- A controller that re-applies an existing mapping, such as a preset replay, makes the device report unsaved state for the rest of the power cycle, though nothing is unsaved and nothing can clear it.
- This is not a false durable claim, so it is not a BLOCKER.
- It is a regression in the status' meaning, and it departs from the unchanged-command control the scope keeps.

**Required outcome.** Either:
- (a) raise the map source only for a record the parent actually writes, so that an unchanged duplicate raises nothing, and add a durable-baseline duplicate control asserting that pending stays clear; or
- (b) publish the conflict on #502 and record a maintainer decision that accepts the conservative over-report. Then make the section 6.1 bit definition, the PR/issue evidence, and a committed durable-baseline duplicate control all state and assert the accepted behaviour.

**Verification.** Re-run probe P3 (`scripts/r329_probe.py`), or the committed equivalent, with the expected result of the chosen option.

There is no BLOCKER or MAJOR finding.

## Clean-lens evidence

`[R329] PASS RTL - hdl/milan/KL_pp_shadow.sv:919-952,1018,1080 @104c8a54 - trigger, latch, pend_i bypass and clock/reset checked against KL_nvm_backend.sv:755-790, milan_datapath.sv:7420-7421 and processor top :647-669. Synchronous reset per CONTRIBUTING section 1; no CDC; the widths are correct (3'd5 against the [2:0] phase). OOC: -89 LUT, no other resource change. Mutants M1-M4 and M7-M10 are killed.`

## Completion ledger (reviewer-owned)

| lens | status | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R329-F3) | issue #502 decision/scope comments; `KL_pp_shadow.sv:919-952`; processor top contract :358-375, :647-669; `milan_datapath.sv:4229-4420`; probes P1-P3 | R329-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |
| RTL | CLEAN | `KL_pp_shadow.sv:919-952,1018,1080`; `KL_nvm_backend.sv:755-790`; `milan_datapath.sv:7420-7421`; `KL_aecp_desc_store.sv:457,545`; OOC base/head logs; mutant campaign | R329-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |
| Robustness | UNCLEAN (R329-F1, R329-F2) | reset/baseline `sim_main.cpp:1298-1320,1433-1434`; refused/duplicate/remove paths; probes P1-P3; mutants M5, M6 | R329-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |
| Tests | UNCLEAN (R329-F1, R329-F2 = R328-F1, R329-F3) | `sim_main.cpp:260-314,518,1252-1435`; `Makefile`; `pending_mutant.py`; `pending_probes.vlt`; `fixtures/pending.yaml`; default-run and pending-mutant receipts; 11-entry mutant campaign | R329-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |
| Docs | UNCLEAN (R329-F3; retained R328-F2, R328-F3) | `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 6.1, section 11 row, D2 notes; `SAVED_STATE_MATERIALIZATION.md:125-144,218-238,474-478`; `TESTING.md:259-275`; `pp_shadow/README.md`; `CHANGELOG.md`; `SUBMODULES.md`; diagram set/manifest (regenerated byte-identical); PR body | R329-1 | 104c8a54b183cd9215ed1e3a2e1be1634f48d33d |

## Prior public findings

The only prior review on this PR is R328-1 (PR comment 5848360185, NEGATIVE at this same head). I read it after the verdict and ledger above were written. I re-checked each of its items at `104c8a54`:

**R328-F1 (MINOR, Tests): RETAINED.**
- It is the same defect as R329-F2 and was found independently: my M5 (phase-4 trigger) survives, and probe P2 kills it.
- I additionally attribute it to Robustness (refused input).

**R328-F2 (MINOR, Docs): RETAINED, confirmed at this head.**
- Stale mark-trigger text remains in `docs/design/SAVED_STATE_MATERIALIZATION.md`:
  - section 1 (:127-131) still says `pend_i` includes "a sticky bit a class-6 or class-7 commit mark sets (`hdl/milan/KL_pp_shadow.sv` lines 935 to 946)";
  - the table rows at :142-143 still read "the class-6 commit mark" and "the class-7 commit mark";
  - :476 still names `aecp_mark_pend_r`, which no longer exists (the head register is `aecp_live_pend_r`).
- My own Docs pass missed these; I confirm them.
- Docs stays UNCLEAN.

**R328-F3 (MINOR, Docs): RETAINED, confirmed at this head.**
- The explicit campaign table in `docs/testing/TESTING.md:265-273` does not list `make -C tb/verilator/pp_shadow pending-mutant`.
- Nothing outside `tb/verilator/pp_shadow/{README.md,Makefile}` invokes it. `scripts/measure_test_evidence.py:600` carries only its disposition.

**R328-S1 (SUGGESTION, Conformance/Robustness): RETAINED AND RAISED to MINOR as R329-F3.**
- The R328 text notes that the behaviour follows the assignment's trigger choice and is disclosed. I agree it is disclosed in the docs.
- I raise the severity for three reasons:
  - it contradicts the frozen unchanged-command control and the section 6.1 bit definition ("accepted work that no verified slot holds");
  - it is a new false-pending path relative to base, with no clearing mechanism;
  - the PR and REVIEW READY evidence claim unchanged and repeated commands are controlled, and the conflict was not published for a decision.
- Probe P3 executes the durable-baseline scenario that R328 notes the harness cannot show.

**R328-S2 (SUGGESTION, Tests): RETAINED as SUGGESTION.**
- I agree the observer defines "unsaved" from the export signals.
- The name pulse is structurally the RAM write enable (`KL_aecp_desc_store.sv:545`), and the parent map store is written in phase 5 (`milan_datapath.sv:4337-4389`). So at this pin there is no gap.

**R329-F1 (REMOVE never observed from a durable baseline; M6 survives) is not in R328.** It is new in this round.

Combined open set at this head:
- MINOR: R329-F1, R329-F2/R328-F1, R329-F3, R328-F2, R328-F3.
- SUGGESTION: R328-S2.

## Real limits

- **Simulator path.** The assigned path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` does not exist. I used a private copy of the identical wrapper from `$VALIDATION_STORAGE/372-manager-r2/pinned-tool-bin/verilator`. It reports `Verilator 5.050 2026-07-01 rev v5.050`, and all 150 pinned wrappers point at the same overlay binary (`verilator_bin` sha256 `44898b22...`).
- **Not run:**
  - the full parent/PP/gPTP/Yosys/builder banks;
  - `nvm_cosim` and `nvm_backend`;
  - behave;
  - the no-git docs mode;
  - act and the hosted contexts.
- **OOC scope.** Only the single-top OOC measurement of `KL_pp_shadow` was run, at base and head.
- **Capture gate.** It was checked, not re-measured.
- **Hardware.** No hardware or physical calibration was run. Skipped field campaigns are not hardware proof.
- **Out of scope.** The firmware channel-map CSR path writes the live map without an AECP command and raises no pending. This is pre-existing and firmware-owned, not a #502 finding.

## Clone integrity

- All builds, mutants and probes ran in disposable copies under the packet's `scratch/`. The review clone was never edited.
- `scripts/r329_restore_check.sh` (`receipts/restore-check.log`) confirms the clone: RESULT OK. It checked:
  - HEAD and tree are exact;
  - index equals HEAD and worktree equals index (bytes and modes);
  - there are 0 untracked or ignored entries;
  - every tracked blob rehashes to its index id;
  - the gitlinks `protocol-processor@870ff88a`, `gptp-processor@5dce647a` and `third_party/verilog-axis@48ff7a7e` are recorded, checked out, and clean.

## Pending manager duties

- Hosted/act acceptance at the exact head.
- Validation of the final current-dev candidate merge.
- Disposition of R329-F1..F3 and the retained R328-F2/F3: an executor fix, or for R329-F3 a maintainer decision under option (b).
- A re-review covering Conformance, Robustness, Tests and Docs at the corrected head.

R329-1 FINISHED

[R439] NEGATIVE - exact head 3370c6cbd5e4b096167c19ca709556a40207e538

# R439-1: external review of milan-fpga issue #635 / PR #636

- Head `3370c6cbd5e4b096167c19ca709556a40207e538`, tree `c7ef42fb98b23ea0a00db283f3e6ea0ba17745e5`: twelve single-parent, one-line commits on dev `cdf49d1a28527562888f0a903de51b6b15b1244f`. At review time, live remote `dev` was still `cdf49d1a` and the remote branch head was `3370c6cb`.
- Scope was reconstructed from public material only:
  - AGENTS.md, CONTRIBUTING.md and docs/README.md;
  - the #635 body (frozen acceptance 1 to 5), the assignment (comment 5958619779), TAKEN (5958652460), REVIEW READY (5962152491) and the PR #636 body;
  - the author packet at `ecc18462` (`review-evidence/635-r1`: MANIFEST.json, HANDOFF.md, PR-BODY.md and the patch, whose sha256 `67bcd698...7bd7c` matches the published value);
  - the merged processor PRs #135 to #140 and #142 and their parent-visible lists.
- **Why NEGATIVE:** one MINOR is open (F1, Docs and Conformance). It was first raised by the concurrent internal round R438-1. This round read that report only after its own independent pass was complete, checked the finding again at this head, and found it valid, so F1 stays open (see "Concurrent public findings").
- **What holds:**
  - the pin;
  - the byte-exact patch application;
  - every generated record, reproduced through its generator;
  - the capture gate;
  - the RTL tie-off;
  - the three disclosed deviations.
- **Other findings:** three RESIDUE items (wording only) and one SUGGESTION. None of them gates the verdict.

## Findings

### F1 - MINOR - Docs, Conformance - `CHANGELOG.md:45`, `docs/reference/SUBMODULES.md:114-115` - C5a's NOT_IMPLEMENTED echo for a non-AEM command whose response memory fails is not recorded

- **Origin:** concurrent round R438-1, finding F1 (issue #635 comment 5962667464). Checked again independently at this head and kept open. This round's own pass missed it.
- **Authority:**
  - Acceptance 5: "Each processor change the parent can observe is recorded where the parent documents it", naming "the AECP deadline and hazard faces".
  - Processor PR #140's round-2 parent-visible list: "a command of any AECP message type but AEM_COMMAND, whose response memory fails or which is preempted past its deadline, answers NOT_IMPLEMENTED with the command echoed".
- **Evidence** (`receipts/concurrent_F1_verification.txt`):
  - At `b2db3a97`, processor `docs/guides/operator.md:54` reads "Anything, while the response memory is broken: a well-formed 60-byte `ENTITY_MISBEHAVING`".
  - At `631eeb34`, `:55` adds "or, for a command that is not an AEM command (a Milan Vendor Unique one), `NOT_IMPLEMENTED` with the command echoed". `:326` names this as GET_MILAN_INFO's fault answer.
  - The parent records only the deadline arm. `CHANGELOG.md:45` reads "Non-AEM messages on that path answer NOT_IMPLEMENTED, echoed", where "that path" is the 100 ms deadline. The C5a rows of `SUBMODULES.md` cover the deadline and the hazard classes only.
  - The parent's response-memory section, `docs/reference/REGISTER_MAP.md:2357-2358`, is keyed on "the entity answers `ENTITY_MISBEHAVING`".
- **Impact:** under a response-memory bridge fault, a controller's GET_MILAN_INFO now answers NOT_IMPLEMENTED, where it answered ENTITY_MISBEHAVING at the previous pin. The parent's record of this adoption does not say so. Acceptance 5 is therefore not fully met, although the PR body claims it is met.
- **Required outcome:** where the parent records the C5a deadline arm (the `631eeb34` CHANGELOG section and the SUBMODULES parent-observable table), also record this: a non-AEM command, GET_MILAN_INFO among them, answers NOT_IMPLEMENTED with the command echoed when its response memory fails. At `b2db3a97` the answer was ENTITY_MISBEHAVING. A pointer from the REGISTER_MAP memory-bridge section is optional.
- **Verification:**
  - The new text matches processor `operator.md:55` and `:326` at `631eeb34`.
  - `scripts/docs_check.py`, the added-line em-dash gate, `scripts/check_submodule_docs.py` and the docs workflow stay green at the new head.
  - A re-review covers Docs and Conformance at that head.

### F2 - RESIDUE - Docs - `CHANGELOG.md:43-44` - the deadline-answer summary is broader than the behaviour

- **Evidence:**
  - `CHANGELOG.md:44` says a command past its deadline answers "ENTITY_MISBEHAVING unless a refusal was chosen".
  - Processor `hdl/aecp/KL_aecp_engine.sv:1723-1737` and `operator.md:56` at `631eeb34` add two cases. A command that has already changed state is not preempted and answers for itself (PR #140's DL section: "A SET_NAME past its name write answers its own SUCCESS"). The registry and map-edit commands run to their own END.
  - Those commands behaved the same way at `b2db3a97`, so no parent-observable change goes unrecorded. Only the summary sentence is too broad.
- **Exact fix** (best made in the same edit as F1): "Its answer is ENTITY_MISBEHAVING unless a refusal was already chosen; a command that had already changed state answers for itself."

### F3 - RESIDUE - Docs, RTL - `hdl/milan/KL_pp_shadow.sv:1099` - a bare `#80` names a processor issue

- **Evidence:**
  - In this repository, `#80` resolves to milan-fpga #80, "Fix optional tsn_fuzz CI accounting".
  - The ruling the comment means is on processor issue #80 (protocol-processor #80 comment 5915765717).
  - The line is byte-identical to the supplied patch, which the assignment required to be applied as-is. The comment does not affect code behaviour.
- **Exact fix:** `//! wired to identify_button_i (processor lane C6, manager ruling on protocol-processor #80)`.
- **Concurrence:** R438-1 S1 reports the same point as a SUGGESTION.

### F4 - RESIDUE - Docs - `docs/reference/SUBMODULES.md:114-115` - the scoreboard kill tie-offs are paired with the hazard row instead of the deadline row

- **Evidence:** at `631eeb34`, `protocol_processor_top.sv:1022-1025` drives the scoreboard's `kill_valid_i`, `kill_id_i` and `kill_resp_queued_i` from the AECP deadline block (`aecp_dl_kill_w`, `aecp_dl_queued_w`). Rule (e) is the deadline kill, not the hazard classifier.
- **Exact fix:**
  - Row "C5a answers an AECP command still running 100 ms after reception": "No top port or parameter; its kill ports stay inside the processor, and the three scoreboard kill tie-offs left the processor top".
  - Row "C5a serializes AECP and ACMP work by hazard class": "No top port or parameter".

### S1 - SUGGESTION - Docs - `docs/reference/REGISTER_MAP.md:1016` - the `ADP_IDX0[15:0]` description predates C3's fallback meaning

- **Evidence:**
  - At `631eeb34` the ADPDU index is `aecp_cur_cfg_v_w ? aecp_cur_config_o : current_cfg_i` (`protocol_processor_top.sv:1860-1862`).
  - The overlay becomes valid on any write to the configuration row (`KL_aecp_engine.sv:1918-1929`), that is, a SET_CONFIGURATION or a D3 restore.
  - The parent drives `current_cfg_i` from `ADP_IDX0[15:0]`, which resets to 0 (`milan_csr.sv:2831`, `milan_datapath.sv:7611`). No firmware writes it (`receipts/parent_binding_checks.txt`).
  - The image declares one configuration (`avdecc/aem_descriptors.py:217`), so 0 is the only valid value, and at 0 the wire is unchanged. The row is therefore exact for every valid use.
- **Optional fix:** "`[15:0]` current_configuration_index the ADPDU carries until a SET_CONFIGURATION or D3 restore writes the processor's configuration row (from processor pin `631eeb34`)".
- This is the same semantic point as the `KL_pp_shadow` `current_cfg_i` comment rewording that the manager routed to #495, and it belongs with that item.

## What was checked, per question

1. **The only processor change is the gitlink** (`receipts/pp_history.txt`).
   - `14f8c27f` changes only the `protocol-processor` gitlink, from `b2db3a97` to `631eeb34`. No other base..head entry falls under the path, and the submodule checkout is clean.
   - `b2db3a97` is an ancestor of `631eeb34`. The first-parent history is exactly seven merges: #136 `0451d83d`, #135 `d5f73bac`, #137 `3f3ea56b`, #138 `16ea10ac`, #140 `03c842a7`, #139 `2ebd4fe8` and #142 `631eeb34`.
   - Upstream records each of these as merged with that merge commit, and the second parents equal the PR heads.
   - No PR #141 exists; issue #141 is closed and was implemented by #142. The issue body's "C2 — " is #135, which the author disclosed.
   - Processor `main` is now 20 commits past `631eeb34` (lane C8 and others). That is outside the frozen scope, and the pin is an ancestor of `main`.
2. **The patch is applied as three commits that together equal it byte for byte** (`receipts/patch_equality.txt`).
   - `git apply` of the published patch on the base files yields blobs `46f3faf8` (KL_pp_shadow.sv) and `b33d91c6` (measure_test_evidence.py). These equal both `927428d16` and the head.
   - The patch-id of `14f8c27f..927428d1` equals the patch file's (`79127757...`).
   - Each commit carries one concern, and no later commit touches either file.
   - **Port and parameter diff of `protocol_processor_top`** (`scripts/top_iface_diff.py`, `receipts/top_iface_diff.txt`): 36 -> 37 parameters and 211 -> 212 ports. The only additions are `parameter bit EN_IDENTIFY_NOTIF_P` (default `1'b0`) and `input wire identify_button_i`. No existing declaration line changed.
   - **Meaning changes in the header:**
     - `current_cfg_i` becomes the fallback (S1). The wire is unchanged at the parent's only valid value.
     - `DESC_LINE_BYTES_P` gains an enforced 576..1008 range in steps of 8 (`KL_aecp_engine.sv:945-966`), and the parent binds 576 (`milan_datapath.sv:330`).
     - `RESP_BASE_P`'s reservation stays 16 + 576 = 592 bytes.
     - `cfg_maap_internal_i` stays tied to 0 (`milan_datapath.sv:7782`), so C2's engine is inactive.
   - `identify_button_i` is read only inside `KL_aecp_notify` `gen_ident` and the top's `gen_uns_departure`, both under `if (EN_IDENTIFY_NOTIF_P)` (`KL_aecp_notify.sv:709`, `protocol_processor_top.sv:4484`). So "never read while EN_IDENTIFY_NOTIF_P is 0" is true.
   - The tie-off is consistent with Milan v1.2 5.4.5.4 (a SHOULD, user-originated) and IEEE 1722.1-2021 7.5.1. The parent compliance matrix already records 5.4.5.4 as "n/a as a gap" (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:145`).
3. **Every pin-derived record re-run through its generator** (`scripts/regen_compare.sh`, `receipts/regen/`). Each of these rewrote a byte-identical file (`git diff --exit-code` rc 0, then restored):
   - `syn/yosys/ooc.sh --record-rom-digests`;
   - `docs/diagrams/submodule_boundaries.gen.py` (write mode; porcelain clean);
   - `check_port_contracts.py --write-budget`;
   - `measure_naming.py --write-budget`.

   Further checks:
   - **ROMs:** running the two ROM generators on their own (`receipts/batch1/roms/`) gives `ltn_rom.hex` `23cc67ee...e956` (equal to the `b2db3a97` row) and `ucode.hex` `518b900c...37f8`.
   - **Base measurement** (`scripts/base_measure.sh`, `receipts/base_*.log`, `*.regen`): run at base parent `cdf49d1a` with processor `b2db3a97`.
     - The base already measured hdl 1916, gptp 125, processor 1747 ports, 62 without a rationale, and naming 96 (processor 22).
     - So the moved header lines for hdl, gptp and naming (95/21 -> 96/22) were stale comment lines at the base, not effects of this pin.
     - The pin's real effects are processor ports 1747 -> 1757 and the three kill-face rows leaving (62 -> 59). The commit messages and PR body attribute these correctly.
   - **SUBMODULES.md:** hand-edited in the same form as the earlier adoptions, and `check_submodule_docs.py` passes.
4. **Capture gate** (`receipts/batch1/nvm_capture.log`, `receipts/parent_binding_checks.txt`).
   - `check_nvm_capture.py` rc 0, with all seven controls detected.
   - The census equals the receipt: 8x8 12,634 B / 156 records; 1x1 TDM8 3,218 B / 53 records.
   - Firmware `milan_baremetal.c` sha256 `a73ecc25...0eb3` equals `product_firmware_sha256`.
   - The processor's NVM path (`hdl/packet_engine/`) is byte-identical between the pins.
   - The receipt's `processor_pins` value `b2db3a97` is provenance. No documented trigger requires a re-measure.
5. **What the parent records as observable** (`receipts/processor_source_checks.txt`).
   - The SUBMODULES lane table matches the processor merges.
   - The `MEDIA_CLOCK_FOLLOWING.md` status matches the processor at `631eeb34`:
     - D3C1 to D3C4 are in `tb/pp_top`;
     - there are six D3C mutants (four `clks_*` in `d3_mutants.py`, plus `sclks-bound-three` and `sclks-bound-inclusive` in `aecp_dispatch_mutants.py`);
     - #142's only `hdl/` change (`2ebd4fe8..631eeb34`) is the `gen_ucode.py` comment;
     - `gen_ucode.py:1654-1663` is the range-check comment and `:1674-1711` is `place(E_SCLKS ...)` through the end of `place(E_SCLKSRF ...)`.
   - These CHANGELOG lines match the processor PRs' final parent-visible lists: C5b's locked refusals carrying the value in force, GET_AUDIO_MAP 63 to 71 records (`GAMAP_PAGE_MAX_C = 71`), C6's 84-byte unsolicited SET_STREAM_INFO, and VERSION `0x0002_0060` (`milan_csr.sv:200`).
   - Processor diagram 21 has no parent copy; the only parent reference is a pinned link in a historical plan.
   - Gaps: F1 (MINOR), plus the F2 and F4 wording.
6. **Disclosed deviations and the manager's rulings.**
   - **xvlog re-run alone:** reproduced. `xvlog_gate.py --check` rc 0, 4 findings == ratchet, 0 in `hdl/` (`receipts/xvlog_gate.log`, 150 s).
   - **Sweep relaunch after nohup:** reproduced. `scripts/test_suite_cancellation.py` passes plain (rc 0) and fails under `nohup` (rc 1, the hard-HUP control times out after 12 s), because it kills its probes with SIGHUP (`:311-316`), which an inherited nohup ignore defeats (`scripts/cancel_nohup.sh`, `receipts/cancel_*.log`). So the first attempt's rc 2 was environmental.
   - **act self-test from the audited install:** accepted. `scripts/act_ci.py` is unchanged on the branch, with sha256 `79579e6b...38f8` at head.
   - **Rulings, taken as stated in the assignment:**
     - `test_evidence.budget` stays at 77 while the ratchet reads 72; a ratchet tightens in its own lane.
     - The stale `milan_dp_gptp` README figure predates the lane and goes to #495.
     - The two processor suggestions go to #495.

     None of these is a finding.

## Fault and mutation probes

Scripts: `scripts/probe_tieoff.sh` and `scripts/probe_dispositions.sh`. Logs: `receipts/probes/`. Each probe edited one tracked file in the clone, ran the gate, and restored the file.

| Probe | Gate | Result |
|---|---|---|
| drop `.identify_button_i (1'b0)` and its rationale | `lint_rtl.py --check` | rc 1, NEW PINMISSING `identify_button_i`: DETECTED |
| same | `check_port_contracts.py` | rc 0 (an absent pin is lint's to catch) |
| drop the `//!` rationale above `identify_button_i` | `check_port_contracts.py` | rc 1, UNJUSTIFIED CONNECTION `u_pp.identify_button_i`: DETECTED |
| drop the `//!` rationale above `EN_IDENTIFY_NOTIF_P` | `check_port_contracts.py` | rc 0: parameter bindings are outside the inventory, and the bound value equals the default |
| drop the `acmp_mutants.py` disposition | `measure_test_evidence.py --check` | rc 1, 1 unexplained DUT-source reader: DETECTED |
| drop the `notify_mutants.py` disposition | same | rc 1: DETECTED |

Both new disposition texts match the drivers. `acmp_mutants.py` and `notify_mutants.py` each plant table edits into a `tempfile` copy of `hdl/`, `tb/common` and the grading suite. A kill counts only when the run completes and every named check fails. The DUT files read are those the texts name.

## Gates run at the head

Logs are in `receipts/batch1/`, each with an rc file, summarised in `SUMMARY.txt`. The scoped Verilator was used, with identity checked as `Verilator 5.050 2026-07-01 rev v5.050` (`receipts/tool_identity.txt`).

| Gate | Result |
|---|---|
| `lint_rtl.py --check` | rc 0, 90 <= 90 |
| `make -C tb/verilator/pp_shadow -j16` | rc 0: 606, 646, 606 and 311 checks, 0 failures, RESULT PASS x4 |
| `check_port_contracts.py` | rc 0: 3798 ports (processor 1757); undocumented 217/19/111 at the ratchet; 59 without a rationale, all recorded |
| `measure_naming.py --check` | rc 0, 96 recorded |
| `measure_test_evidence.py --check` | rc 0: 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 |
| `check_nvm_capture.py` | rc 0 |
| `submodule_boundaries.gen.py --check`, `check_submodule_docs.py` | rc 0, 4 exact gitlinks |
| `docs_check.py` | rc 0, 0 findings |
| `pp_srcs.py --check --selftest`, `check_rtl_source_lists.py` | rc 0 (107 files, 4/4 lists, processor 36/42 tops) |
| `xvlog_gate.py --check` | rc 0, 4 == ratchet |

Restore was verified (`receipts/restore_verify.txt`):

- HEAD is `3370c6cb`, and `git write-tree` is `c7ef42fb`;
- the worktree and index equal HEAD;
- index modes, blobs and paths equal the head tree;
- all three submodules are clean at their gitlinks (`631eeb34`, `5dce647a`, `48ff7a7e`).

## Concurrent public findings

- At this round's start (PR #636 comment 5962460046), the PR carried no review, inline comment or reviewer finding. So there was no prior finding to resolve.
- Round R438-1 published NEGATIVE at 22:46Z, during this round, with these findings:
  - **R438-1 F1 (MINOR, Docs, Conformance): retained as this report's F1.** It was verified here independently, from processor `operator.md:54`/`:55`/`:326` at both pins, PR #140's round-2 list, and the parent's `CHANGELOG.md:45`, `SUBMODULES.md:114-115` and `REGISTER_MAP.md:2357-2358`. It is open at this head.
  - **R438-1 S1 (SUGGESTION, RTL, Docs): agreed.** It is this report's F3, recorded as RESIDUE because it is wording only. Neither classification gates the verdict.

## Hosted evidence at this head

Snapshot at 2026-10-02T22:49Z (`receipts/hosted_snapshot.txt`).

- **Completed with success:**
  - `rtl-fast`;
  - `docs` (docs-check, docs-check-no-git, wire-accountability);
  - `elaborate`;
  - in `rtl-full`: full-ci-gate, verilator-lint, yosys-elaboration, bdd-conformance, Yosys shards 0 to 3, and Verilator shards 0, 2, 3 and 4.
- **Skipped:** the physical gPTP job, which runs nightly and on manual dispatch only. A skipped context is not executed evidence.
- **Still in progress:** `rtl-full` run 37070220891, Verilator shard 1/5. The combined commit status is `pending`, and no `verilator-suites` or `yosys-portability` aggregate had been emitted yet.
- So the premise that every hosted context was green before this review started did not hold at the snapshot. The manager owns hosted acceptance.

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 open) | acceptance 1 to 5 against the diff; `protocol_processor_top` header at both pins (`receipts/top_iface_diff.txt`); `KL_pp_shadow.sv:1094-1140`; Milan v1.2 5.4.5.4 / IEEE 1722.1-2021 7.5.1 tie-off; `MILAN_COMPLIANCE_MATRIX.md:145`; processor PR #135 to #142 parent-visible lists; `operator.md:54-56`, `:326` at both pins | none (R439-1 applied it; F1 open) | `3370c6cbd5e4b096167c19ca709556a40207e538` |
| RTL | CLEAN | `hdl/milan/KL_pp_shadow.sv:1094-1100`, `:1132-1140`; `protocol_processor_top.sv:186-192`, `:228-243`, `:1022-1025`, `:1860-1862`, `:4484`; `KL_aecp_notify.sv:709`; `KL_aecp_engine.sv:945-966`, `:1918-1929`; `milan_datapath.sv:330`, `:7611`, `:7782`; lint 90 <= 90; xvlog 4 == ratchet; pp_shadow 4 builds | R439-1 | `3370c6cbd5e4b096167c19ca709556a40207e538` |
| Robustness | CLEAN | constant tie, so no new CDC path or flop at `EN_IDENTIFY_NOTIF_P` = 0; `DESC_LINE_BYTES_P` 576 inside the enforced 576..1008; `cfg_maap_internal_i` tied 0; `current_cfg_i` fallback at the only valid value 0 (S1); processor NVM path byte-identical between the pins; capture census and firmware unchanged; ROM-ledger refusal paths (`ooc.sh:459-475`) | R439-1 | `3370c6cbd5e4b096167c19ca709556a40207e538` |
| Tests | CLEAN | probes table (5 detected, 2 explained); both new `DUT_READER_DISPOSITIONS` entries checked against `acmp_mutants.py` and `notify_mutants.py`; four generator re-runs byte-identical; independent ROM regeneration; base-pin ratchet measurement; pp_shadow 606/646/606/311; disclosed-deviation reproductions (xvlog, nohup) | R439-1 | `3370c6cbd5e4b096167c19ca709556a40207e538` |
| Docs | UNCLEAN (F1 open; F2, F3, F4 RESIDUE) | `CHANGELOG.md:11`, `:39-59`; `docs/reference/SUBMODULES.md:25`, `:83`, `:93-119`; `docs/design/MEDIA_CLOCK_FOLLOWING.md:8`, `:1278-1286` against `gen_ucode.py:1654-1711` and the D3C suite; boundary diagram and `PNG_MANIFEST.json` (generator); `REGISTER_MAP.md:1016`, `:2357`; `docs_check.py`; `check_submodule_docs.py` | none (R439-1 applied it; F1 open) | `3370c6cbd5e4b096167c19ca709556a40207e538` |

## Real limits

- **Manager banks, not run here:** `scripts/run_all_suites.sh`, `syn/yosys/run.sh`, `sw/builder/test_builder.py`, `milan_dp`, `milan_dp_render` and `nvm_cosim`.
- **Also not run here:**
  - processor suites: processor behaviour claims were checked against the processor's sources, guides and merged PR bodies at `631eeb34`, not by re-running them;
  - act and Docker;
  - hosted re-runs;
  - hardware.
- **Physical calibration NOT RUN.** Field skips are not hardware proof.
- **Identify tie-off values:** no parent test grades the values `EN_IDENTIFY_NOTIF_P` = 0 and `identify_button_i` = 0. At 0 the input is not read, and the sequencer is graded only in the processor's simulation, as the PR states. Lint grades the presence of the pin, and the port-contract gate grades its rationale.
- **xvlog shared the host:** the xvlog gate ran while unrelated builds owned by other parties were active on the host. xvlog analysis does not depend on load, and the verdict equals the author's.
- **Manager's rulings:** the rulings on `test_evidence.budget` and the #495 routing were taken from the assignment. At review time they were not found as public comments on #635, #636 or #495.

## Pending manager duties

- Have F1 fixed (with F2 in the same edit if convenient), then commission a re-review at the new head covering Docs and Conformance. A docs-only change does not un-cover RTL, Robustness or Tests, whose scope it does not touch.
- Carry F2, F3 and F4 (RESIDUE) and S1 to the residue checklist (#495), beside the `current_cfg_i` comment rewording and the compliance-matrix citations already routed there.
- Publish the rulings: `scripts/test_evidence.budget` stays at 77, and the #495 entries for the stale `milan_dp_gptp` README figure and the two processor suggestions.
- Confirm that hosted `rtl-full` completes with `verilator-suites` and `yosys-portability` emitted and successful at the final head.
- At the merge turn, run the act replica and the current-dev candidate build, then the post-merge containment check.

R439-1 FINISHED

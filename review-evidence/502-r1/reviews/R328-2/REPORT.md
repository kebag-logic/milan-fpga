[R328] NEGATIVE - exact head 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e

Round R328-2, internal independent re-review of kebag-logic/milan-fpga PR #579 for issue #502.
Head `5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e`, tree `06e4ce62c7c5fdabc6c9a79f9f1f47e39f94ee64`.
Delta reviewed: `104c8a54..5d4cf33e`, which is two commits: `220c9d56` (option (a)) and `5d4cf33e` (the minimal form).
Source base `831f94f4`. My round 1 (R328-1) covered `104c8a54` in full.

## Summary

The round-2 RTL is correct, and it is exactly equivalent to the base where it must be.

- **Equivalence.** I inlined the head's three new named conditions into its `amap_edit_commit` block. The result equals the `104c8a54` block, whitespace aside.
- **Pulse = write.** `amap_edit_live_wr_p` is true exactly when a phase-5 write branch is taken, on the same `axis_clk` edge.
- **Key exclusivity.** The input and output key-valid flags are structurally mutually exclusive, as the author states.
- **Priority.** The if/else-if priority is preserved. The area reduction therefore comes from restructuring equivalent source, not from lost behaviour.

All eight round-1 findings are closed at this head, and each has executable evidence:

- **Round-1 mutants killed.** `phase4_validate`, M5 and M6 are now killed in both legs by named committed checks.
- **Duplicate probe.** P3 shows pending clear for an unchanged duplicate.
- **Observer.** It is anchored on live storage.
- **Docs.** The three documentation findings are fixed.

The verdict is NEGATIVE because of one new MINOR finding, F1 (Docs). The changelog entry for this PR, and the matching pin-history line, still describe the round-1 unqualified map trigger ("accepted map commit beats raise the same sticky source"). Option (a) removed that behaviour in this round. Two SUGGESTIONs are also recorded; they do not block.

## Reconstruction

- **Contract:** AGENTS.md sections 3 to 8, CONTRIBUTING.md and docs/README.md.
- **Issue #502:** the body; decision and scope 5844866872, 5845129498, 5846418959 and 5847404798; the round-2 assignment and decision 5848417938 (option (a) and items 1-7); the author's REVIEW READY 5853687615.
- **Authorities:**
  - `docs/design/SAVED_STATE_MATERIALIZATION.md` sections 1, 2 and 5.2;
  - `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` sections 6.1 and 11;
  - `docs/testing/TESTING.md`, the explicit-campaign table;
  - the processor map-edit contract at pin `870ff88a` (`protocol-processor/hdl/top/protocol_processor_top.sv:358-375`);
  - the ADD/REMOVE_AUDIO_MAPPINGS program (`protocol-processor/hdl/aecp/ucode/gen_ucode.py:1765-1809`, phase order 0, 4 x n, 1, 5 x n, 2, or 3 on refusal).
- **Diff:** `git diff 104c8a54..5d4cf33e` (9 paths), both commits, and `220c9d56..5d4cf33e`.
- **Public evidence:** branch `502-review-evidence` at `c5b80faa`, `review-evidence/502-r1/author-r3/`. This is the round-2 packet; the `dc9d0928` tree named in the brief holds only the round-1 packet. From it I used:
  - the anchor adapter `adapt-reviewers.py`;
  - the oracle driver `run-r328-oracle.py`;
  - the reviewer-result files;
  - the area records;
  - the default-sweep receipt.
- **Prior findings:** I read the prior public findings (R328-1, R329-1) only after my own independent pass over the delta.

## Verification of the assigned items

### (1) Equivalence of the phase-5 write, and the pulse

**Source-level expansion** (`scripts/r328_2_expand_check.py`, `receipts/expand_check.txt`):

- The head adds four continuous assigns (`hdl/milan/milan_datapath.sv:4248-4271`).
- Each of the three change and beat names is used exactly once in the `amap_edit_commit` block (`:4316`, `:4371`, `:4382`).
- Inlining them gives a block equal to the `104c8a54` block, whitespace removed: `True`. Each definition is a top-level `&&` chain used as a right `&&` operand, so inlining preserves the parse.
- The whole-file diff contains only:
  - the four assigns and their comment;
  - the three condition substitutions;
  - the new port connection `.amap_live_wr_i (amap_edit_live_wr_p)` (`:7498`).
- Every register's next-state function is therefore unchanged, and this covers every record type:
  - input key writes: `amap_in_store_r` and the `iwr` pulse;
  - output key writes: the `owr` pulse, `amap_out_owner_v_r`, `amap_out_owner_r` and `amap_out_cluster_r`;
  - REMOVE, which clears owner and cluster;
  - `amap_edit_changed_r`, the `seen` de-duplication, and the CSR path.

**Pulse = write, on the same edge.**

- `amap_edit_live_wr_p = axis_resetn && beat && phase==5 && context && (in_change || out_change)`.
- The write happens in the `3'd5` case item under `else if (beat)`, taking `if (context && in_change) ... else if (context && out_change)`.
- A truth table over the atoms shows the pulse equals "a write branch is taken" both with and without the exclusivity assumption. Both are combinational over the same registers, sampled on the same `axis_clk` posedge.
- The shadow runs on `clk_i = axis_clk` and `rst_n = axis_resetn` (`milan_datapath.sv:7393-7498`), so no CDC is introduced.

**Key exclusivity is structural.**

- `amap_edit_in_key_v_w` and `amap_edit_out_key_v_w` default to 0 (`:4081-4082`).
- `amap_edit_in_key_v_w` is set only under descriptor type `0x000E` (`:4164`), and `amap_edit_out_key_v_w` only under the else-if for type `0x000F` (`:4189`).
- `in_change` requires the first flag and `out_change` the second, so both are never true together, and if/else-if equals OR.
- An equivalence-control mutant that turns the else-if into two independent `if`s (E2) survives both legs, as expected.

**Area.**

- Published same-recipe figures, LUT total:
  - datapath: `104c8a54` 97292, `220c9d56` 98016, head 96166;
  - shadow: 66902 at `104c8a54`, 66982 at head.
- FF, LUTRAM, RAM and DSP are unchanged, and CARRY4 at head equals `104c8a54`.
- The `104c8a54` shadow LUT (60766 + 6136 LUTRAM) equals the external reviewer's independent round-1 OOC measurement.
- Given the source equivalence above, the -1126 datapath LUT is a synthesis-structure effect of naming the shared comparisons, not lost logic. The +80 shadow LUT comes from replacing an internal phase decode with a free input. I did not re-run synthesis (see Limits).

### (2) Round-1 mutants and probes, rerun

**Scripts.** All four are byte-identical to the round-1 publications:

- `reviewer_mutants.py` `fcca5e03...`;
- `oracle_probe.py` `3af36c1a...`;
- `r329_mutants.py` `3aeb65eb...`;
- `r329_probe.py` `378391e9...`.

**Unchanged runs.**

- The anchors keyed to the removed trigger text are refused (`REFUSED anchor count 0`). They are never counted as kills.
- The mutants whose anchors are unchanged are killed:
  - `delay_one_cycle`, `pulse_only_no_sticky` and `reset_sets_sticky` (`receipts/r328_mutants_unchanged.txt`);
  - control, M3 and M7 (`receipts/r329_mutants_unchanged.txt`).

**The author's adapter** (`author-r3/adapt-reviewers.py`) changes anchors only. It loads the script unchanged, replaces the anchor of each mutant whose anchor is `LIVE` with the head's `aecp_name_wr_w | amap_live_wr_i`, keeps every replacement body, and calls the script's own `main()`.

**My re-anchored runs** use my own independent runner, `scripts/r328_2_reanchor.py`, which does the same and prints the script hash:

- `receipts/r328_mutants_reanchored.txt`:
  - all 7 re-anchored mutants are KILLED in both legs;
  - `phase4_validate` is killed by `K12 refused record input sticky_pending_PP_STAT/PP_NVM_STAT` (static and dynamic), and by the same checks for `refused record output` (dynamic) (`receipts/mutants/r328_reanchored/`).
- `receipts/r329_mutants_reanchored.txt`: all 8 are FAIL in both legs, and the file is byte-identical to the author's published re-anchored results.
  - M5 is killed by `K12 refused record input/output sticky_pending_*`.
  - M6 is killed by `K12 remove input/output no_durable_claim_over_unsaved` and `pending_from_accepting_edge`, in both legs where the direction exists.

**External probe, unchanged** (`receipts/r329_probe_runs.txt`):

- Shipping: 295 checks, 0 failures.
- P3 `duplicate ADD status 0, phase-5 records 1, marks 0, mappings after 1, PP_STAT[11] pend 0, durable 1`, so pending stays clear for an unchanged duplicate.
- P1 (REMOVE from a durable baseline) and P2 (refused ADD, status 7) pass.
- The re-anchored M5 fails P2's sticky checks, and M6 fails P1 with 24667 falsely durable cycles.

**My oracle, unchanged:**

- Against the head's `sim_main.cpp` it refuses on the moved anchors (`receipts/oracle_unchanged_at_head.txt`).
- The unchanged `probe_main.patch`, applied to the round-1 harness and built against the head RTL, passes (`receipts/oracle_unchanged_r1_harness_head_rtl.txt`):
  - 138 checks in the static leg and 193 in the dynamic leg, 0 failures;
  - 10 of 10 static and 14 of 14 dynamic `ORACLE ... live change without pending` assertions pass.
- This confirms the author's clarification: those are two totals, not a pass fraction.
- A re-anchored run on the head harness passes (`scripts/r328_2_oracle_head.py`, `receipts/oracle_reanchored_head_harness.txt`):
  - 195 and 301 checks, with 11 of 11 and 16 of 16 oracle assertions;
  - it rebinds two anchors and gates the oracle on `watching`, so that control-face preloads form the baseline;
  - the oracle sees 0 storage changes for both duplicate controls, and changes on the ADD and REMOVE edges.

**Controls present in both legs.**

- Refused-at-validation: `sim_main.cpp:1451-1457`, the input direction in both legs and the output direction in the dynamic leg (static output is refused before validation).
- REMOVE from a durable baseline: `:1472-1478`.
- Duplicate from a durable baseline: `:1465-1470`.
- Each boots separately into durable status (`pending_boot`, `:1327-1352`).

**Lane mutant.** `make -C tb/verilator/pp_shadow pending-mutant` passes: the clean control passes, and the late-mark mutant fails 12 named K10/K12 checks, including `K12 remove input/output` (`receipts/pending_mutant.log`).

**Default target.** `make -C tb/verilator/pp_shadow` passes 575 + 575 + 575 + 263 checks with 0 failures (`receipts/pp_shadow_make.log`).

**New round-2 mutants of the parent-side pulse** (`scripts/r328_2_dp_mutants.py`, `receipts/r328_2_dp_mutants.txt`):

| mutant | static | dynamic | note |
|---|---|---|---|
| P1 pulse from input changes only | survived | KILLED | the static leg has no output edits; the dynamic leg fails `K12` and `K12 remove output` durability and edge checks |
| P2 output changes only | KILLED | KILLED | `K12 input` and `K12 remove input` durability and edge checks |
| P3 unqualified phase 5 (the round-1 behaviour) | KILLED | KILLED | `K12 duplicate input/output sticky_pending_*` |
| P4 no phase-5 qualifier | survived | survived | S1 below |
| P5 no context term | survived | survived | equivalent under the processor contract: phase 5 follows only an accepted phase 1 in context |
| P6 pulse tied low | KILLED | KILLED | durability and edge checks |
| E1 no beat de-duplication | survived | survived | expected: after the write edge the change term is false |
| E2 else-if split into two ifs | survived | survived | expected: key exclusivity |
| S1 shadow ignores `amap_live_wr_i` | KILLED | KILLED | durability and edge checks |

The shipping sources hashed identically before and after every campaign.

### (3) The observer's unsaved interval is anchored on live state

- `sim_main.cpp:292-302` snapshots `name_r`, `amap_in_store_r`, `amap_out_owner_v_r`, `amap_out_owner_r`, `amap_out_cluster_r` and `cmap_flat_w`.
- `:324-340` starts `unsaved` and `first_write` only on an edge where that snapshot changes.
- The trigger signals (`:309-314`) feed only the `names` and `maps` counters.
- `watching` starts before the first command byte (`:744`), so boot and CSR preloads form the baseline.
- **Executable proof:** the duplicate controls carry a phase-5 trigger (`maps` = 1) with pending clear, and they still pass. A trigger-anchored interval would count missing-pending cycles there.
- Datapath mutants P2 and P6 are killed by `pending_from_accepting_edge`, which is measured from the storage change.

### (4) Documentation

**Round-1 targets fixed.**

- `SAVED_STATE_MATERIALIZATION.md` section 1 (`:128-134`) and its table (`:145-146`) now name `aecp_name_wr_o` and the parent's `amap_edit_live_wr_p`/`amap_live_wr_i`. Their locations are correct (`amap_edit_commit`, `latch_live_pending`).
- Section 5.2 (`:485`) names `aecp_live_pend_r`, which exists at `KL_pp_shadow.sv:938,948-954`.
- The #502 paragraph (`:226-248`) matches the committed controls.
- `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 6.1 (`:961`, `:968-971`) and the section 11 row (`:1263`) match the RTL.
- The `TESTING.md` explicit-campaign row (`:268`) lists `pending-mutant`, with the files whose change requires it.
- The `pp_shadow` README (`:50-94`) matches the tests.

**No residual wording.** No "conservative" wording remains in `hdl/milan/`, the saved-state pages, `TESTING.md`, `tb/verilator/pp_shadow/` or `CHANGELOG.md`.

**The exception.** `CHANGELOG.md:39` and `docs/reference/SUBMODULES.md:61` still carry the round-1 trigger description (F1).

### (5) Firmware, capture gate and repository gates

**Firmware and pins unchanged.**

- `git diff` over `sw hdl/common/csr configs tb/verilator/nvm_capture_cpu` is empty for both `831f94f4..head` and `104c8a54..head`.
- The firmware blob is `a4e560fb` at base and head.
- The gitlinks are identical to `104c8a54`: processor `870ff88a`, gPTP `5dce647a` (`receipts/firmware_unchanged.txt`).

**Gates.** 29 gates and suites exit 0 at the head, in a disposable clone with registered submodules (`receipts/gates_summary.txt`, `receipts/gates/`):

- Git and RTL:
  - `git diff --check`, base..head and 104c8a54..head;
  - `lint_rtl --check`, 90 <= ratchet 90;
  - `check_sv_idiom`, `check_port_contracts`, `check_wire_accountability`, `check_rtl_source_lists` and `xvlog_gate --check`.
- Code idiom and measurement: `check_cpp_idiom`, `check_py_idiom`, `measure_naming --check` and `measure_test_evidence --check`.
- Documentation:
  - `docs_check` in both the git and no-git modes;
  - `check_em_dash --base 831f94f4`, `check_doc_style`, `gen_toc --check` and `gen_toc --verify-anchors`;
  - `check_doc_paths`, `check_submodule_docs`, `check_feature_status` and `gen_module_matrix --check`;
  - `submodule_boundaries.gen.py --check` and `check_diagram_pngs`.
- CI: `ci_events --check`.
- Firmware and capture: `check_nvm_capture`, `check_baremetal_only --check` and the NVM firmware self-test.
- Suites: `nvm_backend`.

**First-pass refusals.** The first pass refused seven code-quality gates because the scratch submodules were standalone clones. After I registered them properly the gates were rerun, and all pass.

**Default sweep.** I did not rerun the full sweep; it is out of my allowance. The published receipt `author-r3/receipts/resume-default-sweep.log` reads `suites: 55 passed: 55 failed: 0 timed out: 0; checks: 2125319`, with four declared field-campaign skips that contribute 0 checks.

## Round-1 findings at this head

| Finding | Severity (round 1) | State | Evidence at `5d4cf33e` |
|---|---|---|---|
| R328-1 F1 (refused-at-validation control; phase4_validate survived) | MINOR | CLOSED | committed controls `sim_main.cpp:1451-1457`; `phase4_validate` killed by named `K12 refused record *` checks in both legs |
| R328-1 F2 (materialization section 1 and 5.2 stale) | MINOR | CLOSED | `SAVED_STATE_MATERIALIZATION.md:128-134,145-146,485` |
| R328-1 F3 (campaign table) | MINOR | CLOSED | `TESTING.md:268` |
| R328-1 S1 (duplicate raises sticky pending) | SUGGESTION | CLOSED | option (a) RTL; P3 pend 0; committed `K12 duplicate input/output` checks; P3-unqualified mutant killed |
| R328-1 S2 (trigger-anchored observer) | SUGGESTION | CLOSED | `sim_main.cpp:292-340`; item (3) |
| R329-1 F1 (REMOVE from durable; M6) | MINOR | CLOSED | `sim_main.cpp:1472-1478`; M6 killed by `K12 remove * no_durable_claim_over_unsaved`/`pending_from_accepting_edge` |
| R329-1 F2 = R328-1 F1 (M5) | MINOR | CLOSED | M5 killed by `K12 refused record *` in both legs |
| R329-1 F3 (unchanged duplicate sets pending) | MINOR | CLOSED | option (a) as decided in 5848417938; P3 pend 0; committed duplicate controls; section 6.1, materialization, README and RTL wording updated. The residual changelog and pin-history wording is recorded as the new F1 below |

## Findings (this round)

### F1 - MINOR - Docs - CHANGELOG.md:39, docs/reference/SUBMODULES.md:61 - round-1 unqualified map trigger still described as shipped behaviour

- **Authority:**
  - Decision 5848417938 makes the map source rise "only on a phase-5 record that the datapath actually writes": "An unchanged duplicate then raises nothing."
  - The decision also says the conservative-duplicate wording "goes away everywhere".
  - AGENTS.md section 6, Docs: "Changed contracts are reflected in authoritative docs".
  - docs/README.md:102 lists `CHANGELOG.md` as the current changelog.
- **Evidence:**
  - `CHANGELOG.md:39`, the #502 entry, reads "Accepted map commit beats raise the same sticky source." At this head an accepted commit beat for an unchanged record raises nothing (`K12 duplicate input/output` checks; P3).
  - `docs/reference/SUBMODULES.md:61` reads "Map phase 5 supplies the corresponding map trigger." The trigger is now the parent's actual-write enable (`amap_live_wr_i` from `amap_edit_live_wr_p`), not the processor's phase-5 export.
  - Both lines date from `87e263fd` and were accurate at `104c8a54`. This round changed the behaviour they describe and left them unchanged (`git diff 104c8a54..5d4cf33e` does not touch either file).
- **Impact:** the product changelog is the record a release reader consults. It states the behaviour that option (a) removed: a re-applied existing mapping would set pending until reset. The pin-history line points a reader at the wrong trigger source.
- **Required outcome:** both lines describe the head. The map source rises on the parent's actual phase-5 write, and unchanged records raise nothing, or the wording is neutral and does not claim every commit beat.
- **Verification:** read both lines against `KL_pp_shadow.sv:388,945-946` and `milan_datapath.sv:4269-4271`. The docs, em-dash, style and path gates pass.

### S1 - SUGGESTION - Tests, Robustness - tb/verilator/pp_shadow/sim_main.cpp:1442-1479 - the pulse's phase-5 term is unguarded

- **Evidence:** datapath mutant P4 drops `(pp_amap_edit_phase_w == 3'd5)` from `amap_edit_live_wr_p` and survives both legs.
- **Reachability:** by the program's phase order, a claimed and changed key can be presented off phase 5 only on the abort (phase 3) of a multi-record command refused after an earlier record claimed the same key.
- **Reviewer probe** (`scripts/r328_2_multirec_probe.py`): a two-record ADD refused at record 1, on the input direction and on the output direction.
  - Shipping: status 7, map empty, pending clear. It passes 295 checks (`receipts/multirec_probe.txt`).
  - P4: fails `R328-2 Q1/Q2 ... sticky_pending_PP_STAT/PP_NVM_STAT`.
  - P5 passes the probe, consistent with the equivalence argument.
- **Why only a suggestion:** the shipping RTL is proven equivalent at source level, and the failure mode is a false pending, not a false durable.
- **Optional:** add a multi-record partial-refusal control from a durable baseline.

### S2 - SUGGESTION - Docs - PR #579 body; SAVED_STATE_SNAPSHOT_OWNERSHIP.md:1263 - small wording drift

- The published PR body's "Status" section says the body "has not been applied to the PR". It has been applied.
- The section 11 map row says "from the first accepted write". "actual" would match its own change-indication column.
- Optional; neither changes any claim about behaviour.

## Lens results

```text
[R328] PASS Conformance - hdl/milan/milan_datapath.sv:4248-4271,4316,4371-4396,7498; hdl/milan/KL_pp_shadow.sv:385-388,931-957 at 5d4cf33e; receipts/expand_check.txt, r329_probe_runs.txt, pp_shadow_make.log - option (a) of 5848417938 checked: the map pending source is the datapath's own write condition, factored once and never restated; the pulse equals the write on the same edge; unchanged duplicates raise nothing (P3, committed duplicate controls); name trigger and late marks unchanged; firmware, CSR, configuration and pins unchanged.
[R328] PASS RTL - hdl/milan/milan_datapath.sv:4081-4082,4164,4189,4248-4271,4298-4420,7393-7498; hdl/milan/KL_pp_shadow.sv:385-388,938-957 at 5d4cf33e - checked against the 104c8a54 block: expanded block identical; if/else-if priority preserved; in/out key exclusivity structural; pulse gated by axis_resetn and low in reset; shadow and datapath share axis_clk/axis_resetn (no CDC); widths unchanged; the sync-reset latch is unchanged; lint within its ratchet; port-contract, SV idiom and wire-accountability gates pass. No timing claim is made or checked.
[R328] PASS Robustness - tb/verilator/pp_shadow/sim_main.cpp:1442-1515 plus reviewer probes at 5d4cf33e (receipts/r329_probe_runs.txt, multirec_probe.txt, oracle_*) - refused-at-validation (single- and two-record), duplicate, REMOVE and ADD each from a durable baseline, zero-record, static-output refusal, repeated SET_NAME, held beats (E1 equivalent), snapshot ACK, reset and both output-map configurations: no false durable and no false pending on shipping. S1 is optional.
[R328] PASS Tests - tb/verilator/pp_shadow/{sim_main.cpp,pending_mutant.py,pending_probes.vlt,Makefile} at 5d4cf33e; receipts/pp_shadow_make.log, pending_mutant.log, r328_mutants_*.txt, r329_mutants_*.txt, r328_2_dp_mutants.txt - every round-1 mutant is killed by a named committed check (anchors rebound only); the storage-anchored observer kills the new pulse mutants P1, P2, P3, P6 and S1; E1, E2 and P5 survive as equivalent; P4 survives (S1, optional); nvm_backend passes.
```

`Docs` is UNCLEAN because F1 is open. What it did cover clean: `SAVED_STATE_MATERIALIZATION.md:128-146,226-248,485`, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md:957-972,1263`, `TESTING.md:268`, the `tb/verilator/pp_shadow/README.md:50-94` pending section, the RTL `//!` comments, and the docs, style, TOC, path, module-matrix and diagram gates.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | issue decision 5848417938; milan_datapath.sv:4248-4271,4316,4371-4396,7498; KL_pp_shadow.sv:385-388,931-957; processor top :358-375 and gen_ucode.py:1765-1809 at 870ff88a; P3 probe; firmware/CSR/config/pin diff | R328-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |
| RTL | CLEAN | milan_datapath.sv:4054-4271,4298-4420,7393-7498 against 104c8a54; KL_pp_shadow.sv:385-388,938-957; expansion/truth-table check; lint, idiom, port-contract, wire-accountability, xvlog gates | R328-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |
| Robustness | CLEAN | pp_shadow K10/K12 both legs; external probe P1-P3; two-record partial-refusal probe; oracle on both harnesses; reset/ACK/held-beat/static-output paths | R328-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |
| Tests | CLEAN | pp_shadow sim_main.cpp/pending_mutant.py/pending_probes.vlt/Makefile; 10 + 11 round-1 mutants (unchanged and re-anchored); 9 new pulse mutants; late-mark campaign; default target; nvm_backend | R328-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |
| Docs | UNCLEAN (F1 open) | CHANGELOG.md; docs/reference/SUBMODULES.md; SAVED_STATE_MATERIALIZATION.md; SAVED_STATE_SNAPSHOT_OWNERSHIP.md; TESTING.md; pp_shadow README; RTL comments; PR body; docs gates | R328-2 | 5d4cf33e3709c35d4f5bc90d3c5a2334ef3bfd8e |

## Limits

- **Simulator path.** The assigned simulator path `$VALIDATION_STORAGE/372-manager-candidate1/pinned-tool-bin/verilator` is absent. I used `$VALIDATION_STORAGE/502-manager-r1/pinned-tool-bin/verilator`, which reports Verilator 5.050, rev v5.050 (wrapper sha256 `905795b9...`, `verilator_bin` sha256 `44898b22...`, the same identity as round 1). A local wrapper caps build parallelism at 8 (`receipts/tool_identity.txt`, `receipts/verilator_wrapper.sh`).
- **Not run by me:**
  - Yosys: the area delta is the author's same-recipe measurement. I explain it by source equivalence and did not re-measure it.
  - The default sweep and the full parent, processor and gPTP banks.
  - `milan_dp`, `nvm_cosim`, behave and the builder.
  - The processor `name_wr_mutant.py`.
  - act or hosted replication, and hardware.
- **Hardware.** Physical calibration was NOT RUN, and the skipped field campaigns are not hardware proof.
- **Timing.** The new combinational path, from the datapath's claim comparisons through the shadow into the backend's registered `pend_i`, has no timing evidence here, and the author makes no timing claim.
- **Probe shapes.** The probes ran only in the `pp_shadow` harness shapes (1x1 static, and the dynamic-output fixture).
- **Hosted snapshot, 2026-09-27T07:52:31Z:**
  - succeeded: `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `full-ci-gate`, `verilator-lint`, `wire-accountability`, `yosys-elaboration`, `bdd-conformance`, `changes`, Yosys shards 0-3/4, and Verilator shards 0, 2, 3 and 4/5;
  - still running: Verilator shard 1/5;
  - not yet emitted: the `verilator-suites` and `yosys-portability` aggregates;
  - skipped: physical gPTP (`receipts/hosted_checks_snapshot.txt`).
- **Clone integrity.** Probes and builds ran in a disposable clone under the packet's `scratch/`. Afterwards the review clone checks clean (`receipts/integrity_pre.txt`, `receipts/integrity_post.txt`):
  - HEAD `5d4cf33e`, tree `06e4ce62`;
  - 915 index entries, 0 blob or mode mismatches, and 0 non-default index flags;
  - the index hash is unchanged, and `git status --ignored` is empty;
  - the submodules sit at their gitlinks (processor `870ff88a`, gPTP `5dce647a`, verilog-axis `48ff7a7e`) and are clean.

## Pending manager duties

- Route F1 to the executor. A re-review must re-cover Docs at the new head, plus any lens whose artifacts the fix touches.
- Accept the exact-head hosted `verilator-suites` and `yosys-portability` aggregates and the act replica.
- Build and validate the current-dev candidate at the merge turn (source base `831f94f4`, live dev `8c8e7bb0`), then run post-merge containment.
- Obtain the external review's exact-head verdict and the maintainer's merge authorization.

R328-2 FINISHED

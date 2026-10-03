[R446] NEGATIVE - exact head 2a765a6c3868400c20ede2e357876f28a811c811

# R446-1 internal review: issue #234 / PR #638

- Head `2a765a6c3868400c20ede2e357876f28a811c811`, tree `09d124d8f8ec3598bfc74572c97a0dfec5273ec4`, base dev `1269cdafb4bb964c757baae0f0c5a932d43f540b`.
- Rebuilt from public state only, in this order: AGENTS.md, CONTRIBUTING.md, docs/README.md, the issue body, the lane assignment (5966260488), the TAKEN comment (5966304381), REVIEW READY (5967818534), the manager rulings (5967852698), NFR-RES-01 (`docs/reference/FR_NFR.md:317`), BUILDING.md section 5, the diff `1269cdaf..2a765a6c` (5 commits, 11 files), and the public evidence tree `43ad8362:review-evidence/234-r1`. All 90 manifest digests were re-verified.
- Prior public review findings on this PR: none. The PR thread holds only manager notices: one withdrawn start and the R446-1 and R447-1 starts. Nothing needs to be resolved or retained.
- Judged against the rulings in 5967852698:
  - (b) the gate runs in both places: hosted (self-test, mutants, `check-baseline`) and in the manager's Vivado bank;
  - (c) criterion 1 is judged at 50 MHz;
  - the tolerances and ceilings are the accepted working policy;
  - (a) the NFR-RES-01 allocation is an open owner decision and is not counted as a defect here;
  - (e) sets the child-issue mapping.

Verdict: NEGATIVE. Three MINOR findings are open: F1, F2 and F3. Four RESIDUE items and five SUGGESTIONs follow.

## Findings

### F1 - MINOR - Conformance, Robustness, Tests - `syn/ooc/pp_resource_gate.py:105`, `:251-260` - a non-finite slack passes the timing floor

- **Requirement/evidence:**
  - `timing()` converts the WNS and WHS columns with `float()`, so the strings `inf` and `nan` are accepted as numbers.
  - `verdict_for()` then compares them with `<` and `>`. `inf` clears the floor and the fall limit. `nan` makes both comparisons false.
  - Vivado prints `inf` for WNS and WHS, with zero endpoints, when no path is constrained.
  - Receipt `receipts/probe-gate-cli.log`. The cases were planted through the gate's own `check` CLI against the real `route-1x1` policy:
    - `unconstrained: WNS/WHS 'inf', 0 endpoints`: rc 0, `RESULT: PASS`;
    - `WNS 'nan'`: rc 0, `RESULT: PASS`;
    - the same report with `NA` is refused, rc 2.
  - `docs/integration/BUILDING.md:72` says the build's WNS and WHS thresholds "are not automatically enforced". That leaves this gate as the only automated timing check on the route.
- **Impact:** a candidate whose route lost every timing constraint passes the timing half of the gate. Criterion 4 asks CI to reject material timing regressions, and this one is missed. Every finite case behaves correctly: +0.030/+0.029, 0.000/-0.001, -2.000 and the 0.25 ns fall all give the documented result.
- **Required change:** a non-finite or unconstrained slack (`inf`, `nan`, or zero total endpoints) is never a pass. It is refused with exit 2 as unreadable, or failed with exit 1. A self-test arm plants it, and a mutant that removes the guard is killed.
- **Verification:** rerun `probe_gate_cli.py`. The two `GAP?` timing lines must exit non-zero, the self-test must report the new arm, and the mutant campaign must kill the new mutant.

### F2 - MINOR - Tests - `syn/ooc/pp_resource_gate_selftest.py:102-153`, `syn/ooc/pp_resource_gate_mutants.py:13-52` - several claimed refusals have no arm, so disabling them leaves hosted CI green

- **Requirement/evidence:**
  - The self-test's docstring says it plants "every regression and refusal the resource gate claims".
  - The gate's docstring (`:12-14`), AREA_BUDGET.md:168-169 and the recipe all claim that the identity covers the tool build, device, design, design state and every flow command, and that standalone RAMB36 and DSP growth is material.
  - `receipts/probe-gate-mutants.log` ran each mutant against the hosted 51-arm self-test. The control passes, and the following enforcement removals all pass too:
    - identity field `design` dropped;
    - identity field `state` dropped;
    - `create_project`, `synth_design`, `opt_design`, `phys_opt_design`, `route_design` or `kl_timing_grade_configure` dropped from `FLOW` (`:53-54`);
    - `RAMB36` or `DSP` dropped from `GATED["ooc"]` (`:49`);
    - the timing floor boundary changed from `<` to `<=`;
    - the fall boundary changed from `>` to `>=`.
  - The only flow arms are the placement directive and the thread count (`_selftest.py:123-125`). No standalone arm grows RAMB36 or DSP.
  - The gate itself enforces every one of these today: `probe-gate-cli.log` gives rc 2 for design, state and synthesis-directive changes, and rc 1 for standalone RAMB36 +1 and DSP +1. The defect is only that nothing would notice if one of them were removed.
- **Impact:** removing one of these checks keeps rtl-fast green. Example: if `route_design` leaves the identity, a PR that changes both the route directive and RTL is judged as an architectural delta instead of being refused as a recipe change. That is the distinction the issue's scope bullet asks CI output to make.
- **Required change:**
  - arms that plant a change in each claimed identity element (design, design state, each flow command) and standalone RAMB36 and DSP growth;
  - a floor-equality arm (WNS = floor passes; BUILDING.md says "at least");
  - mutants for each.
- **Verification:** rerun `probe_gate_mutants.py`. Every mutant listed above must be KILLED.
- **Not required:** five survivors are equivalent or low-value.
  - Equivalent: the read-source presence check and the include-directory presence check. An absent file still raises `OSError`, which is refused with exit 2.
  - Low-value: header uniqueness, `located()` uniqueness, and the decimal count format.

### F3 - MINOR - Docs - `docs/design/AREA_BUDGET.md:156` - "a net 101 LUTs and 95 FFs" mixes two partitions; the FF figure does not reproduce

- **Requirement/evidence:**
  - Re-derived from the published B and A `ooc-1x1` records (`receipts/reconcile.log`).
  - The findings page's "net 101 LUTs" and "sum to 309 LUTs" (`234_PP_SHADOW_AREA_BASELINE.md:134-135`) reproduce only on one partition: the direct children of `u_pp`, minus `u_nvm_port` and minus `u_nvm_arb`. The second exclusion is not stated.
  - On that same partition the FF movement is **-12** (`u_listener` -11, `u_srp` -1), not +95.
  - +95 appears only when the processor top's own +107 FF is added. The findings page reports that +107 separately at `:136`, and `protocol_processor_top` is a file B changes. Adding the top's own logic also moves the LUT figure to +78.
  - The whole wrapper minus `u_nvm_port` gives +79 LUT and +93 FF.
- **Impact:** the published rationale for the accepted FF tolerance cites a movement in untouched blocks that the measurements do not show. This is a wrong figure, not wording, so it is not RESIDUE. The accepted policy values are unaffected.
- **Required change:** AREA_BUDGET.md:156 states a figure pair taken from one partition, and the findings page names that partition at `:134-135`. For example: "u_pp's sub-blocks other than the NVM port and arbiter moved by a net +101 LUTs and -12 FFs; the processor top's own logic kept 107 more FFs".
- **Verification:** rerun `reconcile.py`. It must report 0 mismatches against the published records.

### RESIDUE (wording only; carried to the residue checklist, #495)

- **R1** - `docs/design/AREA_BUDGET.md:114`
  - Now: "proposed reserve: 13.5 tiles (10 %)".
  - Fix: "reserve: 13.5 tiles (10 %), 121.5-tile ceiling, accepted (manager ruling)". Ruling 5967852698 accepted the 121.5-tile ceiling as working policy.
- **R2** - `docs/design/AREA_BUDGET.md:182-185`
  - Now: "The proposal is one run per merge candidate that moves the processor pin, `KL_pp_shadow`, the shipping configuration or the build flow." and "Making it part of the merge bar is an owner decision; CONTRIBUTING is unchanged here."
  - Fix: "The Vivado comparison runs in the manager's merge bank for any PR that changes RTL, the processor pin or the build recipe (manager ruling); it is the local half of #234's fourth criterion."
- **R3** - `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:331`, `:332`, `:335`. Fix the Issue column per ruling (e):
  - lever 2: "#230 (joins its scope)";
  - levers 3 and 6: "#639";
  - lever 5 already reads #232.
- **R4** - PR #638 body.
  - The stale passages: "Decisions needed" items 1 to 3 and 5, and the "Known limitations" bullet "making it part of the merge bar is an owner decision".
  - Fix: the rulings. (b) both places, accepted. (c) 50 MHz, met as ruled. Tolerances and ceiling are "accepted (manager ruling)". (e) the child issues are #232, #230 and #639. (a) the allocation stays open with the owner. Item 4 already matches the ruling.

### SUGGESTION

- **S1** - `syn/ooc/pp_resource_gate.py:311`, `:253`, `:292`.
  - A missing baseline file, malformed baseline JSON, a missing tolerance key at `check`, or a ceiling naming an unknown figure all exit 1 through a traceback (`probe-gate-cli.log`, cli lines).
  - Exit 1 is documented as "material regression". The gate still fails closed. Exit 2 with a `NOT COMPARABLE` line would match the documented contract.
- **S2** - `check_baseline()` (`:279-294`).
  - Deleting the route ceiling, or raising the LUT tolerance to 1e9, still passes `check-baseline` with rc 0.
  - The documented control is review of the JSON diff. Requiring the route ceiling, or pinning the policy values to AREA_BUDGET's accepted table, would make that control mechanical.
- **S3** - an improvement of any size passes silently: LUT -5000 gives rc 0.
  - When a ranked lever lands without a re-recorded baseline, later growth up to the old figure plus the tolerance goes unseen.
  - A "re-baseline recommended" line, or a downward bound, would make the ratchet follow improvements.
  - The ruling paraphrases the standalone policy as "±1 %", while the table and the gate are growth-only. Confirm that was meant.
- **S4** - `docs/findings/README.md` "Current entries" does not list `234_PP_SHADOW_AREA_BASELINE.md`. `PP_SHADOW_BASELINE.md` is not listed either.
- **S5** - optionally add arms for the low-value survivors noted under F2.

## Verified clean, with evidence

- **Measured, not mirrored, at record level** (`receipts/reconcile.log`, `receipts/evidence-manifest-verify.log`, `receipts/baseline-json-format.log`):
  - Each of the three `pp_resource_baseline.json` records equals the published A record for that endpoint: `A-record-route-1x1.json` sha256 `503ed412…`, `A-record-ooc-1x1.json` `11c00112…`, `A-record-ooc-8x8.json` `2f5e62eb…`. Each differs from B's record.
  - The file is byte-identical to the gate's `record --write` format.
  - Every cell of the shipping-route table, the standalone table, the 10 ns control sentence and both per-sub-block tables (1x1 and 8x8, A and B, with grouped instances) re-derives exactly from the records.
  - These all hold: device percentages; the 12,088-LUT NFR gap; 11,849; 121.5 = 135 - 13.5; +259 LUT under the wrapper and 366 outside it; per-context costs 212, 227, 590 and 1,031; tolerances of 0.99 to 1.03 % of their records.
  - The Yosys reconciliation sums close to the gap: 26,235 and 61,664, and both hierarchical tables add up. They match `A-1x1/8x8-yosys-vivado-mapping.tsv` and `A-ax7101-ooc-ranking.tsv`.
- **Ranking spot-check, levers 1 to 3** (plus 5), against the processor at `631eeb34`:
  - `KL_aecp_notify.sv:329`: `(* ram_style = "distributed" *) rows_r`. It is read at `:337`, at the 16-way parallel compare `:541-544`, and at `:551-552`. That read pattern explains why the attribute cannot be honoured.
  - `KL_aecp_notify.sv:392`: `ctr_last_r`. It is reset at `:934` and compared in parallel at `:1034-1037`. N_CTR_DESC_C = 2+2+2 = 6 at 1x1 and 20 at 8x8, so 192 FF.
  - `KL_srp_top.sv:947`: a 2-D `tf_ram_r`, 47-bit words, both FIFOs written in one process at `:959-968` and read at `:970-973`.
  - `protocol_processor_top.sv:2921`: `armq_r [8][4][ARM_W_C]` shift queues.
  - The Vivado-derived cone figures match `A-1x1-storage-cones.tsv`: 2,048 FF / 2,292 LUT; 2,304 FF / 648 LUT / 288 MUXF; 1,153 FF / 1,178 write-side LUT; 192 FF / 48 CARRY4.
  - Savings are labelled as estimates at `:324` and `:337`, and in the PR body.
- **The 25 PR mutants and the 51-arm self-test** (`receipts/probe-pr-mutant-reasons.log`):
  - The arm count reconciles: 33 route + 6 standalone + 11 CLI/baseline + 1 kind check = 51.
  - 23 of the 25 mutants are killed by a named arm assertion.
  - The other 2 (`Slice row`, `baseline floor presence`) are killed by a `KeyError`. The test still fails, so the result is the same.
  - The recipe's 32/32 mutants are killed, including the 4 new `--integrated-clock` mutants.
- **Planted regressions through the CLI with the real policy** (`receipts/probe-gate-cli.log`, 117 cases). Apart from F1 and S1, every case behaves as documented:
  - `route-1x1`: exit 0 at exactly +500 LUT, +600 FF, +80 SLICE, 121.5 tiles, WNS +0.030 and WHS 0.000. Exit 1 at +501, +601, +81, 122, +0.029 and -0.001, and for RAMB36, RAMB18 or DSP +1.
  - `ooc-1x1` and `ooc-8x8`: tolerances +250/+250 and +316/+339. RAMB36, RAMB18 and DSP +1 exit 1.
  - Exit 2 for: tool build, device, design, state, thread count, synthesis directive, standalone clock 10 ns, identical inputs measured differently, every missing report or inventory, a missing script, a missing or duplicate row, a non-count value, a missing timing summary, `NA` slack, an unknown endpoint and an absent directory.
- **CI wiring:**
  - The three lines are in rtl-fast's existing OOC step (`.github/workflows/rtl-fast.yml:212-214`) and in the pin (`scripts/ci_events.py:2328-2330`). `ci_events --check` and `--selftest` pass, with 2,215 arms.
  - Removing any one of the three lines from a disposable export makes `ci_events --check` exit 1 (`receipts/pin-removal-probe.log`).
  - The three lines pass in a submodule-free `git archive` export (`receipts/export-no-submodules-gate-step.log`). No Vivado, runner or tool is added.
  - Hosted `yosys-elaboration` step 9, the changed step, executed with `success` at the exact head (`receipts/hosted-yosys-elaboration-steps.txt`).
  - No make target consumes the gate. Its only consumers are the workflow step and the pin, so the GNU make 4.3 condition does not apply to the changed step.
- **Combination B left nothing behind:**
  - The diff touches only the 11 listed files.
  - The gitlinks are unchanged: `631eeb34`, `5dce647a`, `48ff7a7e`.
  - `syn/yosys/rom_digests.tsv`, `avdecc/`, `configs/`, `sw/builder/` and `docs/design/SAVED_STATE_MATERIALIZATION.md` are untouched.
  - `ddb3119d` appears only in two documentation lines.
- **Docs gates, all rc 0 under the pinned Markdown environment** (receipts `*.log`/`*.rc`): docs_check; em-dash over 541 added lines; doc style; DOC_MAP; solution docs; doc paths; archive; TOC anchors and check; py-idiom (0 over-long lines); hygiene; fail-fast; test-evidence; TODO ownership; feature status; module matrix. `git diff --check` is clean, and all 5 commits are one line with no trailers.
- **Rulings:**
  - Criterion 1: route WNS/WHS +0.063/+0.036 (A) and +0.101/+0.036 (B) at 50 MHz meet BUILDING section 5.
  - The tolerance and ceiling values in the JSON equal AREA_BUDGET's table.
  - The allocation is presented as open (AREA_BUDGET:132-133), consistent with ruling (a).
- **Probe hygiene** (`receipts/final-tree-verify.log`): after the probes, the clone is at the exact head and tree, the index tree is `09d124d8`, nothing is untracked, and all three gitlinks are clean.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | issue criteria 1-5 and lane items against the rulings; `pp_resource_baseline.json` vs published A records; `AREA_BUDGET.md:97-191`; `probe-gate-cli.log` | R446-1 | `2a765a6c3868400c20ede2e357876f28a811c811` |
| RTL | CLEAN | no `hdl/` or gitlink change (diff name list, `ls-tree`); cited lines `KL_aecp_notify.sv:329,337,392,541-544,551-552,934,1034-1037`, `KL_srp_top.sv:944-973`, `protocol_processor_top.sv:2916-2960` at `631eeb34`; `pp_baseline.py:186-193` clock derivation (50 MHz to 20.000 ns; 10 ns default unchanged) | R446-1 | `2a765a6c3868400c20ede2e357876f28a811c811` |
| Robustness | UNCLEAN (F1) | `pp_resource_gate.py:64-148,223-263,297-333` under 117 planted CLI cases; `pp_baseline.py` refusal of a missing or invalid `CLK_HZ_P` | R446-1 | `2a765a6c3868400c20ede2e357876f28a811c811` |
| Tests | UNCLEAN (F1, F2) | `pp_resource_gate_selftest.py`, `pp_resource_gate_mutants.py`, `pp_baseline_mutants.py:77-85`; 25 PR mutants classified; 23 reviewer mutants; workflow-pin removal probes | R446-1 | `2a765a6c3868400c20ede2e357876f28a811c811` |
| Docs | UNCLEAN (F3) | `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` (every table re-derived), `docs/design/AREA_BUDGET.md:97-191`, `docs/testing/PP_SHADOW_BASELINE_RECIPE.md:269-280,439-475`, PR body; docs gates | R446-1 | `2a765a6c3868400c20ede2e357876f28a811c811` |

## Real limits

- The raw Vivado reports are not in the public evidence. That covers `baseline_utilization.rpt`, `baseline_timing.rpt`, `baseline_hierarchy.rpt`, `baseline_cells.tsv` and the logs; only their SHA-256 values are in `run-receipts.json`.
- So the records could not be re-derived from the reports. The check reached the gate records, which match exactly, plus the author's `gate-check-A-*` receipts (delta 0, rc 0).
- These claims rest on unpublished files and were not verified independently: the critical paths (36 and 37 levels, 19.684 and 19.507 ns); integrated synthesis moving from 52,807 to 53,209; equality of the 1x1 elaboration parameters; agreement of the four signoff corners; the `Synth 8-7186` text; the absence of `Synth 8-4445`.
- No Vivado or Yosys run was made in this review. The builder bank is out of scope.
- The host has GNU Make 4.4.1. No make target runs the changed step, so make 4.3 was not exercised.
- Not run: `act_ci --selftest` (not permitted); `make -C gptp-processor docs` and the gPTP doc checks (submodule unchanged); the full suites.
- Hosted contexts at the time of reading: `rtl-fast` and `yosys-elaboration` succeeded. Verilator shards 1, 2 and 4, `elaborate` and `docs-check` were still in progress. `Physical gPTP` was skipped, which is not hardware proof.
- Physical calibration was NOT RUN.

## Pending manager duties

- Publish the A `route-1x1`, `ooc-1x1` and `ooc-8x8` utilization, timing and hierarchy reports with digests matching `run-receipts.json`, so a cold reviewer can re-derive the records from the reports.
- Accept or reject the hosted long contexts at the next exact head.
- Run the Vivado comparison in the merge bank for the candidate, per ruling (b).
- Validate the final current-dev candidate at the merge turn.
- Carry R1 to R4 to the residue checklist (#495) if no next round fixes them.

R446-1 FINISHED

[A527]

> **SIDE PROJECT (#649).** Measurement and analysis only. No RTL, configuration, shipping shape or gate baseline changes in this PR. It adds measurement scripts under `syn/resmap/` and one findings page.

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 2](#round-2)** -- What changed in answer to R466-1 and R467-1, item by item, and the CPU, cache and L2 prices the ruling asked for.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY (round 2): 48 of 48 local gates rc 0, and the docs workflow's builder bank rc 0 with two arms not run for their environment, at `4742d2c02c109f7dd8e21d74905efb182b2dbca2` (GNU Make 4.3, worktree clean before and after), the five self-tests PASS with their new arms (map 15 of 15), every generated (`table:`-delimited) table on the page equal to a fresh generation; `649-resource-map` -> `dev`: round 1's five commits, a `--no-ff` merge of dev `fea346e7`, and seven round-2 commits, not pushed. Side project: measurement and analysis only.

## Linked Issue / roles

Closes #649
Relates to #229 #640

Executor: `[A527]`
Internal cleared-context reviewer: `[R466]`
External reviewer: `[R467]`

## Description

Issue #649, a side project of epic #229 that feeds the #640 redesign: the whole-image resource map of the shipping image and the resource cost of every design parameter. Measurement and analysis only.

| Piece | Change |
|---|---|
| `syn/resmap/route_map.tcl` | New. Reopens a routed checkpoint (changes nothing) and writes the hierarchical utilization at depth 64 with the small-instance filter off, the flat utilization, and a census of every primitive cell with its site and BEL. |
| `syn/resmap/resmap_map.py` | New. Ranks every block (leaf of the rebuilt hierarchy) with LUT (logic, LUT RAM, SRL), FF, I/O-tile FF, RAMB36, RAMB18, DSP, CARRY4 and attributed slices, after five ties: ancestry; census (every leaf's FF, RAMB and DSP, and every row's four LUT columns, leaf or parent, against the distinct LUT sites its placed cells occupy; no cell owned outside the leaves); flat report; the `route-1x1` record (totals and all 51 processor scopes); depth. The leaves' LUT columns do not sum to the image (a LUT site holding two blocks' cells counts in both): the 17 sharing adjustments are published and each is read twice. Splits the LiteX top's own cells by name. `--selftest`: 15 arms, each caught by the tie it names. |
| `syn/resmap/sweep_plan.json` | New. 59 sweep points (`milan_datapath`, `KL_pp_shadow`, `KL_adp_engine`), 9 configuration variants, 8 SoC variants, the per-port block list for the redundancy reading. |
| `syn/resmap/yosys_sweep.py` | New. Generates variant shapes with the builder in a scratch export of `HEAD`, takes the ROM images from `syn/yosys/ooc.sh` and re-hashes every copy against the ledger, rewrites parameter defaults or package constants in scratch copies, maps each point hierarchically (anchors also flattened), lints each point with Verilator to evaluate the RTL's elaboration guards, writes the Vivado point files, and summarizes every point tied to Yosys's own design totals. Refuses a checkout with tracked changes and records HEAD and a clean tree in every receipt. `--selftest`. |
| `syn/resmap/datapath_ooc.tcl` | New. Vivado out-of-context synthesis of one point with the shipping directives, reports after synthesis and after `opt_design` at full depth. |
| `syn/resmap/soc_sweep.py` | New. Exports each SoC variant through `sw/litex/milan_soc.py` without `--build`, records the recipe's refusals, prices the CPU netlist and the stubbed LiteX top in Yosys. `--selftest`. |
| `syn/resmap/resmap_models.py`, `resmap_tables.py` | New. Fits (fixed plus per-unit, residuals; a rank-deficient design is refused), marginals, calibration; a point without a usable guard record stops the models. Renders every generated table of the page between markers, including the LUT reconciliation and the CPU, cache and L2 variant prices, and checks the page's generated tables equal a fresh generation. `--selftest` each. |
| `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md`, `docs/findings/README.md` | New page and its index row. |

No RTL, configuration, shipping shape, gate baseline, workflow or existing script changes. The tracked `sw/litex/milan_soc.py` is unchanged; the CPU, cache and L2 variants were priced from a scratch-only copy that is not committed.

Headline figures:

| Finding | Figure |
|---|---|
| Image (route-1x1 record, dev `241f9184`) | 50,767 LUT: processor 23,904 (47.1 %), rest of datapath 18,296 (36.0 %), SoC side 8,567 (16.9 %); 175 blocks, each one's LUT, FF, RAMB and DSP read from both the report and the census; totals tied to the record |
| Per stream per direction, Vivado OOC after opt (1x1, 2x2, 4x4) | +3,828 LUT, +2,911 FF, +1.5 BRAM tiles (residual RMS 394 LUT), sub-linear: 4,739 for the second stream, 3,464 each for the third and fourth; processor 2,478 LUT of it |
| Channels per stream; TDM capture width | no measurable cost |
| Low-function-cost prunes (RX filter, latency taps, loopback, probes) | up to about 1,200 routed LUT, a tenth of the 12,727-LUT NFR-RES-01 gap |
| Calibration | Vivado opt over Yosys hierarchical LUT 0.36 to 0.45 (1x1 to 8x8); route over OOC opt 0.967 |
| Refusals found | 8x8 TDM8 (235 names > 128 NVM NAME records) accepted by the builder, refused by the RTL; sv2v drops elaboration guards for Yosys |
| SoC | the recipe refuses every CPU, cache and L2 option. Priced from a scratch recipe copy, out of context after synthesis, none buildable under the shipping software profile: +1,484 LUT per core; both L1 caches +1,210; F and D on the M core +6,117 over M; NaxRiscv +14,348; no L2 is built on the shipping cacheless core. AXI-Lite bus +322 LUT (Yosys) |
| Second port (measured, nothing recommended) | at least 7,100 routed LUT and 9,918 FF of per-port blocks, plus the MAC; ADP `N_IF_P` 1 to 2: +239 LUT |

## Round 2

R466-1 and R467-1 were both NEGATIVE on MINOR findings at `da0dbc37`; neither found a wrong published figure. Assignment: issue #649 comment 5978713464.

| Item | Answer |
|---|---|
| Ruling: CPU, cache, L2 (R466-1 F6 = R467-1 F3) | Measured; acceptance 2 is kept. A scratch-only copy of the recipe with exactly the two profile refusals removed (never committed; the tracked recipe is unchanged). 23 exports, 21 generated; the CPU netlists come from scratch copies of the generators, and the shipping control is byte-equal. 20 Vivado out-of-context syntheses, one at a time under the lock, compared after synthesis because `opt_design` refuses the black-boxed datapath. Each is labelled "not buildable under the shipping software profile". CPU count 1, 2, 4: +1,484 LUT per core. L1 ways 1, 2, 4: +132 LUT and +3.5 BRAM tiles per way. L2 on the L1-cached core at 8, 16, 32 KiB: its controller is about +1,300 LUT, and its size costs only BRAM. FPU none, F, F+D on the M core. F and F+D on the shipping RV32I core cannot be generated (the FPU needs the M extension's unsigned-operand service); that is recorded with the reason, and the FPU keeps three points, so there is no STOP. XLEN and the core choice are two-valued by nature, so each is priced at two bases. Two measured no-ops: the recipe's `--with-fpu` on the VexiiRiscv path, and `--l2-bytes` on the shipping cacheless core, where the patched generator builds no L2. |
| 1 What is tied (F1 = F1) | An independent leaf-LUT reading: the census tie now counts each row's distinct LUT sites (slice, LUT letter), leaf and parent, and all 218 rows of the route equal the report's four LUT columns, so every leaf LUT figure and every sharing adjustment is read twice. Partition is stated as an identity, not a tie; five ties remain, each with a self-test arm that only it satisfies (15 arms). A scratch mutation probe disables each check in turn: 12 of 12 tie mutants killed; the two bookkeeping guards the docstring names as implied survive. R467-1's `probe_partition.py`, run unchanged, stops at its arm-A assertion because the function it stubs no longer exists (answered: Partition is an identity); its arm B, run verbatim, is caught (`census: top/leaf LUT counts 2 LUT sites, the report says 7`). The stray-owner check has an arm, and `probe_stray_owner.sh` now fails the self-test. `route_map.tcl`'s depth comment describes the check that exists. Page, README row, this body and both script headers say the same. |
| 2 The LUT sum (F2 = F5) | Generated table "The LUT reconciliation": the 175 leaves' LUT sum (51,123), each of the 17 sharing adjustments by parent beside the census's shared-site count for it (-356 in all), and the image's 50,767. "Partition" is qualified for the LUT columns in the page and the docstring. |
| 3 Growth wording (F3 = F6) | Sub-linear in both places, with the residual signs and the falling increments (processor 10,780, then 5,632, then 5,229 LUT per stream), consistent with the Vivado anchors (4,739, then 3,464). |
| 4 Consistent figures (F4 = F2) | README row: 59 points (52 guard-clean, 7 refused). One census rate, 64 lines a second (12,248 lines in 190 s, the stopped first reopen's own files), on the page and in `route_map.tcl`. |
| 5 Guard exclusion fails closed (F5 = F7) | A point with no guard record, or whose lint hit a hard error, stops `resmap_models.py` (exit 1, named). Arms: a refused point leaves the stream fit, the processor fit, the TDM model and the calibration; a missing and a hard-error record each refuse; the page check fails a stale block and a block with no table. R467-1's `probe_selftests.py`: its three F7 mutants are caught. R466-1's guard probe: the exclusion-removal mutant is killed. |
| 6 Re-runnable receipts (F4) | The small inputs and the logs of `resmap_map.py map` and `resmap_tables.py --page` are in the lane's round-2 evidence (`review-evidence/649-r2/author/` on `649-review-evidence`, once published), with a manifest of every digest; the page names that location. The census `map_cells.tsv` (12.5 MB, 540 KB compressed) is over the evidence size limit, so its digest is published and the file is kept for the manager to publish beside it; both commands read it. |
| 7 Suggestions | Taken: full rank asserted in `fit()`; HEAD and a clean-tree check in every sweep receipt (and a dirty checkout refused); the `ship-8x8` guard record published with the others. Open: a talker-only or listener-only point to split the per-stream cost by direction. |
| 8 Residue | R467-1 RES-1 to RES-5 and R466-1 RES1 to RES4, each as worded: "In the rest of the datapath"; "51 scopes, `pp_shadow` itself and 50 inside it"; "could save up to about 1,200"; "log or `stat.json` digest"; "every generated (`table:`-delimited) table" (Status above). |
| 9 Merge dev `fea346e7` | `--no-ff` merge commit; it brings only documentation and testbench files, so every figure stands at the merged head. |

## Authoritative references

- Issue #649 (scope and acceptance), its lane assignment (comment 5976977547) and the round-2 assignment and ruling (comment 5978713464).
- `docs/findings/234_PP_SHADOW_AREA_BASELINE.md` and PR #638: the round-7 route reused here, and the processor sub-blocks.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: the recipe that produced that route.
- `docs/design/AREA_BUDGET.md`: NFR-RES-01's 60 percent target, the Tier 1 optional blocks and their rules.
- `docs/reference/FR_NFR.md`: FR-CTRL-03 (at least 16 registered controllers), FR-MVU-03 and NFR-SCOUT-05 (the redundancy path kept open, #394).

## How to get into the same state

```sh
git fetch origin
git checkout 649-resource-map
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
# Tools: Vivado 2026.1, Yosys 0.66, sv2v v0.0.13, Verilator 5.050, and for the SoC exports the
# baseline recipe's LiteX environment and verified SDK (docs/testing/PP_SHADOW_BASELINE_RECIPE.md).
# The route reused here is PR #638's round-7 checkpoint, alinx_ax7101_route.dcp,
# sha256 769a04bb733f228110f99677201b5e97e4e770c53338803cd3423c9faf69f0ec.
```

The full measurement sequence is the page's "Reproducing" subsection. The CPU, cache and L2 pricing driver is scratch-only and is published with the round-2 evidence.

## How to validate

Without Vivado or Yosys (seconds):

```sh
python3 syn/resmap/resmap_map.py --selftest
python3 syn/resmap/yosys_sweep.py --selftest
python3 syn/resmap/soc_sweep.py --selftest
python3 syn/resmap/resmap_models.py --selftest
python3 syn/resmap/resmap_tables.py --selftest
```

From the round-2 evidence's `inputs/` (decompress the two `.xz` files, and place the census `map_cells.tsv` in `inputs/map/`):

```sh
python3 syn/resmap/resmap_map.py map inputs/map
python3 syn/resmap/resmap_models.py --work inputs/work --map inputs/map --out "$OUT/models"
python3 syn/resmap/resmap_tables.py --work inputs/work --models inputs/models --map inputs/map \
  --soc-variants inputs/soc_prices.json --out "$OUT/tables.md" \
  --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md
```

Expected result / pass criteria: every self-test prints PASS (the map's: "15 of 15 arms passed"); `map` prints `TIED: 175 blocks, depth 5; LUT 50767, FF 59634, slices 15832.00, CARRY4 3506, RAMB36 79, RAMB18 27, DSP 14`; the regenerated `models.json` equals the published one; the table check prints "every table equals a fresh generation" and exits 0.

## Known limitations / out of scope

- **Side project, measurement only.** Every opportunity is a recommendation with its function cost; nothing is applied, and each belongs to its own issue.
- **One route.** Only 1x1 fits the device (18 slices free; one more stream each way needs over 1,100 more slices even perfectly packed), so the only route is PR #638's round-7 route, reused. No other shape was routed.
- **Eight streams.** The 8x8 variant of the shipping TDM8 shape is refused by the RTL (235 names against the saved-state backend's 128); the tracked `endstation_ax7101_8x8` configuration is the eight-stream anchor instead. It is a different audio shape, so the Vivado per-stream fit uses 1x1, 2x2 and 4x4.
- **Yosys figures are estimates.** Hierarchical mapping, the recipe's instrument; Vivado figures decide. The Vivado anchors ran with two threads where the route used 32, on a shared host.
- **SoC variants.** The recipe's one software profile refuses every CPU, cache and L2 variant; they are priced from a scratch-only recipe copy, after synthesis with the datapath black-boxed, and none is buildable under the shipping software profile. F and F+D cannot be generated on the shipping RV32I core. No variant was routed.
- **The second port** is measured from existing blocks under one stated reading; no RTL parameter builds it, and the processor's per-interface SRP, ACMP and AECP state is not parameterized, so its cost there is not measured.
- **Not posted:** the issue's summary comment on #229 and #640 (this lane posts only on #649); a draft is in the lane's evidence.
- **Not wired into CI:** the new self-tests run by hand; adding them to a workflow would change the workflow pins.
- **Two findings for their own issues:** the Yosys flows do not enforce elaboration guards (sv2v converts them to `initial $display`); the builder accepts an AEM name count above the saved-state backend's 128.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

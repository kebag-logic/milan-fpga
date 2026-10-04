[A527]

> **SIDE PROJECT (#649).** Measurement and analysis only. No RTL, configuration, shipping shape or gate baseline changes in this PR. It adds measurement scripts under `syn/resmap/` and one findings page.

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

REVIEW READY: 46 of 46 local gates rc 0 at `da0dbc37437b58ac591467cd1b8daa9c8896cf6e` (GNU Make 4.3, worktree clean before and after), the five new self-tests PASS, every table on the page equal to a fresh generation; `649-resource-map` -> `dev`, five commits on dev `241f9184`, not pushed. Side project: measurement and analysis only.

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
| `syn/resmap/resmap_map.py` | New. Ranks every block (leaf of the rebuilt hierarchy) with LUT (logic, LUT RAM, SRL), FF, I/O-tile FF, RAMB36, RAMB18, DSP, CARRY4 and attributed slices, after seven ties: ancestry, partition, flat report, the `route-1x1` record (totals and all 51 processor scopes), census per leaf, slices, depth. Splits the LiteX top's own cells by name. `--selftest`: a consistent fixture ties; 11 planted wrong figures are each caught by name. |
| `syn/resmap/sweep_plan.json` | New. 59 sweep points (`milan_datapath`, `KL_pp_shadow`, `KL_adp_engine`), 9 configuration variants, 8 SoC variants, the per-port block list for the redundancy reading. |
| `syn/resmap/yosys_sweep.py` | New. Generates variant shapes with the builder in a scratch export of `HEAD`, takes the ROM images from `syn/yosys/ooc.sh` and re-hashes every copy against the ledger, rewrites parameter defaults or package constants in scratch copies, maps each point hierarchically (anchors also flattened), lints each point with Verilator to evaluate the RTL's elaboration guards, writes the Vivado point files, and summarizes every point tied to Yosys's own design totals. `--selftest`. |
| `syn/resmap/datapath_ooc.tcl` | New. Vivado out-of-context synthesis of one point with the shipping directives, reports after synthesis and after `opt_design` at full depth. |
| `syn/resmap/soc_sweep.py` | New. Exports each SoC variant through `sw/litex/milan_soc.py` without `--build`, records the recipe's refusals, prices the CPU netlist and the stubbed LiteX top in Yosys. `--selftest`. |
| `syn/resmap/resmap_models.py`, `resmap_tables.py` | New. Fits (fixed plus per-unit, residuals), marginals, calibration; renders every table of the page between markers, and checks the page's tables equal a fresh generation. `--selftest` each. |
| `docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md`, `docs/findings/README.md` | New page and its index row. |

No RTL, configuration, shipping shape, gate baseline, workflow or existing script changes.

Headline figures:

| Finding | Figure |
|---|---|
| Image (route-1x1 record, dev `241f9184`) | 50,767 LUT: processor 23,904 (47.1 %), rest of datapath 18,296 (36.0 %), SoC side 8,567 (16.9 %); 175 blocks tied |
| Per stream per direction, Vivado OOC after opt (1x1, 2x2, 4x4) | +3,828 LUT, +2,911 FF, +1.5 BRAM tiles (residual RMS 394 LUT); processor 2,478 LUT of it |
| Channels per stream; TDM capture width | no measurable cost |
| Low-function-cost prunes (RX filter, latency taps, loopback, probes) | about 1,200 routed LUT, a tenth of the 12,727-LUT NFR-RES-01 gap |
| Calibration | Vivado opt over Yosys hierarchical LUT 0.36 to 0.45 (1x1 to 8x8); route over OOC opt 0.967 |
| Refusals found | 8x8 TDM8 (235 names > 128 NVM NAME records) accepted by the builder, refused by the RTL; sv2v drops elaboration guards for Yosys |
| SoC | every CPU and cache option refused by the recipe's one software profile; AXI-Lite bus +322 LUT |
| Second port (measured, nothing recommended) | at least 7,100 routed LUT and 9,918 FF of per-port blocks, plus the MAC; ADP `N_IF_P` 1 to 2: +239 LUT |

## Authoritative references

- Issue #649 (scope and acceptance) and its lane assignment, comment 5976977547.
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

The full measurement sequence is the page's "Reproducing" subsection.

## How to validate

Without Vivado or Yosys (seconds):

```sh
python3 syn/resmap/resmap_map.py --selftest
python3 syn/resmap/yosys_sweep.py --selftest
python3 syn/resmap/soc_sweep.py --selftest
python3 syn/resmap/resmap_models.py --selftest
python3 syn/resmap/resmap_tables.py --selftest
```

With the measurement directories (the route reopen and a sweep work directory, as in the page's "Reproducing"):

```sh
python3 syn/resmap/resmap_map.py map "$WORK/route-map"
python3 syn/resmap/resmap_tables.py --work "$WORK/sweep" --models "$WORK/models" --map "$WORK/route-map" \
  --out "$WORK/tables.md" --page docs/findings/649_RESOURCE_MAP_AND_SENSITIVITY.md
```

Expected result / pass criteria: every self-test prints PASS (the map's: "11 of 11 arms passed"); `map` prints `TIED: 175 blocks, depth 5; LUT 50767, FF 59634, slices 15832.00, CARRY4 3506.0, RAMB36 79, RAMB18 27, DSP 14`; the table check prints "every table equals a fresh generation" and exits 0.

## Known limitations / out of scope

- **Side project, measurement only.** Every opportunity is a recommendation with its function cost; nothing is applied, and each belongs to its own issue.
- **One route.** Only 1x1 fits the device (18 slices free; one more stream each way needs over 1,100 more slices even perfectly packed), so the only route is PR #638's round-7 route, reused. No other shape was routed.
- **Eight streams.** The 8x8 variant of the shipping TDM8 shape is refused by the RTL (235 names against the saved-state backend's 128); the tracked `endstation_ax7101_8x8` configuration is the eight-stream anchor instead. It is a different audio shape, so the Vivado per-stream fit uses 1x1, 2x2 and 4x4.
- **Yosys figures are estimates.** Hierarchical mapping, the recipe's instrument; Vivado figures decide. The Vivado anchors ran with two threads where the route used 32, on a shared host.
- **SoC options.** The recipe's one software profile refuses every CPU and cache variant; pricing them would need a recipe change, which this issue does not make. The accepted bus option is priced.
- **The second port** is measured from existing blocks under one stated reading; no RTL parameter builds it, and the processor's per-interface SRP, ACMP and AECP state is not parameterized, so its cost there is not measured.
- **Not posted:** the issue's summary comment on #229 and #640 (this lane posts only on #649); a draft is in the executor's packet.
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

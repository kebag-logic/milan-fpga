[A703c]

## Contents

- **[Status](#status)** -- Ready for review at the head below; `814-soc-timing-cut` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task and roles.
- **[Description](#description)** -- The three cuts, their check, and the route set judged under #818.
- **[Authoritative references](#authoritative-references)** -- The issue, the rulings and the gate rules.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and environment.
- **[How to validate](#how-to-validate)** -- The commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- The families that set the WNS now, the record, hardware.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**GREEN** at `8b28ebaf035e786ccf5b8e50098dbc111f51831f`: the full suite sweep 64 of 64, rtl-fast all 12 jobs, the docs workflow gates, the builder bank; `814-soc-timing-cut` -> `dev` (`1e80128f`).

- **The route set passes the resource gate under #818** (PR #820's gate at `32f0d9b5`, exit 0). It selects ExtraPostPlacementOpt, the shipping directive, at +0.128 ns. That directive meets the build floor at every signoff corner. The 0.312 ns fall from the +0.440 ns record prints as a WARNING.
- **Every resource figure is within tolerance**: LUT -185, FF +315, slices -16; RAMB36, RAMB18 and DSP unchanged.
- **The record is not re-recorded in this PR.** It is re-recorded once on dev after the last release merge, from the release image's three-directive routes (issuecomment-6525285974).

## Linked Issue / roles

Closes #814
Relates to #818

Executor: `[A703c]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Three families of `sys`-domain paths set the route WNS at dev `1e80128f`. Each cut is a register boundary in the SoC wiring, all in `sw/litex/milan_soc.py`. There is no LiteX patch, no pblock, and no floor or fall exception. The recipe and its directives are unchanged (the #708 ruling).

| Family | Boundary | Cost alone (LUT / FF / slices) | In context, against a control without it (LUT / FF) | Added access latency (sys cycles) |
|---|---|---|---|---|
| F1 bridge -> SPI-flash PHY | `SPIPHYStage` (`sw/litex/milan_soc.py:2465`), between LiteSPI's core and its PHY: registered command and data streams and chip select, installed by `MilanSoC.add_spi_flash` (`:3670`) | 54 / 199 / 49 | +24 to +47 / +173 to +179 | +2 a word in a burst, +8 a new burst |
| F2 LiteDRAM arbitration -> crossing FIFO | `AXIReadyStage` (`:2397`): registered READY on the CPU memory port's aw and ar, between its crossing and LiteDRAM (`cross_cpu_memory_ports`, `:2391`) | 78 / 150 / 39 | 88 FFs named in the netlist | 0 |
| F3 ZQCS timer -> bank machines | `RegisteredRefresher` (`:2430`): LiteDRAM's own refresher with `cmd.valid` and `cmd.last` registered, through `ControllerSettings.refresh_cls` (`add_staged_sdram`, `:2454`) | +0 / +2 / - | 3 FFs named | 0; a refresh runs one cycle later |

**The check.** `sw/litex/test_soc_timing_cuts.py` is a new LiteX simulation in the pinned inventory (`scripts/run_litex_sims.sh`). It builds each path on the real LiteX, LiteSPI and LiteDRAM code through the shipping call, and walks the elaborated netlist back from each endpoint. With a stage replaced by wires, or with LiteDRAM's own refresher, it must fail. The failure must name the bridge state into the PHY counter, the burst-to-beat counter into the FIFO address, or a refresh timer into a bank machine's FIFO level. Its behaviour arms check the flash data, the exact added cycles and chip-select alignment. They also check LiteDRAM's native-port handshakes cycle for cycle, and that the DFI refresh commands arrive one cycle later.

**Route-1x1 at the head**, recipe unchanged, at the recipe's three placement directives. The two comparison directives reuse the shipping run's synthesis checkpoint, default seed. Dev's figures are its own routes on the same bank.

| Directive | WNS / WHS ns, worst corner (dev) | F1 | F2 | F3 | F4 | LUT / FF / slices |
|---|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt (**selected**) | **+0.128** / +0.030 (+0.303) | +2.386 | +1.162 | not in the 5,000 worst | +0.324 | 51,827 / 54,022 / 15,764 |
| AltSpreadLogic_high | +0.039 / +0.029 (+0.230) | +2.110 | +1.460 | +4.379 | +0.039 | 51,895 / 54,024 / 15,839 |
| ExtraTimingOpt | +0.010 / +0.029 (+0.106) | +2.228 | +1.380 | not in the 5,000 worst | +0.059 | 51,882 / 54,029 / 15,839 |

- At dev, F1 to F3 were +0.106 to +0.816 ns. Now each sits more than 1 ns from the worst path at every directive.
- **The #818 judgement.** The gate selects the directive with the best worst-corner WNS, ExtraPostPlacementOpt. Its slow corners give +0.128 / +0.059 ns WNS / WHS and its fast corners +1.311 / +0.030 ns, all at or above the +0.030 / 0 ns floor. ExtraTimingOpt misses the floor at its slow corners (+0.010 ns). It is not selected, so the set does not fail on it.
- **The ruling's reason for the cuts.** The release integration without this change misses the floor on this change's own LiteDRAM families: +0.003 ns at ExtraPostPlacementOpt and -0.220 ns at AltSpreadLogic_high. The integration that included it routed at +0.236 ns.

| Touched | Change |
|---|---|
| `sw/litex/milan_soc.py` | `SPIPHYStage`, `stage_spi_phy`, `MilanSoC.add_spi_flash`; `AXIReadyStage` in `cross_cpu_memory_ports`; `RegisteredRefresher`, `add_staged_sdram` |
| `sw/litex/test_soc_timing_cuts.py` | the new simulation, 15 arms |
| `scripts/run_litex_sims.sh`, `ci/image/exec-audit.json` | the inventory entry and its generated stand-in |
| `docs/testing/TESTING.md`, `docs/litex/CLOCK_DOMAINS.md` | the new member; the CPU DDR crossing's stage |

## Authoritative references

- Issue #814 (body corrected 2026-10-30) and the round-3 ruling (issuecomment-6527475726), which returns it to the release.
- #818: the resource gate judges WNS and WHS on the build floor at every corner of the best of the three directives, and prints the fall from the record as a WARNING. Implemented by PR #820.
- The record rule for the release (issuecomment-6525285974): the record is re-recorded once on dev after the last release merge, and a record that does not yet carry this route is not a finding here.
- The F4 ruling (issuecomment-6516396929) and the #708 ruling (issuecomment-6100507393): logic cut in the SoC wiring, recipe unchanged, no pblocks, no floor exception.
- `docs/integration/BUILDING.md` section 5: WNS at least +0.030 ns and WHS at least 0 at every corner.
- `docs/design/AREA_BUDGET.md` and `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: the resource gate's policy, the recipe and its three-directive comparison.

## How to get into the same state

```sh
git fetch origin
git checkout 814-soc-timing-cut
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
python3 -m pip install -r sw/litex/litex_pins.txt
python3 scripts/ci_litex_env.py
sw/litex/patches/apply.sh
```

## How to validate

```sh
cd sw/litex && PYTHONHASHSEED=0 python3 test_soc_timing_cuts.py
scripts/run_litex_sims.sh --selftest
scripts/run_litex_sims.sh "$(mktemp -d)"
python3 scripts/check_nvm_capture.py
python3 sw/builder/test_builder.py
bash scripts/run_all_suites.sh "$(mktemp -d)" --wait
```

Expected: `RESULT: PASS` (15 arms); the aggregate's self-test 10 of 10 and the aggregate 8 of 8; the capture gate PASS; the builder bank `ALL GATES PASS EXCEPT 2 NOT RUN`, the same two arms dev's bank does not run; the sweep `suites: 64 passed: 64 failed: 0` (four shards: 14, 17, 17, 16).

The route evidence follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, unchanged: route-1x1 at the three directives, the comparisons from the shipping run's synthesis checkpoint. Judge the route set with #818's gate (PR #820):

```sh
python3 syn/ooc/pp_resource_gate.py check <route-dir> --endpoint route-1x1 \
  --comparison <route-dir-AltSpreadLogic_high> --comparison <route-dir-ExtraTimingOpt>
python3 syn/ooc/pp_resource_gate.py check <ooc-1x1-dir> --endpoint ooc-1x1
python3 syn/ooc/pp_resource_gate.py check <ooc-8x8-dir> --endpoint ooc-8x8
```

At the head all three exit 0. The first selects ExtraPostPlacementOpt and prints the WNS fall as a WARNING. Both standalone figures equal the record: 24,346 / 20,404 and 34,156 / 29,782 LUT / FF.

The capture recipe in `tb/verilator/nvm_capture_cpu/README.md` runs six arms and three controls, all exit 0. The worst contract-clock capture is 13.85922 ms, 10.64 ms under the 24.5 ms bound. The service-budget runs (plan `all`, `--populated --enforce-service`, 1x1 and 8x8) both `PASS` with no service finding.

## Known limitations / out of scope

- **What sets the WNS now.** With F1 to F3 cut, the WNS goes to whichever of at least six families draws the worst placement. This change touches none of them: F4 inside the CPU, the processor memory bridges into the CPU DMA port's write arbitration, the milan-domain reset into the MMCM servo's 200 MHz reset synchroniser, the AECP micro-CPU, LiteEth TX and the LiteDRAM bank machines. Each had more slack at dev. Cutting them is new scope. The reset synchroniser crossing is a CDC-constraint question in `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv`, outside the SoC wiring.
- F4 is accepted by the owner ruling and is not cut.
- **The record** still holds dev's +0.440 ns route. It is re-recorded on dev after the last release merge, not here.
- **The flash stage has not been on hardware.** The simulations that boot through it use LiteSPI's model PHY or a device boundary, never the real PHY with a pad-level flash.
- LiteDRAM issues a ZQCS only when its one-cycle ZQCS timer pulse meets the end of a refresh. That is upstream behaviour, unchanged here.
- One seed per directive, as the recipe prescribes. Unchanged logic moved 0.3 to 0.57 ns between routes on this lane.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
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

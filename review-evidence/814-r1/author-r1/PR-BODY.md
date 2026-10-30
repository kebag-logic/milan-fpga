[A703]

## Contents

- **[Status](#status)** -- STOP at the head below: route-8x8 does not fit; `814-soc-timing-cut` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task and roles.
- **[Description](#description)** -- The measurement, the three cuts, where each sits and what it costs.
- **[Authoritative references](#authoritative-references)** -- The issue, the ruling and the gate rules.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and environment.
- **[How to validate](#how-to-validate)** -- The commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- The STOP, the uncut family and what did not run.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**STOP** at `8b28ebaf035e786ccf5b8e50098dbc111f51831f`; `814-soc-timing-cut` -> `dev` (`1e80128f`). Not ready for review.

- **Route-8x8 does not fit the device.** At `139949e2`, the 8x8 export at its own place directive (AltSpreadLogic_high), recipe unchanged, completes `opt_design`, then DRC UTLZ-1 refuses placement. It needs 70,686 LUT-as-logic cells against 63,400 sites (7,286 over). The three stages here cost about 132 LUTs out of context. The 8x8 recipe has never produced a bitstream (`docs/integration/BUILDING.md`), so the issue's route-8x8 acceptance needs an owner decision.
- The head's route-1x1 has not run. The full sweep, rtl-fast, the docs gates, the builder bank, the capture re-measurement and the resource re-record did not run either.

## Linked Issue / roles

Closes #814

Executor: `[A703]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

**Measured first.** Dev `1e80128f`, route-1x1 at the unchanged recipe with its three placement directives: the worst `sys` paths fall in four families.

| Directive | WNS ns | Worst family | F1 flash | F2 LiteDRAM -> crossing FIFO | F3 ZQCS timer -> bank machines | F4 CPU DMA write bridge |
|---|---:|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt (shipping) | +0.303 | F3 | +0.627 | +0.689 | +0.303 | +0.603 |
| AltSpreadLogic_high | +0.230 | F2 | +0.816 | +0.230 | +0.432 | +0.353 |
| ExtraTimingOpt | +0.106 | F2 | +0.784 | +0.106 | +0.572 | +0.686 |

F3 and F4 are within 0.3 ns of the named families, so both joined the scope. F4 runs entirely inside the generated CPU netlist, so no stage in the SoC wiring reaches it; it is reported, not cut.

**The cuts**, all in `sw/litex/milan_soc.py`, no LiteX patch, recipe and directives unchanged:

| Family | Boundary | Cost alone (LUT / FF / slices) | Added access latency (sys cycles) |
|---|---|---|---|
| F1 bridge -> SPI-flash PHY | `SPIPHYStage` between LiteSPI's core and its PHY: registered command and data streams (LiteX `stream.Buffer`) and chip select, installed by `MilanSoC.add_spi_flash` | 54 / 199 / 49 | +2 a word in a burst, +8 a new burst |
| F2 LiteDRAM arbitration -> crossing FIFO | `AXIReadyStage`: LiteX `PipeReady` on the CPU memory port's aw and ar between its crossing and LiteDRAM | 78 / 150 / 39 | 0 |
| F3 ZQCS timer -> bank machines | `RegisteredRefresher`: LiteDRAM's own refresher with `cmd.valid` and `cmd.last` registered, through `ControllerSettings.refresh_cls` | +0 / +2 / - | 0; a refresh runs one cycle later |

The issue's first option, a registered Wishbone stage in front of the flash core (`cd83cd16`), was routed. It left the path 17 levels long from the stage's own address register into the PHY counter, at +0.254 ns, 0.001 ns from the worst path. Most of the path is LiteSPI's burst compare, its mmap FSM and the PHY's counter. So `8b28ebaf` moves the boundary between the core and the PHY and removes the Wishbone stage.

**The check.** `sw/litex/test_soc_timing_cuts.py`, a new LiteX simulation in the pinned inventory, builds each path on the real LiteX, LiteSPI and LiteDRAM code through the shipping call. It walks the elaborated migen netlist back from each endpoint. Built with the stage replaced by wires, or by LiteDRAM's own refresher, it must fail, naming the bridge state into the PHY counter, the burst-to-beat counter into the FIFO address and a refresh timer into a bank machine's FIFO level. Its behaviour arms grade the flash data and its exact added cycles, chip-select alignment, LiteDRAM's native-port handshakes cycle for cycle and the DFI refresh commands one cycle later.

| Touched | Change |
|---|---|
| `sw/litex/milan_soc.py` | `SPIPHYStage`, `stage_spi_phy`, `MilanSoC.add_spi_flash`; `AXIReadyStage` in `cross_cpu_memory_ports`; `RegisteredRefresher`, `add_staged_sdram` |
| `sw/litex/test_soc_timing_cuts.py` | the new simulation, 15 arms |
| `scripts/run_litex_sims.sh`, `ci/image/exec-audit.json` | the inventory entry and its generated stand-in |
| `docs/testing/TESTING.md`, `docs/litex/CLOCK_DOMAINS.md` | the new member; the CPU DDR crossing's stage |

## Authoritative references

- Issue #814 and its assignment (issuecomment-6514717735); the #708 ruling for this class of route miss (issuecomment-6100507393).
- `docs/integration/BUILDING.md` section 5: WNS at least +0.030 ns and WHS at least 0 at every corner.
- `docs/design/AREA_BUDGET.md`: the resource gate's policy; the 8x8 standalone record is synthesis only.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: the recipe, its three-directive comparison and the resource gate.
- `docs/litex/CLOCK_DOMAINS.md`: the #359 CPU memory crossing the F2 stage follows.

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
python3 scripts/check_py_idiom.py
python3 scripts/check_doc_style.py
python3 scripts/check_nvm_capture.py
```

Expected: `test_soc_timing_cuts: 0 failure(s)` and `RESULT: PASS` (15 arms); the aggregate's self-test 10 of 10 and the aggregate 8 of 8 members; the idiom and style gates within every ratchet; the capture gate PASS.

The route evidence follows the recipe in `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, unchanged: route-1x1 at dev and at `cd83cd16`, each with `python3 syn/ooc/pp_resource_gate.py check <dir> --endpoint route-1x1` (PASS both); route-8x8 at `139949e2` refused at placement by DRC UTLZ-1.

## Known limitations / out of scope

- **The STOP: route-8x8 does not fit** (70,686 LUTs for 63,400 sites), independent of this change. The acceptance's route-8x8 half needs an owner decision.
- **F4, the CPU's DMA write bridge, is not cut.** It was 0.123 ns from F2 at AltSpreadLogic_high and the worst path at `cd83cd16` (+0.253 ns). Every cell is in the generated CPU netlist, so a boundary there needs a CPU-generator change, outside the ruling's SoC wiring.
- The head's flash boundary is graded in simulation, not yet routed; its in-context slice cost with 16 slices free on dev's route is unmeasured.
- Not run, by the STOP: the full sweep, rtl-fast, the docs gates, the builder bank, the capture re-measurement and the flash-boot simulations, route-1x1 and the standalone endpoints at the head, the resource gate at the head and the re-record. Flash boot on hardware was out of reach of this lane.
- LiteDRAM issues a ZQCS only when its one-cycle ZQCS timer pulse meets the end of a refresh, so ZQCS is rare in hardware. That is upstream behaviour, unchanged here.

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

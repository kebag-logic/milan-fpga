[A703b]

## Contents

- **[Status](#status)** -- STOP at the head below: the shipping route fails the resource gate's WNS limit; `814-soc-timing-cut` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task and roles.
- **[Description](#description)** -- The three cuts, the head's routes at three directives, the control without the flash stage.
- **[Authoritative references](#authoritative-references)** -- The issue, the rulings and the gate rules.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and environment.
- **[How to validate](#how-to-validate)** -- The commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- The STOP, the families that set the WNS now and what did not run.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**STOP** at `8b28ebaf035e786ccf5b8e50098dbc111f51831f`; `814-soc-timing-cut` -> `dev` (`1e80128f`). Not ready for review.

- **The shipping route fails `pp_resource_gate.py check`, exit 1.** WNS is +0.128 ns against the +0.440 ns record, a 0.312 ns fall against the 0.25 ns limit. Every resource figure passes.
- **Its worst path is a family outside F1 to F4.** The milan-domain reset drives the MMCM servo's 200 MHz reset synchroniser. Five more families outside F1 to F4 lie within 0.3 ns of it.
- **The ExtraTimingOpt comparison route misses the +0.030 ns floor** (+0.010 ns).
- As a result, the record is not re-recorded, and the full sweep, rtl-fast, the docs gates and the builder bank have not run.

## Linked Issue / roles

Closes #814

Executor: `[A703b]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

**The cuts**, all in `sw/litex/milan_soc.py`. There is no LiteX patch, and the recipe and directives are unchanged.

| Family | Boundary | Cost alone (LUT / FF / slices) | In context, against the control (LUT / FF) | Added access latency (sys cycles) |
|---|---|---|---|---|
| F1 bridge -> SPI-flash PHY | `SPIPHYStage`, between LiteSPI's core and its PHY: registered command and data streams (LiteX `stream.Buffer`) and chip select, installed by `MilanSoC.add_spi_flash` | 54 / 199 / 49 | +24 to +47 / +173 to +179 | +2 a word in a burst, +8 a new burst |
| F2 LiteDRAM arbitration -> crossing FIFO | `AXIReadyStage`: LiteX `PipeReady` on the CPU memory port's aw and ar, between its crossing and LiteDRAM | 78 / 150 / 39 | 88 FFs named in the netlist | 0 |
| F3 ZQCS timer -> bank machines | `RegisteredRefresher`: LiteDRAM's own refresher with `cmd.valid` and `cmd.last` registered, through `ControllerSettings.refresh_cls` | +0 / +2 / - | 3 FFs named | 0; a refresh runs one cycle later |

**The check.** `sw/litex/test_soc_timing_cuts.py` is a new LiteX simulation in the pinned inventory. It builds each path on the real LiteX, LiteSPI and LiteDRAM code through the shipping call, and walks the elaborated migen netlist back from each endpoint. Built with a stage replaced by wires, or by LiteDRAM's own refresher, it must fail. The failures must name the bridge state into the PHY counter, the burst-to-beat counter into the FIFO address, and a refresh timer into a bank machine's FIFO level. Its behaviour arms grade the flash data and its exact added cycles, and chip-select alignment. They grade LiteDRAM's native-port handshakes cycle for cycle, and the DFI refresh commands one cycle later.

**Route-1x1 at the head**, recipe unchanged, with its three placement directives. The comparison directives reuse the shipping run's synthesis checkpoint, default seed. Families come from the 5,000 worst endpoints over every path group. Dev's figures are its own routes on the same bank.

| Directive | WNS / WHS ns (dev) | Worst family | F1 | F2 | F3 | F4 | LUT / FF / slices |
|---|---|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt | **+0.128** / +0.030 (+0.303) | milan reset -> MMCM servo PS reset synchroniser, 1 LUT, 86 % routing | +2.386 | +1.162 | not in the 5,000 | +0.324 | 51,827 / 54,022 / 15,764 |
| AltSpreadLogic_high | +0.039 / +0.029 (+0.230) | F4, CPU DMA write bridge, 19 levels | +2.110 | +1.460 | +4.379 | +0.039 | 51,895 / 54,024 / 15,839 |
| ExtraTimingOpt | **+0.010** / +0.029 (+0.106) | `ws0` -> the CPU DMA port's write arbitration -> NVM bridge FSM, 17 levels | +2.228 | +1.380 | not in the 5,000 | +0.059 | 51,882 / 54,029 / 15,839 |

At dev, F1 to F3 were +0.106 to +0.816 ns. Now each sits more than 1 ns from the worst path. The WNS is set by families this change does not touch. Each had more slack at dev.

**The control** is the head with `SPIPHYStage` replaced by wires, for measurement only and never committed. It routed at +0.168 / +0.342 / +0.300 ns. Without the stage, F1 has +0.677 / +0.614 / +0.300 ns and is the worst path at ExtraTimingOpt. The control's shipping route also fails the gate: a 0.272 ns fall, with a milan-domain path outside F1 to F4.

| Touched | Change |
|---|---|
| `sw/litex/milan_soc.py` | `SPIPHYStage`, `stage_spi_phy`, `MilanSoC.add_spi_flash`; `AXIReadyStage` in `cross_cpu_memory_ports`; `RegisteredRefresher`, `add_staged_sdram` |
| `sw/litex/test_soc_timing_cuts.py` | the new simulation, 15 arms |
| `scripts/run_litex_sims.sh`, `ci/image/exec-audit.json` | the inventory entry and its generated stand-in |
| `docs/testing/TESTING.md`, `docs/litex/CLOCK_DOMAINS.md` | the new member; the CPU DDR crossing's stage |

## Authoritative references

- Issue #814 (body corrected 2026-10-30) and its assignments: issuecomment-6514717735 and the round 2 ruling issuecomment-6517931276.
- The F4 ruling (issuecomment-6516396929) and the #708 ruling for this class of route miss (issuecomment-6100507393).
- `docs/integration/BUILDING.md` section 5: WNS at least +0.030 ns and WHS at least 0 at every corner.
- `docs/design/AREA_BUDGET.md`: the resource gate's policy, a 0.25 ns timing fall against the +0.440 ns record.
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`: the recipe, its three-directive comparison and the resource gate.

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
```

Expected: `RESULT: PASS` (15 arms); the aggregate's self-test 10 of 10 and the aggregate 8 of 8; the capture gate PASS.

The route evidence follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, unchanged. Route-1x1 runs at the three directives, then:

```sh
python3 syn/ooc/pp_resource_gate.py check <route-dir> --endpoint route-1x1
python3 syn/ooc/pp_resource_gate.py check <ooc-1x1-dir> --endpoint ooc-1x1
python3 syn/ooc/pp_resource_gate.py check <ooc-8x8-dir> --endpoint ooc-8x8
```

At the head these exit 1, 0 and 0. Both standalone figures equal the record.

The capture recipe in `tb/verilator/nvm_capture_cpu/README.md` runs six arms and three controls, all exit 0. The worst contract-clock capture is 13.85922 ms, 10.64 ms under the 24.5 ms bound.

## Known limitations / out of scope

- **The STOP.** With F1 to F3 cut, the WNS goes to whichever of at least six families this change does not touch draws the worst placement: F4, the memory bridges into the CPU DMA port, the milan reset crossing, the AECP micro-CPU, LiteEth TX, the LiteDRAM bank machines. The gate binds at +0.190 ns. The decision belongs to the owner.
- F4 is accepted by the owner ruling and is not cut.
- The head's flash stage has not been on hardware. The simulations that boot through it use LiteSPI's model PHY or a device boundary, never the real PHY with a pad-level flash.
- Not run, by the STOP: the re-record and its documentation, the full sweep, rtl-fast, the docs gates, the builder bank.
- LiteDRAM issues a ZQCS only when its one-cycle ZQCS timer pulse meets the end of a refresh. That is upstream behaviour, unchanged here.

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

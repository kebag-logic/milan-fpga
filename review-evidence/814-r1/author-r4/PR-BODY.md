[A703d]

## Contents

- **[Status](#status)** -- Ready for review at the head below; `814-soc-timing-cut` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task and roles.
- **[Description](#description)** -- The three cuts, the ZQCS fix, their checks, and the route set judged under #818.
- **[Authoritative references](#authoritative-references)** -- The issue, the rulings and the gate rules.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and environment.
- **[How to validate](#how-to-validate)** -- The commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What sets the WNS now, the record, hardware, the test's runtime.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**GREEN** at `4ee2aa9654196a00876dedade4b2e987c9c06e64` the full suite sweep 64 of 64, rtl-fast all 12 jobs, the docs workflow gates, the builder bank, the LiteX aggregate 8 of 8. Branch `814-soc-timing-cut` -> `dev`.

- **The route set passes the resource gate under #818** (PR #820's gate at `50e5d08d`, exit 0), routed at `0d4a899f`.
  - The gate selects ExtraTimingOpt at +0.406 ns.
  - All three directives meet the build floor at every signoff corner: ExtraPostPlacementOpt +0.322 ns, AltSpreadLogic_high +0.126 ns, ExtraTimingOpt +0.406 ns.
  - The fall from the +0.440 ns record is 0.034 ns, so no WARNING is printed.
  - `0d4a899f..4ee2aa96` changes only the test and TESTING.md, which the build does not read.
- **Every resource figure is within tolerance**: LUT -119, FF +320, slices +31; RAMB36, RAMB18 and DSP unchanged.
- **The record is not re-recorded in this PR** (issuecomment-6525285974).

## Linked Issue / roles

Closes #814
Relates to #818

Executor: `[A703d]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

Three families of `sys`-domain paths set the route WNS at dev `1e80128f`. Each cut is a register boundary in the SoC wiring, all in `sw/litex/milan_soc.py`. There is no LiteX patch, no pblock, and no floor or fall exception. The recipe and its directives are unchanged (the #708 ruling).

| Family | Boundary | Added access latency (sys cycles) |
|---|---|---|
| F1 bridge -> SPI-flash PHY | `SPIPHYStage` (`sw/litex/milan_soc.py:2483`), installed by `MilanSoC.add_spi_flash` (`:3688`): registered command and data streams and chip select between LiteSPI's core and its PHY | +2 a word in a burst, +8 a new burst |
| F2 LiteDRAM arbitration -> crossing FIFO | `AXIReadyStage` (`:2397`): registered READY on the CPU memory port's aw and ar, between its crossing and LiteDRAM (`cross_cpu_memory_ports`) | 0 |
| F3 ZQCS timer -> bank machines | `RegisteredRefresher` (`:2430`): LiteDRAM's own refresher with `cmd.valid` and `cmd.last` registered, through `ControllerSettings.refresh_cls` (`add_staged_sdram`) | 0; each refresh and each ZQCS one cycle later |

**ZQCS.** Registering the refresh request delays the controller's grant, and every refresh sequence's end, by one cycle. LiteDRAM's ZQCS timer is not delayed. LiteDRAM starts a ZQCS only when that timer's one-cycle pulse lands on a sequence end.

At the board's 100 MHz on its DDR3, tREFI is 782 cycles and the ZQCS period is 10^8, with gcd 2. So the undelayed pulse fell on the other parity, and an idle controller never issued ZQCS. LiteDRAM's own refresher issues its first after 76 s.

`RegisteredRefresher` now holds the ZQCS timer in reset one cycle longer (`:2466-2469`). On an idle controller every DFI command, precharge-all, REFRESH and ZQCS, is LiteDRAM's own exactly one cycle later. That holds for the first ZQCS and for the ones after the timer re-phases. Under traffic, whether a ZQCS coincides depends on the traffic, with or without the stage.

**The check.** `sw/litex/test_soc_timing_cuts.py` is a LiteX simulation in the pinned inventory (`scripts/run_litex_sims.sh`). It builds each path on the real LiteX, LiteSPI and LiteDRAM code through the shipping call. It has 23 checks:

- **Structure.** It walks the elaborated netlist back from each endpoint. With a stage replaced by wires, or with LiteDRAM's own refresher, the walk must fail. The failure must name:
  - the bridge state into the PHY counter (F2's starts are taken from the bridge's own registers);
  - the burst-to-beat counter into the FIFO address;
  - a refresh timer into a bank machine's FIFO level.
- **Behaviour without stalls.** The flash data, the exact added cycles and chip-select alignment. LiteDRAM's native-port handshakes, cycle for cycle. The refresh commands one cycle later.
- **ZQCS (Z4, Z5).** With a 6-cycle ZQCS period, which keeps the shipping gcd of 2 with tREFI:
  - the staged DFI commands equal LiteDRAM's own one cycle later, through two ZQCS (2411 and 3193 against 2410 and 3192);
  - the stage without the delay issues none there, and fails.
- **Stalls (F6, F7, D5 to D7).** Each stage's outputs are stalled at random:
  - the flash PHY's command READY also waits behind LiteSPI's own `LiteSPICSControl`, at the cs_delay the shipping PHY uses;
  - the core's flash data READY and LiteDRAM's aw and ar READY are random, under back-to-back traffic.

  In each case every registered READY must hold beats, the transfers must be the issued ones in order, and VALID and payload must hold until taken. A planted lossy registered READY on each stream must fail.

| Touched | Change |
|---|---|
| `sw/litex/milan_soc.py` | `SPIPHYStage`, `stage_spi_phy`, `MilanSoC.add_spi_flash`; `AXIReadyStage` in `cross_cpu_memory_ports`; `RegisteredRefresher` (with the ZQCS timer's start), `add_staged_sdram` |
| `sw/litex/test_soc_timing_cuts.py` | the simulation, 23 checks |
| `scripts/run_litex_sims.sh`, `ci/image/exec-audit.json` | the inventory entry and its generated stand-in |
| `docs/testing/TESTING.md`, `docs/litex/CLOCK_DOMAINS.md` | the member and its arms; the CPU DDR crossing's stage |

**Route-1x1**, recipe unchanged, at the recipe's three placement directives. The two comparison directives reuse the shipping run's synthesis checkpoint, default seed.

| Directive | WNS / WHS ns, worst corner | F1 | F2 | F3 | F4 | LUT / FF / slices |
|---|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt | +0.322 / +0.031 | +2.721 | +1.607 | not in the 5,000 worst | +0.322 | 51,864 / 54,024 / 15,840 |
| AltSpreadLogic_high | +0.126 / +0.035 | +2.085 | +1.392 | not in the 5,000 worst | +0.126 | 51,895 / 54,027 / 15,812 |
| ExtraTimingOpt (**selected**) | **+0.406** / +0.036 | +1.723 | +1.472 | not in the 5,000 worst | +0.453 | 51,893 / 54,027 / 15,811 |

- F1 to F3 each sit more than 1 ns from the worst path at every directive.
- The selected route's corners:
  - Slow 0C / 85C: WNS +0.406, WHS +0.099 ns;
  - Fast 0C / 85C: WNS +1.583, WHS +0.036 ns.
- The worst path at ExtraTimingOpt is a milan-domain reset net into LiteEth MAC status registers (0 levels, 96 % routing). At the other two directives it is F4.

## Authoritative references

- Issue #814 and its rulings:
  - issuecomment-6527475726, which returns it to the release;
  - the round-4 ruling (ZQCS option (a), the stall arms, the re-route judged by #818).
- The reviews this round answers: issuecomment-6532204298 and issuecomment-6532064254.
- #818: the resource gate judges WNS and WHS against the build floor at every corner of the best of the three directives, and prints the fall from the record as a WARNING. Implemented by PR #820.
- The record rule for the release (issuecomment-6525285974).
- The F4 ruling (issuecomment-6516396929) and the #708 ruling (issuecomment-6100507393): a logic cut in the SoC wiring, recipe unchanged, no pblocks, no floor exception.
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
python3 sw/builder/test_builder.py
bash scripts/run_all_suites.sh "$(mktemp -d)" --wait
```

Expected results:

- `test_soc_timing_cuts.py`: `RESULT: PASS`, 23 checks. It takes about 590 s of CPU here, inside the aggregate's 900 s member limit.
- The aggregate's self-test: 10 of 10. The aggregate: 8 of 8.
- The builder bank: `ALL GATES PASS EXCEPT 2 NOT RUN`, the same two arms dev's bank does not run on this host.
- The sweep: `suites: 64 passed: 64 failed: 0` (four shards: 14, 17, 17, 16).

The route evidence follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, unchanged: route-1x1 at the three directives, the comparisons from the shipping run's synthesis checkpoint. Judge the route set with #818's gate (PR #820):

```sh
python3 syn/ooc/pp_resource_gate.py check <route-dir> --endpoint route-1x1 \
  --comparison <route-dir-AltSpreadLogic_high> --comparison <route-dir-ExtraTimingOpt>
```

At `0d4a899f` it exits 0 and selects ExtraTimingOpt at +0.406 ns.

## Known limitations / out of scope

- **What sets the WNS now.** With F1 to F3 cut, the WNS goes to whichever of several families draws the worst placement: F4 inside the CPU, the milan-domain reset nets, the memory bridges into the CPU DMA port, the LiteDRAM bank machines. This change touches none of them. Cutting them is new scope. F4 is accepted by the owner ruling and is not cut.
- **The record** still holds dev's +0.440 ns route. It is re-recorded on dev after the last release merge, not here.
- **The flash stage has not been on hardware.**
  - The simulations that boot through it use LiteSPI's model PHY or a device boundary, never the real PHY with a pad-level flash.
  - The real PHY cannot be elaborated in migen simulation. The stall arm reproduces its chip-select hold with LiteSPI's own `LiteSPICSControl`.
- **ZQCS under traffic.** Both LiteDRAM's refresher and this one issue ZQCS only when the timer pulse meets a sequence end, so under traffic it depends on the traffic. Only the idle behaviour is graded, and there it is LiteDRAM's own, one cycle later.
- **The DRAM arms grade transfers, not read data.** On the test's model PHY setup the DFI write burst goes out masked, so every read returns zero with or without the stage.
- **The test's runtime** rose from about 405 s to about 590 s of CPU. The aggregate allows 900 s per member.
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

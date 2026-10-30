[A709]

## Contents

- **[Status](#status)** -- Review ready, with the resource gate's WNS verdict for a ruling; `817-servo-reset-cdc` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- The task and roles.
- **[Description](#description)** -- The cut, the attribute, the checks, the crossing before and after, the route.
- **[Authoritative references](#authoritative-references)** -- The issue, the constraint contract and the gate rules.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Checkout and environment.
- **[How to validate](#how-to-validate)** -- The commands and the expected results.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- The open questions and what did not run.
- **[Definition of Done](#definition-of-done)** -- The merge bar from CONTRIBUTING.md.

## Status

**REVIEW READY** at `6cfb27dacafb2e5b693412db3342ca0fccc9c0bc`; `817-servo-reset-cdc` -> `dev` (`1e80128f`).

- The crossing is cut and no longer timed as a synchronous path. The constraint report shows it applied, and every other exception is unchanged.
- Route-1x1 at the shipping directive meets the floor at every corner: WNS +0.166 / +0.166 ns slow, +1.481 / +1.481 ns fast; WHS +0.055 / +0.055 ns slow, +0.020 / +0.020 ns fast.
- **`pp_resource_gate.py check --endpoint route-1x1` exits 1, on WNS alone**: 0.44 -> 0.166 ns, a 0.274 ns fall against the 0.25 ns limit. Every resource figure passes. This is reported for the WNS ruling.
- Gates: the constraint-presence check passes, and five planted mutants against it are all killed. The 17 suites that compile the servo pass, and so do the portability synthesis (60 of 60 tops), lint, behave and the docs gates.

## Linked Issue / roles

Closes #817
Relates to #814, #607, #76

Executor: `[A709]`
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

`hdl/ieee1722/crf/KL_mmcm_drp_servo.sv` synchronises the milan-domain reset into the servo's PS clock with a two-flop synchroniser, `psrst_sync_r`. The source is the milan reset flip-flop at 50 MHz; the destination runs at 200 MHz. Both clocks are outputs of the main PLL, so the crossing was timed as a single-cycle path with a 5 ns requirement. In #814's route it was the design's worst path, at +0.128 ns.

| Piece | Change |
|---|---|
| `sw/litex/clock_constraints.tcl` | New `kl_servo_reset_sync_constraints`. It finds the two synchroniser stages by structure and cuts only the first stage's D pin, only from the milan clock: `set_false_path -from <milan clock> -to <psrst_sync_r_reg[0]/D>`. It refuses a stage count other than two, a stage without `ASYNC_REG`, a broken chain, or a PS clock that is not one clock distinct from milan |
| `sw/litex/clock_constraints.py`, `sw/litex/milan_soc.py` | The hook runs in the #607 post-synthesis, pre-optimize phase, beside the Ethernet exceptions. It names the milan PLL output (`_CRG.milan_pll_clk`) through the namespace. It is installed wherever the servo's MMCM boundary is wired and the servo is not pruned |
| `KL_mmcm_drp_servo.sv:1292-1294` | `(* ASYNC_REG = "TRUE" *)` on `psrst_sync_r`, as on the module's other synchronisers. No behaviour change |
| `sw/builder/test_shipping_clock_constraints.py` | Every shipping elaboration (1x1 TDM8 and 8x8, either port) must emit exactly one `kl_servo_reset_sync_constraints <milan PLL output>`, after the hook Tcl is sourced once, between synthesis and optimization |
| `sw/builder/test_clock_constraints.py` | `test_servo_reset_sync` grades the Tcl on a stub netlist: the one exact cut, independent of stage order, and each refusal, none of which emits a constraint |
| Docs | `docs/litex/CLOCK_DOMAINS.md` (alias row, crossing map, constraint bullets), `docs/integration/BUILDING.md` section 5, `docs/testing/RUNNING_TESTS.md` |

**The crossing**, from the same read-only reports on dev's route (`1e80128f`, the same recipe and directive) and on this branch's route:

| `psrst_sync_r_reg[0]/D` | dev | this branch |
|---|---|---|
| Setup | +1.975 ns, requirement 5.000 ns, timed as synchronous, 1 level | False Path, not timed |
| Hold | +0.634 ns | False Path |
| Exception on the pin | none | `-from [get_clocks -of_objects [get_nets milansoc_crg_clkout1]]` `-to [get_pins {...psrst_sync_r_reg[0]/D}]`, setup false, hold false |
| The milan -> PS clock pair | 17 timed endpoints, 5.000 ns | the handshake's 16 still timed at 5.000 ns; this one cut |

- **No other constraint changes.** Dev's routed exception list has 25 entries and this branch's 26. They differ by exactly the new cut, and the ignored-exception reports are identical.
- **The generated files.** The XDC is identical to dev's. The build Tcl gains one line. The generated Verilog differs only in its date and in the order of two lines of its module-tree comment.
- **The CDC report** lists the pair the same way at dev and here: `Info milansoc_crg_clkout1 milansoc_crg_clkout4 Safely Timed None 17 17 0 0 0`, Safe 17 of 17. The whole-design CDC report has identical rows. The tool does not analyse the structure of an endpoint-scoped exception between related clocks. As a diagnostic only, never shipped, declaring the pair asynchronous in memory gives this crossing `CDC-3 1-bit synchronized with ASYNC_REG property` (Safe) here, against `CDC-2 ... missing ASYNC_REG property` at dev.

**Route-1x1, ExtraPostPlacementOpt**, recipe unchanged, default seed:

| Corner | WNS / WHS ns, this branch | dev |
|---|---|---|
| Slow 0C, Slow 85C | +0.166 / +0.055 | +0.303 / +0.051 |
| Fast 0C, Fast 85C | +1.481 / +0.020 | +1.633 / +0.028 |

| Figure | Record | dev route | this route | Gate |
|---|---:|---:|---:|---|
| LUT / FF / slices | 52,012 / 53,707 / 15,780 | 51,801 / 53,760 / 15,834 | 51,805 / 53,759 / 15,834 | ok |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 13 | 74 / 27 / 13 | 74 / 27 / 13 | ok |
| WNS / WHS ns | 0.440 / 0.036 | 0.303 / 0.028 | 0.166 / 0.020 | **WNS: fell by more than 0.25** |

The two worst setup families are LiteEth's TX CRC into the gPTP launch observer (Ethernet RX clock, 10 levels: +1.320 ns at dev, +0.166 here) and LiteDRAM's ZQCS timer into the bank-machine level enables (`sys`, 15 levels: +0.303 ns at dev, +0.196 here). Neither is logic this branch changes. One constraint changes the placement as a whole, and one seed is the recipe.

## Authoritative references

- #817 (the task and its acceptance); #814 (the measurement that found this path)
- #607: `docs/integration/BUILDING.md` section 5 (exception scope, the rejected-constraint log gate) and `docs/litex/CLOCK_DOMAINS.md` (Crossing map, Constraints and verification)
- REQ-CSR-03 (crossings), as cited by `docs/litex/CLOCK_DOMAINS.md`
- `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` (route-1x1 and the resource gate); `docs/testing/RUNNING_TESTS.md` (the constraint tests)

## How to get into the same state

```sh
git fetch origin
git checkout 817-servo-reset-cdc
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
python3 -m pip install -r sw/litex/litex_pins.txt
python3 scripts/ci_litex_env.py
sw/litex/patches/apply.sh
```

## How to validate

```sh
PYTHONHASHSEED=0 python3 sw/builder/test_clock_constraints.py
syn/yosys/run.sh
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
cd tests && behave --no-capture -f plain
```

Expected: the constraint check prints `servo reset synchronizer cut and refusal controls PASS` and four `[constraints] shipping ... kl_servo_reset_sync_constraints milansoc_crg_clkout1 PASS` lines, exit 0. Yosys: `tops: 60 pass: 60 fail: 0`. Every suite passes. Behave: 14 features, 495 scenarios, 0 failed.

The route follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` unchanged, at ExtraPostPlacementOpt, then:

```sh
python3 syn/ooc/pp_resource_gate.py check <route-dir> --endpoint route-1x1
```

At this head it exits 1 on WNS, as above. In the routed design, `report_exceptions -to` the first stage's D pin shows the false path from the milan clock. `report_timing -to` that pin reports `Timing Exception: False Path`.

## Known limitations / out of scope

- **The WNS rule.** The shipping route fails the resource gate on WNS alone. The families that set it are placement-sensitive, and this branch does not touch them. The record was not re-recorded.
- **"The CDC report lists the crossing as safe."** At the pair level it does, Safe 17 of 17, exactly as at dev. A structural CDC-3 row in the shipped report would need a clock-level exception between the milan and PS clocks, which would change the handshake's 16 endpoints. The issue forbids that. The structural classification is shown by the diagnostic above.
- **The cut reset route is unbounded:** 11.368 ns in this route, 2.671 ns at dev. The signal is a level, held for the whole reset. The batch handshake is toggle-based, and the servo issues no batch until a measurement window has produced a nonzero command, so nothing bounds this latency. A `set_max_delay -datapath_only` bound (5 ns, or one milan period) is the alternative. It is one line in the hook.
- **The servo's batch handshake** (16 milan -> PS endpoints) stays timed as synchronous. `cdc_handshake.sv` asks for an exception on it; that would be a new issue.
- Not run: the full sweep (not required for this change); rtl-fast's firmware jobs (no firmware input changed); the two comparison directives; hardware.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (the CDC-report criterion's reading is listed above for the reviewer)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes (the resource gate's WNS rule awaits a ruling)
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

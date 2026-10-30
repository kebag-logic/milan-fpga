# HANDOFF: #817 media-clock servo reset synchroniser crossing, executor [A709]

Status: **REVIEW READY** at head `6cfb27dacafb2e5b693412db3342ca0fccc9c0bc`, with one gate verdict for the manager to rule on: `pp_resource_gate.py check` on the shipping route returns exit 1 on its WNS rule (section 4). No STOP condition holds: the fix needs no RTL behaviour change. Worktree clean, every submodule at its gitlink, live remote dev still `1e80128f`. Nothing pushed.

- Lane: `817-servo-reset-cdc`, from dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141`
- Head: `6cfb27da`. Two commits: `a7ff491a` (the change) and `6cfb27da` (documentation and one test docstring). `git diff --stat a7ff491a 6cfb27da` lists only `docs/integration/BUILDING.md`, `docs/litex/CLOCK_DOMAINS.md`, `docs/testing/RUNNING_TESTS.md` and the docstring of `sw/builder/test_shipping_clock_constraints.py`. None of them is a build input, so the route at `a7ff491a` is the head's route
- origin: https://github.com/kebag-logic/milan-fpga.git (verified). No git command ran inside a lane submodule. The docs replica's driver sets the tsn-c-stack origin inside its own scratch clone, after checking that clone's toplevel (#814's driver, unchanged)
- Assignment: the issue body of #817 and the manager prompt. #817 had no comments at 11:50 UTC, so the prompt's "latest [A10] comment" did not exist. Route-1x1 at ExtraPostPlacementOpt, recipe unchanged, on dev plus this constraint only (not #814's cuts)
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/817#issuecomment-6522040114
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/817#issuecomment-6524540908 (the lane's only other post; text in `REVIEW-READY.md`)

## 1. Changes

| File:line (at the head) | Change | Reason |
|---|---|---|
| `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:1292-1294` | `(* ASYNC_REG = "TRUE" *)` on `psrst_sync_r`; the comment states the cut | Vivado's CDC analysis classes this synchroniser CDC-2 "1-bit synchronized with missing ASYNC_REG property" without the attribute (dev) and CDC-3 "with ASYNC_REG property", Safe, with it (head; section 3). The attribute also keeps both stages in one slice. Same form as `locked_sync_r` at `:567`. No behaviour change: Verilator ignores it, and Yosys maps the module as before (section 5) |
| `sw/litex/clock_constraints.tcl:21-59` | New `kl_servo_reset_sync_constraints {milan_net}` | Cuts only `psrst_sync_r_reg[0]/D`, and only from the milan clock: `set_false_path -from <milan clock> -to <that D pin>`. It finds the two stages by structure (the stage fed by the other is stage 1). It refuses a stage count other than two, a stage without ASYNC_REG, a broken chain, and a PS clock that is not one clock distinct from milan |
| `sw/litex/clock_constraints.py:31-48` | `_source_hooks()` sources the Tcl once; new `add_servo_reset_constraints(platform, crg)` | Runs the hook in the #607 post-synthesis, pre-optimize phase, where the repository's other clock-crossing exceptions are installed. It names the milan PLL output, resolved through the namespace. `add_quasi_static_constraints` emits the same Tcl as before |
| `sw/litex/milan_soc.py:279-281` | `_CRG.milan_pll_clk`, the milan PLL output | The hook resolves the clock on the PLL output, not on its buffered alias, as the Ethernet hook does (#607) |
| `sw/litex/milan_soc.py:3120-3123` | Installs the hook where the servo's MMCM boundary is wired, unless the servo is pruned (`media_clock_servo` False) | A pruned servo has no crossing. A build with the servo present must carry the hook, and the Tcl refuses if the synchroniser is not found |
| `sw/builder/test_shipping_clock_constraints.py:98-106` | Each real shipping elaboration (1x1 TDM8 and 8x8, ports e1 and e2) must emit exactly `kl_servo_reset_sync_constraints <milan PLL output name>`, with the Tcl sourced once, between synthesis and optimization | Presence check on the real builder path |
| `sw/builder/test_clock_constraints.py:164-248` | `test_servo_reset_sync`: a stub netlist grades the one exact cut, its independence from stage order, and each refusal, none emitting a constraint | Scope and refusal check of the Tcl itself |
| `docs/litex/CLOCK_DOMAINS.md:92,237,377-380` | Alias row, crossing-map row, constraint bullets | The changed constraint contract; the batch handshake stays timed |
| `docs/integration/BUILDING.md` section 5 | Four lines on the cut and its refusals | Build-gate contract |
| `docs/testing/RUNNING_TESTS.md:190-195` | The shipping hook and the stub controls | Test contract |

The generated build files against dev's export: the XDC is identical. The build Tcl gains one line, `kl_servo_reset_sync_constraints milansoc_crg_clkout1`, after `milan_eth_constraints`. The generated Verilog differs only in its generation date and the order of two lines in the module-tree comment (`receipts/constraints-text/`). In the route, the earlier hooks report what they report at dev (`quasi_static cells=112`, `MultiReg eth=12 part=198 other=0`), plus the new line `CONSTRAINTS: servo reset synchronizer from=milansoc_crg_clkout1 to=milansoc_crg_clkout4 cut=milan_datapath/g_mmcm_servo.mmcm_servo/psrst_sync_r_reg[0]/D` (`receipts/route-a7ff491a/constraints-lines.txt`). That line means the attribute survived synthesis on both stages.

Not changed: the servo's batch handshake `u_batch_hs` beside the synchroniser has 16 milan -> PS-clock endpoints, which stay timed as single-cycle paths with a 5.000 ns requirement. `cdc_handshake.sv`'s header asks for an exception on them. That is outside this issue (open question 3).

## 2. New checks and their planted mutants

The constraint-presence check is `sw/builder/test_clock_constraints.py`, run with the LiteX interpreter (it also runs `test_shipping_clock_constraints.py`). Unmutated, it passes at `a7ff491a` and at `6cfb27da` (rc 0, 65 s): `servo reset synchronizer cut and refusal controls PASS`, and four `[constraints] shipping <shape> <port>: milan_eth_constraints ...; kl_servo_reset_sync_constraints milansoc_crg_clkout1 PASS` lines.

`scripts/mutants.py` plants each mutant in a scratch clone at `6cfb27da`, runs the whole check, restores the file and requires a clean tree (`receipts/constraint-check/mutants/mutants.json`):

| Mutant | Planted change | Check rc | Failing words | Verdict |
|---|---|---:|---|---|
| M1 | `milan_soc.py`: the `add_servo_reset_constraints(platform, self.crg)` call removed | 1 | `AssertionError: shipping servo reset synchronizer hook missing, duplicated or renamed: []` | killed |
| M2 | `clock_constraints.tcl`: the `set_false_path -from $src -to $pin` line removed | 1 | `servo cut missing or widened: ` | killed |
| M3 | the cut widened to every source clock (`set_false_path -to $pin`) | 1 | `servo cut missing or widened: {set_false_path -to {sv/psrst_sync_r_reg[0]/D}}` | killed |
| M4 | the ASYNC_REG refusal disabled (`if {0} {`) | 1 | `accepted: *lacks ASYNC_REG*` | killed |
| M5 | the hook skipped while the servo is present (condition inverted) | 1 | `AssertionError: shipping servo reset synchronizer hook missing, duplicated or renamed: []` | killed |

A live run on a real netlist, read-only (`receipts/live-hook-dev-netlist/`): the hook, sourced on dev's routed checkpoint, which has no ASYNC_REG, refuses with `CONSTRAINTS: servo reset synchronizer milan_datapath/g_mmcm_servo.mmcm_servo/psrst_sync_r_reg[0] lacks ASYNC_REG`. That is the attribute's planted removal. With the attribute set in memory, it cuts exactly that D pin, and `report_exceptions` shows the cut, setup false and hold false.

## 3. The crossing before and after

Before: dev `1e80128f`'s own route-1x1 at ExtraPostPlacementOpt (#814 round 1, the same recipe, checkpoint SHA-256 in `receipts/route-dev-1e80128f/route-dcp.sha256`). After: the head's route. The same `scripts/post_route.tcl` runs read-only on both (`receipts/post-route-dev/`, `receipts/post-route-head/`).

| `psrst_sync_r_reg[0]/D`, from `FDPE_3/C` (milan reset, `milansoc_crg_clkout1`, 50 MHz) to `milansoc_crg_clkout4` (200 MHz) | dev `1e80128f` | head `a7ff491a` |
|---|---|---|
| Setup | **+1.975 ns, requirement 5.000 ns, timed as synchronous**, 1 level (a LUT1 inverter shared with the AECP reset net), data path 2.671 ns | **False Path, not timed**, data path 11.368 ns |
| Hold | +0.634 ns, timed | False Path |
| Exception on the pin | none | position 26: `-from [get_clocks -of_objects [get_nets milansoc_crg_clkout1]]` `-to [get_pins {...psrst_sync_r_reg[0]/D}]`, setup false, hold false, no override status |
| ASYNC_REG, placement | empty; SLICE_X0Y4 BFF / CFF | TRUE on both; SLICE_X3Y16 AFF / A5FF (one slice) |
| The 17 milan -> PS endpoints (`milan_ps_endpoints.tsv`) | 17 timed, requirement 5.000 ns: this one at +1.975, the handshake's 16 at +2.521 to +3.071 | 16 timed, requirement 5.000 ns, the handshake's 16 at +2.114 to +3.127; this one False Path |

In #814's route of dev plus its cuts, this endpoint was the design's worst path at +0.128 ns. At the head it is no longer timed, so it cannot set the WNS.

**Every other constraint is unchanged.** Dev's routed `report_exceptions` has 25 exceptions and the head's 26. As sets, positions ignored, they differ by exactly the new one (`receipts/route-a7ff491a/exceptions-diff-vs-dev.txt`). The ignored-exception reports are identical (`exceptions_ignored.rpt`).

**The CDC report.** The routed `report_cdc` line for this crossing's clock pair is the same at dev and at the head: `Info milansoc_crg_clkout1 milansoc_crg_clkout4 Safely Timed None 17 17 0 0 0` (endpoints 17, Safe 17, Unsafe 0, Unknown 0, No ASYNC_REG 0). The whole-design signoff CDC report has the same 269 detail rows and the same counts at both (`signoff-cdc-rows-vs-dev.txt`). Vivado lists that pair, this endpoint included, as Safely Timed because the two clocks are related. It does not structurally analyse an endpoint-scoped exception between related clocks. The probes on dev's checkpoint show this for a false path to the pin, a false path to the cell, and `set_max_delay -datapath_only 5` to the pin (`receipts/probe-dev-checkpoint/variants/`). As a diagnostic only, never shipped, declaring the two clocks asynchronous in memory makes `report_cdc` analyse the structure. The crossing's row is then `CDC-3 Info 1-bit synchronized with ASYNC_REG property`, Safe, at the head, and `CDC-2 Warning 1-bit synchronized with missing ASYNC_REG property` at dev (`receipts/cross-probe-*/diag_async_cdc_*`). The shared inverter before the first stage raises no CDC-10. Whether the pair-level line meets "the CDC report lists the crossing as safe" is open question 1.

## 4. Route-1x1 at the shipping directive

Recipe unchanged (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`): the ax7101 export, `pp_baseline.py --single-thread-synthesis`, `baseline_integrated.tcl`, `general.maxThreads` 32, ExtraPostPlacementOpt, Vivado 2026.1, default seed, in a clean clone at `a7ff491a`. It ran through `vivado-slot.sh` in its own user scope: rc 0, 4325 s (synthesis 54 minutes under host contention).

| Corner | head WNS / WHS ns | dev WNS / WHS ns | Floor (WNS >= +0.030, WHS >= 0) |
|---|---|---|---|
| Slow 0C | +0.166 / +0.055 | +0.303 / +0.051 | met |
| Slow 85C | +0.166 / +0.055 | +0.303 / +0.051 | met |
| Fast 0C | +1.481 / +0.020 | +1.633 / +0.028 | met |
| Fast 85C | +1.481 / +0.020 | +1.633 / +0.028 | met |
| Routed summary | +0.166 / +0.020 | +0.303 / +0.028 | met |

TNS 0, THS 0, no failing endpoint, route complete with 0 routing errors. The #607 log gate (`check_implementation_log`) on the route log: no 12-4739, 20-1307 or 12-5201.

**Top 10 setup paths** (every path group, one per endpoint, `receipts/post-route-head/top10_max.tsv`):

| # | Slack ns | Clock | Levels | Data path ns (logic) | From -> to |
|---:|---:|---|---:|---|---|
| 1 | +0.166 | eth_clocks0_rx | 10 | 7.662 (1.888) | `milansoc_liteethmaccore_tx_crc_crc_packet_reg[7]` -> `KL_gptp_gmii_launch/mine_r_reg/D` |
| 2-5 | +0.196 | sys | 15 | 9.490 (2.008) | `milansoc_sdram_zqcs_timer_count1_reg[10]` -> `milansoc_sdram_bankmachine1_level_reg[0..3]/CE` |
| 6-9 | +0.336 | sys | 15 | 9.390 (2.008) | `milansoc_sdram_zqcs_timer_count1_reg[10]` -> `milansoc_sdram_bankmachine3_level_reg[0..3]/CE` |
| 10 | +0.390 | sys | 13 | 9.263 (2.046) | `milansoc_write_w_buffer_level0_reg[2]` -> `storage_10_dat1_reg[14]/D` |

Top 10 hold: +0.020 to +0.046 ns, all milan-clock paths of 0 or 1 level into block-RAM data pins and LUTRAM (AECP response lanes, CPU memory write data, gPTP event queue; `top10_min.tsv`).

**What sets the WNS.** Neither family is logic this lane changes. Each family's worst slack in the two routes (`receipts/cross-probe-*/families.tsv`):

| Family | dev | head |
|---|---:|---:|
| LiteEth TX CRC -> `KL_gptp_gmii_launch` (Ethernet RX clock, 9-10 levels) | +1.320 | **+0.166** |
| LiteDRAM ZQCS timer -> bank-machine level enables (`sys`, 14-15 levels; #814's F3) | **+0.303** | +0.196 |

The one constraint changes placement as a whole: the synchroniser itself moved from SLICE_X0Y4 to SLICE_X3Y16. #814 measured 0.57 ns of route-to-route spread on one family with no logic change. One seed, as the recipe prescribes.

**Resources and `pp_resource_gate.py check --endpoint route-1x1`** (against the twelfth record; `receipts/route-a7ff491a/pp_resource_gate-route-1x1.log`):

| Figure | Record | dev route | head route | head - dev | Gate verdict (head) |
|---|---:|---:|---:|---:|---|
| LUT | 52,012 | 51,801 | 51,805 | +4 | ok, below the baseline |
| FF | 53,707 | 53,760 | 53,759 | -1 | ok |
| SLICE | 15,780 | 15,834 | 15,834 | 0 | ok |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 13 | 74 / 27 / 13 | 74 / 27 / 13 | 0 | ok |
| WNS ns | 0.440 | 0.303 | 0.166 | -0.137 | **REGRESSION: fell by more than 0.25** (-0.274) |
| WHS ns | 0.036 | 0.028 | 0.020 | -0.008 | ok |

**Verdict: exit 1, `RESULT: MATERIAL REGRESSION`, on WNS alone.** Dev's own route passes the same gate (rc 0, WNS -0.137 from the record). The manager rules on the WNS rule separately, as assigned. The record was not re-recorded and no budget document was edited.

## 5. Gate table

| Gate | Head | rc | Result |
|---|---|---:|---|
| route-1x1, ExtraPostPlacementOpt, recipe unchanged | `a7ff491a` | 0 | section 4; floor met at every corner |
| `python3 syn/ooc/pp_resource_gate.py check <gateware> --endpoint route-1x1` | `a7ff491a` | **1** | `MATERIAL REGRESSION`, WNS 0.44 -> 0.166; every other figure ok |
| The same check on dev's own route (reference) | `1e80128f` | 0 | `RESULT: PASS` |
| #607 implementation-log gate on the route log | `a7ff491a` | 0 | no rejected-constraint diagnostic |
| Constraint-presence check, `sw/builder/test_clock_constraints.py` (LiteX interpreter) | `a7ff491a`, `6cfb27da` | 0, 0 | section 2 |
| Five planted mutants against it | `6cfb27da` | 1 each | all killed (section 2) |
| Live hook on dev's routed netlist | dev checkpoint | refusal, then cut | section 2 |
| The 17 Verilator suites that compile `KL_mmcm_drp_servo.sv` (directly or through `milan_datapath`), each as `run_all_suites.sh` runs it plus `suite_tally.py --verdict` | `6cfb27da` | 0 each | 73,367 checks, 0 failures; the suite rows below |
| `syn/yosys/run.sh` (the yosys-portability gate) | `6cfb27da` | 0 | `tops: 60 pass: 60 fail: 0`, `RESULT: PASS`, 1602 s; `KL_mmcm_drp_servo` cells=6252; tied-input and tap-purity PASS |
| rtl-fast replica: `changes`, `verilator-lint`, `bdd-conformance`, `yosys-tool`, `yosys-elaboration` | `6cfb27da` | 0 | classifier: RTL/tooling relevant; `LINT GATE: PASS (89 violation(s) <= ratchet 89)`; pp_srcs derived; behave `14 features passed, 0 failed`, `495 scenarios passed`, `2288 steps passed`; integration tops elaborate; OOC read-set, ROM, guard and cache refusals pass |
| Docs gates replica (`.github/workflows/docs.yml`: wire-accountability, docs-gates-0, builder legs 0 and 1, gate_41) | `6cfb27da` | 0 | `44 steps, 0 failed` |
| Builder leg 1 again with the LiteX interpreter | `6cfb27da` | 0 | `ALL GATES PASS EXCEPT 1 NOT RUN`: gate 11 needs a board utilization report that is not on this host |
| The five markdown gates on CPython 3.12.3 | `6cfb27da` | 0 | `5 steps, 0 failed` |
| The no-git step's two gates, on a `git archive` export | `6cfb27da` | 0, 0 | `docs_check: 0 finding(s)`; `feature_status: 0 finding(s)` |

Suites (`receipts/suites/`; seconds are local wall clock under contention):

| Suite | rc | s | Suite | rc | s |
|---|---:|---:|---|---:|---:|
| capture_coherence | 0 | 753 | milan_dp | 0 | 4040 |
| follow_ring | 0 | 724 | milan_dp_mclk | 0 | 1230 |
| mmcm_servo | 0 | 1428 | media_phase | 0 | 805 |
| mbx | 0 | 45 | pp_shadow | 0 | 648 |
| crf_tx | 0 | 10 | crf_rx | 0 | 742 |
| mmcm_servo_autorepair | 0 | 13 | media_grid_align | 0 | 258 |
| milan_dp_render | 0 | 927 | aaf_clock_meter | 0 | 648 |
| csr | 0 | 174 | avtp_parser | 0 | 41 |
| media_nco | 0 | 17 | | | |

`scripts/suite_tally.py` over the 17 logs: `checks: 73367   in-suite failures: 0` (`receipts/suites/tally.txt`).

`mbx` first returned rc 2 from my environment, not from the change. The suites ran with `MAKEFLAGS=-j2`/`-j4`, without CI's `--no-print-directory`. `mbx`'s `mutants-quick` reads `make print-vflags` from stdout, got `make[1]: Entering directory ...` and tried to execute it (`FileNotFoundError`). Rerun with CI's `MAKEFLAGS=-j1 --no-print-directory`: rc 0, `mbx mutants: 6 of 6 caught`. Both logs are kept. A first attempt at three parallel workers was stopped by me at 22.5 GB of unit memory, before any verdict. The suites then ran with a guard (`scripts/memguard.sh`, 20 GB). The unit peaked at 13.0 GB afterwards, briefly above the 12 GB guidance, under its 24 GB cap.

Not run, and why: the full sweep (not required for this change); rtl-fast's firmware and publication-census jobs (no firmware or publication input changed; the hosted rtl-fast runs them); the act runner (needs a pushed head); the ExtraTimingOpt and AltSpreadLogic_high comparison routes (not assigned); hardware (out of scope). The docs gate `gate_42` was skipped by rule: it executes the candidate's `act_ci.py` on the host.

## Open questions

1. **"The CDC report lists the crossing as safe."** Its pair's line reads Safely Timed, Safe 17 of 17, at both dev and the head, because the clocks are related and the exception is endpoint-scoped. Structurally, under a diagnostic-only asynchronous declaration, the crossing is CDC-3, Safe, at the head (CDC-2 at dev). A shipped structural CDC-3 row would need a clock-level exception between `milan` and `idelay`. That would change the 16 handshake endpoints' constraints, which the issue's second criterion forbids. The reviewer decides which reading the criterion means.
2. **The cut leaves the reset's route unbounded.** It is 11.368 ns at this route (2.671 ns at dev). The signal is a level, held for the whole reset. The batch handshake is toggle-based and tolerates either release order. The servo can send no batch until a measurement window has produced a nonzero command: `acc_r`, `u_cmd_r` and `u_gain_r` reset to zero (`KL_mmcm_drp_servo.sv:921-935`, `:1150-1168`). So no requirement bounds this latency. The issue's other option, `set_max_delay -datapath_only` to the 5 ns destination period, would keep the path timed and back in the WNS. A bound of one milan period (20 ns) is a middle option. Either is a one-line change to the hook.
3. **The batch handshake's 16 milan -> PS endpoints** stay timed as synchronous paths (+2.114 ns worst at the head). `cdc_handshake.sv`'s header asks for an exception on them. If wanted, that is a new issue, not this lane.
4. **The WNS rule.** The shipping route fails `pp_resource_gate.py check` on WNS alone (+0.166 ns, 0.274 under the record against a 0.25 limit). The families that set it are LiteEth TX into the gPTP launch observer and LiteDRAM's ZQCS timer into the bank machines. Both are placement-sensitive and untouched here. The manager rules on this.

## How the runs were made

- Vivado: `scripts/export.sh` (clean clone, export, `pp_baseline.py`, no Vivado), then `scripts/launch.sh`. That runs `setsid nohup vivado-slot.sh` with no timeout, the command in its own user scope (MemoryMax 14G). Every probe opened a routed checkpoint read-only and wrote nothing back. No lock was taken directly.
- Suites, Yosys, rtl-fast and docs each ran in their own clean clone at `6cfb27da`, with their submodules taken from the lane's own checkouts. Pinned tools: Verilator 5.050, sv2v v0.0.12, GNU Make 4.3, Yosys 0.66, CPython 3.12.3 for the CI replicas.
- Receipts redact host paths (`<scratch>`, `<dev-route-scratch>`, `<tools>`, `<home>`). Files over 200 KB are recorded by SHA-256 and size in each directory's `large.sha256`.

## Progress log (UTC)

- 11:51 lane checks: origin, base `1e80128f`, clean tree, submodules at their gitlinks. 11:52 TAKEN.
- 11:53-12:00 read-only probes of dev's routed checkpoint: the crossing as timed, its cells, and its CDC classification under five candidate constraints.
- 12:05 live hook check on dev's netlist. 12:07 commit `a7ff491a`. 12:08 export; route-1x1 started 12:08:49.
- 12:09 constraint-presence check at `a7ff491a`, rc 0. 12:10 docs commit `6cfb27da`. 12:11 planted mutants, all killed. 12:15 check at `6cfb27da`, rc 0.
- 12:13 suites in three clones; 12:16 two workers stopped for memory; 12:17 and 12:21 restarted under the guard.
- 12:31 Yosys gate; 12:32 rtl-fast replica (lint, behave); 12:33 docs gates; 13:05 rtl-fast Yosys jobs.
- 13:20 route rc 0. 13:21-13:27 resource gate, post-route reports on both checkpoints, cross-probes, receipts.
- 13:24 milan_dp rc 0; 13:29 docs legs done; 13:55 the last suite rc 0 (17 of 17). Index, then REVIEW READY.

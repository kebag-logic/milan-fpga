# [A700d] milan-fpga #787 round 3 handoff: route-1x1 at `667b9bbc`, three directives, the #818 gate

Status: **REVIEW READY** at `667b9bbc` (issuecomment-6528972693, `review-ready.md`), unchanged: route only, and the route shows no defect, so there is no commit.
No STOP condition is met. The #818 gate (PR #820's file) gives `RESULT: PASS`, rc 0, with ExtraPostPlacementOpt
selected at +0.165 ns. Every corner of every directive meets both floors, and every figure is inside its tolerance
and ceiling. Nothing was pushed, and no PR was created or edited.

## Assignment

- Issue #787, round 3: [A10] issuecomment-6525242660. Route only: no commit unless the route shows a defect, and then
  STOP first. The area record is not re-recorded here (the record rule).
- Executor [A700d]. TAKEN: issuecomment-6527485786 (`taken.md`). REVIEW READY: issuecomment-6528972693 (`review-ready.md`). These are the lane's
  only posts this round.
- Head **`667b9bbc02b99a08d71efab750f95e8702cbbe57`** (branch `787-reboot-reset`, PR #822), unchanged this round. Base
  dev `1e80128f`, still the live remote dev tip (`git ls-remote`, at the start and at the end). Processor pin `a9e84b66`
  (`git -C protocol-processor rev-parse --show-toplevel` is that directory; its origin is the processor repository).
  `git remote get-url origin` is `https://github.com/kebag-logic/milan-fpga.git`. The lane worktree is clean.

## Changes

None. The route shows no defect, so the assignment's "no commit" holds. No file in the tree was edited, and no file
was regenerated.

## What ran

Vivado 2026.1. Recipe unchanged (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, "Integrated measurements"). Everything
ran in a clean clone at `667b9bbc` (`scripts/make_clone.sh`: the lane's tree, its submodules from the lane's checkouts).

1. **Export and prepare** (`scripts/prep_route.sh`). The shipping AX7101 1x1 export, built from `build.sh ax7101
   --dry-run`'s own argv with `--build` removed, then `pp_baseline.py --single-thread-synthesis`. Then the recipe
   snippet's two comparison scripts, written from the shipping `alinx_ax7101.tcl`: the shipping thread setting,
   `open_checkpoint` of the shipping route's `alinx_ax7101_synth.dcp`, and the shipping tail with only the placement
   directive changed.
2. **One synthesis**: the shipping `baseline_integrated.tcl` (synthesis 16:13 -> 16:57 UTC, 43 min, single-threaded;
   synthesis checkpoint SHA-256 `65f232e3...`).
3. **The three directives in parallel.** Once the shipping run had written the synthesis checkpoint and moved on to
   `opt_design`, both comparisons started (16:57 UTC). Each ran through `vivado-slot.sh` in its own user scope, in
   slots 1, 0 and 2. All used the default seed. Each Vivado run ended rc 0. The shipping run took 3,727 s in total,
   AltSpreadLogic_high 1,151 s and ExtraTimingOpt 1,077 s.
4. **Judged** with PR #820's gate. `syn/ooc/pp_resource_gate.py` at `32f0d9b5` (SHA-256 `83d6d381...`, byte-equal to
   `git show 32f0d9b5:syn/ooc/pp_resource_gate.py`) went into a scratch copy of the head's `syn/ooc` and
   `docs/design`, with #820's three self-test modules beside it. Nothing from #820 entered the tree.

**One harness error, corrected before any measurement.** The first shipping launch (16:12 UTC) stopped at RTL
elaboration with rc 1: `could not open $readmem data file .../sw/builder/out/.../gptp_ucode.hex`. The cause was my
prep script: its exit trap removed the checkout's three artifact links (`sw/builder/out` and the two
`configs/generated` ROM links) before Vivado ran. The bank this was adapted from runs Vivado inside the same script.
The run's project files were removed and its logs set aside (`receipts/prep/failed-run-1*`). The links were restored
for the life of the runs, and the shipping run relaunched at 16:13 UTC into the same export, with no other change.
It is not a design result.

## Results: the route set at `667b9bbc`

Gate (`receipts/results/head-667b9bbc-set-check.log`, rc 0):

```text
route set: the recipe's 3 placement directives, worst-corner WNS_ns and WHS_ns
  ExtraPostPlacementOpt      0.165   0.036
  AltSpreadLogic_high        0.151   0.032
  ExtraTimingOpt              0.12   0.036
directive ExtraPostPlacementOpt selected: the best worst-corner WNS, 0.165 ns
LUT 52012 -> 51568 (-444) ok; FF 53707 -> 53680 (-27) ok; SLICE 15780 -> 15749 (-31) ok
RAMB36 74, RAMB18 27, DSP 13: unchanged
WNS_ns 0.44 -> 0.165 (-0.275)  WARNING: fell by more than 0.25 from the record
WHS_ns 0.036 -> 0.036 ok
WARNING: WNS_ns fell from the record by more than the timing fall; reported, never gated (#818)
route status: complete, no unrouted net and no routing error
RESULT: PASS
```

The WARNING is the #818 ruling's reported-never-gated fall against the twelfth record (+0.440 ns). The floor is the
gate. Dev's own selected route is itself 0.137 ns below that record (below).

### Per directive (`receipts/results/head-figures.md`, from each run's signoff and utilization reports)

| Directive | Corner | WNS ns | TNS ns | WHS ns | THS ns |
|---|---|---:|---:|---:|---:|
| ExtraPostPlacementOpt (selected) | Slow_0C | +0.165 | 0.000 | +0.102 | 0.000 |
| | Slow_85C | +0.165 | 0.000 | +0.102 | 0.000 |
| | Fast_0C | +1.565 | 0.000 | +0.036 | 0.000 |
| | Fast_85C | +1.565 | 0.000 | +0.036 | 0.000 |
| AltSpreadLogic_high | Slow_0C | +0.151 | 0.000 | +0.061 | 0.000 |
| | Slow_85C | +0.151 | 0.000 | +0.061 | 0.000 |
| | Fast_0C | +1.331 | 0.000 | +0.032 | 0.000 |
| | Fast_85C | +1.331 | 0.000 | +0.032 | 0.000 |
| ExtraTimingOpt | Slow_0C | +0.120 | 0.000 | +0.101 | 0.000 |
| | Slow_85C | +0.120 | 0.000 | +0.101 | 0.000 |
| | Fast_0C | +1.331 | 0.000 | +0.036 | 0.000 |
| | Fast_85C | +1.331 | 0.000 | +0.036 | 0.000 |

| Directive | LUT | FF | Slices (free of 15,850) | Block RAM tiles (ceiling 121.5) | RAMB36 / RAMB18 / DSP |
|---|---:|---:|---:|---:|---|
| ExtraPostPlacementOpt | 51,568 | 53,680 | 15,749 (101) | 87.5 | 74 / 27 / 13 |
| AltSpreadLogic_high | 51,520 | 53,682 | 15,837 (13) | 87.5 | 74 / 27 / 13 |
| ExtraTimingOpt | 51,524 | 53,680 | 15,837 (13) | 87.5 | 74 / 27 / 13 |

Against the record (LUT 52,012 +500, FF 53,707 +600, SLICE 15,780 +80, RAM and DSP +0), the comparisons are also
inside every tolerance: LUT -492 / -488, FF -25 / -27, SLICE +57 / +57.

Worst setup path per directive (at both slow corners; all in `milansoc_crg_clkout0`, the 100 MHz `sys` clock, a
10 ns requirement):

| Directive | Slack | Source -> destination | Levels | Data path (logic / route) |
|---|---:|---|---:|---|
| ExtraPostPlacementOpt | +0.165 | `milansoc_write_w_buffer_readable_reg` -> `storage_15_reg_1/ENARDEN` (the 16 x 300-bit `write_w_buffer` store) | 10 | 9.173 ns (16.7 % / 83.3 %) |
| AltSpreadLogic_high | +0.151 | `milansoc_write_w_buffer_level0_reg[0]` -> `storage_10_dat1_reg[20]/D` | 12 | 9.536 ns (18.4 % / 81.6 %) |
| ExtraTimingOpt | +0.120 | `FSM_sequential_subfragments_fsm2_state_reg[0]` -> `milansoc_tmod1_reg[11]/CE` (a response-memory bridge counter) | 16 | 9.592 ns (23.3 % / 76.7 %) |

None of the three is in `KL_reboot_ctrl`, the frame-end toggle or the MAC transmit side. All are `sys`-domain SoC
memory-path logic that this PR does not change.

### This PR's own timing in the route (shipping directive)

- The frame-end toggle crossing (`milansoc_milanmac_ethtxend_tgl_reg` on `eth_clocks0_rx` -> `reboot_ctrl/txend_sync_r_reg[0]`
  on `milansoc_crg_clkout1`): the pair reads `Max Delay Datapath Only`, 8.00 ns, WNS +5.87 ns, 51 endpoints (dev: 50,
  +6.63). Hold is false-pathed on that pair by `milan_eth_constraints`, so the hold row reads slack inf with path group
  none, as designed. The reverse pair `clkout1 -> eth_clocks0_rx` is +6.73 ns, 14 endpoints (dev +6.48, 14)
  (`receipts/head-667b9bbc/EPPO/clock_interaction.rpt`).
- `reboot_ctrl/hold_r_reg` -> its MultiReg into `sys`: asynchronous groups, `ASYNC_REG`. The CDC report's CDC-3 count is
  17 against dev's 16, and every other CDC class count equals dev's. The ten CDC-10 rows reach the same ten
  destinations as on dev (`cdc_summary.txt`).
- The constraint census: `MultiReg eth=12 part=199` (dev 198, the hold's MultiReg). check_timing is identical to dev's.
  The shipping log has no CRITICAL WARNING and no ERROR, the same as dev's.
- ICAPE2 1 and STARTUPE2 1 in all three routes.
- In context (placed hierarchy, shipping directive): `reboot_ctrl` is 46 LUTs and 34 FFs. `pp_shadow` moves from
  24,180 / 19,397 to 23,946 / 19,438 (the processor pin), and the datapath's own cells lose 153 FFs. That last figure
  is the flattened netlist's attribution, not traced this round. The datapath diff since dev removes no register: it
  adds the instance, its parameters and its ports.

## Delta against dev's own routes (#814 round 1, dev `1e80128f`, the same recipe and tool)

Dev's set, judged by the same #820 gate file: rc 0, `RESULT: PASS`, ExtraPostPlacementOpt selected at +0.303 ns
(`receipts/offline/dev-1e80128f-set-check.log`). The figures come from the same collector
(`receipts/offline/dev-figures.md`) and equal #814's published ones.

| Directive | WNS dev -> head (ns) | WHS dev -> head (ns) | LUT dev -> head | FF dev -> head | Slices dev -> head (free) |
|---|---|---|---|---|---|
| ExtraPostPlacementOpt | +0.303 -> **+0.165** (-0.138) | +0.028 -> +0.036 (+0.008) | 51,801 -> 51,568 (-233) | 53,760 -> 53,680 (-80) | 15,834 (16) -> 15,749 (101) |
| AltSpreadLogic_high | +0.230 -> +0.151 (-0.079) | +0.014 -> +0.032 (+0.018) | 51,846 -> 51,520 (-326) | 53,759 -> 53,682 (-77) | 15,795 (55) -> 15,837 (13) |
| ExtraTimingOpt | +0.106 -> +0.120 (+0.014) | +0.054 -> +0.036 (-0.018) | 51,833 -> 51,524 (-309) | 53,758 -> 53,680 (-78) | 15,794 (56) -> 15,837 (13) |

The selected route moves from +0.303 to +0.165 ns (-0.138 ns). Dev's three worst paths are also `sys`-domain SoC
memory logic: LiteDRAM's bank machines and the read-beat path, at 14 levels. One directive rose and two fell, and
the spread across directives is 0.197 ns at dev and 0.045 ns at the head. With one seed per directive this is within
the placement spread #814 measured (about 0.3 ns). It does not separate this PR's own effect.

## Gates

| Gate | Head | rc | Result | Receipt |
|---|---|---:|---|---|
| Vivado route-1x1, ExtraPostPlacementOpt (synthesis, then place and route) | `667b9bbc` | 0 | route complete, 0 routing errors | `head-667b9bbc/EPPO/` |
| Vivado, AltSpreadLogic_high from that synthesis checkpoint | `667b9bbc` | 0 | route complete, 0 routing errors | `head-667b9bbc/ASLH/` |
| Vivado, ExtraTimingOpt from that synthesis checkpoint | `667b9bbc` | 0 | route complete, 0 routing errors | `head-667b9bbc/ETO/` |
| `pp_resource_gate.py check <shipping> --endpoint route-1x1 --comparison <ASLH> --comparison <ETO>` (#820 file) | `667b9bbc` | 0 | `RESULT: PASS`; EPPO selected, +0.165 ns; floors met at all four corners; WNS fall WARNING (not gated) | `results/head-667b9bbc-set-check.log` |
| The same with the comparisons reversed (control) | `667b9bbc` | 0 | the same selection and verdict body | `results/head-667b9bbc-set-check-reversed.log` |
| The same gate on dev's #814 round 1 set | `1e80128f` | 0 | `RESULT: PASS`; EPPO selected, +0.303 ns | `offline/dev-1e80128f-set-check.log` |
| `pp_resource_gate.py check-baseline` (#820 file, head JSON and budget) | `667b9bbc` | 0 | `baseline PASS: 3 endpoints` | `offline/gate820-check-baseline.log` |
| `pp_resource_gate.py --selftest` (#820 file, scratch copy) | `32f0d9b5` file | 0 | every arm PASS | `offline/gate820-selftest.log` |
| `scripts/xvlog_gate.py --check` (through the slot wrapper) | `667b9bbc` | 0 | `PASS (0 finding(s) == ratchet)`; 85 hdl/ files and 52 pinned-processor files; `KL_reboot_ctrl.sv`, `KL_pp_shadow.sv` and `milan_datapath.sv` (every changed RTL file) are in the census, each analysed as its own module | `xvlog/` |
| IOB packing check, in-flow before routing (`kl_iob_pack_check`) | `667b9bbc` x 3 | - | `IOB-PACK OK: 22 port(s) constrained IOB TRUE checked, none unpacked` on each directive; 21 PASS rows plus `eth0_rx_er` INERT (as at dev) | `head-667b9bbc/*/iob_pack.rpt`, `log-excerpt.txt` |
| `python3 sw/litex/iob_pack_selftest.py` | `667b9bbc` | 0 | 22 arms, 21 mutants, 0 failures | `offline/iob_pack_selftest.log` |
| #607 log check (`clock_constraints.check_implementation_log`) on each route log (`scripts/log_gate.py`) | `667b9bbc` x 3 | 0 | no 12-4739, 20-1307 or 12-5201 diagnostic in any of the three logs | `results/head-607.log` |
| #607 control: the shipping log copied with one planted `CRITICAL WARNING: [Vivado 12-4739]` line | scratch copy | 1 (wanted) | `REFUSED: constraint application failed (#607)` naming the planted line | `results/plant-607.log` |

Not run, by the assignment (route only): the full sweep, rtl-fast, the docs gates, the builder bank, Yosys and the
campaigns. Round 2 ran them at this head or at `e12147d4` (see round 2's handoff), and no file changed since.

## STOP conditions

| Condition | Met? |
|---|---|
| The best directive misses +0.030 ns setup or 0 ns hold at any corner | no: ExtraPostPlacementOpt +0.165 / +0.036 ns at its worst corners; all three directives meet both floors at all four corners |
| Placement or routing fails | no: each run rc 0, route status complete, 0 routing errors, 0 unrouted nets |
| A LUT, FF, slice or BRAM ceiling is exceeded | no: every figure of every directive is inside its tolerance; Block RAM tiles 87.5 against 121.5 |

## Receipts

`INDEX.md` lists every file in this directory (generated by `scripts/gen_index.py` from the files present).
`receipts/large.sha256` records the routed and synthesis checkpoints and the full Vivado logs by SHA-256 and size.
Host paths in the receipts are redacted to `<work>`, `<dev-work>`, `<scratch>` and similar.

| Directory | Contents |
|---|---|
| `receipts/head-667b9bbc/{EPPO,ASLH,ETO}/` | route status, post-route utilization, placed hierarchical utilization, IOB packing, clock interaction, check_timing, CDC summary, every timing report's design table, the log excerpt (CONSTRAINTS, IOB-PACK, step times), the run's rc |
| `receipts/dev-1e80128f/{EPPO,ASLH,ETO}/` | the same reports from #814 round 1's dev routes, for the delta |
| `receipts/results/` | the gate set check (and reversed), the per-directive figures, the #607 logs and the planted control |
| `receipts/offline/` | dev's set check and figures, #820's check-baseline and self-test, the IOB self-test, dev's #607 log |
| `receipts/xvlog/` | the xvlog gate log and rc, and the census check for the changed files |
| `receipts/prep/`, `receipts/slotlogs/` | the export and preparation log, the first launch's failure, and the slot wrapper's start and end stamps |

`scripts/`: `make_clone.sh`, `prep_route.sh`, `launch.sh`, `viv.sh`, `xvlog_run.sh`, `route_figures.py`,
`log_gate.py`, `collect.py` and `gen_index.py`.

## For the manager

- Nothing to push: the branch head is unchanged at `667b9bbc`. `PR-BODY.md` is the round 2 body with its timing
  content replaced by this round's measured set.
- No hardware or bench access and no flashing. No sub-agents.

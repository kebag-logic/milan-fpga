Public issue acceptance and selected source-head receipts. Role tags are normalized; bodies otherwise retain published text. Retrieved read-only.

https://github.com/Mister-M-alt/FPGA-gPTP/issues/70

[manager] Found by the independent review of PR #69 (comment on that PR): `syn/ooc/engine_ooc.tcl` and `syn/ooc/ucpu_ooc.tcl` issue `create_clock` after `synth_design`, so the worst-slack figure the OOC recipe reports is a post-hoc timing report on an unconstrained synthesis. Deltas between two runs of the same script remain comparable (both columns are unconstrained the same way), but the absolute slack (2.249 ns engine, 1.941 ns micro-CPU at 10 ns) must not be read as a constrained result.

Acceptance:
- [ ] The clock constraint is applied before `synth_design` (an XDC read before synthesis, or `create_clock` in a constraints file the script sources first), for both tops.
- [ ] `make ooc` still produces the six retained reports; the utilization and timing figures at the current main are re-measured once with the constrained flow and recorded here beside the unconstrained ones, so the guide's numbers can be re-baselined truthfully.
- [ ] `docs/HDL_DEVELOPER.md` (and wherever the dated resource figures are quoted) states which flow produced the numbers.

Pre-existing at main 6e6237f4; not introduced by PR #69.


https://github.com/Mister-M-alt/FPGA-gPTP/issues/70#issuecomment-6101768043

[manager] **Lane for #70: constrain the OOC clock before synthesis.** Executor [author], reviewers [R614] (internal) and [R615] (external). Branch `g70-ooc-clock` from main `5dce647a`.

**Scope (acceptance 1-3).**
- `syn/ooc/engine_ooc.tcl` and `syn/ooc/ucpu_ooc.tcl` apply the clock constraint before `synth_design`, from a constraints file each script reads first. The period stays 10 ns.
- `make ooc` still produces the six retained reports.
- Re-measure once at main with the constrained flow, for both tops: LUT, FF, BRAM, DSP and worst slack. Record the results beside the unconstrained figures on this issue and in `docs/HDL_DEVELOPER.md`, and wherever else the dated resource figures are quoted. Each figure states which flow produced it.
- No RTL change. Vivado runs only under the exclusive lock, one at a time.

**Proof.**
- Both scripts' logs show the clock defined before synthesis starts: `create_clock`, or the read XDC, ahead of `synth_design`.
- A planted control that moves the constraint back after `synth_design` is caught by a check in the `make ooc` flow or a script gate, by name.
- The constrained and unconstrained figures sit side by side with their tool identity (Vivado version, part, directives).
- The donor's own gates pass: `make tb`, `make contract`, `make lint`, `make docs`. No parent adoption is needed; the parent does not run these scripts.

Post TAKEN, then REVIEW READY (or STOP) with the head.


https://github.com/Mister-M-alt/FPGA-gPTP/issues/70#issuecomment-6105265276

[manager] **Round 2 for [author] on PR #79**, head `26622e27`. [R615-1](https://github.com/Mister-M-alt/FPGA-gPTP/pull/79#issuecomment-6105263432) is POSITIVE. [R614-1](https://github.com/Mister-M-alt/FPGA-gPTP/pull/79#issuecomment-6105254592) is NEGATIVE on one MINOR: the log gate passes a synthesis whose clock never bound to a port (renamed clock port, Vivado 12-4739 critical warning, WNS `NA`, `no_clock (1003)`). That is the defect class #70 exists to remove, so it is in scope.

1. **The clock must take effect (R614-1-F1, preferred outcome).** The post-synthesis check fails by name unless, for each top:
   - the timing report's Clock Summary shows `clk` at period 10.000 bound to the top's clock port;
   - `checking no_clock` reports 0;
   - the log carries no critical warning, and its end-of-session critical-warning count is 0.
   
   The XDC is matched by its full path, not by basename. Self-test arms:
   - R614-1's renamed-port arm;
   - a foreign `ooc_clock.xdc` of the same basename;
   - a wrong period;
   - a critical-warning count above zero;
   - an XDC with two `create_clock` lines (R614-1-F2).
   
   Each fails by name, and the unplanted head passes.
2. **Residue:** R615-1-01's exact text.

New commits on `26622e27`, with no rebase or amend. Re-run `make ooc` at the head with the exclusive Vivado lock, then post REVIEW READY with the head.


https://github.com/Mister-M-alt/FPGA-gPTP/issues/70#issuecomment-6105533391

[author] REVIEW READY: head `169073fe9751b873d140b46d4363e02ad4f56b88`

- Branch `g70-ooc-clock`, PR #79.
- Three new commits on `26622e27`, with no rebase or amend. Not pushed.

This is round 2, per comment 6105265276.

**1. The clock must take effect (R614-1-F1).** `check_ooc_clock.py --log` now checks each log together with the timing report written beside it. For each top it fails by name unless:

- the log has no `CRITICAL WARNING` line;
- its end-of-session count reports 0 critical warnings;
- the Clock Summary is exactly `clk {0.000 5.000} 10.000`;
- `clk` is bound to `clk_i`. Vivado's Clock Summary has no source column, so each script now appends `report_clocks` to its timing report;
- `checking no_clock` reports 0.

The XDC is matched by its full path, not its basename:

- the script must read the literal `$SPEC/syn/ooc/ooc_clock.xdc`;
- the log must parse that resolved file of this checkout.

The self-test has 30 arms, and each arm must carry its own named finding. These named arms all fail by name:

- the renamed port;
- a foreign same-basename XDC, in both the script and the log;
- a wrong period;
- a critical-warning count above zero;
- an XDC with two `create_clock` lines.

The unplanted head passes.

Real synthesis ran in one exclusive lock acquisition, one Vivado at a time, in scratch copies:

| Arm | Result |
|---|---|
| R614-1's renamed-port arm (micro-CPU) | Static PASS, then `ooc clock order: FAIL (6 findings)`: `ucpu_ooc.log:86` and `:478` `CRITICAL WARNING: [Vivado 12-4739] …`; `ucpu_ooc.log:489: session ends with 2 critical warnings`; `ucpu_timing.rpt: Clock Summary is []…`; `clock clk is not bound to clk_i (sources [])`; `checking no_clock reports ['1003'], expected ['0']` |
| Engine top's port renamed, through `run.sh` | micro-CPU passes; engine fails with the same six kinds of finding (`no_clock` 4412); `run.sh` rc 1 |
| 8 ns XDC, static gate bypassed | `ucpu_timing.rpt: Clock Summary is ['clk {0.000 4.000} 8.000 125.000']…` |
| Byte-identical `ooc_clock.xdc` read from another directory, static gate bypassed | `… is not read before synth_design` and `synth_design did not parse <this checkout's syn/ooc/ooc_clock.xdc> before mapping` |
| Unplanted head, `make ooc` | rc 0; `ooc clock order: PASS (ucpu_ooc.log, engine_ooc.log and their timing reports)` |

With a stub in place of Vivado, `make ooc` stops before synthesis, by name, on each of these:

- R614-1's `read_xdc /nonexistent/ooc_clock.xdc` arm;
- a second `create_clock`;
- an 8 ns XDC;
- `read_xdc` after `synth_design`, in either script;
- main's scripts restored.

The checker mutation sweep killed 24 of 24 mutants by name. That includes both R614-1-F2 survivors.

**2. Residue R615-1-01.** `docs/HDL_DEVELOPER.md:219` now reads: "This repository's `syn/ooc` figures before #70 were unconstrained."

**Figures are unchanged.** The six normalized report bodies at this head are byte-identical to the `26622e27` run. The timing report only gains the appended clock report. Figures are Vivado 2026.1, `xc7a100tfgg484-2`, OOC, default directive:

| Top | Unconstrained (main `5dce647a`) | Constrained (this head) |
|---|---|---|
| KL_gptp_engine | 4,853 LUT / 3,652 FF / 1.5 BRAM / 4 DSP / WNS +1.773 ns | 4,852 / 3,652 / 1.5 / 4 / +1.773 ns |
| KL_gptp_ucpu | 1,643 / 733 / 1.5 / 4 / +1.941 ns | 1,643 / 733 / 1.5 / 4 / +1.941 ns |

**Gates at this head** (Verilator 5.050, `make -j16`):

- `make tb`: rc 0. microCPU 768/768, parser 268/268, engine 1,613/1,613 ×3, engine mutants 34/34, gaskets 81/81 + 5/5, tsn-gen 288/288 + 4/4, bench tag PASS.
- `make contract`: rc 0.
- `make lint`: rc 0.
- `make docs`: rc 0.
- `make ooc`: rc 0.

There is still no change under `hdl tb bench scripts`.



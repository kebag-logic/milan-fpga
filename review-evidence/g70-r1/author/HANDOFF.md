# [A598] Handoff: #70, constrain the OOC clock before synthesis

Status: REVIEW READY at head `26622e27dfb629a6c59d22b77021012127e0c344`
(branch `g70-ooc-clock`, four commits on main `5dce647a`). Not pushed; no PR
opened. All five donor gates return 0 at that head; see the gate table.

- Repository: Mister-M-alt/FPGA-gPTP, branch `g70-ooc-clock`, base main `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`.
- Assignment: issue #70 comment 6101768043. The finding is the PR #69 cleared-context review (comment 5678061643, "Recorded observations"), relayed in the merge comment 5678167494.
- TAKEN: issue #70 comment 6101778629 (2026-10-10T20:19:15Z).
- REVIEW READY: issue #70 comment 6104614009 (2026-10-11T02:27:58Z). It names the head and carries the side-by-side figure table, so the results are recorded on the issue.

## Commits

| Commit | Subject |
|---|---|
| `48051c5` | Read the OOC clock from an XDC before synth_design and gate that order |
| `adc344c` | Give each OOC clock rule a selftest arm that only it catches |
| `acb23f0` | State the unconstrained OOC flow on each archived page that quotes OOC figures |
| `26622e2` | Record constrained and unconstrained OOC figures side by side with their flow |

One-line subjects, no body, no trailers, configured identity. `git diff --stat 5dce647a HEAD -- hdl tb bench scripts` is empty: there is no RTL, testbench, bench or repository-script change.

## Changes (file:line at 26622e2)

- `syn/ooc/ooc_clock.xdc:9` (new file): `create_clock -period 10.000 -name clk [get_ports clk_i]`. This is the only clock definition, and the period stays 10 ns. The header (:4-8) says why it is read first.
- `syn/ooc/engine_ooc.tcl:14`: `read_xdc $SPEC/syn/ooc/ooc_clock.xdc` is the first file the script reads, ahead of `read_verilog` (:15) and `synth_design` (:22). The old `create_clock` after `synth_design` is gone. The header (:4-12) states that every figure before #70 came from unconstrained synthesis.
- `syn/ooc/ucpu_ooc.tcl:14`: the same change, with `synth_design` at :16. The header (:4-12) records that the 1,070-LUT protocol-processor anchor delta was measured in the old order.
- `syn/ooc/check_ooc_clock.py` (new; the check is named `ooc clock order`):
  - Static rules on the scripts, `script_findings` (:65): exactly one `synth_design`; `read_xdc` of `ooc_clock.xdc` before it; no `create_clock`, `create_generated_clock`, `read_xdc` or `source` after it.
  - XDC rule, `xdc_findings` (:86): exactly one `create_clock`, 10.000 ns on `clk_i`.
  - Log rules on what Vivado actually ran, `log_findings` (:121): synthesis started and completed; a `# read_xdc …ooc_clock.xdc` echo precedes `Command: synth_design`; `Parsing XDC File […/ooc_clock.xdc]` appears inside synthesis before `Start Technology Mapping`; no constraint command is echoed after `synth_design completed successfully`.
  - `--selftest` (:174) has 17 arms: one clean fixture and 16 planted defects. Each rule has at least one arm that only it catches.
- `syn/ooc/run.sh:28`: the static check runs before Vivado's settings are sourced, so a broken order never reaches Vivado. `:36` runs the log check on both logs after both syntheses. Header at :5-6.
- `Makefile:39`: the `ooc` target runs `python3 syn/ooc/check_ooc_clock.py --selftest` before `syn/ooc/run.sh`.
- `docs/HDL_DEVELOPER.md:174`: new section "Out-of-context measurement" covering the flow, the gate, and the side-by-side table with a Flow column plus tool identity. `:228` adds a checklist item, "Keep the OOC clock ahead of synthesis."
- `docs/MANAGER.md:29-56`: "Latest measured snapshot" rewritten with a Flow column, both flows at main, what the order changed, and the PR #76 delta figures labelled as the unconstrained flow.
- Flow notes at `:11` under the archive banner, on every archived page that quotes OOC figures. The notes add text only; no figure changed.
  - `docs/history/v1/RESOURCE_VALIDATION.md` and `docs/history/v1/PROJECT_STATUS.md` (this line): the order is verified from git. Both Tcl scripts are unchanged from root commit `c99f7a8` through `5dce647a`, with `create_clock` after `synth_design`.
  - `docs/history/v1/prototype/RESOURCE_VALIDATION.md`, `IP_BLOCKS.md`, `INTEGRATION_GUIDE.md` and `BENCH_TAP_WIRETRUTH.md` (prototype line): the order is verified at `c99f7a8` only. The prototype line's later scripts are not retained, and the note says so.
- `make docs` passes (current pages keep the ten-word rule; history banners keep their metadata).

## Clock defined before synthesis (log excerpts, both tops)

These are from the final-head `make ooc` at `26622e2`, with the repository path shown as `<repo>`. Line numbers are log lines.

`ucpu_ooc.log`:

```text
3:# Vivado v2026.1 (64-bit)
28:# read_xdc $SPEC/syn/ooc/ooc_clock.xdc
30:# synth_design -mode out_of_context -top KL_gptp_ucpu -part xc7a100tfgg484-2 \
32:Command: synth_design -mode out_of_context -top KL_gptp_ucpu -part xc7a100tfgg484-2 -generic UCODE_HEX_P=gptp_ucode.hex
33:Starting synth_design
82:Processing XDC Constraints
84:Parsing XDC File [<repo>/syn/ooc/ooc_clock.xdc]
86:Completed Processing XDC Constraints
372:Start Technology Mapping
487:synth_design completed successfully
```

`engine_ooc.log`:

```text
3:# Vivado v2026.1 (64-bit)
28:# read_xdc $SPEC/syn/ooc/ooc_clock.xdc
36:# synth_design -mode out_of_context -top KL_gptp_engine -part xc7a100tfgg484-2 \
38:Command: synth_design -mode out_of_context -top KL_gptp_engine -part xc7a100tfgg484-2 -generic UCODE_HEX_P=gptp_ucode.hex
39:Starting synth_design
114:Processing XDC Constraints
116:Parsing XDC File [<repo>/syn/ooc/ooc_clock.xdc]
118:Completed Processing XDC Constraints
443:Start Technology Mapping
566:synth_design completed successfully
```

The same run's gate lines are `ooc clock order: PASS (ooc_clock.xdc, ucpu_ooc.tcl, engine_ooc.tcl)` before Vivado and `ooc clock order: PASS (ucpu_ooc.log, engine_ooc.log)` after.

For contrast, main's unconstrained logs (baseline run below) have no `read_xdc` and no XDC parse, and they show the clock only after synthesis:

```text
ucpu_ooc.log    31:Command: synth_design ...   458:synth_design completed successfully   462:# create_clock -period 10.000 -name clk [get_ports clk_i]
engine_ooc.log  37:Command: synth_design ...   541:synth_design completed successfully   545:# create_clock -period 10.000 -name clk [get_ports clk_i]
```

## Constrained and unconstrained figures

Tool identity, the same for both flows:

- Tool: Vivado v2026.1 (64-bit), lin64, SW Build 6511674 (Tue Jun 16 2026).
- Part: `xc7a100tfgg484-2`.
- Command: `synth_design -mode out_of_context -top <top> -part xc7a100tfgg484-2 -generic UCODE_HEX_P=gptp_ucode.hex`, with no `-directive`, so the Default directive. No other options.
- Clock: `clk` at 10.000 ns, waveform {0.000 5.000}, on `clk_i`.
- ROM: the shipping image, sha256 `c496ed8af59edd42…`. Every run regenerated it byte-identical to the tracked `syn/ooc/work/gptp_ucode.hex`.
- Reports: `report_utilization` (flat and hierarchical) and `report_timing_summary -delay_type max -max_paths 3`.

The two flows:

- Unconstrained: main `5dce647a` exactly, run as `make ooc` from a scratch export, with `create_clock` after `synth_design`.
- Constrained: `make ooc` at head `26622e2`, with `ooc_clock.xdc` read before `synth_design`. It reproduces the 48051c5 run; the normalized bodies of all six reports are identical.

| Top | Metric | Unconstrained (main 5dce647a) | Constrained (head 26622e2) | Delta |
|---|---|---:|---:|---:|
| KL_gptp_engine | Slice LUTs | 4,853 | 4,852 | -1 |
| KL_gptp_engine | LUT as memory | 466 | 466 | 0 |
| KL_gptp_engine | Slice registers | 3,652 | 3,652 | 0 |
| KL_gptp_engine | Block RAM tiles | 1.5 | 1.5 | 0 |
| KL_gptp_engine | DSPs | 4 | 4 | 0 |
| KL_gptp_engine | WNS at 10 ns | +1.773 ns, 0 failing of 12,254 endpoints | +1.773 ns, 0 failing of 12,254 endpoints | 0 |
| KL_gptp_ucpu | Slice LUTs / LUT as memory / registers / BRAM / DSP | 1,643 / 132 / 733 / 1.5 / 4 | 1,643 / 132 / 733 / 1.5 / 4 | 0 |
| KL_gptp_ucpu | WNS at 10 ns | +1.941 ns, 0 failing of 3,165 endpoints | +1.941 ns, 0 failing of 3,165 endpoints | 0 |

Notes:

- The single LUT difference is inside the engine's `u_ucpu` instance (logic LUTs 2,469 to 2,468, from `engine_util_hier.rpt`). The standalone microCPU top is unchanged, and the timing report bodies are identical in both flows: same critical path, same slack.
- The unconstrained run exactly reproduces the dated figures that `docs/MANAGER.md` carried at main (PR #76, 2026-09-24: engine 4,853 / 3,652 / 1.5 / 4 / +1.773 ns; microCPU 1,643 / 733 / 1.5 / 4 / +1.941 ns). That confirms those figures were the unconstrained flow.
- The 2.249 ns engine slack cited in #70 is the PR #69-era figure. PR #76 later moved the unconstrained engine WNS to +1.773 ns.
- Both flows report 0 critical warnings and 0 errors with the same 65-warning set. The constrained runs log three extra infos for the XDC parse.
- Out-of-context synthesis is not board timing. No placement or routing was run.

## Planted controls

**Static gate in the `make ooc` flow** (lane tree, scripts restored after each arm). `VIVADO_SETTINGS` pointed at a stub settings file whose `vivado` only prints `STUB VIVADO REACHED` and exits 3, so no real synthesis could start outside the lock.

| Arm | make rc | Failing words |
|---|---:|---|
| unplanted (positive control) | 2 (stub reached by design) | `ooc clock order selftest: PASS (17 arms)`, `ooc clock order: PASS (ooc_clock.xdc, ucpu_ooc.tcl, engine_ooc.tcl)`, then `STUB VIVADO REACHED: -mode batch -source …/ucpu_ooc.tcl …` |
| engine: `read_xdc` moved after `synth_design` | 2 | `ooc clock order: FAIL (2 findings)` / `engine_ooc.tcl: ooc_clock.xdc is not read before synth_design` / `engine_ooc.tcl:23: read_xdc after synth_design` (stub not reached) |
| ucpu: `read_xdc` moved after `synth_design` | 2 | `ooc clock order: FAIL (2 findings)` / `ucpu_ooc.tcl: ooc_clock.xdc is not read before synth_design` / `ucpu_ooc.tcl:17: read_xdc after synth_design` (stub not reached) |
| both scripts restored to main's order (`create_clock` after `synth_design`) | 2 | `ooc clock order: FAIL (4 findings)` / `ucpu_ooc.tcl: ooc_clock.xdc is not read before synth_design` / `ucpu_ooc.tcl:13: create_clock after synth_design` / `engine_ooc.tcl: ooc_clock.xdc is not read before synth_design` / `engine_ooc.tcl:20: create_clock after synth_design` |

**Log check against real Vivado runs.** These ran under the exclusive lock, one Vivado at a time.

- Planted: both scripts at 48051c5 with `read_xdc` moved after `synth_design`, synthesized by Vivado exactly as `run.sh` does but without its static gate. The log check alone had to catch it, and it returned rc 1:

  ```text
  ooc clock order: FAIL (6 findings)
    ucpu_ooc.log: ooc_clock.xdc is not read before synth_design
    ucpu_ooc.log: synth_design did not parse ooc_clock.xdc before mapping
    ucpu_ooc.log:462: read_xdc after synth_design
    engine_ooc.log: ooc_clock.xdc is not read before synth_design
    engine_ooc.log: synth_design did not parse ooc_clock.xdc before mapping
    engine_ooc.log:545: read_xdc after synth_design
  ```

  Its figures are the unconstrained ones (engine 4,853 LUTs), and its normalized report bodies equal the main baseline's.
- Main's own unconstrained logs (baseline run) also return rc 1, with `ucpu_ooc.log:462: create_clock after synth_design` and `engine_ooc.log:545: create_clock after synth_design` plus the two missing-read and missing-parse findings per log.

**Checker mutation sweep.** Each rule was disabled in a scratch copy, and the 17-arm selftest had to fail. All 10 of 10 mutants were killed, and the unmutated control passed:

- Killed by name: R1 (`no read_xdc escaped`), R2 (`create_clock added after synth_design escaped`), R3 (`second synth_design escaped`), R5 (`8 ns period escaped`), L1 (`synth_design that never started escaped`), L3 (`no read_xdc echo escaped`), L4 (`synthesis without the parsed XDC escaped`) and L5 (`create_clock echoed after a constrained synthesis escaped`).
- Killed by a crash on the guarded input, which also returns rc 1: R4 (IndexError) and L2 (TypeError).

## Donor gate table (head 26622e2)

PATH puts the pinned Verilator 5.050 first; `make -j16`. Each command ran once, unpiped, with output redirected to its own log.

| Command | rc | Wall (UTC) | Result | Log sha256 (prefix), size |
|---|---:|---|---|---|
| `make tb` (fresh: suite build products removed first) | 0 | 02:02:25Z to 02:27:18Z | microCPU 768/768; parser 268/268; engine 1,613/1,613 in the shipping, request-seeded and Sync-seeded images; engine mutation arm 34/34 (33 mutants plus control); gaskets 81/81 plus 5/5 controls; tsn-gen 288/288 plus 4/4 controls; bench tag test PASS; no skips. The gasket build prints the pre-existing `PINCONNECTEMPTY` warning (`tb/verilator/gaskets/gasket_tb_top.sv:127`, not in this diff) under the suite's `-Wno-fatal` policy | `ca032c6241aca3b3`, 39,611 B |
| `make contract` | 0 | 01:36:33Z | `PHC interface contract: PASS` | `cdc70d96a542ea1a`, 62 B |
| `make lint` | 0 | 01:36:33Z | engine and bench lint clean under Verilator 5.050 | `5d3d90aed273a72c`, 1,532 B |
| `make docs` | 0 | 01:36:33Z to 01:36:34Z | diagram check PASS (9 pinned assets, 3 source-bound PNGs) and selftest PASS (10 arms); docs check PASS (11 current pages, 17 historical pages) and selftest PASS (10 arms); source evidence 20 exact, 0 findings, selftest PASS (7 arms) | `e8a0cee284e793a4`, 2,527 B |
| `make ooc` | 0 | 01:37:33Z to 01:40:19Z | `ooc clock order selftest: PASS (17 arms)`; static `ooc clock order: PASS`; both syntheses 0 critical warnings, 0 errors; log `ooc clock order: PASS (ucpu_ooc.log, engine_ooc.log)`; six reports retained | `00d372f6d4171951`, 86,266 B |

The six reports retained in `syn/ooc/work/` by the final-head run (sha256 prefix, size):

- `ucpu_util.rpt`: `fe089997f1103ca1`, 9,038 B
- `ucpu_util_hier.rpt`: `bf9fd781042a8511`, 1,459 B
- `ucpu_timing.rpt`: `6b057a53075f6f37`, 29,277 B
- `engine_util.rpt`: `a0ddd1ca3499bfef`, 9,168 B
- `engine_util_hier.rpt`: `deff76dca211b3fc`, 2,173 B
- `engine_timing.rpt`: `1f8b45351a7adde4`, 33,043 B

The raw hashes differ between runs only through report header dates and paths; the normalized bodies are compared above. `git status --porcelain` is empty before and after the run, because every work product is ignored and the tracked ROM image regenerates byte-identical.

Vivado lock: one exclusive acquisition, 2026-10-11T01:30:56Z to 01:40:19Z. Inside it, eight Vivado sessions ran strictly one after another: the main baseline, the 48051c5 constrained run, the planted control and the final head, two tops each. There was no idle hold, because the final-head signal arrived before the hand-off wait began.

Earlier `make tb` runs:

- A preview at `adc344c` (same tb, RTL and microcode) returned rc 0, 2026-10-10T20:30:53Z to 20:55:38Z.
- An incremental run at `26622e2`, which reused those suite builds (`Nothing to be done`), also returned rc 0, 01:36:33Z to 02:01:24Z. The row above is the fresh rebuild that followed it.

The four quick gates ran concurrently with the final-head `make ooc` and the incremental tb. Afterwards the tb build products (`obj_dir`, `seedrun`, `syncseedrun`, `__pycache__`, all ignored) were removed again. The six `syn/ooc/work` reports of the final-head `make ooc` stay in place, and `git status --porcelain` is empty.

## Residuals and judgement calls for review

- `hdl/ucpu/KL_gptp_ucpu.sv:11` (an RTL comment) quotes the other repository's AECP anchor, "measured 1,070 LUT / 491 FF / 3 RAMB36". RTL is out of scope, so it is unchanged. The flow behind that anchor is now described in the `syn/ooc/ucpu_ooc.tcl` header.
- I annotated archived pages with a flow note rather than editing any archived figure. The bench pages' placed figures (`BENCH_FIRSTLIGHT.md`) come from `bench/arty/build.tcl`, which already reads `arty.xdc` (:20) before `synth_design` (:22) and names its build, so they are not annotated.
- On the prototype pages, the clock order is proven only for the founding commit `c99f7a8`, and the notes say so.
- "Record the results ... on this issue": the only posts allowed on #70 are TAKEN, REVIEW READY and STOP, so the side-by-side table goes in the REVIEW READY comment.
- `Closes #70` is used because every acceptance item and proof item is met (see PR-BODY.md).

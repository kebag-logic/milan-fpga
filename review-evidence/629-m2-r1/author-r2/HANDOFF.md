# [A494] HANDOFF: PR #634 round 2 (issue #629, lane M2)

- Base head: `57f4b742b504f5e69293aaa3e00d0470aa9b6071` (branch `629-media-clock-impl`); commits added, none amended; nothing pushed.
- Head: `d81198c2001756fd84c353d93c312c133c5af66b` (eight commits on `57f4b742`).
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5946975634
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5946993512
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-5951606845
- Status: REVIEW READY. Every item done, every gate rc 0 at the head: 59/59 suites as the five CI shards (2,148,404 checks, 0 failures), the shipping image meets timing. Nothing pushed; the PR body is prepared here.

## Setup

- `git remote get-url origin` = `https://github.com/kebag-logic/milan-fpga.git`; HEAD at start `57f4b742`.
- Submodules at their recorded gitlinks (each `rev-parse --show-toplevel` is its own directory): `third_party/verilog-axis` `48ff7a7e`, `gptp-processor` `5dce647a`, `protocol-processor` `b2db3a97`. No git command was run inside a submodule; no submodule file changed.
- Pinned simulator 5.050 for every suite; Markdown gates with the pinned md venv. The capture harness ran on the Verilator 5.052 its receipt records.
- GNU make 4.3 was built from the GNU tarball (sha256 `e05fdde47c5f7ca45cb697e973894ff4f5d79e13b750ed57d7b66d8defc78e19`, signed by the make maintainer's key `B2508A90102F8AE3B12A0090DEACCAAEDB78137A`) in a scratch directory; every suite shard and both root-suite proofs ran under it, as the hosted runner's make.

## Items

| # | Item | Commit(s) | Result |
|---|---|---|---|
| 1 | Saved-state capture re-measure | `d048e48b7`, `a2f173428`, `d81198c20` | 8x8 maximum 13.86484 ms (limit 24.5 ms, no STOP); gate rc 0 |
| 2 | Root suite under hosted make | `62822ca69` | failure reproduced under GNU make 4.3, then 27/27 rc 0 under it |
| 3 | Ratchets | `13721318e` | naming 95 recorded, port docs 217 <= 217, `git diff --check` clean |
| 4 | Tests that can fail | `21dbf51c0` | root mutants 15 and 16 caught; meter 6 new mutants caught; reviewer probes 15/15 CAUGHT |
| 5 | Docs | `f40822b31` | three fixes |
| 6 | RESIDUE and suggestions | `2253eca31` | residues taken; S1 retained |

### 1. The saved-state capture re-measure (R432-1 F1 = R433-1 F2)

- `tb/verilator/nvm_capture_cpu/run.py:58-66` grades each row against the census the spec carries, not the literal `(12634, 156)`/`(3218, 53)` it held; `soc.py:96-103,184` derives that census (`nvm_shape.closed_record_census`, `scripts/nvm_shape.py:251`) from the same generated shape the firmware constants come from and writes it into `sources.json`. `scripts/check_nvm_capture.py:40,78-84,95-104` uses the same helper, grades rows with it, and drives its timing fixture from the live census.
- The first run (all six arms in parallel, at `62822ca69`) exposed a harness defect: `sim_main.cpp` printed its TX-frame trace onto the stdout the firmware's console shares, and in the 8x8 OFF arm a trace landed inside CAPTURE row 1 (`records=` / trace / `164 mismatches=0 ...`), so `run.py` raised `KeyError: 'mismatches'`. The simulation is deterministic, so a rerun reproduces it. `tb/verilator/nvm_capture_cpu/sim_main.cpp:62-91,190,193` (`a2f173428`) holds each trace until the console stands at a line start. All six arms were re-run at `a2f173428` with the README's recipe (`unshare -Urn "$PRODUCT_PYTHON" -B tb/verilator/nvm_capture_cpu/run.py --shape ... --cpu-hz ... --captures 16 --traffic on|off --build-dir <scratch>`, PYTHONHASHSEED=0, offline, LITEX_ENV_CC_TRIPLE=riscv32-linux). Every capture of the five arms the first run graded reproduces its cycle count exactly, across the meter's port split and the trace fix; the re-run OFF arm reproduces all 16 of the first run's printed cycle counts, the split row included.
- Census: 8x8 164 records / 13,210 bytes (was 156 / 12,634); 1x1 54 / 3,290 (was 53 / 3,218). Product firmware unchanged (`a73ecc25...`), processor pins unchanged, CPU netlist unchanged (`c208df0b...`).

| Shape | CPU / system MHz | Traffic | Elapsed ms, min to max | 49 ms / arm max |
|---|---|---|---|---|
| 1x1 | 50 / 100, contract | ON | 3.96022 to 3.96728 | 12.3510x |
| 1x1 | 50 / 100, contract | OFF | 3.90676 to 3.91182 | 12.5261x |
| 8x8 | 50 / 100, contract | ON | 13.84836 to 13.86484 | 3.5341x |
| 8x8 | 50 / 100, contract | OFF | 13.67682 to 13.69390 | 3.5782x |
| 8x8 | 100 / 100, non-contract | ON | 10.41821 to 10.42973 | 4.6981x |
| 8x8 | 100 / 100, non-contract | OFF | 10.41356 to 10.41566 | 4.7045x |

- 8x8 contract maximum 13.86484 ms, margin 10.63516 ms to the 24.5 ms limit (was 13.23352 ms). STOP condition not reached.
- Receipt `tb/verilator/nvm_capture_cpu/measurements.json` (36,969 B, sha256 `ed871bdd09bde7ebde1ae021cd647e3cad354d3f8682c5b7308cda91e4cbd72a`): base `a2f1734283f367d0d522c8c7cda09b79aff60d06`, tree `c28595df81fb96ae7cb554216c76a23917105169`, `measured_for` and `harness_sha256` recomputed through the gate's own functions, every arm's summary verbatim from `run.py`, the per-arm identities hashed from the build products (`assemble_receipt.py` in this directory; it ends with the gate's `check_receipt`).
- Docs: `docs/design/SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 (timing paragraph, maxima, table, census), section 17 (stage size) and section 20 item 6; `tb/verilator/nvm_capture_cpu/README.md` (census, trace line rule). Every figure written by `refresh_section18.py` (this directory) from the receipt.
- Consequence beyond the findings: `docs/design/SAVED_STATE_FASTCONNECT.md` section 4.2's derivation table (names 39 / 107, raw area 3,290 / 13,210, KLJ2 image 3,336 / 13,256, ids 54 / 164, highest 0xA6 / 0xEA), its deadline block (52 pages, 3,268.48384 ms), the measured-size sentence (20 percent of a slot), the DDR budget (57,352 bytes) and the commit table (14 / 52 pages, 3.07 / 3.27 s). Each equals `scripts/check_nvm_record_space.py`'s output at the head; section 18 cites that section.

### 2. The root suite under hosted make (R432-1 F2)

- `tb/verilator/milan_dp_mclk/Makefile:44-49,57,65`: `--no-print-directory` on both nested derivations, with the reason (the #617 R394-3 F1 fix of `capture_coherence`).
- Before (`d048e48b7` tree, GNU make 4.3 first on PATH, pinned 5.050): `make -C tb/verilator/milan_dp_mclk` rc 2, `%Error: Cannot find file containing module: 'Entering'`, `'directory'`, `'Leaving'`, `[FAIL] the schemata did not compile` (`receipts/mclk_make43_before.log`).
- Probe of the derived lists under `MAKEFLAGS=w MAKELEVEL=1` and make 4.3: 8 print-directory tokens before, 0 after.
- After (`62822ca69`, same make 4.3): legs A 50/0, C 32/0, B 44/0; 10 controls; 14/14 mutants caught; 27/27, rc 0 (`receipts/mclk_make43_after.log`). With item 4's rows (same make 4.3): A 55/0, C 32/0, B 50/0; 12 controls; 16/16 mutants; 31/31, rc 0 in 438 s (`receipts/mclk_suite2.log`). R432-1 F2's verification line, `MAKEFLAGS=w MAKELEVEL=1 make -C tb/verilator/milan_dp_mclk`, rc 0 at `d81198c20` (31/31), and the suite passes inside shard 2/5 under make 4.3, the path that failed on the hosted runner.

### 3. The ratchets (R432-1 F3 and the builder bank)

- `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:113-118` `//!` contracts for `clk_i` (one clock, no crossing) and `rst_n` (synchronous, every register cleared); `:134` `subtype_i`.
- `:107` `CLK_FREQ_HZ_P` documented in Hz (the name's family); `:141-143` `fsh_i` documented by its octets (the gate's documented "noun for the value" exclusion; the port is the header's bytes, not a byte count).
- `:155-162,379-381` the largest deviation split out of `status_o` as `max_dev_ns_o[15:0]` (unit in the name, CODE_QUALITY Rule 4); `status_o` keeps the unit-free levels `[15:0]`. `hdl/milan/milan_datapath.sv:5675-5705` composes `aafm_stat_w = {max_dev_ns_w, status_w}`, so `AAFM_STAT` is unchanged; the two suite wrappers bind the halves.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md`: the trailing blank line removed.
- `measure_naming.py --check` PASS (95 recorded, no budget edit); `check_port_contracts.py` OK (hdl 217 <= 217); `git diff --check` and `git diff --check cdf49d1a HEAD` clean. OOC area unchanged (below).

### 4. Tests that can fail

- R433-1 F1 = R432-1 F4: `tb/verilator/milan_dp_mclk/sim_mclk.cpp:372` sends the talker's `tu` (o+3 bit 0); `:1045-1062` row [TU] in leg A: set, then cleared, each edge one history restart (`AAFM_STAT[15:8]`), rate invalid, lock kept, no request (IEEE 1722-2016 4.4.4.7). `mclk_mutants.py:132-133,170-171` mutant 15 binds the meter's `tu_i` to `avtprx_tv_bit`; caught by "tu: the followed talker's tu edge restarts the meter's history" in the `--tu` short leg. The meter harness comment (`aaf_clock_meter/sim_main.cpp` M7 header) now says the wiring mutant runs at the root; the design's Implementation notes record the placement.
- R432-1 F5, each probe killed in the meter suite (`tb/verilator/aaf_clock_meter/sim_main.cpp`):
  - (a) `:330-334,450-462,751-769` the restart lands inside the step PDU's slot (M3 positions 1 to 15; M12 groups that lose PDU 15, positions 1 to 14);
  - (b) `:555-579,588-601` M7 lock falls per event: a listener change and entry clear the held lock once, silently; root mutant 16 (`mclk_mutants.py:134-135,172-173`) fails "switch (iv): the meter's lock clears at the switch" (`sim_mclk.cpp:1018-1038`, a switch onto a talker silent for 150 ms: no request at the timeout);
  - (c) `:531-542` M6 gap before lock: not locked at the gap PDU and 7 clean PDUs after it, locked at the 8th;
  - (d) `:579,597-601` M7 the bind edge keeps a held lock;
  - (e) `:485` M4 zero channels does not lock;
  - and `:365-370` M1 the largest deviation (`max_dev_ns_o`) equals the offset over 15 spacings.
- The five probes and the largest-deviation probe are named mutants in `tb/verilator/aaf_clock_meter/mutants.py:148-198`, with R432-1's own edits.
- `reviewer_meter_probes.py` from the R432-1 packet, unmodified, pinned 5.050: before the new largest-deviation check 14/15 CAUGHT (`receipts/reviewer_probes1.txt`); at the head 15/15 CAUGHT (`receipts/reviewer_probes2.txt`).

### 5. Docs

- `docs/reference/FR_NFR.md:156` (R433-1 F3 = R432-1 F7): "AAF following implemented and graded in simulation (#629, PR #634); bench acceptance open".
- `docs/reference/REGISTER_MAP.md:1837-1839` (R433-1 F4): `0x8E0`/`0x8E4` carry `AAFM_STAT`/`AAFM_RATE`, linked to their section; `0x8E8` to `0x8F4` unmapped.
- `tb/verilator/milan_dp/README.md:74` (R432-1 F6): the `obj_aclk` row names `milan_dp_mclk` mutant 3.

### 6. RESIDUE and suggestions

- R432-1 R1 = R433-1 R2: design VERSION row "Kept by the [ruling on #629 (comment 5946491571)]".
- R432-1 R2 = R433-1 R1: design area row names `syn/yosys/ooc.sh KL_aaf_clock_meter` with its figures and links the STOP item 8 (both reviewers' texts).
- R433-1 R3: `docs/design/TIME_SYNC.md:203` "HOLDOVER for at least one cycle, until the new reference reads locked, then ACQUIRE".
- R432-1 R3: PR body (status line, limitations).
- R432-1 R4: `docs/testing/TESTING.md:517` "runs the three legs (A, B, C) beside sixteen named mutants" (in `21dbf51c0`, where the count changed).
- R432-1 S2 TAKEN: FR-CLK-04's `mr` shall qualified as the compliance matrix does (`FR_NFR.md:239`).
- R433-1 S2 TAKEN for `tb/verilator/milan_dp/sim_aclk.cpp:701-705`: INTERNAL rate two-sided, |ppm| < 5 (measured +0.80 ppm; `make -C tb/verilator/milan_dp aclk` rc 0, `receipts/aclk1.log`). RETAINED for render T30: its INTERNAL window is the aligner's pull-in after T14's hold (`sim_tdm8_render.cpp:2900-2903`), and the settled two-sided bound is T31's |walk| < 5 ppm.
- R432-1 S1 = R433-1 S1 RETAINED: keying the #386 settle band on `mga_sel_w` changes the merged design's settle table (INTERNAL is always inside the band, `follow_sel_r`) and TIME_SYNC's "at INTERNAL: 2048 ticks after the change"; it is a behavioural design change with its own render, `milan_dp` and image re-validation, and no defect is observed (render T30/T31 count no skip or underrun at INTERNAL). Proposed follow-up for the manager.

## Test rows and their failing mutants (new or changed this round)

| Row | Graded in | Named mutant (runner, id) | Shown failing |
|---|---|---|---|
| Root [TU]: the followed talker's `tu` edges restart the meter's history | `milan_dp_mclk` leg A, `--tu` | `tu` taken from the `tv` net (`mclk_mutants.py` 15) | caught, `receipts/mclk_suite2.log` |
| Root switch (iv): onto a talker silent past the meter's timeout | `milan_dp_mclk` leg B, `--silent` | a listener change keeping a held lock (`mclk_mutants.py` 16) | caught |
| Root campaign under GNU make 4.3 | `milan_dp_mclk` default target | the 14 round-1 mutants | 14/14 at `62822ca69`; 16/16 with item 4 |
| M12: the restart at the step's PDU, before the gap | `aaf_clock_meter` `step_in_gap` | `deviation_verdict_deferred_to_pdu15` | caught, `receipts/meter_suite1.log` |
| M3: the restart at the step's PDU | `aaf_clock_meter` `beyond` | (same probe; graded, not a named target) | probe CAUGHT |
| M7: a listener change clears the held lock | `aaf_clock_meter` `restarts` | `listener_change_keeps_lock` | caught |
| M6: a gap before lock restarts the settle run | `aaf_clock_meter` `lock` | `gap_does_not_break_settle` | caught |
| M7: the bind edge keeps a held lock | `aaf_clock_meter` `restarts` | `bind_edge_clears_lock` | caught |
| M4: zero channels refused | `aaf_clock_meter` `format` | `cpf_zero_accepted` | caught |
| M1: the largest deviation | `aaf_clock_meter` `rates` | `max_dev_not_tracked` | caught |
| INTERNAL rate two-sided | `milan_dp` `obj_aclk` | (milan_dp_mclk mutant 3 is the A2-a negative) | leg rc 0 |
| Capture harness census | `check_nvm_capture.py` | `--mutation bytes`, `records`, `clock`, `ignore-off-timing` | each rc 1 |

Meter suite at the head (inside shard 2/5 at `d81198c20`): cases 446/0, servo 6/0, campaign 33/33 (clean plus 32 mutants); the standalone run took 743 s. Root suite at the head (shard 2/5): A 55/0, C 32/0, B 50/0, campaign 31/31 (12 controls, 16 mutants).

## Area against the design estimate

`syn/yosys/ooc.sh KL_aaf_clock_meter KL_mmcm_drp_servo` (Yosys 0.66, `synth_xilinx -family xc7 -flatten`), after the port split (`receipts/ooc1.log`):

| Block | LUT (LUTRAM) | FF | RAMB18 | DSP | CARRY4 | Design estimate | Verdict |
|---|---:|---:|---:|---:|---:|---|---|
| `KL_aaf_clock_meter` | 574 (16) | 636 | 0 | 0 | 102 | 380 to 580 LUT, 270 to 420 FF, 0 RAMB18 | unchanged by round 2; LUT inside, FF over (accepted by the ruling) |
| `KL_mmcm_drp_servo` | 865 | 792 | 0 | 1 | 150 | 871 LUT, 792 FF at the design base | unchanged |

## Timing of the shipping image

RTL changed this round (the meter's port split and contracts, `13721318e`), so the image was rebuilt through the repository's build path at `d81198c20` (no later commit; nothing under `hdl/`, `sw/litex/`, `syn/` or `configs/` changed after `13721318e`): `TAG=a494m2d81198c2 sw/litex/build.sh ax7101`, one heavy build, Vivado v2026.1, `synth_design -directive AreaOptimized_high`, `opt_design -directive ExploreArea`, `place_design -directive ExtraPostPlacementOpt`, `phys_opt_design -directive AggressiveExplore`, `route_design -directive AggressiveExplore`, post-route `phys_opt_design -directive AggressiveExplore`; design argv from `sw/builder/out/endstation_ax7101_1x1_tdm8/soc_params.json` (regenerated by `build.sh` from `configs/endstation_ax7101_1x1_tdm8.yaml`). Session 11:07:05 to 11:53:28.

| Metric | This image (`d81198c20`) | Round 1 image (`dfa8f360`) |
|---|---|---|
| WNS / TNS | +0.065 ns / 0.000 (0 of 180,759 endpoints failing) | +0.107 ns / 0.000 |
| WHS / THS | +0.036 ns / 0.000 (0 of 180,678 failing) | +0.014 ns / 0.000 |
| WPWS / TPWS | +0.264 ns / 0.000 (0 of 64,012) | +0.264 ns / 0.000 |
| Sign-off corners (Slow/Fast, 0/85 C) negative-slack reports | "No timing paths found" at all four | |
| Route status | 106,333 of 106,333 routable nets fully routed, 0 with routing errors | |
| CRITICAL WARNING in `gateware/vivado.log` | 0 (the one grep hit is the IOB-pack Tcl source echo, a `##` line) | 0 (the same echo) |
| #607 constraint refusal | "no 12-4739, 20-1307 or 12-5201 diagnostics"; bitstream written | clean |
| Slice LUTs | 51,051 (80.52 %): 48,858 logic, 2,193 memory | 51,087 (80.58 %) |
| Slice Registers | 59,519 (46.94 %) | 59,522 |
| Slices | 15,834 of 15,850 (99.90 %) | 15,847 (99.98 %) |
| Block RAM Tile / DSP | 92.5 (68.52 %) / 14 | 92.5 / 14 |
| `milan_datapath` (placed) | 42,243 LUT, 48,314 FF | 42,272 LUT, 48,317 FF |
| `KL_aaf_clock_meter` (placed) | 483 LUT (451 logic, 32 LUTRAM), 630 FF, 0 RAMB, 0 DSP | 481 LUT, 630 FF |
| `KL_mmcm_drp_servo` (placed) | 897 LUT, 814 FF (own logic 790 / 770) | 898, 814 |

The image meets timing with no new critical warning and the #607 refusal clean. Bitstream `alinx_ax7101.bit` 3,825,992 B, sha256 `f9aa63859da17751732086cdba3277ff99c45628bc08ab615421919ef6e6a937`; `alinx_ax7101_timing.rpt` 1,338,063 B, sha256 `4baefaaef0e83068ef11d553e7b39a1d27cf33ecff5ca142ae4ae454fadb4d61`; `vivado.log` 604,290 B, sha256 `37f0f7f3fbde1ecf26cd39420fa32cd5c7d80795387081bea270d3a564d92f0e` (none copied here; the route status, placed utilization, hierarchical utilization, the four sign-off negative-slack reports and the timing summary excerpt are in `receipts/`). WNS fell by 42 ps against round 1's image on a placement that differs only in the split meter port; WHS rose by 22 ps; occupancy moved from 99.98 % to 99.90 %.

## Gates

Every command from the worktree at its physical `/data` path, unpiped, output to a log (copies or excerpts in `receipts/`). Suites on the pinned Verilator 5.050 under GNU make 4.3; Markdown gates in the pinned md venv. Final head `d81198c2001756fd84c353d93c312c133c5af66b`.

| Gate | Command | Head | Result |
|---|---|---|---|
| Suites, shard 0/5 | `scripts/run_all_suites.sh <out> --shard 0/5` | `d81198c20` (and earlier at `2253eca31`, the same) | rc 0: 11/11 suites, 401,934 checks, 0 failures (`receipts/shard0_final_summary.log`; earlier run `receipts/shard0_summary.log`) |
| Suites, shard 1/5 | `... --shard 1/5` | `d81198c20` (and earlier at `a2f173428`, the same) | rc 0: 23/23 suites, 196,276 checks, 0 failures; 4 declared skips (the `tsn_fuzz` field campaigns need an external generator not on this host, as in round 1) (`receipts/shard1_final_summary.log`; earlier run `receipts/shard1_summary.log`) |
| Suites, shard 2/5 | `... --shard 2/5` | `d81198c20` | rc 0: 12/12 suites, 1,523,706 checks, 0 failures; `milan_dp_mclk` A 55/0, C 32/0, B 50/0, campaign 31/31; `aaf_clock_meter` 446/0, servo 6/0, campaign 33/33 (`receipts/shard2_summary.log`) |
| Suites, shard 3/5 | `... --shard 3/5` | `d81198c20` (and earlier at `2253eca31`, the same) | rc 0: 12/12 suites, 14,649 checks, 0 failures (`receipts/shard3_final_summary.log`; earlier run `receipts/shard3_summary.log`) |
| Suites, shard 4/5 | `... --shard 4/5` | `d81198c20` | rc 0: 1/1 suite (`milan_dp`), 11,839 checks, 0 failures, 29.5 min; its `obj_aclk` leg prints the new two-sided INTERNAL check (`receipts/shard4_summary.log`) |
| Capture gate | `python3 scripts/check_nvm_capture.py`; `--mutation bytes`, `records`, `clock`, `ignore-off-timing` | `d81198c20` | rc 0 (all controls detected; receipt agrees); each mutation rc 1 |
| Builder test | `python3 sw/builder/test_builder.py` | `d81198c20` | rc 0: ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs an Arty `milanfinal48` build tree on disk; environmental, as in round 1) (`receipts/builder2.log`) |
| Port contracts | `python3 scripts/check_port_contracts.py` (+ `--selftest`) | `d81198c20` | rc 0: hdl 217 <= 217, 0 wildcard/positional/hierarchical |
| Naming | `python3 scripts/measure_naming.py --check` (+ `--selftest`) | `d81198c20` | rc 0: 95 candidates, all recorded |
| Entity shape | `python3 scripts/check_entity_shape.py` (+ `--self-test`) | `d81198c20` | rc 0: 166 checks, 0 failures |
| Docs gates | `docs_check.py`, `check_em_dash.py --base cdf49d1a` (+ `--selftest`), `check_doc_style.py` (+ `--selftest`), `gen_toc.py --check`, `--verify-anchors`, `--selftest`, `check_doc_paths.py` | `d81198c20` | rc 0 each |
| Hosted `docs-check` / `wire-accountability` / `docs-check-no-git` replica | `docs_check_replica.sh` (this directory): 77 steps, every gate step of `docs.yml` but `make -C gptp-processor docs` (writes into the submodule) and `act_ci.py --selftest` (candidate runner, CI-only) | `d81198c20` | 77/77 rc 0 (`receipts/docs_replica_final.log`); wavedrom steps with `wavedrom==2.0.3.post3` (the workflow's pin) in a scratch venv |
| `git diff --check` | worktree; `cdf49d1a HEAD` | `d81198c20` | rc 0 both |
| Lint ratchet | `python3 scripts/lint_rtl.py --check` (+ `--self-test`) | `d81198c20` | PASS, 90 <= 90 |
| Vivado front end | `python3 scripts/xvlog_gate.py --check` (Vivado 2026.1 environment) | `d81198c20` | PASS: 4 findings == ratchet, 0 in `hdl/` (`receipts/xvlog1.log`) |
| Yosys portability | `syn/yosys/run.sh` | `d81198c20` | rc 0: 55/55 tops, TAP-PURITY PASS (`receipts/yosys1.log`) |
| OOC area | `syn/yosys/ooc.sh KL_aaf_clock_meter KL_mmcm_drp_servo` | after `13721318e` | see Area |
| Idiom and evidence gates | `check_sv_idiom.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sh_idiom.py`, `measure_test_evidence.py --check` (each + self-test) | `d81198c20` | rc 0 each (in the replica) |
| Root suite under make 4.3 | `make -C tb/verilator/milan_dp_mclk` | `62822ca69`; item 4 tree | 27/27 rc 0; 31/31 rc 0 (before: rc 2 at `d048e48b7`) |
| R432-1 F2's own verification | `MAKEFLAGS=w MAKELEVEL=1 make -C tb/verilator/milan_dp_mclk` (GNU make 4.4.1) | `d81198c20` | rc 0: A 55/0, C 32/0, B 50/0, 31/31 (`receipts/mclk_makeflags_w.log`) |
| Meter suite with campaign | `make -C tb/verilator/aaf_clock_meter` | item 4 tree (committed as `21dbf51c0`) | rc 0: 446/0, 6/0, 33/33 in 743 s |
| Reviewer probes | `reviewer_meter_probes.py tb/verilator/aaf_clock_meter --work <scratch>` (R432-1 packet, unmodified) | `a2f173428` (no meter or RTL change after it) | 15/15 CAUGHT |
| `milan_dp` aclk leg | `make -C tb/verilator/milan_dp aclk` | item 6 tree | rc 0 (INTERNAL +0.80 ppm, two-sided check passes) |
| Shipping image | `TAG=a494m2d81198c2 sw/litex/build.sh ax7101` | `d81198c20` | WNS +0.065 ns, WHS +0.036 ns, 0 failing endpoints, 0 critical warnings, #607 clean, bitstream written |

## Parent-visible list

- RTL: `KL_aaf_clock_meter` gains `max_dev_ns_o[15:0]`; `status_o` narrows to `[15:0]`; three port contracts and two port comments. `milan_datapath` composes `AAFM_STAT` from the two (word unchanged). No top-level, SoC, root-parameter, processor-boundary or protocol-processor change; no CSR change.
- Tests: `tb/verilator/aaf_clock_meter` (new checks in M1, M3, M4, M6, M7, M12; six named mutants), `tb/verilator/milan_dp_mclk` (rows [TU] and switch (iv), mutants 15 and 16, `--no-print-directory`), `tb/verilator/milan_dp/sim_aclk.cpp` (two-sided INTERNAL rate).
- Scripts and harness: `scripts/nvm_shape.py` `closed_record_census`; `scripts/check_nvm_capture.py` uses it; `tb/verilator/nvm_capture_cpu/{run.py,soc.py,sim_main.cpp}`; the receipt `measurements.json`.
- Docs: FR_NFR (status row, FR-CLK-04), REGISTER_MAP (0x8C8 sentence), TIME_SYNC (W2 row), the design page (Implementation notes, trailing line), TESTING (two rows), the `milan_dp` and `milan_dp_mclk` READMEs, the capture harness README, SAVED_STATE_SNAPSHOT_OWNERSHIP sections 17, 18, 20 and SAVED_STATE_FASTCONNECT section 4.2's sizes.
- No generated file was edited by hand; none regenerated this round (the census change came from round 1's generators; `check_entity_shape.py` 166/0 confirms the copies are current).

## Observations outside #629 (for the manager to file if wanted)

- `tb/verilator/milan_dp_render/Makefile:57,62` and `tb/verilator/pp_shadow/Makefile:107` derive lists with `$(shell $(MAKE) -s -C ...)` and no `--no-print-directory`; under a nested GNU make 4.3 each list carries print-directory tokens (4 each, probed). Neither is reached by a default target today (`tdm8render-mutants` and `pending-mutant` are explicit), so CI is green; the fix is `62822ca69`'s one flag.
- `tb/verilator/fw_service_budget/oracle.json` records `image_bytes` 3264 and 12680, the pre-#629 images; it is a portable fixture no gate binds to the census, and its suite passes (hosted shard 1/5 green at `57f4b742`, local shard 1 green).
- `.github/workflows/docs.yml` (NVM record-space gate comment) says "156 of 256 ids at 8x8"; it is 164 now. Not edited: a workflow file, comment only.
- `docs/design/SAVED_STATE_FASTCONNECT.md:791` cites a descriptor image "measured at 40,000 bytes at 8x8"; the live 8x8 AEMI image is 19,520 bytes. Unrelated to #629 and left as is.

# HANDOFF: #649 side project (executor [A527])

Status: REVIEW READY at `da0dbc37437b58ac591467cd1b8daa9c8896cf6e` on `649-resource-map` (not pushed; five commits on
dev `241f9184`, one-line subjects, no body, no trailers). Every acceptance item is met; "Closes #649" in PR-BODY.md.

- Lane: `649-resource-map` from dev `241f91845230ae410506dffb16b71937127fd175` (remote and HEAD confirmed)
- Assignment: https://github.com/kebag-logic/milan-fpga/issues/649#issuecomment-5976977547
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/649#issuecomment-5976981437
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/649#issuecomment-5978158007
- Scratch: `$VALIDATION_STORAGE/649-a527/` (never in the tree)
- Packet: this directory

Commits (`git diff --stat 241f9184..HEAD`: 10 files, all new except one index row; no RTL, configuration, shipping
shape, gate baseline, workflow or existing script change):

| Commit | Subject |
|---|---|
| `3bc6528e` | Add the whole-image resource map of a routed checkpoint, tied block by block to the recorded route, with a self-test that plants one wrong figure per tie (#649) |
| `6b2363bf` | Add the design-parameter sweep: its plan, the Yosys driver with a Verilator guard check, the Vivado calibration anchor and the SoC option exports (#649) |
| `98cb840e` | Add the sweep's models, calibration and the generated findings tables, with a check that a page's tables equal a fresh generation (#649) |
| `8e499fd1` | Derive the SDK compiler triple in the SoC sweep as the baseline recipe does, from the SDK installer (#649) |
| `da0dbc37` | Record the whole-image resource map and design-parameter sensitivity findings for issue #649, indexed in the findings README |

Acceptance (#649):

1. Map blocks sum to the routed totals, method stated: met. 175 blocks, seven ties (page, "The map"); `TIED` on the
   reopened round-7 route; processor scopes equal #638's record.
2. Each parameter's per-unit cost at three or more points or justified, models with residuals: met. Streams (Vivado
   1x1/2x2/4x4; Yosys six points), channels (2/4/8), TDM slots (8/16/32), processor parameters (each at three or more
   guard-clean points), ADP interfaces (1/2/4); on/off blocks and options have one marginal each by nature; the
   render lane is structural (full bus width or pruned). Every fit carries per-point residuals, RMS and largest.
3. Yosys and Vivado calibrated at the anchor points: met. Four anchors (1x1, 2x2, 4x4, tracked 8x8), totals and per
   block, both Yosys instruments, plus the route over OOC.
4. Scripts, receipts and findings page published; no RTL, configuration or gate baseline change: met (in the PR at
   this head; receipts in this packet).

## Progress log

- 07:36 remote and HEAD confirmed; skeleton written; TAKEN posted.
- 07:40 Round-7 route of the #234 lane found on disk: `$VALIDATION_STORAGE/234-a516/C/work/ax7101/gateware/alinx_ax7101_route.dcp`,
  sha256 `769a04bb733f228110f99677201b5e97e4e770c53338803cd3423c9faf69f0ec` (equal to the #234 round-7 receipt). Its merge
  commit `4d81e10d` differs from dev `241f9184` only in docs and `syn/ooc/pp_resource_baseline.json`, so the route is
  dev `241f9184`'s image. Reused; no route re-run.
- 07:41 First reopen (`route-map/`) killed by me at 07:49 (rc 143) after 8 minutes: its census loop indexed the property
  lists by position (about 67 lines/s, a projected half hour of held lock). `route_map.tcl` now iterates the lists in
  parallel; relaunched as `route-map-2/` (queued on the shared lock).
- 07:43 Builder control: the scratch export's builder regenerates the tracked 1x1 shape header byte for byte.
- 07:52 `yosys_sweep.py shapes` (8 variant configurations, builder rc 0 each) and `roms` (three images equal to the
  ledger rows at `631eeb34` / `5dce647a`).
- 07:53 Yosys anchors running (ship, streams-2/4/8; hierarchical plus flattened), 2 at a time.
- 07:58 Vivado anchors (milan_datapath OOC, AreaOptimized_high, opt ExploreArea) queued detached on the shared lock:
  ship, streams-2, streams-4, streams-8.
- 08:21 to 09:21 anchors ship (rc 0), streams-2 (rc 0), streams-4 (rc 0); 09:24 streams-8 rc 1 in 14 s (the NVM
  NAME guard, below); 09:27 ship-8x8 (tracked 8x8 configuration) queued, ran 10:05 to 10:29, rc 0.
- 08:43 to 09:36 all Yosys points (59), rc 0 each; 09:28 to 09:47 Verilator guard lint of every point (7 refused).
- 10:31 docs committed; 10:31 to 10:33 the 46 gates at `da0dbc37`, rc 0 each, worktree clean before and after.

## 1. Whole-image map

- 08:17 `route-map-2/` reopen: rc 0, 24 s under the lock; 129,908 primitive cells.
- 08:20 `resmap_map.py map route-map-2 --out map-out`: TIED. 175 blocks (leaves), depth 5; LUT 50,767, FF 59,634, slices
  15,832.00, CARRY4 3,506, RAMB36 79, RAMB18 27, DSP 14, equal to the route-1x1 record and the flat report.
- First tie run found that 21 flip-flops sit in I/O tiles (ILOGIC/OLOGIC: GMII TX/RX, TDM bclk/fsync/dout), which the
  report's FF column (slice registers) leaves out; the census now counts them apart (`IOB_FF`), and a self-test arm
  plants exactly that mistake.

## 2. Parameter inventory

In the findings page, section "Parameter inventory" (three tables: datapath and entity shape, protocol processor, SoC),
with each parameter's source of truth (configuration key, builder output, `milan_soc.py` flag, RTL parameter or package
constant), shipping value and swept values, plus the `sweep.sh` stream-count trap (the fragment pins NS=1; only
`SWEEP_CFG` changes the shape; this sweep never uses `sweep.sh`).

SoC side measured fact: under the one software profile `milan_soc.py` refuses every CPU and cache variant
(`--l2-bytes`, `--xlen 64`, `--cpu-count 2`, `--with-fpu`, `--cpu naxriscv`, `--scala-args`), exit 2 with the refusal
recorded per variant in `receipts/run-receipts.json` (soc.exports). Pricing them would need a change to the recipe; this
lane does not make it and does not treat it as a STOP, because the assignment asks for "the options the LiteX build
exposes", and those are not exposed. The one accepted option with a resource effect is `--bus-standard axi-lite`.

## 3. Sweeps, points and receipts

Plan: `syn/resmap/sweep_plan.json` (54 points: 25 `milan_datapath`, 26 `KL_pp_shadow`, 3 `KL_adp_engine`; 9 variant
configurations; 8 SoC variants; the redundancy block list). Driver: `syn/resmap/yosys_sweep.py` (shapes, roms, run,
vivado-point, summary). Work directory `$VALIDATION_STORAGE/649-a527/sweep`.

- Final: 59 of 59 points rc 0 (26 datapath, 30 processor, 3 ADP); 7 refused by an elaboration guard (Verilator):
  streams-8, streams-8-chans-2, pp-names-235, pp-line-288, pp-line-512, pp-line-1152, pp-ctrl-32.
- Large outputs kept in scratch, digests: `summary.json` 1,454,596 B sha256 `8f8060f52183f9ee...`; `models.json`
  463,073 B `0b779e3204695ca6...`; `route-map-2/map_cells.tsv` 12,531,872 B `b377ddec33c438bc...`.
- 25 of 25 datapath points rc 0 (sv2v, hierarchical; the 4 stream anchors also flattened). Wall time 3.5 to 4 minutes
  per 1x1 point, 35 minutes for the 8x8 flattened mapping.
- `summary`: every point's blocks tie to Yosys's own `design` totals, at depth 3 and depth 1.
- Vivado anchor `ship`: rc 0, 15 minutes under the lock. OOC opt 43,622 LUT / 48,697 FF / 36 BRAM tiles / 14 DSP
  against the routed `milan_datapath` 42,200 / 48,433 / 36 / 14.
- Vivado anchors after opt: 1x1 43,622 LUT; 2x2 48,361; 4x4 55,288; tracked 8x8 60,454 (receipts: `run-receipts.json`).
- SoC: `soc_sweep.py export` (ship and axilite accepted; six refused, each with its refusal line), `price` rc 0.
- Per-point receipts (inputs, ROM digests, shape-header digest, outputs, rc, seconds): `receipts/run-receipts.json`.

### The 8x8 TDM8 refusal and the guard check (09:24 to 09:30)

- The `streams-8` Vivado anchor exited rc 1 in 14 s: `Synth 8-6058 KL_nvm_backend: N_NAME_P=235 outside 1..128: the NAME
  block is 0x80..0xFF` (`hdl/milan/KL_nvm_backend.sv:289`). The builder accepts the 8x8 TDM8 variant (235 writable names);
  the RTL refuses it. Yosys had mapped it (and `streams-8-chans-2`, and `pp-names-235`) without complaint.
- Cause, measured: sv2v converts an elaboration `$error` in a generate block to `initial $display("Error [elaboration]
  ...")`, which Yosys ignores; neither `syn/yosys/ooc.sh` nor `syn/yosys/run.sh` looks for it. A tooling gap worth its own
  issue (not filed: this lane may post only on #649).
- Answer in this lane: `yosys_sweep.py guards` lints every point with the pinned Verilator 5.050 (`USERERROR` is the
  evaluated guard). Refused points are listed and left out of every fit. The eight-stream anchor is now the tracked
  `endstation_ax7101_8x8` configuration (TDM32, 107 names), point `ship-8x8`, run in both tools.
- Also worth an issue: the builder accepts a configuration whose AEM name count exceeds the NVM NAME block (128).

## 4. Models and residuals

All generated by `syn/resmap/resmap_models.py` (fits by least squares, residual per point, RMS, largest) and rendered
by `syn/resmap/resmap_tables.py` into the page's delimited table blocks (`--page ... --write` fills them; without
`--write` it checks they equal a fresh generation). Copies: `models.json`, `tables.md` in this packet.

- Streams, Vivado OOC after opt, three on-line anchors (1x1, 2x2, 4x4): per stream per direction +3,828 LUT,
  +2,911 FF, +1.5 BRAM tiles; residual RMS 394 LUT (1 to 2: +4,739; 2 to 4: +3,464 each). Processor 2,478 LUT and
  1,155 FF of it; `KL_chan_map_capture` 317, `milan_csr` 211, `KL_avtp_rx_monitor_ctx` 209, `KL_render_setpoint` 205.
- Streams and channels, Yosys, y = a + bN + cC + dNC over six guard-clean points: LUT 13,881/stream (RMS 1,228);
  FF 3,202/stream (RMS 81); channel terms within residuals.
- TDM capture slots 8/16/32 (render pruned): within 7 LUT and 6 FF. Render lane: 1,060 LUT / 1,113 FF Yosys, 499 / 623
  routed.
- Optional blocks: marginals per point with the routed block where it ships (taps 674/621, RX filter 512/1,570, servo
  899/814, MAAP 479/267, AAF meter 483/630, gPTP plane 5,004/5,899); probes and loopback small; PPS +156/+294 and
  I2S playback +673/+678 Yosys; LPF nothing while I2S playback is pruned; no-CRF -6,552 Yosys (two processor contexts).
- Processor (KL_pp_shadow, Yosys, three or more guard-clean points each): controllers 635 LUT each; RX slots 215 LUT, 79 FF,
  ~1 BRAM tile each; descriptor index 3.45 LUT/entry; names 1.7 LUT and 1 FF each (to the 128 limit); descriptor line
  nothing measurable over 576..1,008; RX slot bytes 1.2 LUT/byte; RX FIFO bytes nothing; units/domains ~107 LUT each;
  controls nothing; stream contexts 5,886 LUT/stream (super-linear).
- ADP interfaces (redundancy seam): +239 LUT / +76 FF for 1 to 2, +493 / +226 for 1 to 4.

## 5. Yosys-to-Vivado calibration

- Totals, Vivado after opt over Yosys hierarchical: 0.447 (1x1), 0.422 (2x2), 0.402 (4x4), 0.355 (tracked 8x8); over
  Yosys flattened 0.404, 0.393, 0.379, 0.349; FF over flattened 0.99 to 1.02.
- Per block at 1x1 (Vivado opt over Yosys): 0.02 (`@own`) to 38 (`ptp_csr_sync`, Yosys leaves inverters as INV cells
  that the ooc.sh columns do not count); explained outliers listed in the page, three others not explained.
- In context: route over OOC opt is 0.967 for the whole datapath and 0.88..1.06 for every block above 1,000 LUT.

## 6. Ranked opportunities (with function cost)

In the page, "Ranked opportunities": 1 processor redesign and its levers (#640; #232, #230, #639); 2 the CSR block's
structure (3,073 LUT, +211/stream); 3 one microcontroller instead of two (gPTP 2,088 + AECP 1,716; bounded by 1,716);
4 RX address filter prune (512 LUT / 1,570 FF / 247.4 slices; promiscuous policy either way); 5 latency taps prune
(674 / 621 / 190.9; instrumentation lost); 6 loopback lane and probes (~35 LUT). Not recommended, with the function
each carries: render lane, CRF ports, AAF meter, servo, MAAP, gPTP plane, fewer controllers (FR-CTRL-03). Ranks 4 to 6
total about 1,200 routed LUT, a tenth of the 12,727-LUT NFR-RES-01 gap.

## 7. Gates

Runner: `scratch-scripts/run_gates.py` (never committed; derived from the #234 lane's), every gate in the foreground,
no pipelines, GNU Make 4.3 first on `PATH`, `PYTHONDONTWRITEBYTECODE=1`. Final run at `da0dbc37`: 46 of 46 rc 0,
worktree clean before and after (ignored files included), 2.5 minutes (`receipts/gates/gate-results.json`, one log
per gate). Highlights: the five new self-tests (map 11 of 11 arms; sweep, SoC, models, tables PASS); `docs_check` 0
findings with and without git; `check_em_dash --base 241f9184` 0 findings over 1,062 added lines; `gen_toc --check`,
`--verify-anchors`, `--selftest`; `check_doc_paths` 907 paths resolve; `check_baremetal_only`; `pp_srcs --check
--selftest`; `check_rtl_source_lists`; `ooc_selftest` 75 arms; `pp_resource_gate check-baseline` 3 endpoints;
`check_py_idiom` and the other code-quality ratchets; `ci_scope`/`ci_events`; `make -C gptp-processor docs`;
`git diff --check` against the base and in the worktree. An early run at `98cb840e` (worktree not yet clean) found one failure, `check_baremetal_only.py`:
`soc_sweep.py` spelled the SDK triple literally (a retired-stack term); fixed in `8e499fd1` by deriving it from
`scripts/ci_rv32_sdk.py` as the recipe does. The SoC exports and prices were rerun with the fixed script: identical.

## 8. Open items

- The issue's "short summary comment on #229 and #640" is not posted: this lane may post only TAKEN / REVIEW READY /
  STOP on #649. Draft for the maintainer: `summary-comment-229-640.md`.
- Two findings worth their own issues (not filed, same reason):
  1. The Yosys flows (`syn/yosys/run.sh`, `syn/yosys/ooc.sh`) do not enforce elaboration guards: sv2v turns a
     generate-block `$error` into `initial $display("Error [elaboration] ...")`, which Yosys ignores. A refused
     configuration maps and the portability gate would pass it. This lane's sweep checks every point with Verilator.
  2. The builder accepts a configuration whose AEM writable-name count exceeds the saved-state backend's 128 NAME
     records (the 8x8 TDM8 variant, 235); the RTL refuses it at elaboration and Vivado in synthesis.
- The new scripts' self-tests are not wired into a CI workflow: that would change `.github/workflows/*` and the
  `scripts/ci_events.py` pins, outside this measurement-only scope. They run by hand (commands in the PR body).

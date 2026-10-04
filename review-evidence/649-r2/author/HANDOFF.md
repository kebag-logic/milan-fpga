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

## Round 2

Status: REVIEW READY at `4742d2c02c109f7dd8e21d74905efb182b2dbca2` on `649-resource-map` (not pushed): round 1's five
commits, the `--no-ff` merge `689a9010` of dev `fea346e7`, and seven round-2 commits, one-line subjects, no body, no
trailers. Against the merged dev the lane still touches only its ten files (`syn/resmap/` and two findings pages).
Round-2 packet: `r2/` in this directory.
REVIEW READY (round 2): https://github.com/kebag-logic/milan-fpga/issues/649#issuecomment-5980922096

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/649#issuecomment-5978713464 (ruling: price the CPU, cache
  and L2 variants with a scratch-only recipe copy; Vivado OOC synthesis of the SoC, one run at a time under the lock).
- Reviews of `da0dbc37`: R466-1 (5978523295) NEGATIVE, R467-1 (5978705424) NEGATIVE; six and seven MINOR, no wrong figure.
- Round-1 head `da0dbc37`; dev to merge `fea346e76c2a57ed5cd131af8fc68dfeff57f877` (`--no-ff`).

| Item | Status |
|---|---|
| Ruling: CPU, cache, L2 priced by Vivado OOC from a scratch recipe copy | done: 20 syntheses, 2 variants not generatable (reason recorded), no STOP (R2.0) |
| 1 What is tied (page, README row, PR body, both script headers; arms per tie; depth comment) | done: census LUT tie on every row; Partition an identity; 15 arms; probes (R2.1) |
| 2 Leaf LUT sum and sharing adjustments by parent, generated | done: `map-lut-sharing` (R2.2) |
| 3 Growth wording (sub-linear) | done (R2.3) |
| 4 README 59 points; one census rate tied to a receipt | done: 64 lines/s (R2.4) |
| 5 Guard exclusion fails closed, with arms | done (R2.5) |
| 6 Re-runnable public inputs and logs in the packet | done, except the census (over the size limit; staged for the manager) (R2.6) |
| 7 Suggestions (full rank in fit(); HEAD and clean tree in sweep receipts; rest listed open) | done; S4 open (R2.7) |
| 8 Residue R467-1 RES-1..5, R466-1 RES1..4 | done (R2.8) |
| 9 Merge dev `fea346e7` (`--no-ff`) | done: `689a9010` (R2.9) |

### Round 2 progress log

- 11:55 round-2 assignment and both reports read; skeleton written.
- 11:58 dev `fea346e7` merged `--no-ff` as `689a9010` (brings only docs and testbench files; no RTL or recipe change, so
  every round-1 figure stands at the merged head).
- 12:00 census LUT probe: the distinct LUT sites (slice, LUT letter) each row's cells occupy equal the report's LUT,
  logic, LUTRAM and SRL columns on all 218 rows of the route (leaves and parents), so leaf LUT figures can be read
  twice. Made it tie 2 of `resmap_map.py`; Partition restated as an identity.
- 12:04 SoC pricing: scratch export of `689a9010`, scratch recipe copy `milan_soc_pricing.py` (exactly the two
  refusal blocks removed), scratch copies of the two CPU generator packages (PYTHONPATH first). A first launch was
  duplicated by mistake (two chains in one directory); both stopped, the scratch generator's compiled classes cleared
  and recompiled (26 s), one chain rerun 12:09 to 12:14.
- 12:14 exports: 18 of 20 generated (ship, ship through the tracked recipe, 16 variants); `fpu-f`, `fpu-fd` not
  generated (the core's FPU needs the M extension's unsigned-operand service); ISA ladder `isa-m`, `isa-mf`,
  `isa-mfd` added and generated. The scratch generator reproduces the cached shipping CPU netlist byte for byte
  (`c208df0b`). Shipping top through the pricing copy equals the tracked recipe's with comments removed.
- 12:17 Vivado chain queued on the shared lock (other lanes' runs ahead).
- 12:10 map self-test 15 of 15; tie mutation probe 12 of 12 tie mutants killed, 2 bookkeeping guards survive (stated);
  R467-1 probes run unchanged (results in section R2.1).
- 16:12 builder bank rc 0 (two environment arms not run); 48 of 48 gates rc 0 at `4742d2c0` (15:48); packet `r2/`
  assembled, cold re-run from its inputs rc 0; REVIEW READY posted on #649.
- 15:37 to 15:46 the three L2 points on the L1-cached core (added after the shipping-core L2 points priced the same as
  `ship`: the patched generator builds no L2 without an LSU L1), rc 0 each.
- 14:56 to 15:36 one hold: shipping SoC, the route reopen with the committed Tcl (rc 0, census byte-equal to round 1's),
  and 16 variants, every run rc 0.
- 14:55 second attempt at the shipping SoC: `opt_design` refuses primitives a black box drives (`Opt 31-30`); every
  variant is compared after synthesis from here on.
- 14:29 to 14:30 first hold: shipping SoC synthesized in about a minute (rc 0 to the synthesis report), then
  `opt_design` refused the black boxes (DRC INBB-3), rc 1; the batch stopped as designed and released the lock.
  Fix: lower only INBB-3 to a warning before `opt_design`; all 17 directories re-prepared (attempt kept as
  `r2/soc/vivado-ship-attempt1/`). 14:33 one hold for every run queued (`r2/chain_held2.sh`).
- 13:03 the per-run chain had waited 46 minutes without its first run (another lane's full build held the lock, two
  more lanes queued); stopped before it ever held the lock (no run started) and relaunched detached as two holds of the
  lock, each running its Vivado jobs one after another with a log and rc file per run (`r2/bin/held_batch.sh`).
- 13:00 commits `b7ae0a62` (map), `6d90dd64` (models), `dd05657c` (sweep receipts), `42c4f6c2` (SoC sweep wording).
- 12:16 models fail closed (missing or hard-error guard record stops the build), full rank asserted; R467-1's three
  F7 mutants caught. models.json regenerated: every fit identical to round 1.

### R2.1 What is tied (item 1; R466-1 F1 = R467-1 F1)

Chosen: an independent leaf-LUT reading, plus the stated limitation that Partition is an identity.

- `resmap_map.py` tie 2 (Census) now counts, per row (leaf AND parent), the distinct LUT sites (slice, LUT letter)
  the row's cells occupy, split by primitive into logic / LUTRAM / SRL, and requires the four report LUT columns to
  equal them. On the route: 218 of 218 rows equal, so every leaf's LUT figure and every sharing adjustment is read
  twice (the 17 adjustments, -356 in all, equal the census's shared sites parent by parent).
- Partition is no longer called a tie: the docstring and the page say it is an identity of the adjustment's
  definition. Ties are now five: Ancestry, Census, Flat report, Record, Depth. Slices are described as an attribution
  whose sum ties 3 and 4 compare. Two implied bookkeeping checks (census totals, names sum) are named as such.
- Self-test: 15 arms (was 11). New: a leaf's LUT figure outside the recorded scopes (R467-1 probe arm B's exact
  plant), a LUT site shared by two blocks, a LUT-RAM cell counted as logic, a stray-owner cell.
- `route_map.tcl` header now describes the depth check that exists (deepest row against the report's own requested
  depth; the census plays no part), and its census-rate comment gives the one measured rate (item 4).
- Mutation evidence (`r2/probes/`): `mutate_map_r2.py` disables each check in turn: 12 of 12 tie mutants killed;
  the 2 bookkeeping guards survive, as stated.
- R467-1 `probe_partition.py`, run unchanged: stops at its arm-A assertion (`assert stub != orig`), because the
  function it stubs, `partition_ties`, no longer exists; arms A and C are answered by the stated limitation
  (Partition is an identity, not a tie). Its arm B, extracted verbatim (header and arm B only), is caught:
  `census: top/leaf LUT counts 2 LUT sites, the report says 7`.
- R467-1 `probe_stray_owner.sh`, unchanged: stray-owner check disabled, self-test rc 1 (killed).
- R466-1 `mutate_map_selftest.py`, unchanged: stops at its `partition-off` assertion (mutation site gone).
- The real map at the new code: `TIED: 175 blocks, depth 5; LUT 50767, FF 59634, slices 15832.00, CARRY4 3506,
  RAMB36 79, RAMB18 27, DSP 14`; `blocks_ranked.md` and `partition.md` byte-identical to round 1.

### R2.2 The LUT sum (item 2)

Generated table `map-lut-sharing` on the page (new subsection "The LUT reconciliation"): the leaves' LUT, logic,
LUTRAM and SRL sums (51,123 / 48,891 / 2,228 / 4), every one of the 17 sharing adjustments by parent beside the
census's shared-site count for it, their sum (-356), and the image's top row (50,767). "Partition" is qualified for the
LUT columns in the page's method and in the `resmap_map.py` docstring.

### R2.3 Growth wording (item 3)

Page :626 (now the Yosys stream paragraph) and :741 (processor stream contexts) say sub-linear, with the residual
signs (Yosys datapath -, +, - at N = 1, 2, 4; processor -, +, +, - at 1, 2, 4, 8 ports) and the falling increments
(processor 10,780 then 5,632 then 5,229 per stream; ACMP talker 6,390 then 2,166; datapath own logic 5,046 then
4,082), consistent with the Vivado anchors (4,739 then 3,464). The README row says "a falling cost per added stream".

### R2.4 Consistent figures (item 4)

- README row: 59 Yosys sweep points (52 guard-clean, 7 refused).
- Census rate, one figure everywhere (page run receipts, `route_map.tcl`, this file): 12,248 complete census lines in
  the 190.4 s between the stopped first reopen's last log line (07:45:53.9) and its census file's last write
  (07:49:04.3), 64 lines/s, about 34 minutes for 129,908 cells. Receipt: `$VALIDATION_STORAGE/649-a527/route-map/`,
  `map_cells.tsv` (partial, 868,352 B, sha256 `56763a0be20f3053...`, over the packet limit) and `route_map.log`
  (6,740 B, sha256 `70e1dc88fd63eeb8...`). Round 1's "about 67" (page) and "about 35" (Tcl) are both replaced.

### R2.5 Guard exclusion fails closed (item 5)

- `resmap_models.refusals()` raises `GuardError` for a point with no guard record, or whose lint had hard errors (or a
  non-zero exit with no guard message); `build()` checks every summary point first and `main` exits 1 naming them.
  The three exclusion lines R467-1's probe targets are kept verbatim; the TDM model and the calibration now also
  exclude refused points.
- Self-test arms (synthetic plan and summary, exact lines with one refused point far off each): refused point out
  of the stream fit, the processor fit, the TDM model and the calibration; a missing record and a hard-error record
  each raise. Plus a rank-deficient design is refused (item 7).
- Real data: a copy of `summary.json` with `streams-2`'s guard record deleted: `models: refused, a point's guard
  record is not usable: streams-2: no guard record; ...`, rc 1 (`r2/probes/failclosed-missing-record.log`).
- `resmap_tables.py`: the page check is a function (`check_page`, the line R467-1 mutates kept verbatim) with arms:
  an equal page passes, a stale block fails, a block with no table fails, `--write` then checks equal.
- R467-1 `probe_selftests.py`, unchanged: its three F7 mutants are CAUGHT (stream fit, processor fit, page check);
  it then stops at its fourth arm's assertion (partition tie gone). Its remaining two arms, run from a copy with only
  that arm removed: guard lines ignored CAUGHT; "summary tie disabled" NOT CAUGHT, as in round 1: `yosys_sweep.tie()`
  compares the expansion with Yosys's totals and the blocks with them, and the blocks partition the expansion, so
  each comparison implies the other. Neither is claimed as a separate tie.
- R466-1 `guard_exclusion_probe.py`, unchanged: the exclusion-removal mutant is now killed (models self-test rc 1).
- `yosys_sweep.py guards` now catches a per-point failure, reports it and continues with the other points.
- `models.json` regenerated at the new code: every fit identical to round 1; only the `guards` key changed (no
  `unchecked` list: an unchecked point now stops the build).

### R2.0 Ruling: CPU, cache and L2 priced (R466-1 F6 = R467-1 F3)

Method (scratch only; nothing committed; tracked `sw/litex/milan_soc.py` unchanged):

- Scratch export of `689a9010` (`$VALIDATION_STORAGE/649-a527/r2/soc/tree`), the builder run on the shipping configuration,
  and a second copy of the recipe beside it, `milan_soc_pricing.py`, with exactly the two baremetal-profile `ap.error`
  blocks removed (`r2/inputs/soc-variants/pricing-copy.diff`; tracked recipe sha256 in `prepare.json`).
- CPU netlists generated by SBT in scratch copies of the VexiiRiscv and NaxRiscv LiteX data packages (PYTHONPATH
  first), never in the shared LiteX tree. Control: the scratch generator reproduces the cached shipping netlist byte
  for byte (`c208df0b`). The shipping variant through the pricing copy and through the tracked recipe gives the same
  top with comments removed (`strip_compare.py`); round 1's export differs only in scratch-tree paths.
- Vivado 2026.1 out-of-context `synth_design -directive default` of each exported top, the datapath and the parent's
  two SystemVerilog blocks black-boxed (1024-bit ports, as in the Yosys pricing), every variant reading the shipping
  BIOS ROM image. Compared after synthesis: `opt_design` refuses black boxes (first `DRC INBB-3`; with that lowered,
  `Opt 31-30`), two shipping attempts recorded (`r2/soc/vivado-ship-attempt1`, `-attempt2`, scratch).
- All runs one at a time inside holds of `flock /tmp/milan-vivado.lock` (14:56 to 15:36, 15:37 to 15:46).

Variants (generated table `soc-variant-prices` on the page; SoC = LiteX top + CPU after synthesis; changes against
`ship`; every one labelled "not buildable under the shipping software profile"):

| Parameter | Points | Result |
|---|---|---|
| CPU count | 1, 2, 4 | +1,484 LUT, +1,091 FF, +1.0 BRAM tile per core (RMS 2 LUT) |
| XLEN | 32, 64 (VexiiRiscv); 32, 64 (NaxRiscv) | +1,167 LUT (Vexii); +4,232 LUT, +12 DSP (Nax). Two-valued by nature; two bases |
| Recipe `--with-fpu` | RV64 with and without | no effect: the recipe passes it only to NaxRiscv; same netlist hash as `rv64` |
| FPU (core option) | none, F, F+D on the M core | F +2,569 LUT over M; D +3,548 LUT and +5 DSP over M+F; not generatable on the shipping RV32I core (below) |
| ISA M | I, M | +426 LUT, +4 DSP |
| L1 caches | none, fetch only, both at 1, 2, 4 ways | fetch +137 LUT, +1.5 tiles; both 1-way +1,210 LUT, +2,080 FF, +4 tiles; +132 LUT and +3.5 tiles per way (RMS 53) |
| L2 bytes, shipping core | 0, 8, 16, 32 KiB | no effect: the lane's patched VexiiRiscv SoC generator builds no hub or L2 for a core without an LSU L1 (`unified` fabric); the three netlists equal the shipping one with the module name normalized (sha256 `39bb485228a6faa3`) |
| L2 bytes, both L1 caches | 0, 8, 16, 32 KiB | controller +1,300 to +1,364 LUT, +1,696 to +1,789 FF over `l1-caches`; size costs only BRAM (+4 tiles per doubling), LUT per KiB inside its residual |
| Core | VexiiRiscv, NaxRiscv at RV32 and RV64 | Nax RV32 +14,348 LUT, +7,955 FF, +47 BRAM tiles (its default 128 KiB L2) |

- Not generated even from the scratch copy: `fpu-f`, `fpu-fd` (F and F+D on the shipping RV32I core): `Can't find the
  service vexiiriscv.execute.RsUnsignedPlugin`, a service only the M extension's multiplier and divider provide. The FPU
  keeps three points on the M core, so no parameter falls below three points for a generation failure: no STOP.
- XLEN and the core choice are two-valued by nature (each priced at two bases); the recipe's `--with-fpu` is a measured
  no-op on the shipping path. These are stated on the page, not fitted.
- Calibration: the shipping variant's synthesis is 1.13 times the routed LUTs of the SoC top's own logic and CPU (9,455
  against 8,371) and 1.16 times the CPU's (4,077 against 3,524).
- Receipts: `r2/inputs/soc_prices.json` (rc, start, end, log digest per run), the generated `soc-variant-receipts`
  table on the page, every variant's `synth_hierarchy.rpt` and `meta.json` in `r2/inputs/soc-variants/`.

### R2.6 Re-runnable public receipts (item 6)

Packet `r2/` (this directory), for the manager to publish as `review-evidence/649-r2/author/` on `649-review-evidence`
(the page names that path; if it is published elsewhere, the page's last paragraph needs the same change):

- `inputs/`: `map/` (`map_hierarchy.rpt`, `map_utilization.rpt`, `route_map.log`, `tcl.sha256`, from the round-2
  reopen with the committed Tcl); `work/summary.json.xz`; `work/vivado/{ship,streams-2,streams-4,ship-8x8}/{synth,opt}_hierarchy.rpt`;
  `work/soc/{exports,prices}.json`; `work/guards/<point>.json` for all 59 points including `ship-8x8`;
  `models/models.json.xz`; `soc_prices.json`; `soc-variants/` (each variant's reports, meta and Tcl; the pricing diff).
- `MANIFEST.json`: sha256 and bytes of every placed file and its source, and of 44 inputs kept out (Vivado and export logs,
  and the census).
- **Not in the packet: the census `map_cells.tsv`** (12,531,872 B, sha256 `b377ddec33c438bc...`), over the 200 KB limit
  even compressed. Both `map` and `tables --page` read it. A compressed copy is staged for the manager at
  `$VALIDATION_STORAGE/649-a527/r2/publish/map_cells.tsv.xz` (539,572 B, sha256 `65748b1fc8683938...`; decompresses to
  `b377ddec...`). Until it is published beside the packet, the "cold reviewer re-runs both commands" bar needs it.
- `logs/`: `resmap_map-map.log`, `resmap_models.log`, `resmap_tables-page.log` at the head, and
  `cold-rerun-from-inputs.log`: from a git archive of the head and the packet's inputs (plus the census), `map` TIED,
  `models.json` byte-equal to the published one, and `tables --page` "every table equals a fresh generation", rc 0 each.
- `probes/`: every reviewer probe re-run at the head (R2.1, R2.5), the mutation probe, the fail-closed check, the
  census LUT probe. `outputs/`: `map.json`, `blocks_ranked.md`, `partition.md`, `lut_sharing.md`, `tables.md`.
  `runs/`: the export and Vivado chain logs. `scratch-scripts/`: the pricing driver, the batch and launcher scripts,
  the collector and the gate runner.

### R2.7 Suggestions (item 7)

- Taken: `fit()` refuses a rank-deficient design (S3 / R466 S2); HEAD and a clean-tree check in every sweep receipt,
  a checkout with tracked changes refused by `run`, `guards` and `vivado-point` (S2 / R466 S1); the `ship-8x8` guard
  record published with the others (S5 / R466 S4).
- Open: a talker-only or listener-only point to split the 3,828-LUT per-stream cost by direction (S4 / R466 S3).
- Round-1 receipts predate the HEAD field; their figures are unchanged at this head (reviewers reproduced 19 points).

### R2.8 Residue (item 8)

R467-1 RES-1 (page :21 "In the rest of the datapath"), RES-2 (page "51 scopes, `pp_shadow` itself and 50 inside it"),
RES-3 = R466-1 RES2 ("could save up to about 1,200 routed LUTs"), RES-4 = R466-1 RES3 ("log or `stat.json` digest"),
RES-5 = R466-1 RES4 (PR body Status "every generated (`table:`-delimited) table"); R466-1 RES1 = R467-1 RES-1. All applied.

### R2.9 Merge (item 9)

`689a9010` = `--no-ff` merge of dev `fea346e7` (PR #648) into `da0dbc37`: seven documentation and testbench files, no
conflict, no RTL or recipe change.

### R2.10 Commits and gates

| Commit | Subject |
|---|---|
| `689a9010` | Merge dev fea346e7 into the issue #649 resource map lane |
| `b7ae0a62` | Tie every block's LUT columns to the placed-cell census, state the leaf LUT partition as an identity, and arm every tie in the map self-test (#649) |
| `6d90dd64` | Fail closed on a missing or hard-error guard record and refuse a rank-deficient fit in the sweep models, with self-test arms for both (#649) |
| `dd05657c` | Record HEAD and a clean tree in every sweep receipt, refuse a checkout with tracked changes, and keep guarding the other points when one fails (#649) |
| `42c4f6c2` | State in the SoC sweep and its plan that the refused CPU, cache and L2 variants are priced from a scratch-only recipe copy (#649) |
| `22dbc119` | Wrap the census LUT tie's failure message inside the 120-column limit (#649) |
| `80f3a3b7` | Render the LUT reconciliation and the CPU, cache and L2 variant prices and receipts as generated page tables, and self-test the page check and the variant tables (#649) |
| `4742d2c0` | Record round 2 of the #649 findings: the census-read map ties and LUT reconciliation, sub-linear stream growth, fail-closed guards, the CPU, cache and L2 prices and where the evidence is |

Gates at `4742d2c0` (`r2/scratch-scripts/run_gates.py`, every gate in the foreground, no pipelines, GNU Make 4.3 first
on `PATH`, `PYTHONDONTWRITEBYTECODE=1`): 48 of 48 rc 0 in 2.9 minutes, worktree clean before and after with ignored
files included (`r2/gates/gate-results.json`, one log per gate). The round-1 set plus `git diff --check` and
`check_em_dash` against the merged dev. Highlights: the five self-tests with their new arms (map 15 of 15; models,
tables, sweep, SoC PASS); `docs_check` with and without git; `check_em_dash` against both bases; `gen_toc` check,
anchors and self-test; `check_doc_paths`; `check_py_idiom` (over-long lines 0, after `22dbc119`); `pp_srcs`;
`check_rtl_source_lists`; `ooc_selftest`; `pp_resource_gate check-baseline`; `ci_scope`, `ci_events`; `make -C
gptp-processor docs`.

Also at the head:
- The table-equality check: `resmap_tables.py ... --soc-variants ... --page` "every table equals a fresh generation",
  rc 0 (`r2/logs/resmap_tables-page.log`); `resmap_map.py map` TIED rc 0; `resmap_models.py` rc 0, `models.json`
  equal to the published one.
- The builder bank (the docs workflow's `sw/builder/test_builder.py --require-rv32`, which runs the bank's arms that
  read pages under `docs/`): rc 0, "ALL GATES PASS EXCEPT 2 NOT RUN", in a git-listable scratch export of the head
  (scratch commits in the export and its three submodule copies, so its outputs never touch the lane), 20 minutes.
  The two arms not run say why: gate 1b's `MAKEFLAGS += -e` control (this make does not re-read MAKEFLAGS mid-parse) and
  gate 11 (needs an Arty `mf48` build tree that is not on this host). Log `r2/gates/builder-bank-require-rv32.log`
  (100,670 B, sha256 `ae5a6e61617b969c...`). Its `FAIL` lines are negative controls catching their mutants.
- One mistake on the way, corrected: a `--help` probe of the bank at 12:30 actually ran part of it in the lane, which
  left ignored build outputs (`sw/builder/out/`, two generated ROM images, `__pycache__` in the tree and in
  `protocol-processor/hdl/aecp/desc/`). Removed at once (`git clean -fdX` in the lane; the one submodule directory
  checked with `rev-parse --show-toplevel` first); the gate run's clean-tree checks include ignored files.

### R2.11 Open items for the manager

- Publish the round-2 packet `r2/` as `review-evidence/649-r2/author/` on `649-review-evidence` (the page names that
  path), and the census `$VALIDATION_STORAGE/649-a527/r2/publish/map_cells.tsv.xz` beside it if the cold re-run bar is to be
  met without this host.
- The #229 and #640 summary comment is still unposted; the draft `summary-comment-229-640.md` is updated for round 2.
- File the two tooling issues from round 1 (Yosys flows ignore sv2v-converted elaboration guards; the builder accepts
  235 names against the backend's 128). A third observation for the CPU work: `milan_soc.py`'s `--with-fpu` reaches
  only the NaxRiscv path, so on the shipping VexiiRiscv path it is a silent no-op (measured: the same netlist).
- Suggestion S4 (a talker-only or listener-only point) remains open.
- Hosted, act and exact-head long-gate acceptance; candidate merge on current dev; post-merge containment.

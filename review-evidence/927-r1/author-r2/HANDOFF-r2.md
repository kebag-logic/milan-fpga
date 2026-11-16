# #927 [A791] round 2 handoff — the split images' timing floor

Lane `927-8x8-timing`, base `dev-soft-core` `70f4056f`. Round 1 head `1010aa6f` (STOP, #927 issuecomment-6912069366).
Round 2 per the manager's ruling (#927 issuecomment-6914223799) and the scope widening (issuecomment-6908876362).
Nothing pushed; the manager pushes and opens the PR. Round 1's handoff: `../round1/HANDOFF-r1.md`.

## Status (kept current)

- [x] 1. the third cut: `KL_mbx_dma`'s ring address registered with `index_r` (+ plant "a step behind": caught)
- [x] 1b. every suite that builds `KL_mbx_dma` (mbx all, run-dma + dma-mutants, the split leg, the twin's split
      half, the CPU service-budget harness, the split boot)
- [x] 2. CPU service-budget harness 1x1/1if and 8x8/1if on the cut's RTL, as parallel part units, complete
- [x] 3. routes, S9's recipe, three directives: 8x8/1if (ExtraTimingOpt hold +0.029, reported), 1x1/1if (met); the
      release image at its own floor (met, gate PASS)
- [x] 4. ROM-fill spread, the recipe's directive: both shapes meet padded
- [x] 5. clean-clone runs (every target rc 0 but the twin's base-owned 2), native 4-shard sweep (65 of 65),
      workflow gates (0 bad at 0297a19a)
- [x] REVIEW READY on #927, posted once: issuecomment-6933066988 (2026-11-17 01:0x CET; text `comments/REVIEW-READY.md`)
- [x] round2/PR-BODY.md (head 0297a19a); receipts `receipts/INDEX.md` (264 files, `sanitize.py --check` rc 0)

## Routes at the round-2 cut (S9's recipe; WNS / WHS at the worst corner, ns)

**The floor is #818's: setup +0.030 and hold 0** (#927 issuecomment-6930885657, 2026-11-16 22:09 UTC: the prompts'
+0.030 on hold was the manager's error; #927 leaves the flip train and lands after the flip). Graded so, every route
below meets at every corner (`signoff.py`'s "issue floors" line in each receipt). Under the same floor the base misses
only 8x8/1if's recipe directive (+0.011 setup), flagged in REVIEW READY against the re-grade's "the base meets".

| Shape | Directive | WNS / WHS | #818's floor | Worst setup | Worst hold |
|---|---|---|---|---|---|
| 8x8/1if | ExtraPostPlacementOpt | +0.293 / +0.033 | met | CPU DMA bridge `downW_header_r` -> `pendings_valids_r` (clkout0) | MMCM servo `win_start_r` -> `pp_d_r` (5 levels, clkout1) |
| 8x8/1if | ExtraTimingOpt | +0.073 / +0.029 | met (hold under the prompts' +0.030 by 1 ps) | bridge FSM -> `KL_mbx/face_f_fmt_out_lo_r` CE, 11 levels | `KL_mbx/pub_src_sid_lo_r[0][5][26]` -> `KL_mbx_cdc/u_pub/data_hold_reg[1466]`, 0 levels, skew 0.277 (a copy across the backbone's centre) |
| 8x8/1if | AltSpreadLogic_high | +0.058 / +0.034 | met | the same bridge path, 12 levels | `KL_mbx/pub_src_sid_lo_r` -> `u_pub/data_hold_reg` again, +0.034 |

| 1x1/1if | ExtraPostPlacementOpt | +0.081 / +0.036 | met | bridge FSM -> `KL_mbx/face_f_pt_offset_r` CE, 14 levels | the render's `bank_r` -> `u_fcdc/g_mem.mem_r` RAM32M, +0.036 (distributed RAM now) |
| 1x1/1if | ExtraTimingOpt | +0.135 / +0.033 | met | bridge FSM -> `KL_mbx/u_evt/tag_r` CE, 15 levels | LiteEth rx converter -> `storage_4` block RAM (eth rx) |
| 1x1/1if | AltSpreadLogic_high | +0.126 / +0.033 | met | the same, 15 levels | the same |

1x1/1if meets on all three (#925's base image: +0.208 / +0.014 and +0.260 / +0.014 on the first two, the render
FIFO's block RAM). 1x1/1if place (ExtraPostPlacementOpt): LUT 31,979, LUTRAM 1,249, FF 42,311, slices 13,575
(85.65 %), BRAM 78 (60/36); the render FIFO is 32 RAM32M ("User Attribute" in synthesis).

**ROM-fill spread** (the recipe's directive, ExtraPostPlacementOpt; `fill_patch.py` 2,168 B read once in
`ctrl_plat_main.c`, the budget lifted 56 -> 57 in the scratch clone only):

| Shape | ROM at the head | Margin | ROM padded | Margin | Placed BRAM |
|---|---|---|---|---|---|
| 8x8/1if | 56.0 RAMB36 (130,200 B, one bank) | +0.293 / +0.033 | 56.5 (132,376 B; banks 128 KB + 2 KB) | +0.213 / +0.033, met | 92.5 at both (76 + 33): the 512-word tail bank maps to LUTs (below Vivado's ROM address threshold), as in #923's 56.5 image (92.5, 76 + 33) |

| 1x1/1if | 43.0 RAMB36 (117,488 B) | +0.081 / +0.036 | 43.5 (119,664 B; banks 64+32+16+4+2 KB) | +0.049 / +0.036, met | 78 -> 79 (60 -> 61 RAMB36) |

Padded 8x8/1if: worst setup the bridge -> `KL_mbx/face_f_fmt_out_hi_r` CE (10 levels), worst hold the datapath's
`ethernet_counters` copy (+0.033); LUT 42,076, FF 50,687, slices 15,544. Padded 1x1/1if: worst setup
`KL_mbx/u_evt/tick_cnt_r` -> its own reset (19 levels, +0.049), worst hold a CPU hub register into its LUTRAM
(+0.036); LUT 32,085, FF 42,315, slices 13,291. Receipts `receipts/route/f2-*-fill-*`.

**The release image** (`endstation_ax7101_1x1_tdm8`, all-fabric, integrated route at 338ece89, rc 0, 19:45-20:56):
WNS +0.553 / WHS +0.023 at the worst corners, against the release's floor (WNS >= +0.03, WHS >= 0): **met** at every
corner. `pp_resource_gate.py check --endpoint route-1x1 --shipping-selection`: **PASS** (LUT 52,012 -> 52,042, FF
53,707 -> 54,238, slices 15,780 -> 15,836, RAMB36 74 -> 71, WNS 0.44 -> 0.553, WHS 0.036 -> 0.023, each within its
tolerance; "re-baseline recommended: RAMB36 improved", not done: the baseline record is not this lane's to move).
Worst hold: the protocol processor's `u_aecp/u_resp/lane_ix_r` -> `storage_40_reg_0/DIADI` (a register written straight
into a block RAM, +0.023, 0 levels), RTL this lane does not touch. Receipts `receipts/route/rel2-head-1x1-tdm8-release`,
`receipts/release/`.

clkout1 (the datapath) is +0.771 / +0.865 / +0.865 on the three: the edit path no longer binds. The record mover's
family (round 1's +0.023 on ExtraPostPlacementOpt) is off every directive's worst list. Receipts
`receipts/route/h2-8x8-*`. 8x8/1if place: LUT 41,906, FF 50,655, slices 15,630 (98.61 %), BRAM 92.5 (76/33).

## CPU service-budget harness on the cut's RTL

- **1x1/1if, complete** (`--regrade` of the combined 96 groups, rc 0): 96 graded, 0 refusals, 0 of 130,341 passes over
  the per-pass share; 7 budget misses, all in `backlog-owed` (`backlog.owed` and `owed_behind0-3` 62.905 to 63.652 ms,
  the service's ACMP and AECP rows 62.002 and 61.736 ms, against 20 ms). **The base build's `backlog-owed`
  (`base-1x1/partq-o`) gives the same 7 lines to the microsecond**: the base's. The base's `backlog`, `aecp-fanout`,
  `acmp-notk` and `save-second` have no miss (save-second durable 6,030.359 ms against 6,070, as the head's).
- **8x8/1if:** 94 of 95 groups finished (`part-*`, `partq-0..3`), `save-second` running (`partq-4`). Part 1 exits 1
  on `backlog-owed`'s STATED lines (3 ACMP items over 5,500, 4 declined ACMP offers over 2,000) with 7 budget
  misses; **the base build's `backlog-owed` gives the same BUDGET and STATED lines** (`diff` empty): #914's per-shape
  statements, as #925 recorded. The base's `save-second` exits on two STATED polls-base lines (22,653 and 23,164
  over 22,500), durable 22,829.732 ms against 22,870.

## Changes (file:line, reason) — commits on round 1's 1010aa6f

| Commit | File:line | Change | Reason |
|---|---|---|---|
| 914d9d48 | `hdl/milan/mailbox/KL_mbx_dma.sv:182-195, 230, 297, 321, 337, 384` | `ring_word(base, mask, index)`; `ring_addr_r` loaded at the start with `ring_word(ring_base_i, ring_mask_i, ring_index_i)` and at each answer with `ring_addr_next_w = ring_word(base_r, mask_r, index_r + 1)`, beside `index_r`; `host_addr_o` reads it | the ruling's third cut: the mover's host address is a register equal to the old `ring_addr_w` in every cycle (no cycle, no contract change), so KL_mbx's write decode reads no mask-and-add |
| 3c18b5ec | `tb/verilator/mbx/dma_mutants.py:76-81` | `ring-index-unwrapped` re-anchored on `ring_word`; new `ring-address-a-step-behind`; `hold-address-moves` re-anchored on the R_S answer block | the cut's plant; keep the existing plants on the new code |
| f6170bf4 | `docs/design/MAILBOX_SPLIT.md:311-313`, `tb/verilator/mbx/README.md:39-44` | the registered ring address; 25 plants | docs |
| ef87d5c0 | `hdl/common/cdc_pair_fifo.sv:30-35, 105-128` | `DIST_RAM_P` (default 0): the storage in `g_mem`, two branches differing only in `(* ram_style = "distributed" *)` | the widened scope's TDM render FIFO path: a block RAM's write-data hold requirement (~0.243 ns) leaves the slot bank written straight into it at +0.014 to +0.023 ns at the fast corner (#925's routes at the base and at its head); distributed RAM's write path sits at +0.036 in the same routes |
| ef87d5c0 | `hdl/ieee1722/aaf/KL_tdm_render_master.sv:358-368` | `u_fcdc` with `.DIST_RAM_P(1)` | the render's 192 x 4 frame FIFO, 3 RAMB36 in #925's 1x1/1if image, into distributed RAM; the 8x8/1if image builds no TDM render (`tdm32`, no render slots), so only 1x1/1if changes |
| 5d098172 | `tb/verilator/milan_dp/Makefile:157-159, 249`, `tb/verilator/milan_dp_render/Makefile:74-83`, `tdm8_render_mutants.py` | `PAIRFIFO_SRC` override; a `fifo` source kind; the arm "the render FIFO's distributed storage written at the read pointer" | the remedy's plant, on the branch only the render takes |
| 0297a19a | `tb/verilator/milan_dp_render/tdm8_render_mutants.py:143-152, 297-308` | `FIFO_DIST_READ`; the arm becomes "the render FIFO's distributed storage read at the write pointer", naming `T6 FIRST EVENT` and `T6 PRESENTATION`; the `#632` comment back above its own arm | 5d098172's plant SURVIVED the clean-clone run at 338ece89 (31 of 32): the prefetch drains the crossing before each write, so the pointers are equal at every write and a write at the read pointer changes nothing. Read at the write pointer, the serializer gets the whole frame written three ticks before: IDENTITY passes, presentation fails (`one_render_arm.sh`, caught) |

## New checks (planted mutant, failing words)

| Suite | Plant | Caught by | Receipt |
|---|---|---|---|
| `mbx` `dma-mutants` | `ring-address-a-step-behind` | `D1 memory holds the record's bytes in ring order` | 25 of 25 caught, clean clone of 338ece89 (`receipts/editpath/at-338ece89/mbx__all.log`) |
| `milan_dp_render` `tdm8render-mutants` | the render FIFO's distributed storage read at the write pointer (0297a19a) | `T6 FIRST EVENT` and `T6 PRESENTATION` | caught alone (`one_render_arm.sh` on c-g1), then the full target on a clean clone of 0297a19a: 32 of 32 PASS, rc 0 (`receipts/editpath/at-0297a19a-h1/`) |
| same, 5d098172's arm | the storage written at the read pointer | (named `T6 IDENTITY`) | **SURVIVED**, clean clone of 338ece89 (`receipts/editpath/at-338ece89-g1`): replaced |

## Gate table

| Gate | Command | Head | rc | Receipt |
|---|---|---|---|---|
| Workflow jobs (rtl-fast, elaborate, docs) | `run_wf.py` per job on fresh clones; `verify_wf.py` | 338ece89 | 118 rc 0, 130 not run with a reason, 0 bad | `receipts/workflows/verify-338ece89.md` |
| Workflow jobs (rtl-fast, elaborate, docs) | the same, each batch on 8 CPUs | 0297a19a | 118 rc 0, 130 not run with a reason, 0 bad | `receipts/workflows/verify-0297a19a.md` |
| `mbx all` | clean clone | 338ece89 | 0 (record mover mutants 25 of 25) | `receipts/editpath/at-338ece89/` |
| `milan_dp` split, split-mutants, split-cdc, dynmap, maprec8, maprec4; `aaf_clock_meter` all; `tdm8render` | clean clone | 5d098172 | 0 each | `receipts/editpath/at-5d098172/` |
| `milan_dp twin`, `twin-plants` | clean clone | 5d098172 (base 70f4056f) | 2, 2 (the base's: same verdict lines) | `receipts/editpath/twin-verdict-head-5d098172.txt`, `base-70f4056f/` |
| `tdm8render-mutants` | clean clone | 338ece89 | 2: 5d098172's FIFO plant SURVIVED (31 of 32) -> 0297a19a | `receipts/editpath/at-338ece89-g1/` |
| `tdm8render-mutants` | clean clone | 0297a19a | 0: 32 of 32 | `receipts/editpath/at-0297a19a-h1/` |
| `dynmap-mutants` | clean clone | 338ece89 (0297a19a changes none of its inputs) | 0: 71 of 71 | `receipts/editpath/at-338ece89-g2/` |
| CPU service budget 1x1/1if | parts + `--regrade` | build 5d098172 | 0 | `receipts/budget/` |
| CPU service budget 8x8/1if | parts + `--regrade` | build 5d098172 | 1, STATED lines only (the base's) | `receipts/budget/` |
| Routes, release, ROM fill | S9's recipe; `pp_resource_gate.py` | 5d098172 / 338ece89 | 0 each; release gate PASS | `receipts/route/`, `receipts/release/` |
| Native sweep, 4 shards | `native-shards.py` (`run_all_suites.sh --shard k/4`) | 0297a19a | 0 each: 65 of 65 suites, 2,713,101 checks, 0 failures, 0 timeouts | `receipts/sweep/` |

## Notes

- **Power cycle at 15:40** (the host's memory upgrade). Recorded before it: 8x8/1if ExtraPostPlacementOpt rc 0
  (+0.293 / +0.033) and ExtraTimingOpt rc 0 (+0.073 / +0.029); every clean-clone suite with an rc
  (`editpath3/RUN-summary.txt`); the budget builds (rc 0) and the groups whose logs end in SUMMARY (1x1/1if 59 of 96,
  8x8/1if 34 of 95). Cut and rerun after it: 8x8/1if AltSpreadLogic_high (its half-written reports removed, the
  script kept), the rest of the route queue (`rt/tools/route_queue2.sh`, `q3/`), 12 unfinished harness files at each
  point (removed; their groups rerun in `partq-*`), `tdm8render-mutants` and `dynmap-mutants` (at 338ece89,
  `editpath4/`), and every workflow job (fresh run directory at 338ece89).
- **Host crash at 18:46** (a hard reset; back at 19:06). Recorded before it: 1x1/1if on all three directives (rc 0,
  collected), the 1x1/1if harness complete (regrade rc 0), 8x8/1if's harness parts 1-3 (rc 1, 0, 0), part 0's 15 of
  16 groups (their logs end in SUMMARY), `mbx all` and `tdm8render-build` at 338ece89 (`editpath4/`), every workflow
  job but the publication census, and the release image's export (rc 0). Cut and rerun after it: the release
  image's route (6 min into synthesis; its Vivado products removed, the export kept) and the ROM-fill images after
  it (`rt/tools/route_queue4.sh`, `q4/`); 8x8/1if's `save-second` (`partq-4`); the base samples' `acmp-notk` and
  `save-second`, with 8x8/1if's `backlog-owed` added to its base sample (`partq-r`); `tdm8render-mutants` and
  `dynmap-mutants` on fresh clones (`editpath5/g1`, `g2`: the two cut legs had shared one output directory, so
  `tdm8render-build` reruns in each). The publication census had already been OOM-killed at 17:22 inside its 10 GB
  unit: the run's jobs saw 32 or 128 CPUs where round 1's saw 8 (something widened the pool's affinity mid-run);
  rerun alone on 8 CPUs, as round 1's passing run (`census workers: 5 of 8`).
- **Host shutdown at 19:39** (maintenance; back at 19:43). Recorded between the two stops: `tdm8render-build` rc 0 on
  each fresh clone (`editpath5/g1`, `g2`); the base samples' `backlog` and `aecp-fanout` graded (`--regrade`, rc 0,
  0 budget misses at either point). Cut again and rerun from 19:45: the release route (its Vivado products removed
  again) and the queue after it, the census, the two mutant targets, and every harness group above (none had
  reached SUMMARY; their logs removed).
- **At 0297a19a** (22:1x): every workflow batch on a fresh run directory (`wf/launch_wf2.sh`, each batch pinned to 8 of
  the pool's CPUs), `tdm8render-mutants` on a fresh clone (`editpath6/h1`), and from 22:54 the native 4-shard sweep
  (`native-shards.py 927-a791-sweep`, booked 48-55, 24-31, 72-79, 64-71 through `cpu_ranges.pick8`, after every
  Vivado build had finished). `dynmap-mutants` stays at 338ece89: 0297a19a changes only the render's mutants file.
- Heads: the routes of 8x8/1if ran on `5d098172`'s clone; `65c76c13` (the regenerated module matrix) and `338ece89`
  (a doc comment moved in `cdc_pair_fifo.sv`, a plant's line wrapped) change no logic: `git diff 5d098172 338ece89
  -- hdl` is a generated README and comments. The harness builds are at `5d098172`, whose recorded inputs
  `338ece89` does not change.
- CPU bookings: none free from about 12:30 (and again within minutes of the 15:40 restart); campaigns, single legs
  and the route queue ran on the shared session pool (`rt/tools/unitpool.sh`), each its own unit under a memory cap;
  the resumed queue `queue3` took a booked range (32-47). After the 19:06 reboot all 128 were booked within
  minutes, so every rerun is on the session pool.

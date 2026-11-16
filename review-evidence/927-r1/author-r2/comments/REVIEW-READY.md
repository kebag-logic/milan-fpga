[A791] REVIEW READY — at `0297a19a`, 8x8/1if and 1x1/1if meet #818's floor on all three of S9's directives, and the release image meets its own

Commit: `0297a19a` (`927-8x8-timing`, thirteen one-line commits on `dev-soft-core` `70f4056f`). Nothing pushed; the PR body is with the manager.

**Changed in round 2** (per the ruling issuecomment-6914223799 and the scope widening issuecomment-6908876362):
- `914d9d48` `KL_mbx_dma.sv`: the record mover's ring address is a register.
  - It loads `ring_word(ring_base_i, ring_mask_i, ring_index_i)` at a transfer's start, and `ring_word(base_r, mask_r, index_r + 1)` beside `index_r` at each answer.
  - It equals the old `ring_addr_w` in every cycle, so no cycle changes and nothing the mailbox contract states changes.
  - `3c18b5ec` plants it a step behind (`index_r` for `index_r + 1`). `dma-mutants` catches it with `D1 memory holds the record's bytes in ring order`: 25 of 25.
- `ef87d5c0` `cdc_pair_fifo.sv` `DIST_RAM_P` (default 0): two `g_mem` branches that differ only in `ram_style = "distributed"`.
  - `KL_tdm_render_master` sets it for its 192 x 4 frame crossing: 3 RAMB36 become 32 RAM32M.
  - `5d098172` makes the shared FIFO plantable from the render mutants. Its first plant, the storage *written* at the read pointer, survived the clean-clone run at `338ece89`: the prefetch drains the crossing before every write, so the two pointers are equal at each write.
  - `0297a19a` replaces it with the storage *read* at the write pointer. That hands the serializer the whole frame from three ticks earlier, and `T6 FIRST EVENT` and `T6 PRESENTATION` catch it: `tdm8render-mutants` 32 of 32 on a clean clone of `0297a19a`.
- `f6170bf4`, `65c76c13`, `338ece89`: docs, the regenerated module matrix, the parameter's doc. Round 1's `a4a0c7dc`, `dfc6ce50`, `f6037ea4`, `a21e685d` and `1010aa6f` are unchanged.

**Routes, S9's recipe**, graded against #818's floor per issuecomment-6930885657: setup +0.030 and hold 0 at every corner (WNS / WHS at the worst corner, ns; 0 failing endpoints and 0 routing errors on every route):

| Shape | ExtraPostPlacementOpt (recipe's) | ExtraTimingOpt | AltSpreadLogic_high |
|---|---|---|---|
| 8x8/1if | +0.293 / +0.033 met | +0.073 / +0.029 met | +0.058 / +0.034 met |
| 1x1/1if | +0.081 / +0.036 met | +0.135 / +0.033 met | +0.126 / +0.033 met |

- **The least hold**, 8x8/1if ExtraTimingOpt +0.029, is `KL_mbx/pub_src_sid_lo_r[0][5][26]` -> `KL_mbx_cdc/u_pub/data_hold_reg[1466]`.
  - It is a copy with 0 logic levels across the clock backbone's centre, with 0.277 ns of skew at the fast corner, and the router stops at +0.029.
  - It is the meter pair's shape, on the publication crossing's hold register, a path #927 does not name. The same family is +0.034 on AltSpreadLogic_high.
- **Setup** binds on the bus clock: the CPU bridge's decode into `KL_mbx` register enables (11 to 15 levels), or, on 8x8/1if's recipe directive, inside the CPU's DMA bridge (+0.293).
  - The datapath clock is +0.771 or better at 8x8/1if. The edit path and the record mover's family are off every worst list.
  - 1x1/1if's render FIFO write path, +0.014 at the base (#925), is +0.036 on the recipe's directive in distributed RAM.
- **Release image** (all-fabric `1x1_tdm8`; it reads the meter, the datapath and the render FIFO, but neither mailbox file):
  - Integrated route: +0.553 / +0.023, which meets the release's floor (WNS >= +0.03, WHS >= 0) at every corner.
  - `pp_resource_gate.py check --endpoint route-1x1 --shipping-selection`: PASS. RAMB36 is 74 -> 71. The gate's re-baseline recommendation is not taken here.
  - Its worst hold is the protocol processor's `u_aecp/u_resp/lane_ix_r` -> a block RAM's `DIADI`, RTL this lane does not touch.
  - The release firmware is byte-identical to the base's: `bios.bin` and its disassembly, and the ELF and library with debug sections stripped.
- **ROM-fill spread**, the recipe's directive. Both meet at both fills:
  - 8x8/1if: +0.293 / +0.033 at 56.0 RAMB36, and +0.213 / +0.033 at 56.5 (as #923's image; placed BRAM 92.5 at both, also as #923's).
  - 1x1/1if: +0.081 / +0.036 at 43.0, and +0.049 / +0.036 at 43.5.

**Area**, placed on the recipe's directive, base -> head:
- 8x8/1if: LUT 42,607 -> 41,906 (−701), FF 50,722 -> 50,655, slices 15,415 -> **15,630 (+215)**, BRAM 92.5. Round 1's cut was LUT −517 beside slices **+187**.
  - On every directive the slices rise while the logic falls: slices +215 / +105 / +108 beside LUT −701 / −718 / −700.
  - The slice count is the placer's packing at 98.6 % of the device's slices. The base's own netlist moves 344 slices between directives.
- 1x1/1if: BRAM 81 -> 78. LUT as memory is +129 (the FIFO's 32 RAM32M), FF +184 (its read register now in fabric), slices 13,309 -> 13,575.

**Validation:**
- Clean clones:
  - At `338ece89`: `mbx all` (record mover 520,041 checks, 0 failures; its mutants 25 of 25; mbx mutants 12 of 12).
  - At `5d098172` (later commits change no logic): `milan_dp split` 143 checks, `split-mutants` 29 of 29, `split-cdc` 13, `dynmap` 711, `maprec8` 219, `maprec4` 137, `aaf_clock_meter` all (mutants 38/38), `tdm8render` 263.
  - At `338ece89`: `dynmap-mutants` 71 of 71 (`0297a19a` changes none of its inputs). At `0297a19a`: `tdm8render-mutants` 32 of 32.
  - The split boot passes at both shapes (each route's prep).
- `milan_dp twin` and `twin-plants` exit 2 at the head and at the base `70f4056f`, with the same verdict lines (the owed row `split-talker-failed`; the `srp-plus-k` plant's escape). These are the base's.
- **CPU service-budget harness on the cut's RTL**, each point complete as parallel parts:
  - 1x1/1if: 96 groups, 0 refusals, 0 of 130,341 passes over the share, rc 0.
  - 8x8/1if: 95 groups, 0 refusals, 0 of 270,769 passes over the share. It exits 1 on STATED lines only.
  - Both points' 7 probe misses are all in `backlog-owed`. The base build's `backlog-owed` gives the same lines at both points, and at 8x8/1if the same STATED lines (`diff` empty).
  - The base's `save-second` gives the same polls-base lines. These are #914's per-shape statements, as #925 recorded; no stated cost changes.
- Workflow jobs (rtl-fast, elaborate, docs), each on a fresh clean clone:
  - At `338ece89`: 118 steps rc 0, 130 not run with a stated reason, 0 bad.
  - At `0297a19a`: 118 steps rc 0, 130 not run with a stated reason, 0 bad.
- Native 4-shard sweep at `0297a19a` (after every Vivado build): 65 of 65 suites passed, 0 failed, 0 timed out; 2,713,101 checks, 0 in-suite failures.

**Acceptance criteria:** met.
- 1x1/1if and 8x8/1if each meet #818's floor on all three directives, with the ROM banking each image plans.
- Both still meet on the recipe's directive with the ROM padded to the composed train's size.
- The release meets its own floor, and its resource gate passes.

**Open risks/questions:**
- Under #818's floor, this lane's reproduction of the base on 8x8/1if's recipe directive is +0.011 setup (round 1's STOP; #919's and #920's figure), which misses the +0.030. The base's other split routes meet. If the re-grade in issuecomment-6930885657 read another directive or head, this is the figure to check it against.
- The release gate's re-baseline recommendation (RAMB36 74 -> 71) is left to the record's owner.

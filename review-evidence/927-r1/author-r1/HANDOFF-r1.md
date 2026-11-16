# #927 [A791] round 1 handoff — split 8x8/1if timing floor

Lane: `927-8x8-timing`, base `dev-soft-core` `70f4056f`. Nothing pushed (the manager pushes and opens the PR).
TAKEN posted: #927 issuecomment-6907845172.

## Status (kept current)

**STOP posted** (#927 issuecomment-6912069366, 2026-11-16 10:05): at the cut, 8x8/1if meets on ExtraTimingOpt
(+0.234 / +0.036) and AltSpreadLogic_high (+0.078 / +0.036) and misses on the recipe's ExtraPostPlacementOpt by
0.007 ns (+0.023 / +0.036), on the bus clock: `KL_mbx_dma/mask_r` -> `KL_mbx/face_f_fmt_in_lo_r` CE (the record
mover's ring address into the host write decode), a path #927 does not name. Decision asked: a third cut on the
mover's ring address (zero cycle cost, sketched in the STOP) in this lane, or an issue of its own. Text:
`comments/STOP.md`. Head `1010aa6f`, nothing pushed.

- [x] TAKEN (#927 issuecomment-6907845172)
- [x] 1. base reproduction at 70f4056f, 8x8/1if, the recipe's directive: +0.011 / +0.034, the #919/#920 path
- [x] 1a. setup path analysis; 1b. hold pair analysis (below)
- [x] 2. two logic cuts, committed (a4a0c7dc, dfc6ce50)
- [x] 3. tests: split leg `[EDIT]` + 3 plants (29/29 on a clean clone); meter 2 plants (38/38, lane tree)
- [x] release firmware image byte-identical; release gateware changes (stated); its route NOT run (stop)
- [~] 4. workflow gates 118 rc 0 / 130 reasoned / 0 bad; edit-path suites on clean clones (below; the twin's
      one finding is the base's); budget harness both points stopped part-way (identity receipt: no input
      changed); 8x8/1if three directives done (miss); 1x1/1if routes, release route, native sweep NOT run (stop)
- [x] STOP text; PR-BODY.md (state at the stop); receipts INDEX.md (regenerated at the end)

## Base reproduction at 70f4056f (step 1)

8x8/1if split platform image through S9's recipe (`rt/tools/route_image.sh` + `route_one.sh`, the integrated
run at the recipe's directive ExtraPostPlacementOpt; synthesis 21 min, peak 6.5 GB). Receipts:
`receipts/route/base-8x8-ExtraPostPlacementOpt/`.

| Corner | WNS ns | WHS ns |
|---|---:|---:|
| Slow 85C | +0.011 | +0.070 |
| Slow 0C | +0.011 | +0.070 |
| Fast 85C | +1.370 | +0.034 |
| Fast 0C | +1.370 | +0.034 |

- Floor (WNS and WHS >= +0.030 at every corner): **missed on setup**, as #919 and #920 measured at 659d7687
  (no HDL change 659d7687..70f4056f; the 8x8 export's ROM contents are the only difference between those
  heads' images).
- Worst setup: `KL_mbx_cdc/u_edit/rq_r_reg[80]` -> `milan_datapath/amap_edit_oclaim_expect_r_reg[599]/CE`
  (and `_word_r[599]`), +0.011 ns, 40 levels, clkout1; then `amap_edit_oclaim_cluster_r[116..125]` +0.018 and
  `[64..67]` +0.031, the same source. Bus clock worst +0.133 (`KL_mbx_dma/base_r` -> `KL_mbx/face_f_fmt_out_hi_r`
  CE, 12 levels); eth rx +0.339.
- Worst hold +0.034, `liteethmaccore rx_converter` -> `storage_4` RAM (eth rx). The meter pair is the hold
  floor's miss only in #919's ExtraTimingOpt and AltSpreadLogic_high runs (+0.014); this lane did not rerun those
  two at the base (step 1 asks for the recipe's directive).
- Utilisation (placed): LUT 42,607 (67.20 %), LUTRAM 1,141, FF 50,722, slices 15,415 (97.26 %), BRAM tiles 92.5
  (76 RAMB36 / 33 RAMB18), DSP 9, CARRY4 2,766; 87,998 nets routed, 0 errors.

## Routes at the cut (1010aa6f)

8x8/1if, ExtraPostPlacementOpt (integrated, synthesis 22 min): `receipts/route/head-8x8-ExtraPostPlacementOpt/`.

| Corner | WNS ns | WHS ns |
|---|---:|---:|
| Slow 85C / 0C | +0.023 | +0.102 |
| Fast 85C / 0C | +1.660 | +0.036 |

- clkout1 (the datapath, the cut's clock): worst +0.794 ns, `KL_mbx_cdc/u_edit/rq_r[98]` (record bit 34, the
  stream channel) -> `amap_edit_oclaim_expect_r[652]` CE, 24 levels (was +0.011 over 40). Post-synthesis the
  edit path left clkout1's worst list (base +0.581 at 39 levels; head's worst +1.208, an unrelated 0-level pair).
- Hold +0.036 (the CPU's probe RAM, the gPTP event queue's LUTRAM): over the floor.
- **Setup misses the floor by 0.007 ns on the bus clock (clkout0, 100 MHz)**: `KL_mbx_dma/mask_r[5]` ->
  `KL_mbx/face_f_fmt_in_lo_r[0][14][*]` CE, +0.023 ns, 12 levels (CARRY4=3), 9.794 ns, 70.5 % route, slices
  X64Y107 -> X63Y179. At the base's run of this directive the same family was +0.133
  (`KL_mbx_dma/base_r[0]` -> `face_f_fmt_out_hi_r[0][5]` CE). The logic: the record mover's
  `ring_addr_w = base_r + (index_r & mask_r)` (LUT3 + 2 CARRY4) is `host_addr_o` by default, and KL_mbx's host
  write decode (a CARRY4 range compare, 6 LUTs, fanouts 54/16/27) reads it for every register's write enable,
  the face block's included, although the mover only ever addresses ring words.

8x8/1if, ExtraTimingOpt: +0.234 / +0.036 (met); worst setup eth rx `KL_gptp_gmii_launch` reset paths, then the bus
clock's read multiplexer `rd_off_r` -> `reg_rdata_r` +0.303; clkout1 +0.650. AltSpreadLogic_high: +0.078 / +0.036
(met); worst setup the bus bridge FSM -> `KL_mbx/face_f_fmt_out_hi_r[0][3]` CE; clkout1 +0.739. Worst hold +0.036
on both (TDM capture LUTRAM), where the base held +0.014 (the meter pair). Receipts `route/head-8x8-*`.

**After the STOP was posted** (decision input, `route/head-8x8-ExtraPostPlacementOpt/bus-paths-by-source.txt`):
at the cut's ExtraPostPlacementOpt checkpoint, `get_timing_paths` over the bus clock's 2,000 worst endpoints. The
record mover's family is +0.023 to +0.026. The worst path from any other source is +0.133
(`KL_mbx/u_evt/tick_cnt_r[5]` -> `ctr_seen_r[0][4]`, 15 levels), then the read multiplexer +0.177 (18 levels), then
0-level reset paths from +0.273. So at this placement the mover's family is the only one under the floor; a cut
that takes about 1 ns off it would leave the bus clock at +0.133 there. A new netlist places anew, so this is
indicative only.

Area at ExtraPostPlacementOpt, base -> cut: LUT 42,607 -> 42,090, LUTRAM 1,141 -> 1,142, FF 50,722 -> 50,642,
slices 15,415 -> 15,602 (98.44 %), BRAM tiles 92.5 (76/33) both, DSP 9 both, CARRY4 2,766 -> 2,777; nets 87,998 ->
88,073, 0 routing errors. ROM: 8x8/1if 56.0 tiles (rom 130,200 B in one 131,072 B bank, 32 RAMB36; sram 24
RAMB36), the base's export's, ELF identical; 1x1/1if 43.0 (rom 117,488 B, 29 RAMB36; sram 14). Both unledgered,
<= 56: no S14 entry.

## Analysis (step 1, before any change)

### (a) Setup: `KL_mbx_cdc/u_edit/rq_r[80]` -> `amap_edit_oclaim_{expect,word}_r` CE (clkout1, 20 ns)

- `rq_r` is `KL_mbx_cdc_window`'s request register for the EDIT window; its layout is
  `{phase, remove, type, index, count, rec, record[63:0], value[63:0]}` (`KL_mbx_cdc.sv` u_edit), so bit 80 is
  record bit 16, the record's `cluster_offset[0]` (`amap_edit_co_w`), and the #810 variants' bits 82/84 are
  `cluster_offset[2]`/`[4]`.
- Logic, in order (40 levels, CARRY4=6 LUT2=3 LUT3=3 LUT4=6 LUT5=9 LUT6=13; 19.691 ns, 72 % route):
  1. 4 CARRY4: `cluster_offset` against the port's cluster count / the cluster index compares of
     `amap_edit_out_encode` (`milan_datapath.sv`, the function above `amap_edit_validate`);
  2. ~22 LUTs: the function's port-by-cluster priority search (`for p ... for c ... r = {1, CSRC[c]}`), the
     record's capture-source word and its valid bit `enc[13]`;
  3. 2 CARRY4 + 1 LUT: the word and cluster compares of the verdict (`obase_c == out_word`, cluster compares);
  4. ~10 LUTs: `amap_edit_accept_w`, the key decode and the claim enable (fanout 121 at the end), into CE.
- What a register cut can remove: stages 1-2 (about 27 of 40 levels) depend on the request's fields alone
  (`cluster_offset`, `descriptor_index`) and the shape's constants. Registering `amap_edit_out_encode`'s result
  removes them from every path to the claim registers, to the phase-5 live-write enables (#810's
  `amap_out_owner_r`/`amap_out_cluster_r` CE family, through `amap_edit_out_key_v_w` = `enc[13]`) and to the
  answer. Stages 3-4 read live state (claims, owner/cluster arrays, the live map, streaming levels) that a
  beat itself updates; registering them would need the answer a clock later.
- Cycle cost: none. `KL_mbx_cdc_window` loads `rq_r` only on `in_p_w` and goes to `PRE_S` (req low); it
  raises req no earlier than the next clock. So in every cycle `d_req_o` is high, `rq_r` equals the previous
  clock's, and a register of a function of `rq_r` alone holds the current request's value. The answer is taken
  in the same cycle as before; the mailbox contract's window bound (`MBX_WIN_EDIT_WAIT_CYCLES` 64) and every
  stated latency are unchanged. A cut of stages 3-4 would add a datapath wait cycle per beat (a contract
  latency change, a STOP): not taken.
- All-fabric: the processor drives the same face and may change fields in the cycle it raises req, so the
  register is the split's only (`generate` on `CTRL_SPLIT_P`); all-fabric keeps the combinational word.
- Note: at this head no split firmware drives the EDIT window (`mbx_win_read` is called only for GSI and CTR),
  so no co-simulation reaches the path; the split leg's new `[EDIT]` checks are its coverage.

### (b) Hold: `g_aaf_meter.aaf_clock_meter` `s2_ts_r[6]` -> `grp_ts0_r[6]` (+0.014 ns, Fast 85C)

Read from #919's 8x8/1if ExtraTimingOpt route report at 55769f09 (the same RTL as 70f4056f; its scratch copy).

- Both flops are on the same global clock net, `BUFG_1` (the PLL's `CLKOUT1`, `milansoc_crg_clkout1`,
  fo 33,688): no gated clock, no derived clock, no second buffer.
- They are placed in adjacent slices `SLICE_X43Y99` and `SLICE_X43Y100`. Row 100 starts a new clock region
  (7-series regions are 50 CLB rows), and on the 4-region-high xc7a100t the Y1/Y2 boundary is the clock
  backbone's centre: the source's leaf clock is fed from the lower half, the destination's from the upper.
  At the fast corner the clock arrives 0.834 ns after `BUFG_1` at the destination and 0.567 ns at the source.
  The common path's pessimism removal is 0.410 ns, which leaves 0.268 ns of skew.
- The data path is a copy with 0 logic levels: clock-to-out 0.128 ns plus 0.176 ns of route. The router fixes
  hold to 0 and no further, which left +0.014 ns.
- Logic remedy: the group's reference is now the next PDU's nominal timestamp, `ts_0 + i x PDU_NS`, exact mod
  2^32, in place of PDU 0's timestamp plus an offset. It loads through `s2_ts_r + PDU_NS` at PDU 0 and
  advances by `PDU_NS` per PDU, so the reference is no longer a copy of `s2_ts_r`. The deviation becomes one
  subtraction, and `grp_off_r` goes away (19 flops and 15 LUTs fewer out of context, Yosys). `pc_ts0_r` is `ref - (GRP-1) x PDU_NS`, no longer a copy
  of the reference. Bits [2:0] of every multiple of `PDU_NS` (125,000 ns) are zero, so those three bits of each
  remain a pass-through.
- `KL_aaf_clock_meter` is in every shape (`AEM_N_AAF_CLKSRC_C` != 0), so this changes the release netlist:
  stated in the STOP; the release image's route is owed (not run after the stop).

## Changes (file:line, reason) — commits a4a0c7dc, dfc6ce50, f6037ea4, a21e685d, 1010aa6f on 70f4056f

| Commit | File:line | Change | Reason |
|---|---|---|---|
| a4a0c7dc | `hdl/milan/milan_datapath.sv:4628-4649` | `g_af_amap_enc` keeps `amap_edit_out_enc_w` the combinational `amap_edit_out_encode(...)`; `g_sp_amap_enc` (`CTRL_SPLIT_P != 0`) registers it in `enc_r` (`amap_edit_enc_reg`, async reset as the edit block) | removes the port-and-cluster search (about 27 of the 40 levels) from every path from the EDIT request register to the claim, live-write and answer logic, at no cycle cost |
| a4a0c7dc | `hdl/milan/milan_datapath.sv:4681` | the validator reads `amap_edit_out_enc_w` instead of computing it | the one word, two sources by placement |
| a4a0c7dc | `hdl/milan/milan_datapath.sv:765-768` | `i_ctl_edit_*` port doc: held from the clock before req rises | the contract the register relies on |
| a4a0c7dc | `hdl/milan/mailbox/KL_mbx_cdc_window.sv:18-23` | header: the fields change only on an edge that leaves req low, req rises no earlier than the next edge | states the window's existing property the datapath now relies on (comment only) |
| dfc6ce50 | `hdl/ieee1722/crf/KL_aaf_clock_meter.sv:184` | `GRP_LAST_NS_C = GRP_NS_C - PDU_NS_C`, derived | the last PDU's nominal offset |
| dfc6ce50 | `KL_aaf_clock_meter.sv:306-314, 329, 424, 491, 505, 510` | `grp_ts0_r` + `grp_off_r` -> `grp_ref_r` (the next PDU's nominal timestamp): `s1_dev_w = s1_ts_r - grp_ref_r`; opened `s2_ts_r + PDU_NS_C`; advanced `+ PDU_NS_C`; `pc_ts0_r <= grp_ref_r - GRP_LAST_NS_C` | removes the 0-level copy `s2_ts_r -> grp_ts0_r` (the hold pair) and `grp_ts0_r -> pc_ts0_r`; bit-exact mod 2^32; 19 flops fewer out of context |
| f6037ea4 | `tb/verilator/milan_dp/sim_split.cpp:465-561, 769` | `[EDIT]`: `edit_beat`, `edit_one`, `check_edit` | the split's EDIT path had no check (README listed it "not held") |
| f6037ea4 | `tb/verilator/milan_dp/tb_split_top.sv:112-124, 417-424` | probes: live map words 0/1, channel 1's cluster, streaming, port 0's cluster count and CSRC words of clusters 0-2 (from the shape's own constants) | derived, never mirrored |
| f6037ea4 | `tb/verilator/milan_dp/split_mutants.py:83-98` | three arms | the cut's plants |
| a21e685d | `tb/verilator/aaf_clock_meter/mutants.py:220-228` | two mutants | the meter cut's plants |
| 1010aa6f | `docs/design/MAILBOX_SPLIT.md:1618-1630, 1642` | the crossing: the window's property and the split's registered word; split mutants 24 -> 29 (24 was stale: 26 at the base) | docs |
| 1010aa6f | `docs/design/MEDIA_CLOCK_FOLLOWING.md:2498` | meter area 636 FF / 574 LUT -> 617 / 559 (Yosys OOC, re-measured) | docs |
| 1010aa6f | `tb/verilator/milan_dp/README.md:1136, 1162-1172, 1187` | `[EDIT]` row; mutants 26 -> 29 and the three named; `EDIT` dropped from "not held" | docs |

## New checks (planted mutant, failing words)

| Suite | Plant | Caught by (failing words) | Receipt |
|---|---|---|---|
| `milan_dp` `split-mutants` | a request raised in the clock its fields load (`KL_mbx_cdc_window` IDLE_S -> REQ_S) | `[EDIT] phase 4: the next beat's held mapping 0 -> 0 is accepted` | editpath/split-mutants |
| `milan_dp` `split-mutants` | the record's word registered a clock late (`enc_q_r` behind `enc_r`) | `[EDIT] phase 4: the next beat's held mapping 0 -> 0 is accepted` | same |
| `milan_dp` `split-mutants` | the record's word encoded from its stream channel (`amap_edit_sc_w` for `amap_edit_co_w`) | `[EDIT] the ADD writes cluster 2's word into channel 1` | same |
| `aaf_clock_meter` `mutants` | `group_reference_not_advanced` | `[M2 indep] no history restart` | editpath/aaf_clock_meter |
| `aaf_clock_meter` `mutants` | `group_reference_opened_without_the_first_pdu` | `[M2 indep] no history restart` | same |

WIP (pre-commit, same content) runs: split leg 143 checks 0 failures; split mutants 29 of 29; meter 465 + 6 checks,
mutants 38/38.

## Edit-path suites on clean clones of 1010aa6f (`receipts/editpath/`)

`tools/editpath.sh` (clone `c-edit`) and, beside its long `dynmap-mutants`, `tools/editpath2.sh` (clone `c-edit2`):

| Suite target | rc | Result |
|---|---|---|
| `milan_dp split` | 0 | checks 143, failures 0 (`[EDIT]` included) |
| `milan_dp split-mutants` | 0 | 29 of 29 caught (the three new arms by their named checks) |
| `milan_dp split-cdc` | 0 | the crossing's structure and its twelve plants |
| `milan_dp dynmap`, `maprec8`, `maprec4` | 0, 0, 0 | the all-fabric map-edit legs |
| `milan_dp dynmap-mutants` | stopped | its listener-leg control failed (`[FAIL] the unmutated gateware does NOT pass the listener leg (caught)`); the dynmap, talker, maprec8 and maprec4 controls passed and 22 mutants were caught, none survived, when it was stopped at 11:2x. See "dynmap-mutants' listener control" below |
| `aaf_clock_meter all` | 0 | 465 + 6 checks; mutants 38/38 |
| `mbx all` | 0 | Wishbone/AXI-Lite/model legs 0 failures; cosim 32/0; record mover mutants 24 of 24; mutants 12 of 12 |
| `milan_dp twin` | **2** | one finding: owed row `split-talker-failed` does not hold. **The base 70f4056f gives the same rc and the same verdict line for line** (`twin-verdict-base-70f4056f.txt` against `twin-verdict-head-1010aa6f.txt`, same frame counts per half), so the finding is the base's, not this lane's |
| `milan_dp twin-plants` | not finished | stopped to run the base's twin on its CPUs (its control is the twin, which fails at the base) |

**dynmap-mutants' listener control.** The listener leg is `tb/verilator/milan_dp_render`'s `tdm8render`, which
`dynmap_mutants.py` builds itself, passing `-o ltn_rom.hex -o ucode.hex -o tdm8r_aemi.bin` (inputs its build "may
not remake"). `make dynmap-mutants` builds only milan_dp's legs, and no workflow runs it, so on a fresh clone where
`milan_dp_render` was never built those three files do not exist. This is the likely cause. The direct check, `make
tdm8render` at the head (which builds its own inputs), did NOT run: from about 10:30 to 12:30 the host had no free CPU range
(cpu_ranges.py: 126 of 128 busy, no hold acquiring), and a simulation runs only on booked CPUs. Owed next round: build
`milan_dp_render`'s inputs (`make -C tb/verilator/milan_dp_render tdm8render`), then `make -C tb/verilator/milan_dp dynmap-mutants`.
Neither cut can change that leg: the meter's outputs are bit-exact, and the all-fabric encode is the same function. Lane #925's sweep at its head
`09a948d4` (`70f4056f` merged; the same RTL as the base) passes `milan_dp_render` (tdm8_render 79 + 263 checks, 0
failures).

**For the manager (new work, not this lane's): the twin's owed row `split-talker-failed` is stale at
`dev-soft-core` `70f4056f`.** The row (`twin_compare.py:475`) owes "Talker Failed for both sources' streams from
boot, never withdrawn" (`New x2, JoinMt x89` each). At the base, the split sends Talker Advertise for STREAM_OUTPUT
0's stream (`New x2, JoinMt x19, Lv x1`), as the fabric does, apparently since #895/#901 ("a Talker declares only
while its SRP parameters are valid"). The twin's rule: a row whose findings have gone is a finding, so the lane
that fixed the defect deletes the row. I posted nothing about it (one STOP only).

## Gate table

| Gate | Command | Head | rc | Receipt |
|---|---|---|---|---|
| Base 8x8/1if split image, S9's recipe, ExtraPostPlacementOpt | `tools/pipeline.sh` (boot, `route_image.sh`, `route_one.sh` via vivado-slot.sh) | 70f4056f | 0; floor missed (setup +0.011) | `route/base-8x8-ExtraPostPlacementOpt/` |
| 8x8/1if at the cut, ExtraPostPlacementOpt (integrated) | `tools/prep.sh` + `tools/chain.sh` | 1010aa6f | 0; **floor missed** (setup +0.023, bus clock) | `route/head-8x8-ExtraPostPlacementOpt/` |
| 8x8/1if at the cut, ExtraTimingOpt | `chain.sh` (prep_directives3.py, `route_directive.sh`) | 1010aa6f | 0; met (+0.234 / +0.036) | `route/head-8x8-ExtraTimingOpt/` |
| 8x8/1if at the cut, AltSpreadLogic_high | same | 1010aa6f | 0; met (+0.078 / +0.036) | `route/head-8x8-AltSpreadLogic_high/` |
| 1x1/1if at the cut, three directives | `prep.sh` done (export at `rt/head1`); chain not run | 1010aa6f | NOT RUN (stop) | - |
| Release image route | `release_export.sh ... route` done (script written); route not run | 1010aa6f | NOT RUN (stop) | `release/` |
| Release firmware image hash, base and head | `release_export.sh` | 70f4056f, 1010aa6f | 0; byte-identical | `release/` |
| Workflow jobs rtl-fast, elaborate, docs | `run_wf.py` per job on a fresh clone (5 batches) | 1010aa6f | 0 (verify_wf.py: 118 rc 0, 130 reasoned, 0 bad) | `workflows/` |
| Edit-path suites on a clean clone | `tools/editpath.sh` (one make target each) | 1010aa6f | see "Edit-path suites" | `editpath/` |
| Split leg + mutants, meter + mutants (lane tree, the committed content) | `tools/sim.sh` | lane tree (= f6037ea4/a21e685d content) | 0; 143 checks; 29/29; 465+6; 38/38 | `wip/` |
| Lint ratchet | `scripts/lint_rtl.py --check` | 1010aa6f | 0 (89 <= 89) | `lint/` |
| placement_identity, recipe shape, base vs head | `pi_try.py` | 70f4056f, head | digests differ (stated) | `identity/` |
| Meter area, Yosys OOC | `syn/yosys/ooc.sh KL_aaf_clock_meter` | 70f4056f, head | 0; 574/636 -> 559/617 LUT/FF | `area/` |
| CPU service-budget harness 1x1/1if | `tools/budget.sh ... 1x1 ... 8` | 1010aa6f | running when the STOP was posted; stopped 10:33 with 63 groups logged, its CPUs given to the edit-path suites (none of its inputs changes, `budget/inputs-vs-diff.txt`) | `budget/run-1x1-partial.log` |
| CPU service-budget harness 8x8/1if | `tools/budget.sh ... 8x8-1if ... 8` | 1010aa6f | stopped 10:01 with 28 groups logged, its CPUs given to the bus-path query | `budget/run-8x8-1if-partial.log`, `budget/inputs-vs-diff.txt` |
| Native verilator sweep (4 shards) | `native-shards.py` (spec at `sweep/spec.json`) | - | NOT RUN (never beside a route; stop) | - |

## Notes

- Base clones: `rt/repo8-base` (route), `rt/repo-pi-base` (identity dump), both at 70f4056f, submodules from
  the lane's module stores.
- Vivado: the base route took slot 2 at 07:09 and the head 8x8 chain slot 2 at 07:57; the bus-path query slot
  1 at 10:18. The base chain's two other directives were not run (step 1 asks for the recipe's): its `chain.sh`
  was paused (SIGSTOP) during the integrated run and ended once that run had written its rc.
- Host CPUs were fully booked from about 10:30; the units stopped to free CPUs are listed in the gate table.

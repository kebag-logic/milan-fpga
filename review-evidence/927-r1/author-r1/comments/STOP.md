[A791] STOP — at the cut, 8x8/1if meets on two of S9's directives and misses on the recipe's by 0.007 ns, on the bus clock

Head: `1010aa6f`, five commits on `dev-soft-core` `70f4056f` (`a4a0c7dc`, `dfc6ce50`, `f6037ea4`, `a21e685d`, `1010aa6f`). Nothing pushed, no PR.
Stop condition: a timing miss after the three directives at the cut, on a path #927 does not name. Its remedy is a design question #927 does not settle.

**The base, reproduced at `70f4056f`** (S9's recipe, the recipe's directive): WNS +0.011 / WHS +0.034 ns. These are #919's and #920's figures, on the same path: `KL_mbx_cdc/u_edit/rq_r[80]` -> `amap_edit_oclaim_{expect,word}_r[599]` CE, 40 levels.

**The two cuts:**
- **Setup, the edit-claim enable.**
  - `rq_r[80]` is the EDIT record's `cluster_offset[0]`. About 27 of the 40 levels are `amap_edit_out_encode`'s port-and-cluster search, which reads the request's fields alone.
  - The split now registers that word (`milan_datapath`, `g_sp_amap_enc`) at no cycle cost. `KL_mbx_cdc_window` changes its fields only on an edge that leaves req low, and raises req no earlier than the next edge (`PRE_S`), so the register holds the current request's word in every cycle req is high.
  - The answer leaves on the cycle it did before. No window bound or stated latency of the mailbox contract changes. The all-fabric build keeps the word combinational.
- **Hold, the meter pair.**
  - Both flops are on one global buffer (`BUFG_1`, `clkout1`): no gated or derived clock.
  - They sit in adjacent slices across a clock-region boundary, `X43Y99` -> `X43Y100`, which on this device is the clock backbone's centre. Net of pessimism removal, the destination's clock arrives 0.268 ns after the source's at the fast corner.
  - The data path is a copy with 0 logic levels (0.304 ns), so the router fixed hold only to +0.014.
  - `KL_aaf_clock_meter` now holds the group's reference as the next PDU's nominal timestamp, `ts_0 + i x PDU_NS`, exact mod 2^32. It loads through `s2_ts_r + PDU_NS` and advances by `PDU_NS`, so the reference no longer copies `s2_ts_r`, and `pc_ts0_r` no longer copies the reference.
  - The deviation is one subtraction, and the meter is 19 flops and 15 LUTs smaller out of context. The outputs are bit-exact.

**8x8/1if at the cut, S9's recipe** (one synthesis checkpoint, the default seed; WNS and WHS at the worst corner, ns):

| Directive | WNS / WHS | Worst setup on clkout1 (the cut's clock) | Floor (+0.030) |
|---|---|---|---|
| ExtraPostPlacementOpt (the integrated run) | **+0.023** / +0.036 | +0.794 (the edit path's remainder, 24 levels) | **setup missed** |
| ExtraTimingOpt | +0.234 / +0.036 | +0.650 | met |
| AltSpreadLogic_high | +0.078 / +0.036 | +0.739 | met |

- Both base misses are gone. The edit-claim path no longer binds anywhere.
- The worst hold is +0.036 on the two directives where the meter pair held +0.014 at the base.
- Area at the recipe's directive, base to cut: LUT 42,607 to 42,090, FF 50,722 to 50,642, slices 15,415 to 15,602. BRAM (92.5 tiles) and DSP are unchanged.

**The path that now binds on ExtraPostPlacementOpt** is on the 100 MHz bus clock: `KL_mbx_dma/mask_r[5]` -> `KL_mbx/face_f_fmt_in_lo_r[0][14][*]` CE, +0.023 ns, 12 levels, 70 % route.
- At the base's run of this directive the same family was +0.133 ns.
- The record mover's `ring_addr_w = base_r + (index_r & mask_r)` is its default host address. `KL_mbx`'s host-write decode reads it for every register's write enable, the face block's included, although the mover only ever addresses ring words.
- Neither cut touches this clock. The new placement cost the family 0.110 ns.
- On the other two directives the bus clock's worst is the register read multiplexer (`rd_off_r` -> `reg_rdata_r`, +0.303 on ExtraTimingOpt) and the bridge's path into the face registers' enables (+0.078 on AltSpreadLogic_high).

**A remedy, not taken.** Keep the mover's ring address in a register that updates with `index_r`.
- At a transfer's start it loads `ring_base_i + (ring_index_i & ring_mask_i)`; at each answer, `base_r + ((index_r + 1) & mask_r)`.
- It always equals today's `ring_addr_w`, so it costs no cycle and changes nothing the mailbox contract states.
- It takes the mask-and-add (about 4 of the 12 levels) off every path from the mover through the host decode.
- It changes `KL_mbx_dma`, which is split-only RTL. The CPU service-budget harness builds that file, so its rows would be measured again.

**Decision needed.** Should this lane take that third cut, on a mailbox path #927 does not name, or should it be an issue of its own? If neither, which other remedy within the timing-flow rule? I have run no seed, no other directive and no constraint.

**Every other gate at this head:**
- **Workflow jobs** (rtl-fast, elaborate, docs), each on a fresh clean clone of `1010aa6f`: 118 steps rc 0, 130 not run with a stated reason (the hosted-only steps), 0 bad.
- **The split leg's new `[EDIT]` checks**, through `KL_mbx`, `KL_mbx_cdc` and the split datapath:
  - Phase 4 runs beat after beat with verdicts that alternate.
  - A REMOVE and an ADD go through every phase, and the live map's word is checked.
  - The leg passes on a clean clone.
  - `split_mutants.py`: 29 of 29 caught. Its three new plants are each caught by the check it names: the window raising req in the clock its fields load, the word registered a clock late, and the word encoded from the record's stream channel.
- **On the same clean clone:** `split-cdc`, `dynmap`, `maprec8` and `maprec4` pass. `dynmap-mutants`, the twin and its plants, the mailbox suite and the meter suite were still running when this was posted; their results go in the lane's handoff.
- **The meter suite, run in the lane's tree on the committed content:** 465 + 6 checks, and its mutants 38 of 38. The two new ones (the reference not advanced, and opened without the first PDU) are each caught by `[M2 indep] no history restart`. The clean clone's run is among those still going.
- **The release firmware image** is byte-identical: `bios.bin` and its disassembly, and the ELF with debug sections stripped.
- **The release gateware changes:** the meter, and the all-fabric datapath's elaboration (placement_identity's digest moves as the encode's call site moves; the logic is the same). Its route was not run.
- **The CPU service-budget harness:** none of its recorded build inputs is a file this head changes, and no firmware source changed, so it measures the base's image on the base's RTL. The 1x1/1if run is still going. The 8x8/1if run was stopped with 28 groups logged, to free CPUs.
- **Not run after the stop:** the 1x1/1if routes, the release route and the native sweep. Each is owed at the head the ruling leads to.
- **ROM per image:** 8x8/1if 56.0 tiles, with 130,200 B of `rom` in one bank, equal to the base's export. 1x1/1if 43.0. The firmware is unchanged. Both are unledgered and at or under 56, so no S14 entry.

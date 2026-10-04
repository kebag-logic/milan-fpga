# [A520] HANDOFF: #232 area lane (notification storage), processor branch `pp232-notify-ram`

Round 2 (assignment: milan-fpga #232 comment 5976892215, after R452-1 and R453-1 on PR
#153): **REVIEW READY** at head `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d`, not pushed
(posted as milan-fpga #232 comment 5978213864);
see "Round 2" at the end. Every item is done and no STOP condition arose. The new
coverage kills all 22 reviewer controls. The Vivado evidence, the lockstep bench and the
probes are published in `evidence-r2/`, and the parent patch is
`parent-adoption-232-241f9184.patch`. The earlier rounds' sections stand as recorded,
unless Round 2 says otherwise.

Round 1b (assignment: milan-fpga #232 comment 5974077269; lever 5 ruled (c), comment
5974004216): **REVIEW READY** at head `6e950fea861d76664dc2f7396c980b1ada2e47c1` (merge of `main`
`5c71928a` + #22's declaration reorder), not pushed; see "Round 1b" at the end. Sections 1 to 11
below are round 1's record at `3ab2e4da` and stand unless round 1b says otherwise: the
standalone figures of section 4 stand (R1b.6), and section 6's ruling is (c).

Round 1 status: STOP on lever 5 only (section 6: shrinking the counter stamps needs a timing or port-contract change; a ruling is asked). Everything else in the assignment is done and validated at head `3ab2e4da`: lever 1, the inventory, the valid/bulk split, the command queue, the exhaustion record, the response-buffer confirmation, the Vivado before/after, every processor suite and campaign, and the parent consumer set.

- Executor: [A520]. Reviewers: [R452] (internal), [R453] (external).
- Assignment: kebag-logic/milan-fpga#232, comment 5970460015 (epic #229; baseline PR #638 at `79e53831`).
- Processor repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked).
- Branch `pp232-notify-ram`, base processor `main` `f4167536d358c996f4e1b70b875879c1651f85d3` (HEAD checked at start).
- Head: `3ab2e4dace36b76b6a89135dd7f77c1412f9723d`. Three commits, one-line subjects, no body, no trailer, not pushed:
  - `9e29e2a8` RTL: the identity index, the row table in LUTRAM, the counter stamps without reset
  - `0c76b218` tests: `tb/aecp_notify` section IX, four controls in `notify_mutants.py`
  - `3ab2e4da` docs: 06 section 7 storage record, 09 section 8.4 row
- TAKEN: kebag-logic/milan-fpga#232 comment 5970465850.
- STOP (lever 5 ruling asked; the rest done at this head): kebag-logic/milan-fpga#232 comment 5973996744.

## 1. Outcome in one table

| | Lever 1, registry (`KL_aecp_notify.sv:329` at base) | Lever 5, counter stamps (`:392` at base) |
|---|---|---|
| Done | yes: row table in distributed RAM, cycle-exact | no: needs a timing or port-contract change (STOP item, section 6) |
| `rows_r` flip-flops (census) | 2,048 -> 0 | n/a |
| `ctr_last_r` flip-flops (census) | n/a | 192 at 1x1, 640 at 8x8, unchanged; reset dropped |
| `u_notify`, routed image | 3,171 LUT / 3,299 FF -> 2,327 LUT (960 LUTRAM) / 1,276 FF | |
| Whole routed image | 50,740 LUT / 59,631 FF / 15,839 slices -> 50,090 / 57,681 / 15,824; WNS +0.116 -> +0.143 ns | |

## 2. Changes (file:line at head `3ab2e4da`)

| File:line | Change |
|---|---|
| `hdl/aecp/KL_aecp_notify.sv:38-48` | banner: the walk keeps one walk port; the one all-rows check reads the identity index |
| `hdl/aecp/KL_aecp_notify.sv:330-336` | `rows_r` comment: three read indices, no reader sees every row |
| `hdl/aecp/KL_aecp_notify.sv:349-351` | write-strobe comment corrected (the index reads the written row on purpose) |
| `hdl/aecp/KL_aecp_notify.sv:399-404` | `ctr_last_r`: `ctr_sent_r` is its valid bit; bulk data, no reset |
| `hdl/aecp/KL_aecp_notify.sv:551-602` | the identity index (`IXC_W_C` 6-bit chunks, `N_IXC_C` 19; `g_ix_row[i].g_ix_chunk[j].mem_r` 64x1 LUTRAM per row and chunk; `initial` empty; write `ix_write`; `ix_wr_row_w = rows_r[wr_ix_r]`; `ix_own_w` the one 112-bit compare) and `command_registry_hit` reading it (the bank `rows_r[i]` compares at base `:539-546` removed) |
| `hdl/aecp/KL_aecp_notify.sv:1044-1045`, `:1053-1054` | `ix_clr_r`/`ix_set_r` reset and pipeline (`ix_set_r <= ix_clr_r`) |
| `hdl/aecp/KL_aecp_notify.sv:1362` | `N_APPLY`'s row write raises `ix_clr_r` |
| base `KL_aecp_notify.sv:934` | removed: `for ... ctr_last_r[c] <= 32'd0;` |
| `tb/aecp_notify/sim_main.cpp:209`, `:212-288` | section IX (`cancels_row0`, `identity_index`): IX1, IX2, IX3, IX4a, IX4, IX4b |
| `tb/aecp_notify/README.md:11`, `:19`, `:61-95` | build table; section IX and its mutation record |
| `tb/pp_top/notify_mutants.py:13-20`, `:57`, `:264-285` | docstring; `INDEX` suite (`tb/aecp_notify`, `make run`); `IDENTITY_INDEX` four controls |
| `tb/pp_top/README.md:2086-2089`, `:2133-2136` | notify record: 44 of 44, four `ix_*` rows |
| `docs/architecture/06_aecp_engine.md:864-866`, `:887-904` | realization status; "Storage (issue #232)" table and exhaustion paragraph |
| `docs/architecture/09_verification.md:280`, `:291` | two notification-block sections; the IX row |

How the index keeps the bank's behaviour, cycle for cycle (06 section 7 and the RTL comment
carry the same text): the 112-bit {eid, mac} is cut into 19 six-bit chunks; row i keeps one
64x1 memory per chunk with a 1 at its chunk value; a row matches when all 19 read 1 at the
command's chunks. A REGISTER (`N_APPLY`, the only writer of an identity) re-indexes its row
in the two cycles after the row write: the write's own cycle clears the old identity's bits
(the write-index read port still returns the old row), the next cycle sets the new
identity's. In those two cycles that row's match is one 112-bit comparator against the same
read port, which returns exactly what `rows_r` holds in each of them. The emission
write-back rewrites a row's own {eid, mac} with seq + 1 and leaves the index as it is. The
index starts empty (LUTRAM INIT 0; an explicit `initial`); bits enter only through a row
write, so a clear always empties the row. Neither the index nor `rows_r` is reset, as
before; a reset inside the window leaves the row invalid and its index a subset of its
identity, which the next REGISTER clears.

## 3. Tests and their controls

| Test | Where | What it proves | Control (killed) |
|---|---|---|---|
| Lockstep differential bench | scratch (`work/lockstep`), not committed | base `KL_aecp_notify` (renamed `_ref`, from `git show f4167536`) and the head file side by side; same inputs every cycle; every output and the internal `rx_cmd_hit_w` compared every cycle; 40 runs x 1,000,000 cycles; shapes N_CTRL/N_IN/N_OUT 16/2/2, 16/9/9, 2/1/1, 16/2/2 with identify, 5/8/8; protocol-shaped and fully random inputs; resets mid-run: **0 mismatches** | 7 planted copies of the head file, each with mismatches over 8 runs: no override 173,409; no clear 14,881,140; no set 11,083,946; override only in the set cycle 14,887,932; last chunk ignored 393,332; REGISTER not re-indexed 11,084,522; stamp read without its valid bit 49,343 |
| `tb/aecp_notify` IX1 | committed | the reused row refuses its previous controller | `ix_old_identity_kept`: IX1 |
| IX2 | committed | none of 112 identities one bit from a registered one matches | `ix_last_chunk_ignored`: IX2 |
| IX3 | committed | the registered identity matches in the command's cycle | `ix_new_identity_unset`: IX3, IX4 |
| IX4a, IX4, IX4b | committed | two cycles after a REGISTER, during the rewrite, the command still beats a failed probe in the same cycle; the failure alone removes the row | `ix_rewrite_unmatched`: IX4 |
| the IX bench on base RTL | scratch copy: `f4167536` `hdl/` + head `tb/aecp_notify` | 20 of 20 PASS: IX describes behaviour that did not change | n/a |

`notify_mutants.py --only` the four: 4 of 4 KILLED, golden `tb/aecp_notify` `make run` PASS.

Module-level choice (scratch; `KL_aecp_notify` alone at 1x1 16/2/2, 20 ns, AreaOptimized_high,
ExploreArea, placed):

| Variant | LUT (logic + memory) | FF | Slices (L + M) | WNS ns | `Synth 8-7186` |
|---|---:|---:|---:|---:|---:|
| base | 3,319 (3,223 + 96) | 3,323 | 1,315 (931 + 384) | +7.178 | 16 |
| A: per-row index, rewrite read through the walk port | 2,243 (1,377 + 866) | 1,280 | 1,006 (526 + 480) | +3.366 | 0 |
| B: per-chunk read-modify-write index, walk port | 2,288 (1,422 + 866) | 1,277 | 969 (511 + 458) | +4.256 | 0 |
| **C: per-row index, own read port (landed)** | 2,386 (1,426 + 960) | 1,280 | 1,000 (538 + 462) | +7.524 | 0 |
| D: per-chunk index, own read port | 2,376 (1,416 + 960) | 1,279 | 971 (456 + 515) | +6.987 | 0 |

A's worst path ran from `pend_r` through the drain index and the walk port into the new
comparator (16.4 ns); C gives the rewrite its own port and leaves the walk's paths alone. C
and D map to the same LUTRAM; C needs no read-modify-write.

## 4. Vivado before and after (#638 recipe and tools at `79e53831`)

Base: scratch parent dev `bbf704ec` + processor `f4167536` + c8-bbf704ec + p2-p1-1269cdaf.
Head: the same with the processor at `3ab2e4da`. Vivado 2026.1 build 6511674,
`xc7a100t-fgg484-2`, 50 MHz (20 ns), AreaOptimized_high / ExploreArea / ExtraPostPlacementOpt
/ AggressiveExplore, 32 threads, default seed. The base and head exports differ only in two
generated comments (a date, a tree listing's order); ROMs, Tcl, XDC and init files hash equal.

**Integrated shipping route, `endstation_ax7101_1x1_tdm8`, whole image**

| | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | CARRY4 | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | 50,740 | 59,631 | 15,839 (99.93 %) | 79 / 27 | 14 | 3,520 | +0.116 / +0.012 |
| head | 50,090 | 57,681 | 15,824 (99.84 %) | 79 / 27 | 14 | 3,373 | +0.143 / +0.027 |
| head - base | -650 | -1,950 | -15 | 0 / 0 | 0 | -147 | +0.027 / +0.015 |

LUT as logic 48,510 -> 46,993 (-1,517); LUT as memory 2,230 -> 3,097 (+867); SLICEL 11,091 ->
11,083; SLICEM 4,748 -> 4,741. Route status: all routable nets fully routed (base 106,340,
head 103,816), 0 with routing errors. The four signoff corners agree with the summary:
setup worst at Slow 0/85 C (+0.116, +0.143), hold worst at Fast 0/85 C (+0.012, +0.027).
Worst setup path: base `u_rx_validator/hdr_ctlr_eid_r_reg[3]` -> `u_tx_arbiter/FSM_onehot_arb_st_r_reg[0]/CE`,
38 levels, 19.485 ns; head `u_notify/wr_ix_r_reg[0]_replica` -> the same endpoint, 40 levels
(RAMS32 1, CARRY4 9), 19.593 ns. Both run through `rx_cmd_hit_w` and the existing
hit-to-arbiter chain.

Routed hierarchy (default flow; names rebuilt after cross-boundary optimization):

| Scope | LUT base / head | of which LUTRAM | FF base / head |
|---|---:|---:|---:|
| `milan_datapath/pp_shadow` | 24,175 / 23,407 | 1,108 / 1,972 | 24,276 / 22,257 |
| `pp_shadow/u_pp` | 23,597 / 22,835 | | 23,448 / 21,429 |
| `pp_shadow/u_pp/u_notify` | 3,171 / 2,327 | 96 / 960 | 3,299 / 1,276 |
| `pp_shadow/u_pp/u_aecp/u_resp` | 333 / 334 | 0 / 0 | 260 / 260 |

**Standalone `KL_pp_shadow`, 20 ns (`--integrated-clock`)**

| | LUT (logic + memory) | FF | RAMB36 / RAMB18 | DSP | CARRY4 | int. WNS ns (estimate) |
|---|---:|---:|---:|---:|---:|---:|
| 1x1 base | 24,494 (23,252 + 1,242) | 25,471 | 21 / 3 | 8 | 1,638 | -0.496 |
| 1x1 head | 23,600 (21,494 + 2,106) | 23,429 | 21 / 3 | 8 | 1,487 | -4.409 |
| 1x1 head - base | -894 | -2,042 | 0 / 0 | 0 | -151 | |
| 8x8 base | 31,383 (30,345 + 1,038) | 33,968 | 26 / 5 | 8 | 2,016 | -2.222 |
| 8x8 head | 30,458 (28,556 + 1,902) | 31,793 | 26 / 5 | 8 | 1,865 | -2.728 |
| 8x8 head - base | -925 | -2,175 | 0 / 0 | 0 | -151 | |

`u_notify` standalone: 1x1 3,194 LUT (96 LUTRAM) / 3,299 FF -> 2,261 (960) / 1,253 (-933 LUT,
-2,046 FF); 8x8 2,846 (96) / 3,799 -> 2,396 (960) / 1,753 (-450 LUT, -2,046 FF). Its head
cells (1x1): 1,253 FDRE, 1,301 logic LUTs, RAM64X1D 288 (576 LUTs), RAM32X1D 16 (32 LUTs),
RAM32M 88 (352 LUTs: `rows_r` 64, `cmdq_*` 24), CARRY4 179 -> 23.

The standalone timing figure is a synthesis estimate with no I/O constraints (as #638 states).
Its worst path at head starts at the same register as the routed one
(`u_pp/u_notify/wr_ix_r_reg[0]` -> `u_pp/u_tx_arbiter/slot_r_reg[0]/D`, 54 levels estimated);
at base it started at `u_notify/pend_r_reg[4]` (39 levels). The routed image, where the
replicated register closes it, improves from +0.116 to +0.143 ns.

Against #638's recorded A (its gate, `pp_resource_gate.py check`):

| Endpoint | base rc | head rc | Note |
|---|---:|---:|---|
| route-1x1 | 1 (+612 LUT, +625 FF over A) | 0 | base is the next adoption, not re-baselined (#638 ruling (d)); head passes, "re-baseline recommended" for FF |
| ooc-1x1 | 0 | 0 | head "re-baseline recommended" (LUT, FF) |
| ooc-8x8 | 0 | 0 | head "re-baseline recommended" (LUT, FF) |

Against #638's lever-1 estimate (about 2,000 FF and 1,500 LUT): FF -2,046 in `u_notify`
(standalone 1x1) as estimated; LUT -933 there, lower than estimated, because a same-cycle
match needs the 608-LUT identity index where the estimate assumed a serial walk with one
comparator (a timing change).

## 5. Storage inventory (#232 scope; 1x1; Vivado lines from each run's `baseline.log`, "Distributed RAM: Final Mapping Report" unless noted)

| Structure | Source (base) | 1x1 shape | Intended | Actual, base | Actual, head | Vivado lines (head 1x1 standalone `baseline.log`) |
|---|---|---|---|---|---|---|
| Notification registry rows `rows_r` | `KL_aecp_notify.sv:329` (head `:336`) | 16 x 128 | distributed RAM (attribute) | 2,048 FF; `WARNING: [Synth 8-7186] Applying attribute ram_style = "distributed" is ignored, object 'rows_r[0]' is not inferred as ram due to incorrect usage` (x16, base log lines 778-793) | distributed RAM | `\|u_notify \| rows_r_reg \| User Attribute \| 16 x 128 \| RAM32M x 64 \|` (line 2301); zero 8-7186 |
| Registry identity index (new) | head `KL_aecp_notify.sv:581-593` | 16 rows x 19 chunks x 64 x 1 | distributed RAM | n/a | distributed RAM: 288 RAM64X1D + 16 RAM32X1D | synthesis mapping report: `\|u_notify \| g_ix_row[0].g_ix_chunk[0].mem_r_reg \| User Attribute \| 64 x 1 \| RAM64M x 1 \|` (line 2302; 288 such rows) and `... g_ix_chunk[18].mem_r_reg \| ... \| 16 x 1 \| RAM16X1D x 1 \|` (16 rows, last at 2605); implemented cells after optimization: 288 RAM64X1D (576 LUTs) and 16 RAM32X1D (32 LUTs), which with `rows_r`'s 64 and `cmdq_*`'s 24 RAM32M make `u_notify`'s 960 LUTRAM (round 2) |
| Registry valid / TL / parked / monitor / probe flags | `:337`, `:410` (head) | 1 bit x 16 each | flops | flops | flops | (census FDRE) |
| Command notification queue `cmdq_*` | `:371-376` (head `:379-384`) | 16 x 132 (6 arrays) | distributed RAM | 24 RAM32M | 24 RAM32M | `\|u_notify \| cmdq_class_r_reg \| Implied \| 16 x 4 \| RAM32M x 1 \|` (2606), `cmdq_type_r_reg` x 3, `cmdq_index_r_reg` x 3, `cmdq_excl_r_reg` x 11, `cmdq_arg0_r_reg` x 3, `cmdq_arg1_r_reg` x 3 |
| Counter throttle stamps `ctr_last_r` | `:392` (head `:404`) | 6 x 32 (20 x 32 at 8x8) | flops (read in parallel every cycle) | 192 FF (640 at 8x8) | 192 FF (640), no reset | census `ctr_last_r_reg` FD cells |
| Packet pools: RX slots `mem_r` | `KL_pp_rx_slots.sv:193` | 5 x 2 K x 8 | block RAM | 5 RAMB36 | 5 RAMB36 | Block RAM report: `\|\g_rx_pool[k].u_rx_slots \| mem_r_reg \| 2 K x 8 ... \| 0 \| 1 \|` |
| AECP response storage | `KL_aecp_resp_buf.sv:336-339` | main memory at `RESP_BASE_P` | off chip | `u_resp` 260 FF, 0 RAM | 260 FF, 0 RAM | hierarchy: `u_resp` 260 FF in every run (route, 1x1, 8x8; base and head). The 5,079-FF spill of #229's history cannot recur: the module holds no array |
| Microcode `rom_r` | `KL_aecp_ucpu.sv:149` | 2,048 x 48 | block RAM | 3 RAMB36 | 3 RAMB36 | hierarchy `u_ucpu` RAMB36 3 |
| Microcontroller register file `rf_r` | `KL_aecp_ucpu.sv:159` | 16 x 64, 1W3R | distributed RAM | 33 RAM32M | 33 RAM32M | `\|u_ucpu \| rf_r_reg \| User Attribute \| 16 x 64 \| RAM32M x 33 \|` |
| Descriptor index `idx_r` | `KL_aecp_desc_store.sv:279` | 32 x 128 | distributed RAM | 22 RAM32M | 22 RAM32M | `\|\u_pp/u_aecp/u_store \| idx_r_reg \| Implied \| 32 x 128 \| RAM32M x 22 \|` |
| Descriptor lines and names `line_r`, `name_r` | `KL_aecp_desc_store.sv:291`, `:303` | 72 x 64, 312 x 64 | block RAM | 1 + 1 RAMB36 | same | Block RAM report: `line_r_reg \| 72 x 64 ... \| 0 \| 1`, `name_r_reg \| 312 x 64 ... \| 0 \| 1` |
| AECP map staging `amap_stage_r` | `KL_aecp_engine.sv:1188` | 256 x 64 | block RAM (attribute) | 1 RAMB36 | same | `\|KL_aecp_engine__GB0 \| amap_stage_r_reg \| 256 x 64 ... \| 0 \| 1 \|` |
| Trace ring `mem_r` | `KL_pp_trace_ring.sv:86` | 256 x 128 | block RAM | 1 RAMB36 | same | `\|u_trace \| mem_r_reg \| 256 x 128 ... \| 0 \| 1 \|` |
| TX slots `mem_r` | `KL_pp_tx_slots.sv:263` | 3 K x 8 | block RAM | 1 RAMB36 | same | `\|u_tx_slots \| mem_r_reg \| 3 K x 8 ... \| 0 \| 1 \|` |
| Timer slots `slot_ram_r` | `KL_pp_timer_service.sv:108` | 61 x 40 | block RAM | 1 RAMB36 | same | `\|u_timer \| slot_ram_r_reg \| 61 x 40 ... \| 0 \| 1 \|` |
| Dispatch queues `u_*_q/mem_r` | `KL_pp_dispatch.sv:302` | 4 x 393 (MAAP 2 x 393), four queues | distributed RAM (attribute) | 4 x 66 RAM32M | same | `\|u_dispatch \| u_aecp_q/mem_r_reg \| User Attribute \| 4 x 393 \| RAM32M x 66 \|` |
| Originator inflight `tslot_r`, `tout_r` | `KL_pp_originator.sv` | 4 x 6, 4 x 16 | distributed RAM | 4 + 3 RAM32M | same | `\|u_originator \| tslot_r_reg \| ... \| RAM32M x 4 \|`, `tout_r_reg ... RAM32M x 3` |

No AECP or notification data buffer maps into flip-flops at head. The notification flags and
the counter stamps are flops by design (each is read in parallel every cycle); the stamps are
lever 5 (section 6).

Exhaustion, per structure (no change to any; 06 section 7 records the notification half):
REGISTER into a full registry answers NO_RESOURCES; the command queue holds at most one
command's pushes because `amap_busy_o` holds the engine while anything is pending, and a push
into a full queue is dropped and counted (`cmdq_drop_r`, which no port reads); the counter,
stream-info, AVB-info, AS-path, lock and map classes coalesce into one pending bit per class
or descriptor; the response buffer is in main memory and holds no on-chip array. None needs a new defined behaviour, so the overflow STOP condition did not arise.

## 6. STOP item: lever 5, the counter throttle stamps (ruled (c), final for #232: comment 5974004216)

What the stamps do (base `:1034-1037`, head `:1093-1096`): in every cycle, for every served
descriptor c (6 at 1x1, 20 at 8x8), `ctr_dirty_r[c] && !ctr_pend_r[c] && (!ctr_sent_r[c] ||
(now_ms_i - ctr_last_r[c]) >= 1000)` moves the descriptor from dirty to pending. The stamp
is written at emission selection (base `:1237`, head `:1296`).

Why exact behaviour keeps them in flops: the condition reads every stamp against the
`now_ms_i` of the same cycle, and the module's port admits any `now_ms_i` sequence, so which
descriptors become pending in a cycle needs all stamps at once, which a RAM read port cannot
give. All 32 bits are needed: for an arbitrary `now_ms_i` the condition is false exactly on
`[last, last + 999]` modulo 2^32, which fixes `last`. Both ways to shrink the stamps change
something the rules hold:

- (a) Serialize the check over LUTRAM stamps, one per clock. A ripe descriptor's pending bit
  rises up to N_CTR_DESC_C clocks (6 or 20) after the ms tick that ripened it, and two
  descriptors ripened by the same tick can be emitted in scan order instead of index order:
  a timing change and possibly an ordering change.
- (b) Precompute, one stamp per clock after each ms tick, whether each descriptor is ripe at
  the next ms, and apply the flags at the tick. Cycle-exact inside the processor, where
  `now_ms_i` is `KL_pp_timer_service`'s `now_ms_o` (`now_ms_r + 1` per tick; ticks
  `CLK_HZ_P / 1000` clocks apart, 50,000 at 50 MHz, 100 in `tb/pp_top`'s compressed
  timebase). But it narrows `KL_aecp_notify`'s `now_ms_i` contract to "advances by one per
  tick, at least N_CTR_DESC_C + 2 clocks apart", a port-contract change. Estimated 192 FF
  to about 20 at 1x1 (640 to about 50 at 8x8) and 48 CARRY4 to about 8.
- (c) Keep them in flops (landed): only the reset is dropped, because `ctr_sent_r` is their
  valid bit. That is the "valid metadata separated from bulk arrays" item for this array and
  changes no behaviour (lockstep with mid-run resets: 0 mismatches; the control reading a
  stamp without its valid bit: 49,343). It frees no resource (the census is 192 / 640 FD
  cells at base and head).

Ruling asked: (c) as final for #232, or (b) as a follow-up with the `now_ms_i` contract
written into 02 and the integrator guide.

## 7. Processor suites (base `f4167536` in the lane; head from a `git archive` of `3ab2e4da`)

| Command | Base | Head |
|---|---|---|
| `./scripts/lint_hdl.sh` | rc 0, 41 of 41 | rc 0, 41 of 41 |
| `./scripts/run_suites.sh` | rc 0, 33 suites, 1,020,227 checks, 0 failing (871 s) | rc 0, 33 suites, 1,020,233 checks, 0 failing (1,012 s); only `tb/aecp_notify` moved |
| `tb/aecp_notify` | 14 checks | 20 checks (+6: section IX) |
| `tb/pp_top` | 9,196 checks | 9,196 checks |
| `make check` | | rc 0 (in the lane at head content): 41 mermaid + 18 wavedrom blocks, 1,105 links, 115 REQ rows, 94 matrix rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | | rc 0, 94 rows, 0 untested |
| `./syn/yosys/run.sh` | | rc 0: 36 of 36 tops elaborate (`KL_aecp_notify` among them); `KL_aecp_engine` Xilinx mapping OK |

## 8. Campaigns (the `tb/pp_top` set the assignment names, plus the two other drivers that build the top; base and head each from a `git archive`)

"Record identical" compares every arm's verdict and failing-check count (the drivers' `results.json`, or their printed record lines) between base and head. The hdl workflow's other campaigns (`tb/srp_top`, `tb/maap`, `tb/adp_engine`) and `tb/nvm_port figures` build no file this lane changes (their Makefiles do not list `KL_aecp_notify.sv` or the top) and were not run.

| Campaign | Base | Head |
|---|---|---|
| `ctr_mutants.py --jobs 4` | rc 0, control PASS, 17 of 17 KILLED (119 s) | rc 0, the same (132 s); record identical |
| `notify_mutants.py --jobs 4` | rc 0, 40 of 40 KILLED, goldens PASS (320 s) | rc 0, 44 of 44 KILLED, goldens PASS (391 s); the 40 identical (verdict and failing-check count), plus the four `ix_*` and the `tb/aecp_notify` golden |
| `acmp_mutants.py --jobs 4` | rc 0, 19 of 19 KILLED, goldens PASS (131 s) | rc 0, the same (128 s); record identical |
| `aecp_mutants.py --jobs 4` | rc 0, 60 checks PASS: 5 controls, 55 KILLED (330 s) | rc 0, the same (359 s); record identical |
| `aecp_dispatch_mutants.py --jobs 4` | rc 0, 41 checks PASS: 4 controls, 37 KILLED (340 s) | rc 0, the same (341 s); record identical |
| `d3_mutants.py --jobs 4` | rc 0, 87 of 87 KILLED, goldens PASS (1,600 s) | rc 0, the same (1,744 s); record identical |
| `gsi_mutants.py --jobs 4` (also builds the top) | not run (C7 record at `af751a5`: 20 detected, golden and restored PASS) | rc 0, 20 detected by named checks, golden and restored PASS (428 s) |
| `name_wr_mutant.py` (also builds the top) | not run (C7 record: decode killed) | rc 0, decode killed, golden and restored PASS (45 s) |

## 9. Parent consumer set (dev `bbf704ec` + c8-bbf704ec + p2-p1-1269cdaf, processor `3ab2e4da`)

Scratch parent `$VALIDATION_STORAGE/pp232-a520/parent` (never committed or pushed): clone of
kebag-logic/milan-fpga detached at `bbf704ecc3ef2e9cdd4cfdb72ec085e7428d1352`; submodules
`external` `efeb541a`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`,
`protocol-processor` (each `rev-parse --show-toplevel` checked before any git command in it);
the processor gitlink set in the index only (`git update-index --cacheinfo`); the two patches
(`parent-adoption-c8-bbf704ec.patch` sha256 `3340d2e8...a38a4c`, `parent-adoption-p2-p1-1269cdaf.patch`
sha256 `d3034e89...613d84`) applied with `git apply --check` then `git apply`. GNU Make 4.3
(sha256 `2cc4089a...234f`) and the pinned Verilator 5.050 wrapper (sha256 `905795b9...`) first on PATH.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 49 checks, 49 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,756 ports (C7's count), undocumented 111 <= 111 |
| 6 | `scripts/measure_naming.py --check` | 0 | all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | within ratchets |
| 8 | `scripts/docs_check.py` | 0 | 0 findings, 186 md + 970 files |
| 9 | `scripts/xvlog_gate.py --check` (alone) | 0 | 4 findings == ratchet (0 hdl/, 4 pinned processors), analysed at `protocol-processor@3ab2e4da` (147 s) |
| 10 | `sw/builder/test_builder.py` (alone) | 0 | Make 4.3: "ALL GATES PASS EXCEPT 2 NOT RUN": gate 11 needs the local mf48 build tree (as in the P1 record), and gate 1b's `MAKEFLAGS += -e` mutation, which Make 4.3 does not re-read mid-parse, so it has nothing to detect (1,183 s). Rerun alone with the host's Make 4.4.1: rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11 only, as in the P1 record) (1,143 s) |
| 11 | `scripts/lint_rtl.py --check` | 0 | |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures (288 s) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS, 0 FAIL; 4 render mutants caught; gmstep controls 6 of 6 (2,777 s) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | two-stream leg 65 checks and shipping leg 155 checks, 0 failures; leg defects 5 of 5 (664 s). T30 INTERNAL law: first-event delay 17,469..17,894 cycles = 8.385..8.589 media ticks, the P1 record's figure for `f4167536`; this bench's law depends on the feed's phase against the grid (#643), which the processor's boot length sets, so an equal figure is end-to-end evidence that the boot timing did not move. Nothing to record against #643 |

## 10. Parent-visible list

- No port, parameter, register or behaviour change: every output of `KL_aecp_notify` is
  cycle-identical (lockstep); the port gate counts 1,756 processor ports, as at C7.
- No parent patch needed; the generated exports at base and head are identical but for two
  generated comments.
- The routed image's worst setup path now starts in `u_notify` (`wr_ix_r`, replicated by
  phys_opt) instead of `u_rx_validator`; same endpoint, slack +0.143 ns (was +0.116).
- The #638 gate passes the head on all three endpoints and recommends a re-baseline
  (improvements beyond tolerance); recording one is the merge bank's step.

## 11. Run receipts

Vivado runs (scratch `$VALIDATION_STORAGE/pp232-a520/meas/<combination>/`; reports, checkpoints
and logs stay there, none in this directory). Each recorded input image rehashed equal after
the runs (6 of 6 per run). Every log: zero `Synth 8-4445` diagnostics (the one match is the
echoed `set_msg_config` line); `Synth 8-7186`: 16 per base log, 0 per head log. Base's 1x1 and 8x8
standalone syntheses ran beside each other and swapped (no OOM); head's ran one after the
other.

| Combination | Run | rc | Minutes | Log | Log SHA-256, first 16 | Log bytes |
|---|---|---:|---:|---|---|---:|
| base | Integrated route, 1x1 | 0 | 38.0 | `baseline.log` | `91c14839314a6d5a` | 607,592 |
| base | Standalone synthesis, 1x1 | 0 | 17.6 | `baseline.log` | `46897cb6e929dce0` | 245,625 |
| base | RTL elaboration, 8x8 parameters | 0 | 1.2 | `elaborate.log` | `ae63a6cb2a3ce6a2` | 216,560 |
| base | Standalone synthesis, 8x8 | 0 | 25.1 | `baseline.log` | `db02bbc29a04e090` | 247,475 |
| head | Integrated route, 1x1 | 0 | 34.1 | `baseline.log` | `c951b7a679df3c23` | 888,632 |
| head | Standalone synthesis, 1x1 | 0 | 18.8 | `baseline.log` | `ab9e117f1d659197` | 314,436 |
| head | RTL elaboration, 8x8 parameters | 0 | 1.1 | `elaborate.log` | `d3444f2d1beaed00` | 212,850 |
| head | Standalone synthesis, 8x8 | 0 | 23.3 | `baseline.log` | `1908735e4c6b333e` | 315,641 |

Verilator and parent runs (rc, seconds): base lint 0/11, base sweep 0/871, base campaigns ctr
0/119, notify 0/320, acmp 0/131, aecp 0/330, dispatch 0/340, d3 0/1,600; head lint 0/16, head
sweep 0/1,012, head campaigns ctr 0/132, notify 0/391, acmp 0/128, aecp 0/359, dispatch
0/341, d3 0/1,744, gsi 0/428, name_wr 0/45; parent gates 1 to 8, 3b and 11 rc 0 (1 to 8 s
each), 12 0/288, 13 0/1, 14 0/34, 16 0/664, 15 0/2,777, 10 0/1,183 (Make 4.3) and 0/1,143 (Make 4.4.1), 9 0/147. No command's
output was piped; every one wrote its own log and rc file.

Scratch evidence kept outside the tree: `$VALIDATION_STORAGE/pp232-a520/` (`work/lockstep`:
the lockstep bench, its generator and the seven control copies; `work/viv`: the module-level
variant runs; `base/`, `head-3ab2e4da/`: suite and campaign logs; `pgates-head/`, `pgates-head-make441/`: parent
gate logs; `meas/`: Vivado runs, `*-figures.json`, gate logs).

## Round 1b

Assignment: milan-fpga #232 comment 5974077269. Lever 5 ruled (c), final for #232 (comment
5974004216). Status: **REVIEW READY** at `6e950fea`, posted as milan-fpga #232 comment
5976213371. Every item done; no STOP condition arose.

- Head: `6e950fea861d76664dc2f7396c980b1ada2e47c1`, not pushed. Two commits on top of round 1's
  `3ab2e4da`, one-line subjects, no body, no trailer:
  - `823fc20c` the `--no-ff` merge of processor `main` `5c71928ad2bf1a854a5538d69b77214dfdf1697f`
    (P1 #150, C10 #149); parents `3ab2e4da`, `5c71928a`
  - `6e950fea` #22 in passing: `pd_any_w`/`pd_ix_w` declared above their first use
- Every measurement below is at `6e950fea` (the merge plus a declaration reorder; no logic
  change after the merge), from a `git archive`, unless a row says otherwise.

### R1b.1 The merge (item 1)

| File | Resolution |
|---|---|
| `tb/pp_top/README.md:2289-2294` | the one conflict, the notify mutation record's lead: P1's re-run note kept verbatim ("Re-run 2026-10-03 at lane P1's merge ... `main` alone still fails 20"), then this lane's sentence ("Issue #232 adds the four `ix_*` controls ..., for 44 of 44:"). The four `ix_*` rows stay at `:2338-2341` |
| `docs/architecture/06_aecp_engine.md` | merged without conflict: P1's name stage in the D3 contract (`:171-190`), the name write (`:457-458`) and the map records (`:549-552`), and this lane's §7 text (`:875-876`, "Storage (issue #232)" `:897-914`) |
| `docs/architecture/09_verification.md` | merged without conflict: P1's rows (AD8/AD9 `:161`, §8.2 `:176-178`, D3V, D3N, D3K, D3KR and the record-restore row `:190-194`, the 110 controls `:213-217`), C10's (NSD `:163`, the §8.6 `MAX_PAYLOAD_P` row `:357`), this lane's IX row (`:296`) |

Both sides' contracts are kept: P1's name stage, D3 amendment (§8.2, 110 controls) and D3KR;
C10's census (`syn/yosys/run.sh`), declaration order (`protocol_processor_top.sv`) and
citations; this lane's registry index. Neither side's code touches a file the other changed:
`main` changed neither `hdl/aecp/KL_aecp_notify.sv` nor `tb/aecp_notify/` nor
`notify_mutants.py`, and this lane changed none of `main`'s HDL.

Line citations re-derived: the files both sides changed are `06`, `09` and
`tb/pp_top/README.md`. The tree's only line citations into them are
`tb/nvm_port/README.md:1067` and `:1352` (`09_verification.md:56`), which still name the NVM
row of F09.3. No line added on either side cites a line of a file the other side changed
(`git diff f4167536 5c71928a` and `git diff f4167536 3ab2e4da`, searched for
`<file>:<line>`), and the tree holds no line citation into `KL_aecp_notify.sv`.

ROMs regenerated (`hdl/aecp/ucode/gen_ucode.py`, `hdl/acmp/rom/gen_ltn_rom.py`, rc 0 each),
at the head and at `main`: `ucode.hex` sha256 `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8`
(2,048 words) and `ltn_rom.hex` `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956`
(129 lines), equal at both, and equal to the parent export's `roms/` for the route. The
repository tracks no ROM image; every bench and the export generate them.

### R1b.2 #22 in passing (item 3)

| File:line at `6e950fea` | Change |
|---|---|
| `hdl/aecp/KL_aecp_notify.sv:604-606` | `pd_any_w`, `pd_ix_w` declared above `ca_request` (`:608`), whose cancel term (`:616-619`, first use `:617`) reads them; one comment line names their driver |
| `hdl/aecp/KL_aecp_notify.sv:725-726` | the two declarations removed above `pend_pick`, which still drives them |

| Proof | Command | Result |
|---|---|---|
| red, at the merge `823fc20c` | `xvlog -sv hdl/common/pp_pkg.sv hdl/aecp/KL_aecp_notify.sv` (Vivado 2026.1, under the lock) | rc 1: `ERROR: [VRFC 10-3380] identifier 'pd_ix_w' is used before its declaration [.../hdl/aecp/KL_aecp_notify.sv:613]`, `ERROR: [VRFC 10-8530] module 'KL_aecp_notify' is ignored due to previous errors` |
| green, at `6e950fea` | the same | rc 0, no ERROR or WARNING line: `analyzing module KL_aecp_notify` |
| no next finding | the parent's `xvlog_gate.py`, one module per invocation, every processor file | `KL_aecp_notify.sv` absent from its findings (xvlog stops at a module's first error, so a second one would have surfaced here) |
| no logic change | lockstep bench, R1b.3 | 0 mismatches |

#22 stays open for `KL_pp_originator.sv:194` (`cancel_hit_w`) and `KL_pp_rx_validator.sv:383`
(`vd_push_w`), which this lane does not touch.

Route evidence too (R1b.6): `Synth 8-6901` for `pd_ix_w` in `KL_aecp_notify.sv`, 3 at `main`
and at round 1's base and head, is 0 in the head route.

Section 2's citations at `6e950fea` (round 1's at `3ab2e4da`; the rest are unchanged):
`KL_aecp_notify.sv:1044-1045`, `:1053-1054`, `:1362` are now `:1046-1047`, `:1055-1056`,
`:1364`; `tb/pp_top/README.md:2086-2089`, `:2133-2136` are now `:2289-2294`, `:2338-2341`;
`06_aecp_engine.md:864-866`, `:887-904` are now `:874-876`, `:897-914`;
`09_verification.md:280`, `:291` are now `:285`, `:296`.

### R1b.3 Behaviour: lockstep bench of `main` against the head (item 2)

Scratch `$VALIDATION_STORAGE/pp232-a520/r1b/lockstep` (not committed): round 1's bench, generator
and harness unchanged; the reference is `main` `5c71928a`'s `KL_aecp_notify.sv` (byte-equal
to `f4167536`'s, renamed `KL_aecp_notify_ref`, byte-equal to round 1's reference); the
candidate is `6e950fea`'s file. Every output and the internal `rx_cmd_hit_w` compared at both
clock phases of every cycle; resets mid-run.

| Shape N_CTRL/N_IN/N_OUT | Runs (seeds 1-4 protocol-shaped, 5-8 fully random) x 1,000,000 cycles | Mismatches |
|---|---:|---:|
| 16/2/2 | 8 | 0 |
| 16/9/9 | 8 | 0 |
| 2/1/1 | 8 | 0 |
| 16/2/2, `EN_IDENTIFY_NOTIF_P=1` | 8 | 0 |
| 5/8/8 | 8 | 0 |
| total | 40 | **0** (423,284 commands during a rewrite window, 46,701 hits in one) |

Controls: round 1's seven planted copies, each re-planted on the `6e950fea` file by its own
diff (1 to 3 lines each), built at 16/2/2, 8 runs of 1,000,000 cycles:

| Control | Mismatches | Runs caught |
|---|---:|---:|
| no rewrite comparator (`no_override`) | 118,069 | 8 of 8 |
| no clear (`no_clear`) | 14,840,381 | 8 of 8 |
| no set (`no_set`) | 10,944,924 | 8 of 8 |
| comparator only in the set cycle (`override_set_only`) | 14,848,035 | 8 of 8 |
| last chunk ignored (`last_chunk_ignored`) | 545,407 | 4 of 8 |
| REGISTER not re-indexed (`refresh_not_reindexed_claim_too`) | 10,945,711 | 8 of 8 |
| a stamp read without its valid bit (`stamp_unread_valid`) | 161,278 | 7 of 8 |

### R1b.4 Processor suites and gate (item 2)

| Command | `main` `5c71928a` | Head `6e950fea` |
|---|---|---|
| `./scripts/lint_hdl.sh` | | rc 0, 41 of 41 (14 s) |
| `./scripts/run_suites.sh` | rc 0, 33 suites, 1,021,449 checks, 0 failing (1,018 s) | rc 0, 33 suites, 1,021,455 checks, 0 failing (1,168 s); per suite identical but `aecp_notify` 14 -> 20 (section IX); `pp_top` 10,416 both |
| `make check` | | rc 0: 41 mermaid + 18 wavedrom blocks, 1,114 links, 115 REQ rows, 94 matrix rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | | rc 0, 94 rows, 0 untested |
| `./syn/yosys/run.sh` (C10's census) | | rc 0 (83 s): `YOSYS 42 tops, all.v parsed 1 time(s)`, each `YOSYS OK` (`KL_aecp_notify` among them); `YOSYS XILINX OK KL_aecp_engine` |

### R1b.5 Campaigns (item 2)

Every `tb/pp_top` campaign driver, at `6e950fea`, each rc 0, `--jobs 4` where the driver has
it. "At its README count": each arm's verdict and failing-check count equals the count in the
merged `tb/pp_top/README.md` (P1's re-runs included), compared by script from the drivers'
`results.json` or record lines.

| Campaign | rc, seconds | Result |
|---|---|---|
| `notify_mutants.py --jobs 4` | 0, 400 | 44 of 44 KILLED, six goldens PASS; 44 of 44 at their README counts (`ident_burst_from_t0` 21, P1's) |
| `ctr_mutants.py --jobs 4` | 0, 129 | control PASS, 17 of 17 KILLED; 17 of 17 at their README counts |
| `d3_mutants.py --jobs 4` | 0, 3,165 | 110 of 110 KILLED, six goldens PASS (`--d3-only`, `--adp-only`, `--volatile-only`, `--cuts-only`, `tb/acmp_nvm`, `tb/rx_validator`); the 98 `tb/pp_top` arms at their README counts; the 12 in `tb/acmp_nvm` and `tb/rx_validator` (recorded there under other names) identical to round 1's head run |
| `aecp_mutants.py --jobs 4` | 0, 425 | 5 controls PASS, 55 KILLED (60 checks PASS); 55 of 55 at their README counts |
| `aecp_dispatch_mutants.py --jobs 4` | 0, 388 | 4 controls PASS, 40 KILLED (44 checks PASS); 40 of 40 at their README counts |
| `acmp_mutants.py --jobs 4` | 0, 150 | 19 of 19 KILLED, three goldens PASS; 22 of 22 records identical to round 1 (18 also at their README counts) |
| `gsi_mutants.py --jobs 4` | 0, 452 | 20 detected by named checks; golden and restored PASS |
| `name_wr_mutant.py` | 0, 58 | decode killed; golden and restored PASS |

### R1b.6 Vivado: the integrated route at the merge (item 2)

#638's recipe and gate at milan-fpga `79e53831` (the tools of round 1, unchanged). Vivado
2026.1 build 6511674, `xc7a100t-fgg484-2`, 50 MHz (20 ns), AreaOptimized_high / ExploreArea /
ExtraPostPlacementOpt / AggressiveExplore, 32 threads, default seed. Each run alone (no other
build of this lane beside it) under `flock /tmp/milan-vivado.lock`, which another lane's runs
also took in between. Scratch parent as in R1b.7 (dev `5fabb46e` + c8 + p2-p1 + c10; the
lane's budget patch touches no Vivado input).

- **Head** (as assigned): processor `6e950fea`.
- **Base, added**: processor `main` `5c71928a` on the same parent. The head's route moved
  +581 LUT against round 1's head route, past the #638 gate's 500-LUT tolerance, so "moves
  materially" needed the merge's own base to separate `main`'s growth from the lane's effect.
- The two exports differ only in the generated date, a tree listing's order and the output
  path (Tcl, XDC, init files, ROMs and builder outputs equal). Each route's six memory images
  (`baseline_images.json`) hash equal between the two and to round 1's. The head route's link
  step found `sw/builder/out` a real directory left by gate 10's builder test, so it read
  `gptp_ucode.hex` from there: sha256 `78c8418a...` as in the export's builder output, and
  `diff -rq` of the whole shape directory against the export's is empty. Before `main`'s
  export that directory and the two gate-generated ROM files (all gitignored) were moved aside
  to `$VALIDATION_STORAGE/pp232-a520/r1b/parent-aside/`.

**Integrated shipping route, `endstation_ax7101_1x1_tdm8`, whole image**

| | LUT (logic + memory) | FF | Slice (of 15,850) | RAMB36 / RAMB18 | DSP | CARRY4 | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| `main` `5c71928a` | 51,434 (49,158 + 2,276) | 59,691 | 15,847 (99.98 %) | 79 / 27 | 14 | 3,526 | +0.079 / +0.014 |
| head `6e950fea` | 50,671 (47,533 + 3,138) | 57,660 | 15,841 (99.94 %) | 79 / 27 | 14 | 3,376 | +0.274 / +0.023 |
| **head - `main`** | **-763** (-1,625 + 862) | **-2,031** | **-6** | 0 / 0 | 0 | -150 | +0.195 / +0.009 |
| round 1: head - base (section 4) | -650 (-1,517 + 867) | -1,950 | -15 | 0 / 0 | 0 | -147 | +0.027 / +0.015 |

SLICEL / SLICEM: `main` 11,099 / 4,748, head 11,093 / 4,748. Route status: every routable
net fully routed (`main` 107,053, head 104,326), 0 with routing errors. Signoff corners: setup
worst at Slow 0/85 C (`main` +0.079, head +0.274), hold worst at Fast 0/85 C (+0.014, +0.023).
`main`'s route took 94.7 minutes against the head's 28.0.

| Scope (routed hierarchy) | LUT `main` / head | of which LUTRAM | FF `main` / head |
|---|---:|---:|---:|
| `milan_datapath/pp_shadow` | 24,485 / 23,862 | 1,152 / 2,016 | 24,267 / 22,254 |
| `pp_shadow/u_pp` | 23,910 / 23,286 | | 23,437 / 21,424 |
| `pp_shadow/u_pp/u_notify` | 3,270 / 2,343 | 96 / 960 | 3,299 / 1,287 |
| `pp_shadow/u_pp/u_aecp/u_resp` | 345 / 345 | 0 / 0 | 260 / 260 |

Census (`baseline_cells.tsv`): `u_notify` `rows_r_reg` FD cells 2,048 at `main`, 0 at head;
`ctr_last_r_reg` 192 at both.

Worst setup paths. `main`: `u_pp/u_rx_validator/hdr_ctlr_eid_r_reg[5]` ->
`u_pp/u_tx_arbiter/FSM_onehot_arb_st_r_reg[0]/CE`, 39 levels, data path 19.696 ns (round 1
base's chain, through `rx_cmd_hit_w` and the comparator bank). Head: `u_pp/u_aecp/u_ucpu/uop_e_r_reg[imm][3]`
-> `u_pp/u_aecp/u_d3/deb_cnt_r_reg[1]/R`, 33 levels (CARRY4 13), 19.202 ns, in P1's D3 writer;
`u_notify`'s internal worst slack is +6.058 ns at head (+4.767 at `main`; round 1 head +6.141).

Head route log, "Distributed RAM: Final Mapping Report" (line 3916): `|u_notify | rows_r_reg |
User Attribute | 16 x 128 | RAM32M x 64 |`; 288 rows `|u_notify | g_ix_row[i].g_ix_chunk[j].mem_r_reg
| User Attribute | 64 x 1 | RAM64M x 1 |` and 16 `... g_ix_chunk[18].mem_r_reg | ... | 16 x 1 |
RAM16X1D x 1 |` (each printed in both mapping reports: 576 + 32 lines); `cmdq_*` 24 RAM32M
(`cmdq_excl_r_reg | Implied | 16 x 64 | RAM32M x 11`, class 1, type, index, arg0, arg1 3
each). Diagnostics: `Synth 8-7186` 16 at `main` (`rows_r[i]`), 0 at head; `Synth 8-4445` 0
at both (beyond the echoed `set_msg_config`); `Synth 8-6901` in `KL_aecp_notify` (`pd_ix_w`,
#22) 3 at `main` and at round 1's base and head, **0 at head** (5 in other files: originator 2,
rx_validator 2, `milan_datapath` 1; 8 at `main`).

#638's gate, `pp_resource_gate.py check --endpoint route-1x1`:

| Candidate | Against | rc | Verdict |
|---|---|---:|---|
| head | #638's recorded A | 1 | LUT 50,671 vs 50,128: +543, "grew by more than 500"; FF -1,346, re-baseline recommended. Sub-blocks: `u_notify` -792 LUT / -2,012 FF, `u_aecp/u_d3` +639 / +96 |
| `main` | #638's recorded A | 1 | LUT +1,306 and FF +685 over A; `u_aecp/u_d3` +605 / +96, `u_notify` +135 / 0 |
| head | `main`, recorded into a scratch copy (`record --write`) | 0 | PASS: LUT -763, FF -2,031, slices -6, WNS +0.195; re-baseline recommended (LUT, FF). Sub-blocks: `u_notify` -927 / -2,012; nothing else beyond +112 LUT (`u_aecp`) |
| head | round 1's head route, recorded the same way | 1 | LUT +581 ("grew by more than 500"), FF -21, slices +17: `u_aecp/u_d3` +619 / +96 (P1), `u_notify` +16 / +11 |

**Judgement (item 2's "unless the route moves materially").** The image moved against round
1 by +581 LUT, all of it P1's D3 writer (`u_d3`), which also puts `main` over #638's A by
+1,306 LUT and +685 FF. The lane's effect did not move: at the merge it saves 763 LUT and
2,031 FF in the route (round 1: 650 and 1,950), `u_notify` 927 LUT and 2,012 FF (844 and
2,023), and the worst setup slack improves by 0.195 ns. So the standalone figures of section 4
stand. The head fails #638's A only by `main`'s growth, which the lane reduces from +1,306 to
+543 LUT; recording a new A is the merge bank's step (#638 ruling (d)).

### R1b.7 Parent consumer set

Scratch parent `$VALIDATION_STORAGE/pp232-a520/parent` (never committed or pushed), moved from
`bbf704ec` to dev `5fabb46e767c9308ab2580916237f43577698c6e` (`bbf704ec..5fabb46e`: two
findings documents only; the four submodule pins unchanged): round 1's patches reversed with
`git apply -R --check` then `git apply -R`, the gitlink unstaged, `git checkout --detach
5fabb46e`; the processor submodule (`rev-parse --show-toplevel` checked first) fetched from
the lane and detached at `6e950fea`; the gitlink set in the index only (`git update-index
--cacheinfo`). Patches, each `git apply --check` clean at `5fabb46e`, then applied:

| Patch | sha256 | Applies at `5fabb46e` |
|---|---|---|
| `parent-adoption-c8-bbf704ec.patch` | `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c` | yes |
| `parent-adoption-p2-p1-1269cdaf.patch` | `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84` | yes |
| `parent-adoption-c10-1269cdaf.patch` | `55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9` | yes |
| `parent-adoption-pp232-xvlog-c10-5fabb46e.patch` (this lane, after c10) | `88ee5e9643a453f8c31dc76e5f8d57e8deec89bcbbf9d4a4a8ca005757b72560` | yes, after c10 |

GNU Make 4.3 and the pinned Verilator 5.050 first on PATH.

| # | Command | rc | Result (three patches unless noted) |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files, 4 of 4 consumer lists; processor 42/42 tops, 0 recorded (C10) |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports (1,759 at `main` `5c71928a` too), undocumented 111 <= 111 |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | within ratchets |
| 8 | `scripts/docs_check.py` | 0 | 0 findings, 186 md + 970 files |
| 9 | `scripts/xvlog_gate.py --check` | **1** | three patches: `BANK IT [submodules]: protocol-processor:hdl/aecp/KL_aecp_notify.sv\|VRFC 10-3380\|pd_ix_w no longer occurs`; 2 findings (originator, rx_validator) (395 s) |
| 9b | `scripts/xvlog_gate.py` (its default run, which banks) | 0 | `wrote scripts/xvlog.budget: 2 grandfathered finding(s)`; the diff is the lane's patch above (264 s) |
| 9c | `scripts/xvlog_gate.py --check`, four patches | 0 | `PASS (2 finding(s) == ratchet; 0 hdl/, 2 pinned processors)`, pinned at `protocol-processor@6e950fea` (512 s) |
| 10 | `sw/builder/test_builder.py` | 0 | Make 4.3: "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 11's mf48 tree; gate 1b's `MAKEFLAGS += -e` arm, which Make 4.3 cannot exercise) (1,151 s). Make 4.4.1: "ALL GATES PASS EXCEPT 1 NOT RUN", gate 11 only (1,155 s). As round 1 |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | legs 606, 606, 646 and 311 checks, 0 failures (308 s) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS, 0 FAIL; 4 render mutants caught; gmstep 6 of 6 (2,583 s) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | **2** | two-stream leg 65 checks, 0 failures; shipping leg 155 checks, **2 failures**: `T30 INTERNAL LAW: the fill at accept is the 8-event setpoint for every PDU got=227 exp=292` and `... every PDU's first event is inside the law band got=285 exp=292`; first-event delay 18,396..18,821 cycles = 8.830..9.034 ticks (214 s). Recorded against milan-fpga #643: these are #643's figures for P1's processor. With the processor at `main` `5c71928a`: rc 2, and all 48 result lines identical to the head's (189 s), so the lane does not move the boot timing |
| 16b | `python3 tdm8_render_mutants.py --leg-defects` (gate 16's last step, not reached after the failure) | 0 | 5 of 5: two positive controls and three leg defects caught (406 s) |

Light gates 1 to 8, 3b and 11 re-run with the fourth patch applied: all rc 0, same summaries.

### R1b.8 Parent-visible list (round 1b)

- No port, parameter, register or behaviour change; the port gate counts 1,759 processor
  ports at `main` and at the head.
- One parent adoption line: `scripts/xvlog.budget` banks the vanished `pd_ix_w` finding (3 to
  2). Without it gate 9 exits 1, as the gate is built to ("bank the improvement
  deliberately"). `parent-adoption-pp232-xvlog-c10-5fabb46e.patch` in this directory, made by
  the gate's own default run, applies after the c10 patch.
- Gate 16's two T30 INTERNAL law checks fail at `main` and at the head identically:
  milan-fpga #643, not this lane.
- The routed image's worst setup path is now in P1's D3 writer (`u_ucpu` -> `u_d3`, +0.274 ns);
  at `main` it is the `rx_cmd_hit_w` chain into `u_tx_arbiter` (+0.079 ns).
- #638's gate: head against A fails on LUT (+543) by `main`'s growth (`main` alone: +1,306 LUT,
  +685 FF); head against `main` passes with "re-baseline recommended". Recording a new A is the
  merge bank's step.

### R1b.9 Run receipts

Vivado runs (scratch `$VALIDATION_STORAGE/pp232-a520/meas/r1b-main/` and `r1b-head/`; reports,
checkpoints and logs stay there):

| Combination | Run | rc | Minutes | Log | Log SHA-256, first 16 | Log bytes |
|---|---|---:|---:|---|---|---:|
| processor `main` `5c71928a` | Integrated route, 1x1 | 0 | 94.7 | `baseline.log` | `3345c0ac81f8f149` | 687,698 |
| processor `6e950fea` | Integrated route, 1x1 | 0 | 28.0 | `baseline.log` | `4d18c2905ff3e812` | 806,747 |

xvlog runs, under the same lock: the file alone at the merge (rc 1) and at the head (rc 0),
seconds each; the parent's `xvlog_gate.py` three times (395, 264 and 512 s).

Other runs (rc, seconds), each with its own log and rc file, never piped: lint 0/14, head sweep
0/1,168, `main` sweep 0/1,018, `make check` 0, `gen_matrix` 0, Yosys gate 0/83; campaigns notify
0/400, ctr 0/129, acmp 0/150, aecp 0/425, dispatch 0/388, gsi 0/452, name_wr 0/58, D3 0/3,165;
lockstep 40 runs and 56 control runs, each 0 (match) or 1 (mismatch, controls only); parent
gates as in R1b.7. Concurrency: the suites, the Yosys gate, the lockstep bench and the campaigns
(two chains) ran together, peak 11.7 GB of the 12 GB cap, page-cache reclaim only (0 OOM
events, 0 swap); the parent's heavy gates overlapped the D3 campaign's simulation phase.

Scratch evidence outside the tree: `$VALIDATION_STORAGE/pp232-a520/r1b/` (`tree-head/`,
`tree-main/`: the `git archive` trees; `logs/`, `logs-main/`: suites, lint, Yosys, route
wrappers, gate logs, `mem.log`; `camp/`: campaign outputs and the README comparisons;
`lockstep/`: bench, reference, candidate, controls, runs; `roms/`; `xvlog-merge/`,
`xvlog-fix/`; `pgates/`, `pgates-4patches/`, `pgates-xvlog/`, `pgates-make441/`,
`pgates-main/`: parent gate logs; `tools/`: the record comparison scripts;
`baseline-r1head.json`, `baseline-r1bmain.json`: scratch gate baselines; `parent-aside/`).

## Round 2

Assignment: milan-fpga #232 comment 5976892215 (round 2 for processor PR #153), after
R452-1 (PR #153 comment 5976816563) and R453-1 (5976889224). Both were NEGATIVE on MINOR
findings and found the RTL change clean. Status: **REVIEW READY** at `2ea3dee`: every
item done, every gate at its count, no STOP condition. Posted as milan-fpga #232 comment
5978213864.

- Head: `2ea3dee2cd92e5907a8942a8c32436ab2f46ff2d`, not pushed. Three commits on top of
  `6e950fea`, one-line subjects, no body, no trailer, no rebase or amend:
  - `f3abfc6` coverage: `tb/aecp_notify` IX5, IX5b, IX6a, IX6, IX6b and section TS; three
    controls in `notify_mutants.py`; the two READMEs and 09
  - `0d9e5e7` residue: the index comment (RTL), 06's identity-index row
  - `2ea3dee` the `--no-ff` merge of processor `main` `83999eba1ef4756e9e769e4fba164f5095761604`
    (PR #152, processor #85); parents `0d9e5e7`, `83999eba`
- Every measurement below is at `2ea3dee` from a `git archive` (scratch
  `$VALIDATION_STORAGE/pp232-a520/r2/tree-head`), with the pinned Verilator 5.050, unless a row
  says otherwise.

### R2.1 Committed coverage for the three dependencies (item 1; R452-1 F1, R453-1 F2)

Directed arms in `tb/aecp_notify` (the assignment's second option), and the reviewers' three
faults as killed controls in `notify_mutants.py`.

| File:line at `2ea3dee` | Change |
|---|---|
| `tb/aecp_notify/sim_main.cpp:23-24`, `:32` | `KIND_CTRS` (pp_pkg `PP_UNS_CTRS_C`), `DT_AVB_INTERFACE`, `COUNTER_JOB_CYCLES` |
| `tb/aecp_notify/sim_main.cpp:41-42`, `:51-55` | C's identity moved to the harness (IX4 and IX5 share it); the new members |
| `tb/aecp_notify/sim_main.cpp:132-137` | `warm_reset()` |
| `tb/aecp_notify/sim_main.cpp:227-228` | `run()` calls `rewrite_window()` and `counter_stamps()` after section IX |
| `tb/aecp_notify/sim_main.cpp:266-269` | IX4's comment: the rewrite spans the row write's own cycle and the cycle after it |
| `tb/aecp_notify/sim_main.cpp:307-326` | `register_to_write()`: a REGISTER up to the cycle in which `rgy_wait_o` falls, the cycle the row write lands in (`wr_en_r`, `ix_clr_r` high); returns there with the clock low |
| `tb/aecp_notify/sim_main.cpp:328-343` | `after_failure()`: one clock with a failed probe for a row, and optionally a command; returns the live row count after the drain's time |
| `tb/aecp_notify/sim_main.cpp:345-380` | IX5, IX5b, IX6a, IX6, IX6b (`rewrite_window()`) |
| `tb/aecp_notify/sim_main.cpp:382-411` | TS1, TS2, TS3 (`counter_job()`, `counter_stamps()`) |
| `tb/pp_top/notify_mutants.py:13-20`, `:264-265`, `:284-294` | docstring; `override_set_only` (IX6), `own_compare_new_row` (IX5), `stamp_read_without_valid` (TS3), each the reviewer's own edit |
| `tb/aecp_notify/README.md:11-12`, `:20`, `:80-101`, `:103-118`, `:120-132` | lead; build table (10 + 11 + 5); IX5 to IX6b; section TS; the mutation record, seven controls |
| `tb/pp_top/README.md:2293-2296`, `:2341-2346` | the notify record: 47 of 47; two `ix_*` counts that moved; the three new rows |
| `docs/architecture/09_verification.md:287`, `:298-299` | three of the notification block's sections; the IX row; a TS row |

| Check | What it drives | Control (killed) |
|---|---|---|
| IX5 | D registers into row 1, which still holds C (IX4b removed C). In the row write's own cycle (T+1), C's command and a failed probe for row 1 arrive together: C still matches row 1 (`rows_r` holds C until that cycle's edge), so the row stays (2 live) | `own_compare_new_row`: IX5 (the compare reads `wr_row_r` = D) |
| IX5b | the same failure alone removes row 1 | (vacuity guard, as IX4b) |
| IX6a | warm reset; E registers into row 0, and a reset lands in its row write's own cycle: the row write and the clear land, the set does not; registry empty | (premise) |
| IX6 | E registers again into row 0. In its row write's own cycle, E's command and a failed probe for row 0 arrive together: only the comparator matches (the index holds nothing for row 0), so the row stays | `override_set_only`: IX6, IX6b (the T+1 hit reads the empty index) |
| IX6b | after the rewrite, E's command and a failed probe again: the re-indexed row matches through the index | `ix_new_identity_unset`, `ix_rewrite_unmatched` (also) |
| TS1 | warm reset, a controller registered, a change on AVB_INTERFACE[0]: a GET_COUNTERS job within 16 clocks | (premise) |
| TS2 | a second change in the same ms: no job within 16 clocks (the stamp is live) | (premise of TS3's meaning) |
| TS3 | warm reset (the stamp kept, `ctr_sent_r` cleared), a controller registered, a change in that same ms: a job within 16 clocks | `stamp_read_without_valid`: TS3 (the stale stamp holds it) |

| Proof | Command | Result |
|---|---|---|
| the bench at the head | `make` in `tb/aecp_notify` | rc 0, `30 checks: 30 PASS, 0 FAIL` (default build 26, identify build 4) |
| the bench on `main`'s RTL | scratch copy: `83999eba`'s `hdl/` (its `KL_aecp_notify.sv` sha256 `e7e127cf...f3f2`, byte-equal to `5c71928a`'s and `f4167536`'s) + the head's `tb/aecp_notify` | rc 0, 30 of 30: the new checks describe behaviour that did not change |
| the seven index and stamp controls | `notify_mutants.py --jobs 7 --only` the four `ix_*` and the three new | rc 0, 7 of 7 KILLED, golden PASS; failing checks: `ix_old_identity_kept` IX1; `ix_new_identity_unset` IX3, IX4, IX6b; `ix_last_chunk_ignored` IX2; `ix_rewrite_unmatched` IX4, IX6, IX6b; `override_set_only` IX6, IX6b; `own_compare_new_row` IX5; `stamp_read_without_valid` TS3 |
| the whole campaign | `notify_mutants.py --jobs 4` (R2.6) | rc 0, 47 of 47 KILLED, six goldens PASS, 47 of 47 at their README counts |

Reviewer probes, run unchanged at `2ea3dee` (scripts from the parent's `pp232-review-evidence`
branch, `4e438b23`): R452-1's `plant.py` and R453-1's `make_controls.py` both plant every
control on the head file (every snippet found exactly once: 10 and 12 controls; 7 of
R453-1's are byte-equal to R452-1's, `own_vs_new_row` equal to `own_compare_new_row`).
R452-1's `clear_cycle_probe.sh` (the lane repository, commit `2ea3dee`) and R453-1's
`probe_committed.sh` (the `git archive` tree; suites `aecp_notify pp_top`) then ran each
control, three at a time (each script exits 0 when it has run its suites; the verdict is
in the suites' output). A failing `tb/aecp_notify` stops at its first build, so the
reviewer scripts print "rc=2 no tally" for it; the FAIL lines below are read from each
run's log. Published in `evidence-r2/probes/` (logs, the planted diffs, raw-log sha256).

| Reviewer | Control | script rc, s | `tb/aecp_notify` | `tb/pp_top` |
|---|---|---|---|---|
| R452-1 | `clear_new_identity` | 0, 899 | FAIL (1: IX1) | PASS 10416/10416 |
| R452-1 | `last_chunk_ignored` | 0, 858 | FAIL (1: IX2) | PASS 10416/10416 |
| R452-1 | `no_clear` | 0, 907 | FAIL (1: IX1) | PASS 10416/10416 |
| R452-1 | `no_override` | 0, 881 | FAIL (3: IX4, IX6, IX6b) | PASS 10416/10416 |
| R452-1 | `no_set` | 0, 860 | FAIL (3: IX3, IX4, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R452-1 | `override_clr_only` | 0, 850 | FAIL (1: IX4) | PASS 10416/10416 |
| R452-1 | `override_set_only` | 0, 746 | FAIL (2: IX6, IX6b) | PASS 10416/10416 |
| R452-1 | `own_compare_new_row` | 0, 731 | FAIL (1: IX5) | PASS 10416/10416 |
| R452-1 | `register_not_reindexed` | 0, 751 | FAIL (5: IX3, IX4, IX5, IX6, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R452-1 | `stamp_without_valid` | 0, 672 | FAIL (1: TS3) | PASS 10416/10416 |
| R453-1 | `first_chunk_ignored` | 0, 662 | FAIL (1: IX2) | PASS 10416/10416 |
| R453-1 | `index_wrong_row` | 0, 668 | FAIL (2: IX3, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R453-1 | `key_swapped` | 0, 616 | FAIL (2: IX3, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R453-1 | `last_chunk_ignored` | 0, 611 | FAIL (1: IX2) | PASS 10416/10416 |
| R453-1 | `no_clear` | 0, 642 | FAIL (1: IX1) | PASS 10416/10416 |
| R453-1 | `no_override` | 0, 642 | FAIL (3: IX4, IX6, IX6b) | PASS 10416/10416 |
| R453-1 | `no_set` | 0, 650 | FAIL (3: IX3, IX4, IX6b) | FAIL (384: U10a4, U10a5, U10a5.1, U10a5.10, U10a5.2, U10a5.11, ...) |
| R453-1 | `override_clr_only` | 0, 626 | FAIL (1: IX4) | PASS 10416/10416 |
| R453-1 | `override_set_only` | 0, 622 | FAIL (2: IX6, IX6b) | PASS 10416/10416 |
| R453-1 | `own_vs_new_row` | 0, 607 | FAIL (1: IX5) | PASS 10416/10416 |
| R453-1 | `reindex_late` | 0, 619 | FAIL (1: IX4) | PASS 10416/10416 |
| R453-1 | `stamp_read_without_valid` | 0, 612 | FAIL (1: TS3) | PASS 10416/10416 |

22 of 22 controls fail a committed check

Every one fails `tb/aecp_notify`; `tb/pp_top` alone catches only the four that break
every match after a REGISTER.

### R2.2 Vivado evidence (item 2; R453-1 F1)

`evidence-r2/vivado/` in this directory (1.6 MB, no file over 190 KB): for each of the
eight runs (round 1's base and head routes and four standalone syntheses, round 1b's `main`
and head routes), #638's utilization, hierarchy, scope and image reports whole; the LiteX
flow's route status, placement utilization and signoff corner files whole; a timing extract
(design summaries of #638's timing report, the flow's and the four corners'; the intra-clock
table; the worst setup and hold paths); a log extract (both final mapping reports, every
`Synth 8-7186` / `8-4445` / `8-6901` line with counts, completion lines); a cell census;
`figures.json`; and `sources.tsv` with every raw file's full sha256 and bytes.
`evidence-r2/vivado/README.md` maps each quoted figure to its file and line;
`tools/rederive.py` re-derives them from the packet alone (`rederive.txt`, rc 0): route
-763 LUT / -2,031 FF, `u_notify` -927 / -2,012, WNS +0.274, 88 RAM32M + 288 RAM64X1D + 16
RAM32X1D, zero `Synth 8-7186` at every head (16 at every base and `main`).

The round-2 head adds no HDL logic: `git diff 6e950fea 2ea3dee -- hdl/` touches
`KL_aecp_notify.sv` (the comment) and `KL_adp_engine.sv` (`main`'s comments), and each file
is equal to its `6e950fea` form with comments stripped (checked by script). So round 1b's
head route is this head's.

The lockstep bench is published too (`evidence-r2/lockstep/`), with the corrected control
table (R453-1 F2's last bullet): round 1b's "comparator only in the set cycle" was planted as
`ix_busy_w = ix_set_r`, which also drops the clear (a superset of `no_clear`, hence its
count). The reviewers' true edits on the same bench: `override_set_only` 8 mismatches, 4 of 8
runs (random-input seeds only); `own_compare_new_row` 4,611, 8 of 8.

### R2.3 Parent adoption patch (item 3)

`parent-adoption-232-241f9184.patch` (this directory; sha256
`88ee5e9643a453f8c31dc76e5f8d57e8deec89bcbbf9d4a4a8ca005757b72560`, 587 bytes) lowers
`scripts/xvlog.budget` by the `pd_ix_w` line (3 to 2 findings in the submodule section),
made by `scripts/xvlog_gate.py`'s own default run. It is byte-equal to round 1b's
`parent-adoption-pp232-xvlog-c10-5fabb46e.patch`, because `5fabb46e..241f9184` changes neither
the budget nor the gate. Run at dev `241f9184` + c8 + p2-p1 + c10 with the processor at
`2ea3dee`, Vivado 2026.1's xvlog, under the shared Vivado lock (`flock
/tmp/milan-vivado.lock`, taken 10:29:32, freed 10:37:35; no other build of this lane
running):

| Step | Command | rc, seconds | Result |
|---|---|---|---|
| red | `xvlog_gate.py --check` (three patches) | 1, 174 | `BANK IT [submodules]: protocol-processor:hdl/aecp/KL_aecp_notify.sv\|VRFC 10-3380\|pd_ix_w no longer occurs - run scripts/xvlog_gate.py to lower the ratchet`; 2 findings left (originator `cancel_hit_w`, rx_validator `vd_push_w`); pinned at `protocol-processor@2ea3dee2` |
| bank | `xvlog_gate.py` (its default run) | 0, 157 | `wrote scripts/xvlog.budget: 2 grandfathered finding(s)`; the patch is the budget's diff over the c10 state |
| apply | `git apply -R --check` and `-R` (back to the c10 state, `cmp` equal), then `git apply --check` and `git apply` | 0 | applies after c10 |
| green | `xvlog_gate.py --check` (four patches) | 0, 152 | `xvlog gate: PASS (2 finding(s) == ratchet; 0 hdl/, 2 pinned processors)`, pinned at `protocol-processor@2ea3dee2` |

With the fourth patch applied, gates 1 to 8, 3b and 11 re-ran: all rc 0, the same
summaries (R2.7). Gates 10 and 12 to 16 ran before the fourth patch. They read nothing
it changes: `scripts/xvlog.budget` is read only by `xvlog_gate.py`, and named by
`check_port_contracts.py` and `measure_naming.py`, which re-ran.

### R2.4 The merge (item 4)

`git merge --no-ff 83999eba`: no conflict. `git merge-base` is `5c71928a`. Files only
`main` changed are byte-equal to `83999eba` in the merge, files only the lane changed are
byte-equal to `0d9e5e7`, and `docs/architecture/09_verification.md`, the one file both
changed, carries both hunks (main's F04.7/F04.8 sentence at `:143-145`; the lane's rows at
`:287`, `:298-299`). Touched gates re-run at the merge: the suite sweep (`adp_engine` 1,328
-> 1,348, `main`'s own count: `tb/adp_engine` at `83999eba` alone is 1,348), and the ADP
campaign (R2.6).

### R2.5 Residue (item 5)

| Finding | Fix | Where |
|---|---|---|
| R453-1 R1 | "re-indexes its row over two cycles: the cycle in which the row write lands (`wr_en_r` high) clears the old identity's bits, and the cycle after it sets the new identity's" | `hdl/aecp/KL_aecp_notify.sv:559-562` (comment only); PR body item 1 |
| R453-1 R1 | "over the row write's own cycle and the cycle after it" | `docs/architecture/06_aecp_engine.md:904` |
| R452-1 F2 | the index row's head cell: "synthesis mapping report:" before the quotes; "; implemented cells after optimization: 288 RAM64X1D (576 LUTs) and 16 RAM32X1D (32 LUTs), which with `rows_r`'s 64 and `cmdq_*`'s 24 RAM32M make `u_notify`'s 960 LUTRAM" after | PR body inventory; HANDOFF section 5 |
| R452-1 S1 (suggestion, taken) | "The index's correctness relies on its configuration-time zero content (an explicit `initial`), as the ROM images rely on `$readmemh`; `rst_n` leaves both the index and `rows_r` as they are" | `docs/architecture/06_aecp_engine.md:904` |
| R453-1 F2, last bullet | the lockstep control table corrected and published | R2.2 |

Line citations moved by the comment's extra line (PR body updated): index `:551-603`,
`g_ix_row` `:582-594`, `mem_r` `:585`, `pd_*_w` `:605-607`, `ca_request` `:609`, first use
`:618`, `pend_pick` `:727`, `ix_clr_r`/`ix_set_r` `:1047-1048`, `:1056-1057`, the window
check `:1097-1099`, the stamp write `:1297-1299`, `N_APPLY`'s `ix_clr_r` `:1365`.

### R2.6 Processor gates at `2ea3dee`

All from the `git archive` tree, each with its own log and rc file, never piped; campaigns
with `--jobs 4` (the ADP campaign `JOBS=4`). "At its README count": each arm's verdict and
failing-check count equal the count the merged README records, compared by script
(`cmp_records.py`; rows the script cannot parse read by hand, named below). "Identical to
round 1b": every record equal to round 1b's head run, verdict and failing-check count.

| Command | rc, seconds | Result |
|---|---|---|
| `./scripts/lint_hdl.sh` | 0, 14 | 41 of 41 LINT OK |
| `./scripts/run_suites.sh` | 0, 1,466 | 33 suites, **1,021,485 checks, 0 failing**. Against round 1b's head (1,021,455) only two suites move: `aecp_notify` 20 -> 30 (R2.1) and `adp_engine` 1,328 -> 1,348 (`main`'s PR #152; `tb/adp_engine` at `83999eba` alone: rc 0, 1,348); `pp_top` 10,416 both |
| `make check` | 0, 31 | 41 mermaid + 18 wavedrom blocks, 1,120 links, 115 REQ rows (17 GAP findings, OK), 94 matrix rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | 0, 1 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0, 75 | `YOSYS 42 tops, all.v parsed 1 time(s)`, 42 `YOSYS OK` (`KL_aecp_notify` among them), `YOSYS XILINX OK KL_aecp_engine` |
| ROMs, `gen_ucode.py`, `gen_ltn_rom.py` (a separate archive copy) | 0, 0 | `ucode.hex` `518b900c4a5650902c3ea9125941e434857ba2f379b6c92268a67fef459d37f8` (2,048 words), `ltn_rom.hex` `23cc67eeadc7ecad8c9ceb7f9391095b64ada44d4e0f3a232ce82a2a69e7e956` (129 lines): round 1b's |
| `notify_mutants.py --jobs 4` | 0, 569 | 47 of 47 KILLED, six goldens PASS; 47 of 47 at their README counts (the 44 of round 1b with `ix_new_identity_unset` 2 -> 3 and `ix_rewrite_unmatched` 1 -> 3 from the new checks, as recorded; the three new at 2, 1, 1) |
| `ctr_mutants.py --jobs 4` | 0, 273 | control PASS, 17 of 17 KILLED (18 checks PASS); 17 of 17 at their README counts; identical to round 1b |
| `d3_mutants.py --jobs 4` | 0, 4,074 | 110 of 110 KILLED, six goldens PASS; the 98 `tb/pp_top` arms at their README counts; all 116 records (with the 12 in `tb/acmp_nvm` and `tb/rx_validator` and the goldens) identical to round 1b |
| `aecp_mutants.py --jobs 4` | 0, 576 | 60 checks PASS: 5 controls, 55 KILLED; 55 of 55 at their README counts (`hz-stream-key-none-talker-read` and `-talker-step` by hand: "the same 12"); identical to round 1b |
| `aecp_dispatch_mutants.py --jobs 4` | 0, 634 | 44 checks PASS: 4 controls, 40 KILLED; 40 of 40 at their README counts; identical to round 1b |
| `acmp_mutants.py --jobs 4` | 0, 214 | 19 of 19 KILLED, three goldens PASS; 22 of 22 records identical to round 1b |
| `gsi_mutants.py --jobs 4` | 0, 537 | 20 detected by named checks, golden and restored PASS; record lines identical to round 1b |
| `name_wr_mutant.py` | 0, 70 | decode killed, golden and restored PASS |
| `make -C tb/adp_engine mutants JOBS=4` (the merge touches `tb/adp_engine`) | 0, 197 | 43 checks PASS: both controls PASS, 41 of 41 KILLED, as `main`'s README records ("all 41 arms are KILLED"); 41 of 41 at their README counts (`cfg-valid-no-reset` 9 and `gate-enable-dropped-top` 7 by hand: their rows give those counts since lane P1) |

The hdl workflow's other campaigns (`tb/srp_top`, `tb/maap`) build no file the round changes
and were not run.

### R2.7 Parent consumer set at dev `241f9184`

Scratch parent `$VALIDATION_STORAGE/pp232-a520/parent` (never committed or pushed), moved from
`5fabb46e` to dev `241f91845230ae410506dffb16b71937127fd175` (`5fabb46e..241f9184` is PR
#638's merge: the baseline tools, the resource gate, `ci_scope.py`/`ci_events.py`; the four
submodule pins unchanged). Each `rev-parse --show-toplevel` checked before any git command:
round 1b's four patches reversed (`git apply -R --check`, then `git apply -R`, in reverse
order), the gitlink unstaged, `git checkout --detach 241f9184`; the processor submodule
fetched from the lane and detached at `2ea3dee`; the gitlink set in the index only
(`git update-index --cacheinfo 160000,2ea3dee...,protocol-processor`; `git submodule status`
shows no prefix). Patches, each `git apply --check` clean at `241f9184`, then applied:

| Patch | sha256 | Applies at `241f9184` |
|---|---|---|
| `parent-adoption-c8-bbf704ec.patch` | `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c` | yes |
| `parent-adoption-p2-p1-1269cdaf.patch` | `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84` | yes |
| `parent-adoption-c10-1269cdaf.patch` | `55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9` | yes |
| `parent-adoption-232-241f9184.patch` (this round, R2.3) | `88ee5e9643a453f8c31dc76e5f8d57e8deec89bcbbf9d4a4a8ca005757b72560` | yes, after c10 |

GNU Make 4.3 and the pinned Verilator 5.050 first on PATH (gate 10 also with the host's
Make 4.4.1). The numbering is this handoff's (sections 9 and R1b.7); round 2's "consumer gate
3" for the xvlog ratchet is gate 9 here.

| # | Command | rc, seconds | Result |
|---:|---|---|---|
| 1 | `scripts/check_cpp_idiom.py` | 0, 2 | every ratchet held (172 translation units) |
| 2 | `scripts/check_py_idiom.py` | 0, 4 | every ratchet held (307 modules) |
| 3 | `scripts/check_rtl_source_lists.py` | 0, 2 | 108 files, 4 of 4 consumer lists; processor 42/42 tops, 0 recorded |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0, 18 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0, 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0, 3 | protocol-processor 1,759 ports (as at `main` and round 1b), undocumented 111 <= 111 |
| 6 | `scripts/measure_naming.py --check` | 0, 0 | 95 recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0, 7 | within ratchets (its "can be lowered to 72" note as in round 1b) |
| 8 | `scripts/docs_check.py` | 0, 5 | 0 findings, 187 md + 975 files |
| 9 | `scripts/xvlog_gate.py --check` | 1, 174 (three patches); **0**, 152 (four patches) | three patches: `BANK IT ... pd_ix_w no longer occurs`; with `parent-adoption-232-241f9184.patch`: `PASS (2 finding(s) == ratchet; 0 hdl/, 2 pinned processors)`, pinned at `protocol-processor@2ea3dee2` (R2.3) |
| 10 | `sw/builder/test_builder.py` | 0, 1,779 (Make 4.3); 0, 1,255 (Make 4.4.1) | Make 4.3: "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 11's mf48 tree; gate 1b's `MAKEFLAGS += -e` arm, which Make 4.3 cannot exercise). Make 4.4.1: "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11 only). As in rounds 1 and 1b |
| 11 | `scripts/lint_rtl.py --check` | 0, 10 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0, 321 | legs 606, 606, 646 and 311 checks, 0 failures |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0, 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0, 31 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0, 2,624 | 9 benches RESULT: PASS, 0 FAIL; 4 render mutants caught; gmstep controls 6 of 6 |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | **2**, 204 | two-stream leg 65 checks, 0 failures; shipping leg 155 checks, **2 failures**: the two T30 INTERNAL LAW checks (`got=227 exp=292`, `got=285 exp=292`; first-event delay 18,396..18,821 cycles = 8.830..9.034 ticks). All 48 result lines identical to round 1b's run at `6e950fea`, which was identical to `main` `5c71928a`'s: recorded against milan-fpga #643, as the assignment directs |
| 16b | `python3 tdm8_render_mutants.py --leg-defects` (gate 16's last step, not reached after the failure) | 0, 480 | 5 of 5: two positive controls and three leg defects caught |

With the fourth patch applied, gates 1 to 8, 3b and 11 re-ran: all rc 0, the same
summaries (`pgates-4patches/`).

### R2.8 Parent-visible list (round 2)

- No port, parameter, register or behaviour change; the port gate counts 1,759 processor
  ports, as at `main` and round 1b. The round adds tests and documentation only (and
  `main`'s merge).
- One parent adoption line, as in round 1b: `parent-adoption-232-241f9184.patch` (after the
  c10 patch) banks the vanished `pd_ix_w` finding in `scripts/xvlog.budget`. Without it gate 9
  exits 1 (`BANK IT`); with it, rc 0.
- Gate 16's two T30 INTERNAL law checks fail at the head exactly as at `main` (all 48 result
  lines identical): milan-fpga #643.
- #638's gate, the routed worst paths and the area figures are round 1b's (the head's HDL
  logic is unchanged); recording a new #638 baseline A is the merge bank's step.
- For the manager (both reviews' pending duties): link #232's results from epic #229
  (acceptance criterion 5); archive `evidence-r2/`; build the final current-dev candidate
  with the four patches.

### R2.9 Run receipts

Scratch (outside the tree): `$VALIDATION_STORAGE/pp232-a520/r2/`:
- `tree-head/`, `tree-main83/`, `tree-rom/`: `git archive` trees;
- `logs/`: lint, suites, `make check`, `gen_matrix`, Yosys, ROMs, `tb/adp_engine` at `main`,
  `mem.log`;
- `camp/`: campaign logs, rc files, `results.json` and the README comparisons
  (`*-compare.txt`);
- `ixmain/`: the IX bench on `main`'s RTL;
- `camp-ix-dev*`: the seven controls with `--only`;
- `probes/`: the 22 reviewer probes;
- `lockstep/`: the reviewer edits on the round-1b bench;
- `pgates/`, `pgates-make441/`, `pgates-xvlog/`, `pgates-4patches/`: parent gate logs;
- `review-evidence/`: the two reviews' packets, from the parent's `pp232-review-evidence`
  branch at `4e438b23`;
- `tools/`: the extraction, re-derivation and probe-table scripts.

Each command wrote its own log and rc file, and none was piped. Seconds are in R2.6 and
R2.7; the probes took 607 to 907 s each, three at a time. There were no Vivado
implementation runs this round. xvlog ran only under the shared lock, beside no other build
of this lane.

Concurrency: these ran together, under the 12 GB service cap:
- the suites, the D3 campaign and the second campaign chain;
- then the probes beside the remaining campaigns and the parent's builder and heavy gates.

The cgroup reached its cap repeatedly. `memory.events` reports `max` 134,607 (reclaim at
the cap), `oom` 0 and `oom_kill` 0; swap peaked at 5.63 GB. Every run completed with the rc
reported above.

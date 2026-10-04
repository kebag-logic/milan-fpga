# [A525] HANDOFF — milan-fpga #639 (epic #229 levers 3 and 6)

Status: ROUND 2b REVIEW READY (section 14). Head `c725be12d7ea6bf96f1b64e3a56416f0d4defd6c`
on local branch `pp639-armq-lsnrec`, not pushed. It is the `--no-ff` merge of `main`
`b0a74196` (PR #157) on the manager's `1cba30c9`, and no fix commit was needed. Every
processor suite and campaign is rc 0, and each record equals the union of the two sides.
The parent consumer set at dev `6c22d3ca` with four patches is 17 of 17 rc 0. Area is
unchanged.

Round 2 status: REVIEW READY (section 13). Head `2ff8183ac3ae8b70462d4d6e702c31a00b76ea90`
on local branch `pp639-armq-lsnrec`, not pushed: four one-line commits on round 1's
`9e8699105c126db7764820916a827ef0538bc4b2` (pushed by the manager as processor PR #155).
R462-1 F1 is closed by a committed drive of the arm-port faces (`tb/pp_top` AQ3, AQ4) and
nine controls; S1 is taken as a comment; the lockstep benches are published in `lockstep/`;
`main` has not moved. Round 1: both levers done, cycle-exact, no port, parameter or
register change.

- Processor repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
  (`git remote get-url origin` checked); HEAD at start `5c71928ad2bf1a854a5538d69b77214dfdf1697f`.
- Branch `pp639-armq-lsnrec` from `main` `5c71928a`.
- Assignment: kebag-logic/milan-fpga#639 comment 5976100204. TAKEN: comment 5976102877.
  REVIEW READY: comment 5980139653 (round 1), 5982661712 (round 2), 5984636752 (round 2b).
- Executor: [A525]. Reviewers: [R462] (internal), [R463] (external).

## 1. Outcome

| | Lever 3: the top's timer arm-port queues | Lever 6: the ACMP listener records |
|---|---|---|
| Source at `main` | `protocol_processor_top.sv:2952` `armq_r`, 8 x 4 x 47 bits at 1x1 (48 at 8x8), a packed shift queue | `KL_pp_acmp_listener.sv:385` `rec_ram_r`, N_SINKS_P x 384 bits (376 kept), sync-read RAM |
| Primitive, `main` -> head | 1,152 flops (1x1 standalone; 1,012 routed, 1,316 at 8x8) -> eight 4-entry rings, `RAM32M x 8` each in synthesis (54 RAM32M + 1 RAM32X1D routed) | 5 RAMB36E1 -> `RAM32M x 63` in synthesis (52 routed: bits never read are trimmed); no read register |
| Behaviour | cycle-identical at the arm port and the drop counter (lockstep, 3.1) | cycle-identical at every port (lockstep, 3.2) |
| Shipping route, base -> head (both levers) | LUT 51,434 -> 51,152 (-282); FF 59,691 -> 58,598 (-1,093); slices 15,847 -> 15,803 (-44); RAMB36 79 -> 74 (-5); WNS +0.079 -> +0.093 ns, WHS +0.014 -> +0.036 ns | |
| Standalone 1x1, base -> head | LUT 24,930 -> 24,648 (-282); FF 25,465 -> 24,278 (-1,187); RAMB36 21 -> 16 | |
| Standalone 8x8, base -> head | LUT 32,584 -> 32,154 (-430); FF 34,211 -> 32,858 (-1,353); RAMB36 26 -> 21 | |

Against #638's estimates: lever 3's flop saving is as estimated (about 1,100); its LUT
saving is about 400 at 1x1, not about 1,000 (5.4). Lever 6 frees the five RAMB36 for 38 to
195 more LUTs in the listener (5.3), inside the estimated "about 250".

## 2. Commits

| Commit | Subject |
|---|---|
| `b42066c` | Hold the eight timer-arm queues in distributed-RAM rings and grade the arm port against a model in tb/pp_top |
| `1bb3ba4` | Hold the ACMP listener records in distributed RAM read without a read register, and grade the reset sweep |
| `9eebc61` | Plant the issue #639 storage controls in acmp_mutants.py |
| `5828bb8` | Run one acmp_mutants.py golden per suite and run mode |
| `cfd62e8` | Record the issue #639 storage, its section AQ, check RS and their controls in the docs |
| `b845d01` | Merge main 83999eba (PR #152, the ADP walk lane) into the issue #639 lane |
| `9e86991` | Merge main c050d971 (PR #153, the #232 notification registry) into the issue #639 lane |

One-line subjects, no body, no trailer; no rebase, no amend. Every Vivado run and the full
parent set measure `9eebc61`'s code. `5828bb8` and `cfd62e8` change no `hdl/` file. Both
merges leave `protocol_processor_top.sv` and `KL_pp_acmp_listener.sv` byte-identical to
`9eebc61` (sha256 `ada29e74...` and `f8bc590e...`), and the four test files of this lane
too (`acmp_mutants.py` differs only by `5828bb8`).

## 3. Changes (file:line at the head)

### 3.1 Lever 3: the top's timer arm-port queues

| File:line | Change |
|---|---|
| `hdl/top/protocol_processor_top.sv:2952-2953` | `armq_r` (8 x 4 x `ARM_W_C` flops) replaced by `armq_hd_w` (each face's oldest entry, read from its ring) and `armq_hd_r` (a 2-bit head index per face); `armq_cnt_r` unchanged |
| `:2994-3005` | the ring's contract: entries never move, push at head + count, the full-and-pop overwrite of the leaving head, why eight rings and not one array, why the entries need no reset, why an unpacked memory (not the packed part-write yosys lowered as a barrel shift) |
| `:3006-3018` | `g_armq[g]`: `(* ram_style = "distributed" *) mem_r [0:3]`; write port `armq_ram_wr` at `wr_ix_w = armq_hd_r[g] + armq_cnt_r[g][1:0]`, gated by `armq_push_ok_w[g]`; asynchronous read `armq_hd_w[g] = mem_r[armq_hd_r[g]]` |
| `:3022` | reset clears `armq_hd_r` (with `armq_cnt_r`, as before) instead of 1,504 queue bits |
| `:3035-3037` | a pop loads the arm port from `armq_hd_w[i]` and advances `armq_hd_r[i]`; the shift and the equality-decoded append are gone |

Unchanged on purpose: the drain pick (`arm_drain_pick`), `armq_mid_w`, `armq_push_ok_w`,
the count update, the drop counter `arm_drop_r` (snapshot word 24) and the arm-port
registers.

### 3.2 Lever 6: the listener records

| File:line | Change |
|---|---|
| `hdl/acmp/KL_pp_acmp_listener.sv:13` | banner: the record lives in a distributed RAM |
| `:381-394` | the storage comment: a 1W1R RAM with no reset on the array (X_INIT sweeps it); why distributed (the wide-and-shallow trap `KL_pp_dispatch` documents); why the read register can go |
| `:395-396` | `(* ram_style = "distributed" *)` on `rec_ram_r`; the read register `rec_rdata_r` and its `always_ff` removed |
| `:746` | `rec_rd_w = rec_ram_r[sink_r]`, an asynchronous read |
| `:1034`, `:1067` | X_STRT_RD and X_RDREC comments: "record read next cycle" |
| `:1051`, `:1072` | X_STRT_AP and X_LATCH load `rec_r` from `rec_rd_w` |

Why the read in the consuming cycle equals the old register's: `sink_r` is written only in
reset and X_IDLE; X_RDREC and X_STRT_RD are entered only from X_IDLE, and X_LATCH and
X_STRT_AP only from them; `recwr_en_w` is true only in X_INIT, X_PRELOAD and X_WB, so no
record is written at the edge between issue and consumption; `rec_rd_w` and the old
`rec_rdata_r` are read nowhere else. The walk keeps both issue states, so every record is
consumed in the same cycle as on `main`.

A single-port form (the read on the write port's address, equal outside X_INIT) was tried
first: Vivado mapped it `RAM16X1S x 376`, one LUT per bit (376 LUTs) against `RAM32M x 63`
(252) for the dual-port form, so the dual-port read on `sink_r` was kept (module-level
synthesis, scratch).

### 3.3 Tests and docs

| File:line | Change |
|---|---|
| `tb/pp_top/pp_top_wrap.sv:484-495`, `:879-903` | `dbg_aq_vld_o`, `dbg_aq_arm_o`, `dbg_aq_port_valid_o`, `dbg_aq_port_o`, `dbg_aq_drop_o`: the eight faces from their own nets, the arm port and the drop counter |
| `tb/pp_top/sim_main.cpp:713-796` | `ArmQueueModel`: the banner's contract as an eight-FIFO model, with coverage counters |
| `:805`, `:1516`, `:1519` | every harness runs it at every edge (`H::step`) |
| `:13810-13828` | `run_arm_queue`: AQ1, AQ2 and the coverage line |
| `:13882-13909` | `--arm-queue-only`; AQ graded at the end of a full default run or that mode |
| `tb/acmp_listener/sim_main.cpp:765`, `:988-1005`, `:1780` | RS: a reset with records bound, then GET_RX_STATE on every sink through the walk |
| `tb/pp_top/acmp_mutants.py:53`, `:164-218` | `PP_TOP_AQ`; the issue #639 group `STORAGE` (ten controls); `TALLY` reads an `AQ:` tally |
| `tb/pp_top/acmp_mutants.py:280-284`, `:304-305` | one golden per suite and run mode (`golden_label`) |
| `tb/pp_top/README.md` | the AQ bullet in "What it proves"; section AQ (rule, coverage, controls with counts); the ACMP controls paragraph's re-run |
| `tb/acmp_listener/README.md` | 3,111 checks; RS; the issue #639 controls table |
| `docs/architecture/09_verification.md` §8.8 | the two structures, their checks and controls |
| `docs/guides/hdl-engineer.md` §3.1 | the asynchronously read distributed RAMs (µCPU operand file, the arm-port rings, the listener records), the listener's kept issue cycle |
| `docs/architecture/07_memory_maps.md` §6 | the sink records are distributed RAM, and why |
| `docs/architecture/08_timing.md` §3 | the one arm port, the four-deep per-face rings, the drain priority, the counted overrun |

## 4. Tests and their controls

### 4.1 Lockstep, the arm-port block (not committed; published in round 2, 13.6)

The block is cut byte for byte from each version of the top: from the `====` line above
"timer arm-port priority mux (banner)" to the one above "PRNG draw-port owner mux
(banner)", then wrapped with the eight faces as inputs and the arm port and drop counter as
outputs. Reference: `main` `5c71928a` (top sha256 `d49482e9...b2374d`); candidate:
`9eebc61` (`ada29e74...552248`). Identical random arms into both every cycle; port, valid
and drop counter compared after both clock phases; resets mid-run. Seeds 1-4 per shape are
bursty "shaped" phases, 5-8 fully random rates with long saturation.

| Shape (`TMR_AW_C`, arm width) | Runs x cycles | Mismatches |
|---|---|---|
| 6, 47 bits (1x1) | 8 x 1,000,000 | 0 |
| 7, 48 bits (8x8) | 8 x 1,000,000 | 0 |
| 5 | 8 x 1,000,000 | 0 |
| 8 | 8 x 1,000,000 | 0 |
| total | 32 runs | **0**: 23,976,104 arms issued; 41,742,164 offers to a full face (drops); 8,003,108 clocks a full face popped and pushed (the leaving head overwritten); 12,874,888 drop-counter rises; 412 resets mid-run |

| Control (planted in the candidate) | Mismatches | Runs caught |
|---|---:|---:|
| `wr_at_head`: push at the head index | 6,039,149 | 8 of 8 |
| `wr_at_mid`: push at head + the count after the pop | 9,552,242 | 8 of 8 |
| `head_stuck`: a pop never advances the head | 9,799,762 | 8 of 8 |
| `read_tail`: the port reads head + count | 11,760,798 | 8 of 8 |
| `write_refused`: the write gated by the offer, not its acceptance | 922,754 | 8 of 8 |
| `ring_of_three`: the head wraps after entry 2 | 6,420,932 | 8 of 8 |
| probe, not a control: the head index not reset | 0 | 0 of 8 (equivalent: the count is reset, and a ring may start anywhere) |

### 4.2 Lockstep, the listener (not committed; published in round 2, 13.6)

`main`'s `KL_pp_acmp_listener` renamed `_ref` (sha256 `7f6bed96...3292f`) beside
`9eebc61`'s (`f8bc590e...fec57fc`), identical inputs from emulated faces (RX slot sync
read, TX slot grant, PRNG, timer expiries, TK events, preloads, started/stopped requests,
lock), every output compared after both clock phases, resets mid-run. The bench snoops the
listener's own PROBE_TX commands and answers about half of them with a matching
PROBE_TX_RESPONSE, so streams settle.

| `N_SINKS_P` | Runs x cycles | Mismatches |
|---|---|---|
| 2 (1x1) | 8 x 1,000,000 | 0 |
| 9 (8x8) | 8 x 1,000,000 | 0 |
| 8, 1, 3 | 8 x 1,000,000 each | 0 |
| total | 40 runs | **0**: 544,621 transactions; 614,189 X_LATCH and 141,062 X_STRT_AP record reads; 523,900 record writes; 214,333 probe responses; 31,686 settles; 375 resets |

| Control (planted in the candidate) | Mismatches | Runs caught |
|---|---:|---:|
| `read_sink_zero` | 15,836,966 | 8 of 8 |
| `read_sampled_in_idle` (a register sampled in X_IDLE: the stale read) | 15,862,266 | 8 of 8 |
| `started_bit_unstored` (record bit 12) | 15,605,320 | 8 of 8 |
| `settled_vlan_bit_unstored` (record bit 305) | 1,613,238 | 8 of 8 |
| `sweep_misaddressed` (X_INIT writes `sink_r`) | 5,295,758 | 8 of 8 |

### 4.3 Committed: `tb/pp_top` section AQ

AQ1 (the model saw arms) and AQ2 (port, valid and drop counter equal the model after every
edge of the main harness). Coverage at the head (`--arm-queue-only`, 208-211 s): 71,258,305
edges, 8,270 arms, 28 clocks with two faces holding arms, 4,288 pushes as a face's one arm
left, 0 onto a face still holding one, 0 fills, 0 drops; the full default run: 71,290,136
edges, 8,280 arms, the same zeros. From outside the top no face ever holds two arms, so in
round 1 the full-queue path was the lockstep bench's; round 2 grades it in the tree (AQ3,
AQ4, 13.4). **Red proof that AQ describes unchanged
behaviour:** the head's `tb/pp_top` built against `main`'s RTL passes AQ with the same
coverage to the edge (71,258,305 edges, 8,270 arms, 28, 4,288).

| Control (`acmp_mutants.py`, `--arm-queue-only`) | Named check | Verdict | Failing checks in the run |
|---|---|---|---:|
| `armq_read_tail` | AQ2 | KILLED | 71 |
| `armq_head_stuck` | AQ2 | KILLED | 2 |
| `armq_ring_of_three` | AQ2 | KILLED | 11 |
| `armq_write_at_head` | AQ2 | KILLED | 2 |
| `armq_write_at_mid` | AQ2 | KILLED | 2 |
| `write_refused` (not shipped in round 1) | AQ2 | survives at the top (no face fills); the lockstep bench kills it. Round 2: `armq_write_refused`, KILLED by AQ3 (13.4) | 0 |

### 4.4 Committed: `tb/acmp_listener` RS

RS: with records bound at the end of the walk, a reset, then GET_RX_STATE per sink must
answer the unbound record and write the model's unbound record back: +123 checks (2,988 ->
3,111). Red proof: `rec_sweep_misaddressed` passed the suite without RS (0 of 2,988 failing)
and fails 37 of 3,111 with it. RS describes unchanged behaviour: the head's suite passes
3,111 of 3,111 on `main`'s RTL.

| Control (`acmp_mutants.py`, `tb/acmp_listener`) | Named checks | Verdict | Failing |
|---|---|---|---|
| `rec_read_sink_zero` | B12 parked sink 7; F05.3 BIND_SAME x PWA sm_state | KILLED | 645 of 3,080 |
| `rec_read_in_idle` | RV8(setup) state sync | KILLED | 1 of 3,111 |
| `rec_started_unstored` | S1d; F05.3 GETRX x PWA flags | KILLED | 91 of 3,111 |
| `rec_settled_vlan_unstored` | F05.3 GETRX x SOK settled; B12 | KILLED | 25 of 3,111 |
| `rec_sweep_misaddressed` | RS binding | KILLED | 37 of 3,111 |

### 4.5 The golden keying (`5828bb8`)

The driver kept one golden per suite directory, so with two `tb/pp_top` run modes only the
last (`--arm-queue-only`) ran a golden and the `--acmp-only` golden silently did not. Found
in this lane's own campaign at `9eebc61` (its record shows three goldens); `5828bb8` keys
goldens by directory and run (four goldens).

## 5. Vivado before and after (#638's recipe and gate on dev `241f9184`)

Base: scratch parent dev `241f91845230ae410506dffb16b71937127fd175` + processor `5c71928a` +
c8 (`-bbf704ec`), p2-p1 and c10 patches. Head: the same with the processor at `9eebc61`.
Vivado 2026.1 build 6511674, `xc7a100t-fgg484-2`, 50 MHz (20 ns), AreaOptimized_high /
ExploreArea / ExtraPostPlacementOpt / AggressiveExplore, 32 threads, default seed; the
standalone runs use `--integrated-clock`, the 8x8 parameters an RTL elaboration. One
Vivado at a time, each under `flock /tmp/milan-vivado.lock` (other lanes shared the host and
the lock). The two exports differ only by their work-directory paths, two generated dates
and the order of one tree listing in the top Verilog; ROMs (`ltn_rom.hex` `23cc67ee...`,
`ucode.hex` `518b900c...`), XDC and the three `.init` images hash equal.

### 5.1 Integrated shipping route, `endstation_ax7101_1x1_tdm8`, whole image

| | LUT | FF | Slice | RAMB36 / RAMB18 | DSP | CARRY4 | WNS / WHS ns |
|---|---:|---:|---:|---:|---:|---:|---:|
| base | 51,434 | 59,691 | 15,847 (99.98 %) | 79 / 27 | 14 | 3,526 | +0.079 / +0.014 |
| head | 51,152 | 58,598 | 15,803 (99.70 %) | 74 / 27 | 14 | 3,527 | +0.093 / +0.036 |
| head - base | -282 | -1,093 | -44 | -5 / 0 | 0 | +1 | +0.014 / +0.022 |

LUT as logic 49,158 -> 48,450 (-708); LUT as memory 2,276 -> 2,702 (+426); SLICEL 11,099 ->
11,073; SLICEM 4,748 -> 4,730; BRAM tiles 92.5 -> 87.5; F7 1,448 -> 1,378. Route status:
base 107,053 routable nets, head 105,954, all fully routed, 0 with routing errors. Both
meet the build gate (WNS at least +0.030, WHS at least 0). The base route needed seven
global routing iterations (88.3 min); the head two (35.9 min).

### 5.2 Standalone `KL_pp_shadow`, 20 ns

| | LUT (logic + memory) | FF | RAMB36 / RAMB18 | DSP | CARRY4 | internal WNS ns (estimate) |
|---|---:|---:|---:|---:|---:|---:|
| 1x1 base | 24,930 (23,644 + 1,286) | 25,465 | 21 / 3 | 8 | 1,643 | -2.059 |
| 1x1 head | 24,648 (22,908 + 1,740) | 24,278 | 16 / 3 | 8 | 1,644 | -0.743 |
| 1x1 head - base | -282 | -1,187 | -5 / 0 | 0 | +1 | |
| 8x8 base | 32,584 (31,502 + 1,082) | 34,211 | 26 / 5 | 8 | 2,028 | -2.161 |
| 8x8 head | 32,154 (30,608 + 1,546) | 32,858 | 21 / 5 | 8 | 2,028 | -2.153 |
| 8x8 head - base | -430 | -1,353 | -5 / 0 | 0 | 0 | |

The standalone WNS is a synthesis estimate with no I/O constraints (as #638 states).

### 5.3 The two sub-blocks (hierarchy reports, `pp_baseline_rank.py` own-logic rows)

| Scope | Endpoint | LUT (LUTRAM) base -> head | FF base -> head | RAMB36 base -> head |
|---|---|---|---|---|
| top's own logic, `u_pp` outside its sub-blocks | route | 390 (0) -> 654 (218) | 2,968 -> 1,972 | 0 -> 0 |
| | 1x1 | 447 (0) -> 769 (246) | 3,167 -> 2,034 | 0 -> 0 |
| | 8x8 | 465 (0) -> 880 (256) | 4,735 -> 3,433 | 0 -> 0 |
| listener store, `u_pp/u_listener` | route | 1,301 (0) -> 1,496 (208) | 1,106 -> 1,055 | 5 -> 0 |
| | 1x1 | 1,434 (0) -> 1,557 (208) | 1,106 -> 1,051 | 5 -> 0 |
| | 8x8 | 1,630 (0) -> 1,668 (208) | 1,128 -> 1,079 | 5 -> 0 |
| wrapper | route | 24,485 (1,152) -> 24,516 (1,578) | 24,267 -> 23,221 | 21 -> 16 |

### 5.4 Reading the LUT figures

- The top's own logic grows by the rings (218-256 LUTs as memory) plus 46-159 logic LUTs
  (pointers, write index, read mux), and loses 996-1,302 flops.
- The base's shift-queue logic is not all in the top's own row: Vivado pulled part of it
  into the engines that drive the faces. At 1x1 those blocks shrink with nothing changed
  in them: `u_notify` -201, `u_originator` -136, `u_adp` -109, `u_maap` -87, `u_srp` -87
  (the gate's sub-block lines, head against base). So lever 3's LUT saving is about the
  wrapper's -282 less lever 6's +123: about 400 at 1x1.
- #638 estimated about 1,000 because it counted the 1,178 write-side LUTs as removable; the
  ring keeps a read mux and pointers and adds 218-256 LUTs of RAM32M.
- Lever 6 costs +38 to +195 LUTs in the listener (208 LUTs of RAM32M less 85 to 170 logic
  LUTs), for 5 RAMB36 at every endpoint.
- Routed, the wrapper's LUTs are flat (+31) and its flops -1,046; the image's other -313 LUTs
  are optimization elsewhere in the datapath, so the route's LUT delta is within its noise.
  The flop, BRAM and slice figures are the route's real effect.

### 5.5 The cell census (by cell name, `baseline_cells.tsv`)

| Census | Route base / head | 1x1 base / head | 8x8 base / head |
|---|---|---|---|
| `armq_r` flops | 1,012 / 0 | 1,152 / 0 | 1,316 / 0 |
| other `armq` flops (count; head index) | 22 / 37 | 22 / 39 | 24 / 38 |
| `u_pp/g_armq` RAM | - / 54 RAM32M + 1 RAM32X1D | - / 61 RAM32M + 1 RAM32X1D | - / 64 RAM32M |
| `u_pp/u_listener/rec_ram` | 5 RAMB36E1 / 52 RAM32M | 5 RAMB36E1 / 52 RAM32M | 5 RAMB36E1 / 52 RAM32M |
| `rec_rdata` flops | 0 / 0 | 0 / 0 | 0 / 0 |

### 5.6 #638's gate

The gate re-hashes each run's sources from the paths its script names, so each check ran
with the scratch parent's processor at that run's revision (base at `5c71928a`, head at
`9eebc61`).

| Endpoint | base vs committed record (dev C) | head vs committed record | head vs base (base `record --write` into a scratch copy of the baseline) |
|---|---|---|---|
| route-1x1 | 1: LUT +667 over 500 (the unrecorded adoption: P1, C8, C10) | 0, "re-baseline recommended" (FF, RAMB36) | 0, "re-baseline recommended" (FF, RAMB36) |
| ooc-1x1 | 1: LUT +598 over 250 | 1: LUT +316 over 250 | 0, "re-baseline recommended" (LUT, FF, RAMB36) |
| ooc-8x8 | 1: LUT +1,028 over 316 | 1: LUT +598 over 316 | 0, "re-baseline recommended" (LUT, FF, RAMB36) |

The committed record is dev C (processor `631eeb34`); against it the base, the next
adoption, already fails, by more than the head. `check-baseline` on the scratch copy with
base's three records: "baseline PASS: 3 endpoints". The scratch copy is not a change to the
parent: re-recording the gate's baseline belongs to the adoption that moves the pin (the
round-7 rule of #638), with this lane's head as the measurement.

### 5.7 Run receipts

Every run rc 0, started in the background with its own log, one `Synth 8-4445` match each
(the echoed severity command, not a diagnostic), 16 `Synth 8-7186` each (all the
notification registry's `rows_r` at `main`, none from either structure).

| Combination | Run | rc | Minutes | Log | Log SHA-256, first 16 | Log bytes |
|---|---|---:|---:|---|---|---:|
| base | Integrated route, 1x1 | 0 | 88.3 | `baseline.log` | `d43db15726a34de9` | 686,459 |
| base | RTL elaboration, 8x8 parameters | 0 | 1.1 | `elaborate.log` | `41d92901f4cd46f7` | 208,598 |
| base | Standalone synthesis, 1x1 | 0 | 17.9 | `baseline.log` | `1687a452d71a4fe8` | 235,426 |
| base | Standalone synthesis, 8x8 | 0 | 22.1 | `baseline.log` | `b53595fff80c8795` | 239,819 |
| head | Integrated route, 1x1 | 0 | 35.9 | `baseline.log` | `e915fb5988d4e39a` | 702,897 |
| head | RTL elaboration, 8x8 parameters | 0 | 1.2 | `elaborate.log` | `e17c0daff1477ebb` | 208,596 |
| head | Standalone synthesis, 1x1 | 0 | 20.3 | `baseline.log` | `694ef6e0c2da3914` | 236,822 |
| head | Standalone synthesis, 8x8 | 0 | 26.0 | `baseline.log` | `32b7b48d49080be8` | 239,477 |

## 6. Storage inventory (the two structures in scope, and the other arrays of the two blocks)

Vivado report lines are from each run's `baseline.log`, "Distributed RAM: Final Mapping
Report" or "Block RAM: Final Mapping Report"; flop counts from the cell census.

| Structure | Source (head) | Shape | Intended | Actual, base | Actual, head | Vivado report lines |
|---|---|---|---|---|---|---|
| Arm-port queues | `protocol_processor_top.sv:3006-3018` (`:2952` at `main`) | 8 x 4 x 47 (1x1), x 48 (8x8) | distributed RAM, one ring per face (attribute) | flip-flops, a shift queue: 1,152 / 1,012 routed / 1,316 at 8x8 | `RAM32M x 8` per face | head route `:3657-3664` `\|protocol_processor_top__GCB1 \| g_armq[k].mem_r_reg \| User Attribute \| 4 x 47 \| RAM32M x 8 \|` (k = 7..0); head 1x1 `:1991-1998` the same; head 8x8 `:1997-2004` `... \| 4 x 48 \| RAM32M x 8 \|`; base: no mapping line, `armq_r_reg` FD cells in the census |
| Queue counts and head indices | `:2953-2954` | 8 x (3 + 2) bits | flip-flops (read in parallel by the drain pick) | 22-24 FD | 37-39 FD | census |
| Listener records | `KL_pp_acmp_listener.sv:395-396` (`:385` at `main`) | N_SINKS_P x 384 (376 kept): 2 at 1x1, 9 at 8x8 | distributed RAM (attribute), read asynchronously, no register | block RAM, 5 RAMB36 (the sixth, a RAMB18, removed by constant propagation in the route) | `RAM32M x 63` in synthesis, 52 routed | base route `:3582` `\|u_listener \| rec_ram_r_reg \| 2 x 376(READ_FIRST) \| W \| \| 2 x 376(WRITE_FIRST) \| \| R \| Port A and B \| 1 \| 5 \|` and `:3277` `Removed Macro Instance : u_listener/i_1/rec_ram_r_reg_5, of type : RAMB18E1 in constant propagation`; base 1x1 `:1946` and 8x8 `:1968` (`9 x 376`); head route `:3667` `\|u_listener \| rec_ram_r_reg \| User Attribute \| 2 x 376 \| RAM32M x 63 \|`; head 1x1 `:2003`; head 8x8 `:2005` (`16 x 376`) |
| Listener transition ROM `trom_r` | `KL_pp_acmp_listener.sv:418` | 128 x 32 (23 kept) | "BRAM-shaped" sync-read ROM | logic (no block RAM or ROM mapping line) | unchanged | `Synth 8-3936 ... 'trom_rdata_r_reg' ... trimmed from '32' to '23' bits` (head route `:1514`) |
| Bound views `bound_*_r` | `protocol_processor_top.sv:986-989` | per sink, 188 bits | flip-flops (each sink is a parallel output port) | flip-flops | unchanged | census |
| RX free FIFO `rxf_slot_r`, TX lane queues `laneq_*_r`, PRNG kinds `pr_kind_r`, GSI status `lstn_gsi_status_r` | `:1327`, `:4349`, `:3061`, `:3404` | a few bits per entry | flip-flops | flip-flops | unchanged | census |

Exhaustion is unchanged: an arm offered to a full face is dropped and counted (snapshot
word 24); the listener has no exhaustion (one record per sink, indexed).

## 7. Suites

### 7.1 At `main` and at the code head

| Command | `main` `5c71928a` | Head |
|---|---|---|
| `./scripts/run_suites.sh` | rc 0, 33 suites, 1,021,449 checks, 1,004 s | rc 0 at `9eebc61`, 33 suites, 1,021,574 checks, 1,072 s; only `acmp_listener` 2,988 -> 3,111 (RS) and `pp_top` 10,416 -> 10,418 (AQ1, AQ2) |
| `./scripts/lint_hdl.sh` | | rc 0, 41 of 41 |
| `./syn/yosys/run.sh` | | rc 0 at `5828bb8`, 40 s: `YOSYS 42 tops, all.v parsed 1 time(s)`; `YOSYS OK KL_pp_acmp_listener`, `YOSYS OK protocol_processor_top`; `YOSYS XILINX OK KL_aecp_engine` |
| `make check` (scratch snapshot of the head's files) | | rc 0 at `cfd62e8`: 41 mermaid + 18 wavedrom blocks, 1,117 links, 115 REQ rows, 94 matrix rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | | rc 0, 94 rows, 0 untested |

### 7.2 At the merges

`main` moved twice during the lane; each was merged with `--no-ff` (assignment: "Merge
`main` at the end if it moved"), each merge tree equal to `git merge-tree --write-tree`'s,
so nothing was hand-merged and neither merge touched a file of this lane's code or tests.

| | `b845d01`: `main` `83999eba` (PR #152) | `9e86991`: `main` `c050d971` (PR #153) |
|---|---|---|
| `main`'s change | the ADP walk lane: `KL_adp_engine.sv` comments only, `tb/adp_engine`, docs 04, 09 (line 140), 00 | the #232 registry: `KL_aecp_notify.sv` (functional), `tb/aecp_notify`, `notify_mutants.py`, docs 06, 09, `tb/pp_top/README.md` (the notify record) |
| `run_suites.sh` | rc 0, 1,054 s, 33 suites, 1,021,594 checks; only `adp_engine` moved (1,328 -> 1,348, PR #152's checks) | rc 0, 1,105 s, 33 suites, 1,021,610 checks; against `b845d01` only `aecp_notify` moved (14 -> 30, PR #153's checks) |
| `lint_hdl.sh` | rc 0, 41 of 41 | rc 0, 41 of 41 |
| `make check`, `gen_matrix --check` | rc 0 (1,123 links), rc 0 | rc 0 (1,123 links), rc 0 |
| ROMs | regenerate equal (`23cc67ee...`, `518b900c...`) | equal |
| `syn/yosys/run.sh` | | rc 0, 74 s, 42 tops, one parse |

## 8. Campaigns

### 8.1 At the code head

Every driver whose build list holds `protocol_processor_top.sv` or
`KL_pp_acmp_listener.sv`: the eight `tb/pp_top` drivers, `tb/adp_engine/mutants.py` and
`tb/maap/mutants.py` (both have `pp_top` arms). `tb/srp_top`, `tb/srp_admission`,
`tb/acmp_talker` and `tb/desc_store` build neither file and were not run. Each ran from a
`git archive` of `5828bb8` (its `hdl/` is `9eebc61`'s), the driver in the foreground of
its own job with its own log and rc file, never piped. "At the record" compares every arm's
failing-check count (the FAIL lines of its own log, or `results.json`) with the count the
suite README records for it, which is `main`'s (the convention lane #232's round 1b used);
where an arm differed it was re-run on a `git archive` of `main` and compared line by line.

| Campaign | Head | Every arm against the record |
|---|---|---|
| `acmp_mutants.py --jobs 1` | rc 0, 1,877 s: 29 of 29 KILLED, four goldens PASS | the 19 earlier arms at their recorded counts (14 `pp_top`, 4 `tb/acmp_listener` now of 3,111 / 3,107 checks, 1 `tb/rx_validator`); the ten issue #639 arms are new (4.3, 4.4) |
| `notify_mutants.py --jobs 2` | rc 0, 583 s: 40 of 40 KILLED, goldens PASS | 40 of 40 |
| `ctr_mutants.py` | rc 0, 126 s: control PASS, 17 of 17 KILLED (18 checks) | 17 of 17 |
| `aecp_mutants.py` | rc 0, 394 s: 60 checks PASS (5 controls, 55 KILLED) | 55 of 55 |
| `aecp_dispatch_mutants.py` | rc 0, 434 s: 44 checks PASS (4 controls, 40 KILLED) | 40 of 40 |
| `d3_mutants.py --jobs 2` | rc 0, 5,397 s: 110 of 110 KILLED, goldens PASS | the 98 `pp_top` arms at the record; the 12 `tb/acmp_nvm` / `tb/rx_validator` arms (recorded there under other names) re-run on `main` (rc 0, 74 s): verdicts and failing checks identical, 12 of 12 |
| `gsi_mutants.py` | rc 0, 433 s: 20 detected by named checks; golden and restored PASS | the record names a check per arm, no counts: all 20 fail |
| `name_wr_mutant.py` | rc 0, 47 s: decode killed; golden and restored PASS | as recorded |
| `tb/adp_engine/mutants.py --jobs 2` | rc 0, 245 s: 32 checks PASS (2 controls, 30 KILLED) | 28 of 30; `cfg-valid-no-reset` and `gate-enable-dropped-top` fail more checks than the README's 2026-09-29 counts, and on `main` (rc 0, 103 s) their FAIL lines are identical to the head's: a stale record, not this lane |
| `tb/maap/mutants.py --jobs 2` | rc 0, 148 s: 32 checks PASS (3 controls, 29 KILLED) | 29 of 29 |

### 8.2 At the merges

| Campaign | `b845d01` | `9e86991` |
|---|---|---|
| `tb/adp_engine/mutants.py --jobs 2` (PR #152 changed it) | rc 0, 284 s: 43 checks PASS (2 controls, 41 KILLED); 39 of 41 at the merged record, the same two stale rows | |
| `acmp_mutants.py --jobs 2` (this lane's controls) | | rc 0, 1,248 s: 29 of 29 KILLED, four goldens PASS; every arm's verdict and failing count identical to the code head's run; AQ's coverage identical to the edge (71,258,305 edges, 8,270 arms, 28, 4,288), so PR #153 leaves the arm traffic as it was |
| `notify_mutants.py --jobs 1` (PR #153 changed it) | | rc 0, 1,142 s: 47 of 47 KILLED, goldens PASS; 47 of 47 at the merged README's record |

## 9. Parent consumers

### 9.1 The set of 17 at the code head

Scratch parent: clone of kebag-logic/milan-fpga detached at dev
`241f91845230ae410506dffb16b71937127fd175` (branch `234-area-baseline` fetched); submodules
`external` `efeb541a`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`,
`protocol-processor` (each `rev-parse --show-toplevel` checked before any git command in
it); the processor gitlink set in the index only (`git update-index --cacheinfo`); the three
patches applied with `git apply --check` then `git apply`; never committed or pushed.

| Patch | sha256 |
|---|---|
| `parent-adoption-c8-bbf704ec.patch` | `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c` |
| `parent-adoption-p2-p1-1269cdaf.patch` | `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84` |
| `parent-adoption-c10-1269cdaf.patch` | `55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9` |

GNU Make 4.3 (sha256 `2cc4089a...a81234f`) and the pinned Verilator 5.050 wrapper (sha256
`905795b9...e79e92f`) first on PATH. Processor at `9eebc61`.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every ratchet held (all 0) |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files, 4 of 4 consumer lists; processor 42/42 tops, 0 recorded |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports (1,759 at `main`), undocumented 111 <= 111 |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | within ratchets (72 <= 77 suites without a mutation arm) |
| 8 | `scripts/docs_check.py` | 0 | 0 findings, 187 md + 975 files |
| 9 | `scripts/xvlog_gate.py --check` (under the host lock) | 0 | 151 s: "PASS (3 finding(s) == ratchet; 0 hdl/, 3 pinned processors)": `KL_pp_originator.sv:194`, `KL_pp_rx_validator.sv:383`, and `main`'s `KL_aecp_notify` `pd_ix_w`; none in a file this lane touches |
| 10 | `sw/builder/test_builder.py` | 0 | Make 4.3: "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 11's mf48 tree; gate 1b's `MAKEFLAGS += -e` arm, which Make 4.3 cannot exercise), 1,237 s; as lane #232's record |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | legs 606, 606, 646 and 311 checks, 0 failures (316 s) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 (31 s) |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS, 0 FAIL; 4 render mutants caught; gmstep 6 of 6 (2,549 s) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | **2** | two-stream leg 65 checks, 0 failures; shipping leg 155 checks, **2 failures**: `T30 INTERNAL LAW: the fill at accept is the 8-event setpoint for every PDU got=227 exp=292` and `... every PDU's first event is inside the law band got=285 exp=292`; first-event delay 18,396..18,821 cycles = 8.830..9.034 ticks (177 s). Recorded against milan-fpga #643 (PR #648): with the processor at `main` the gate exits 2 too, its 48 result lines identical (9.2) |
| 16b | `python3 tdm8_render_mutants.py --leg-defects` (gate 16's last step, not reached after its failure) | 0 | 5 of 5 (425 s) |

The gates wrote `sw/builder/out/` and `configs/generated/{ltn_rom,ucode}.hex` into the
parent (gitignored); they were moved aside, not deleted, before the head export, which the
recipe requires to start without them.

### 9.2 Gate 16 with the processor at `main`

Between the head and base Vivado runs, with nothing else of this lane running, the parent's
processor was moved to `main` `5c71928a` and gate 16 run again: rc 2 (185 s), the same two
failures and figures; all 48 result lines (`[PASS]`, `[FAIL]`, `[i]` and the two tallies)
identical to the head's. The lane moves neither the boot timing nor the render law.

### 9.3 At the merges (the light gates; every heavy gate reads `hdl/`, which the first merge changes in comments only)

| | `b845d01` | `9e86991` |
|---|---|---|
| gates 1 to 8, 3b, 11 | all rc 0; port gate 1,759 ports | all rc 0; port gate 1,759 ports |

At `9e86991` the heavy gates were not re-run: `main`'s PR #153 is the #232 lane's change,
measured by that lane with these gates. Its record says gate 9 needs PR #153's xvlog finding
banked in the parent (`scripts/xvlog.budget`, 3 to 2) when the pin moves past it: an
adoption line of #232's, not of this lane.

## 10. Parent-visible list

- No port, parameter, register or behaviour change; the port gate counts 1,759 processor
  ports at `main` and at the head. No parent patch is needed by this lane.
- The gate's baseline should be re-recorded by the adoption that moves the pin past this
  lane (#638's round-7 rule; #639's acceptance asks it "in the same reviewed change", which
  lives in the parent, so this processor PR says "Relates to milan-fpga#639").
- Gate 16's two T30 checks fail at `main` and at the head identically: #643 (PR #648).

## 11. Findings outside the scope

- **The drop counter counts a clock, not an arm** (`protocol_processor_top.sv:3038`): when
  two faces overrun in the same clock, every face's increment reads the same old
  `arm_drop_r`, so the counter rises by one. The banner says "counts — never silent", and
  the operator guide's word 24 is "timer-arm drops". Kept as it is (a behaviour change is
  out of this lane); section AQ records the rule. From outside the top no face ever fills
  (4.3), so it is not observed on traffic.
- **Two `tb/adp_engine` records are stale at `main`**: `cfg-valid-no-reset` and
  `gate-enable-dropped-top` fail more checks than recorded on 2026-09-29, identically at
  `main` and the head.
- **#638's gate hashes sources from the parent tree at check time**, so a check run with the
  parent's processor at another revision digests the wrong sources (this lane's first head
  checks were re-run for that reason, 5.6).

## 12. Scratch evidence (outside the tree and this directory)

`$VALIDATION_STORAGE/pp639-a525/`: `work/lockstep_armq`, `work/lockstep_lsn` (benches,
extractors, controls, results), `work/viv` (module-level variant runs), `work/lsnctl`,
`work/aqctl` (control trials), `work/newtests-on-main` (AQ and RS on `main`'s RTL),
`camp/{head,base,merge,merge2}` (campaign logs and results), `pgates-{head,main,merge,merge2}`
(parent gate logs), `meas/{base,head}` (Vivado runs, `compare.json`, the scratch baseline
copy), `logs`, `head-logs`, `merge-logs`, `merge2-logs`, `mbin` (scripts).

Round 2: `r2/` (`r462/` the review packet's scripts as fetched; `tree-*`, `head-2ff8183`,
`suites-2ff8183`, `snap-2ff8183` exports; `runs/` the probe, mutant and red-proof runs;
`camp/` the campaign outputs; `v/` every round-2 log and rc file; `regen/` the bench
regeneration check; `forcetest/` the simulator's force/release trial; `bin/` scripts),
`pgates-r2/` and `pgates-r2-main/` (parent gate logs), `aside-gates-r2pre/` (the round-1
gate outputs moved out of the parent).

Round 2b: `r2b/` (`head-c725be1`, `suites-c725be1`, `snap-c725be1`, `pptop-c725be1`, the
exports of the merge; `pptop-1cba30c`, `pptop-b0a74196`, `snap-07b1469d`, `snap-1cba30c`,
`snap-b0a74196`, the two sides and the base; `aq-mainrtl`, this head's benches over
`b0a74196`'s `hdl/`; `td-aq-probe`, the scratch TD probe; `camp/`, the campaign outputs;
`v/`, every log, rc file and comparison diff; `bin/`, the scripts). Also `pgates-r2b/` (the
parent gate logs, the four per-revision port-gate logs among them) and `aside-gates-r2/`
(round 2's gate outputs, moved out of the parent).

## 13. Round 2 (test-only; R462-1 F1 and S1)

Assignment: milan-fpga #639 comment 5981052216. Review: R462-1 on processor PR #155
(comment 5981047114), NEGATIVE on one MINOR (F1: the arm-port rings' full-queue path has no
committed check), and S1; R463-1 POSITIVE. Continued on `pp639-armq-lsnrec` from `9e869910`
with one-line commits: no rebase, no amend, not pushed. REVIEW READY: milan-fpga #639
comment 5982661712. `main` is still `c050d971`, merged in
round 1, so item 4 needs no merge.

### 13.1 Items

| Item | State |
|---|---|
| 1. F1: a committed check that drives a face full, with the six required states; `write_refused` and `wr_wrap_hi` in `acmp_mutants.py`, KILLED by a named check, recorded in section AQ; 09 §8.8, README `:2009`/`:2028` and the `acmp_mutants.py:165-168` comment corrected | done (13.3 to 13.5) |
| 2. S1: name the source of "1,153 flops" (comment only) | done (13.3) |
| 3. Publish the lockstep benches, with digests | done: `lockstep/` in this directory (13.6) |
| 4. Merge `main` if it moved | not needed: `main` is `c050d971`, already in the head |

### 13.2 Commits

| Commit | Subject |
|---|---|
| `89b000c` | Drive the eight timer-arm faces from the bench through full queues, drops, saturation and resets in tb/pp_top section AQ (AQ3, AQ4) |
| `b1b6a5a` | Plant the review's four full-queue controls in acmp_mutants.py and name AQ3 for the five ring arms |
| `6b82f9b` | Record section AQ's drive and its nine controls, and stop pointing at the unpublished lockstep bench |
| `2ff8183` | Name the revisions behind the ring banner's shift-queue flop count |

Head `2ff8183ac3ae8b70462d4d6e702c31a00b76ea90`. No behaviour-changing HDL edit: the only
`hdl/` change is `2ff8183`, a comment.

### 13.3 Changes (file:line at `2ff8183`)

| File:line | Change |
|---|---|
| `tb/pp_top/pp_top_wrap.sv:496-507` | wrap-only inputs: `dbg_aq_drive_i` and, per face in drain order, valid, cancel, slot, owner, deadline (`dbg_aq_drv_*_i`). The top's port list is unchanged |
| `tb/pp_top/pp_top_wrap.sv:916-961` | `aq_drive`: on the rise of `dbg_aq_drive_i`, `force` on the eight faces' own nets (`u_dut.lstn_arm_*_w` ... `u_dut.ntfy_mon_arm_*_w`) and `force u_dut.u_timer.arm_valid_i = 0`. Nothing is released; the drive is a run's last stimulus |
| `tb/pp_top/sim_main.cpp:737-745` | `ArmQueueModel` coverage of the full-queue path: `onto[0..4]` (pushes by the arms the face held before the clock, so the write offset; 4 is the write onto the leaving head), `refused`, `multi` (two or more faces dropping), `held_sat` (a drop with the counter at 0xFFFF), `rst_queued`, `rst_offers` |
| `tb/pp_top/sim_main.cpp:750-806` | the model's `edge()` counts them; its rule is unchanged |
| `tb/pp_top/sim_main.cpp:13832-13897` | `drive_arm_faces`: `std::mt19937` seed 639. 256 blocks of 64 clocks at per-face rates (light {0, 8, 16, 32, 64}/256 or heavy {64, 128, 192, 224, 256}/256, as the draw falls), a reset of 1-4 clocks after every eighth block with arms still offered; heavy rates until the counter has held 0xFFFF through 4,096 dropping clocks (cap 2^18 clocks); a 2-clock reset with the faces full; 64 more blocks. Every arm's deadline is its serial number |
| `tb/pp_top/sim_main.cpp:13902-13944` | `run_arm_queue`: AQ1, AQ2 as before; then the drive, its coverage line `AQ drive:`, **AQ3** (port, valid and counter equal the model at every edge of the drive) and **AQ4** (the drive reached every state: offsets 0-3, the leaving-head write, two faces dropping, the held counter, a reset with arms queued, arms offered in reset) |
| `tb/pp_top/acmp_mutants.py:164-169` | the issue #639 comment: the drive, not an unpublished bench, grades the full-queue path |
| `tb/pp_top/acmp_mutants.py:175-180` | `RING_STORE`, `PUSH_OK`, `DROP_COUNT`, `AQ_DRIVE`, `AQ_BOTH` |
| `tb/pp_top/acmp_mutants.py:208-231` | the five ring arms now name AQ2 and AQ3; four new arms name AQ3: `armq_write_refused`, `armq_write_wrap_hi`, `armq_full_pop_refuses`, `armq_drop_skip_sat` (R462-1's `write_refused`, `wr_wrap_hi`, `full_pop_refuses`, `drop_skip_sat`; each planted top is byte-identical to the one `gen.py --mutant` plants, checked) |
| `tb/pp_top/README.md:944-952` | "What it proves": the drive |
| `tb/pp_top/README.md:1959-1963` | the ACMP controls paragraph: fourteen issue #639 controls, 33 KILLED |
| `tb/pp_top/README.md:2006-2072` | section AQ: the drive, AQ3, AQ4, its coverage table, the nine controls with counts; the two sentences that pointed at the lockstep bench are gone |
| `docs/architecture/09_verification.md:388-399` | §8.8: no pointer to the unpublished benches; every check named also passes on `main`'s RTL; the arm-port row names AQ2, AQ3, AQ4 and the nine arms |
| `hdl/top/protocol_processor_top.sv:3002-3007` | S1, comment only: "held 1,152 flops at the 1x1 shape at processor 5c71928a, this change's base (1,153 at 631eeb34, the figure of milan-fpga's #234 area baseline)". The #234 figure is combination A (dev `1269cdaf`, processor `631eeb34`) of `docs/findings/234_PP_SHADOW_AREA_BASELINE.md`; 1,152 is this lane's census at its base (section 5.5) |

### 13.3a Why the drive is built this way

- **In `tb/pp_top`, under `--arm-queue-only`.** R462-1's `aq_probe.sh` builds `gsi-build` and
  runs `--arm-queue-only`, so the check had to live in that binary for the probes, run
  unchanged, to fail. The assignment's second form (an AQ sub-section driving the faces
  directly against `ArmQueueModel`) does exactly that. The full default run grades it too.
- **`force` on the faces' own nets.** The model already reads the faces from those nets
  (`dbg_aq_vld_o`, `dbg_aq_arm_o`), so `ArmQueueModel`'s rule is untouched and the drive
  passes through the same face concatenation the engines use. Nothing in `hdl/` changes, and
  no port of the top changes.
- **The timer service's arm input held idle** (`force u_dut.u_timer.arm_valid_i = 0`). The
  drive's random arms never reach the timer, so no engine sees a spurious expiry. The force
  sits on the timer's own input port, and the registered arm port the taps read stays
  visible. A trial with the pinned simulator showed both (`r2/forcetest`), and AQ3 passing
  with 88,003 arms issued shows it in the real build.
- **No `release`.** In the same trial, a released net kept its forced value until its
  driver next changed. So the drive is a run's last stimulus and nothing is released. Both
  `run_arm_queue` callers (the full default run and `--arm-queue-only`) end with it.
- **Resets mid-drive** drop `rst_n` directly, for 1 to 4 clocks, with the faces still
  offering. `H::reset()` would re-initialise every input and idle 30 clocks. The harness's
  per-edge samplers only count; none checks during the drive (the run's
  check count rises by exactly AQ3 and AQ4: 1,653 -> 1,655 in `--arm-queue-only`).
- **AQ4 is model-only**, so it can only fail if the drive stops reaching a state. It guards
  AQ3 against a vacuous drive and adds no RTL dependence.

### 13.4 Tests and their controls

The drive at `2ff8183`, `--arm-queue-only` (the full default run prints the same drive
line; 13.7):

```
AQ drive: 90172 edges, 88003 arms issued; pushed onto a face holding 0, 1, 2, 3 and 4 arms (at 4 its head leaving): 18778, 48239, 3636, 5594, 12481; 352294 arms refused in 80719 drop clocks, 78930 of them with two or more faces dropping, 4096 with the counter held at 0xFFFF; 36 resets with arms queued, 366 arms offered in reset
AQ: 4 checks, 0 failures
```

Against R462-1's required outcome: counts 2 to 4 (pushes onto 1, 2, 3 arms: 48,239, 3,636,
5,594); a full queue popping and pushing in one clock, the leaving head overwritten
(12,481); refused pushes with their drops (352,294 in 80,719 clocks); two faces dropping in
one clock (78,930 clocks); counter saturation (4,096 clocks held at 0xFFFF); resets with
arms queued (36) and arms offered in reset (366).

**Passes on `main`'s RTL** (`c050d971`'s `hdl/`, the shift queue, with this head's
`tb/pp_top`): rc 0, AQ 4 of 4, the same two coverage lines to the digit (first on the
pre-commit tree; re-run at `2ff8183`, 13.5). So AQ3 and AQ4 grade behaviour the change
kept.

**The full default run** (`./obj_dir/Vpp_top_sim` of the `run_suites.sh` build at
`2ff8183`): rc 0, 693 s; traffic's line 71,290,136 edges, 8,280 arms, 28, 4,291, 0, 0, 0;
the drive's line identical to the one above; `AQ: 4 checks, 0 failures`; `[build default]
9935 checks, 0 failures`.

**The bar, R462-1's probes run unchanged** (`scripts/aq_probe.sh` from the review packet,
milan-fpga `pp639-review-evidence` `37608cc8`, `HEAD_TREE` = `hdl/`, `tb/common/` and
`tb/pp_top/` of a `git archive` of `2ff8183`):

| Probe | rc | Failing checks | AQ3 | Seconds |
|---|---:|---:|---|---:|
| `aq_probe.sh HEAD_TREE WORK write_refused` | 1 | 1 of 1,655 | FAIL: 8,272 of 90,172 edges differ | 326 |
| `aq_probe.sh HEAD_TREE WORK wr_wrap_hi` | 1 | 1 of 1,655 | FAIL: 19,343 of 90,172 edges differ | 348 |

At round 1's head the same two probes exit 0 (R462-1's receipts, and 13.4's red proof).

**Every `lockstep_armq/gen.py --mutant` control of R462-1**, its exact text planted in the
full top (its `MUTANTS` table read unchanged), `--arm-queue-only`. These ran on the
pre-commit tree, which differs from `2ff8183` only by the S1 comment and the line breaks of
one `printf`'s arguments; the campaign (13.5) then planted the same nine edits at
`2ff8183` with the same result, and `hd_not_reset` was re-run there (13.5):

| Control | rc | Failing checks | AQ2 (traffic) | AQ3 (the drive) |
|---|---:|---:|---|---|
| `write_refused` | 1 | 1 | pass | FAIL, 8,272 edges |
| `wr_wrap_hi` | 1 | 1 | pass | FAIL, 19,343 edges |
| `full_pop_refuses` | 1 | 1 | pass | FAIL, 61,730 edges |
| `drop_skip_sat` | 1 | 1 | pass | FAIL, 4,099 edges |
| `wr_at_head` | 1 | 3 | FAIL | FAIL, 59,652 edges |
| `wr_at_mid` | 1 | 3 | FAIL | FAIL, 65,779 edges |
| `head_stuck` | 1 | 3 | FAIL | FAIL, 68,820 edges |
| `read_tail` | 1 | 72 | FAIL | FAIL, 74,397 edges |
| `ring_of_three` | 1 | 12 | FAIL | FAIL, 36,176 edges |
| `hd_not_reset` (the review's equivalence probe) | 0 | 0 | pass | pass (equivalent, as expected) |

**Red proof** (the round-1 bench, `9e86991`'s `hdl/` and `tb/pp_top`, the same four
plants): `write_refused`, `wr_wrap_hi`, `full_pop_refuses`, `drop_skip_sat` each rc 0, AQ 2
of 2, 1,653 checks, 0 failures. Each now fails AQ3.

AQ4 reads only the model, which the forced faces feed: it cannot fail on an RTL defect,
only if the drive stops reaching a state, so it guards AQ3 against a vacuous drive.

### 13.5 Campaigns at `2ff8183`

Every driver whose build holds `protocol_processor_top.sv`, `KL_pp_acmp_listener.sv` or
`tb/pp_top` (the set of 8.1), from a `git archive` of `2ff8183`, each in the foreground of its
own job with its own log and rc file, never piped; pinned Verilator 5.050, GNU Make 4.3.
"Against round 1" compares every arm's failing-check count (the FAIL lines of its own log)
and verdict with round 1's run of the same driver: at the code head (8.1), or at the merge
that changed the driver (8.2) for `adp` (`b845d01`) and `notify` (`9e86991`).

| Campaign | rc | Seconds | Result | Against round 1 |
|---|---:|---:|---|---|
| `acmp_mutants.py --jobs 3` | 0 | 1,274 | 33 of 33 KILLED, four goldens PASS | the 24 arms outside the ring identical, verdict and every failing check; the five ring arms each add exactly AQ3 (`armq_read_tail` 71 -> 72, `armq_head_stuck` 2 -> 3, `armq_ring_of_three` 11 -> 12, `armq_write_at_head` 2 -> 3, `armq_write_at_mid` 2 -> 3); the four new arms fail AQ3 alone (1 each) |
| `notify_mutants.py --jobs 2` | 0 | 962 | 47 of 47 KILLED, goldens PASS | 53 of 53 arm logs identical to `9e86991`'s |
| `ctr_mutants.py --jobs 2` | 0 | 301 | control PASS, 17 KILLED (18 checks) | 18 of 18 identical |
| `aecp_mutants.py --jobs 2` | 0 | 931 | 60 checks: 5 controls PASS, 55 KILLED | 60 of 60 identical |
| `aecp_dispatch_mutants.py` | 0 | 436 | 44 checks: 4 controls PASS, 40 KILLED | 44 of 44 identical |
| `d3_mutants.py --jobs 2` | 0 | 6,334 | 110 of 110 KILLED, goldens PASS | 116 of 116 records identical in verdict and failing checks, once the undefined number in two `D3C3`/`D3C4` messages is ignored (13.11) |
| `gsi_mutants.py` | 0 | 578 | 20 detected by named checks; golden and restored PASS | 44 of 44 arm logs identical |
| `name_wr_mutant.py` | 0 | 78 | decode killed; golden and restored PASS | 6 of 6 identical |
| `tb/adp_engine/mutants.py --jobs 2` | 0 | 407 | 43 checks: 2 controls PASS, 41 KILLED | 43 of 43 identical to `b845d01`'s (the two stale README rows unchanged, 8.1) |
| `tb/maap/mutants.py --jobs 2` | 0 | 161 | 32 checks: 3 controls PASS, 29 KILLED | 32 of 32 identical |

The acmp campaign's per-arm counts are the ones `tb/pp_top/README.md` now records (section
AQ and the ACMP controls table); `tb/acmp_listener` and `tb/rx_validator` are unchanged.

**The bar re-run at `2ff8183` itself** (R462-1's `aq_probe.sh`, 13.4; the `main`-RTL run;
the equivalence probe):

| Run | rc | Seconds | Result |
|---|---:|---:|---|
| `aq_probe.sh ... write_refused` | 1 | 326 | AQ3 FAIL, 8,272 of 90,172 edges; 1 of 1,655 checks fail |
| `aq_probe.sh ... wr_wrap_hi` | 1 | 348 | AQ3 FAIL, 19,343 of 90,172 edges; 1 of 1,655 checks fail |
| `gen.py`'s `hd_not_reset` planted (a probe, expected equivalent) | 0 | 377 | AQ 4 of 4, 1,655 checks, 0 failures |
| this head's `tb/pp_top` on `main` `c050d971`'s `hdl/` | 0 | 291 | AQ 4 of 4, both coverage lines identical to the head's |

### 13.6 The lockstep benches, published

`lockstep/` in this directory: `README.md` (what each bench is, the revisions, the exact
regeneration and re-run steps, the results), `armq/` and `lsn/` (the benches as run, and
`results-head9eebc61/`, the run set HANDOFF 4.1 and 4.2 cite), `GENERATED.sha256` (digest
and size of each input the benches generate from processor sources: the two tops, the cut
blocks, the renamed listener and the planted copies, the ROM image; not published as tree
copies, each checked to regenerate byte for byte with the steps in the README) and
`SHA256SUMS` (every published file: 186 files, 146,103 bytes; none over 200 KB; no home
path in any).

| Manifest | sha256 |
|---|---|
| `lockstep/SHA256SUMS` | `bcebcc12f5a1764951f97e276d6a90b374b102df1a95931156664610cab4cced` |
| `lockstep/GENERATED.sha256` | `e3f357aaa6baf8ddf3b7f70da2a0e45a6c28a7821a006f52bcb1485bd3fb0a6f` |

Not published (tree copies or cuts; digest and size in `GENERATED.sha256`): `armq/top_main.sv`
(`5c71928a`'s top, `d49482e9...`, 236,713 bytes), `armq/top_head.sv` (`9eebc61`'s top,
byte-identical at `9e86991`, `ada29e74...`, 237,200 bytes), `armq/ref.sv`, `armq/dut.sv`,
seven `armq/ctl_*.sv`, `lsn/ref_listener.sv` (`7f6bed96...`), `lsn/dut_listener.sv`
(`f8bc590e...`), five `lsn/ctl_*.sv`, `lsn/ltn_rom.hex` (`23cc67ee...`). Earlier iterations of
the benches' result sets (`results-wt1`, `results-wt2`, `results-ctl2`) stay in scratch; the
record cites only `results-head9eebc61`.

### 13.7 Suites and static gates at `2ff8183`

| Command | rc | Result |
|---|---:|---|
| `./scripts/lint_hdl.sh` | 0 | 41 of 41, 14 s |
| `make check` (a git snapshot of the head's files) | 0 | 41 mermaid + 18 wavedrom blocks, 1,123 links, 115 REQ rows, 94 matrix rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 79 s, `YOSYS 42 tops, all.v parsed 1 time(s)`; `YOSYS OK KL_pp_acmp_listener`, `YOSYS OK protocol_processor_top` |
| `./scripts/run_suites.sh` | 0 | 1,121 s: 33 suites, 1,021,612 checks, 0 failing. Against `9e86991` (1,021,610) only `pp_top` moved, 10,418 -> 10,420 (AQ3, AQ4); `acmp_listener` 3,111 |
| the full default `tb/pp_top` binary of that build, run again for its AQ lines | 0 | 693 s; 13.4 |

### 13.8 Parent consumers at `2ff8183`

A parent-visible file changed: `hdl/top/protocol_processor_top.sv` (a comment), and
`tb/pp_top/` (the parent's port-contract gate inventories its hierarchical references;
`measure_test_evidence.py` names `acmp_mutants.py`; `check_cpp_idiom.py` scans processor
C++). So the set of 17 ran again. The scratch parent is the same as round 1's (9.1): dev
`241f9184` with the c8, p2-p1 and c10 patches, digests as recorded there and the patches
still applied. Its processor checkout and gitlink (in the index only) were moved to
`2ff8183`, with each `rev-parse --show-toplevel` checked first. The 36 build products the
round-1 gates left in the parent were moved aside to scratch, not deleted, so every bench
built fresh. GNU Make 4.3 and the pinned Verilator 5.050 were first on PATH.

| # | Command | rc | Seconds | Result |
|---:|---|---:|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | 1 | every ratchet held (all 0) |
| 2 | `scripts/check_py_idiom.py` | 0 | 4 | every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 2 | 108 files, 4 of 4 consumer lists; processor 42/42 tops, 0 recorded |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 3 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | 2 | protocol-processor 1,759 ports, undocumented 111 <= 111. The inventory reads 297 test-only hierarchical observations, against 256 at `9eebc61` and `9e86991`: these are the drive's 41 `force` targets. It is an inventory, not a ratchet |
| 6 | `scripts/measure_naming.py --check` | 0 | 1 | 95 recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 6 | within ratchets (72 <= 77 suites without a mutation arm), unchanged |
| 8 | `scripts/docs_check.py` | 0 | 8 | 0 findings, 187 md + 975 files |
| 9 | `scripts/xvlog_gate.py --check` (under the host lock) | **1** | 148 | `BANK IT [submodules]: protocol-processor:hdl/aecp/KL_aecp_notify.sv\|VRFC 10-3380\|pd_ix_w no longer occurs`; 2 findings (originator, rx_validator). PR #153 (`main` `c050d971`, merged at `9e86991`) removed the `pd_ix_w` finding, and the parent's `scripts/xvlog.budget` still lists it. With the parent's processor at `main` `c050d971` the gate gives rc 1 (144 s) and output identical apart from the pin. It is the adoption's banking step (#232's line, R462-1's pending duties), not this lane's |
| 10 | `sw/builder/test_builder.py` | 0 | 1,174 | "ALL GATES PASS EXCEPT 2 NOT RUN" (gate 11's mf48 tree; gate 1b's `MAKEFLAGS += -e` arm), as round 1 |
| 11 | `scripts/lint_rtl.py --check` | 0 | 15 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 288 | legs 606, 606, 646 and 311 checks, 0 failures |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 30 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` (alone) | 0 | 2,722 | 9 benches RESULT: PASS, 0 FAIL; 4 render mutants caught; gmstep 6 of 6. All 1,150 verdict lines (`[PASS]`, `[FAIL]`, `RESULT:` and tallies) identical to round 1's |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | **2** | 211 | two-stream leg 65 checks, 0 failures; shipping leg 155 checks, 2 failures: #643's two T30 INTERNAL LAW checks (first-event delay 18,396..18,821 cycles = 8.830..9.034 ticks). Every `[PASS]`, `[FAIL]`, `[i]` and tally line is identical to round 1's run at `9eebc61`, which matched `main` line for line (9.2) |
| 16b | `python3 tdm8_render_mutants.py --leg-defects` | 0 | 452 | 5 of 5 |

Summary: 15 of 17 rc 0, and 16b rc 0. Gate 16 fails #643's two T30 checks exactly as in
round 1 and on `main`. Gate 9 fails only on banking PR #153's removed finding, exactly as
with the processor at `main` `c050d971`. Neither failure is this lane's. Round 1 ran gate 9
at `9eebc61`, before PR #153 was merged, so it passed then. No OOM kill in the unit
through round 2 (`memory.events` `oom_kill 0`).

### 13.9 Parent-visible list (round 2)

- Still no port, parameter, register or behaviour change (the port gate counts 1,759
  processor ports). No parent patch is needed.
- `hdl/` changes by one comment, so synthesis and the Vivado figures of section 5 are
  unchanged and no Vivado run was made. The resource gate's input digests do change, and
  the adoption's re-baseline measures its own pin anyway (#639's acceptance, section 10).
- The parent's port-contract inventory: 297 test-only hierarchical observations, up from
  256 (the drive's 41 `force` targets). It is not a ratchet.
- Gate 9 at this head (and at `main` `c050d971`) asks to bank PR #153's removed `pd_ix_w`
  finding in `scripts/xvlog.budget` (3 to 2): the adoption's step past `c050d971`.
- Gate 16's two T30 checks: #643, unchanged.

### 13.10 Limits

- The drive runs at the suite's one shape (1x1: slot width 6, 47-bit arms). The ring's index
  arithmetic does not depend on the width; widths 5, 7 (8x8) and 8 rest on the lockstep
  bench (4.1, published in 13.6).
- The drive is one fixed seed (`std::mt19937`, 639), so the run is reproducible. Its reach
  is printed and held by AQ4, and R462-1's lockstep (32 seeds x 1,000,000 cycles) is the
  wide random search.
- Vivado was not re-run (no RTL change).
- No hardware was used.

### 13.11 Findings outside the scope (round 2)

- **`tb/pp_top/d3_phases.hpp:2963` and `:2993`** (since `a1f5cd5`, on `main`): the D3C3 and
  D3C4 messages end "... blank %u of %d)" with no argument for the `%d`. The build's two
  `-Wformat` warnings point at them. The checks' conditions are unaffected; only the
  printed last number is undefined, and it differs from run to run (9 of d3's 116 records
  differ from round 1 only there). Left as it is: not this lane's code.

## 14. Round 2b (merge only: `main` `b0a74196`, PR #157)

Assignment: milan-fpga #639 comment 5983576287. REVIEW READY: comment 5984636752.
R462-2 and R463-2 are POSITIVE at
`1cba30c9` (the manager's merge of round 2's `2ff8183` with `main` `07b1469d`, PR #154,
pushed as processor PR #155). `main` then moved to `b0a74196` (PR #157, #81/#84).

### 14.1 The merge

- `c725be12d7ea6bf96f1b64e3a56416f0d4defd6c` = `git merge --no-ff b0a74196` on `1cba30c9`,
  parents `1cba30c9` and `b0a74196`. Its tree `0bb7199a3caf38df44071cac4e2d56fef89f1b7c` is
  `git merge-tree --write-tree 1cba30c b0a74196`'s, rc 0: nothing hand-merged. Subject:
  "Merge processor main b0a74196 (PR #157) into the issue #639 lane" (one line, no body).
- `git diff --check b0a74196 HEAD` and `git diff --check 1cba30c HEAD`: rc 0.
- Each side's change reaches the merge unchanged. `git diff 1cba30c c725be1` equals
  `git diff 07b1469d b0a74196` (PR #157's change), and `git diff b0a74196 c725be1` equals
  `git diff 07b1469d 1cba30c` (this lane's), by `git patch-id --stable` for `hdl/` and
  `docs/`. For `tb/`, the changed lines (`-U0`) are identical both ways. Only two files'
  patch-ids differ, `tb/pp_top/sim_main.cpp` and `tb/pp_top/README.md`, where a hunk of one
  side sits within three lines of the other's, so its context lines differ.
- This lane's RTL is byte-identical to `1cba30c`'s. `KL_pp_acmp_listener.sv` sha256
  `f8bc590e...` at both. In `protocol_processor_top.sv` the merge adds PR #157's one
  hunk (the GET_DYNAMIC_INFO classifier and its banner, `:1539-1554`, `:1645-1646`) and
  nothing else. No file needed a hand resolution.

### 14.2 Where the two sides meet (the semantic check)

| Shared file | PR #157 | This lane | Interaction |
|---|---|---|---|
| `hdl/top/protocol_processor_top.sv` | GET_DYNAMIC_INFO presents `MAP_CFG` at the scoreboard classifier (`:1645-1646`) | the arm-port block with its rings (`:2935-3060` at the merge) | Disjoint logic: the classifier feeds the scoreboard, and the rings feed the timer service. No signal is shared |
| `tb/pp_top/pp_top_wrap.sv` | `ifndef PP_TOP_TIM_DEFAULTS` around the two 400 ms overrides (`:573-581`) | the AQ taps, the drive's wrap-only inputs and the drive (`:494-510`, `:897-967`) | Disjoint |
| `tb/pp_top/sim_main.cpp` | HZ8's batch check and HZ13, run inside `run_hazards`; the sixth build's `#elif PP_TOP_TIM_DEFAULTS` branch in `main` | `ArmQueueModel` in `H::step`; `run_arm_queue` last in the first build's `#else` branch | The drive is still the first build's last stimulus. HZ8 and HZ13 run inside `run_hazards`, before `run_arm_queue`. The sixth build never runs AQ, so its unreleased `force` cannot reach TD |
| `tb/pp_top/README.md`, 08, 09 | sections TD and HZ, the six-build tables, the AECP record, 08 F08.1 rows and §6, 09 §3 TIM, §8.3 | section AQ, the ACMP record, 08 §3, 09 §8.8 | 14.6 |

**The one real meeting point: TD runs over the rings.** The two timers TD grades
(`T-LOCK-UNLOCK`, `T-NOTIF-TIMELIMITED`) belong to `KL_aecp_notify`
(`LOCK_TIMEOUT_MS_P`, `TL_TIMEOUT_MS_P`). Each is armed through the notification face,
which is now a ring in distributed RAM. So TD in the merged sixth build exercises PR #157's
check over this lane's storage. It passes with the same measurements PR #157 recorded on
the shift queue: the auto-unlock 60,003 ms after the LOCK_ENTITY, the TIME_LIMITED expiry
300,002 ms after the REGISTER, and 6 monitor probes answered. TD's harness
(`NotifyBench::io`) steps its own `ArmQueueModel` at every edge but never grades it. A
scratch probe printed that model's tally after TD (14.4).

No test depends on the other side's behaviour. HZ never reads the arm port. AQ's traffic
coverage comes from the main harness, which HZ (a fresh processor of its own) does not
drive: the full default run's AQ traffic line is identical to round 2's.

### 14.3 Suites and static gates at `c725be1`

| Command | rc | Seconds | Result | The two sides |
|---|---:|---:|---|---|
| `./scripts/run_suites.sh` | 0 | 2,234 | 33 suites, 1,021,627 checks, 0 failing | `1cba30c9` (the manager's receipt): 1,021,612. Only `pp_top` moved, 10,420 -> 10,435, by PR #157's +15 (HZ +12, TD +3). PR #157's own record is +15 in both of its rounds. Every other suite equals `1cba30c9`'s line for line (`acmp_listener` 3,111) |
| `make -C tb/pp_top` (all six builds, its own log) | 0 | 1,423 | 10,435 checks: default 9,947, fixture 20, identify 178, line 231, timebase 56, defaults 3 | 14.4 |
| `./scripts/lint_hdl.sh` | 0 | 36 | 41 of 41 | |
| `make check` | 0 | 70 | 41 mermaid + 18 wavedrom blocks; 1,136 links; 115 REQ rows; 94 matrix rows, 0 untested; 28 parameters | links 1,136 = base `07b1469d` 1,131 + this lane's 3 (`1cba30c`: 1,134) + PR #157's 2 (`b0a74196`: 1,133). Each run rc 0 |
| `python3 scripts/gen_matrix.py --check` | 0 | 0 | 94 rows, 0 untested | |
| `./syn/yosys/run.sh` | 0 | 157 | `YOSYS 42 tops, all.v parsed 1 time(s)`; `YOSYS OK` for `KL_pp_acmp_listener` and `protocol_processor_top`; `YOSYS XILINX OK KL_aecp_engine` | |

### 14.4 `tb/pp_top` against each side, section by section

`make -C tb/pp_top` ran at the merge and at both parents, each from its own `git archive`
with its own log. These are the run-output lines, with the compiler and Verilator warning
lines left out. The warnings differ only in line numbers.

| Comparison | Lines that differ |
|---|---|
| merge against `main` `b0a74196` (rc 0, 1,239 s, 10,431 checks) | Only this lane's: the three AQ lines and the totals (default 9,943 -> 9,947, the tally 10,431 -> 10,435). Every other line is identical, TD's measurement line and TB's histogram included |
| merge against `1cba30c` (rc 0, 770 s, 10,420 checks) | Only PR #157's: `HZ: 177` -> `189`, default 9,935 -> 9,947, the sixth build (`[TD] auto-unlock 60003 ms ..., expiry 300002 ms ..., 6 monitor probes answered`, `TD: 3 checks`), and the tally 10,420 -> 10,435. AQ's three lines are identical |

AQ at the merge, in the full default run: traffic 71,290,136 edges, 8,280 arms, 28, 4,291,
then 0, 0, 0. The drive line is the README's to the digit (90,172 edges, 88,003 arms, ...;
`AQ: 4 checks, 0 failures`). Both lines equal round 2's full default run (13.4).

**AQ on `main` `b0a74196`'s RTL** (this head's `tb/pp_top` over `b0a74196`'s `hdl/`,
`gsi-build`, `--arm-queue-only`): rc 0, 456 s, AQ 4 of 4, 1,655 checks, 0 failures. Both
coverage lines equal the README's (71,258,305 edges, 8,270 arms, 28, 4,288; the drive as
above). So 09 §8.8's "each also passes on `main`'s RTL" still holds at the new `main`.

**The scratch TD probe** (not committed: one `printf` of `io.aq`'s tally after TD, in a
scratch copy of `c725be1`, `make timer-defaults`): rc 0, 109 s. `[TD] auto-unlock 60003 ms
..., TIME_LIMITED expiry 300002 ms ..., 6 monitor probes answered`; `[TD-AQ probe] the TD
harness's arm-port model: 30003382 edges, 3456 arms issued, 0 edges differing`; `TD: 3
checks, 0 failures`. So every arm the sixth build's engines offered, the two long timers'
among them, left the rings exactly as the eight-FIFO model of the shift queue's contract
says.

### 14.5 Campaigns at `c725be1`

Every driver whose build holds `protocol_processor_top.sv`, `KL_pp_acmp_listener.sv` or
`tb/pp_top`, as in 13.5: the four the assignment names and the six others. Each ran from a
`git archive` of `c725be1`, in its own job with its own log and rc file, never piped, with
`--jobs` where the driver has it. Pinned Verilator 5.050, GNU Make 4.3. "Against round 2"
compares each log with round 2's run at `2ff8183` (13.5), paths normalized and lines sorted
(print order varies with `--jobs`). For acmp it also compares every arm's own log (its FAIL,
AQ and tally lines, not the compiler's) and `results.json` keyed by arm.

| Campaign | rc | Seconds | Result | Against round 2, and the record |
|---|---:|---:|---|---|
| `acmp_mutants.py --jobs 3` | 0 | 2,149 | 33 of 33 KILLED, four goldens PASS | Summary identical (38 of 38 lines). All 37 arm logs identical in every FAIL, AQ and tally line, and `results.json` identical arm by arm. These are the counts `tb/pp_top/README.md` records (section AQ, the ACMP table) |
| `aecp_mutants.py --jobs 2` | 0 | 1,731 | 67 checks: 6 controls PASS, 61 KILLED | Exactly PR #157's change and nothing else: the `timer-defaults` control; six new arms, `td-lock-default-59s` 1, `td-tl-default-301s` 1, `hz-gdi-key-none`, `-held`, `-no-stream` 7 each, `hz-gdi-as-barrier` 2; and three moved counts, `hz-stub-restored` 74 -> 81, `hz-acmp-reads-as-steps` 26 -> 27, `hz-barrier-no-priority` 127 -> 139. Every count is the merged README's (PR #157's record). Every other arm's FAIL lines are identical to round 2's |
| `notify_mutants.py --jobs 2` | 0 | 1,365 | 47 of 47 KILLED, goldens PASS | identical (54 of 54 lines) |
| `d3_mutants.py --jobs 2` | 0 | 6,900 | 110 of 110 KILLED, goldens PASS | summary identical (117 of 117 lines); 116 of 116 records in `results.json` identical in verdict, named checks and failing checks once the undefined number of the D3C3/D3C4 messages is ignored (9 records differ only there, as in round 2, 13.11) |
| `ctr_mutants.py --jobs 2` | 0 | 289 | control PASS, 17 KILLED (18 checks) | identical (112 of 112 lines) |
| `aecp_dispatch_mutants.py` | 0 | 536 | 44 checks: 4 controls PASS, 40 KILLED | identical but for the undefined `%d` of two D3C3 and one D3C4 message (13.11) |
| `gsi_mutants.py` | 0 | 772 | 20 detected by named checks; golden and restored PASS | identical (23 of 23 lines) |
| `name_wr_mutant.py` | 0 | 130 | decode killed; golden and restored PASS | identical |
| `tb/adp_engine/mutants.py --jobs 2` | 0 | 573 | 43 checks: 2 controls PASS, 41 KILLED | identical (366 of 366 lines) |
| `tb/maap/mutants.py --jobs 2` | 0 | 243 | 32 checks: 3 controls PASS, 29 KILLED | identical (101 of 101 lines) |

### 14.6 The two sides' docs (item 3)

Each pair was read at the merge for a claim one side makes that the other's change falsifies.
None was found, so no doc commit was needed.

| Place | PR #157 | This lane | Agreement |
|---|---|---|---|
| 08 §2 F08.1 | T-IDENT-BURST and T-IDENT-REARM marked landed; T-CTR-OBSERVE integrator-owned. The T-NOTIF-TIMELIMITED (300 s, registry) and T-LOCK-UNLOCK (60 s, lock mgr) rows are unchanged | none | Agree. Both rows' timers are armed through the arm port that 08 §3's bullet describes |
| 08 §3 | none (§6 adds GET_DYNAMIC_INFO to the MAP_CFG cross-lock holds) | the arm-port bullet: one port, four-deep per-face rings, fixed drain priority, overrun dropped and counted | Agree. TD's 60,000 and 300,000 ms deadlines ride that port, and TD passes on the rings with PR #157's measurements |
| 09 §3 TIM | "every F08.1 row this processor implements (T-CTR-OBSERVE is integrator-owned)" | none | Agree |
| 09 §8.3 | the TD1/TD2 row; HZ1 (GET_DYNAMIC_INFO as MAP_CFG), HZ8's over-serialization, HZ13; TD runs in the sixth build | none | Agree. §8.3 names no arm-port property |
| 09 §8.8 | none | the rings' checks AQ2 to AQ4 "over every section the full default run drives on it", and "each also passes on `main`'s RTL" | Agree. TD runs in the sixth build, not the full default run. The `main`-RTL claim was re-proved at `b0a74196` (14.4) |
| `tb/pp_top/README.md` TD (`:894-912`), HZ (`:913-969`) | TD on "a fresh processor of its own in the sixth build"; HZ8's batch "runs after HZ12, so every earlier arm keeps its clock"; HZ13 | none | Agree with AQ. AQ grades the main harness of the first build, and the drive stays that build's last stimulus |
| `tb/pp_top/README.md` AQ (`:2022-2112`), "What it proves" (`:970-978`) | none | the model "in `H::step`" in every harness, graded in the full default run; the coverage figures; the nine controls | Agree. The sixth build's harness steps the model ungraded, as the third to fifth builds' do. Every figure re-measured equal (14.4, 14.5) |
| `tb/pp_top/README.md` build tables (`:20-22`, `:1818-1825`, `:2237-2244`) | six builds | none | Agree. AQ is in the first build |
| `tb/pp_top/README.md` AECP record (`:1189-1270`) and ACMP record (`:1988-2020`) | the AECP record re-run in full, 6 controls and 61 arms | the ACMP record, 33 arms | Both re-measured equal at the merge (14.5) |

### 14.7 Area (item 4)

A merge changes no synthesized logic of either side. The merged `hdl/` is this lane's
`hdl/` plus PR #157's one classifier hunk (14.1), which PR #157 measured itself. So this
lane's Vivado figures (section 5) are unchanged by the merge, and no Vivado run was made.

### 14.8 Parent consumers at `c725be1`

Scratch parent: the same clone as before (9.1), moved to milan-fpga dev
`6c22d3cad7c8c24ed3f0c5eab535922a3428c8d5`. Round 2's 45 ignored build products were moved
aside to scratch (`aside-gates-r2/`), not deleted. The three patches were reversed with
`git apply -R --check` then `git apply -R`, and the index reset. The clone was then detached
at `6c22d3ca`; `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e` and
`external` `efeb541a` are its pins, unchanged. Each submodule's `rev-parse --show-toplevel`
was checked first. The processor checkout was moved to `c725be1`, and its gitlink set in the
index only (`git update-index --cacheinfo`). The four patches were applied in order with
`git apply --check` then `git apply`. Nothing was committed or pushed.

| Patch | sha256 |
|---|---|
| `parent-adoption-c8-bbf704ec.patch` | `3340d2e8e389a52c49c32611c6eb36f55bef4534d30ecafbecad25b9a1b38a4c` |
| `parent-adoption-p2-p1-1269cdaf.patch` | `d3034e89dba34862a0c8534472043212fd1f56412a90397997dcce3441613d84` |
| `parent-adoption-c10-1269cdaf.patch` | `55e62329f52e352bdd56b6d37bf2877aa952063f43221bb3f1d8583274ea34b9` |
| `parent-adoption-232-241f9184.patch` (#232's, as PR #157's body records) | `88ee5e9643a453f8c31dc76e5f8d57e8deec89bcbbf9d4a4a8ca005757b72560` |

GNU Make 4.3 and the pinned Verilator 5.050 were first on PATH. "Against `1cba30c9`" compares
each log with the manager's consumer run at `1cba30c9`, which used the same dev and the same
four patches (`pp639-manager-1cba30c9/parent-consumer`), with paths normalized.

| # | Command | rc | Seconds | Result | Against `1cba30c9` |
|---:|---|---:|---:|---|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | 1 | every count 0 <= 0 | identical |
| 2 | `scripts/check_py_idiom.py` | 0 | 5 | every ratchet held; 312 modules, 198,382 lines | +21 lines: PR #157's arms in `aecp_mutants.py`, as its body records |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 1 | 108 files, 4 of 4 lists; processor 42/42 tops, 0 recorded | identical |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 4 | 50 of 50 | identical |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 0 | 46 tracked sources derived, self-test passed | identical |
| 5 | `scripts/check_port_contracts.py` | 0 | 3 | 1,759 processor ports, 111 <= 111 undocumented; 317 test-only hierarchical observations | identical. Run with the processor at each revision: base `07b1469d` 230, `1cba30c9` 317, `b0a74196` 230, `c725be1` 317, 1,759 ports at each. The +87 is this lane's `u_dut.` references in `tb/pp_top/*.sv` (111 -> 198: round 1's 46 AQ taps and round 2's 41 `force` targets); PR #157 adds none. Dev `6c22d3ca`'s gate counts each reference, so it reads +87 where dev `241f9184`'s read +41 for round 2 (13.8). It is an inventory, not a ratchet |
| 6 | `scripts/measure_naming.py --check` | 0 | 0 | 95 recorded | identical |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | 7 | 72 <= 77, 10 <= 10, 0 <= 0, 3 <= 3 | identical |
| 8 | `scripts/docs_check.py` | 0 | 6 | 0 findings across 188 md + 984 files | identical |
| 9 | `scripts/xvlog_gate.py --check` (under the host lock) | 0 | 150 | `PASS (2 finding(s) == ratchet; 0 hdl/, 2 pinned processors)`: `KL_pp_originator.sv:194`, `KL_pp_rx_validator.sv:383`. #232's patch banks PR #153's `pd_ix_w` | identical but the pin line |
| 10 | `sw/builder/test_builder.py` | 0 | 1,226 | "ALL GATES PASS EXCEPT 2 NOT RUN": gate 11's mf48 tree, and gate 1b's `MAKEFLAGS += -e` arm, which GNU Make 4.3 cannot exercise (as in rounds 1 and 2) | the manager's run, under its own tool path, lists only gate 11 as not run. The difference is the make version |
| 11 | `scripts/lint_rtl.py --check` | 0 | 8 | 90 <= 90 | identical |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 295 | legs 606, 606, 646 and 311 checks, 0 failures | the same four legs and counts. The log interleaves `-j8` compiler output with run lines, so it is not compared line by line |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | 0 | | identical |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 32 | 315 of 315, `RESULT: PASS` | identical |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 2,625 | 9 benches `RESULT: PASS`, 0 FAIL; 4 render mutants caught; gmstep 104 checks, 0 failures, and its controls 6 of 6 (run beside the d3 campaign) | every verdict line identical (1,174 of 1,174); this log adds two build lines (a Verilator command, and `[INFO]` that the gmstep control was rebuilt in the fresh tree) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 797 | two-stream leg 65 checks, shipping leg 245 checks, 0 failures; its recipe's leg-defect step 5 of 5. Dev `6c22d3ca` carries #643's fix, so the two T30 failures of rounds 1 and 2 (dev `241f9184`) are gone | all 109 verdict lines (`[PASS]`, `[FAIL]`, `[i]`, tallies, `RESULT:`) identical |
| 16b | `python3 tdm8_render_mutants.py --leg-defects` | 0 | 449 | 5 of 5 | as gate 16's own step |
| 17 | `scripts/check_sh_idiom.py` (PR #157's seventeenth) | 0 | 1 | every count held | |

Summary: 17 of 17 rc 0, plus 16b and PR #157's `check_sh_idiom.py`. Every result equals the
manager's `1cba30c9` run on the same parent, with three exceptions: py-idiom's +21 lines
(PR #157's arms), the xvlog pin line, and the builder's not-run ledger, where GNU Make 4.3
adds gate 1b's arm. So the merge adds nothing parent-visible beyond PR #157's own
change. The 45 round-2 build products stay aside in `aside-gates-r2/`. This round's gates
left their outputs in the scratch parent, which is gitignored and not part of any tree. No
OOM kill in the unit (`memory.events` `oom_kill 0`).

### 14.9 Limits

- No Vivado run (item 4).
- The TD probe is a scratch measurement, not a committed check. Grading the model on TD's
  harness would be a test change, which a merge round does not make.
- No hardware was used.

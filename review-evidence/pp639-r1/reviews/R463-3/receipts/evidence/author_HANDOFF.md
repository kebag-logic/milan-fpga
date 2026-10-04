# [A525] HANDOFF — milan-fpga #639 (epic #229 levers 3 and 6)

Status: REVIEW READY. Both levers done, cycle-exact, no port, parameter or register
change; validated; `main` merged twice as it moved. Head
`9e8699105c126db7764820916a827ef0538bc4b2` on local branch `pp639-armq-lsnrec`, not pushed;
`main` is still `c050d971` at the head's writing.

- Processor repository: Mister-M-alt/protocol-processor-control-plane-avb-milan
  (`git remote get-url origin` checked); HEAD at start `5c71928ad2bf1a854a5538d69b77214dfdf1697f`.
- Branch `pp639-armq-lsnrec` from `main` `5c71928a`.
- Assignment: kebag-logic/milan-fpga#639 comment 5976100204. TAKEN: comment 5976102877.
  REVIEW READY: comment 5980139653.
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

### 4.1 Lockstep, the arm-port block (scratch, not committed)

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

### 4.2 Lockstep, the listener (scratch, not committed)

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
edges, 8,280 arms, the same zeros. From outside the top no face ever holds two arms, so the
full-queue path is the lockstep bench's. **Red proof that AQ describes unchanged
behaviour:** the head's `tb/pp_top` built against `main`'s RTL passes AQ with the same
coverage to the edge (71,258,305 edges, 8,270 arms, 28, 4,288).

| Control (`acmp_mutants.py`, `--arm-queue-only`) | Named check | Verdict | Failing checks in the run |
|---|---|---|---:|
| `armq_read_tail` | AQ2 | KILLED | 71 |
| `armq_head_stuck` | AQ2 | KILLED | 2 |
| `armq_ring_of_three` | AQ2 | KILLED | 11 |
| `armq_write_at_head` | AQ2 | KILLED | 2 |
| `armq_write_at_mid` | AQ2 | KILLED | 2 |
| `write_refused` (not shipped) | AQ2 | survives at the top (no face fills); the lockstep bench kills it | 0 |

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

# [A523] HANDOFF: milan-fpga #230 (SRP area lane, epic #229)

**Round 2: REVIEW READY at head `1199255bee820eb46c24fe5d0cbf7f043c828a3c`** (section "Round 2", at the end). Round 1's
text below is kept as written, with two exceptions: section 4.2's control count is corrected in place (R458-1 F3), and
section 6's question was ruled (b) (milan-fpga#230 comment 5977836860: the parallel evaluation is final for #230).

Status: STOP on lever 4's shared evaluator only (section 6: sharing the per-stream evaluation needs a timing change and
a decoder port change; a ruling is asked). Everything else in the assignment is done and validated at head `65324390`:
lever 2, lever 4's storage part, the per-block measurements, the storage inventory, the inactive-slot check, the
marginal cost per talker and listener, the lockstep bench with its controls, the Vivado before/after, every processor
suite and campaign, and the parent consumer set. No port, parameter, register or behaviour change; no parent patch.

- Executor: [A523]. Reviewers: [R458] (internal), [R459] (external).
- Assignment: kebag-logic/milan-fpga#230 comment 5974045353 (epic #229; baseline PR #638 at `68d26ea0`).
- Processor repository: Mister-M-alt/protocol-processor-control-plane-avb-milan (`git remote get-url origin` checked).
- Branch `pp230-srp-area`, base processor `main` `c4cb84ff8cecad19bedaa85dde594a8ed68012f6` (HEAD checked at start).
- Commits (one-line subjects, no body, no trailer, not pushed):
  - `25847d07` SRP storage for issue #230: timer-arm FIFOs, walk records and admission slopes in distributed RAM
  - `65324390` Record the SRP storage map and per-stream cost for issue #230 in 10 section 5.1
- TAKEN: kebag-logic/milan-fpga#230 comment 5974057432.
- STOP (lever 4's shared evaluator ruling asked; the rest done at this head): kebag-logic/milan-fpga#230 comment 5977826098.

## 1. Outcome in one table

| | Lever 2: SRP timer-arm FIFOs (`KL_srp_top.sv:947` at base) | Lever 4: SRP per-stream evaluation |
|---|---|---|
| Done | yes: one distributed-RAM memory per FIFO, cycle-exact | storage part yes (walk records and slopes in distributed RAM, cycle-exact); the shared evaluator no: STOP item (section 6) |
| Flip-flops (census) | `tf_ram_r` 2,304 -> 0 at 1x1, 2,688 -> 0 at 8x8 | walk fields and slopes 168 -> 0 at 1x1, 756 -> 0 at 8x8 |
| Standalone 1x1, sub-blocks | top glue 907 -> 354 LUT, 2,836 -> 545 FF | talker, listener, admission: -37 LUT, -168 FF |
| Standalone 8x8, sub-blocks | top glue 1,053 -> 297 LUT, 3,387 -> 703 FF | talker, listener, admission: -791 LUT, -762 FF |

| Endpoint (whole) | Base | Head | Head - base |
|---|---|---|---|
| Integrated route 1x1 | 51,434 LUT, 59,691 FF, 15,847 slices, 79/27 BRAM, 14 DSP, WNS/WHS +0.079/+0.014 | 51,005 LUT, 57,262 FF, 15,837 slices, 79/27, 14, +0.354/+0.036 | -429 LUT, -2,429 FF, +0.275 ns WNS |
| Standalone 1x1 | 24,930 LUT, 25,465 FF | 24,258 LUT, 23,130 FF | -672 LUT, -2,335 FF |
| Standalone 8x8 | 32,584 LUT, 34,211 FF | 31,109 LUT, 30,648 FF | -1,475 LUT, -3,563 FF |
| `u_srp` route / 1x1 / 8x8 | 4,340 / 4,558 / 8,705 LUT; 6,263 / 6,438 / 11,192 FF | 3,711 / 3,988 / 7,313 LUT; 3,839 / 3,979 / 7,747 FF | -629 / -570 / -1,392 LUT; -2,424 / -2,459 / -3,445 FF |
| SRP cost per added stream context (standalone) | 592 LUT, 679 FF | 475 LUT, 538 FF | -117 LUT, -141 FF |

## 2. Changes (file:line at `25847d07`)

| File:line | Change |
|---|---|
| `hdl/srp/KL_srp_top.sv:947-954` | the timer-arm FIFO storage: two one-dimensional memories `tf_tk_ram_r`, `tf_ls_ram_r` (each one write and one read port) with `ram_style = "distributed"`, replacing base `tf_ram_r [0:1][0:31]` (`:947`); comment on why and on the missing reset |
| `hdl/srp/KL_srp_top.sv:966-984` | `tf_tk_write`, `tf_ls_write` (one process per memory, base `tf_write` `:959-968`); `tf_read` reads each memory into the unchanged `tf_q_r` heads |
| `hdl/srp/KL_srp_talker_fsm.sv:56-67` | banner Decision: the matcher's copy stays in flops; the walk's copy is distributed RAM |
| `hdl/srp/KL_srp_talker_fsm.sv:352-372` | record declarations: `mfs_r`, `mif_r`, `prio_r`, `rank_r`, `lat_r` removed; `wtsp_r` (68 bits per source, distributed RAM) |
| `hdl/srp/KL_srp_talker_fsm.sv:495-518` | `gate_open_acc_w`; `walk_tspec_write`; `g_wid_ram` (from 3 sources: `wid_r`, 124 bits per source, distributed RAM, written by the gate open) or `g_wid_flops` (1 and 2 sources: the matcher's `sid_r`/`da_r`/`vid_r` at the walk source) |
| `hdl/srp/KL_srp_talker_fsm.sv:520-531` | `walk_msg` assembles the FirstValue from `wid_w` and `wtsp_w` (same layout) |
| base `KL_srp_talker_fsm.sv:507-511`, `:559-563` | removed: the reset and gate-open capture of the five walk-only fields |
| `hdl/srp/KL_srp_listener_fsm.sv:54-61` | banner Decision, as for the talker |
| `hdl/srp/KL_srp_listener_fsm.sv:534-558` | `g_wsid_ram` (from 3 sinks: `wsid_r`, distributed RAM, written by the A15 settle) or `g_wsid_flops` (the matcher's `sid_r`); `walk_msg` reads `wsid_w` |
| `hdl/srp/KL_srp_admission.sv:111-115` | `slope_q_r` as an unpacked array with `ram_style = "distributed"`, no reset |
| `hdl/srp/KL_srp_admission.sv:162-169` | stage 3 moves to its own process `slope_store` (written only out of reset, as before) |
| `docs/architecture/10_srp_engine.md:194-248` (`65324390`) | section 5.1: the storage map with intended and actual primitives, what stays per stream and why, and the measured marginal cost per talker and listener |

Why each storage change keeps behaviour identical (also in the RTL comments):

- **FIFOs.** Same pointers, counts, depth (32), full guard and registered head (`tf_q_r`); only the storage is split. A
  word is read only after its push (`tf_cnt_r`), so the missing reset is invisible, as it already was for `tf_ram_r`.
- **Talker walk record.** Every field is written by the gate open, the only writer of the matcher record; the walk
  pushes a source only while `rec_valid_r` is set, and only a gate open sets it. So the RAM copy equals the flop record
  whenever it is read, and its lack of a reset is invisible. The walk and a gate open never act on the same source in
  one cycle (the applicant arbitration takes the gate first), and both read the pre-edge value anyway.
- **Listener walk stream_id.** The same argument with the A15 settle, the only writer of `sid_r`.
- **Slopes.** A slope is read only with its `slope_valid_r` bit, which stage 3 writes with it; invalidation clears the
  bit only.
- **The elaboration-time choice** (`N > 2`) selects between two equivalent read paths; it changes no port, parameter
  or behaviour, and the lockstep bench covers both arms (1/1 and 2/2 the flop arms, 3/5, 8/8 and 9/9 the RAM arms).

## 3. Storage inventory (KL_srp_top; intended and actual primitive; Vivado report lines)

Report lines are from each run's `baseline.log`: "Distributed RAM: Final Mapping Report" unless marked "block"
("Block RAM: Final Mapping Report"). Flip-flop counts are census FD cells under the register's name (`baseline_cells.tsv`).
Shapes are 1x1 (2 sources, 2 sinks, `SLOT_AW_P` 6) and 8x8 (9, 9, 7). The same table, in prose, is 10 section 5.1.

| Structure | Source (base -> head) | Words x bits, 1x1 / 8x8 | Intended | Actual, base | Actual, head | Head report lines (1x1 standalone; 8x8 standalone; route) |
|---|---|---|---|---|---|---|
| Timer-arm FIFOs | `tf_ram_r` `KL_srp_top.sv:947` -> `tf_tk_ram_r`, `tf_ls_ram_r` `:953-954` | 2 x 32 x 47 / 2 x 32 x 48 | a FIFO memory (distributed RAM) | flip-flops: 2,304 / 2,688, no RAM-report row (`Synth 8-3333 ... u_srp/\tf_ram_r_reg[1][31][39]`, base 1x1 log `:1827`) | distributed RAM, 0 flip-flops | `\|u_srp \| tf_ls_ram_r_reg \| User Attribute \| 32 x 47 \| RAM32M x 8 \|` and `tf_tk_ram_r_reg` (`:2035-2036`); `\|KL_srp_top__GB0 \| tf_ls_ram_r_reg \| User Attribute \| 32 x 48 \| RAM32M x 8 \|` and `tf_tk_ram_r_reg` (`:2048-2049`); route `:3708-3709` |
| FIFO heads | `tf_q_r` `:955` | 2 x 47 / 2 x 48 | flip-flops (registered read) | 72 / 84 FF | 88 / 94 FF | census |
| Cadence deadlines | `cad_dl_r` | 5 x 32 | flip-flops | 160 FF | 160 FF | census |
| Talker matcher {stream_id, DA, VLAN} | `sid_r`, `da_r`, `vid_r` `KL_srp_talker_fsm.sv:357-359` | M x 124 | flip-flops (parallel compare) | 248 / 1,116 FF | the same | census (`sid_r` 128 / 576) |
| Talker walk TSpec, priority, rank, latency | `mfs_r`, `mif_r`, `prio_r`, `rank_r`, `lat_r` (base `:354-358`) -> `wtsp_r` `:372` | M x 68 | distributed RAM | flip-flops 104 / 468 behind an M-way multiplexer | distributed RAM | `\|u_srp/u_talker \| wtsp_r_reg \| User Attribute \| 2 x 68 \| RAM32M x 12 \|` (`:2032`); `\|u_talker \| wtsp_r_reg \| ... \| 16 x 68 \| RAM32M x 12 \|` (`:2046`); route `:3705` |
| Talker walk {stream_id, DA, VLAN} | the matcher flops -> `g_wid_ram.wid_r` `:509` from 3 sources | M x 124 | 1x1: the matcher flops; 8x8: distributed RAM | the matcher flops behind an M-way multiplexer | 1x1: the same (`g_wid_flops`); 8x8: distributed RAM | 8x8 `\|u_talker \| g_wid_ram.wid_r_reg \| User Attribute \| 16 x 124 \| RAM32M x 21 \|` (`:2047`) |
| Talker push register | `push_val_r` | 272 bits | flip-flops (held while the encoder accepts) | 225 / 225 FF | 226 / 227 FF | census |
| Listener matcher {stream_id, DA, VLAN} | `sid_r`, `da_r`, `vid_r` `KL_srp_listener_fsm.sv:350-352` | N x 124 | flip-flops | 248 / 1,116 FF | the same | census |
| Listener walk stream_id | `sid_r` -> `g_wsid_ram.wsid_r` `:542` from 3 sinks | N x 64 | 1x1: the matcher flops; 8x8: distributed RAM | the matcher flops behind an N-way multiplexer | 1x1: the same (`g_wsid_flops`); 8x8: distributed RAM | 8x8 `\|u_listener \| g_wsid_ram.wsid_r_reg \| User Attribute \| 16 x 64 \| RAM32M x 11 \|` (`:2052`) |
| Listener registration data | `lat_r`, `fcode_r`, `fsysid_r` | N x 104 | flip-flops (published per sink) | 208 / 936 FF | the same | census |
| Admission slopes | `slope_q_r` `KL_srp_admission.sv:111` (base) -> `:115` | M x 32 | distributed RAM | flip-flops 64 / 288 behind an M-way multiplexer | distributed RAM | `\|u_srp/u_admission \| slope_q_r_reg \| User Attribute \| 2 x 32 \| RAM32M x 6 \|` (`:2031`); `\|u_admission \| ... \| 16 x 32 \| RAM32M x 6 \|` (`:2045`); route `:3704` |
| Admission working and published grants | `wgslope_r`, `gslope_r` | M x 32 each | flip-flops (published in one cycle) | 64 + 64 / 288 + 288 FF | the same | census |
| Encoder pending tables | `msrp_ram_r`, `mvrp_ram_r` `KL_srp_encoder.sv:255-256` | 12 x 285, 12 x 19 | distributed RAM | RAM32M x 48, x 4 | the same | `\|u_srp/u_encoder \| msrp_ram_r_reg \| User Attribute \| 16 x 285 \| RAM32M x 48 \|` (`:2034`; base `:2017`) |
| Decoder listener pairing buffer | `tp_ram` (`KL_srp_decoder.sv`) | 1,024 x 8 | block RAM | 1 RAMB18 | the same | block: `\|u_srp/u_decoder \| tp_ram_reg \| 1 K x 8(READ_FIRST) \| ... \| 1 \| 0 \|` (`:2007`; base `:1994`) |
| VLAN membership table | `tbl_r` (`KL_srp_vlan.sv`) | 4 x 17 | distributed RAM | RAM32M x 3 | the same | `\|u_srp/u_vlan \| tbl_r_reg \| Implied \| 4 x 17 \| RAM32M x 3 \|` (`:2030`; base `:2015`) |

No SRP structure maps into flip-flops by accident at head. What remains in flip-flops is read by every context in one
cycle or published per stream (section 6), or is a register by design (FIFO heads, push register, cadence deadlines).
SRP's only block RAM is the decoder's RAMB18 at either shape, as at base; every other SRP memory is distributed RAM.

## 4. Tests and their controls

### 4.1 Lockstep bench (scratch, not committed)

`KL_srp_top_ref` (base `c4cb84ff`'s eight SRP modules, each renamed `_ref`) and `KL_srp_top` (the committed RTL
`25847d07`, a byte-identical snapshot) are instantiated side by side in a generated `lockstep_top` with the same
inputs every cycle. Compared every cycle (after the first reset edge):

- all 51 outputs of `KL_srp_top` (`diff_o`, one bit per port);
- 56 internal signals by hierarchical reference: both FSMs' `dbg_app_state_o`/`dbg_reg_state_o`, their encoder intake
  faces (valid, type, event, FourPacked, the 272-bit value), VLAN user faces, timer-arm faces and `txop_done`, the
  admission verdicts and round strobe, the encoder intake mux, and the FIFO bookkeeping (`tf_push_w`, `tf_pop_w`,
  `tm_st_r`, `tm_sel_r`, `tm_rr_r`, `tf_cnt_r`, `tf_wptr_r`, `tf_rptr_r`).

Environment (C++): MRPDUs built per 802.1Q §10.8.1.2 with values drawn from the same pools as the class-B requests (so
declarations, registrations and LeaveAll aging all occur), random LeaveAll flags, NumberOfValues 0..5, out-of-alphabet
events, corrupted and truncated PDUs (noisy mode); the class-B port with every op including invalid ones and
out-of-range indices; a TX-slot pool and arbiter; a timer-service model fed by the ref's arm face plus spurious
expiries of any slot; a PRNG model; `now_ms` advancing every 8..47 cycles; link, `p2p`, port rate and latency
changes; random mid-run resets. Verilator 5.050 with `--x-initial unique` and `--x-assign unique`, so every unreset
memory starts with different random contents in the two models.

| Shape (sources/sinks) | Runs x cycles | MRPDUs in | Timer arms (registrar) | Requests | Frames out | Registrations | Resets | Mismatching cycles (top / internal) |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2/2 (1x1), compressed and default cadences | 16 x 1,000,000 | 116,168 | 211,023 (7,096) | 214,828 | 60,965 | 5,383 | 226 | 0 / 0 |
| 9/9 (8x8) | 8 x 1,000,000 | 59,624 | 206,242 (25,501) | 96,125 | 39,049 | 9,328 | 104 | 0 / 0 |
| 1/1 | 8 x 1,000,000 | 59,836 | 182,553 (1,741) | 97,209 | 61,017 | 1,278 | 104 | 0 / 0 |
| 3/5 | 8 x 1,000,000 | 55,949 | 230,460 (8,014) | 118,493 | 58,201 | 6,106 | 94 | 0 / 0 |
| 8/8 | 8 x 1,000,000 | 59,763 | 175,065 (22,605) | 96,807 | 37,610 | 8,929 | 119 | 0 / 0 |
| total | 48 x 1,000,000 | 351,340 | 1,005,343 (64,957) | 623,462 | 256,842 | 31,024 | 647 | 0 / 0 |

### 4.2 Planted controls (each a copy of the committed RTL with one edit; mismatching cycles over 6 runs x 300,000)

| Control | Edit | 2/2 | 9/9 | 3/5 | 1/1 | Caught at |
|---|---|---:|---:|---:|---:|---|
| `tf-heads-swapped` | each FIFO head reads the other memory | 28,558 | 90,193 | 39,345 | 7,640 | 4 of 4 |
| `tf-head-at-write-pointer` | talker head read at `wptr - 1` | 4 | 2,490 | 80 | 0 | 3 of 4 |
| `tf-listener-push-dropped` | listener push lost when both push | 263 | 1,398 | 421 | 0 | 3 of 4 |
| `walk-record-written-on-close` | the walk record also written by a gate close | 347,115 | 498,126 | 296,453 | 485,703 | 4 of 4 |
| `wtsp-first-open-only` | TSpec record written only by a source's first open | 1,717,915 | 1,967,517 | 1,820,782 | 1,742,753 | 4 of 4 |
| `wtsp-latency-field-shifted` | latency field read one bit off | 1,845,675 | 1,884,652 | 1,858,005 | 1,829,707 | 4 of 4 |
| `wtsp-read-at-gate-source` | TSpec record read at the gate source | 737,949 | 2,306,384 | 1,156,517 | 48,259 | 4 of 4 |
| `wid-ram-first-open-only` | RAM arm: {stream_id, DA, VLAN} written only by the first open | 0 (arm not elaborated) | 2,054,932 | 1,901,974 | 0 (n/e) | 2 of 4 |
| `wid-ram-read-at-gate-source` | RAM arm read at the gate source | 0 (n/e) | 1,849,595 | 1,245,932 | 0 (n/e) | 2 of 4 |
| `wid-flops-da-of-gate-source` | flop arm: DA of the gate source | 580,488 | 0 (n/e) | 0 (n/e) | 47,564 | 2 of 4 |
| `wsid-ram-written-on-teardown` | listener RAM arm also written by A8 | 0 (n/e) | 3,095,938 | 2,635,468 | 0 (n/e) | 2 of 4 |
| `wsid-ram-first-settle-only` | listener RAM arm written only by the first settle | 0 (n/e) | 3,234,988 | 3,116,499 | 0 (n/e) | 2 of 4 |
| `wsid-flops-of-control-sink` | listener flop arm read at the control sink | 1,331,017 | 0 (n/e) | 0 (n/e) | 0 (equivalent in simulation: the out-of-range control index reads sink 0 in Verilator) | 1 of 4 |
| `slope-stored-at-stage-2-index` | slope written at the stage-2 index | 3,351,682 | 3,585,898 | 3,530,423 | 0 (one source) | 3 of 4 |
| `slope-store-source-0-only` | only source 0's slope stored | 3,287,544 | 3,584,959 | 3,493,546 | 0 (one source) | 3 of 4 |
| `talker-vid-unreset` | the matcher VID loses its reset (a stored value read without its valid bit) | 474,271 | 451,732 | 477,294 | 5 | 4 of 4 |

Every control is caught at one to four of the four shapes, as the last column shows row by row: six at four shapes,
four at three, five at two and one (`wsid-flops-of-control-sink`) at one. (Corrected in round 2: this sentence said
"each at three or four shapes", which six rows contradict; R458-1 F3.) A zero means one of three things:
- the edited arm is not elaborated at that shape (n/e);
- the edit is equivalent by construction (one source or one sink);
- for `wsid-flops-of-control-sink` at 1/1, equivalent in simulation only: Verilator 5.050 reads the out-of-range 64-bit control index as sink 0;
- for `tf-head-at-write-pointer` and `tf-listener-push-dropped` at 1/1, the situation the edit needs (two queued
  arms in one FIFO; both FSMs pushing in one cycle) did not arise in those six runs.

The same situations make the `tf-head-at-write-pointer` count small at 2/2 (4). It is 2,490 at 9/9.

### 4.3 Module-level variant choice (scratch Vivado; not the recipe)

`KL_srp_top` alone in a wrapper that ties `req_max_interval_i` to 1 as `protocol_processor_top` does; Vivado 2026.1,
`xc7a100t-fgg484-2`, out of context, `AreaOptimized_high`, 20 ns, N = 2 / `SLOT_AW_P` 6 and N = 9 / 7. LUT (of which
LUTRAM) / FF.

| Variant | N | `u_srp` | top glue | `u_talker` | `u_listener` | `u_admission` | F7 |
|---|---:|---:|---:|---:|---:|---:|---:|
| v0 base `c4cb84ff` | 2 | 4,460 (186) / 6,395 | 881 (0) / 2,785 | 636 (0) / 715 | 395 (0) / 666 | 269 (0) / 271 | 331 |
| v1 lever 2 only | 2 | 3,840 (250) / 4,170 | 327 (64) / 560 | 605 (0) / 715 | 364 (0) / 666 | 269 (0) / 271 | 51 |
| v2 v1 + talker walk-only fields in RAM | 2 | 3,849 (286) / 4,064 | 327 (64) / 560 | 604 (36) / 609 | 364 (0) / 666 | 269 (0) / 271 | 53 |
| v5 v1 + whole walk records and slopes in RAM | 2 | 3,885 (438) / 3,999 | 327 (64) / 560 | 636 (120) / 608 | 378 (44) / 666 | 276 (24) / 207 | 52 |
| **vF landed** | 2 | 3,856 (310) / 4,000 | 327 (64) / 560 | 604 (36) / 609 | 364 (0) / 666 | 276 (24) / 207 | 53 |
| v0 base | 9 | 8,249 (186) / 10,973 | 931 (0) / 3,167 | 2,144 (0) / 2,263 | 1,800 (0) / 2,612 | 782 (0) / 977 | 377 |
| v1 | 9 | 7,622 (250) / 8,531 | 308 (64) / 720 | 1,872 (0) / 2,267 | 1,909 (0) / 2,612 | 783 (0) / 977 | 91 |
| v2 | 9 | 7,505 (286) / 8,054 | 308 (64) / 720 | 1,802 (36) / 1,790 | 1,871 (0) / 2,612 | 781 (0) / 977 | 126 |
| v5 | 9 | 6,952 (438) / 7,760 | 340 (64) / 720 | 1,703 (120) / 1,783 | 1,558 (44) / 2,612 | 761 (24) / 689 | 77 |
| **vF landed** | 9 | 6,962 (438) / 7,760 | 339 (64) / 720 | 1,697 (120) / 1,783 | 1,558 (44) / 2,612 | 761 (24) / 689 | 76 |

At two contexts a second, RAM copy of {stream_id, DA, VLAN} costs more than the 2-way multiplexer behind the
matcher's flops (v5 against v2: talker +32 LUT, listener +14), at nine it saves 99 and 351 LUTs; the landed RTL
selects by N (`N > 2`). Without `ram_style = "distributed"` the split FIFOs mapped to one RAMB36 each
(`Synth 8-7052 ... tf_tk_ram_r_reg (implemented as a Block RAM)`), which #638's gate forbids (+0 BRAM); every new
memory carries the attribute.

### 4.4 Lint and portability

- `scripts/lint_hdl.sh` rc 0, 41 of 41 at base and head. The flop arms are not elaborated at the modules' default
  N = 8, so the three changed modules were also linted with the same flags at 1, 2, 3 and 9 contexts, and
  `KL_srp_top` at 1/1, 2/2 and 9/9: all clean.
- `syn/yosys/run.sh` rc 0 at `25847d07`: 36 of 36 tops, `KL_aecp_engine` Xilinx mapping OK; Yosys 0.66 and sv2v
  0.0.13 also elaborate the talker and listener at 1, 2 and 9 contexts and admission at 2 (`chparam`).
- No committed test changes: behaviour is unchanged, so every suite and campaign keeps its count.

## 5. Vivado before and after (#638 recipe and tools at `68d26ea0`)

### 5.1 Combinations and method

- **Base:** scratch parent kebag-logic/milan-fpga dev `5fabb46e767c9308ab2580916237f43577698c6e`, processor gitlink set
  in the index to `c4cb84ff`, `parent-adoption-c8-bbf704ec.patch` (sha256 `3340d2e8...a38a4c`) and
  `parent-adoption-p2-p1-1269cdaf.patch` (sha256 `d3034e89...613d84`) applied with `git apply --check` then
  `git apply`; submodules `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`, `external` `efeb541a`.
- **Head:** the same with the processor at `25847d07` (the RTL commit; `65324390` adds only
  `docs/architecture/10_srp_engine.md`, so the measured image is the head's).
- **Recipe:** `docs/testing/PP_SHADOW_BASELINE_RECIPE.md` with the tools of `234-area-baseline` `68d26ea0`
  (`pp_baseline.py --selftest` rc 0, `pp_resource_gate.py check-baseline` rc 0): the export (`build.sh ax7101` and
  `ax8x8` previews, `milan_soc.py` without `--build`), the integrated 1x1 route, the 8x8 RTL elaboration, and both
  standalone syntheses with `--integrated-clock` (20 ns). Vivado 2026.1, `xc7a100t-fgg484-2`, `AreaOptimized_high` /
  `ExploreArea` / `ExtraPostPlacementOpt` / `AggressiveExplore`, 32 threads, default seed. Every run held
  `/tmp/milan-vivado.lock` and was this lane's only Vivado; no heavy build of this lane ran beside one.
- **Exports:** base and head differ only in the generated Verilog's comments (date, tree-listing order) and the Tcl's
  output path; ROMs (`ltn_rom.hex`, `ucode.hex`), XDC and every `.init` hash equal.

### 5.2 Whole endpoint

| Endpoint | | LUT (logic + memory) | FF | Slice | RAMB36 / RAMB18 | DSP | CARRY4 | F7 | WNS / WHS ns |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Route 1x1, whole image | base | 51,434 (49,158 + 2,276) | 59,691 | 15,847 (99.98 %) | 79 / 27 | 14 | 3,526 | 1,448 | +0.079 / +0.014 |
| | head | 51,005 (48,611 + 2,394) | 57,262 | 15,837 (99.92 %) | 79 / 27 | 14 | 3,524 | 1,066 | +0.354 / +0.036 |
| | head - base | -429 (-547 + 118) | -2,429 | -10 | 0 / 0 | 0 | -2 | -382 | +0.275 / +0.022 |
| Standalone 1x1 | base | 24,930 (23,644 + 1,286) | 25,465 | | 21 / 3 | 8 | 1,643 | 639 | estimate -2.059 / +0.159 |
| | head | 24,258 (22,848 + 1,410) | 23,130 | | 21 / 3 | 8 | 1,644 | 343 | estimate -1.874 / +0.159 |
| | head - base | -672 | -2,335 | | 0 / 0 | 0 | +1 | -296 | |
| Standalone 8x8 | base | 32,584 (31,502 + 1,082) | 34,211 | | 26 / 5 | 8 | 2,028 | 1,158 | estimate -2.161 / +0.159 |
| | head | 31,109 (29,779 + 1,330) | 30,648 | | 26 / 5 | 8 | 2,039 | 851 | estimate -1.495 / +0.159 |
| | head - base | -1,475 | -3,563 | | 0 / 0 | 0 | +11 | -307 | |

- **Route status.** Base routes all 107,053 routable nets, head all 104,430, both with 0 nets with routing errors;
  both meet the build gate (BUILDING section 5: WNS at least +0.03 ns, WHS at least 0) at 50 MHz. The head route
  finished in 32.8 minutes against base's 83.2 (section 5.6).
- **Slices.** The placer fills the device at this occupancy; the freed logic shows as timing margin (+0.275 ns WNS)
  and routing time, not as a slice count.
- **Standalone timing.** A synthesis estimate with no I/O constraints, as #638 states; not a closure verdict.

### 5.3 `u_srp` sub-blocks: LUT (of which LUTRAM) / FF

| Endpoint | | `u_srp` | top glue | `u_talker` | `u_listener` | `u_admission` | `u_decoder` | `u_encoder` | `u_domain` | `u_vlan` |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Route 1x1 | base | 4,340 (180) / 6,263 | 921 (0) / 2,792 | 623 (0) / 671 | 466 (0) / 667 | 224 (0) / 207 | 589 (0) / 630 | 1,316 (168) / 1,062 | 79 (0) / 108 | 139 (12) / 126 |
| | head | 3,711 (298) / 3,839 | 350 (64) / 500 | 604 (32) / 604 | 442 (0) / 667 | 244 (22) / 143 | 587 (0) / 630 | 1,286 (168) / 1,061 | 73 (0) / 108 | 138 (12) / 126 |
| Standalone 1x1 | base | 4,558 (186) / 6,438 | 907 (0) / 2,836 | 663 (0) / 714 | 422 (0) / 667 | 331 (0) / 271 | 589 (0) / 630 | 1,450 (174) / 1,086 | 53 (0) / 108 | 143 (12) / 126 |
| | head | 3,988 (310) / 3,979 | 354 (64) / 545 | 648 (36) / 610 | 385 (0) / 667 | 346 (24) / 207 | 607 (0) / 630 | 1,450 (174) / 1,086 | 54 (0) / 108 | 144 (12) / 126 |
| Standalone 8x8 | base | 8,705 (186) / 11,192 | 1,053 (0) / 3,387 | 2,151 (0) / 2,261 | 2,014 (0) / 2,615 | 844 (0) / 977 | 856 (0) / 630 | 1,472 (174) / 1,088 | 59 (0) / 108 | 256 (12) / 126 |
| | head | 7,313 (438) / 7,747 | 297 (64) / 703 | 1,549 (120) / 1,787 | 1,843 (44) / 2,615 | 826 (24) / 689 | 906 (0) / 630 | 1,452 (174) / 1,089 | 42 (0) / 108 | 398 (12) / 126 |

`u_srp` head - base: route -629 LUT / -2,424 FF; 1x1 -570 / -2,459; 8x8 -1,392 / -3,445. The names come from the
rebuilt hierarchy, so logic can move between siblings (the decoder and VLAN blocks, which this lane did not change,
move by +18 to +142 LUTs). Against #638's estimates: lever 2 ("about 2,300 FF, 580 LUT and 288 MUXF7") measures
-2,291 FF and -553 LUT in the top glue and -296 F7 at 1x1; lever 4 ("about 440 LUT at 1x1, about 3,100 at 8x8")
measures its storage part only (talker, listener and admission at 1x1: -37 LUT, -168 FF; at 8x8: -791 LUT, -762 FF),
because the shared evaluator is the STOP item (section 6).

### 5.4 Marginal cost of one stream context, (8x8 - 1x1) / 7, standalone

| Block | LUT base | LUT head | FF base | FF head |
|---|---:|---:|---:|---:|
| `u_srp/u_talker` (per source) | 213 | 129 | 221 | 168 |
| `u_srp/u_listener` (per sink) | 227 | 208 | 278 | 278 |
| `u_srp/u_admission` (per source) | 73 | 69 | 101 | 69 |
| `u_srp/u_decoder` | 38 | 43 | 0 | 0 |
| `u_srp/u_vlan` | 16 | 36 | 0 | 0 |
| top glue `(u_srp)` | 21 | -8 | 79 | 23 |
| `u_srp`, total | 592 | 475 | 679 | 538 |
| wrapper, total | 1,093 | 979 | 1,249 | 1,074 |

One more talker now costs about 200 LUTs and 240 FFs (its FSM and its admission share), one more listener about 210
LUTs and 280 FFs. The remaining per-context logic is the matcher, the transitions and the published levels (section 6).
The 1x1 configuration has no logic for inactive stream slots: every per-stream structure is sized by the bound
`N_STREAM_OUT_P`/`N_STREAM_IN_P`, which is 2 at 1x1 (the stream and CRF), and the census shows exactly two contexts
(`sid_r` 128 FF per FSM at 1x1, 576 at 8x8).

### 5.5 #638's gate (`pp_resource_gate.py check`, against the recorded C of dev `54643724`)

| Endpoint | Base | Head |
|---|---|---|
| route-1x1 | rc 1: LUT +667 over the 500 tolerance (`u_pp/u_aecp/u_d3` +580) | rc 0: LUT +238, FF -2,372 ("re-baseline recommended" for FF), WNS +0.354, route complete |
| ooc-1x1 | rc 1: LUT +598 over the 250 tolerance (`u_d3` +617) | rc 0: LUT -74, FF -2,215 ("re-baseline recommended" for FF) |
| ooc-8x8 | rc 1: LUT +1,028 over 316 (`u_d3` +1,204) | rc 0: LUT -447, FF -3,289 ("re-baseline recommended" for LUT and FF) |

`check-baseline` rc 0 ("baseline PASS: 3 endpoints"). Base fails because it is the un-rebaselined next adoption (its
`u_d3` growth comes from the processor content since `631eeb34`), as #232's base did (#638 ruling (d)). Head passes
partly because the SRP saving offsets that growth; the like-for-like comparison is head against base (5.2, 5.3).
Nothing was recorded into `pp_resource_baseline.json` (not in this lane's scope).

### 5.6 Run receipts

| Combination | Run | rc | Minutes | Log | Log SHA-256, first 16 | Log bytes | `Synth 8-4445` diagnostics |
|---|---|---:|---:|---|---|---:|---:|
| base | RTL elaboration, 8x8 parameters | 0 | 1.0 | `elaborate.log` | `ce6ce4f803d232f4` | 216,488 | 0 |
| base | Integrated route, 1x1 | 0 | 83.2 | `baseline.log` | `b2ee637b627ac44a` | 694,335 | 0 |
| base | Standalone synthesis, 1x1 | 0 | 46.9 | `baseline.log` | `0cd111793f38d9bc` | 243,319 | 0 |
| base | Standalone synthesis, 8x8 | 0 | 28.0 | `baseline.log` | `e4f3c0cc23ea9d37` | 247,522 | 0 |
| head | RTL elaboration, 8x8 parameters | 0 | 2.0 | `elaborate.log` | `e42bc7a1c94bc26a` | 216,498 | 0 |
| head | Integrated route, 1x1 | 0 | 32.8 | `baseline.log` | `7a6ddd0e74f7d3c2` | 599,831 | 0 |
| head | Standalone synthesis, 1x1 | 0 | 12.6 | `baseline.log` | `350d7e157fd5da6c` | 247,200 | 0 |
| head | Standalone synthesis, 8x8 | 0 | 32.2 | `baseline.log` | `4d12c536cd869681` | 251,156 | 0 |

The one `Synth 8-4445` match in each log is the echoed `set_msg_config` command (line 262). Minutes include time
shared with other lanes' work on the host (load average up to 46). The base 8x8 run was first launched at 03:55,
waited on another lane's lock, and was stopped before it started (empty log) to run the heavy campaign stage in that
window; it was rerun in a fresh directory at 06:29 (the receipt above). During the base route's synthesis this
service unit reached its 12 GB cap (`memory.events` max 53,574 then 61,118, oom 0, oom_kill 0; swap peak about
8 GB) with no other heavy work of this lane running; the run completed rc 0.

## 6. STOP item: lever 4's shared evaluator needs a timing change

#638 estimated lever 4 as "one evaluator per FSM instead of two saves one context's marginal cost": about 440 LUT at
1x1 and 3,100 at 8x8. The storage part of that cost is done (section 2). What remains per context is evaluation that
the RTL performs for every context in the same cycle, by contract:

- **The matcher.** `KL_srp_decoder` emits one value per cycle while it drains a packed vector, and its event port has
  no ready (`evt_valid_o`, banner "one event strobe per cycle while draining packed bytes"). Every source and every
  sink compares {stream_id, DA, VLAN} with it in that cycle (`KL_srp_talker_fsm.sv` `hit_map`,
  `KL_srp_listener_fsm.sv` `hit_map`), and several contexts may match the same value.
- **The Table 10-3/10-4 transitions.** A matched value, `periodic!`, a received LeaveAll and the own LeaveAll reach
  every context in the same cycle (`app_arb`, `app_plane`, `reg_plane`); the existing `per_pend_r`/`rla_pend_r`
  deferral only covers a context that is busy with a higher-priority event in that cycle.
- **The published levels.** `tk_decl_state`, `lstn_reg_state`, `active`, `tk_reg_state`, `lstn_decl_state`,
  `acc_latency`, `msrp_fail_code/bridge` and `granted_slope_bps` are per-stream ports of `KL_srp_top`; their gates
  (for example 48 AND terms per source for `src_fail_bridge_o`) are the ports' functions.

None of these can be time-multiplexed without moving protocol-visible timing. The options:

- **(a) One evaluator per FSM.** Contexts move to distributed RAM and are evaluated one per cycle. `KL_srp_decoder`
  gains a ready on its event port (a port change). Each received value then takes up to M or N cycles, and
  TK_ATTR_REGISTERED/UNREGISTERED, LISTENER_REG_CHANGE and the applicant moves of a broadcast land up to M - 1 or N - 1
  cycles later. A burst of values also holds the MRPDU RX queue longer. The saving is about #638's estimate (the
  measured per-context logic is in section 5.4).
- **(b) Keep the parallel evaluation (landed).** Cycle-exact; lever 4 then delivers its storage saving only.

Requested: (b) as final for #230, or (a) as an input to the redesign (#640). With (b), this head is ready for review
as it stands.

## 7. Processor suites (base `c4cb84ff`, head `25847d07`, each from a `git archive`)

| Command | Base | Head |
|---|---|---|
| `./scripts/lint_hdl.sh` | rc 0, 41 of 41 (14 s) | rc 0, 41 of 41 (31 s) |
| `./scripts/run_suites.sh` | rc 0, 33 suites, 1,021,423 checks, 0 failing (1,054 s) | rc 0, 33 suites, 1,021,423 checks, 0 failing (1,125 s); every suite's tally equal to base |
| SRP suites in it | `srp_admission` 991,231, `srp_decoder` 190, `srp_encoder` 581, `srp_stream_fsms` 1,219, `srp_top` 2,200 | the same |
| `tb/pp_top` in it | 10,390 | 10,390 |
| `make check` | | rc 0 at the final head `65324390`: 41 mermaid + 18 wavedrom blocks, 1,114 links, 115 REQ rows, 94 matrix rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` | | rc 0 at `65324390`: 94 rows, 0 untested |
| `./syn/yosys/run.sh` | | rc 0 (section 4.4) |

## 8. Campaigns (every driver whose build includes a changed file)

"Record identical": every line of the two logs, scratch paths removed, is the same, in the same order or, for the
drivers that print arms as they finish, as the same set of lines (`compare_camp.py`). One normalisation: `d3`'s
D3C3/D3C4 failure messages print `"blank %u of %d"` with no argument for the `%d`
(`tb/pp_top/d3_phases.hpp:2963-2965`, `:2992-2994`), so that number is unpassed varargs and differs from run to run;
it is the only field normalised. `tb/acmp_talker/retry_mutants.py`, `tb/desc_store` and `tb/nvm_port` build no SRP
file and no top, so they were not run.

| Campaign | Base `c4cb84ff` | Head `25847d07` | Record |
|---|---|---|---|
| `tb/srp_top/mutants.py --jobs 4` | rc 0, 90 checks: 90 PASS (533 s) | rc 0, 90 checks: 90 PASS (614 s) | identical; all 73 patches still apply |
| `tb/srp_admission/mutants.py --jobs 4` | rc 0, 12 checks: 12 PASS (207 s) | rc 0, 12 checks: 12 PASS (206 s) | identical |
| `tb/maap/mutants.py --jobs 4` (pp_top arms) | rc 0, 32 checks: 32 PASS (84 s) | rc 0, 32 checks: 32 PASS (83 s) | identical |
| `tb/adp_engine/mutants.py --jobs 4` (pp_top arms) | rc 0, 32 checks: 32 PASS (148 s) | rc 0, 32 checks: 32 PASS (139 s) | identical |
| `tb/pp_top/ctr_mutants.py --jobs 4` | rc 0, 18 checks: 18 PASS (157 s) | rc 0, 18 checks: 18 PASS (164 s) | identical |
| `tb/pp_top/notify_mutants.py --jobs 4` | rc 0, 40 of 40 KILLED, goldens PASS (373 s) | rc 0, the same (321 s) | identical (set) |
| `tb/pp_top/acmp_mutants.py --jobs 4` | rc 0, 19 of 19 KILLED, goldens PASS (123 s) | rc 0, the same (134 s) | identical (set) |
| `tb/pp_top/aecp_mutants.py --jobs 4` | rc 0, 60 checks: 60 PASS (383 s) | rc 0, the same (374 s) | identical |
| `tb/pp_top/aecp_dispatch_mutants.py --jobs 4` | rc 0, 41 checks: 41 PASS (397 s) | rc 0, the same (366 s) | identical (with the one normalisation) |
| `tb/pp_top/d3_mutants.py --jobs 4` | rc 0, 110 of 110 KILLED, goldens PASS (2,925 s) | rc 0, the same (2,914 s) | identical (set) |
| `tb/pp_top/gsi_mutants.py --jobs 4` | rc 0, 20 detected by named checks, golden and restored PASS (596 s) | rc 0, the same (591 s) | identical |
| `tb/pp_top/name_wr_mutant.py` | rc 0, decode killed, golden and restored PASS (65 s) | rc 0, the same (62 s) | identical |

## 9. Parent consumer set (dev `5fabb46e` + c8-bbf704ec + p2-p1-1269cdaf, processor `65324390`)

Scratch parent `$VALIDATION_STORAGE/pp230-a523/parent` (never committed or pushed): a clone of kebag-logic/milan-fpga
detached at `5fabb46e767c9308ab2580916237f43577698c6e`; submodules `external` `efeb541a`, `gptp-processor`
`5dce647a`, `third_party/verilog-axis` `48ff7a7e`, `protocol-processor` (each `rev-parse --show-toplevel` checked
before any git command in it); the processor gitlink set in the index only (`git update-index --cacheinfo`) to the
final head `65324390`, its checkout detached there; both patches applied with `git apply --check` then `git apply`.
GNU Make 4.3 and the pinned Verilator 5.050 wrapper first on PATH; `make -j16` for the bench builds.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | every ratchet held |
| 2 | `scripts/check_py_idiom.py` | 0 | every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files in the `milan_datapath` closure, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 49 checks, 49 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports, undocumented 111 <= 111 (this lane changes no port) |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | within ratchets |
| 8 | `scripts/docs_check.py` | 0 | 0 findings, 186 md + 970 files |
| 9 | `scripts/xvlog_gate.py --check` (alone, under the Vivado lock) | 0 | 4 findings == ratchet (0 hdl/, 4 pinned processors), analysed at `protocol-processor@65324390` (714 s, including the wait for the lock) |
| 10 | `sw/builder/test_builder.py` | 0 | Make 4.3: "ALL GATES PASS EXCEPT 2 NOT RUN": gate 11 needs the local mf48 build tree, and gate 1b's `MAKEFLAGS += -e` mutation, which Make 4.3 does not re-read mid-parse (1,318 s). Rerun alone with the host's GNU Make 4.4.1: rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11 only, as in the P1 record) (1,111 s) |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 violations <= ratchet 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | 311 checks, 0 failures (282 s) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS, 0 FAIL; 4 render mutants caught; gmstep controls 6 of 6 (2,512 s) |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 2 | two-stream leg 65 checks, 0 failures; shipping leg 155 checks, **2 failures, both T30 INTERNAL LAW**: the fill at accept 227 of 292, the first event in the law band 285 of 292, first-event delay 18,396..18,821 cycles = 8.830..9.034 media ticks (210 s). These are #643's checks with #643's P1 figures to the digit (#643: "227 of 292", "285 of 292, delay 8.830..9.034"), so they are recorded against #643. The same gate at the base processor `c4cb84ff` (checkout and index switched, then back): rc 2 with the same two failures and the same figures, 18,396..18,821 cycles (181 s) |

Gate 16's T30 law depends on the feed's phase against the INTERNAL grid, which the processor's boot length sets
(#643); P1 (in `main` since `c4cb84ff`) moved it. An equal first-event delay at base and head is end-to-end evidence
that this lane did not move the boot timing.

## 10. Scratch, receipts and notes

Everything below stays in `$VALIDATION_STORAGE/pp230-a523/` (outside every repository; never committed or pushed). Digests
are SHA-256, first 16 hex digits.

| Item | Where (under the scratch root) | Digest |
|---|---|---|
| Lockstep top generator | `lockstep/gen_top.py` | `37e13f65c48cf82d` |
| Lockstep harness (C++) | `lockstep/lockstep_main.cpp` | `eda930b367eaed36` |
| Lockstep build script | `lockstep/build.sh` | `822204c3daf8be31` |
| Lockstep campaign script / its log | `lockstep/campaign.sh` / `lockstep/campaign-final.log` | `654ca3eea663f91f` / `52b707744cf948e0` |
| Planted controls / runner / log | `lockstep/make_controls.py` / `lockstep/run_controls.sh` / `lockstep/controls-final.log` | `0547433a18153166` / `85be3a023b74871a` / `536cdd3ab7faa066` |
| Renamed base RTL (`_ref`) | `lockstep/ref/*.sv` (from `git archive c4cb84ff`) | `KL_srp_top_ref.sv` `cd34e8c4949d0454` |
| RTL under test (snapshot, `diff -r` equal to `25847d07`'s `hdl/srp`) | `lockstep/final/srp-rtl/` | |
| Module-level wrapper / Tcl / runs | `explore/srp_area_wrap.sv` / `explore/synth_one.tcl` / `explore/run-v*` | `e79bf4ff14f6206b` / `673de1d3dc7e8bea` |
| Recipe runner and chain | `bin/meas.sh`, `bin/run_chain.sh`, `bin/export_combo.sh`, `bin/export.py` | `d5c83a5b845a4a4f`, `750e9ec59daf94e2`, `539888cf86285d5d`, `92fd41531ebba4c7` |
| Measurement directories (reports, checkpoints, logs) | `meas/base/`, `meas/head/` (998 MB) | receipts in 5.6 |
| Campaign runner / comparator / logs | `bin/heavy.sh` / `bin/compare_camp.py` / `camp/` | `8288509814be178a` / `f1f7749f2f1290eb` |
| Suite logs | `suites/` | |
| Parent gate runner / logs | `bin/pgates.sh` / `pgates/` | `f5249b3ee1ca2460` |
| Table generator | `bin/tables.py` | `c02e3b4e3f0761e8` |
| Scratch parent | `parent/` (clone at `5fabb46e`, both patches applied in the work tree, processor gitlink set in the index only) | |
| #638 tools | `tools234/` (`git archive 68d26ea0`) | |

Notes:
- **Memory.** This service unit reached its 12 GB cap during Vivado runs (`memory.events` max 53,574 after the base
  route, 61,118 after the base 1x1 run, 139,528 by the parent stage; oom 0, oom_kill 0 throughout; swap peak about
  8 GB). The heavy campaign stage peaked at about 9.4 GB.
- **Lock contention.** Other lanes held `/tmp/milan-vivado.lock` for long stretches (another lane's route, xvlog gate
  and a sweep). The base 8x8 run's first launch waited behind one and was stopped before it started.
- **A bench-message defect found on the way** (not fixed, out of scope): `tb/pp_top/d3_phases.hpp:2963-2965` and
  `:2992-2994` print `"blank %u of %d"` with no argument for `%d`, so the D3C3/D3C4 failure messages of killed `d3`
  arms print unpassed varargs, which differ from run to run.
- **The session brief** also carried a paragraph addressed to another executor ([A518], issue #25, PR #26). It
  conflicts with this lane's rules (only TAKEN, REVIEW READY or STOP on milan-fpga #230), so nothing was posted on #25
  and no [A518] packet was written.

## Round 2

Status: **REVIEW READY** at head `1199255bee820eb46c24fe5d0cbf7f043c828a3c` (branch `pp230-srp-area`, not pushed).

- REVIEW READY posted: kebag-logic/milan-fpga#230 comment 5979936594.

- Assignment: kebag-logic/milan-fpga#230 comment 5978448959, after R458-1 (processor PR #154 comment 5978441050) and
  R459-1 (5978360032), both NEGATIVE on MINOR findings, none in the RTL. Their packets with probes and lockstep benches:
  parent branch `pp230-review-evidence` at `75be5c11`, read from a scratch fetch.
- No rebase and no amend: a `--no-ff` merge of processor `main` `83999eba`, then one-line commits on top of `65324390`.
- No HDL changed in round 2; no port, parameter, register or behaviour change. The RTL is still `25847d07`'s.

### R2.1 Items and outcome

| Item | Outcome |
|---|---|
| 1. Committed coverage of the new storage paths at both arms | done: walk-record arms WK1-WK8 in `tb/srp_stream_fsms` and timer-arm FIFO arms TF1-TF5 in `tb/srp_top`, each at sources/sinks 1/1, 2/2, 3/5 and 9/9; the slopes are the admission suite's (1, 2, 3, 5 and 8 sources). Both reviews' probes and the sixteen round-1 controls are 33 killed controls of `tb/srp_top/mutants.py` (one patch per distinct edit) and are tabled in the srp_top README. Both bars hold (R2.4.5). The round-1 lockstep bench and its controls are in the packet `lockstep-r1/` |
| 2. The control count | stated row by row: the round-1 table (section 4.2) now has a "Caught at" column and a corrected summary; the new table is R2.4.4 and the srp_top README; the PR body carries both |
| 3. Residue | R1 and R2 fixed in PR-BODY.md; S1 taken, as one sentence in `docs/guides/hdl-engineer.md` section 3.1 |
| 4. Merge `main` `83999eba` | `4994ada`, no conflict, no SRP HDL in it; the campaigns and gates it touches re-run (R2.7, R2.8) |
| Gates | every processor suite, lint, `make check`, the Yosys gate, the srp_top and srp_admission campaigns (the srp_stream_fsms arms run in the srp_top campaign), the campaigns the merge touches, the new coverage and its controls, and the parent consumer set of 17 at dev `241f9184` with c8, p2-p1 and c10 (R2.8) |

### R2.2 Commits on top of `65324390`

| Commit | Subject |
|---|---|
| `4994ada` | Merge processor main 83999eba (C10, #85) into pp230-srp-area (parents `65324390`, `83999eba`) |
| `eb352ff` | Check the #230 walk-record copies at sources/sinks 1/1, 2/2, 3/5 and 9/9 in tb/srp_stream_fsms (WK1-WK8) |
| `d47ce65` | Check the #230 timer-arm FIFOs at 1/1, 2/2, 3/5 and 9/9 in tb/srp_top, the full guard under a forced stall (TF1-TF5) |
| `d21dd8e` | Plant both #230 reviews' probes and the lane's controls as 33 killed controls of the srp_top campaign |
| `df02e64` | Name the #230 walk copies, slopes and timer-arm FIFOs in the storage rule and point 10 section 5.1 at their tests |
| `f727957` | Give the #230 arms' shape -CFLAGS groups -Wall -Wextra and drop four one-line multi-element initialisers, for the parent's C++ idiom gate |
| `7365022` | Walk the #230 records again with the idle gate and control faces parked on their highest index (WK1, WK6) |
| `1199255` | Re-measure the #230 control table from the head's campaign after the parked-index walk arms |

`df02e64`'s subject says "10 section 5.1", the form R459-1 R1 called ambiguous; the file is
`docs/architecture/10_srp_engine.md`. With no amend allowed it stays; the PR body names the file in full.

### R2.3 Changes (file:line at `1199255`)

| File:line | Change |
|---|---|
| `tb/srp_stream_fsms/srp_walk_wrap.sv` (new, 240 lines) | both FSMs at any shape (`N_SOURCES_P`, `N_SINKS_P`); 4-bit index inputs cut to each FSM's width; declaration levels padded to 16 streams |
| `tb/srp_stream_fsms/walk_main.cpp:1-29` | banner: what the walk copies are and the checks WK1-WK8 |
| `tb/srp_stream_fsms/walk_main.cpp:220-235` | `park_gate`, `park_ctl`: the idle face on the highest index its width can name (`kParkedIndex`) |
| `tb/srp_stream_fsms/walk_main.cpp:326-374` | the talker arm: WK1 (twice: gate face on the last source, then parked), WK2-WK5 |
| `tb/srp_stream_fsms/walk_main.cpp:376-415` | the listener arm: WK6 (twice), WK7, WK8 |
| `tb/srp_stream_fsms/Makefile:18-56` | `WALK_SHAPES = 1x1 2x2 3x5 9x9`; `make` runs `walk` at each shape, then the 8-stream suite (its tally last); every part runs after a failure; `RUN_ARGS=walk` or `suite`; `--x-initial unique` and `+verilator+rand+reset+2` |
| `tb/srp_top/srp_store_wrap.sv` (new, 322 lines) | the real engine, tx slots, timer service and PRNG at any shape; read-only probes of both FSM arm faces, the merged face, the FIFO counts and the issue state; `:20-27` the Decision; `:164-169` the one forced state, `tm_stall_i` |
| `tb/srp_top/store_main.cpp:164-220` | the FIFO model (`Scoreboard`): offers, the full-guard refusal, issued words against the model's head |
| `tb/srp_top/store_main.cpp:408-471` | the first arm: own LeaveAll, the re-declaration on the LeaveAll clock, the round-robin parity step; TF1-TF3 |
| `tb/srp_top/store_main.cpp:473-518` | the held arm; TF4, TF5 |
| `tb/srp_top/Makefile:24-62` | `STORE_SHAPES`; `make` runs `storage` at each shape, then the suite (its tally last); `RUN_ARGS=storage`; BLKANDNBLK, MULTIDRIVEN and PINCONNECTEMPTY waived for that build alone |
| `tb/srp_top/mutants.py:110-150` | 33 rows: suites `srp_top` (group `storage`), `srp_stream_fsms` (`walk`), `srp_admission` |
| `tb/srp_top/mutants.py:34-35`, `:103` | the three existing srp_stream_fsms rows run the group `suite` (the 8-stream suite alone, as before) |
| `tb/srp_top/mutants.py:182` | `srp_admission` copied into each scratch tree |
| `tb/srp_top/mutants.py:241-243` | assertion coverage also requires TF1-TF5 and WK1-WK8 |
| `tb/srp_top/mutations/*.patch` (33 new) | one unified diff per distinct edit, `git apply --check` clean |
| `tb/srp_top/README.md:14-17`, `:245-249`, `:497-626` | `make`'s new order, `RUN_ARGS=storage`, the FIFO arms and the control table |
| `tb/srp_stream_fsms/README.md:7-9`, `:171-207` | `make`'s new order, the walk-record arms |
| `docs/guides/hdl-engineer.md:88-93` | S1: the walk copies, slopes and FIFOs named in the storage rule's exceptions |
| `docs/architecture/10_srp_engine.md:219-222` | section 5.1 points at the arms and the campaign |

### R2.4 Item 1: coverage, controls and the bar

#### R2.4.1 Walk records (`tb/srp_stream_fsms`)

The walk copies are elaborated in both arms: flops at one and two contexts (`g_wid_flops`, `g_wsid_flops`), distributed
RAM from three (`g_wid_ram.wid_r`, `g_wsid_ram.wsid_r`); `wtsp_r` is RAM at every shape. Every check compares the
FirstValue the walk hands the encoder with the record the harness declared, settled or tore down; unreset memories start
random.

| Check | What it proves |
|---|---|
| WK1 | every source publishes its own declaration, with the idle gate face on the last source and then on the highest index its width names (beyond the last source at 1, 3 and 9 sources, as the top's latched index of a refused request can be) |
| WK2 | a re-declaration replaces every field, made in the opposite order (the gate face on source 0) |
| WK3 | a close sends one Leave of the record declared, not of the values on the gate face |
| WK4 | a closed source re-opened publishes its new record beside the others |
| WK5 | a reset empties the records: a close of a source not opened since leaves VID 0, and the walk publishes only what was declared after the reset |
| WK6 | every sink publishes its own settled stream_id, with the idle control face on the last sink and then parked |
| WK7 | a teardown sends one Leave of the settled stream_id, not of the one on the control face |
| WK8 | a re-settle on a new stream replaces the stream_id, made in the opposite order |

Positive, at the head (the campaign's `control srp_stream_fsms walk` receipt): 23, 30, 43 and 79 checks at 1/1, 2/2,
3/5 and 9/9, all PASS.

#### R2.4.2 Timer-arm FIFOs (`tb/srp_top`)

A scoreboard reads both FSMs' arm faces (offers) and the merged face (issues) and holds the FIFO contract: every op
leaves once, in its FSM's order, unmodified, except one offered while its FIFO holds 32 words, which the guard refuses.

- **Both FSMs offering in one clock** (what `tf-listener-push-dropped` needs): an own LeaveAll ages both registrar arrays
  in one clock. Every source and sink is registered first.
- **Two words in the talker FIFO at a selection** (what `tf-head-at-write-pointer` needs at 1/1): on a LeaveAll clock
  where the round-robin will serve the listener FIFO first, a DECLARE_TALKER of source 0 is accepted; its gate op cancels
  the leave timer the LeaveAll started, so the talker FIFO is offered a second op before its first is issued. When the
  round-robin points at the talker FIFO, the peer re-joins all but source 0, whose timer runs out: an odd number of
  issues, so the next LeaveAll serves the listener first. At every shape the second LeaveAll is the one.
- **The full guard** (what `tf-full-guard-31` and both `*-write-ignores-full` need): no port sequence fills a FIFO (it
  drains a word every two clocks; a registrar walk offers at most one op per context). The wrap holds the merged issue in
  TM_SEL while `tm_stall_i` is high, the one forced state of these arms (`srp_store_wrap.sv:164-169`, its Decision at
  `:20-27`); peer LeaveAll MRPDUs then offer each FIFO 36 or more ops, and the stall is released.
- **Verilator 5.050** faults (internal fault, signal 11) on a hierarchical reference to `KL_srp_top`'s enum item
  `u_dut.TM_SEL`, with or without the force; the wrap names the encoding instead (`TB_TM_SEL_C = 1'b0`,
  `srp_store_wrap.sv:105-107`).

| Check | What it proves |
|---|---|
| TF1 | the talker FIFO issues every op it accepted once, in order, unmodified: none lost, reordered, altered, duplicated or invented, and every queued word drains |
| TF2 | the same for the listener FIFO |
| TF3 | no op is refused while the issue runs unforced |
| TF4 | held, the talker FIFO accepts exactly 32 ops and refuses the rest; released, it issues those 32 in order |
| TF5 | the same for the listener FIFO |

Positive, at the head (the `control srp_top storage` receipt), 15 checks at each shape, all PASS:

| Shape | First arm: offered (= issued), talker / listener | Clocks with both offering | Two-word selections, talker / listener | Held arm: MRPDUs; offered; refused |
|---|---|---:|---|---|
| 1/1 | 3 / 4 | 2 | 1 / 0 | 18; 36 / 36; 4 / 4 |
| 2/2 | 7 / 8 | 4 | 2 / 1 | 9; 36 / 36; 4 / 4 |
| 3/5 | 11 / 20 | 7 | 4 / 7 | 6; 36 / 60; 4 / 28 |
| 9/9 | 35 / 36 | 18 | 19 / 15 | 2; 36 / 36; 4 / 4 |

#### R2.4.3 Admission slopes

`slope_q_r` has no arms: it is distributed RAM at every shape, and the committed admission suite already runs at 1, 2,
3, 5 and 8 sources (12,615 / 41,012 / 201,073 / 991,231 checks above one source). Its slope controls are R2.4.4's last
four rows.

#### R2.4.4 The 33 controls, row by row

`tb/srp_top/mutants.py` at the head (`7365022`, the receipts of the README table; `1199255` changes only that README):
**rc 0, 126 checks: 126 PASS, 0 FAIL, assertion coverage 78/78** (999 s, `--jobs 3`). The 84 labels of round 1 (11
controls and 73 arm labels over 78 runs) give the same verdict, failure count and failing checks as round 1's head record (`90 checks: 90
PASS`, coverage 65/65); the 36 new labels are 3 positive controls and 33 KILLED arms. Each arm is killed by its named
check. Failing checks per shape (the `[sources/sinks]` suffix of each failing line); "n/e": the edited arm is not
elaborated; "equivalent": one source or sink, the edit names it; "equivalent in simulation": at one sink the parked
control index (WK6) is the face's only out-of-range value, and Verilator 5.050 reads a single 64-bit packed element at
an out-of-range index as element 0 (a 48-bit element reads 0: checked with a small module), so that edit also reads
sink 0.

| Control | From | Edit | Named failing checks | 1/1 | 2/2 | 3/5 | 9/9 | Caught at |
|---|---|---|---|---:|---:|---:|---:|---|
| `tf-heads-swapped` | A523, R458-1 | each FIFO head reads the other FIFO's memory | TF1, TF2 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-head-at-write-pointer` | A523 | talker head read at `wptr - 1`, the newest word | TF1, TF4 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-listener-push-dropped` | A523 | listener push lost when both FSMs push | TF2 | 1 | 1 | 1 | 1 | 4 of 4 |
| `tf-ls-written-at-tk-pointer` | R458-1 | listener word written at the talker's write pointer | TF2, TF5 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-tk-head-read-ahead` | R458-1, R459-1 (`tf-tk-head-reads-next`) | talker head read at `rptr + 1` | TF1, TF4 | 4 | 4 | 3 | 2 | 4 of 4 |
| `tf-ls-head-reads-tk-ram` | R459-1 | listener head reads the talker memory | TF1, TF2, TF3, TF4, TF5 | 4 | 4 | 4 | 5 | 4 of 4 |
| `tf-tk-write-at-rptr` | R459-1 | talker word written at the read pointer | TF1, TF4 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-full-guard-31` | R458-1 | talker full guard at 31 words | TF4 | 1 | 1 | 1 | 1 | 4 of 4 |
| `tf-tk-write-ignores-full` | R459-1 (stall probe) | talker memory written while full | TF4 | 1 | 1 | 1 | 1 | 4 of 4 |
| `tf-ls-write-ignores-full` | R459-1 | listener memory written while full | TF5 | 1 | 1 | 1 | 1 | 4 of 4 |
| `walk-record-written-on-close` | A523, R459-1 (`wtsp-written-on-close`) | walk records also written by a gate close | WK3 | 1 | 1 | 1 | 1 | 4 of 4 |
| `wtsp-first-open-only` | A523, R458-1 | walk TSpec written only by a source's first open | WK2, WK3, WK4 | 3 | 5 | 7 | 19 | 4 of 4 |
| `wtsp-read-at-gate-source` | A523, R458-1 | walk TSpec read at the gate source | WK1, WK2, WK4 | 1 | 4 | 9 | 33 | 4 of 4 |
| `wtsp-read-at-source-0` | R459-1 | walk TSpec read at source 0 | WK1, WK2, WK3, WK4, WK5 | 0 (equivalent) | 6 | 10 | 34 | 3 of 4 |
| `wtsp-latency-field-shifted` | A523 | latency read one bit off (`wtsp_w[32:1]`) | WK1, WK2, WK3, WK4, WK5 | 6 | 10 | 14 | 38 | 4 of 4 |
| `wtsp-latency-shifted` | R458-1 | latency shifted left one bit | WK1, WK2, WK3, WK4, WK5 | 6 | 10 | 14 | 38 | 4 of 4 |
| `wtsp-rank-dropped` | R458-1 | rank bit published as 0 | WK1, WK2, WK3, WK4, WK5 | 3 | 5 | 6 | 19 | 4 of 4 |
| `wtsp-prio-rank-swapped` | R459-1 | priority and rank bits rotated | WK1, WK2, WK3, WK4, WK5 | 5 | 9 | 13 | 34 | 4 of 4 |
| `wid-ram-first-open-only` | A523, R458-1 | RAM {stream_id, DA, VLAN} written only by the first open | WK2, WK3, WK4 | 0 (n/e) | 0 (n/e) | 7 | 19 | 2 of 4 |
| `wid-ram-read-at-gate-source` | A523, R458-1 | RAM {stream_id, DA, VLAN} read at the gate source | WK1, WK2, WK4 | 0 (n/e) | 0 (n/e) | 9 | 33 | 2 of 4 |
| `wid-ram-read-neighbour` | R459-1 | RAM {stream_id, DA, VLAN} read at the previous source | WK1, WK2, WK3, WK4, WK5 | 0 (n/e) | 0 (n/e) | 14 | 38 | 2 of 4 |
| `wid-flops-da-of-gate-source` | A523, R458-1 | flop arm reads the gate source's DA | WK1, WK2, WK4 | 1 | 4 | 0 (n/e) | 0 (n/e) | 2 of 4 |
| `wid-flops-sid-of-source-0` | R458-1 | flop arm reads source 0's stream_id | WK1, WK2, WK3, WK4, WK5 | 0 (equivalent) | 6 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `wid-flops-vid-of-source-0` | R459-1 | flop arm reads source 0's VLAN | WK1, WK2, WK3, WK4, WK5 | 0 (equivalent) | 6 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `talker-vid-unreset` | A523 | the matcher VLAN loses its reset (a stored value read without its valid bit) | WK5 | 1 | 1 | 1 | 1 | 4 of 4 |
| `wsid-ram-first-settle-only` | A523, R458-1 | RAM stream_id written only by the first settle | WK8 | 0 (n/e) | 0 (n/e) | 5 | 9 | 2 of 4 |
| `wsid-ram-written-on-teardown` | A523, R458-1, R459-1 | RAM stream_id also written by a teardown | WK7 | 0 (n/e) | 0 (n/e) | 1 | 1 | 2 of 4 |
| `wsid-flops-of-control-sink` | A523, R458-1 | flop arm reads the control sink's stream_id | WK6, WK8 | 0 (equivalent in simulation) | 3 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `wsid-flops-read-sink-0` | R459-1 | flop arm reads sink 0's stream_id | WK6, WK7, WK8 | 0 (equivalent) | 4 | 0 (n/e) | 0 (n/e) | 1 of 4 |

Slope controls, the admission suite one shape at a time (its `shapes` target stops at the first failing shape, so the
campaign itself sees N = 2), failing checks of the shape's total:

| Control | From | Edit | N = 1 | N = 2 | N = 3 | N = 5 | N = 8 | Caught at |
|---|---|---|---:|---:|---:|---:|---:|---|
| `slope-stored-at-stage-2-index` | A523, R458-1, R459-1 (`slope-store-at-stage-1-index`) | slope written at `cidx_q1_r`, not `cidx_q2_r` | 0 (equivalent) | 1,333 of 12,615 | 4,109 of 41,012 | 12,760 of 201,073 | 38,919 of 991,231 | 4 of 5 |
| `slope-stored-at-source-0` | R458-1 | every slope written to source 0 | 0 (equivalent) | 1,521 of 12,615 | 3,915 of 41,012 | 12,415 of 201,073 | 39,056 of 991,231 | 4 of 5 |
| `slope-store-source-0-only` | A523 | only source 0's slope stored | 0 (equivalent) | 1,201 of 12,615 | 3,163 of 41,012 | 10,281 of 201,073 | 33,958 of 991,231 | 4 of 5 |
| `slope-read-source-0` | R459-1 | the admission walk reads source 0's slope | 0 (equivalent) | 578 of 12,615 | 1,683 of 41,009 | 6,125 of 201,068 | 22,202 of 991,223 | 4 of 5 |

So, row by row as the table shows: 18 controls are caught at all four shapes; one at three
(`wtsp-read-at-source-0`, which names source 0, the only one at 1/1); six at two (the five RAM-arm controls at 3/5 and
9/9, and `wid-flops-da-of-gate-source` at 1/1 and 2/2); four at one (the flop-arm reads of context 0 and of the control
sink, at 2/2); and the four slope controls at four of the admission suite's five shapes (not at one source).
Against round 1's lockstep, the committed arms now also catch `tf-head-at-write-pointer` and
`tf-listener-push-dropped` at 1/1 (the assignment's two FIFO controls) and, at every shape, the full-guard edits, which
no round-1 control or run reached.

The three edits R459-1 planted as equivalent stay silent in every suite that builds the edited file:
`tf-tk-same-entry-bypass`, `wid-threshold-ram-from-1` and `wid-threshold-flops-always` pass `srp_top` and
`srp_stream_fsms` with every new arm (R2.4.5), and `tb/pp_top` too (10,416 checks: 10,416 PASS each, 531 to 539 s).

#### R2.4.5 The bar: both reviews' probes, run unchanged

**R458-1** (`lockstep/probes.py`, unchanged; base `git archive c4cb84ff`, head `git archive 1199255`, its
`verilator-jcap.sh` wrapper over the pinned Verilator 5.050; rc 0, 1,177 s). The evidence branch stores its helper scripts
without execute bits (mode 100644), so `chmod +x` was the one change; their content matches R458-1's `MANIFEST.sha256`.
A probe is caught when a committed suite's `make` exits nonzero.

| Probe | At `65324390` (R458-1's receipt): srp_top / second suite | At the head: srp_top | At the head: second suite | R458-1's own lockstep, at the head |
|---|---|---|---|---|
| `tf-heads-swapped` | caught (rc 2) / - | caught (rc 2) | - | top 525717/833 out/int mismatching cycles |
| `tf-ls-written-at-tk-pointer` | caught (rc 2) / - | caught (rc 2) | - | top 32241/98 out/int mismatching cycles |
| `tf-tk-head-read-ahead` | caught (rc 2) / - | caught (rc 2) | - | top 348827/473 out/int mismatching cycles |
| `tf-full-guard-31` | passes / - | caught (rc 2) | - | top 0/0 out/int mismatching cycles |
| `wtsp-read-at-gate-source` | passes / passes | passes | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 0 / 470,380 / 619,031 / 808,622 |
| `wtsp-first-open-only` | passes / passes | passes | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 898,584 / 898,047 / 897,357 / 893,001 |
| `wtsp-latency-shifted` | caught (rc 2) / passes | caught (rc 2) | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 898,899 / 898,921 / 898,897 / 898,885 |
| `wtsp-rank-dropped` | caught (rc 2) / caught (rc 2) | caught (rc 2) | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 450,370 / 450,022 / 451,897 / 451,156 |
| `wid-ram-first-open-only` | passes / passes | passes | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 0 / 0 / 868,559 / 862,702 |
| `wid-ram-read-at-gate-source` | caught (rc 2) / passes | caught (rc 2) | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 0 / 0 / 599,869 / 783,964 |
| `wid-flops-da-of-gate-source` | passes / passes | passes | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 0 / 234,096 / 0 / 0 |
| `wid-flops-sid-of-source-0` | passes / passes | passes | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 0 / 597,592 / 0 / 0 |
| `wsid-ram-first-settle-only` | passes / passes | passes | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 0 / 0 / 780,610 / 779,923 |
| `wsid-ram-written-on-teardown` | passes / passes | passes | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 0 / 0 / 237,301 / 200,595 |
| `wsid-flops-of-control-sink` | passes / passes | passes | srp_stream_fsms: caught (rc 2) | N=1/2/3/9: 0 / 420,237 / 0 / 0 |
| `slope-stored-at-stage-2-index` | caught (rc 2) / caught (rc 2) | caught (rc 2) | srp_admission: caught (rc 2) | N=1/2/3/9: 0 / 339,741 / 426,104 / 580,575 |
| `slope-stored-at-source-0` | caught (rc 2) / caught (rc 2) | caught (rc 2) | srp_admission: caught (rc 2) | N=1/2/3/9: 0 / 226,940 / 330,263 / 559,213 |

All 17 are caught by a committed suite at the head, the eight that survived at `65324390` included (WK1-WK8 in
`srp_stream_fsms`), and `tf-full-guard-31`, which R458-1 left as S1 (TF4 in `srp_top`). Its own lockstep results equal
its receipt cell for cell: the RTL is the same.

**R459-1** (`scripts/make_controls.py`, unchanged, run on the head's `hdl/srp`; rc 0, "ALL OK", 1,942 s). Each
control replaces `hdl/srp` in a copy of the head tree, and every SRP suite that builds the edited file runs with its full
default `make` (`srp_top`; `srp_stream_fsms` for the stream FSMs, `srp_admission` for admission; R458-1's mapping),
so the new arms run inside them. "Failing" sums the failing checks over the suite's tallies.

| Control | Declared | srp_top | Second suite | Verdict |
|---|---|---|---|---|
| `tf-ls-head-reads-tk-ram` | catch | rc 2, 24 failing | - | caught, as declared |
| `tf-tk-head-reads-next` | catch | rc 2, 14 failing | - | caught, as declared |
| `tf-ls-write-ignores-full` | catch-at-full | rc 2, 4 failing | - | caught, as declared |
| `tf-tk-write-at-rptr` | catch | rc 2, 9 failing | - | caught, as declared |
| `tf-tk-same-entry-bypass` | equiv | rc 0, passes | - | passes, as declared |
| `wtsp-written-on-close` | catch | rc 2, 2 failing | srp_stream_fsms: rc 2, 4 failing | caught, as declared |
| `wtsp-prio-rank-swapped` | catch | rc 2, 2 failing | srp_stream_fsms: rc 2, 82 failing | caught, as declared |
| `wtsp-read-at-source-0` | catch | rc 2, 1 failing | srp_stream_fsms: rc 2, 50 failing | caught, as declared |
| `wid-ram-read-neighbour` | catch | rc 2, 26 failing | srp_stream_fsms: rc 2, 94 failing | caught, as declared |
| `wid-flops-vid-of-source-0` | catch | rc 0, passes | srp_stream_fsms: rc 2, 6 failing | caught, as declared |
| `wid-threshold-ram-from-1` | equiv | rc 0, passes | srp_stream_fsms: rc 0, passes | passes, as declared |
| `wid-threshold-flops-always` | equiv | rc 0, passes | srp_stream_fsms: rc 0, passes | passes, as declared |
| `wsid-ram-written-on-teardown` | catch | rc 0, passes | srp_stream_fsms: rc 2, 2 failing | caught, as declared |
| `wsid-flops-read-sink-0` | catch | rc 0, passes | srp_stream_fsms: rc 2, 4 failing | caught, as declared |
| `slope-store-at-stage-1-index` | catch | rc 2, 673 failing | srp_admission: rc 2, 1,333 failing | caught, as declared |
| `slope-read-source-0` | catch | rc 2, 217 failing | srp_admission: rc 2, 578 failing | caught, as declared |

Its stall probe is not a defect but a stimulus (the same edit in both models); its one defect under the stall,
`tf-tk-write-ignores-full`, is a planted control (killed by TF4). The committed held arm replaces the stall.

#### R2.4.6 Packet

`lockstep-r1/` in this directory: the round-1 bench and its controls as they ran (`gen_top.py`, `lockstep_main.cpp`,
`build.sh`, `campaign.sh`, `make_controls.py`, `run_controls.sh`, both final logs and rc files), `make_ref.py` (written
for the packet; it rebuilds `ref/` from `git archive c4cb84ff` byte for byte, checked with `diff -r`), a README and
`MANIFEST.sha256`. 13 files, 92 KB.

| File | SHA-256 |
|---|---|
| `build.sh` | `822204c3daf8be315b7f49cfb7feaa2f47537a98ecf022c656b55121ef32a774` |
| `campaign-final.log` | `52b707744cf948e046d026acbb45c0e337c5b6a3eb171828934eca71bae5337a` |
| `campaign-final.rc` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `campaign.sh` | `654ca3eea663f91f4e90255e69edb691f10fd191ba7b1a9c358173dae1b9f93e` |
| `controls-final.log` | `536cdd3ab7faa066620da666be8c47508e1c546ae68ee200c430cb09815dd896` |
| `controls-final.rc` | `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` |
| `gen_top.py` | `37e13f65c48cf82d80fe8f44a71c8943c02f60e385f5c847d09fb9abea8aeb97` |
| `lockstep_main.cpp` | `eda930b367eaed36eef0968679206e44507ac3c061f8258ae99234ae0d951a49` |
| `make_controls.py` | `0547433a18153166bd8169afb4690e71eeefcc9b4f116ef1684c24b1152b1822` |
| `make_ref.py` | `34cb53a77576b840bfb9c9877051f31e427f1f9d9e8e6424937cb22cbdded39b` |
| `README.md` | `850aafed696250ba3dece6e02ecc2f435dc621e07119c65f91f74b1fc84dac8f` |
| `run_controls.sh` | `85be3a023b74871a79cb44dc1ef23aee3f5e0ddf3dbd5edd63e886640ffffaaa` |
| `MANIFEST.sha256` (the twelve above) | `ba39be98de52d432c90736a82e861db5bd65571446611ed04a43f87e400d9cf2` |

### R2.5 Item 2: the control count

- Round 1's section 4.2 now carries a "Caught at" column, row by row, and its summary reads: caught at one to four of
  the four shapes, six controls at four, four at three, five at two and one (`wsid-flops-of-control-sink`) at one. The
  old sentence ("each at three or four shapes") is quoted as corrected.
- The committed controls are R2.4.4's table; the PR body carries that table and the round-1 counts.

### R2.6 Item 3: residue

- **R1** (PR body "10 section 5.1"): every mention in PR-BODY.md now names `docs/architecture/10_srp_engine.md`
  section 5.1 (the three places R459-1 listed, and the new text).
- **R2** (the "all rc 0" header): PR-BODY.md's header reads "Validation (all rc 0 except parent gate 16, recorded
  against #643; no pipes)", because gate 16 still exits 2 on #643's two T30 checks.
- **S1**: one sentence, `docs/guides/hdl-engineer.md:88-93`: the walk copies (`wtsp_r`, `g_wid_ram.wid_r`,
  `g_wsid_ram.wsid_r`), `slope_q_r` and the FIFOs `tf_tk_ram_r`, `tf_ls_ram_r`, and which read is registered.

### R2.7 Item 4: the merge of `main` `83999eba`

- `4994ada`, parents `65324390` and `83999eba`; no conflict (the branch touched `hdl/srp` and
  `docs/architecture/10_srp_engine.md` only, `main` neither).
- It brings C10 (PR #149: `protocol_processor_top.sv` declaration order, the Yosys gate's parse-once census,
  `KL_pp_nvm_port`'s `MAX_PAYLOAD_P` bound, the dispatch campaign's SET_CLOCK_SOURCE arms) and #85 (PR #152: the ADP
  engine's available_index comments and walk tests).
- **No SRP HDL**: `git diff 83999eba 1199255 -- hdl` lists only the four SRP files of `25847d07`. So the area claims
  stay as round 1 measured them, base `c4cb84ff` against head, as a delta (sections 1 and 5); no Vivado run was
  repeated.
- **What it touches, re-run** (targeted, per the #232 rule: every input the merge changed): every processor suite (it
  changes `pp_top`, `adp_engine`, `nvm_port`), the Yosys gate (`syn/yosys/run.sh`), every campaign that builds
  `protocol_processor_top` (the pp_top campaigns, maap and adp with their pp_top arms), the adp campaign (new arms),
  nvm_port's elaboration bounds (in its suite) and figures gate, and the parent consumer set with c10.

### R2.8 Gates at the head

Processor, at `7365022` (`1199255` adds only the srp_top README's re-measured table; the docs gates ran at
`1199255`). Every command without a pipe; log and rc per run in the scratch.

| Command | Result |
|---|---|
| `./scripts/lint_hdl.sh` | rc 0, 41 of 41 (13 s) |
| `./scripts/run_suites.sh` | rc 0, 33 suites, 1,021,469 checks, 0 failing (1,124 s). Against round 1's head: `adp_engine` 1,328 -> 1,348 and `pp_top` 10,390 -> 10,416, both from the merge; every other suite equal, the SRP suites' tallies included (srp_top 2,200, srp_stream_fsms 1,219, srp_admission 991,231; the new arms print their tallies before each) |
| `make check` (at `1199255`) | rc 0: 41 mermaid + 18 wavedrom blocks, 1,131 links, 115 REQ rows, 94 matrix rows 0 untested, 28 parameters |
| `python3 scripts/gen_matrix.py --check` (at `1199255`) | rc 0, 94 rows, 0 untested (the matrix is unchanged: the new builds use modules the benches already listed) |
| `./syn/yosys/run.sh` (at `1199255`) | rc 0: 42 tops `YOSYS OK`, `KL_aecp_engine` Xilinx mapping OK, one parse (41 s) |

Campaigns (`--jobs 3` or `4`):

| Campaign | Tree | Result | Against the record |
|---|---|---|---|
| `tb/srp_top/mutants.py` | head | rc 0, 126 checks: 126 PASS, assertion coverage 78/78 (999 s) | round 1's 84 labels identical; 36 new (R2.4.4) |
| `tb/srp_admission/mutants.py` | head | rc 0, 12 checks: 12 PASS (402 s) | identical to round 1 |
| `tb/adp_engine/mutants.py` | merge `4994ada` | rc 0, 43 checks: 43 PASS (201 s) | README: both controls and all 41 arms killed (#85's arms) |
| `tb/maap/mutants.py` | merge | rc 0, 32 PASS (94 s) | as round 1 |
| `tb/pp_top/ctr_mutants.py` | merge | rc 0, 18 PASS (166 s) | as round 1 |
| `tb/pp_top/notify_mutants.py` | merge | rc 0, 40 of 40 KILLED, goldens PASS (465 s) | as round 1 |
| `tb/pp_top/acmp_mutants.py` | merge | rc 0, 19 of 19 KILLED, goldens PASS (140 s) | as round 1 |
| `tb/pp_top/aecp_mutants.py` | merge | rc 0, 60 PASS (422 s) | as round 1 |
| `tb/pp_top/aecp_dispatch_mutants.py` | merge | rc 0, 44 PASS (394 s) | round 1's 41 plus C10's three NSD arms (README) |
| `tb/pp_top/d3_mutants.py` | merge | rc 0, 110 of 110 KILLED, goldens PASS (2,936 s) | as round 1 |
| `tb/pp_top/gsi_mutants.py` | merge | rc 0, 20 detected by named checks, golden and restored PASS (415 s) | as round 1 |
| `tb/pp_top/name_wr_mutant.py` | merge | rc 0, decode killed, golden and restored PASS (51 s) | as round 1 |
| `make -C tb/nvm_port figures` | the lane checkout at the head, after `git fetch origin refs/pull/13/head` as CI does | rc 0, "all measured figures agree with the tree" (160 Verilator builds, 903 s). A first run without PR #13's ref failed only its git-form pins ("cannot read dc354be~1"), every figure matching | |

Parent consumer set: scratch parent at dev `241f91845230ae410506dffb16b71937127fd175` (detached; submodules `external`
`efeb541a`, `gptp-processor` `5dce647a`, `third_party/verilog-axis` `48ff7a7e`), the processor gitlink set in the index
only to `1199255` with its checkout detached there, and `parent-adoption-c8-bbf704ec.patch`,
`parent-adoption-p2-p1-1269cdaf.patch` and `parent-adoption-c10-1269cdaf.patch` (sha256 `3340d2e8...a38a4c`,
`d3034e89...613d84`, `55e62329...74ea34b9`) applied with `git apply --check` then `git apply`. Never committed or
pushed. GNU Make 4.3 and the pinned Verilator 5.050 first on PATH.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | 174 translation units (the two new harnesses included), every ratchet held |
| 2 | `scripts/check_py_idiom.py` | 0 | 307 modules, every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files in the `milan_datapath` closure, 4 of 4 consumer lists; processor 42/42 tops |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports, undocumented 111 <= 111 |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | within ratchets |
| 8 | `scripts/docs_check.py` | 0 | 0 findings, 187 md + 975 files |
| 9 | `scripts/xvlog_gate.py --check` (alone, under the Vivado lock) | 0 | PASS: 3 findings == ratchet (0 in `hdl/`, 3 in the pinned processors: `KL_aecp_notify.sv:557` `pd_ix_w`, `KL_pp_originator.sv:194` `cancel_hit_w`, `KL_pp_rx_validator.sv:383` `vd_push_w`, each used before its declaration), analysed at `protocol-processor@1199255b` (6,521 s, nearly all of it waiting for another lane's held lock). Round 1 counted 4: C10 moved one declaration, and the c10 patch sets the ratchet to 3 |
| 10 | `sw/builder/test_builder.py` | 0 | GNU Make 4.3: "ALL GATES PASS EXCEPT 2 NOT RUN": gate 11 needs the local mf48 build tree, and gate 1b's `MAKEFLAGS += -e` mutation, which Make 4.3 does not re-read mid-parse (1,178 s); identical to round 1. With the host's GNU Make 4.4.1: rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11 only, as in P1's record) (1,125 s) |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 violations <= ratchet 90 |
| 12 | `make -C tb/verilator/pp_shadow -j16` | 0 | 311 checks, 0 failures (287 s) |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j16 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS, 0 FAIL; 4 render mutants caught; gmstep controls 6 of 6 (2,389 s) |
| 16 | `make -C tb/verilator/milan_dp_render -j16` | 2 | two-stream leg 65 checks, 0 failures; shipping leg 155 checks, **2 failures, both T30 INTERNAL LAW**: the fill at accept 227 of 292, the first event in the law band 285 of 292, first-event delay 18,396..18,821 cycles = 8.830..9.034 media ticks (215 s). Exactly #643's checks and P1 figures, as in round 1 at dev `5fabb46e` (base and head alike there); recorded against #643 / milan-fpga PR #648 |


### R2.9 Notes

- **The one forced state.** The srp_top suite's own banner says no DUT state is forced. The FIFO arms keep that for
  every arm but the held one, and say so in the wrap's Decision and in the README; the held arm forces only the issue
  state, and the scoreboard checks that nothing issues while held (TF4 precondition).
- **Verilator.** The fault on the hierarchical enum item and the 64-bit aliasing are simulator behaviours, recorded in
  the wrap and the README; neither touches the RTL.
- **nvm_port figures** read git history (their matrix pins name revisions of PR #13, squash-merged), so that gate ran
  in the lane checkout at the head after `git fetch --no-tags origin refs/pull/13/head`, as CI runs it. A run in a `git
  archive` copy, and one in the checkout without that ref, failed only those pins ("cannot read dc354be~1"), every
  figure matching.
- **Interrupted and superseded runs.** A command of mine stopped some background runs mid-way (a process-name match on
  my own command line), and runs started at earlier round-2 heads were superseded. Every result above is from a run
  that completed undisturbed at the head, or, for the campaigns the merge touches, at the merge commit `4994ada`, whose
  inputs to them equal the head's (`git diff 4994ada 1199255 -- hdl tb/common tb/pp_top tb/maap tb/adp_engine
  tb/nvm_port syn scripts` is empty): adp to name_wr finished before the interruption, d3 after it.
- **Memory.** This unit reached its 12 GB cap during parallel builds (`memory.events` max 145,930, oom 0, oom_kill 0).
- **Make.** The parent gates ran with GNU Make 4.3 (the hosted runner's) first on PATH, as in round 1, and the builder
  gate also with the host's Make 4.4.1 (P1's record).

## Round 3

Status: **REVIEW READY** at head `d18270d69eea9cdf35f846c77821d5488dab97cc` (branch `pp230-srp-area`, not pushed).

- REVIEW READY posted: kebag-logic/milan-fpga#230 comment 5981062645.
- Assignment: kebag-logic/milan-fpga#230 comment 5980793710, after R458-3 (processor PR #154 comment 5980789211,
  NEGATIVE on one MINOR, F1, test coverage) and R459-3 (POSITIVE). R458-3's packet (probe diffs, its disposable stall
  arm and log) was read from the parent's `pp230-review-evidence` branch at `151666f1`, in a scratch fetch.
- Test-only: no HDL change, no port, parameter, register or behaviour change. One-line commits on top of `b59e99cb`,
  no rebase, no amend. `git diff b59e99cb d18270d6 -- hdl scripts syn` is empty.

### R3.1 Items and outcome

| Item | Outcome |
|---|---|
| 1. R458-3-F1 | done: WK9 (talker) and WK10 (listener) in `tb/srp_stream_fsms/walk_main.cpp`; R458-3's two probes are killed controls `wtsp-write-ignores-ready` and `wsid-write-ignores-ready` with checked-in patches; both READMEs' tables and counts updated; coverage tags WK1-WK10. The bar holds (R3.4) |
| 2. R458-3-R1 | done as written: `docs/guides/hdl-engineer.md:88-94`, the lead-in replaced word for word and lines 88-93 rewrapped to the block's width (now 88-94, at most 86 columns) |
| 3. PR-BODY.md | a "Round 3" section; the round-2 counts that change brought up to date (35 controls, campaign 128/128, coverage 80/80, walk arms 35/46/67/123, the control table and its row-by-row line); the commit table, header and Validation updated |
| Gates | `tb/srp_stream_fsms` (walk arms 35, 46, 67, 123; suite 1,219), `tb/srp_top` (15 per shape; 2,200), `pp_top` (10,416) inside `run_suites.sh`; the srp_top campaign; `make check`; `gen_matrix --check`; `lint_hdl.sh`; the parent gates that read the changed files (R3.7) |

### R3.2 Commits on top of `b59e99cb`

| Commit | Subject |
|---|---|
| `7f7104f` | Walk the #230 records with a gate open and a settle offered under a busy decoder bus (WK9, WK10) |
| `d562ac2` | Plant R458-3's two ready-handshake probes of the #230 walk-copy writes as killed controls of the srp_top campaign |
| `fb06a93` | Table WK9, WK10 and R458-3's two controls in the #230 READMEs, re-measured from the campaign at d562ac2 |
| `d18270d` | Narrow the hdl-engineer storage-rule lead-in to the per-context records the SRP walks read (R458-3-R1) |

### R3.3 Changes (file:line at `d18270d`)

| File:line | Change |
|---|---|
| `tb/srp_stream_fsms/walk_main.cpp:29-35` | banner: WK9 and WK10 |
| `tb/srp_stream_fsms/walk_main.cpp:175-184` | `bus_busy`, `gate_held`, `ctl_held`; `gate_taken`, `ctl_taken` count the clocks an offer meets its ready |
| `tb/srp_stream_fsms/walk_main.cpp:190-197` | `step()`: while `bus_busy`, an MVRP decoder value (`evt_valid_i` 1, `evt_msrp_i` 0, which neither FSM matches: `KL_srp_talker_fsm.sv:416-425`, `KL_srp_listener_fsm.sv:406-412`) every clock; a held offer re-asserted every clock; offers taken counted before the edge |
| `tb/srp_stream_fsms/walk_main.cpp:233-260` | `drive_gate` and `drive_ctl` (the face's fields without an offer); `gate`, `ctl`, `park_gate`, `park_ctl` now call them (same assignments as before) |
| `tb/srp_stream_fsms/walk_main.cpp:308-309` | `run()` calls the two new arms after WK1-WK8 |
| `tb/srp_stream_fsms/walk_main.cpp:440-446` | `release_bus()`: the bus goes idle with the offer still held (taken in that clock), then the offer drops |
| `tb/srp_stream_fsms/walk_main.cpp:448-471` | WK9: every source declared (phase 5), then the open of source `M-1` with its phase-6 record offered from the own LeaveAll through the txLA! walk under the busy bus; precondition (the walk completes, 0 offers taken), `expect_talker` (the old records), the open taken once when the bus goes idle, then a txLA! walk publishing the new record |
| `tb/srp_stream_fsms/walk_main.cpp:473-503` | WK10: the same for sink `N-1`'s settle on its phase-6 stream; after the settle is taken, a Talker Advertise registers the new stream (as WK8) and the next walk publishes it |
| `tb/srp_top/mutants.py:142-143` | two rows, `srp_stream_fsms` group `walk`, named checks `WK9:` and `WK10:` |
| `tb/srp_top/mutants.py:245` | assertion coverage requires WK1-WK10 (80 tags) |
| `tb/srp_top/mutations/wtsp-write-ignores-ready.patch` (new) | `KL_srp_talker_fsm.sv:498` `gate_acc_w` -> `gate_valid_i` (feeds `wtsp_r` and `g_wid_ram.wid_r`) |
| `tb/srp_top/mutations/wsid-write-ignores-ready.patch` (new) | `KL_srp_listener_fsm.sv:544` `ctl_acc_w` -> `ctl_valid_i` |
| `tb/srp_stream_fsms/README.md:200-207`, `:212` | WK9, WK10 rows; why they hold the ready low; 35, 46, 67 and 123 checks |
| `tb/srp_top/README.md:558-567`, `:579-610`, `:623-624` | R458-3 named, 35 patches, WK1-WK10; the control table re-measured, two new rows; "R458-3" in the From legend |
| `docs/guides/hdl-engineer.md:88-94` | R458-3-R1, as written |

The two patches' edit lines equal R458-3's published probe diffs (`receipts/probe-r3-*-write-ignores-ready.diff`)
byte for byte; the headers are the repository's `a/` `b/` form. `git apply --check` is clean on the head. The labels
drop R458-3's round prefix (`r3-`); the README and PR body name the originals in "From".

### R3.4 Tests, controls and the bar

| Check | What it proves | Red proof (failing control) |
|---|---|---|
| WK9 | a gate open of another record for the last source, offered while decoder values hold `gate_ready_o` low through a txLA! walk, is not taken: that walk publishes the declared records; the open is taken once, in the clock the bus goes idle; the next walk publishes the new record | `wtsp-write-ignores-ready` (R458-3 `r3-wtsp-write-ignores-ready`): 1 failing check at each of 1/1, 2/2, 3/5, 9/9, "WK9: push M-1 carries its source's declared record" |
| WK10 | the same for a settle of the last sink on another stream while `ctl_ready_o` is held low | `wsid-write-ignores-ready` (R458-3 `r3-wsid-write-ignores-ready`): 1 failing check at 3/5 and 9/9, "WK10: push N-1 carries its sink's settled stream_id"; 1/1 and 2/2 pass, the RAM arm is not elaborated there (n/e) |

- **Head** (the campaign's `control srp_stream_fsms walk` receipt, and `make` at the head): 35, 46, 67 and 123 checks
  at 1/1, 2/2, 3/5 and 9/9, all PASS (round 2: 23, 30, 43, 79; WK9 adds 4 + 2M checks, WK10 4 + 2N).
- **First run** (scratch copies of the working tree, `make RUN_ARGS=walk`, before the commit): the same three results,
  rc 0 / 2 / 2; the build has no compiler or Verilator warning.
- **The bar, as stated**: talker control fails the new check at 4 of 4 shapes; listener control at 3/5 and 9/9, n/e
  at 1/1 and 2/2; the head passes; the campaign stays all-PASS with WK9 and WK10 in its coverage; `make check` passes.
  R458-3's own disposable arm (`r3-stall-arm.log`) failed the same pushes (push 0, 1, 2, 8 talker; push 4, 8 listener).
- **The refactor is neutral**: in all 120 control receipts, the FAIL lines other than WK9/WK10 equal round 2's
  receipts line for line (round 2's campaign receipts at `7365022` against round 3's at `d562ac2`).

Campaign (`tb/srp_top/mutants.py --jobs 4`, `git archive d562ac2`, the pinned Verilator 5.050): **rc 0, 128 checks: 128
PASS, 0 FAIL, assertion coverage 80/80** (769 s). Against round 2's receipt (126/126, 78/78), every verdict line is
the same except the walk group's failure counts and the two new KILLED rows. 17 walk controls also fail WK9 or WK10,
each only at shapes where it was already caught, so no "Caught at" cell changes. Rows by the README's table:
19 controls at four shapes, one at three, seven at two, four at one; the slope controls at four of five.

| Control | From | Edit | Named failing checks | 1/1 | 2/2 | 3/5 | 9/9 | Caught at |
|---|---|---|---|---:|---:|---:|---:|---|
| `tf-heads-swapped` | A523, R458-1 | each FIFO head reads the other FIFO's memory | TF1, TF2 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-head-at-write-pointer` | A523 | talker head read at `wptr - 1`, the newest word | TF1, TF4 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-listener-push-dropped` | A523 | listener push lost when both FSMs push | TF2 | 1 | 1 | 1 | 1 | 4 of 4 |
| `tf-ls-written-at-tk-pointer` | R458-1 | listener word written at the talker's write pointer | TF2, TF5 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-tk-head-read-ahead` | R458-1, R459-1 (`tf-tk-head-reads-next`) | talker head read at `rptr + 1` | TF1, TF4 | 4 | 4 | 3 | 2 | 4 of 4 |
| `tf-ls-head-reads-tk-ram` | R459-1 | listener head reads the talker memory | TF1, TF2, TF3, TF4, TF5 | 4 | 4 | 4 | 5 | 4 of 4 |
| `tf-tk-write-at-rptr` | R459-1 | talker word written at the read pointer | TF1, TF4 | 2 | 2 | 2 | 2 | 4 of 4 |
| `tf-full-guard-31` | R458-1 | talker full guard at 31 words | TF4 | 1 | 1 | 1 | 1 | 4 of 4 |
| `tf-tk-write-ignores-full` | R459-1 (stall probe) | talker memory written while full | TF4 | 1 | 1 | 1 | 1 | 4 of 4 |
| `tf-ls-write-ignores-full` | R459-1 | listener memory written while full | TF5 | 1 | 1 | 1 | 1 | 4 of 4 |
| `walk-record-written-on-close` | A523, R459-1 (`wtsp-written-on-close`) | walk records also written by a gate close | WK3 | 1 | 1 | 1 | 1 | 4 of 4 |
| `wtsp-first-open-only` | A523, R458-1 | walk TSpec written only by a source's first open | WK2, WK3, WK4, WK9 | 4 | 6 | 8 | 20 | 4 of 4 |
| `wtsp-read-at-gate-source` | A523, R458-1 | walk TSpec read at the gate source | WK1, WK2, WK4, WK9 | 1 | 6 | 13 | 49 | 4 of 4 |
| `wtsp-read-at-source-0` | R459-1 | walk TSpec read at source 0 | WK1, WK2, WK3, WK4, WK5, WK9 | 0 (equivalent) | 8 | 14 | 50 | 3 of 4 |
| `wtsp-latency-field-shifted` | A523 | latency read one bit off (`wtsp_w[32:1]`) | WK1, WK2, WK3, WK4, WK5, WK9 | 8 | 14 | 20 | 56 | 4 of 4 |
| `wtsp-latency-shifted` | R458-1 | latency shifted left one bit | WK1, WK2, WK3, WK4, WK5, WK9 | 8 | 14 | 20 | 56 | 4 of 4 |
| `wtsp-rank-dropped` | R458-1 | rank bit published as 0 | WK1, WK2, WK3, WK4, WK5, WK9 | 4 | 8 | 9 | 28 | 4 of 4 |
| `wtsp-prio-rank-swapped` | R459-1 | priority and rank bits rotated | WK1, WK2, WK3, WK4, WK5, WK9 | 7 | 13 | 19 | 48 | 4 of 4 |
| `wid-ram-first-open-only` | A523, R458-1 | RAM {stream_id, DA, VLAN} written only by the first open | WK2, WK3, WK4, WK9 | 0 (n/e) | 0 (n/e) | 8 | 20 | 2 of 4 |
| `wid-ram-read-at-gate-source` | A523, R458-1 | RAM {stream_id, DA, VLAN} read at the gate source | WK1, WK2, WK4, WK9 | 0 (n/e) | 0 (n/e) | 13 | 49 | 2 of 4 |
| `wid-ram-read-neighbour` | R459-1 | RAM {stream_id, DA, VLAN} read at the previous source | WK1, WK2, WK3, WK4, WK5, WK9 | 0 (n/e) | 0 (n/e) | 20 | 56 | 2 of 4 |
| `wid-flops-da-of-gate-source` | A523, R458-1 | flop arm reads the gate source's DA | WK1, WK2, WK4, WK9 | 1 | 6 | 0 (n/e) | 0 (n/e) | 2 of 4 |
| `wid-flops-sid-of-source-0` | R458-1 | flop arm reads source 0's stream_id | WK1, WK2, WK3, WK4, WK5, WK9 | 0 (equivalent) | 8 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `wid-flops-vid-of-source-0` | R459-1 | flop arm reads source 0's VLAN | WK1, WK2, WK3, WK4, WK5, WK9 | 0 (equivalent) | 8 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `talker-vid-unreset` | A523 | the matcher VLAN loses its reset (a stored value read without its valid bit) | WK5 | 1 | 1 | 1 | 1 | 4 of 4 |
| `wsid-ram-first-settle-only` | A523, R458-1 | RAM stream_id written only by the first settle | WK8, WK10 | 0 (n/e) | 0 (n/e) | 6 | 10 | 2 of 4 |
| `wsid-ram-written-on-teardown` | A523, R458-1, R459-1 | RAM stream_id also written by a teardown | WK7 | 0 (n/e) | 0 (n/e) | 1 | 1 | 2 of 4 |
| `wsid-flops-of-control-sink` | A523, R458-1 | flop arm reads the control sink's stream_id | WK6, WK8, WK10 | 0 (equivalent in simulation) | 5 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `wsid-flops-read-sink-0` | R459-1 | flop arm reads sink 0's stream_id | WK6, WK7, WK8, WK10 | 0 (equivalent) | 6 | 0 (n/e) | 0 (n/e) | 1 of 4 |
| `wtsp-write-ignores-ready` | R458-3 (`r3-wtsp-write-ignores-ready`) | walk records written by a gate open not yet taken (`gate_valid_i` for `gate_acc_w`) | WK9 | 1 | 1 | 1 | 1 | 4 of 4 |
| `wsid-write-ignores-ready` | R458-3 (`r3-wsid-write-ignores-ready`) | RAM stream_id written by a settle not yet taken (`ctl_valid_i` for `ctl_acc_w`) | WK10 | 0 (n/e) | 0 (n/e) | 1 | 1 | 2 of 4 |

### R3.5 Item 2: the residue

`docs/guides/hdl-engineer.md:88-94`: "What the SRP walks read one context per cycle (the stream FSMs' tick walks and
the admission walk) is distributed RAM read in the cycle of its address, with no latency:" became R458-3's exact text
"The per-context records the SRP walks read one context per cycle (the stream FSMs' tick walks and the admission walk)
are distributed RAM read in the cycle of their address, with no latency:", and the paragraph from line 88 is rewrapped
(widest line 86 columns; the block's lines run 82 to 89). `make check` passes (1,131 links).

### R3.6 Item 3: PR-BODY.md

Header (round 3 comment, head `d18270d6`), the commit table (four rows), item 2's single-writer bullet (the write
process repeats the writer's enable, the ready term included, pinned by WK9 and WK10), the round-2 counts that changed
(35 controls, 128/128, 80/80, the walk counts, the control table and its row-by-row line), a "Round 3" section, and
Validation (round 3 suites, campaign and parent gates beside the round-2 records). No absolute paths, no tool names, no
footer.

### R3.7 Gates at the head

Processor (each command without a pipe; log and rc per run in the scratch, `r3/suites`, `r3/camp`):

| Command | Tree | Result |
|---|---|---|
| `./scripts/run_suites.sh` | `git archive d562ac2` (the head adds only `.md` files) | rc 0, 33 suites, 1,021,485 checks, 0 failing (1,209 s). Against round 2 only `aecp_notify` 14 -> 30 (the manager's merge of `main` `c050d971`); srp_top 2,200, srp_stream_fsms 1,219, srp_admission 991,231, pp_top 10,416 |
| `make` in `tb/srp_stream_fsms` | `git archive d18270d` | rc 0: 35, 46, 67, 123, then 1,219 (35 s) |
| `./scripts/lint_hdl.sh` | head | rc 0, 41 of 41 LINT OK (15 s) |
| `make check` | head | rc 0: 41 mermaid + 18 wavedrom blocks, 1,131 links, 115 REQ rows, 94 matrix rows 0 untested, 28 parameters (42 s) |
| `python3 scripts/gen_matrix.py --check` | head | rc 0, 94 rows, 0 untested |
| `tb/srp_top/mutants.py --jobs 4` | `git archive d562ac2` | rc 0, 128/128, assertion coverage 80/80 (769 s) |

Not re-run in round 3, with the reason: the srp_admission campaign (12/12 at `1199255`; `git diff 1199255 d18270d --
hdl/srp tb/srp_admission` is empty), the Yosys gate and the other campaigns (no HDL or campaign input changed since
`b59e99cb`, where the manager re-ran the donor and parent sets).

Parent consumer gates whose inputs include a file round 3 changed (the processor's C++, Python, READMEs and guide), in
the scratch parent at dev `241f91845230ae410506dffb16b71937127fd175` with `parent-adoption-c8-bbf704ec`,
`parent-adoption-p2-p1-1269cdaf` and `parent-adoption-c10-1269cdaf` applied (as round 2, never committed or pushed),
the processor gitlink set in the index only to `d18270d6` and its checkout detached there (top level verified first).
GNU Make 4.3 and the pinned Verilator 5.050 first on PATH:

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `scripts/check_cpp_idiom.py` | 0 | 174 first-party translation units, every ratchet held ("build without warnings: 0 <= 0") |
| 2 | `scripts/check_py_idiom.py` | 0 | 307 modules, every ratchet held |
| 3 | `scripts/check_rtl_source_lists.py` | 0 | 108 files, 4 of 4 consumer lists; processor 42/42 tops |
| 3b | `scripts/check_rtl_source_lists.py --selftest` | 0 | 50 checks, 50 PASS |
| 4 | `scripts/pp_srcs.py --check --selftest` | 0 | 46 tracked sources derived, self-test passed |
| 5 | `scripts/check_port_contracts.py` | 0 | protocol-processor 1,759 ports, undocumented 111 <= 111 |
| 6 | `scripts/measure_naming.py --check` | 0 | 95 candidates, all recorded |
| 7 | `scripts/measure_test_evidence.py --check` | 0 | within ratchets (72 <= 77 suites without a mutation arm) |
| 8 | `scripts/docs_check.py` | 0 | 0 findings, 187 md + 975 files |
| 11 | `scripts/lint_rtl.py --check` | 0 | 90 <= ratchet 90 |

Gates 9, 10 and 12-16 build or read the processor's HDL and source lists, not its `tb/srp_*` or guides, and round 3
changes none of their inputs; their round-2 records stand, and the manager re-ran the set at `b59e99cb`.

### R3.8 Out-of-context cost

No HDL changed in round 3, so the Vivado figures of section 5 (OOC 1x1 and 8x8, the integrated route) stand as
measured, base `c4cb84ff` against the lane's RTL (`25847d07`'s, unchanged since).

### R3.9 Scratch and notes

- Scratch: `$VALIDATION_STORAGE/pp230-a523/r3/` (`bin/` scripts: `arm_trial.sh`, `gen_patches_r3.py`,
  `readme_rows_r3.py`, `heavy.sh`, `pgates3.sh`; `logs/`, `suites/`, `camp/`, `pgates/`, `trees/`). Nothing generated
  is in the tree; `git status` is clean.
- `readme_rows_r3.py` reproduced all 29 round-2 rows byte for byte from round 2's receipts before it was run on round
  3's.
- HANDOFF and PR-BODY of round 2 are kept in the scratch as `HANDOFF-r2-final.md` and `PR-BODY-r2-final.md`.
- WK9 and WK10 offer to the last context, the one the walk reaches last; under either control the write lands in the
  first held clock, before the walk starts.

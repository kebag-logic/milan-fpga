# [A523] HANDOFF: milan-fpga #230 (SRP area lane, epic #229)

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

| Control | Edit | 2/2 | 9/9 | 3/5 | 1/1 |
|---|---|---:|---:|---:|---:|
| `tf-heads-swapped` | each FIFO head reads the other memory | 28,558 | 90,193 | 39,345 | 7,640 |
| `tf-head-at-write-pointer` | talker head read at `wptr - 1` | 4 | 2,490 | 80 | 0 |
| `tf-listener-push-dropped` | listener push lost when both push | 263 | 1,398 | 421 | 0 |
| `walk-record-written-on-close` | the walk record also written by a gate close | 347,115 | 498,126 | 296,453 | 485,703 |
| `wtsp-first-open-only` | TSpec record written only by a source's first open | 1,717,915 | 1,967,517 | 1,820,782 | 1,742,753 |
| `wtsp-latency-field-shifted` | latency field read one bit off | 1,845,675 | 1,884,652 | 1,858,005 | 1,829,707 |
| `wtsp-read-at-gate-source` | TSpec record read at the gate source | 737,949 | 2,306,384 | 1,156,517 | 48,259 |
| `wid-ram-first-open-only` | RAM arm: {stream_id, DA, VLAN} written only by the first open | 0 (arm not elaborated) | 2,054,932 | 1,901,974 | 0 (n/e) |
| `wid-ram-read-at-gate-source` | RAM arm read at the gate source | 0 (n/e) | 1,849,595 | 1,245,932 | 0 (n/e) |
| `wid-flops-da-of-gate-source` | flop arm: DA of the gate source | 580,488 | 0 (n/e) | 0 (n/e) | 47,564 |
| `wsid-ram-written-on-teardown` | listener RAM arm also written by A8 | 0 (n/e) | 3,095,938 | 2,635,468 | 0 (n/e) |
| `wsid-ram-first-settle-only` | listener RAM arm written only by the first settle | 0 (n/e) | 3,234,988 | 3,116,499 | 0 (n/e) |
| `wsid-flops-of-control-sink` | listener flop arm read at the control sink | 1,331,017 | 0 (n/e) | 0 (n/e) | 0 (one sink: same index) |
| `slope-stored-at-stage-2-index` | slope written at the stage-2 index | 3,351,682 | 3,585,898 | 3,530,423 | 0 (one source) |
| `slope-store-source-0-only` | only source 0's slope stored | 3,287,544 | 3,584,959 | 3,493,546 | 0 (one source) |
| `talker-vid-unreset` | the matcher VID loses its reset (a stored value read without its valid bit) | 474,271 | 451,732 | 477,294 | 5 |

Every control is caught, each at three or four shapes. A zero means one of three things:
- the edited arm is not elaborated at that shape (n/e);
- the edit is equivalent by construction (one source or one sink);
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

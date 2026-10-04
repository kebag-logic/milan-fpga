[A523]

Relates to milan-fpga#230
Relates to milan-fpga#229

The #230 area lane: the second area lever of epic milan-fpga#229, as ranked by the #234 baseline (milan-fpga PR
#638) (assignment: milan-fpga #230 comment 5974045353). Branch `pp230-srp-area` from `main` `c4cb84ff`, two
commits, head `65324390`.

The SRP timer-arm FIFOs no longer spill into flip-flops. The two FIFOs were one two-dimensional array written for
both in one process, which mapped to 2,304 flip-flops and a read multiplexer at 1x1. Each FIFO is now its own
memory, with one write and one registered read port, pinned to distributed RAM. The per-stream records that only the
walks read, and the admission slopes, move to distributed RAM too. Every output of `KL_srp_top` is cycle-identical to
`main`'s. No port, parameter or register changes, and the parent needs no patch.

Lever 4's larger saving, one shared evaluator per stream FSM, needs a protocol-visible timing change. It was ruled
out of #230 and recorded for the redesign (What remains). The rest of #230's scope is below: each SRP block measured separately, the replicated logic
found, the storage map, the inactive slots, and the marginal cost per talker and listener.

| Commit | Item |
|---|---|
| `25847d0` | the FIFO memories in distributed RAM; the talker's walk record, the listener's walk stream_id and the admission slopes in distributed RAM |
| `6532439` | 10 section 5.1: SRP storage map, what stays per stream and why, the marginal cost per talker and listener |

## Items

### 1. Lever 2: the SRP timer-arm FIFOs (`KL_srp_top.sv:947` on `main`)

`tf_ram_r [0:1][0:31]` held both FIFOs in one array written in one process. Vivado kept it in flops: 2,304 at 1x1,
2,688 at 8x8, with a 648-LUT read multiplexer.
- **The change.** Two one-dimensional memories, `tf_tk_ram_r` and `tf_ls_ram_r` (`KL_srp_top.sv:947-984`), each
  written in its own process and read into the unchanged head registers `tf_q_r`. Pointers, counts, the depth of 32,
  the full guard and the two-cycle arm rhythm are unchanged.
- **Mapping.** Each memory is `RAM32M x 8`. `ram_style = "distributed"` is needed: without it the registered read made
  Vivado spend a RAMB36 on each FIFO, which #638's gate forbids.
- **Measured** (standalone 1x1, top glue): 907 -> 354 LUT, 2,836 -> 545 FF, and 296 fewer F7 muxes in the wrapper.
  #638 estimated about 2,300 FF, 580 LUT and 288 MUXF7.

### 2. Lever 4: SRP per-stream evaluation, storage part

What only the walks and the admission walk read moves to distributed RAM, each with one write and one read per cycle:
- **Talker.** `wtsp_r` holds the walk-only fields {MaxFrameSize, MaxIntervalFrames, priority, rank, latency}
  (`KL_srp_talker_fsm.sv:361-372`, `:495-506`). The walk's copy of {stream_id, DA, VLAN} is `g_wid_ram.wid_r` from
  three sources up. At one and two sources the walk keeps reading the matcher's flops (`:508-518`): there, a 2-way
  multiplexer is cheaper than a second copy (measured at 2 and 9 contexts).
- **Listener.** The walk's stream_id is `g_wsid_ram.wsid_r`, with the same split (`KL_srp_listener_fsm.sv:534-558`).
- **Admission.** `slope_q_r` (`KL_srp_admission.sv:111-115`, `:162-169`).

Why behaviour is unchanged:
- Each copy has a single writer, the one that also writes the flop record (the gate open, the A15 settle, slope
  stage 3).
- Each is read only under a valid bit written with it (`rec_valid_r`, `slope_valid_r`), so its missing reset is
  invisible.
- The matcher's flops, which every context compares in the decoder's event cycle, are untouched.

Measured, talker, listener and admission together: 1x1 -37 LUT and -168 FF; 8x8 -791 LUT and -762 FF.

### 3. The rest of #230's scope

- **Each block measured separately.** Talker FSM, listener FSM, top glue, decoder, encoder and admission, at the
  route, 1x1 and 8x8, base and head, are tabled in HANDOFF section 5.3.
- **Logic replicated per stream.** Three kinds, listed in 10 section 5.1:
  - per-stream reads that the walks already serialise: now RAM;
  - the matcher and the Table 10-3/10-4 transitions, which must evaluate every context in one cycle;
  - the per-stream published levels, which are port functions.
- **Inactive slots.** The 1x1 configuration has none. Every per-stream structure is sized by the bound
  `N_STREAM_OUT_P`/`N_STREAM_IN_P`, which is 2 at 1x1 (the stream and CRF), and the census shows exactly two
  contexts per FSM.
- **Marginal cost.** One more talker costs about 200 LUT and 240 FF (base 286 and 322); one more listener about 210
  LUT and 280 FF (base 227 and 278). For the whole engine, one source plus one sink: 592 -> 475 LUT, 679 -> 538 FF.
  These are in 10 section 5.1. The epic issue (milan-fpga#229) is not updated from here: this lane posts only on #230.

## Vivado (#638 recipe and tools at `68d26ea0`; 50 MHz)

Base: scratch parent dev `5fabb46e` + processor `c4cb84ff` + `parent-adoption-c8-bbf704ec` +
`parent-adoption-p2-p1-1269cdaf`. Head: the same with this processor. Never committed or pushed.

| Endpoint | LUT | FF | Slice | RAMB36/18 | DSP | WNS / WHS ns | `u_srp` LUT (LUTRAM) / FF |
|---|---:|---:|---:|---:|---:|---:|---:|
| Route base | 51,434 | 59,691 | 15,847 | 79/27 | 14 | +0.079 / +0.014 | 4,340 (180) / 6,263 |
| Route head | 51,005 | 57,262 | 15,837 | 79/27 | 14 | +0.354 / +0.036 | 3,711 (298) / 3,839 |
| 1x1 base / head | 24,930 / 24,258 | 25,465 / 23,130 | - | 21/3 | 8 | estimate -2.059 / -1.874 | 4,558 / 3,988; 6,438 / 3,979 |
| 8x8 base / head | 32,584 / 31,109 | 34,211 / 30,648 | - | 26/5 | 8 | estimate -2.161 / -1.495 | 8,705 / 7,313; 11,192 / 7,747 |

- **Routes.** Both are complete (0 routing errors), and both corners meet BUILDING section 5 at 50 MHz. The head route
  gains +0.275 ns WNS and took 33 minutes against base's 83.
- **#638's gate.** Head: rc 0 on all three endpoints ("re-baseline recommended"). Base: rc 1 on all three, the
  un-rebaselined next adoption (`u_d3` growth since `631eeb34`), as on #232.

## What remains

**Lever 4's shared evaluator.** #638 estimated "one evaluator per FSM instead of two" at about 440 LUT at 1x1 and
3,100 at 8x8. What is per stream now is evaluated for every context in the same cycle, by contract:
- **The matcher.** `KL_srp_decoder` emits one value per cycle with no ready on its event port, and every context
  compares it in that cycle.
- **The transitions.** `periodic!`, LeaveAll and a matched value reach every context in that cycle.
- **The published levels.** They are per-stream ports.

The options:
- (a) One evaluator per FSM, with contexts in RAM evaluated one per cycle. The decoder gains a ready (a port change).
  Registration indications and LISTENER_REG_CHANGE move by up to M - 1 or N - 1 cycles. A timing change.
- (b) Keep the parallel evaluation (landed): cycle-exact.

Ruled (b) (milan-fpga#230 comment 5977836860): the parallel evaluation is final for #230; (a) is recorded as an input to the redesign (milan-fpga#640).

## Validation (all rc 0, no pipes)

- **Equivalence.** A lockstep bench ran `main`'s `KL_srp_top` beside the head's, with the same inputs each cycle,
  comparing all 51 outputs and 56 internal signals every cycle:
  - 48 runs x 1,000,000 cycles over 2/2, 9/9, 1/1, 3/5, 8/8, and 2/2 at the default cadences;
  - generated MRPDUs and service requests from shared value pools, timer, PRNG and TX models, and 647 mid-run resets;
  - unreset memories started random and different in the two models;
  - 0 mismatches.
  - Sixteen planted controls were each caught at every shape where the edited code is elaborated.
- **Processor suites.** `lint_hdl.sh` 41/41, plus the changed modules at 1, 2, 3 and 9 contexts. `run_suites.sh`:
  33 suites, 1,021,423 checks at base and head, every suite's tally equal. `make check`, `gen_matrix --check` and
  `syn/yosys/run.sh` (36/36) pass.
- **Campaigns, base and head.** Every arm's record is identical:
  - srp_top 90/90 (all 73 patches still apply) and srp_admission 12/12;
  - maap 32 and adp 32 (their pp_top arms);
  - pp_top ctr 18, notify 40/40, acmp 19/19, aecp 60, dispatch 41, d3 110/110, gsi 20, name_wr 1.
- **Parent consumer set** at dev `5fabb46e` + both patches with this processor: 16 of 17 rc 0. That is gates
  1-15 and `check_rtl_source_lists.py --selftest`; builder "all pass except gate 11 not run (mf48 tree)", as in P1's
  record. Gate 16 (`milan_dp_render`) exits 2 on exactly its two T30 INTERNAL law checks, with #643's P1 figures
  (227/292, 285/292, delay 8.830..9.034 ticks). The base processor `c4cb84ff` gives the same two failures with the same
  figures, so they are recorded against #643, and this change moves no boot timing.

Raw Vivado reports, logs, the lockstep bench and its controls stay in scratch, with their digests in HANDOFF.

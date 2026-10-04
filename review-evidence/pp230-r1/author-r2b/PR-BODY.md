[A523]

Relates to milan-fpga#230
Relates to milan-fpga#229

The #230 area lane: the second area lever of epic milan-fpga#229, as ranked by the #234 baseline (milan-fpga PR
#638) (assignment: milan-fpga #230 comment 5974045353; round 2: comment 5978448959). Branch `pp230-srp-area` from
`main` `c4cb84ff`: round 1's two commits, then round 2's merge of `main` `83999eba` and seven test and documentation
commits. Head `b59e99cb`: a docs-only manager commit applying R458-2 F1 and R459-2 F1 as written, on the manager's `--no-ff` merge `9160f7d7` of `main` `c050d971` on the lane's `1199255`.

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
| `6532439` | `docs/architecture/10_srp_engine.md` section 5.1: SRP storage map, what stays per stream and why, the marginal cost per talker and listener |
| `4994ada` | round 2: merge of `main` `83999eba` (C10, #85), no conflict, no SRP HDL |
| `eb352ff` | the walk-record arms WK1-WK8 at sources/sinks 1/1, 2/2, 3/5, 9/9 (`tb/srp_stream_fsms`) |
| `d47ce65` | the timer-arm FIFO arms TF1-TF5 at the same shapes (`tb/srp_top`) |
| `d21dd8e` | 33 killed controls in the srp_top campaign: both reviews' probes and round 1's controls |
| `df02e64` | the storage rule (`docs/guides/hdl-engineer.md` section 3.1) names the new memories; `docs/architecture/10_srp_engine.md` section 5.1 points at the tests |
| `f727957` | the new arms' build flags and initialisers, for the parent's C++ idiom gate |
| `7365022` | WK1 and WK6 also walk with the idle gate and control faces on their highest index |
| `1199255` | the control table re-measured from the head's campaign |

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
- **Logic replicated per stream.** Three kinds, listed in `docs/architecture/10_srp_engine.md` section 5.1:
  - per-stream reads that the walks already serialise: now RAM;
  - the matcher and the Table 10-3/10-4 transitions, which must evaluate every context in one cycle;
  - the per-stream published levels, which are port functions.
- **Inactive slots.** The 1x1 configuration has none. Every per-stream structure is sized by the bound
  `N_STREAM_OUT_P`/`N_STREAM_IN_P`, which is 2 at 1x1 (the stream and CRF), and the census shows exactly two
  contexts per FSM.
- **Marginal cost.** One more talker costs about 200 LUT and 240 FF (base 286 and 322); one more listener about 210
  LUT and 280 FF (base 227 and 278). For the whole engine, one source plus one sink: 592 -> 475 LUT, 679 -> 538 FF.
  These are in `docs/architecture/10_srp_engine.md` section 5.1. The epic issue (milan-fpga#229) is not updated from here: this lane posts only on #230.

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

## Round 2

R458-1 and R459-1 found no RTL defect. Round 2 answers their findings with tests and documentation; no HDL changed.

### Committed coverage of the new storage paths, at both arms

The walk copies are elaborated in two arms: flops at one and two contexts, distributed RAM from three. Round 1's suites
ran at eight contexts only, so eight reviewer probes survived every committed suite. Two new sets of arms now run at
sources/sinks 1/1, 2/2, 3/5 and 9/9 in the default `make`, before each suite (whose tally stays the last line):

- **Walk records, `tb/srp_stream_fsms` (WK1-WK8).** Every FirstValue the walk hands the encoder is compared with the
  record the harness declared, settled or tore down. Every stream_id, DA, VLAN, TSpec and latency differs between any
  two contexts and phases, and unreset memories start random. The arms cover a re-declaration and a re-settle in the opposite order, a close and a
  teardown that carry other values on their faces, a reset, and the idle gate and control faces on the last context
  and on the highest index their width can name. 23, 30, 43 and 79 checks at the four shapes.
- **Timer-arm FIFOs, `tb/srp_top` (TF1-TF5).** The real engine and services. A scoreboard holds the FIFO contract:
  every op an FSM offers leaves the merged arm face once, in order and unmodified, except those the full guard
  refuses.
  - An own LeaveAll makes both FSMs offer an op in one clock.
  - A re-declaration accepted on that LeaveAll's clock, at the round-robin phase that serves the listener first,
    leaves two words in the talker FIFO at a selection, at 1/1 too.
  - The full guard, which no port sequence reaches, is checked by holding the merged issue: the one forced state of
    these arms, test-only, documented in the wrap. Each FIFO then accepts exactly 32 ops and issues them in order once
    released.
  - 15 checks at each shape.
- **Admission slopes.** These have no arms (distributed RAM at every shape). The admission suite already runs at 1, 2,
  3, 5 and 8 sources.

### Every reviewer probe and every own control is a killed control

`tb/srp_top/mutants.py` plants 33 controls, one patch per distinct edit: R458-1's 17 probes, R459-1's 13 non-equivalent
controls and its stall probe, and round 1's 16 lockstep controls (shared edits share a patch). Each must fail its
named check. The campaign at the head: 126 checks, 126 PASS, assertion coverage 78/78. All 84 of round 1's labels keep
their verdicts and failing checks. Failing checks per shape (n/e: the edited arm is not elaborated; equivalent: one
context, the edit names it; equivalent in simulation: Verilator reads the one out-of-range index of a single 64-bit
element as element 0):

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

| Slope control | From | N = 1 | N = 2 | N = 3 | N = 5 | N = 8 | Caught at |
|---|---|---:|---:|---:|---:|---:|---|
| `slope-stored-at-stage-2-index` | A523, R458-1, R459-1 (`slope-store-at-stage-1-index`) | 0 (equivalent) | 1,333 of 12,615 | 4,109 of 41,012 | 12,760 of 201,073 | 38,919 of 991,231 | 4 of 5 |
| `slope-stored-at-source-0` | R458-1 | 0 (equivalent) | 1,521 of 12,615 | 3,915 of 41,012 | 12,415 of 201,073 | 39,056 of 991,231 | 4 of 5 |
| `slope-store-source-0-only` | A523 | 0 (equivalent) | 1,201 of 12,615 | 3,163 of 41,012 | 10,281 of 201,073 | 33,958 of 991,231 | 4 of 5 |
| `slope-read-source-0` | R459-1 | 0 (equivalent) | 578 of 12,615 | 1,683 of 41,009 | 6,125 of 201,068 | 22,202 of 991,223 | 4 of 5 |

Row by row: 18 controls are caught at all four shapes, one at three, six at two and four at one; the slope controls at
four of five. R459-1's three equivalent edits leave every suite that builds the edited file passing (`srp_top`,
`srp_stream_fsms` and `pp_top`).

Round 1's lockstep controls (mismatching cycles over 6 runs x 300,000 per shape; HANDOFF section 4.2), row by row:

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

Six were caught at four shapes, four at three, five at two and one at one, not "each at three or four" as the round-1
body said.
- The two FIFO controls missed at 1/1 (`tf-head-at-write-pointer`, `tf-listener-push-dropped`) are now caught there.
- The round-1 bench and its controls are published with digests (the evidence packet `lockstep-r1/`).

### The bar

Both reviews' probe scripts, run unchanged against this head:

- **R458-1's `lockstep/probes.py`**, unchanged (only its scripts' execute bits restored, which the evidence branch
  dropped): all 17 probes are caught by a committed suite at this head. The eight that survived at `65324390` are now
  caught by `srp_stream_fsms` (WK1-WK8), and `tf-full-guard-31` by `srp_top` (TF4). Its own lockstep results equal its
  receipt, cell for cell.
- **R459-1's `make_controls.py`**, unchanged, against every SRP suite that builds the edited file (full default
  `make`): all 13 defect controls are caught and its three equivalent edits pass. Its stall probe's defect
  (`tf-tk-write-ignores-full`) is a planted control, killed by TF4.

### Merge of `main` `83999eba`

`4994ada` brings C10 (PR #149) and #85 (PR #152, tests only) with no conflict and no SRP HDL. The area figures above
therefore stand as measured: base `c4cb84ff` against this RTL, as a delta. Everything the merge touches was re-run
(Validation).

### Residue

- The storage rule in `docs/guides/hdl-engineer.md` section 3.1 now names the walk copies, the slopes and the FIFOs.
- This body names `docs/architecture/10_srp_engine.md` section 5.1 in full.
- One commit subject (`df02e64`) still says "10 section 5.1"; history is not rewritten for it.

## Validation (all rc 0 except parent gate 16, recorded against #643; no pipes)

- **Equivalence (round 1).** A lockstep bench ran `main`'s `KL_srp_top` beside this RTL, with the same inputs each
  cycle, comparing all 51 outputs and 56 internal signals every cycle:
  - 48 runs x 1,000,000 cycles over 2/2, 9/9, 1/1, 3/5, 8/8, and 2/2 at the default cadences;
  - generated MRPDUs and service requests from shared value pools, timer, PRNG and TX models, and 647 mid-run resets;
  - unreset memories started random and different in the two models;
  - 0 mismatches.
  - Its sixteen planted controls were caught at one to four of the four shapes (Round 2 above has each row). The
    bench, its controls and their logs are published with digests.
- **Processor suites, at `7365022`** (the lane's head before the manager's merge; `1199255` adds only a README). `lint_hdl.sh` 41/41. `run_suites.sh`: 33 suites, 1,021,469 checks, 0 failing.
  Against round 1, `adp_engine` +20 and `pp_top` +26 come from the merge; the SRP suites keep their tallies (srp_top
  2,200, srp_stream_fsms 1,219, srp_admission 991,231), each now preceded by the new arms. `make check` (1,131 links),
  `gen_matrix --check` and `syn/yosys/run.sh` (42 tops, one parse) pass.
- **Campaigns.**
  - srp_top, at the head: 126/126, assertion coverage 78/78. Each of round 1's 84 labels keeps its verdict and failing
    checks.
  - srp_admission, at the head: 12/12.
  - The campaigns the merge touches, run at the merge commit `4994ada` (their inputs equal `1199255`'s): adp 43 (2
    controls, 41 arms), maap 32, pp_top ctr 18, notify 40/40, acmp 19/19, aecp 60, dispatch 44, d3 110/110, gsi 20 and
    name_wr 1.
  - nvm_port's figures gate, in the git checkout as CI runs it: rc 0, every figure agrees with the tree.
- **Parent consumer set** at dev `241f9184` + c8, p2-p1 and c10, with this processor: 16 of 17 rc 0.
  - The xvlog gate (gate 9) passes at this processor: 3 findings == ratchet, 0 in the parent's `hdl/`.
  - Gates 1-8 and 11-15 and `check_rtl_source_lists.py --selftest` pass.
  - The builder (gate 10) gives "all pass except gate 11 not run (mf48 tree)" under the host's Make 4.4.1, as in
    P1's record. Under Make 4.3 its gate 1b arm does not run either.
  - Gate 16 (`milan_dp_render`) exits 2 on exactly its two T30 INTERNAL law checks, with #643's figures (227/292,
    285/292, first-event delay 8.830..9.034 ticks). Round 1 found the same at base and head on dev `5fabb46e`. They
    are recorded against #643 / milan-fpga PR #648.

The eight Vivado runs' logs and reports are published in the evidence (milan-fpga `06fe795b`,
`review-evidence/pp230-r1/author-r1/vivado/`, original digests in its MANIFEST.json). Round 2 changes no HDL, so they
stand. The round-1 lockstep bench and its controls are in this round's packet (`lockstep-r1/`, with `MANIFEST.sha256`).

**Manager merge (round 2).** Processor `main` `c050d971` (PR #153: notify files only, no file in common with this PR) was merged at `9160f7d7` with no conflicts; the donor and parent consumer sets are re-run at that head.

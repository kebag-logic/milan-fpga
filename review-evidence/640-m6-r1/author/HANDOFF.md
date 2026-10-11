# HANDOFF: lane M6 for #640 (media context tables), executor [A591]

Status: REVIEW READY at `ee0fc6fd9abd393ac48d5d5f4f9e2452dc5f6937` (resumed
after an external usage-limit stop at 21:06 on 2026-10-10).

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6098405082
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6098443919
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6103630528
- Branch: `640-m6` from dev `e8454e2751d05b02ee8e5a571857589ab358ab86` (local, not pushed)
- Reviewers: [R600] (internal), [R601] (external)
- Plan: `docs/design/MARK_II_AREA_PLAN.md`, "L9 Media context tables" (600 LUT, 400-900)

Resume notes: the cut session left the tree clean at `8b209daa7`. Its
route was queued but never took the host lock, its last capture OOC run
(`run6`) never produced a result, and its suite sweep ran on an earlier
working state (before the skid change) with shard 2 never started. All
three are re-run at the head here; nothing of the cut session's results is
quoted unless it was produced at the head's RTL.

## 1. Measured starting point (before any change)

Routed hierarchy of dev `e8454e27` through the M0s recipe (the M2 lane's
base route of the same dev, rc 0, equal to the `route-1x1` record in every
gated figure; reused read-only, route checkpoint SHA-256
`017a9a6c1241087b5115683c094091d66d9581ebc96105bb1289a0f9a5f67f3b`):

| Block | Module | LUT | logic | LUTRAM | FF | RAMB36 | RAMB18 |
|---|---|---:|---:|---:|---:|---:|---:|
| `avtp_rx_monitor` | `KL_avtp_rx_monitor_ctx` | 966 | 966 | 0 | 1,353 | 0 | 1 |
| `chan_map_capture` | `KL_chan_map_capture` | 1,069 | 1,069 | 0 | 1,360 | 1 | 0 |
| `render_setpoint` | `KL_render_setpoint` | 383 | 255 | 128 | 137 | 0 | 0 |
| `talker_diag` | `KL_talker_diag_ctx` | 195 | 195 | 0 | 359 | 0 | 0 |
| Total | | 2,613 | 2,485 | 128 | 3,209 | 1 | 1 |

Shipping shape: `--num-streams 1 --loopback-lane --audio-interface tdm8`,
50 MHz datapath clock.

Per-cell census of the same route (every LUT attributed to the registers
its output reaches): at 1x1 every per-stream table has ONE entry, so a
table conversion alone saves little. The cost sits in the multiplexers and
queues around the tables:

- rx monitor: PDU bundle queue and in-service copy 262 cells; the
  GET_COUNTERS word multiplexer the route absorbed into it 140; the RAM
  write-data path about 260.
- talker diag: 160 of its 195 are the GET_COUNTERS read multiplexer.
- capture: the two channel resolvers 415; the commit skid's write side 268.
- render set-point: storage already distributed RAM (128 LUTRAM).

## 2. Changes (file:line, at the head)

Commits on `640-m6` (dev `e8454e27` + 8): RTL `073b0985b`, `dced661a3`,
`e53a76e5a`; tests `3f655acf0`, `dbf54cce9`, `8b209daa7`; header and suite
index `930340145`; ledger docs `ee0fc6fd9`. Measured product commit:
`930340145`.

- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv`
  - :293-297 PDU bundle ring: the two waiting bundles and the one in
    service share one 4-entry table (`pq_ring_r`) with one write port
    (:472-475). Every accepted pulse is written once at `pq_wp_r`; the
    walker reads its bundle through `cur_idx_r` (`cur_w`). Replaces the
    2-entry flop queue `pq_r` plus the in-service flop copy `cur_r`.
    Capacity unchanged: `penq_w` still refuses a third waiting bundle
    (:418-419), so a write never lands on the slot in service.
  - :856-873 ring pointers (`pq_wp_r`, `pq_rp_r`, `cur_idx_r`) and the
    unchanged waiting count `pq_cnt_r`; reset clears all four (:793-799).
  - :219-220 port `diag_cnt_o[12*32]` becomes `diag_col_i[4]` in and
    `diag_q_o[32]` out: GET_COUNTERS reads ONE counter by sink and column.
  - :774-788 counter mirror: one `N x 16` write-through LUT-RAM table
    (`cnt_mirror_r`) at `{stream, column}` replaces ten column arrays; the
    column is part of the read address, so the word multiplexer that used
    to sit in the answer server is inside the LUT-RAM read. Columns 10/11
    (TV/TNV) still come from their flop counters.
- `hdl/milan/milan_datapath.sv`
  - :3451, :3507-3533 the STREAM_INPUT GET_COUNTERS word index now names
    a monitor column (`mon_diag_col_w`); quadlets 0..11 read `mon_diag_q_w`,
    quadlet 32 is still `counters_valid`, every other quadlet still 0.
  - :6337, :6344 the new ports.
- `hdl/milan/KL_pp_shadow.sv:333` comment names the new port.
- `hdl/ieee1722/aaf/KL_chan_map_capture.sv`
  - :1277-1292 one flat source table `cand_w` of every mono cluster (0
    silence, I2S L/R, tone, each TDM pair's L/R, each loopback hold pair's
    L/R); :1300-1326 a channel entry decodes to one row index;
    :1327-1332 one indexed read per channel. Replaces the per-channel
    bucket -> pair -> half resolver.
  - :735-738, :748 commit FORMS: each commit word is one of four
    arrangements of the beat's `{stash-or-0, smp0, smp1}`.
  - :826-849 skid entries hold a 2-bit form and a 2-bit beat slot instead
    of the 48-bit word; a 4-slot LUT-RAM beat bank (`beat_bank_r`, one
    write port :1006-1008) holds each admitted beat once; :853-864 the
    drain rebuilds the head commit's word. Capacity, order, refusal and
    flush-kill unchanged. :1036-1041 resets on the descriptor arrays are
    functionally invisible and avoid a Verilator 5.050 internal error
    (V3Gate.cpp:986) when the loopback feed is tied off.

Not changed: `KL_render_setpoint` (its storage is already distributed RAM,
128 LUTRAM, and its pop schedule is unchanged) and `KL_talker_diag_ctx`.
Talker diag reasoning: its five counters per context increment and reset
in parallel at the interval tick and on streaming edges, so a RAM form
needs a serialising walker, which changes timing. Folding its read
multiplexer into a column read, as for the monitor, is estimated at 30 to
50 LUT. That is recorded as a follow-up option, not done here.

Tests and docs: see section 3. `docs/testing/TESTING.md` suite index rows
for `avtp_rxmon` and `chmap_capture`; `scripts/measure_test_evidence_readers.py`
records the two new harnesses' source-reader dispositions;
`tb/verilator/capture_coherence/mutants.py` re-anchors its two TDM junction
mutants on the new source-table line (same defects, same expected break).

## 3. Tests and the planted defect each catches

Two lockstep legs run the shipping module beside the pre-change module
(`reference/`, dev `e8454e27`'s file with only the module name changed),
fed the same inputs every cycle, at both shapes, inside each suite's
default target.

`tb/verilator/avtp_rxmon` (`make lockstep`, N=1 and N=8; then
`lockstep_mutants.py`):

| Case | What it drives | Planted defect | Named check it fails |
|---|---|---|---|
| [H1] same-stream back-to-back updates | bursts of gap PDUs on one stream at spacings 1-12 cycles | lost increment: a pulse landing on a queued dispatch drops from the queue count | `[H1] STREAM_INTERRUPTED moved by exactly one per accepted gap PDU` |
| [H2] update colliding with read | GET_COUNTERS read held across the write cycle, counter seeded 0x0000FFFF | torn read: the mirror takes the high half one cycle after the low half | `[H2] GET_COUNTERS read identical to the reference in every cycle of the update window` |
| [GC] every sink and column | seeded per-sink signatures read back by value | wrong stream index: the read ignores the sink | `[GC] every sink answers its own row and column (seeded signatures)` |
| [H4] reset during update | reset at every offset into a PDU burst | missed reset: the queue count survives a reset | `[H4] no bundle queued before a reset is served after it` |
| [H3] wrap | counters seeded near 2^32 | (covered by [LS]/[GC] equality) | |
| [SO] soak | seeded random inputs with resets, binds, window traffic | | |

`tb/verilator/chmap_capture` (`make lockstep`, 4 slots/1 stream and 32
slots/8 streams; then `lockstep_mutants.py`):

| Case | Planted defect | Named check it fails |
|---|---|---|
| [ST] source table | wrong row decode: a TDM entry ignores its half | `[ST] every channel entry resolves to its own source sample` |
| [SK] mono wire | beat slot reused: the bank's write slot never advances | `[SK] mono wire, two commits per beat: every event replayed once, in order` |
| [SK] three-channel wire | commit form swapped: a lone even channel commits the first sample | `[SK] three-channel wire, stashed and lone channels: every event replayed once, in order` |
| [SO] soak | | |

Run at `8b209daa7` (test and RTL content of the head; the later commit
`ee0fc6fd9` changes only `docs/design/*.md`), each suite's default target
with the pinned Verilator 5.050, never piped, one log and rc per suite:

| Suite | rc | Checks (failures) | Notes |
|---|---:|---:|---|
| `avtp_rxmon` | 0 | 292 (0) | lockstep N=1 36/36, N=8 36/36; mutants `5 checks: 5 PASS, 0 FAIL` |
| `chmap_capture` | 0 | 847 (0) | lockstep 4 slots 19/19, 32 slots 19/19; mutants `4 checks: 4 PASS, 0 FAIL` |
| `tkdiag` | 0 | 101 (0) | |
| `render_setpoint` | 0 | 277 (0) | |
| `milan_dp` | 0 | 12,065 (0) | N_STREAMS 1 (ax7101 1x1 TDM8), 4 and 8 legs, pruned shape |
| `capture_coherence` | 0 | 21,194 (0) | its mutant campaign `30 checks: 30 PASS, 0 FAIL`, incl. the two re-anchored junction mutants |
| `csr` | 0 | 1,797 (0) | builds `milan_datapath` |
| `pp_shadow` | 0 | 2,184 (0) | |
| `milan_dp_render` | 0 | 342 (0) | |
| `milan_dp_mclk` | 0 | 168 (0) | |
| `follow_ring` | 0 | 66 (0) | |
| `media_grid_align` | 0 | 45 (0) | |
| `nvm_cosim` | 0 | 465 (0) | |
| `rx_filter` | 0 | 88 (0) | |
| `avtp_parser` | 0 | 11,201 (0) | |
| `tsn_fuzz` | 0 | 56 (0) | 4 declared skips: tsn-gen absent on this host |

"Both shapes": the lockstep legs build the shipping 1x1 parameters and the
8x8 parameters; `milan_dp` runs the ax7101 1x1 TDM8 shape and the N=8 leg.

Full sweep at `8b209daa7`: `scripts/run_all_suites.sh <logdir> --shard
K/3` for K = 0, 1, 2, each from a clean scratch worktree of the head, with
the pinned Verilator (preflight controls passed in each shard):

| Shard | Suites | Passed | Failed | Checks | rc |
|---|---:|---:|---:|---:|---:|
| 0/3 | 25 | 25 | 0 | 1,961,885 | 0 |
| 1/3 | 35 | 34 | 1 (`crf_rx`) | 212,007 | 1 |
| 2/3 (`milan_dp`) | 1 | 1 | 0 | 12,065 | 0 |

`python3 scripts/suite_tally.py` over the three shard directories: rc 0,
61 suites, 2,185,957 checks, 0 in-suite failures, 4 declared skips
(`tsn_fuzz`, tsn-gen absent).

`crf_rx` in shard 1: every check passed (16,557, 0 failures); then its
mutant driver took an external SIGTERM after 8 of its 10 checks (make
`Error 143` at 00:03:16, nine minutes into the suite, far inside its
1,800 s guard; nothing of this lane was running a kill then). `crf_rx`
builds none of the changed files (`KL_crf_rx.sv`, `cdc_pulse.sv`,
`cdc_handshake.sv`, `KL_mmcm_drp_servo.sv`). Re-run directly at the same
head: rc 0, discontinuity 2,201/0, talker_step 69/0, mutants 10/0.

Earlier aborted launches (recorded for honesty, not evidence): three
earlier launches of these shards aborted in the sweep's cancellation
preflight, before any suite ran. They were started under `nohup`, which
makes SIGHUP ignored, so the hard-HUP control can never pass (the first
also met a load average above 200). Relaunched with `setsid` only, the
preflight passed in every shard.

`milan_dp_gptp` (scheduled physical suite, outside the default shards;
builds the changed datapath): run directly at the same head, rc 0,
197 checks, 0 failures (physical leg 143/0 in 3,776 s, abort, no-Pdelay and
recentre controls).

## 4. Primitive mapping before/after

Out-of-context, 1x1 parameters (Vivado 2026.1, xc7a100t-fgg484-2,
AreaOptimized_high):

| Block | Before | After |
|---|---|---|
| rx monitor | 1,366 FDRE, 1,048 LUT, 1 RAMB18E1 | 714 FDRE, 832 LUT, 156 RAMD32 + 46 RAMS32 (110 LUT as memory), 1 RAMB18E1 |
| capture | 1,373 FDRE + 2 FDSE, 1,254 LUT, 63 MUXF7, 1 RAMB36E1 | 1,196 FDRE + 2 FDSE, 808 LUT, 66 MUXF7, 72 RAMD32 + 24 RAMS32 (48 LUT as memory), 1 RAMB36E1 |

Integrated route (per-cell census of each route, LUT cells before packing):

| Block | Base `e8454e27` | M6 `930340145` |
|---|---|---|
| rx monitor | 1,125 LUT cells, 1,353 FF, RAMB18E1 `lctx_r` | 831 LUT cells, 23 RAM32M + 9 RAM32X1D, 691 FF, RAMB18E1 `lctx_r` |
| capture | 1,159 LUT cells, 1,360 FF, RAMB36E1 `lb_q_r` | 889 LUT cells, 12 RAM32M, 1,183 FF, RAMB36E1 `lb_q_r` |
| render set-point | 351 LUT cells, 32 RAM64M, 137 FF | identical |
| talker diag | 195 LUT cells, 359 FF | 163 LUT cells, 359 FF (RTL unchanged) |

Block RAM is unchanged in both blocks: the monitor's context RAM stays one
RAMB18E1 and the capture's queue one RAMB36E1. No new tile is used.
Out-of-context timing at the 20 ns clock stays met: capture WNS +12.784 ns
before, +12.623 ns after.

## 5. Resource and route before/after (M0s recipe)

Out-of-context A/B at the 1x1 parameters (Slice LUTs):

| Variant | Slice LUT | LUTRAM | FF | Note |
|---|---:|---:|---:|---|
| capture, base | 1,172 | 0 | 1,375 | |
| capture, flat source table | 997 | 0 | 1,375 | -175 |
| capture 8x8, base / flat | 3,320 / 3,264 | 0 | 4,071 / 4,070 | -56 |
| capture, flat + descriptor skid + beat bank (head) | 787 | 48 | 1,198 | -385 |
| capture 8x8, base / head | 3,320 / 3,052 | 0 / 48 | 4,071 / 3,891 | -268 |
| rx monitor, base | 885 | 0 | 1,366 | |
| rx monitor, ring + counter table (head) | 825 | 110 | 714 | -60 |
| rx monitor + talker + GET_COUNTERS muxes, base | 1,192 | 0 | 1,795 | |
| same, ring + counter table | 1,025 | 110 | 1,143 | -167 |
| rx monitor 8x8, base / new | 2,105 / 1,936 | 240 / 174 | 1,847 / 1,519 | -169 |
| rx monitor, plus shared RMW adder and shared TV/TNV incrementer | 832 | 110 | 714 | +7 against ring + table: not adopted |

Integrated route through the M0s recipe (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`
"Integrated measurements"): export of `930340145` (RTL identical to the head;
later commits touch only tests and docs), `pp_baseline.py
--single-thread-synthesis`, `vivado -mode batch -source
baseline_integrated.tcl`, one job under the exclusive host lock (locked
22:32:16, route rc 0, job end 23:34:05). Base is the M2 lane's route of dev
`e8454e27` (equal to the `route-1x1` record).

| Measurement | LUT | FF | Slices | RAMB36 / RAMB18 | DSP | WNS / WHS, ns |
|---|---:|---:|---:|---:|---:|---|
| Base route, dev `e8454e27` | 50,267 | 54,413 | 15,779 | 74 / 27 | 14 | +0.299 / +0.031 |
| M6 route, `930340145` | 49,561 | 53,455 | 15,791 | 74 / 27 | 14 | +0.141 / +0.018 |
| Routed delta | -706 | -958 | +12 | 0 / 0 | 0 | -0.158 / -0.013 |
| Post-synthesis (same runs) | 52,731 -> 52,207 (-524) | 54,531 -> 53,574 (-957) | | 74 / 27 both | | |

Gate: `python3 syn/ooc/pp_resource_gate.py check <gateware> --endpoint
route-1x1` rc 0, `RESULT: PASS`; route status complete (100,259 of 100,259
routable nets routed, 0 routing errors); timing summary 0 failing setup
(180,304 endpoints), hold (180,223) and pulse-width (60,610) endpoints; the
four signoff corners (Slow/Fast at 0 and 85 C) each report "No timing paths
found" with negative slack. WNS +0.141 is above the 0.03 floor; the worst
path is inside the unchanged protocol processor (`baseline_scope_timing.tsv`:
`milan_datapath/pp_shadow/u_pp` 0.141). No exception: a fresh export of
dev `e8454e27` through the same recipe step and the candidate's export
give byte-identical `alinx_ax7101.xdc`, `alinx_ax7101.tcl`,
`baseline_integrated.tcl` and `baseline_images.json` once the checkout and
work paths are normalised (`cmp` rc 0 for all four). The gate prints
"re-baseline recommended"; not done (D7).
The base route's reports lived in the M2 lane's scratch and have since
been removed by their owner; the base figures above were read from them
before removal and match the `route-1x1` record.
Candidate route checkpoint: SHA-256
`17d4e88ae2df3f0455fc3cc6925b8ed08b5c07701947b8e0f8f469f655b369a0`,
108,940,354 bytes (kept in scratch, not in this directory).

Per block (hierarchical utilisation of the same runs):

| Block | Routed LUT | Post-synthesis LUT | FF |
|---|---:|---:|---:|
| `KL_avtp_rx_monitor_ctx` | 966 -> 754 (-212) | 993 -> 818 (-175) | 1,353 -> 691 |
| `KL_chan_map_capture` | 1,069 -> 813 (-256) | 1,107 -> 864 (-243) | 1,360 -> 1,183 |
| `KL_talker_diag_ctx` (RTL unchanged) | 195 -> 161 (-34) | 197 -> 165 (-32) | 359 -> 359 |
| `KL_render_setpoint` (RTL unchanged) | 383 -> 381 (-2) | 399 -> 399 (0) | 137 -> 137 |
| Four L9 blocks | 2,613 -> 2,109 (-504) | 2,696 -> 2,246 (-450) | 3,209 -> 2,370 |

Unchanged RTL also moved: `pp_shadow/u_pp` -358 post-synthesis / -333
routed; the gPTP shadow -698 at its own level and +537 in `u_engine`
post-synthesis; `csr` +98; the CPU +92; the top's own logic +167. That is
the synthesis's global non-locality, not a saving of this lane, and it is
not credited.

Saving against the plan's 600 (400-900):

- whole image: -706 routed, -524 post-synthesis (includes the uncredited
  movement above);
- reproducible, the two changed blocks: **418 LUT post-synthesis**, 468
  routed, 839 FF;
- out of context, the changed modules at 1x1: 552 (monitor and the
  GET_COUNTERS path -167, capture -385).

All three sit low in the range, below the 600 central figure. No block-RAM
tile is added.

## 6. Gate table

Every command run from the lane tree at the head `ee0fc6fd9` (unless
noted), under CPython 3.12.3 with the pinned Markdown renderer and the
pinned Verilator 5.050 first on PATH; one log and rc per gate, none piped.

| Command | rc |
|---|---:|
| `python3 scripts/docs_check.py` | 0 |
| `python3 scripts/docs_check.py --selftest` | 0 |
| `python3 scripts/check_em_dash.py --base e8454e2751d05b02ee8e5a571857589ab358ab86` | 0 |
| `python3 scripts/check_em_dash.py --selftest` | 0 |
| `python3 scripts/check_doc_style.py` | 0 |
| `python3 docs/DOC_MAP.gen.py --check` | 0 |
| `python3 scripts/check_feature_status.py` | 0 |
| `python3 scripts/check_feature_status.py --self-test` | 0 |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 |
| `python3 scripts/check_doc_paths.py` | 0 |
| `python3 scripts/gen_toc.py --check` | 0 |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 |
| `python3 scripts/check_archive.py` | 0 |
| `python3 scripts/check_solution_docs.py` | 0 |
| `python3 scripts/check_gptp_docs.py` | 0 |
| `python3 scripts/check_rtl_source_lists.py` | 0 |
| `python3 scripts/check_rtl_source_lists.py --selftest` | 0 |
| `python3 scripts/check_soc_sources.py` | 0 |
| `python3 scripts/measure_naming.py --check` | 0 |
| `python3 scripts/check_port_contracts.py` | 0 |
| `python3 scripts/measure_fail_fast.py --check` | 0 |
| `python3 scripts/check_todo_ownership.py` | 0 |
| `python3 scripts/measure_test_evidence.py --check` | 0 |
| `python3 scripts/check_hygiene.py --check` | 0 |
| `python3 scripts/check_sv_idiom.py` | 0 |
| `python3 scripts/check_cpp_idiom.py` | 0 |
| `python3 scripts/check_py_idiom.py` | 0 |
| `python3 scripts/check_sh_idiom.py` | 0 |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 |
| `python3 scripts/ci_scope.py --selftest` | 0 |
| `python3 scripts/ci_events.py --check` | 0 |
| `python3 scripts/check_wire_accountability.py --self-test` | 0 |
| `python3 scripts/check_entity_shape.py` | 0 |
| `python3 scripts/check_deploy_shape.py` | 0 |
| `python3 scripts/check_sweep_shape.py` | 0 |
| `python3 syn/ooc/dp_srcs.py --selftest` | 0 |
| `python3 syn/ooc/dp_srcs.py --top milan_datapath` | 0 |
| `python3 syn/ooc/dp_srcs.py --top KL_pp_shadow` | 0 |
| `python3 syn/ooc/ooc_tcl_selftest.py` | 0 |
| `python3 syn/ooc/pp_baseline.py --selftest` | 0 |
| `python3 syn/ooc/pp_baseline_mutants.py` | 0 |
| `python3 syn/ooc/pp_baseline_reports_selftest.py` | 0 |
| `python3 syn/ooc/pp_resource_gate.py --selftest` | 0 |
| `python3 -X cpu_count=4 syn/ooc/pp_resource_gate_mutants.py` | 0 |
| `python3 syn/ooc/pp_resource_gate.py check-baseline` | 0 |
| `git diff --check e8454e2751d05b02ee8e5a571857589ab358ab86 HEAD` | 0 |
| `git diff --check` | 0 |
| `python3 scripts/check_cpp_idiom.py --selftest` | 0 |
| `python3 scripts/measure_test_evidence.py --selftest` | 0 |
| `python3 scripts/gen_toc.py --selftest` | 0 |
| `python3 scripts/check_doc_style.py --selftest` | 0 |
| `python3 scripts/check_hygiene.py --selftest` | 0 |
| `python3 scripts/suite_shards.py --selftest` | 0 |
| `python3 syn/yosys/ooc_selftest.py` | 0 |
| `python3 syn/yosys/guard_selftest.py` | 0 |
| `python3 syn/yosys/cache_selftest.py` | 0 |
| `syn/yosys/run.sh --mode elaborate --no-structural --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow` | 0 |
| `python3 scripts/xvlog_gate.py --check` (at `8b209daa7`, same RTL, under the host lock) | 0 |
| `python3 syn/ooc/pp_resource_gate.py check <M6 route gateware> --endpoint route-1x1` | 0 |
| `python3 scripts/lint_rtl.py --check` (90 <= ratchet 90; none in a changed file) | 0 |
| `python3 scripts/lint_rtl.py --check --self-test` | 0 |
| `MAKEFLAGS=w make -C tb/verilator/avtp_rxmon` under GNU make 4.3 (at `8b209daa7`) | 0 |
| `MAKEFLAGS=w make -C tb/verilator/chmap_capture` under GNU make 4.3 (at `8b209daa7`) | 0 |

`measure_test_evidence.py --check` prints "the mutation ratchet can be
lowered to 68" (77 recorded); lowering a shared ratchet is left to the
manager, since parallel lanes also move it.

## 7. Open risks / decisions

- Saving below the central estimate: 418 LUT reproducible (468 routed in
  the changed blocks, 552 out of context) against 600 (400-900). Option not
  taken: fold the talker counters' read multiplexer into a column read
  (estimated 30-50 LUT); a RAM form for those counters would need a
  serialising walker and change timing, so it is not identical function.
- Untouched blocks move by hundreds of LUTs between the two images
  (protocol processor -333 routed); the whole-image -706 is reported but
  only the changed blocks are credited.
- WNS fell from +0.299 to +0.141 ns (floor 0.03); the worst path is inside
  the unchanged protocol processor, so this is placement variation, not a
  path through the changed blocks.
- Standalone `ooc-1x1` / `ooc-8x8` gate endpoints not re-run: their 50-file
  source set differs from dev `e8454e27` only by one comment line in
  `KL_pp_shadow.sv`, submodule pins unchanged.
- Merge note: the unmerged M2 lane also edits `MARK_II_AREA_PLAN.md` and
  `AREA_BUDGET.md`; M6's insertions sit at different anchors (before
  "Cumulative default-image estimates"; after the AREA_BUDGET paragraph
  ending "not added to the default ledger"). `git merge-tree --write-tree
  HEAD 2b22bf291` (M2's ledger commit) exits 0 with no conflict.
- Record: not re-recorded (D7 keeps the gate record until M9).

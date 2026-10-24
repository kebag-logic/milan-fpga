# HANDOFF - lane 775 ([A666])

Issue: kebag-logic/milan-fpga#775. A discarded off-format PDU does not advance the sequence state, so the next in-order PDU counts SEQ_NUM_MISMATCH (AAF and CRF inputs, #765 follow-up).
Assignment: [A10] issuecomment-6379902989. Its ruling (Milan v1.2 Table 5.6): an off-format Stream Data AVTPDU is a received PDU, so its sequence_num advances the input's sequence state, while it counts only UNSUPPORTED_FORMAT and presents nothing. STOP condition: route-1x1 grows by more than +5 slices.
Branch: `775-offformat-seq-advance` from dev `a032c6d6`. `git merge-base HEAD origin/dev` is `a032c6d6`, and the live remote dev tip is still `a032c6d6` (fetched for the em-dash gate). Origin is `https://github.com/kebag-logic/milan-fpga.git`. Submodules sit at the dev pins, each verified at its own top level and origin (`receipts/submodules.txt`). Nothing pushed.
TAKEN: issuecomment-6379929702 (text in `TAKEN-COMMENT.md`).

## Status

REVIEW READY at `c7e87c8c` posted as issuecomment-6381447825 on #775 (text in `REVIEW-READY-COMMENT.md`). Every gate the assignment names is rc 0 at this head: the two touched suites with their mutant drivers, the full sweep as four parallel shard units, Yosys, lint, the docs gates under GNU Make 4.3, and route-1x1 against the eleventh record (SLICE -2, so the +5-slice STOP condition is not reached). Nothing pushed; no PR opened. `PR-BODY.md` says `Closes #775`.

## Commits (on `a032c6d6`; one-line subjects, no body, no trailers)

| Commit | What |
|---|---|
| `0ee987f4` | AAF input: the prev_seq advance on a discarded off-format PDU, the same edit in the lockstep reference, the `[SQ]` cases and three mutants |
| `6ff2880a` | CRF input: the exp_seq_r advance on a discarded off-format PDU, the same rule in the harness replica, the `[SQ]` cases and two mutants. Reject stimulus that reused a sequence number now consumes one (crf_rx, milan_dp) |
| `c7e87c8c` | docs: FR-STR-03, the compliance-matrix 4.4.2.2 / Table 5.6 row, and the testing guide's avtp_rxmon and crf_rx rows |

Head `c7e87c8c87494f3444000b46954648ba1a94dcb8`.

## Changes (file:line at `c7e87c8c`, clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:1009-1020` | M_PDEC_S, `!fmt_ok_w` branch (assignment item 1). It sets `monst_r <= {ram_q_r[31:8], cur_w.seq}` and `mst_r <= M_PSEQ_S`. Only MON_STATE[7:0] (prev_seq) changes, to the PDU's sequence_num, which is what an accepted PDU writes there (`monst_next_w[7:0] = cur_w.seq`, `:560`). Lock, settle, wire_chans, the mr reference and its seed keep their values. There is no accept verdict, no LAST_TS/LAST_TSD write and no counter walk, and iv_events still raises only the UF flag (`:595-596`). So there is no MEDIA_RESET, timestamp or presentation side effect | Milan v1.2 5.3.8.10 Table 5.6: SEQ_NUM_MISMATCH counts a PDU "received" with a non-sequential sequence_num; UNSUPPORTED_FORMAT counts one that "has been received with a format that did not match". Also 4.4.2.2 |
| `...ctx.sv:292` | a new walker state, `M_PSEQ_S`, the tenth value of the 4-bit enum | -- |
| `...ctx.sv:637-642` | write mux: `M_PSEQ_S` writes `monst_r` to the stream's w8 in one cycle. It is M_PWR_S's wrph-0 write on its own | -- |
| `...ctx.sv:1061` | `M_PSEQ_S : mst_r <= M_IDLE_S` | -- |
| `...ctx.sv:19-21` | banner: a rejected PDU advances the sequence state and affects nothing else (#775) | -- |
| `hdl/ieee1722/crf/KL_crf_rx.sv:603-607` | the rejected branch (assignment item 2) sets `exp_seq_r <= seq_i + 8'd1`. `have_seq_r` is untouched, so only an accepted PDU seeds the cursor: the first-PDU behaviour is kept. settle_r still breaks, as before | Milan v1.2 Table 5.6 |
| `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:15-16,292,619-623,990-993,1045` | the lockstep reference takes the same edit in the same lines (the #762 and #765 precedent). Its `[SO]` soak sends off-format PDUs, so without the edit the cycle-exact `[LS]`/`[GC]` compare would diverge. #775 is graded by `[SQ]` by count, never against this copy | -- |

There is no register-map, port, parameter or interface change. A discarded AAF PDU now costs one more walker cycle (PDEC, PSEQ, idle instead of PDEC, idle). That is still fewer than an accepted PDU's PDEC, PWR x3 and INC walk, so the ring's two waiting slots are no closer to full than with accepted traffic.

## Stimulus and harness changes (file:line at `c7e87c8c`)

Under the ruling, a sequence number reused across a reject is a real repeat: a SEQ_NUM_MISMATCH and, mod 256, a "loss" of 255 PDUs (STREAM_INTERRUPTED). Each such site now drives what the bench drove, an in-order stream with one PDU replaced. **No check, count or expectation changed.**

| File:line | Change |
|---|---|
| `tb/verilator/avtp_rxmon/sim_main_nx.cpp:339,346-348` | `[G5]`: the second reject carries 65, and the next PDU carries 66 (it was 64, 64, 64). "no mismatch across bad-format PDUs" now fails without the advance |
| `sim_main_nx.cpp:931,938-939,949,960` | `[UF2]`, `[UF3]`, `[UF4c]` rejects carry `q++`, and the `[UF2]` comment is updated. `[UF2g]` "...with no SEQ_NUM_MISMATCH" now fails without the advance |
| `sim_main_nx.cpp:130,991-1075` | the new `[SQ]` phase (next section) |
| `tb/verilator/avtp_rxmon/format_mutants.py:4,11-20,65-76` | three #775 mutants and the docstring |
| `tb/verilator/crf_rx/sim_main.cpp:191-197` | the replica's `bad_pdu(seq)` advances `exp_seq`; `have_seq` is untouched |
| `sim_main.cpp:500,687,783,809,817,1043,1306,1418,1426,1551` | every reject site passes the sequence_num it drove and consumes it (`m.bad_pdu(seq++)`). The pre-lock burst keeps seq 0 (`bad_pdu(0)`; no cursor is seeded there) |
| `sim_main.cpp:275,311,344` | `[SQ]` is wired into `run()`, plus a ts_p_o strobe tally |
| `sim_main.cpp:1523-1524,1560-1561` | the `[FMT]` comments say the cursor advances. `[FMT-c1]` now also fails without the advance |
| `sim_main.cpp:1570-1685` | the new `[SQ]` phase (next section) |
| `tb/verilator/crf_rx/sim_discontinuity.cpp:138,198` | the two in-place rejects consume their sequence number (`++seq`). "rejected marker never seeds the reference" fails without that, because the next PDU would be a repeat |
| `tb/verilator/crf_rx/mutants.py:7-15,83-92` | two #775 mutants and the docstring |
| `tb/verilator/milan_dp/sim_nxn.cpp:7047,7065-7067` | `[CTRS-CRF]` event arm: the seven rejects carry `cseq++`. The planned counts are unchanged and pass in the sweep (STREAM_INTERRUPTED 3, SEQ_NUM_MISMATCH 4, UNSUPPORTED_FORMAT 7, FRAMES_RX 21), because P2's two lost PDUs are now counted from the last reject |

## New checks, planted mutants, failing words

**AAF input, `tb/verilator/avtp_rxmon/sim_main_nx.cpp:991-1075` `[SQ]`, 22 checks (NX 147 -> 169).** Stream 3 is re-bound, given the 8-channel format and locked with 9 PDUs (`[SQ0]`).

- Mid-stream, one 2-channel PDU arrives carrying a toggled mr, tu and a timestamp already past (ptp_now = ts + 1000).
  - `[SQ1a]` no accept verdict.
  - `[SQ1b]` no payload emitted.
  - `[SQ1c]` prev_seq = its sequence_num.
  - `[SQ1d]` LAST_TSD unchanged.
  - `[SQ1e]` wire_chans stays 8.
- Six in-order PDUs follow, over two observation intervals.
  - `[SQ2a]` all six accepted.
  - `[SQ2b]` UNSUPPORTED_FORMAT +1.
  - `[SQ2c]` to `[SQ2i]`: SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, LATE_TIMESTAMP, EARLY_TIMESTAMP, STREAM_INTERRUPTED and MEDIA_UNLOCKED +0.
  - `[SQ2j]` FRAMES_RX +6.
- Then a second off-format PDU arrives, early (ptp_now = ts - 50 ms), with one PDU lost after it, then four in-order PDUs.
  - `[SQ3a]` all four accepted.
  - `[SQ3b]` SEQ_NUM_MISMATCH +1, so a real gap still counts.
  - `[SQ3c]` STREAM_INTERRUPTED +0: one PDU was lost counted from the off-format PDU's sequence_num, where two would be counted without the advance.
  - `[SQ3d]` UNSUPPORTED_FORMAT +1.
  - `[SQ3e]` EARLY_TIMESTAMP +0.
  - `[SQ3f]` MEDIA_RESET and TIMESTAMP_UNCERTAIN +0.

Mutants, in `format_mutants.py`. Each must make the harness fail by its own verdict, with the named check among the failures. The run is `receipts/suites-c7e87c8c/avtp_rxmon.log`, 9/9, and every failed check is listed there:

| Mutant (plant at `KL_avtp_rx_monitor_ctx.sv`) | Named check | Every check it fails |
|---|---|---|
| no advance: `:1019` writes `ram_q_r` back. This is the defect, and the planted control the assignment asks for | `[SQ2c] SEQ_NUM_MISMATCH unchanged: the next PDU was in sequence` | `no mismatch across bad-format PDUs`; `[UF2g] ...with no SEQ_NUM_MISMATCH`; `[SQ1c] ...and its sequence_num is prev_seq`; `[SQ2c]`; `[SQ3c] ...one PDU lost from the off-format PDU's: no STREAM_INTERRUPTED` |
| whole state: `:1019` writes `monst_next_w`, an accepted PDU's MON_STATE | `[SQ2d] MEDIA_RESET unchanged` | `[UF2e] ...and leaves wire_chans at 8`; `[UF4g] wire_chans follows the accepted PDU`; `[SQ1e] ...and wire_chans stays 8`; `[SQ2d]`; `[SQ3f] ...and MEDIA_RESET and TIMESTAMP_UNCERTAIN unchanged` |
| accepted walk: `:1020` goes to `M_PWR_S`, which also writes LAST_TS/LAST_TSD | `[SQ1d] ...and it writes no timestamp word (LAST_TSD)` | `[SQ1d]` |

**CRF input, `tb/verilator/crf_rx/sim_main.cpp:1570-1685` `[SQ]`, 23 checks.** The bound, locked input (`[SQ-0]`) gets one AAF PDU in a CRF PDU's slot, carrying a toggled mr, tu and a late reference timestamp (ptp_now = ts + 4 ms).

- `[SQ-a1]` it is not accepted.
- `[SQ-a2]` no timing point (ts_p_o).
- `[SQ-a3]` delta_o unchanged.
- `[SQ-a4]` the lock is kept.
- Six in-order PDUs follow, over two intervals.
  - `[SQ-b1]` UNSUPPORTED_FORMAT +1.
  - `[SQ-b2]` to `[SQ-b8]`: SEQ_NUM_MISMATCH, MEDIA_RESET, TIMESTAMP_UNCERTAIN, LATE_TIMESTAMP, EARLY_TIMESTAMP, STREAM_INTERRUPTED and MEDIA_UNLOCKED +0.
  - `[SQ-b9]` FRAMES_RX +6.
- An early AAF PDU, then one CRF PDU lost, then four in order.
  - `[SQ-c1]` SEQ_NUM_MISMATCH +1.
  - `[SQ-c2]` STREAM_INTERRUPTED +0.
  - `[SQ-c3]` UNSUPPORTED_FORMAT +1.
  - `[SQ-c4]` EARLY +0.
  - `[SQ-c5]` MEDIA_RESET and TU +0.
- `[SQ-d]`, after a re-bind: an AAF PDU first in the era, then an accepted PDU five numbers past it, then three more.
  - `[SQ-d1]` SEQ_NUM_MISMATCH 0.
  - `[SQ-d2]` STREAM_INTERRUPTED 0.
  - `[SQ-d3]` UNSUPPORTED_FORMAT 1.
  - `[SQ-d4]` FRAMES_RX 4.
  - Only an accepted PDU seeds the cursor (assignment item 2).

The harness's per-PDU replica compare also pins every counter against the replica, which carries the same rule.

Mutants, in crf_rx `mutants.py` UNIT_MUTANTS. The run is 23/23 (`receipts/suites-c7e87c8c/crf_rx.log`). Every failed check is listed in `receipts/crf-sq-mutants-detail/`, by `scripts/crf_sq_mutants_detail.py`, which plants the same anchors:

| Mutant (plant at `KL_crf_rx.sv`) | Named check | Every check it fails |
|---|---|---|
| `offformat_no_advance`: `:607` removed. This is the defect and the planted control | `[SQ-b2] SEQ_NUM_MISMATCH unchanged: the next PDU was in sequence` | `[5t-a5] clean stream: STREAM_INTERRUPTED still`; `[ST-c3] no phantom STREAM_INTERRUPTED: the cursor survived`; `[FMT-c1] the next CRF PDU is accepted with no SEQ_NUM_MISMATCH`; `[SQ-b2]`; `[SQ-c2] ...one PDU lost from the AAF PDU's: no STREAM_INTERRUPTED`; plus 170 per-PDU replica-compare failures |
| `offformat_seeds_sequence`: `have_seq_r <= 1'b1` added after `:607` | `[SQ-d1] an AAF PDU first in an era seeds no SEQ_NUM_MISMATCH` | `seq skip: ONE interval tick`; `clean resume: seq_err holds at 1`; `[SQ-d1]`; `[SQ-d2] ...nor a STREAM_INTERRUPTED`; plus 1,972 per-PDU replica-compare failures |

**The base RTL fails the head's harnesses as the bench did** (`receipts/base-rtl/`, `scripts/base_rtl.sh`). The head's harnesses were built against byte copies of dev `a032c6d6`'s `KL_avtp_rx_monitor_ctx.sv` and `KL_crf_rx.sv`:

- NX: rc 1, 5 failures: `no mismatch across bad-format PDUs` (got 3, exp 2), `[UF2g]` (got 1), `[SQ1c]` (got 48, exp 49), `[SQ2c]` (got 1), `[SQ3c]` (got 1).
- crf_rx unit: rc 1, 175 failures, among them `[FMT-c1]`, `[SQ-b2]` and `[SQ-c2]`.
- crf_rx discontinuity: rc 1, `rejected marker never seeds the reference`.

## Resource and route timing (route-1x1 against the eleventh record, 2026-10-23)

Recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, unchanged: the shipping AX7101 1x1 export from a clean clone at `c7e87c8c` (`scripts/route_export.sh`), `pp_baseline.py --single-thread-synthesis` (synth.maxThreads 1, general.maxThreads 32, synthesis and implementation in one process, the record's flow). Vivado v2026.1 SW Build 6511674. The run was started as `setsid nohup flock $VIVADO_LOCK route_vivado.sh ...`, after the sweep had ended. It waited for the exclusive lock behind another lane's out-of-context run and held it from 06:34 to 07:23 UTC, alone, with MemAvailable 48 GB at the start. `scripts/route_vivado.sh` restores the export's three links (builder out and the two ROM images, which the netlist names) for the run and removes them after; the clone was clean before and after.

The record is the eleventh, 2026-10-23 (#632/#764, PR #770), `inputs_sha256` `e67f9619...`. Its RTL inputs are lane head `5282b8b6`, an ancestor of `a032c6d6`, and `git diff 5282b8b6 a032c6d6` touches no `hdl/`, `sw/litex`, `configs` or submodule file, only the record itself. So the record measures this lane's base design, and every delta below is this change plus placement movement.

| Figure | Record (base design) | Head `c7e87c8c` | Delta | Gate verdict |
|---|---:|---:|---:|---|
| LUT | 51,259 | 51,313 | +54 | ok (tolerance 500) |
| FF | 53,208 | 53,218 | +10 | ok |
| **SLICE** | **15,835** | **15,833** | **-2** | ok, below the record. **STOP threshold +5: not reached** |
| RAMB36 / RAMB18 / DSP | 74 / 27 / 13 | 74 / 27 / 13 | 0 / 0 / 0 | ok |
| WNS ns | +0.236 | +0.141 | -0.095 | ok |
| WHS ns | +0.028 | +0.019 | -0.009 | ok |

- `syn/ooc/pp_resource_gate.py check <gateware> --endpoint route-1x1`: **rc 0, RESULT: PASS**. "route status: complete, no unrouted net and no routing error": 101,188 routable nets, all fully routed. "All user specified timing constraints are met" (TNS 0, THS 0, TPWS 0).
- The worst setup path is `FSM_onehot_socbushandler0_axilite2wishbone_state_reg[1]/C` -> `milansoc_spiflash_phy_cnt_reg[8]/D`, `milansoc_crg_clkout0`, 20 logic levels: the SoC bus, not logic this change reaches (`receipts/route-c7e87c8c/worst_setup_path.txt`).
- The gate's ungated sub-block movements are all inside the protocol processor (wrapper +112 LUT, u_aecp +109, u_pp +102, ... u_listener -19, u_notify -17; FF +0 everywhere). This change does not reach that logic, so they are synthesis and placement movement.
- The two changed blocks after place: `avtp_rx_monitor` (KL_avtp_rx_monitor_ctx) 727 LUT (623 logic, 104 LUTRAM), 743 FF, 1 RAMB18; `crf_rx` 227 LUT, 574 FF, 1 RAMB18. After synthesis: 811 and 231 LUT. No base route was run in this lane, so these block figures have no same-run base. The Yosys generic counts at base and head are in the gate table (-1 and +36 cells).
- `alinx_ax7101_timing.rpt` at the head: SHA-256 `480473270b9a62f36a34b615224210a50aaba46cbb7c5ca3bf6782c408af9662`, 1,303,432 B. It is kept in scratch with the checkpoints; digests are in `receipts/route-c7e87c8c/large-artifacts.sha256`.

## Gate table (head `c7e87c8c`, clean clones)

Verilator 5.050 (the pinned CI build), sv2v v0.0.12, Yosys 0.66, Vivado 2026.1 SW Build 6511674. The sweep and the suites ran on the host CPython 3.14.8, because `scripts/owned_process.py` needs `os.pidfd_open`. The static gates and the non-Markdown docs gates ran on CPython 3.12.3 (the CI image's); the five Markdown gates ran on the pinned Markdown environment, CPython 3.14.8.

| Gate | Result | Receipt |
|---|---|---|
| `make -C tb/verilator/avtp_rxmon` | rc 0: flat 97/0, NX 169/0, lockstep N=1 116/0, N=8 119/0, `lockstep_mutants.py` 14/14, `format_mutants.py` 9/9 | `suites-c7e87c8c/` |
| `make -C tb/verilator/crf_rx` | rc 0: unit 15,714/0, discontinuity 2,201/0, talker step 69/0, `mutants.py` 23/23 | `suites-c7e87c8c/` |
| Full sweep, `scripts/run_all_suites.sh <logs> --wait --shard k/4`, four parallel shard units, one clone each (MemoryMax 10G, -j4, CPUs 0-11/12-23/24-35/36-47) | **rc 0 on all four: 64/64 suites, 2,189,615 checks, 0 in-suite failures, 0 timeouts.** Shard 0: 15 suites, 54,074 checks (milan_dp: every leg and the render mutants; `[CTRS-CRF]` events read 2/1/3/4/5/6/7/8/9/21). Shard 1: 16 suites, 331,530. Shard 2: 17 suites, 262,066. Shard 3: 16 suites, 1,541,945 (avtp_rxmon, crf_rx). The sweep skips tsn_fuzz's tsn-gen campaigns (no `TSN_GEN_ROOT`) | `sweep-c7e87c8c/` |
| `syn/yosys/run.sh` | rc 0: 60/60 tops, tap purity PASS. `KL_avtp_rx_monitor_ctx` 10,991 cells (base 10,992); `KL_crf_rx` 30,776 (base 30,740), from `--top` runs at `a032c6d6` | `yosys-c7e87c8c/`, `yosys-base-a032c6d6/` |
| Lint: `scripts/lint_rtl.py --check` | rc 0: 89 violations <= ratchet 89 | `static-c7e87c8c/lint_rtl.log` |
| Static gates (`scripts/gates.sh`, 30): lint, test evidence, the four idiom gates, hygiene, port contracts, RTL source lists, TODO ownership, `check_em_dash.py --base a032c6d6`, doc style, doc paths, archive, feature status, solution, submodule and gPTP docs, diagram PNGs, bare-metal only, SoC sources, NVM capture and record space, `ci_events.py`, `ci_gate_workflows.py`, module matrix, resource-gate selftest and `check-baseline`, `git diff --check a032c6d6 HEAD`, `docs_check.py` | all 30 rc 0; the clone is clean before and after | `static-c7e87c8c/gates.tsv` |
| Docs workflow gates under GNU Make 4.3 (`scripts/docs_steps.py`: each step's `run:` body executed literally with `bash -e` from the clone root, with the job and step env): `wire-accountability/ci_step_4`, every `docs-gates-0` gate (gate_1 to gate_50), `gate_25_0`, `gate_25_1`, `gate_41` | 42 run, all rc 0. `gate_25_0` and `gate_25_1` (builder legs) first refused in 1 s: "source dependency origin differs: third_party/tsn-c-stack", because the scratch clone's submodule origins pointed at the lane. The origins were set to the `.gitmodules` URLs and both legs re-ran at the same head: rc 0 in 854 s and 248 s. Two are not run, with the reason: `gate_42` executes the candidate `act_ci.py` on the host (AGENTS.md section 5); `docs-check-no-git/ci_step_3` runs `rm -rf .git`, and its two gates, `docs_check.py` and `check_feature_status.py`, are in the static row | `docs-c7e87c8c/`, `docs-builder0-c7e87c8c/`, `docs-builder1-c7e87c8c/` |
| route-1x1 and `syn/ooc/pp_resource_gate.py check --endpoint route-1x1` | routed, rc 0; SLICE 15,833 (-2 against the record, STOP threshold +5 not reached), LUT +54, FF +10, WNS +0.141 ns, WHS +0.019 ns, all constraints met; **resource gate rc 0, RESULT: PASS** | `route-c7e87c8c/` |

Before the commits, the lane tree ran the same two suites with the same results, plus pre-commit idiom checks. A multi-declarator C++ line was found there and fixed before the commit (`pre-commit/`).

Not run, with the reason:

- tsn_fuzz: it builds only the flat `KL_avtp_rx_monitor` (`tb/verilator/tsn_fuzz/Makefile:114`), which this change does not touch.
- xvlog: not in the assignment's gate list; route-1x1 is the Vivado evidence.
- ooc endpoints: not assigned.

## Open risks / questions

- The flat test instrument `KL_avtp_rx_monitor` (no shipping module instantiates it; it is the DUT of tsn_fuzz and of avtp_rxmon's flat leg) keeps the old reject path: it leaves `prev_seq_r` untouched (`KL_avtp_rx_monitor.sv:265-269`). Not assigned and unchanged. Whether the instrument should follow is a possible new issue for the maintainer; none filed.
- The off-format PDU's own sequence_num is not graded: a gap or repeat on the discarded PDU counts nothing (it counts only UNSUPPORTED_FORMAT, the ruling). The next PDU is measured from it.
- On the CRF input, an AAF PDU in a CRF slot still restarts the 256-PDU rate ring at the next accepted PDU. Its timestamp spacing is two periods, so `ts_jump_w` fires. That is a measurement, not a counter, and it is unchanged from before (the old sequence mismatch restarted it too).
- No bench run (not allowed here). The bench check of #775 is for the test machine.

## Receipts

`receipts/` (index `receipts/INDEX.md`, generated from the files present by `receipts/scripts/gen_index.py`). Host paths in copied logs are replaced by placeholders (`<lane>`, `<clone>-*`, `<scratch>`, `<tools>`, `<tools-ci>`, `<sdk>`, `<home>`, `<out>`). A log over 200 KB is kept as its SHA-256 and size (`.sha256`) and its last 200 lines (`.tail`).

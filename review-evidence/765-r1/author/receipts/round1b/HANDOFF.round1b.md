# HANDOFF — lane 765 ([A657]), round 1b

Issue: kebag-logic/milan-fpga#765 — UNSUPPORTED_FORMAT counts and discards a PDU whose format differs from the current one.
Branch: `765-unsupported-format`, head `4605409b1f4f7388c6050af902d3af8b8c9c0e8c`. Nothing pushed; no PR opened (`PR-BODY.md` is ready).
Assignment: the [A10] ruling on #765 (issuecomment-6268149013), items 2 and 3, on top of the original assignment (issuecomment-6260493268).

## Status

REVIEW READY at `4605409b`, posted as issuecomment-6289875162 (text in `receipts/round1b/REVIEW-READY-COMMENT.md`). The route-1x1 resource gate passes (LUT 49,857, +244 over the record, tolerance 500, rc 0), so ruling item 3's first branch applies. Every gate below is rc 0 at this head. The full sweep passed in two shards: 63 suites, 0 failed, 2,187,728 checks. Two earlier sweep runs were cut by host resets, one after 22 of 63 suites and one in shard 1/2 after 21 of 31, every finished suite PASS. Neither counts; both are kept under `receipts/round1b/sweep-attempts/` (README there).

The round-1 hand-off (STOP at `cc71db3a`, LUT +545) is kept as `receipts/round1/HANDOFF.round1.md`, with its PR body and STOP comment.

## Re-stack (ruling item 2)

| Commit | What |
|---|---|
| `31903ec1`, `91aaa6bd`, `cc71db3a` | round 1, unchanged (ruling item 4) |
| `2f33a9ce` | **merge** of PR #767's round-2b head `eef90b42` (first parent `cc71db3a`, second `eef90b42`). #767's history is not rewritten |
| `4605409b` | two stale references after the merge: `docs/design/MEDIA_CLOCK_FOLLOWING.md:315,459` now point at the format check's lines at this head (`KL_avtp_rx_monitor_ctx.sv:497-528`, `:512-528`), and the crf_rx harness comment at `tb/verilator/crf_rx/sim_main.cpp:459` names the `[FMT]` case instead of "the end of the run" (#762's cases now follow it). No build input changes (`git diff --stat 2f33a9ce 4605409b -- hdl protocol-processor gptp-processor third_party sw configs syn` is empty) |

The RTL merged without a conflict, and both behaviours are kept:

- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv`: #762's `stopped_i` port (`:155`), the silence rule (`:913-918`, a bound **started** stream) and the gap rule (`:1027-1033`, `!stopped_i[ev_s_r]`) are byte-identical to `eef90b42`. The #765 compare (`:501`, `:508`, `:512-528`) is byte-identical to `cc71db3a`.
- `hdl/ieee1722/crf/KL_crf_rx.sv`: #762's `w_ev_si_w ... && !stop_i` (`:406`) and this lane's `w_hit` / `w_fmt_ok` (`:323-335`) are both present. They do not interact: a format reject is not `w_acc`, so it never reaches `w_ev_sm_w` / `w_ev_si_w`.
- Check: for every file, the merge's delta against `eef90b42` has the same changed lines as round 1's delta against `4191b098`, except the five resolved files below.

Conflicts resolved (both sides kept, in each case by concatenation):

| File | Resolution |
|---|---|
| `tb/verilator/crf_rx/sim_main.cpp:270-272` | the run calls `pin_aaf_pdu_on_the_crf_input()` where round 1 put it (after `pin_unbind_scores_one_unlock()`), then #762's `pin_stopped_silence_is_no_interruption()` and `pin_stopped_gap_is_no_interruption()`. Each #762 case re-establishes a started, locked sink first; `[FMT]` leaves the sink bound, started and locked |
| `tb/verilator/crf_rx/mutants.py:6-14, 46-107` | docstring names both sets; `UNIT_MUTANTS` (`:46-82`) holds #762's five and #765's three; #762's `BOTH_MUTANTS` (`:88-107`) follows unchanged |
| `tb/verilator/avtp_rxmon/Makefile:43-48` | comment names `REF_SRC` (#762) and `NX_MDIR` / `format_mutants.py` (#765) |
| `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:6-13` | header names #762's stop rule and #765's compare, each graded outside the reference |
| `docs/testing/TESTING.md` avtp_rxmon and crf_rx rows | #762's text, then #765's `[UF]` / `[FMT]` sentences; the reference's description names #765's compare too |

## Changes (file:line at `4605409b` — clause)

Unchanged in substance from round 1; lines moved by the merge.

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:501` | `f_cpf_w = fmt_r[31:22]`, the current format's 10-bit channels_per_frame | IEEE 1722-2016 I.2.4.1 |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:508` | `p_cpf_w = fsh[49:40]`, the PDU's 10-bit channels_per_frame | IEEE 1722-2016 7.3, Figure 26 |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:512-528` | `fmt_ok_w` adds `p_cpf_w == f_cpf_w` (nonzero kept); the comment citing the superseded BAF v1.1 reading is replaced | Milan v1.2 4.4.2.2, Table 5.6 UNSUPPORTED_FORMAT, Table 6.2; 1722-2016 I.2.4 |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:95-98` | banner: the flat `KL_avtp_rx_monitor` (test instrument, not shipped) keeps no channel compare | -- |
| `hdl/ieee1722/crf/KL_crf_rx.sv:323-328` | `w_hit` no longer requires the CRF subtype | Milan v1.2 Table 5.6, 4.4.2.2 |
| `hdl/ieee1722/crf/KL_crf_rx.sv:330` | `w_fmt_ok` requires `subtype_i == CRF_SUBTYPE_C`: an AAF PDU is a format reject | Milan v1.2 Table 5.6, 4.4.2.2, 7.3.2 |
| `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:13,483,489,506-509` | the lockstep reference applies the same compare (the #762 precedent) | -- |
| `docs/reference/FR_NFR.md` FR-STR-03 and its status row; `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 4.4.2.2 / Table 5.6 row; `docs/reference/REGISTER_MAP.md` `CRF_STATUS[15:8]`; `docs/design/MEDIA_CLOCK_FOLLOWING.md`; `docs/testing/TESTING.md` | as round 1 | FR-STR-03 |
| `tb/verilator/milan_dp/{Makefile,sim_main.cpp,sim_nxn.cpp,sim_prune.cpp,stream_counters.hpp}` | stimulus carries each input's current format (round 1) | -- |

No register-map layout, top-level port or parameter change from this lane (the `stopped_i` port is #767's).

## New checks and planted mutants (re-run at the merge)

AAF inputs, `tb/verilator/avtp_rxmon/sim_main_nx.cpp:903` `[UF]`, mutants in `format_mutants.py`:

| Check | Mutant (`format_mutants.py:line`) | Caught at the merge |
|---|---|---|
| `[UF1a]` `:920` matching 8 ch accepted | `inverted` (`:50`) | yes |
| `[UF2a]` `:929` 2 ch vs 8 ch rejected, discarded, UF +1 | `family compare` (`:42`) | yes |
| `[UF3a]` `:947` 264 ch (high bits) rejected | `low byte` (`:46`) | yes |
| `[UF4a]` `:958` format moved to 2 ch: 2 ch accepted, 8 ch rejected | `fixed count` (`:54`) | yes |
| `[UF5a]` `:974` stream 0 via `fmt0_i` | `stream 0` (`:58`) | yes |

CRF input, `tb/verilator/crf_rx/sim_main.cpp:1510` `[FMT]`, mutants in `mutants.py`:

| Check | Mutant (`mutants.py:line`) | Caught at the merge |
|---|---|---|
| `[FMT-a1]` matching CRF accepted | `crf_rejected` (`:78`) | yes |
| `[FMT-b1]` AAF on the CRF stream_id not accepted | `aaf_accepted` (`:74`) | yes |
| `[FMT-b3]` `:1548` counts UNSUPPORTED_FORMAT once | `aaf_ignored` (`:69`) | yes |
| `[FMT-c1]` `:1555` next CRF PDU, no SEQ_NUM_MISMATCH | -- | -- |

Merge-tree run before the merge commit (`receipts/round1b/merge-targeted/`): avtp_rxmon flat 97/97, NX 147/147, lockstep N=1 116/116 and N=8 119/119, `lockstep_mutants.py` 14/14 (#762's nine planted in both modules), `format_mutants.py` 6/6; crf_rx unit 15,379 checks / 0, discontinuity 2,201 / 0, talker step 69 / 0, `mutants.py` 21/21 (#762's seven, #765's three).

## Resource and route timing (route-1x1)

Recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, unchanged: shipping AX7101 1x1 export from a clean clone at `2f33a9ce` (build inputs identical at the head `4605409b`), `pp_baseline.py --single-thread-synthesis`, Vivado v2026.1 SW Build 6511674, under the exclusive lock, 20:22 to 21:06. Base = PR #767 lane's own route of `eef90b42` (same recipe, export script, tool build, pins; copied with `PROVENANCE.md`, not re-run). The exports differ only in RTL, paths and LiteX's timestamp / comment order (memory init files, `.xdc` and build script identical).

| Figure | Record | Base `eef90b42` | Candidate | Cand. - base | Gate verdict (cand.) |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,597 | 49,857 | +260 | ok (+244 over the record, tolerance 500) |
| FF | 52,353 | 52,400 | 52,291 | -109 | ok, below the record |
| SLICE | 15,725 | 15,680 | 15,738 | +58 | ok |
| RAMB36 / RAMB18 / DSP | 74 / 25 / 14 | 74 / 25 / 14 | 74 / 25 / 14 | 0 | ok |
| WNS ns | +0.215 | +0.189 | +0.137 | -0.052 | ok |
| WHS ns | +0.036 | +0.014 | +0.024 | +0.010 | ok |

- `syn/ooc/pp_resource_gate.py check --endpoint route-1x1`: **rc 0, RESULT: PASS**; route complete, no unrouted net, no routing error.
- Changed blocks (after place, LUT / FF): `avtp_rx_monitor` 800 / 741 -> 697 / 742; `crf_rx` 276 / 541 -> 282 / 541. After synthesis: 822 -> 750 and 278 -> 283.
- After synthesis the whole design moves +27 LUT (52,349 -> 52,376). After place it is +260: `KL_gptp_shadow` +258, top-level glue +103, `chan_map_render` +87, `aaf_packetizer` +64, `milan_csr` -164 (`receipts/round1b/route/hier-place-base-vs-cand.md`, `hier-synth-base-vs-cand.md`). None of those is reached by this RTL; the movement is placement.
- Per-clock WNS / WHS, base -> candidate: `clkout0` 0.189 / 0.063 -> 0.137 / 0.048; `clkout1` 0.498 / 0.014 -> 0.313 / 0.024; `clkout4` 1.391 / 0.121 -> 1.391 / 0.105; `eth_clocks0_rx` 0.870 / 0.083 -> 0.625 / 0.035; `audio_mclk_raw` 26.371 / 0.039 -> 25.585 / 0.079; `clk200_p` 3.810 / 0.227 -> 3.817 / 0.237.
- Worst setup path, candidate: `milansoc_write_w_buffer_readable_reg/C` -> `storage_10_dat1_reg[44]/D`, `clkout0`, data path 9.466 ns, 14 logic levels, in the SoC bus (base: inside the SoC CPU's DMA bridge). Not the changed logic.
- `alinx_ax7101_timing.rpt` candidate SHA-256 `79576ed304c52bd9f0d9fa14eb415e1df46829055df88e70578d85a17af6a8b6` (1,294,971 B); base `92526027b73badf98c426acc14cf93f7b14820dd2084d180835f3519fbbaf70f` (1,316,045 B).

Yosys generic cells (host Yosys 0.66, sv2v 0.0.12, clean clones at `eef90b42` and `2f33a9ce`, both run here): `KL_avtp_rx_monitor_ctx` 10,892 -> 10,992 (+100), `KL_crf_rx` 30,650 -> 30,684 (+34), `milan_datapath` 1,710,945 -> 1,711,480 (+535).

## Gate table

Head `4605409b` unless noted. Verilator 5.050 (pinned), sv2v 0.0.12, Yosys 0.66, Vivado 2026.1 build 6511674.

| Gate | Result |
|---|---|
| `scripts/run_all_suites.sh <logs> --shard 0/2` and `--shard 1/2` (63-suite sweep, lane tree at `4605409b`) | both rc 0. Shard 0: 32/32 PASS, 1,574,154 checks, 0 in-suite failures. Shard 1: 31/31 PASS, 613,574 checks, 0 in-suite failures. Total 63/63, 2,187,728 checks. The sweep skips tsn_fuzz's tsn-gen campaigns (no `TSN_GEN_ROOT`); they ran separately (next row) (`receipts/round1b/sweep-head/s0/`, `s1/`) |
| `make -C tb/verilator/tsn_fuzz` with `TSN_GEN_ROOT` at the CI pin `deca300c`, clean clone at `4605409b` | rc 0: AAF/AVTP 164 pass / 0 fail, gPTP 677 / 0, both artifact freshness checks PASS (the counts equal the committed `TEST_RESULTS.md`; only the timestamp line differs) (`receipts/round1b/tsnfuzz/`) |
| `make -C tb/verilator/milan_dp unb-mutants` (outside the sweep), clean clone at `4605409b` | rc 0, 6 checks: 6 PASS (`receipts/round1b/milan_dp-unb/`) |
| avtp_rxmon and crf_rx, merge tree before commit | rc 0 (above) |
| `syn/yosys/run.sh`, clean clone at `2f33a9ce` | rc 0, 58/58 tops, tied-input and tap-purity PASS |
| `scripts/xvlog_gate.py --check` (exclusive lock) | rc 0, 0 findings == ratchet |
| 29 static gates (`receipts/round1b/static-head/gates.tsv`) and `scripts/docs_check.py` | all rc 0 (CPython 3.12.3 venv); also rc 0 at `2f33a9ce` |
| route-1x1, clean clone at `2f33a9ce` | routed, rc 0; WNS +0.137 ns, WHS +0.024 ns |
| `syn/ooc/pp_resource_gate.py check --endpoint route-1x1` | **rc 0, PASS** (LUT +244 over the record) |

## Open risks / questions

- **PR #767 is still moving.** R663-2 is NEGATIVE at `eef90b42`, and #767 has a round-3 assignment (issuecomment-6274405031). Its branch now stands at `f3fef856`, five commits on `eef90b42`. In those commits the RTL changes only two comment lines (`KL_avtp_rx_monitor_ctx.sv:152`, `milan_datapath.sv:6307`). No build input changes, so this route stays valid. Everything else is in `tb/verilator/milan_dp/`: a new `[762-DP]` case in `sim_nxn.cpp` (+139 lines, a file this lane also edits), `dynmap_probes.vlt`, and README text. `git merge-tree` of this head with `f3fef856` reports no textual conflict. **There is a behaviour risk anyway**, which I inferred from the source and have not run. The new `prove_a_stopped_stream_input_counts_no_interruption()` feeds STREAM_INPUT 0 with `mkaaf(sid0, seq, 2, 0xC0)`, a fixed 2-channel PDU. This lane's compare rejects that PDU on any leg where the input's current format is not 2 channels, so its "started ... locked" check would fail there. Round 1 had to change 11 cases for exactly this reason. When this branch takes #767's next head, that case needs the same `rx_chans(0)` / `aaf_bytes()` change. This lane was assigned `eef90b42` and has merged nothing later. Dev has moved to `e26f1816` (PR #766), which this branch has not merged either.
- Round 1's open risks stand unchanged: the short-frame depacketizer commit window on the pruned 1x1 leg; inputs above 0 reading their current format only from LCTX words 2/3; samples_per_frame has no PDU field; the flat test instrument keeps no channel compare. New issues recommended; none filed.
- `docs/design/MEDIA_CLOCK_FOLLOWING.md` also carries `KL_crf_rx.sv:<line>` references (`:295-299`, `:494`, `:516`, `:531`, `:632`, `:759`, `:973`, `:991`, `:1832`) that do not land on what they describe, already at dev `e9cbb676`. Not this lane's; left alone.
- The sweep runs on the host CPython 3.14.8, as in round 1: the provided 3.12.3 build lacks `os.pidfd_open`, which `scripts/owned_process.py` requires.

## Receipts

`receipts/` (index `receipts/INDEX.md`, generated from the files present). Host paths in copied logs are replaced by placeholders; a log over 200 KB is kept as its SHA-256, size and last 200 lines (`.tail`).

- `round1b/sweep-head/s0/`, `s1/`: the two sweep shards at `4605409b` (`runner-summary.out` in each); `round1b/sweep-attempts/`: the runs that produced no verdict.
- `round1b/tsnfuzz/`, `round1b/milan_dp-unb/`: the tsn-gen campaigns and `unb-mutants`, clean clone at `4605409b`.
- `round1b/merge-targeted/`: avtp_rxmon and crf_rx on the resolved merge tree.
- `round1b/route/`: `base-eef90b42/` (copied, with `PROVENANCE.md`), `cand-2f33a9ce/`, hierarchy comparisons.
- `round1b/static/` (at `2f33a9ce`), `round1b/static-head/` (at `4605409b`), `round1b/yosys/`, `round1b/xvlog/`.
- `round1b/scripts/`: the scripts that produced them (paths replaced).
- `round1/`: round 1's hand-off, PR body and STOP comment. Every other top-level directory is round 1's evidence at `cc71db3a` / `91aaa6bd`.

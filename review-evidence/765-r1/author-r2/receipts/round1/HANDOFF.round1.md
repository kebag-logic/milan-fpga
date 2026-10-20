# HANDOFF — lane 765 ([A657])

Issue: kebag-logic/milan-fpga#765 — UNSUPPORTED_FORMAT counts and discards a PDU whose format differs from the current one.
Branch: `765-unsupported-format`, stacked on PR #767 head `4191b098` (two commits on dev `e9cbb676`).
Assignment: the newest [A10] comment on #765 (items 1-4).

## Status

**STOP** at head `cc71db3a557bb6160c81e69a52fd3ceed6622dc5`: all work done and every gate rc 0 except the route-1x1 **resource gate, rc 1** (LUT +545 over the record, tolerance 500). Accepting it is a reviewed re-record under `docs/design/AREA_BUDGET.md`, not this lane's decision. Comment text: `STOP-COMMENT.md`, posted as issuecomment-6268128740 on #765; TAKEN was issuecomment-6260543554. Nothing pushed; no PR opened (`PR-BODY.md` is ready).

Commits (one-line subjects, configured identity, no trailers):

- `31903ec1` RTL + tests + mutant arms.
- `91aaa6bd` docs (FR-STR-03, compliance matrix, register map, test index, media-clock design doc).
- `cc71db3a` milan_dp harnesses feed each Stream Input in its current format.

No register-map layout, top-level port or parameter change (the assignment's STOP condition is not hit; the STOP is the gate).

## Changes (file:line — clause)

| File:line | Change | Clause |
|---|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:496` | `f_cpf_w = fmt_r[31:22]`, the current format's 10-bit channels_per_frame | IEEE 1722-2016 I.2.4.1 (format layout) |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:503` | `p_cpf_w = fsh[49:40]`, the PDU's full 10-bit channels_per_frame | IEEE 1722-2016 7.3, Figure 26 |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:507-523` | `fmt_ok_w` adds `p_cpf_w == f_cpf_w` (and keeps a nonzero count); the comment citing the superseded BAF v1.1 reading is replaced | Milan v1.2 4.4.2.2, Table 5.6 UNSUPPORTED_FORMAT, Table 6.2; 1722-2016 I.2.4 (ut = 0 in a current format) |
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:93-96` | banner: the flat `KL_avtp_rx_monitor` (test instrument, not shipped) keeps no channel compare; delta recorded | -- |
| `hdl/ieee1722/crf/KL_crf_rx.sv:321-326` | `w_hit` no longer requires the CRF subtype: a Stream Data AVTPDU on this input's stream_id is received on it | Milan v1.2 Table 5.6 ("received ... on this Stream Input"), 4.4.2.2 |
| `hdl/ieee1722/crf/KL_crf_rx.sv:328` | `w_fmt_ok` requires `subtype_i == CRF_SUBTYPE_C`: an AAF PDU is a format reject (UNSUPPORTED_FORMAT, not accepted, lock kept, sequence unmoved) | Milan v1.2 Table 5.6, 4.4.2.2, 7.3.2 |
| `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:11,480,486,503` | the lockstep reference gains the same compare in its own lines (the #762 precedent), so the #640 M6 cycle comparison stays exact; #765 is graded by `[UF]`, never against this copy | -- |
| `docs/reference/FR_NFR.md` FR-STR-03 row and the FR-STR-03 status row | discard required; clauses cited; CRF subtype; inputs above 0 read their format from LCTX only | FR-STR-03 |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md` new 4.4.2.2 / Table 5.6 row | live traceability entry; closes the v1 family-compare record (task #24) | 4.4.2.2 |
| `docs/reference/REGISTER_MAP.md` `CRF_STATUS[15:8]` | description names the subtype check (layout unchanged) | -- |
| `docs/design/MEDIA_CLOCK_FOLLOWING.md` source table and meter section | the format check is no longer a family compare; line references moved | -- |
| `docs/testing/TESTING.md` avtp_rxmon and crf_rx rows | `[UF]`, `format_mutants.py`, `[FMT]` | -- |

The only record of the family compare as a 4.4.2.2 divergence is `docs/history/v1/reference/PROTOCOL_TRACEABILITY.md:318,342`, an archived page that "never defines current behavior" (`docs/README.md` History). It is left as archived evidence; the live entry is the new compliance-matrix row, which states that it closes the v1 record.

## New checks and planted mutants

AAF inputs, `tb/verilator/avtp_rxmon/sim_main_nx.cpp:902` `[UF]` (N=4 stack: table + parser + context engine + depacketizer + route). Discard is read at the depacketizer: no accept verdict and no emitted payload.

| Check | Case | Mutant (`format_mutants.py`) | Caught |
|---|---|---|---|
| `[UF1a]` `:920` | matching PDU (8 ch vs 8 ch) accepted, emitted, no UF, FRAMES_RX +1 | `inverted`: `p_cpf_w != f_cpf_w` (`:50`) | yes |
| `[UF2a]` `:929` | 2 ch vs 8 ch: no verdict, discarded, UF +1, FRAMES_RX and wire_chans unchanged, next matching PDU accepted with no SEQ_NUM_MISMATCH | `family compare`: the channel term deleted (`:42`) | yes |
| `[UF3a]` `:947` | 264 ch (channels_per_frame[9:8] = 1, low byte 8) vs 8: rejected | `low byte`: `p_cpf_w = {2'b00, fsh[47:40]}` (`:46`) | yes |
| `[UF4a]` `:958` | current format moved to 2 ch through LCTX: 2 ch accepted, 8 ch rejected | `fixed count`: `f_cpf_w = 10'd8` (`:54`) | yes |
| `[UF5a]` `:974`, `[UF5d]` `:981` | stream 0's format from `fmt0_i`: 2 ch rejected at 8 ch, accepted at 2 ch | `stream 0`: `fmt_r <= {fmt0_i[63:32], fmt_r[31:0]}` (`:58`) | yes, by `[UF5a]` |

Positive control: the unmutated engine passes (6/6). Existing `[R3]` (`:500`) sent 2 ch against the 8 ch format; it now sets stream 1's current format to 2 ch first, as SET_STREAM_FORMAT would, and restores it.

CRF input, `tb/verilator/crf_rx/sim_main.cpp:1508` `[FMT]`:

| Check | Case | Mutant (`mutants.py`) | Caught |
|---|---|---|---|
| `[FMT-a1]` `:1521` | matching CRF PDU accepted, no UF | `crf_rejected`: `subtype_i != CRF_SUBTYPE_C` (`:70`) | yes |
| `[FMT-b1]` `:1536` | AAF subtype, otherwise a valid 7.3.2 profile, on the CRF stream_id: not accepted, lock kept | `aaf_accepted`: subtype dropped from `w_fmt_ok` (`:66`) | yes |
| `[FMT-b3]` `:1540` | ...counts UNSUPPORTED_FORMAT once | `aaf_ignored`: subtype restored in `w_hit` (the old behaviour) (`:61`) | yes |
| `[FMT-c1]` `:1547` | next CRF PDU continues the sequence (no SEQ_NUM_MISMATCH) | -- | -- |

The gating case at `:449` keeps a wrong stream_id ignored for both subtypes.

### Integration harnesses whose stream-0 stimulus no longer matched its format (milan_dp)

The first sweep at `91aaa6bd` failed `milan_dp` only: 36 checks in 11 cases across counters-1/-8 (and -frames), notify `[UNB]`, nxn/nxn8/nxn4c/nxndv 5.3.8.7, ax1x1 and prune. Every one fed STREAM_INPUT 0 with a channel count other than that input's current format (2 channels into the 4-channel `arty_4x4` and 8-channel AX7101 shapes; 8 channels into the 2-channel `arty_current` prune leg). The new compare rejects them, as #765 requires. The stimulus now carries the current format; no check was removed or weakened.

| File | Change |
|---|---|
| `tb/verilator/milan_dp/Makefile` | `in0_fmt` / `in0_fmt_cflags` read `ADP_STRIN0_FMT_C` out of the shape header each build includes and pass it as `IN0_FMT_TB` to every `sim_main.cpp` and `sim_prune.cpp` build (base, option-off, nolpf, prune, AX1X1_BUILD) |
| `tb/verilator/milan_dp/sim_main.cpp` | `kIn0ChansTb` from `IN0_FMT_TB` (`#error` if unset); `mkaaf` carries it. The 48-byte payload is kept (the harness's beat counts and captured frames are built on it); no check reads the sample count |
| `tb/verilator/milan_dp/sim_prune.cpp` | `kAafChans` from `IN0_FMT_TB` (2 on this shape), six samples per channel; the window format copy is the same value; the frame is zero-padded to the 230 octets this leg fed before (see open risks) |
| `tb/verilator/milan_dp/sim_nxn.cpp` | `rx_chans(s)`: STREAM_INPUT 0 from GET_STREAM_FORMAT (the processor's current format, which the `fmt0_i` fold serves), inputs above 0 from the harness's LCTX `FMT_LO`; `aaf_bytes`; `mkaaf` writes `stream_data_length = 24 x chans`; the 5.3.8.7 case and `unb_pdu` use the current count |
| `tb/verilator/milan_dp/stream_counters.hpp` | `counter_feed` uses `counter_state.rx_chans[s]`, read once in `counter_setup` |

## Resource and route timing

Recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, unchanged: shipping AX7101 1x1 export from a clean clone at `91aaa6bd` (RTL and every build input identical at the head `cc71db3a`; `git diff --stat 91aaa6bd cc71db3a -- hdl protocol-processor gptp-processor third_party sw configs syn` is empty), `pp_baseline.py --single-thread-synthesis`, Vivado v2026.1 build 6511674, background job under the exclusive lock, 10:46 to 11:34. Base = the PR #767 lane's route of `4191b098` (same recipe, tool build, submodule pins and Tcl; copied with provenance, not re-run). The exports differ only in the RTL and in LiteX's generation timestamps (memory init files identical).

| Figure | Record | Base `4191b098` | Candidate | Cand. - base | Gate verdict (cand.) |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,411 | 50,158 | +747 | **REGRESSION: grew by more than 500** (+545 over the record) |
| FF | 52,353 | 52,297 | 52,312 | +15 | ok |
| SLICE | 15,725 | 15,751 | 15,609 | -142 | ok, re-baseline recommended |
| RAMB36 / RAMB18 / DSP | 74 / 25 / 14 | 74 / 25 / 14 | 74 / 25 / 14 | 0 | ok |
| WNS ns | +0.215 | +0.161 | +0.363 | +0.202 | ok |
| WHS ns | +0.036 | +0.036 | +0.015 | -0.021 | ok (floor 0) |

- `pp_resource_gate.py check --endpoint route-1x1`: **rc 1** (MATERIAL REGRESSION, LUT only); route status complete, no unrouted net, no routing error.
- Changed blocks (hierarchical, after place, LUT / FF): `avtp_rx_monitor` 778 / 732 -> 749 / 734; `crf_rx` 253 / 541 -> 281 / 541. Net -1 LUT.
- Where the +746 lies (after place): `KL_gptp_shadow` +281, SoC CPU `VexiiRiscvLitex_...` +239, top-level glue +201, `chan_map_render` +89, `ctl_tx_mux` +79, `milan_csr` -118 (`receipts/route/hier-place-base-vs-cand.md`). After synthesis alone the design is already +621 (CPU +369, top +248; `hier-synth-base-vs-cand.md`), so the movement starts in the flattened area-optimised synthesis, not in placement. `AREA_BUDGET.md` (route policy, combination B) charges such movement to the change and makes accepting it a reviewed re-record.
- Per-clock WNS / WHS base -> candidate: `clkout0` 0.161 / 0.069 -> 0.363 / 0.065; `clkout1` 0.608 / 0.036 -> 0.759 / 0.015; `clkout4` 1.391 / 0.121 unchanged; `eth_clocks0_rx` 0.420 / 0.067 -> 0.955 / 0.118; `clk200_p` 3.815 / 0.237 -> 3.489 / 0.191.
- Worst setup path, candidate: `VexiiRiscvLitex_.../dma_bridge_write_bridge/aligner/downW_header_reg[2]/C` -> `.../onPerId_bridge/pendings_valids_reg[0]/D`, `clkout0`, data path 9.583 ns, 19 logic levels, in the SoC CPU; not the changed logic.
- `alinx_ax7101_timing.rpt` candidate SHA-256 `52e42427dd372503c5a4bb1ff346234b233044bf5de20f167dd92878f8bf72c6` (1,307,948 B).

Yosys generic cells (host Yosys 0.66, sv2v 0.0.12, clean clone at `91aaa6bd`): `KL_avtp_rx_monitor_ctx` 10,936 -> 10,957 (+21), `KL_crf_rx` 30,660 -> 30,674 (+14), `milan_datapath` 1,710,797 -> 1,711,031 (base figures from the PR #767 lane).

## Gate table

Head `cc71db3a` unless noted. Verilator 5.050 (pinned), sv2v 0.0.12, Yosys 0.66, Vivado 2026.1 build 6511674.

| Gate | Result |
|---|---|
| `scripts/run_all_suites.sh <logs>` (63-suite sweep, in the lane tree) | **rc 0. 63/63 suites, 2,186,679 checks, 0 failures, 0 timeouts.** Ran under the host CPython 3.14.8: the provided 3.12.3 build lacks `os.pidfd_open`, which `scripts/owned_process.py` requires. Its 4 declared skips are the tsn-gen campaigns, run next |
| `make -C tb/verilator/tsn_fuzz` with `TSN_GEN_ROOT` at the CI pin `deca300c` | rc 0: AAF/AVTP campaign 164 pass / 0 fail, gPTP 677 / 0, both freshness checks PASS (the two `TEST_RESULTS.md` rewrites changed only their timestamp line and were restored) |
| avtp_rxmon (in the sweep) | flat 97/97, NX 147/147, lockstep 53/53 at N=1 and N=8, lockstep_mutants 8/8, **format_mutants 6/6** |
| crf_rx (in the sweep) | unit 14,468 checks / 0, discontinuity, talker step 69/69, **mutants 18/18** |
| milan_dp (in the sweep) | rc 0; every case also rc 0 one by one in a clean clone (`receipts/milan_dp/run2-harness-fixed`) |
| `make -C tb/verilator/milan_dp unb-mutants` (the `[UNB]` section changed), clean clone | 6/6 |
| `syn/yosys/run.sh`, clean clone at `91aaa6bd` (RTL identical) | rc 0, 58/58 tops PASS, tied-input and tap-purity PASS |
| `scripts/xvlog_gate.py --check` (exclusive lock) | rc 0, 0 findings == ratchet |
| 29 static gates (`receipts/final-static/gates.tsv`): lint_rtl, measure_test_evidence, py/cpp/sv/sh idiom, hygiene, port contracts, RTL source lists, TODO ownership, em dash, doc style/paths, archive, feature status, solution/submodule/gPTP docs, diagram PNGs, bare-metal-only, SoC sources, NVM capture/record space, ci_events, ci_gate_workflows, module matrix, resource-gate selftest and check-baseline, `git diff --check` | all rc 0 (CPython 3.12.3 venv with the locked renderer and PyYAML) |
| route-1x1 (clean clone at `91aaa6bd`, build inputs identical at the head) | routed, rc 0; WNS +0.363 ns, WHS +0.015 ns |
| `syn/ooc/pp_resource_gate.py check --endpoint route-1x1` | **rc 1, MATERIAL REGRESSION (LUT +545 over the record)**; see above |

Not run: `sw/builder/test_builder.py` (no builder input changed).

## Open risks / questions

- **Short frames miss the depacketizer's commit window (pre-existing, outside #765).** On the pruned 1x1 leg (`sim_prune.cpp`, `arty_current`, `PRUNE_G`), 16 conformant 2-channel PDUs in bare 86-octet frames are all accepted by the monitor (FRAMES_RX 16, no format error) and none is emitted (PCMRX_CNT 0). The same at the base commit `4191b098`; padded to 120 octets, 15 of 16; to 230, 16 of 16. The depacketizer commits only if the verdict lands before the frame's last beat. A real 2-channel Milan stream uses 86-octet frames (90 tagged). The leg pads to 230 to keep its subject (structural zeros); recommend a new issue. Receipts: `receipts/milan_dp/short-frame-*`.

- Inputs above 0 take their current format only from LCTX w2/w3 (the CSR window `A_STRMW_FMT_LO/HI`); the processor's SET_STREAM_FORMAT reaches stream 0 only (`hdl/milan/milan_datapath.sv:3379`), and no firmware writes those words. Pre-existing, but the compare now also depends on the channel count there. Shipping route-1x1 has one input. Recommend a new issue.
- samples_per_frame is part of a Table 6.2 format but no PDU field carries it (1722-2016 I.2.4.1 ties only channels_per_frame to the PDU). It is implied by stream_data_length; no check added (out of the issue's scope, recorded already in `MEDIA_CLOCK_FOLLOWING.md`).
- The flat `KL_avtp_rx_monitor` (test instrument, not shipped) keeps no channel compare; the context engine's banner records the delta.

## Receipts

`receipts/` (index `receipts/INDEX.md`, generated from the files present). Host paths in copied logs are replaced by placeholders; a log over 200 KB is kept as its SHA-256, size and last 200 lines (`.tail`).

- `commit1/`: the targeted avtp_rxmon and crf_rx runs and mutant campaigns before the first commit.
- `static/`, `final-static/`: the static gates (first pass, and at the head with `gates.tsv`); xvlog.
- `yosys/`: the Yosys gate.
- `milan_dp/`: run 1 (old harness, failing, with `FAIL-lines.txt`), run 2 (fixed harness, every case plus `unb-mutants`), `short-frame/` (the depacketizer reproduction, with its own README).
- `route/`: `base-4191b098/` (copied, with `PROVENANCE.md`), `cand-91aaa6bd/`, and the hierarchy comparisons.
- `sweep-final-cc71db3a/` (the gate sweep and tsn_fuzz with tsn-gen), `sweep-first-91aaa6bd-cancelled/`, `sweep-attempts/` (refused and cancelled launches, with a README).

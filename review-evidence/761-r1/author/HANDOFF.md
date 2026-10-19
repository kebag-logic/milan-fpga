# HANDOFF: lane 761 ([A652]) -- issues #761 and #762

Status: REVIEW READY -- every gate below is rc 0 at head `4191b098`, the route-1x1 resource gate included.

- Repository: kebag-logic/milan-fpga, branch `761-762-mr-interrupt` (local only, not pushed), base dev
  `e9cbb676d7fdd6539aa408e5dfe38870a4ae1a5f`.
- Assignment: issue #761 comment 6256482625. TAKEN: issuecomment-6256557482. REVIEW READY: issuecomment-6260470296
  (text in `REVIEW-READY-COMMENT.md`).
- Commit 1 (#761): `f443ed9befd924015ceda9eff226e99a213ab99d` -- "Request a media clock restart on the selected
  CRF's return as on its loss (#761)".
- Commit 2 (#762): `4191b0987d1313abc86c747ad6a9c3c0963f17da` -- "Count a silence that unlocks a bound Stream Input
  as STREAM_INTERRUPTED, never an unbind (#762)". Head; tree `5c21b067`.
- STOP conditions checked: no register-map, top-level port or parameter change (no port, parameter or CSR is added,
  removed or renamed; `REGISTER_MAP.md` only gains prose on counter semantics).

## Changes, with clause

### #761 (commit 1)

| Where | Change | Clause |
|---|---|---|
| `hdl/milan/milan_datapath.sv:3249` | `mcr_restart_p_w`'s CRF term is `(tkd_crflk_q_r ^ crf_locked_w)`, either edge of the selected CRF sink's lock, instead of the falling edge alone. Still gated by `crf_clk_selected_r`; the received-mr echo and the two AAF-meter terms are unchanged | IEEE 1722-2016 4.4.4.3 (a change of the media clock's source needs a restart; holdover -> CRF is one) and its CRF-disruption sentence |
| `hdl/milan/milan_datapath.sv:3191`, `:3200` | comments: the rising edge is the return | same |
| `hdl/ieee1722/avtp/KL_media_clock_restart.sv:170` | port comment lists the return among `restart_p_i`'s causes (no logic change) | same |
| `sw/builder/test_builder.py` (`direct_initializer` for `mcr_restart_p_w`, the ADP-splice mutation's reason, the boot-contract description) | the pinned initializer text follows the new term | -- |
| `tb/verilator/milan_dp_gm_steps/gmstep_mutants.py:80`, `:161` | `CRF_RESTART_TERMS` anchor and the "selected CRF mr propagation is removed" replacement follow the new term (the replacement keeps both lock edges) | -- |
| Docs: `MEDIA_CLOCK_FOLLOWING.md` (test-plan row, `mr` section, restart step), `GM_LOSS_RECOVERY.md`, `BAREMETAL_FIRMWARE.md` (pinned expression row, now the full initializer), `MILAN_COMPLIANCE_MATRIX.md` 4.4.4.3 row, `TESTING.md` mclk row, mclk `README.md` | behaviour and mutant inventory | -- |

### #762 (commit 2)

| Where | Change | Clause |
|---|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:322` | new per-stream `sil_si_r`: the pending unlock is the silence watchdog's | Milan v1.2 5.3.8.10 Table 5.6 (STREAM_INTERRUPTED: any interruption other than a Controller Unbind), 5.4.2.25 Table 5.16 |
| `:905` | the 100 ms watchdog marks `sil_si_r` when the stream is bound and not unbinding this cycle | same |
| `:892` | `bind_fall_i` clears it: an unbind, even one landing on a pending silence unlock, never counts | same |
| `:1063-1074` | at the end of the unlock walk, a marked silence queues `C_SI_C` into `inc_list_r` and continues in `M_INC_S`, the ordinary RMW that yields to PDU pressure (parked remainder, bind-wipe rules unchanged) | same |
| `:1138` | the bind decode clears `sil_si_r` with `sil_pend_r` | 5.3.8.10 era rule |
| `:17-34`, `:92-93` | banner: the two causes of STREAM_INTERRUPTED; the flat `KL_avtp_rx_monitor` delta | -- |
| `hdl/ieee1722/crf/KL_crf_rx.sv:556` | the 100 ms timeout of a locked sink counts `cnt_intr_o` when `en_i && !stop_i`; the gap increment cannot land in the same cycle (a started sink's accept refreshes the timeout) | Table 5.6 |
| `KL_crf_rx.sv:83-92`, `:636-639` | banner and unbind comment | -- |
| `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv` | the lockstep reference (dev `e8454e27`'s engine) gains the same #762 lines and a header saying so, so the #640 M6 comparison stays exact on every column; #762 itself is graded by count, never against this copy | -- |
| Docs: `REGISTER_MAP.md` (CRF counter paragraph), `MILAN_COMPLIANCE_MATRIX.md` 5.4.2.25 row, `TESTING.md` avtp_rxmon row, rxmon `Makefile` and lockstep wrapper comments | -- | -- |

## New checks and their planted mutants

| Check (file:line) | Planted mutant | Caught |
|---|---|---|
| mclk `CRF return: one request at the sink's re-lock` and one `mr` toggle per output (`sim_mclk.cpp:898-900`), leg B and the new `--crfloss` short leg (`:1147`) | 17: the lock-gain edge dropped, `tkd_crflk_q_r & ~crf_locked_w` (`mclk_mutants.py:181`) | yes, named check fails |
| mclk `CRF loss: one request at the sink's timeout` (existing, `sim_mclk.cpp:882`) | 18: the lock-loss edge dropped, `~tkd_crflk_q_r & crf_locked_w` (`mclk_mutants.py:183`) | yes |
| lockstep `[SI] a silence that unlocks a bound stream counts STREAM_INTERRUPTED once` (`sim_lockstep.cpp:483`), and the resume adds nothing | `silence:` the watchdog never marks its unlock (`lockstep_mutants.py:92`) | yes, N=1 and N=8 |
| lockstep `[SI] a sequence gap of two lost PDUs counts STREAM_INTERRUPTED once` (`:499`) | `gap:` the gap term removed (`lockstep_mutants.py:96`) | yes |
| lockstep `[SI] an unbind of a locked stream counts no STREAM_INTERRUPTED` (`:505`), nor the silence after it | `unbind:` an unbind marks the interruption (`lockstep_mutants.py:100`) | yes |
| lockstep `[SI]` sweep: unbind at 60 offsets across the silence unlock, MU once, SI at most once, both orders seen (`:515-541`) | (boundary sweep; the three mutants above also break the comparison) | -- |
| lockstep `[H3] ...and that silence counts STREAM_INTERRUPTED on from the wrap` (`:443`); the SI wrap check now reads before the interval wait that outlasts the silence timeout | -- | -- |
| crf_rx `[762-a] silence: STREAM_INTERRUPTED counts the silence once`, `[762-b]` resume adds none (`sim_main.cpp:603`, `:625`) | `silence_not_interrupted` (`mutants.py:41`) | yes |
| crf_rx `[5t-e2]` (existing gap check) | `gap_not_interrupted` (`mutants.py:44`) | yes |
| crf_rx `[UNB-a6]` (existing unbind check) | `unbind_interrupts`: the unbind's unlock counts SI (`mutants.py:48`) | yes |
| crf_rx `[UNB-d0b]`, `[UNB-d5] ...the unbind wins the edge` (`sim_main.cpp:1575`, `:1593`) | `unbind_edge_timeout_interrupts`: the `en_i` gate removed (`mutants.py:54`) | yes |
| avtp_rxmon N=4 stack `[G6-762]` (`sim_main_nx.cpp:355`, `:359`) | (integration twin of the lockstep checks) | -- |
| milan_dp `[CTRS-CRF] events: ...and the silence counts STREAM_INTERRUPTED @8` (`sim_nxn.cpp:5656`); the event plan keeps ten distinct counts (P4 now loses one PDU: SI 2 gaps + silence = 3, SM 4) | (root binding; the static_assert keeps the counts distinct) | -- |

The crf_rx driver gained a `unit-build` target (`Makefile`) so its #762 mutants run the counter harness; its
positive control `unit_clean` passes.

## Resources and route timing

Recipe `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`, unchanged: shipping AX7101 1x1 export from a fresh clean clone
per tree, `pp_baseline.py --single-thread-synthesis`, Vivado v.2026.1 (lin64) build 6511674, `xc7a100tfgg484-2`,
synth `AreaOptimized_high`, opt `ExploreArea`, place `ExtraPostPlacementOpt`, phys_opt and route
`AggressiveExplore`, default seed; each run a background job under the exclusive lock. The two exports differ only in
LiteX's generation timestamps; the RTL is each clone's own.

| Figure | Record | Base `e9cbb676` | Candidate `4191b098` | Cand. - base | Gate verdict (cand.) |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,613 | 49,411 | -202 | ok, below the baseline |
| FF | 52,353 | 52,353 | 52,297 | -56 | ok, below the baseline |
| SLICE | 15,725 | 15,725 | 15,751 | +26 | ok |
| RAMB36 / RAMB18 / DSP | 74 / 25 / 14 | 74 / 25 / 14 | 74 / 25 / 14 | 0 | ok |
| WNS ns | +0.215 | +0.215 | +0.161 | -0.054 | ok (floor +0.030) |
| WHS ns | +0.036 | +0.036 | +0.036 | 0 | ok |

- `pp_resource_gate.py check --endpoint route-1x1`: base rc 0 (identical to the record), candidate **rc 0**, route
  status complete, no unrouted net, no routing error.
- Changed blocks (hierarchical utilization after place, LUT / FF): `avtp_rx_monitor` 777 / 740 -> 778 / 732,
  `crf_rx` 237 / 541 -> 253 / 541. `milan_datapath` 41,063 -> 40,829 LUT; the rest of the movement is placement and
  optimization variation outside the change (the gate's own sub-block list puts the largest in the processor).
- Per-clock WNS, base -> candidate: `clkout0` 0.215 -> 0.161, `clkout1` 0.607 -> 0.608, `clkout4` 1.383 -> 1.391,
  `eth_clocks0_rx` 0.798 -> 0.420, `clk200_p` 3.523 -> 3.815; every WHS unchanged or better.
- Worst setup path, candidate: `VexiiRiscvLitex_.../dma_bridge_write_bridge/aligner/downW_header_reg[0]/C` ->
  `.../dma_bus_aw_rValid_reg/D`, `milansoc_crg_clkout0` (10 ns), data path 9.771 ns, 20 logic levels, in the SoC CPU.
  Base: `FSM_onehot_socbushandler0_axilite2wishbone_state_reg[3]/C` -> `milansoc_spiflash_phy_cnt_reg[8]/D`, 17 levels.
  Neither touches the changed logic.
- `alinx_ax7101_timing.rpt`: base SHA-256 `ebd3e67c668e2c68369ca8096cc2fffd4b0f3ad5ba17db78d736136da4b916e8`
  (1,326,646 B), candidate `0b08d76aef77276efc8d6f6c7dfa5df511ae4b2991e59c14eda46776655bbb61` (1,310,778 B).

Yosys generic cells (same host Yosys 0.66, sv2v 0.0.12): `KL_avtp_rx_monitor_ctx` 10,829 -> 10,936 (+107),
`KL_crf_rx` 30,459 -> 30,660 (+201); `milan_datapath` at the head 1,710,797.

## Gate table (head `4191b098` unless noted)

| Gate | Result |
|---|---|
| 63-suite sweep, `scripts/run_all_suites.sh <logs> --shard i/5`, i = 0..4, two clean clones, CI's CPython 3.12.3 build (`python-3.12.3-linux-24.04-x64.tar.gz`, SHA-256 `07ef2452a390e765...`, 121,683,532 B), Verilator 5.050, sv2v 0.0.12, tsn-gen `deca300c` | rc 0 x5. **63/63 suites, 2,187,305 checks, 0 failures, 0 timeouts.** Shards 0: 11/11, 12,518; 1: 13/13, 35,543; 2: 12/12, 424,706; 3: 13/13, 1,672,586; 4: 14/14, 41,952. Union of shard lists equals `--list` (63). Shard 3's first attempt was refused in the runner's own preflight cancellation control (`test_suite_cancellation.py`: "owned descendants remain", no suite started); rerun clean, both attempts kept |
| `syn/yosys/run.sh` (full serial), clean clone | rc 0, 58/58 tops PASS, tied-input and tap-purity gates PASS |
| `scripts/xvlog_gate.py --check` (exclusive lock) | rc 0, 0 findings == ratchet |
| `sw/builder/test_builder.py --require-rv32` | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, the historical calibration that needs a local mf48 build tree) |
| 42 static gates (`receipts/final-static/gates.tsv`) | all rc 0 |
| `make -C tb/verilator/milan_dp_gm_steps gmstep-mutants` (all 20 controls), clean clone at `f443ed9b` | 22/22 PASS |
| `make -C tb/verilator/milan_dp_mclk` at the lane | 34/34 (3 legs, 13 controls, 18 mutants) |
| avtp_rxmon / crf_rx / milan_dp at the committed tree (scratch clone, tree `5c21b067`) | rc 0 each; lockstep 53/53 at N=1 and N=8, lockstep mutants 8/8, crf_rx mutants 15/15 |
| `syn/ooc/pp_resource_gate.py check --endpoint route-1x1` | **rc 0** candidate (base rc 0, equal to the record); WNS +0.161, WHS +0.036, fully routed |

## Open questions to publish

- A followed AAF stream's return still raises no restart: the issue and assignment name the CRF only, and the
  4.4.4.3 shall names CRF; `MEDIA_CLOCK_FOLLOWING.md` now says so explicitly.
- A STOPPED CRF sink's 100 ms timeout still unlocks without counting STREAM_INTERRUPTED: it is not a silence (frames
  may still arrive), but Table 5.6 excludes only an Unbind, so a ruling may want a Controller stop counted.
- The flat `KL_avtp_rx_monitor` (a test instrument, not shipped) keeps the old law; the context engine's banner
  records the delta.
- The silence walk pulses `dirty_p_o` at its MEDIA_UNLOCKED write and STREAM_INTERRUPTED lands a few cycles later
  through the yielding RMW -- the same ordering the PDU walk already uses for MEDIA_LOCKED and the gap's SI.

## Receipts

`receipts/` (index: `receipts/INDEX.md`, generated from the files present). Logs over 200 KB are kept by SHA-256 and
size with their last 200 lines.

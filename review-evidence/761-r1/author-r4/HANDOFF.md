# HANDOFF: lane 761 ([A652]) -- issues #761 and #762

Current status: **Round 3 REVIEW READY at head `d30a208d`** -- see Round 3 at the end (R663-2: the datapath grade of the AAF `stopped_i` wiring, two comments, the PR body's status lines). Round 2b (head `eef90b42`, pushed as PR #767) and Round 2 precede it; Round 2 supersedes round 1 where they differ (notably the `:892` Unbind clear, removed in round 2).

Round 1 status: REVIEW READY -- every gate below is rc 0 at head `4191b098`, the route-1x1 resource gate included.

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

# Round 2 (assignment: PR #767 comment 6260976498; ruling: #762 comment 6260976223)

Status: REVIEW READY at head `2cd2750d0a07b8516328de7c0b57773ed0000f45` (local, not pushed; PR #767 not edited), three
commits on `4191b098`. Every gate this change touches is rc 0, route-1x1 and the resource gate included; two self-tests
fail on this host only and are explained below. Round 2 REVIEW READY posted on #761: issuecomment-6265725347 (text in
`REVIEW-READY-R2-COMMENT.md`).

| Commit | Subject |
|---|---|
| `ba9ac06a1` | Derive the over-shard receipt control from the mclk driver's real case count |
| `492207f71` | Count a silence once its watchdog expires, whatever Unbind follows, and never on a stopped input (#762) |
| `2cd2750d0` | Grade each #762 boundary trial in its own function, inside the C++ length rule |

Inputs read: the assignment, the #762 ruling, R664-1 (6260664989) and R663-1 (6260969105), and R664-1's published probes
(`review-evidence/761-r1/reviews/R664-1/probe_silence_order.py`, `probe_stopped_silence.cpp`, branch
`761-review-evidence` at `defe80cff`). Lane 765 is stacked on `4191b098` and edits `KL_avtp_rx_monitor_ctx.sv`: the engine
delta here is one removed line, one added port and one widened condition, plus comments.

## Item 1 -- R663-1-F1 (BLOCKER): gate_50 over-shard control

| Where | Change |
|---|---|
| `scripts/ci_case_receipts_selftest.py:174` | the refused over-shard count is `f"0/{len(names) + 1}"`, one more than the mclk driver's real inventory (34 cases now, so `0/35`), instead of the fixed `0/32`. The accepted `len(names)`-way split above it is unchanged, so the control still sits exactly one past the largest legal count |

Planted mutant: the count set to `len(names)` (a legal split, i.e. the vacuous form) makes the selftest fail with
`AssertionError: receipt control accepted: shard 0/34` (rc 1).

## Item 2 -- R664-1-F1 (MAJOR): a later Unbind erased a silence interruption

Cause: the watchdog marked `sil_si_r` at the expiry, the walk consumed it at its phase 3, and `bind_fall_i` cleared it in
between, so an Unbind landing after the MEDIA_UNLOCKED write and before phase 3 lost the count.

| Where | Change | Clause |
|---|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:894` (was `:892`) | the `if (bind_fall_i[s]) sil_si_r[s] <= 1'b0;` clear is removed. The watchdog's expiry is now the one event boundary for both writes: the mark and the unlock request are set in the same cycle, and nothing but the walk's own consume, the bind-era wipe (`:1138` area, unchanged) and reset clears the mark | Milan v1.2 5.3.8.10 Table 5.6 (STREAM_INTERRUPTED: any interruption other than a Controller Unbind) |
| `:910-911` | the mark needs `bound_i[s] && !bind_fall_i[s] && !stopped_i[s]` at the expiry. In the datapath `bound_i` falls one cycle before `bind_fall_i` (`KL_stream_table` registers the edge), so an Unbind on or before the expiry edge leaves no mark and its unlock counts nothing | same |
| `:28-36` | banner: the two causes, the started condition, and that an unbind after the expiry leaves the silence counted | -- |
| `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv` | the same lines, so the #640 M6 cycle comparison stays exact; its header says #762 is graded by count and that every #762 mutant is planted in both copies | -- |

## Item 3 -- R664-1-F2 / R663-1-F2: the #762 stopped-input ruling in both engines

| Where | Change | Clause |
|---|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:151-153` | new input `stopped_i[N]`, the per-stream bound-and-stopped level | Milan v1.2 5.3.8.7 (a stopped input discards its AVTPDUs: no playback), 5.4.2.19 / 5.4.2.20 (START / STOP change the state) |
| `:910` | `!stopped_i[s]` in the silence mark: a stopped input's silence unlocks it (MEDIA_UNLOCKED) and counts no STREAM_INTERRUPTED. STOP with live traffic: the monitor sits upstream of the 5.3.8.7 discard and keeps accepting, so nothing unlocks and nothing counts. After START the mark is armed again | Table 5.6 and the #762 ruling |
| `hdl/milan/milan_datapath.sv:6307-6308` | `.stopped_i (acmpl_stopped_v_w[N_STREAMS-1:0])`, the same vector the listener accept gate and `KL_aaf_clock_meter` already use (bound AND not started; an entry with no ACMP binding is never stopped) | 5.3.8.7 |
| `hdl/ieee1722/crf/KL_crf_rx.sv:91-93` | comment only: the stopped timeout's reason. The CRF logic already implements the ruling (`:557`, `en_i && !stop_i`) | same |
| `tb/verilator/avtp_rxmon/avtp_rxmon_lockstep_wrap.sv`, `avtp_rxmon_nx_wrap.sv`, `Makefile` | the wrapper drives `stopped_i` into both copies; the N=4 stack ties it to 0 (every input started); `REF_SRC` makes the reference overridable so mutants plant into both | -- |
| `docs/reference/REGISTER_MAP.md:873-889` | the ruling stated exactly, for both engines, with 5.3.8.7, 5.4.2.19, 5.4.2.20, Table 5.6 and the ruling link, and the expiry as the one boundary | -- |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 5.4.2.25 row, `docs/testing/TESTING.md` avtp_rxmon and crf_rx rows | the same law and the new checks and mutants | -- |

## New checks, each graded by count (never against the reference or the replica), and their mutants

The AAF oracle (`tb/verilator/avtp_rxmon/sim_lockstep.cpp:306`, `silence_expiry_edge`) is the harness's own: it owns the
reset, so it knows the 1 ms grid (CLK_FREQ_HZ_P / 1000 = 10 cycles from reset release); it sees the stream's last accept on
`pdu_accept_p_o`; the expiry is the 100th grid tick after it. Expected: an event sampled after that edge leaves exactly one
interruption, one on or before it none, and the stream unlocks once either way. The clean run passing at every swept cycle,
at both shapes, is itself the check that this model of the time base is exact.

| Check (file:line) | Planted mutant (both copies for #762) | Caught |
|---|---|---|
| `[SI] boundary (an unbind, idle/busy): after the expiry the silence counts once, on or before it never` (`sim_lockstep.cpp:695`, trials `:644`): offsets -200, -40, every cycle -12..+24, +40, +80; liveness: sampled before the expiry, during the walk, between its MU and SI writes, and after it | `consume race` -- the bind_fall clear reinstated (`lockstep_mutants.py:114`) | yes, only by this check, N=1 and N=8, idle and busy |
| `[SI] boundary (a STOP, idle/busy): ...` | `stop at the walk` -- the stopped state read at the walk's phase 3 instead of at the expiry (`:120`) | yes |
| `[SI] a stopped input's silence unlocks it but counts no STREAM_INTERRUPTED` (`si_stop_rule`, `:576`), MEDIA_UNLOCKED +1 | `stopped` -- `!stopped_i[s]` dropped (`:117`) | yes |
| `[SI] START: ...relocks`, `...the resume counts no STREAM_INTERRUPTED`, `after START a silence counts STREAM_INTERRUPTED again` | (same mutants) | -- |
| `[SI] STOP with live traffic unlocks nothing` / `counts no STREAM_INTERRUPTED`; `START after stopped live traffic: the next silence counts once` | -- | -- |
| `[SI] an unbind of a stopped, locked input unlocks it once` / `...counts no STREAM_INTERRUPTED` | `unbind` (re-anchored) | yes |
| busy liveness (N=8): `some interruption write yielded to a PDU walk` (6 trials), `the load held the unlock walk longer than an idle engine does` (138 vs 3 cycles); N=1 busy: depacketizer pulses held it 5 vs 3 | -- | -- |
| CRF `[762-ST-a1..e3]` (`tb/verilator/crf_rx/sim_main.cpp:1628`): started silence +1; stopped silence after an established lock: MU +1, SI +0; START: relock, resume +0, later silence +1; STOP with live traffic: lock times out once, SI +0; Unbind: MU +1, SI +0, nor the silence after | `stopped_silence_interrupts` -- `en_i && !stop_i` -> `en_i` (`mutants.py:59`), named check `[762-ST-b2]` | yes |

The earlier `silence`, `gap` and `unbind` lockstep mutants are now also planted in both copies, and each is still caught
by an `[SI]` count check. R663-1's `aaf_both` edit is this round's fix; its converse (the clear reinstated in both copies) is
the `consume race` mutant above, killed by `[SI]`.

## Reviewer probes at the new head

- R664-1 `probe_silence_order.py`, with its call-site anchor moved from the replaced sweep to `si_stop_rule();` and
  `make -j8` (diff in receipts): N=1 113 checks, N=8 115 checks, 0 failures; interruption = 1 at every delay 0..8 after the
  committed MEDIA_UNLOCKED (it was 0 at delay 0 on `4191b098`).
- R664-1 `probe_stopped_silence.cpp`, unchanged: rc 1 by design, because its oracle is the pre-ruling frozen acceptance:
  started MU 1 / SI 1, stopped MU 1 / SI 0. The same probe with the ruling's expectation (diff in receipts): rc 0.

## Resources and route timing (route-1x1)

Same recipe as round 1 (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`; shipping AX7101 1x1 export from a fresh clean clone at
`2cd2750d`; `pp_baseline.py --single-thread-synthesis`; Vivado v.2026.1 build 6511674; `xc7a100tfgg484-2`; default seed),
one background run under the exclusive lock, 09:08:29 -> 09:59 (receipts `r2-route/`). The base is round 1's route of
`e9cbb676`, which equals the record.

| Figure | Record = base `e9cbb676` | Round 1 `4191b098` | Round 2 `2cd2750d` | R2 - base | Gate verdict (R2) |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,411 | 49,509 | -104 | ok, below the baseline |
| FF | 52,353 | 52,297 | 52,348 | -5 | ok, below the baseline |
| SLICE | 15,725 | 15,751 | 15,649 | -76 | ok, below the baseline |
| RAMB36 / RAMB18 / DSP | 74 / 25 / 14 | 74 / 25 / 14 | 74 / 25 / 14 | 0 | ok |
| WNS ns | +0.215 | +0.161 | +0.287 | +0.072 | ok (floor +0.030) |
| WHS ns | +0.036 | +0.036 | +0.036 | 0 | ok |

- `pp_resource_gate.py check --endpoint route-1x1`: **rc 0**, route status complete, no unrouted net, no routing error.
- Changed blocks (hierarchical utilization after place, LUT / FF), base -> R2: `avtp_rx_monitor` 777 / 740 -> 777 / 741,
  `crf_rx` 237 / 541 -> 234 / 541 (comment-only change), `milan_datapath` 41,063 -> 41,021 LUT. The remaining movement is
  placement and optimization variation outside the change (the gate's sub-block list is all in the processor).
- Per-clock WNS / WHS at R2: `clkout0` +0.287 / +0.065, `clkout1` +0.593 / +0.036, `clkout4` +1.304 / +0.121,
  `eth_clocks0_rx` +0.704 / +0.094, `clk200_p` +3.617 / +0.159.
- Worst setup path at R2: `milansoc_write_w_buffer_readable_reg/C` -> `storage_15_reg_4/ENARDEN` (RAMB18E1),
  `milansoc_crg_clkout0` (10 ns), data path 8.901 ns, 12 logic levels, in the SoC bus fabric; it does not touch the changed
  logic.
- `alinx_ax7101_timing.rpt` at R2: SHA-256 `f49d59186f401615076b85740bb6065285833e040dd030734afaee8803a7c5cf`
  (1,306,649 B), kept in scratch.
- Yosys generic cells: `KL_avtp_rx_monitor_ctx` 10,829 (base) -> 10,936 (R1) -> 10,810 (R2); `KL_crf_rx` 30,660 (R1 and R2);
  `milan_datapath` 1,710,889 at R2.

## Gate table (head `2cd2750d`, clean clones, CI's CPython 3.12.3 build, Verilator 5.050, sv2v 0.0.12)

| Gate | Result | Receipts |
|---|---|---|
| docs gate_50, all fourteen commands (`.github/workflows/docs.yml` step `gate_50`) | rc 0 x14 at `ba9ac06a` and at `2cd2750d`; `shard 0/35 refused`, `34 driver cases` | `r2-gate50/` |
| over-shard control mutant (`len(names)`, a legal split) | selftest rc 1, `receipt control accepted: shard 0/34` (caught) | `r2-gate50/ba9ac06a-mutant_vacuous_shard.log` |
| 63-suite sweep, `scripts/run_all_suites.sh <logs> --shard i/5`, i = 0..4, two clean clones, tsn-gen `deca300c` | **63/63 suites, 2,188,042 checks, 0 failures, 0 timeouts**, rc 0 x5. Shard 0: 11/11, 12,518; 1: 13/13, 35,543; 2: 12/12, 424,777; 3: 13/13, 1,673,252; 4: 14/14, 41,952. Union of the shard lists equals `--list` (63). Inside it: mclk 34/34, avtp_rxmon lockstep mutants 11/11, crf_rx mutants 16/16 | `r2-sweep/` |
| sweep attempts not counted | (a) the first launch ran under `nohup`, which ignores SIGHUP for every child, so the runner's own preflight cancellation control (`hard-HUP`) refused all five shards before any suite ran; relaunched without it. (b) shard 3's first clean attempt failed one suite, `gptp_shadow`'s process-lifecycle control (`CLEANUP FAILED: owned descendants remain` after its SIGKILL case) at host load ~100; the suite and `scripts/owned_process.py` are unchanged by this branch; shard 3 re-run in the second clone: 13/13 | `r2-sweep/nohup-attempt-*`, `attempt1-shard3*` |
| `make -C tb/verilator/avtp_rxmon` (clean clone) | rc 0: flat 97, N=4 stack 121, lockstep 86 (N=1) / 88 (N=8), mutants 11/11 | `r2-focused/c2-avtp_rxmon.log` |
| `make -C tb/verilator/crf_rx` (clean clone) | rc 0: 14,956 + 2,201 + 69 checks, mutants 16/16 | `r2-focused/c2-crf_rx.log` |
| `make -C tb/verilator/milan_dp` (clean clone) | rc 0, every shape 0 failures (root `[UNB]` U3: STREAM_INTERRUPTED 0 on AAF and CRF) | `r2-focused/c2-milan_dp.log.tail` |
| `make -C tb/verilator/milan_dp_gm_steps gmstep-mutants` (clean clone) | 22/22 | `r2-gmstep/` |
| R664-1 probes at the head | `probe_silence_order.py` rc 0 at N=1 and N=8 (interruption 1 at delays 0..8); `probe_stopped_silence.cpp` rc 1 on its pre-ruling oracle (started 1/1, stopped 1/0), ruling copy rc 0 | `r2-probes/` |
| `syn/yosys/run.sh` (full serial) | rc 0, 58/58 tops, tied-input and tap-purity gates PASS | `r2-final/yosys.log` |
| `scripts/xvlog_gate.py --check` (exclusive lock) | rc 0, 0 findings == ratchet | `r2-final/xvlog.log` |
| `sw/builder/test_builder.py --require-rv32` | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, the calibration that needs a local mf48 build tree) | `r2-final/builder.log` |
| every other docs-workflow gate command (82, incl. the HDL reference build with the pinned `pyslang`, wavedrom with the pinned `wavedrom`, lint ratchet, em-dash vs `e9cbb676`) | 80 rc 0; two self-tests fail on this host only: `act_ci.py --selftest` (16 process-group containment probes; the file is unchanged and an unchanged copy at `ba9ac06a` fails the identical 16) and `check_todo_ownership.py --selftest`'s git-absent case (this host's CPython 3.12.3 build cannot start with a stripped environment, rc 127; 45/45 under the host Python 3.14.8). The checks themselves (`check_todo_ownership.py`, and no file of the act runner) pass or are untouched | `r2-static/gates-all.tsv` |
| `syn/ooc/pp_resource_gate.py check --endpoint route-1x1` | **rc 0**; WNS +0.287, WHS +0.036, fully routed | `r2-route/` |

Not run: the hosted `docs-gates-*`, `docs-check` and the act replica, because the head is not pushed (pushing is outside
this lane). Physical calibration NOT RUN; no hardware.

## Open questions (round 2)

- A sequence gap on a STOPPED input still counts STREAM_INTERRUPTED, in both engines alike (both keep observing a stopped
  input). The #762 ruling covers a silence; a gap while stopped is left as is.
- A followed AAF stream's return still raises no restart (unchanged from round 1).
- R663-1-S1 (a dynamic ungated-edge row in the mclk suite) is not taken; the builder pin still refuses that edit.

## Receipts

`receipts/INDEX.md` lists every file present with its size and SHA-256, generated from the directory. Round 2's folders
are the `r2-*` ones.

# Round 2b (ruling: #762 comment 6265746720, extended stopped-input rule)

Status: REVIEW READY -- head `eef90b4238b6c19b679b44adc6f09362809be153` (local, not pushed; PR #767 not edited), one
commit on `2cd2750d`: "Count no STREAM_INTERRUPTED for a sequence gap on a stopped input, in both engines (#762)". Every
gate the change touches is rc 0, route-1x1 and the resource gate included; the same two host-only self-tests as round 2
fail and are explained below. Round 2b REVIEW READY posted on #761: issuecomment-6273816545 (text in
`REVIEW-READY-R2B-COMMENT.md`).

The ruling (read exactly): a stopped input has no playback (Milan v1.2 5.3.8.7, 5.4.2.20), so Table 5.6 has nothing to
count for any interruption. A sequence gap on a stopped input counts no STREAM_INTERRUPTED in `KL_avtp_rx_monitor_ctx.sv`
and `KL_crf_rx.sv`; a started input's gap counts once; after START a gap counts again. The second round-2 open risk (an
AAF stream's return raising no restart) stays as is.

## Changes, with clause

| Where | Change | Clause |
|---|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:1020-1026` | the gap term that queues `C_SI_C` gains `&& !stopped_i[ev_s_r]`; the stopped state is read at the PDU's accept verdict (`M_PDEC_S`), the gap's one boundary. The engine delta is one widened condition plus a two-line comment (lane 765 also edits this file) | Milan v1.2 5.3.8.7 (a stopped input discards its AVTPDUs: no playback), 5.4.2.19 / 5.4.2.20, 5.3.8.10 Table 5.6 STREAM_INTERRUPTED |
| `KL_avtp_rx_monitor_ctx.sv:28-32` | banner: both causes count only while the input is started | same |
| `hdl/ieee1722/crf/KL_crf_rx.sv:399-401` | `w_ev_si_w` gains `&& !stop_i`; read on the gap PDU's own accept edge (`w_acc`). SEQ_NUM_MISMATCH (`w_ev_sm_w`) is unchanged | same |
| `KL_crf_rx.sv:91-94` | banner: a stopped sink's gaps count SEQ_NUM_MISMATCH but not STREAM_INTERRUPTED | -- |
| `tb/verilator/avtp_rxmon/reference/KL_avtp_rx_monitor_ctx_ref.sv:1009-1015`, header `:6-11` | the same line, so the #640 M6 comparison stays exact; the rule is graded by count | -- |
| `tb/verilator/crf_rx/sim_main.cpp:167-169` | the C++ replica carries the same rule (`&& !stop`), so the per-PDU replica compare stays exact | -- |
| `docs/reference/REGISTER_MAP.md:875-899` | the rule list gains the three gap rules and the gap's boundary, linking the extended ruling | -- |
| `docs/reference/MILAN_COMPLIANCE_MATRIX.md:131` (5.4.2.25 row), `docs/testing/TESTING.md:614`, `:625` | the same law, the new checks and the new mutants | -- |

No port, parameter, CSR or register-map field is added, removed or renamed.

## New checks, graded by count, and their planted mutants

| Check (file:line) | Planted mutant (engine AND reference / replica) | Caught |
|---|---|---|
| AAF `[SI] a stopped input's sequence gap counts no STREAM_INTERRUPTED` (`sim_lockstep.cpp:675`), `...nor does a second stopped gap`, `...and the stopped gaps unlock nothing`; liveness `the stopped gaps were seen: SEQ_NUM_MISMATCH moved` (`:680`) | `stopped gap` -- the `!stopped_i` term dropped (`lockstep_mutants.py:132`) | yes, N=1 and N=8 (12 checks broke) |
| AAF `[SI] after START a sequence gap counts STREAM_INTERRUPTED again` (`:686`); control `[SI] a started input's sequence gap counts STREAM_INTERRUPTED once` (`:666`) | `sticky stop` -- a STOP disarms the gap until the next bind (`:135`) | yes (11 checks broke) |
| AAF `[SI] another input's STOP leaves this input's gap counted` (`:691`, N=8 only) | -- | -- |
| AAF `[SI] gap boundary (a STOP / a START, idle / busy): the gap counts once when started at its verdict, never when stopped` (`si_gap_boundary`, `:706`, check `:771`): the event lands on every edge from 4 before to 20 after the gap PDU's pulse; the verdict edge is where `pdu_accept_p_o` rises for that stream; every trial starts at one phase of the 500-cycle interval so the verdict wait is constant. Liveness: landed before the pulse, before the verdict, on it and after it; busy held the verdict longer (N=1: 4 vs 2 cycles; N=8: 15 vs 3) | `gap stop late` -- the stopped state read one cycle after the verdict (`:142`) | yes, only by the sweep (8 checks broke) |
| CRF `[762-SG-b1]` `stopped gap: no STREAM_INTERRUPTED`, `-b2`, `-b3`; liveness `-b4` one SEQ_NUM_MISMATCH interval (`sim_main.cpp:1753-1758`) | `stopped_gap_interrupts` (`mutants.py:73`) | yes; only `[762-SG]` count checks fail, no replica compare (receipt) |
| CRF `[762-SG-c1] after START a gap counts STREAM_INTERRUPTED again` (`:1766`); `[762-SG-a1]` started gap counts once | `sticky_stop_gap` (`mutants.py:77`) | yes; only `[762-SG]` count checks fail |
| CRF `[762-SG-d1..d5]` (`:1772-1782`): a STOP on the gap's own edge counts nothing, one an edge later leaves it counted; a START on the gap's edge counts it, one an edge later does not | (both mutants above break d1-d5) | -- |

The existing `gap` mutant (AAF) and `gap_not_interrupted` (CRF) follow the moved line and are still caught by
`[SI] a sequence gap of two lost PDUs counts STREAM_INTERRUPTED once` and `[5t-e2]`. The CRF driver now builds every
counter-harness case, its positive control included, from a copy of `sim_main.cpp` in the temporary directory
(`UNIT_CPP`, with `-I` in the existing warning-carrying `-CFLAGS`), so a mutant can be planted in the replica.

## Resources and route timing (route-1x1)

Same recipe as rounds 1 and 2 (`docs/testing/PP_SHADOW_BASELINE_RECIPE.md`; shipping AX7101 1x1 export from a fresh clean
clone at `eef90b42`; `pp_baseline.py --single-thread-synthesis`; Vivado v.2026.1 build 6511674; `xc7a100tfgg484-2`;
default seed), one background run under the exclusive lock, 16:08:21 -> 17:04:36 (receipts `r2b-route/`).

| Figure | Record = base `e9cbb676` | Round 2 `2cd2750d` | Round 2b `eef90b42` | R2b - base | Gate verdict (R2b) |
|---|---:|---:|---:|---:|---|
| LUT | 49,613 | 49,509 | 49,597 | -16 | ok, below the baseline |
| FF | 52,353 | 52,348 | 52,400 | +47 | ok |
| SLICE | 15,725 | 15,649 | 15,680 | -45 | ok, below the baseline |
| RAMB36 / RAMB18 / DSP | 74 / 25 / 14 | 74 / 25 / 14 | 74 / 25 / 14 | 0 | ok |
| WNS ns | +0.215 | +0.287 | +0.189 | -0.026 | ok (floor +0.030) |
| WHS ns | +0.036 | +0.036 | +0.014 | -0.022 | ok |

- `pp_resource_gate.py check --endpoint route-1x1`: **rc 0**, `RESULT: PASS`, route status complete, no unrouted net, no
  routing error. Its sub-block list (not gated) is all in the protocol processor (`u_pp/...`, largest `u_aecp/u_dyn` +75
  LUT), which this change does not touch.
- Changed blocks (hierarchical utilization after place, LUT / FF), base -> R2 -> R2b: `avtp_rx_monitor` 777 / 740 ->
  777 / 741 -> 800 / 741; `crf_rx` 237 / 541 -> 234 / 541 -> 276 / 541; `milan_datapath` 41,063 -> 41,021 -> 41,064 LUT.
  Each engine gains one AND term; the rest of the movement is placement and optimization variation.
- Per-clock WNS / WHS at R2b: `clkout0` +0.189 / +0.063, `clkout1` +0.498 / +0.014, `clkout4` +1.391 / +0.121,
  `eth_clocks0_rx` +0.870 / +0.083, `clk200_p` +3.810 / +0.227.
- Worst setup path: `VexiiRiscvLitex_.../dma_bridge_write_bridge/aligner/downW_header_reg[0]_replica/C` ->
  `.../dma_bus_aw_rValid_reg/D`, `clkout0` (10 ns), data path 9.740 ns, 19 logic levels, in the SoC CPU (round 1's worst
  path too). Worst hold path: `milan_datapath/g_tdm_render_live.g_master.chan_tdm_render/bank_r_reg[2][7]/C` ->
  `.../u_fcdc/mem_r_reg_0/DIBDI[23]`, `clkout1`, +0.014 ns, in the TDM render FIFO. Neither touches the changed logic.
- `alinx_ax7101_timing.rpt` at R2b: SHA-256 `92526027b73badf98c426acc14cf93f7b14820dd2084d180835f3519fbbaf70f`
  (1,316,045 B), kept in scratch.
- Yosys generic cells: `KL_avtp_rx_monitor_ctx` 10,810 (R2) -> 10,892; `KL_crf_rx` 30,660 -> 30,650; `milan_datapath`
  1,710,889 -> 1,710,945.

## Gate table (head `eef90b42`, clean clones, CI's CPython 3.12.3 build, Verilator 5.050, sv2v 0.0.12)

| Gate | Result | Receipts |
|---|---|---|
| lane runs before commit: lockstep N=1 / N=8, `lockstep_mutants.py`, crf_rx counter harness, `mutants.py` | 116 / 119 checks, 0 failures; mutants 14/14; 15,202 checks; mutants 18/18. The CRF engine+replica mutants run directly: only `[762-SG]` count checks fail | `r2b-lane/` |
| docs gate_50, all fourteen commands | rc 0 x14; `shard 0/35 refused`, `34 driver cases` | `r2b-gate50/` |
| 63-suite sweep, `scripts/run_all_suites.sh <logs> --shard i/5`, i = 0..4, two clean clones, tsn-gen `deca300c` | **63/63 suites, 2,188,354 checks, 0 failures, 0 timeouts**, rc 0 x5, no re-runs. Shard 0: 11/11, 12,518; 1: 13/13, 35,543; 2: 12/12, 424,841; 3: 13/13, 1,673,500; 4: 14/14, 41,952. Union of the shard lists equals `--list` (63). Inside it: mclk 34/34, avtp_rxmon lockstep mutants 14/14, crf_rx mutants 18/18 | `r2b-sweep/` |
| `make -C tb/verilator/avtp_rxmon` (clean clone) | rc 0: flat 97, N=4 stack 121, lockstep 116 (N=1) / 119 (N=8), mutants 14/14 | `r2b-focused/c2-avtp_rxmon.log` |
| `make -C tb/verilator/crf_rx` (clean clone) | rc 0: 15,202 + 2,201 + 69 checks, mutants 18/18 | `r2b-focused/c2-crf_rx.log` |
| `make -C tb/verilator/milan_dp` (clean clone) | rc 0, every shape 0 failures (root `[UNB]` U3: STREAM_INTERRUPTED 0). A first start beside the route was stopped by hand to keep the unit's memory down (the unit reached its cap reclaiming page cache, no OOM kill) and re-run after the route | `r2b-focused/c2-milan_dp.log.tail`, `c2-milan_dp-stopped-for-memory.log` |
| `make -C tb/verilator/milan_dp_gm_steps gmstep-mutants` (clean clone) | 22/22 (gmstep 190 checks, 0 failures) | `r2b-gmstep/` |
| `syn/yosys/run.sh` (full serial) | rc 0, 58/58 tops, tied-input and tap-purity gates PASS | `r2b-final/yosys.log` |
| `scripts/xvlog_gate.py --check` (exclusive lock; it queued behind another lane's build) | rc 0, 0 findings == ratchet | `r2b-final/xvlog.log` |
| `sw/builder/test_builder.py --require-rv32` | rc 0, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, the calibration that needs a local mf48 build tree) | `r2b-final/builder.log` |
| every other docs-workflow gate command (82, the same list as round 2: HDL reference build with the pinned `pyslang`, wavedrom with the pinned `wavedrom`, lint ratchet, em-dash vs `e9cbb676`, C++/Python/SV/shell idiom, ...) | 80 rc 0; the same two host-only self-tests fail: `act_ci.py --selftest` (the same 31 failure lines as round 2; the file is unchanged since the base) and `check_todo_ownership.py --selftest`'s git-absent case (this host's CPython 3.12.3 build cannot start with a stripped environment; 45/45 under the host Python 3.14.8; unchanged since the base) | `r2b-static/gates.tsv`, `console.txt` |
| `syn/ooc/pp_resource_gate.py check --endpoint route-1x1` | **rc 0**; WNS +0.189, WHS +0.014, fully routed | `r2b-route/` |

Not run: the hosted `docs-gates-*`, `docs-check` and the act replica, because the head is not pushed (pushing is outside
this lane). Physical calibration NOT RUN; no hardware. The sweep clone `swA` shows the `tsn_fuzz` campaign's rewritten
`TEST_RESULTS.md` timestamps, as round 2's did; the lane tree is clean.

## Open questions (round 2b)

- A followed AAF stream's return still raises no restart; the extended ruling keeps it as is.
- A gap's stopped state is read at its accept verdict (AAF) or accept edge (CRF): a STOP landing between a gap PDU's
  arrival and its verdict, a few cycles, already suppresses that gap. Both sweeps grade this boundary.
- R663-1-S1 is still not taken (unchanged from round 2).

## Receipts (round 2b)

`receipts/INDEX.md` is regenerated from the files present. Round 2b's folders are the `r2b-*` ones.

# Round 3 (assignment: the newest [A10] comment on PR #767, 6274405031; review: R663-2, 6274385352)

Status: REVIEW READY -- head `d30a208d44d5868cc356e6a8b7abc89b062ca9bd` (tree `d203767a`), three commits on the pushed
PR head `eef90b42`, no rebase, no amend. The new commits are on the lane branch for the manager to push; PR #767 is not
edited. R664-2 is POSITIVE (6274077431); R663-2 was NEGATIVE on one MINOR (F1, Tests) and two residues (F2, F3).
R663-2-S1 is not assigned and not taken. Round 3 REVIEW READY posted on #761: issuecomment-6275750885 (text in
`REVIEW-READY-R3-COMMENT.md`).

| Commit | Finding | Change |
|---|---|---|
| `cb65d9d7` | R663-2-F2 | the two port comments, word for word as the review wrote them |
| `336a6f6a` | R663-2-F1 | `[762-DP]` in `sim_nxn.cpp`: the integrated case |
| `d30a208d` | R663-2-F1 (Docs) | the milan_dp README paragraph for `[762-DP]` |

## Changes, with clause

| Where | Change | Clause |
|---|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:152` | comment: "input has no playback, so neither its silence nor its sequence gap is an interruption (#762)" | Milan v1.2 5.3.8.7 |
| `hdl/milan/milan_datapath.sv:6307` | comment: "#762: a stopped input's silence or sequence gap interrupts no playback (5.3.8.7)" | Milan v1.2 5.3.8.7 |
| `tb/verilator/milan_dp/sim_nxn.cpp:6653-6729` (`prove_a_stopped_stream_input_counts_no_interruption`, called at `:6438` right after the 5.3.8.7 discard section) | the integrated case. On AAF Stream Input 0 it uses STOP_STREAMING / START_STREAMING over the wire as AECP and reads every count with `GET_COUNTERS(STREAM_INPUT, 0)`: (1) started, locked and settled baseline; (2) STOP, then a gap of two lost PDUs; (3) still stopped, the 100 ms silence expires; (4) START, relock past the 8-PDU settle window, then the same gap | Milan v1.2 5.3.8.7, 5.4.2.19, 5.4.2.20, 5.3.8.10 Table 5.6; rulings 6260976223 / 6265746720 |
| `tb/verilator/milan_dp/README.md:1188` | what `[762-DP]` grades, how the silence is shortened, and which wiring mutant breaks which step | -- |

No RTL logic change: the two RTL edits are comments only, so route-1x1 was not re-run (per the assignment). No port,
parameter, CSR or register-map field is touched.

The silence in step 3 is the monitor's own 1 ms-tick watchdog (`sil_ms_r`). Run whole, it would be 10,000,000 cycles
on every broad leg. The harness writes the stream-0 watchdog through the engine's hierarchy to 97 of its 100 ticks,
then runs 4 ms for real: the expiry, the unlock walk and every count after it are the engine's. This is the
`[CTRS-CRF]` precedent (`tout_r`). A guard check requires the watchdog to be below 97 before the write, so the write
can only shorten the silence.

The case runs on every broad `sim_nxn` leg: `obj_nxn` (arty 4x4 entity), `obj_nxndv`, `obj_nxn8` (8x8) and
`obj_nxn4c` (the shipping Arty shape, 4 streams x 4 wire channels).

## New checks and their planted mutants

Each check below is in `sim_nxn.cpp`.

| Check | Expected | Mutant at `milan_datapath.sv:6308` that fails it |
|---|---|---|
| `[762-DP] 2 stopped gap: SEQ_NUM_MISMATCH +1 (the gap was seen)` (`:6693`) | +1 (live) | -- (liveness) |
| `[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0` (`:6695`) | +0 | `tie0`: `.stopped_i ('0)`; `sink1`: `.stopped_i (acmpl_stopped_v_w[N_STREAMS:1])` |
| `[762-DP] 3 the stopped input's silence unlocked it` (`:6710`), `3 stopped silence: MEDIA_UNLOCKED +1` (`:6713`) | 0 / +1 (live) | -- (liveness) |
| `[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0` (`:6715`) | +0 | `tie0`, `sink1` |
| `[762-DP] 4 started again: MEDIA_LOCKED +1`, `4 started gap: SEQ_NUM_MISMATCH +1` (`:6723`, `:6725`) | +1 / +1 (live) | -- |
| `[762-DP] 4 started gap: STREAM_INTERRUPTED +1` (`:6727`) | +1 | `bound`: `.stopped_i (acmpl_bound_v_w[N_STREAMS-1:0])` |

The mutant run (`receipts/r3-mutants/`, driver `dp_stopped_mutants.sh`) used a clean clone at `336a6f6a`, which is
the head minus the README-only commit. It plants each form in `milan_datapath.sv`, rebuilds `obj_nxn4c` through the
Makefile's own `build-nxn4c` recipe, runs it from the leg directory, and restores the file. It then rebuilds and runs
the clean leg.

| Leg | rc | Failing checks (all of them) |
|---|---|---|
| `tie0` | 1 | `2 stopped gap: STREAM_INTERRUPTED +0` (got 1), `3 stopped silence: STREAM_INTERRUPTED +0` (got 1) |
| `sink1` (stream 0 reads sink 1's level) | 1 | the same two |
| `bound` (the bound level for the stopped level) | 1 | `4 started gap: STREAM_INTERRUPTED +1` (got 0) |
| clean control | 0 | none: 1,981 checks, 0 failures |

No other check in the leg moves under any mutant, so each catch is attributable to the planted wiring. The run is a
lane campaign with published receipts, not a new in-tree driver. Adding one would register a new campaign (Makefile
target, README, `TESTING.md`, the test-evidence reader inventory); the assignment asked for the plant and the named
failure.

A first attempt of the driver ran each leg from outside its directory, so `$readmem` could not find `ucode.hex`, and
every leg, the clean one included, failed and crashed. The driver was corrected to run from the leg directory and
re-run whole. Only the corrected run is published.

## Gate table (head `d30a208d`, clean clone, CI's CPython 3.12.3 build, Verilator 5.050)

| Gate | Result | Receipts |
|---|---|---|
| `make -C tb/verilator/milan_dp` (every leg, the ones that build the change) | **rc 0**, 0 `[FAIL]` lines. Per-leg checks: notify 423, crflic 416, dynmap 162, `obj_nxn` 1,981, `obj_nxndv` 1,983, `obj_nxn8` 3,765, `obj_nxn4c` 1,981, prune 33, all 0 failures; base, nolpf, ax1x1, aclk, the counter legs and render-mutants PASS. Each of the four `sim_nxn` broad legs is +13 (the `[762-DP]` checks) over the last full logs (1,968 / 1,970 / 3,752 / 1,968; `sim_nxn.cpp` was unchanged from `4191b098` to `eef90b42`); 52 `[762-DP]` `[ok]` lines, 13 per leg | `r3-focused/c3-milan_dp.*` |
| `make -C tb/verilator/avtp_rxmon` (the comment-touched engine) | **rc 0**: flat 97, N=4 stack 121, lockstep 116 (N=1) / 119 (N=8), 0 failures; `lockstep_mutants.py` 14/14 | `r3-focused/c3-avtp_rxmon.*` |
| `[762-DP]` wiring mutants on `obj_nxn4c` | 3/3 caught by the named checks; clean control 1,981 / 0 | `r3-mutants/` |
| docs gate_50, all fourteen commands | **rc 0 x14** (`shard 0/35 refused`, 34 driver cases) | `r3-gate50/` |
| every other docs-workflow gate (82 commands, the same list as rounds 2 and 2b) | 80 rc 0. The same two host-only self-tests fail, on files unchanged since the base. `act_ci.py --selftest`: the same 31 failure lines as round 2b (an identical sorted multiset). The git-absent case of `check_todo_ownership.py --selftest`: this host's CPython 3.12.3 build cannot start with a stripped environment, and the host Python 3.14.8 gives 45/45, rc 0. Hosted `docs-gates-*` and `docs-check` succeeded at `eef90b42` | `r3-static/` |
| `sw/builder/test_builder.py --require-rv32` (the builder bank) | **rc 0**, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, the calibration that needs a local mf48 build tree) | `r3-final/builder.*` |
| route-1x1 | not re-run: no RTL logic changed (the RTL edits are comments) | -- |

Hosted CI at the pushed PR head `eef90b42`: every check run completed `success`, except the nightly physical gPTP
job (`skipped`). That includes `rtl-fast`, `verilator-suites` (16 shards), `yosys-portability` (4 shards),
`docs-check`, `docs-gates-0/1/2`, `verilator-lint` and `yosys-elaboration` (`r3-hosted/checks_eef90b42.tsv`, snapshot
2026-10-19T18:54:54Z). The round-3 commits get hosted runs and the act replica once they are pushed. This lane does not
push, so neither was run on them. No hardware; physical calibration NOT RUN.

## Open questions (round 3)

- R663-2-S1 (CRF STOP trials one edge around the timeout) is not assigned and not taken.
- R663-1-S1 is still not taken (unchanged).
- A followed AAF stream's return still raises no restart; the ruling keeps it as is.

## Receipts (round 3)

`receipts/INDEX.md` is regenerated from the files present. Round 3's folders are the `r3-*` ones.

# Round 4 (head `d30a208d` -> `f3fef856`, two new commits, no rebase, no amend)

Assignment: PR #767 comment 6283915359, answering R663-3 (6283905996) and R664-3 (6275950683), which retain the same
item (R663-3-F1 / R664-3-F1, MINOR, filed by both under Conformance, Robustness, Tests and Docs). Status: DONE; REVIEW
READY posted on #761: issuecomment-6285115002 (text in `REVIEW-READY-R4-COMMENT.md`).

| Item | Finding | Status |
|---|---|---|
| 1 | R663-3-F1 / R664-3-F1: `[762-DP]` on the shipping AX7101 shape, elaborated parameters logged against the entity definition, the tie-off and the `[N_STREAMS:1]` mutant (the CRF sink at N=1) each failing a named `[762-DP]` check there, existing legs kept | met: commits `16358b62`, `f3fef856`; receipts `r4-focused/`, `r4-shape/`, `r4-mutants/` |
| 2 | wording: PR body and mutant script header name every shape accurately (`obj_nxn4c` is the retired Arty 4x4) | met: PR-BODY.md Round 3 rows; `r3-mutants/dp_stopped_mutants.sh` header (`r4-wording/`); the round-4 driver header |
| 3 | R663-3-R1: PR status lines cite the hosted run at `d30a208d`, `Physical gPTP` recorded as skipped | met: PR-BODY.md Status and Known limitations, R663-3-R1's exact text; `r4-hosted/` |

| Commit | Change |
|---|---|
| `16358b62` | `[762-DP]` at the end of the `obj_dynmap` leg, which elaborates `endstation_ax7101_1x1_tdm8` with the `obj_ax1x1` argv; the leg prints its elaborated parameters, read back through `dynmap_probes.vlt` |
| `f3fef856` | the milan_dp README: the `obj_dynmap` row, its section intro and the `[762-DP]` paragraph |

## Why the dynmap leg, and not a new one

The four broad legs run `[762-DP]` inside the broad flow, and the two `sim_nxn` legs on the AX 1x1 shape (`notify`,
`dynmap`) return before it (`sim_nxn.cpp:3031-3060`). `obj_ax1x1` runs `sim_main.cpp`. The notify recipe elaborates the
AX 1x1 entity but keeps the datapath's default geometry (2 wire channels, no TDM). `DYNMAP_BUILD` is the `obj_ax1x1`
argv (`Makefile:325-331`): 8 wire channels, TDM8 master, loopback, I2S playback and LPF pruned. So the case runs at the
dynmap leg's end. A new leg would add a binary and a build argv to the reviewed CI command table
(`ci/image/command-table.json`, which records each leg's full argv). The dynmap argv is unchanged, so the table is
untouched. The leg's last arm (`dynmap_edit_meets_the_sweep`) already ends on a reset and a COMPLETE restore walk. The
new function boots again so the case does not depend on it.

## Changes, with clause

| Where | Change | Clause |
|---|---|---|
| `tb/verilator/milan_dp/sim_nxn.cpp:4564-4621` (`stopped_input_law_on_the_shipping_geometry`, in the `DYNMAP_DEFAULT_TB`-only block) | prints the elaborated parameters, then checks one AAF input and the CRF sink at `N_STREAMS` (`:4603`, `:4605`), boots afresh (reset, entity id, restore walk), then runs the TRAP-1 bind and its bound-alias grade, the 5.3.8.7 discard section and `[762-DP]`, unchanged | Milan v1.2 5.3.8.7, 5.4.2.19, 5.4.2.20, 5.3.8.10 Table 5.6; #762 rulings 6260976223 / 6265746720 |
| `tb/verilator/milan_dp/sim_nxn.cpp:3036` | the dynmap leg calls it after `[DYNMAP]`, before its tally | -- |
| `tb/verilator/milan_dp/dynmap_probes.vlt:24-41` | `public_flat_rd` on the datapath's stream, audio and prune parameters and the generated `ADP_*_C` / `CRF_SNK_IDX_C`, so Verilator emits them as constants; no logic effect | -- |
| `tb/verilator/milan_dp/README.md:82,778-780,1189-1209` | the `obj_dynmap` row and section intro; the `[762-DP]` paragraph names the dynmap leg, its fresh boot, the logged parameters, the CRF sink at sink 1 and the `obj_ax1x1` substitutes | -- |

No RTL change, so no resource or route figure changes (route-1x1 last ran at `eef90b42`). No port, parameter, CSR,
register-map field, Makefile recipe or CI table is touched. Every other leg is unchanged: the new function compiles
only with `DYNMAP_DEFAULT_TB`, and `dynmap_probes.vlt` is used only by `DYNMAP_BUILD`.

## The elaboration, against the entity definition

`r4-shape/dynmap-elaborated-vs-shipping.md` (`shape_params.py`) compares the three logged parameter lines with the
shipping values. These come from the config's generated design argv (`configs/generated/sweep_opts_ax7101.sh` OPTS),
mapped as `sw/litex/milan_soc.py` `add_milan_datapath` maps them (`:952-1120`, `:4160-4190`), and from the config's
generated `adp_shape_defaults.svh`. 19 of 22 are the same: `N_STREAMS` 1, `ADP_TALKER_SRC_C` 2, `ADP_LISTENER_SINK_C` 2,
`CRF_SNK_IDX_C` 1, `TALKER_WIRE_CHANS_P` 8, `AUDIO_IF_SLOTS_P` 8, `AUDIO_IF_MASTER_P` 1, `AUDIO_IF_CLK_HZ_P`
24,576,000, `LOOPBACK_P` 1, `I2SPB_P` 0, `LPF_P` 0, and the other prunes 1. Three differ, and each is a documented
substitute every `obj_ax1x1`-geometry leg shares:

| Parameter | Leg | Shipping | Substitute |
|---|---:|---:|---|
| `MILAN_CLK_FREQ_HZ` | 100,000,000 | 50,000,000 | the verification fabric clock; `[762-DP]`'s 1 ms step assumes it |
| `GPTP_PLANE_EN_P` | 0 | 1 | gPTP option OFF (`GPTP_OFF_VFLAGS`); the plane is graded on `obj_gptp` / `obj_ax1x1gptp` |
| `AUDIO_IF_RENDER_SLOTS_P` | 0 | 8 | the render lane is pruned in the `obj_ax1x1` argv; the shipping TDM8 render lane is `tb/verilator/milan_dp_render` |

None of the three is on the `stopped_i` path. The geometry the finding names is the same: at `N_STREAMS` 1 the CRF
Media Clock Input is sink 1, so `[N_STREAMS:1]` feeds input 0 the CRF sink's level. The mutant runs log byte-identical
parameter lines (`r4-shape/same-elaboration.txt`), so they ran on that elaboration.

## New checks and their planted mutants (the `obj_dynmap` leg)

| Check | Expected | Mutant at `milan_datapath.sv:6308` that fails it |
|---|---|---|
| `[762-DP] AX 1x1: one AAF Stream Input (N_STREAMS 1)` (`sim_nxn.cpp:4603`) | 1 | -- (geometry) |
| `[762-DP] AX 1x1: the CRF Media Clock Input is sink N_STREAMS, the entity's last` (`:4605`) | 1 | -- (geometry) |
| the 13 `[762-DP]` case checks (`:6735-6789`), as in round 3 | as in round 3 | below |
| `[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0` (`:6755`) | +0 | `tie0` (`.stopped_i ('0)`), `sink1` (`acmpl_stopped_v_w[N_STREAMS:1]`: the CRF sink's level here) |
| `[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0` (`:6775`) | +0 | `tie0`, `sink1` |
| `[762-DP] 4 started gap: STREAM_INTERRUPTED +1` (`:6787`) | +1 | `bound` (`acmpl_bound_v_w[N_STREAMS-1:0]`) |

`r4-mutants/dynmap_762dp_mutants.sh` runs on a clean clone of `f3fef856`. Each mutant is a copy of
`milan_datapath.sv` with the one line replaced. It is built through the Makefile's own `dynmap-build` recipe, with
`DP_SRC` and `DYNMAP_MDIR` overridden (the `dynmap_mutants.py` route), so no tracked file is edited. Each binary runs
from the leg directory. The driver passes only if every build succeeds and each mutant fails exactly its expected set
and nothing else:

| Run | build rc | run rc | Checks | Failing checks (all of them) |
|---|---:|---:|---:|---|
| `tie0` | 0 | 1 | 199 | `2 stopped gap: STREAM_INTERRUPTED +0` (got 1), `3 stopped silence: STREAM_INTERRUPTED +0` (got 1) |
| `sink1` | 0 | 1 | 199 | the same two |
| `bound` | 0 | 1 | 199 | `4 started gap: STREAM_INTERRUPTED +1` (got 0) |
| clean | 0 | 0 | 199 | none |

The first run of the driver also passed, all four exact. It is superseded: its redaction patterns carried two host-path
literals, so the patterns were moved to the environment and the campaign was re-run whole. Only the re-run is
published.

## Wording (item 2) and status lines (item 3)

- PR-BODY.md Round 3 now names each broad leg's entity: `obj_nxn`, `obj_nxndv` and `obj_nxn4c` on the retired Arty 4x4,
  `obj_nxn8` on the AX7101 8x8 at the default geometry. Its mutant line names `build-nxn4c` as the retired Arty 4x4.
- `receipts/r3-mutants/dp_stopped_mutants.sh`: header comment corrected, no executable line changed. Published round-3
  sha256 `b2d85578...`, now `551242c2...` (`r4-wording/r3-mutant-header.diff`, `.sha256.txt`). The round-4 driver's
  header names the AX7101 1x1 TDM8 geometry and its substitutes.
- Status and Known limitations take R663-3-R1's exact text. `r4-hosted/checks_d30a208d.tsv`: 64 check runs at `d30a208d`,
  63 `success`, `Physical gPTP (nightly and manual)` `skipped`.
- Not changed (pre-existing tree text, outside this lane's scope): the `obj_nxn4c` README row, the `build-nxn4c` comment
  and the `CASE_OPTIONS_nxn4c` banner still say "shipping Arty". The banner is part of the reviewed CI command table.
  BUILDING.md calls the Arty retired. Recorded as an open question.

## Gate table (head `f3fef856`, clean clones, CI's CPython 3.12.3 build, Verilator 5.050)

| Gate | Result | Receipts |
|---|---|---|
| `make -C tb/verilator/milan_dp` (every leg) | **rc 0**, 0 `[FAIL]` lines. notify 423, crflic 416, **dynmap 199** (162 + 37: 2 geometry, 1 boot, 6 TRAP-1, 15 5.3.8.7, 13 `[762-DP]`), `obj_nxn` 1,981, `obj_nxndv` 1,983, `obj_nxn8` 3,765, `obj_nxn4c` 1,981, prune 33, all 0 failures; base, nolpf, ax1x1, aclk, the counter legs and render-mutants PASS. 67 `[762-DP]` `[ok]` lines (13 x 4 broad legs + 15 on dynmap) | `r4-focused/` |
| `[762-DP]` wiring mutants on `obj_dynmap` | 3/3 fail exactly their named checks; clean control 199 / 0 | `r4-mutants/` |
| `make -C tb/verilator/milan_dp dynmap-mutants` (the leg's own 13 planted controls; the leg changed) | **rc 0**, 16/16: the three clean controls (dynmap, the render suite's listener leg, capture_coherence's talker leg) pass and all 13 planted controls are caught by their named checks. A first run in the fresh clone failed the listener clean control: the campaign builds that leg with `-o tdm8r_aemi.bin`, so it never generates the render suite's AEM image, and no render build had run in that clone. The inputs were generated with the render and coherence suites' own targets and the campaign re-run whole; both runs are kept | `r4-dynmap-mutants/` |
| elaborated parameters vs the entity definition | 19 same, 3 documented substitutes, 0 unexplained | `r4-shape/` |
| docs gate_50, all fourteen commands | **rc 0 x14** (`shard 0/35 refused`, 34 driver cases) | `r4-gate50/` |
| every other docs-workflow gate (82 commands, the same list as rounds 2-3) | 80 rc 0. The same two host-only self-tests fail, on files unchanged since the base. `act_ci.py --selftest`: the same 31 failure lines as round 3, an identical sorted multiset. `check_todo_ownership.py --selftest`: only its git-absent case fails, because this host's CPython 3.12.3 build cannot start with a stripped environment; the host Python 3.14.8 gives 45/45, rc 0 | `r4-static/` |
| `sw/builder/test_builder.py --require-rv32` | **rc 0**, "ALL GATES PASS EXCEPT 1 NOT RUN" (gate 11, which needs a local mf48 build tree) | `r4-final/` |
| avtp_rxmon, crf_rx, the 63-suite sweep, Yosys, route-1x1 | not re-run: no RTL, engine or harness of theirs changed since `d30a208d` (the round-3 receipts stand) | `r3-*`, `r2b-*` |

Hosted CI at `d30a208d`: 63 check runs `success`, the nightly physical gPTP job `skipped` (`r4-hosted/`). The round-4
commits are not pushed by this lane, so neither hosted CI nor the act replica ran on them. No hardware; physical
calibration NOT RUN.

## Open questions (round 4)

- Pre-existing "shipping Arty" text in the tree (README `obj_nxn4c` row, `build-nxn4c` comment, the `CASE_OPTIONS_nxn4c`
  banner in the CI command table) contradicts BUILDING.md. Candidate for its own Issue; not changed here.
- `AX1X1_BUILD`'s comment says "byte for byte the cfg_ax7101 argv", but the shipping argv now carries
  `--audio-interface-render 8` and the leg prunes the render lane. That lane is graded in `milan_dp_render`. Candidate
  for its own Issue.
- `dynmap_mutants.py` builds its listener leg with `-o tdm8r_aemi.bin` (and the hex files), so in a clone where the
  render suite never ran, its clean listener control fails for a missing image. Pre-existing; candidate for its own
  Issue (the campaign could make the inputs or refuse by name).
- R663-3-S1 (grade a non-zero bit of `stopped_i` on an N >= 2 leg) is optional and not assigned; not taken. It cannot
  arise on the N=1 shipping shape.
- R663-2-S1, R663-1-S1 and R664-2-S2 are still not taken (unchanged).

## Receipts (round 4)

`receipts/INDEX.md` is regenerated from the files present. Round 4's folders are the `r4-*` ones.

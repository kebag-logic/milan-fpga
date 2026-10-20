[A652]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Round 2](#round-2)** -- Answers to R664-1 and R663-1 and the #762 scope ruling.
- **[Round 2b](#round-2b)** -- The ruling extended to a sequence gap on a stopped input.
- **[Round 3](#round-3)** -- The datapath grade of the AAF `stopped_i` wiring, two comments and these status lines.
- **[Round 4](#round-4)** -- `[762-DP]` on the shipping AX7101 1x1 TDM8 geometry, with its wiring mutants there.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN -- `761-762-mr-interrupt` -> `dev`, eleven commits on dev `e9cbb676`.

- Hosted CI: every check run at `d30a208d` succeeded, with the nightly physical gPTP job skipped. That includes
  `rtl-fast`, `verilator-suites`, `yosys-portability`, `docs-check`, `docs-gates-0/1/2`, `verilator-lint` and
  `yosys-elaboration`.
- Round 3 added three commits on `eef90b42`, ending at `d30a208d44d5868cc356e6a8b7abc89b062ca9bd`: two comments, one
  integrated test and its README paragraph.
- Round 4 adds two commits on `d30a208d`, ending at `f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d`: `[762-DP]` on the
  shipping AX7101 1x1 TDM8 dynmap leg, and its README text. No RTL change. Their hosted evidence is this PR's Checks
  tab at that commit.
- Local at `f3fef856`: milan_dp all legs 0 failures (`obj_dynmap` 199 checks, 15 of them `[762-DP]`); the three
  wiring mutants on `obj_dynmap` each fail exactly their named checks; `make dynmap-mutants` 16/16; docs
  gate_50 14/14; the other 82 docs-workflow commands 80 rc 0 (the same two host-only self-tests); builder bank pass
  (one arm NOT RUN, gate 11).
- Local at `d30a208d`: milan_dp all legs 0 failures; avtp_rxmon rc 0; docs gate_50 14/14; builder bank pass (one arm
  NOT RUN, gate 11).
- Local at `eef90b42`: 63/63 suites, 2,188,354 checks, 0 failures; Yosys 58/58; xvlog 0 findings; route-1x1 gate
  pass (WNS +0.189 ns, LUT -16 against the record). No RTL logic changed after it.

## Linked Issue / roles

Closes #761, closes #762

Executor: `[A652]`
Internal cleared-context reviewer: `[R663]`
External reviewer: `[R664]`

## Description

Two defects in the AVTP receive and media-clock path, one commit each, then a second round answering R664-1 and
R663-1 and the #762 scope ruling (see [Round 2](#round-2) below), then round 2b for the ruling's extension to
sequence gaps (see [Round 2b](#round-2b)), then round 3, which grades the AAF half of that rule through the
datapath wiring (see [Round 3](#round-3)), then round 4, which runs that grade on the shipping AX7101 1x1 TDM8
geometry (see [Round 4](#round-4)).

**#761 (`f443ed9b`): mr toggles when the media clock returns to the CRF.** The restart request took only the
falling edge of the selected CRF sink's lock, so the AAF and CRF outputs toggled `mr` when the CRF stopped and stayed
silent when it came back. The return moves the media clock from holdover back onto the CRF, a change of its source,
so it needs its own restart.

| Piece | Change |
|---|---|
| `hdl/milan/milan_datapath.sv` `mcr_restart_p_w` | the CRF term is `tkd_crflk_q_r ^ crf_locked_w` (either lock edge), still gated by `crf_clk_selected_r`; the received-`mr` echo and the AAF-meter terms are unchanged |
| `tb/verilator/milan_dp_mclk` | the CRF loss/return row now requires one request and one `mr` toggle per output on the return; new `--crfloss` short leg; mutants 17 (gain edge dropped) and 18 (loss edge dropped) |
| text pins of the expression | `sw/builder/test_builder.py`, `gmstep_mutants.py` anchors, `BAREMETAL_FIRMWARE.md` row |
| docs | `MEDIA_CLOCK_FOLLOWING.md` test plan and `mr` section, `GM_LOSS_RECOVERY.md`, compliance matrix 4.4.4.3, `TESTING.md`, mclk README |

**#762 (`4191b098`): STREAM_INTERRUPTED counts a silence.** A 100 ms silence unlocked a bound input (MEDIA_UNLOCKED
+1) and the first PDU after it re-seeded the sequence, so the interruption was never counted. Both receive engines now
count it once at the unlock; an unbind never counts.

| Piece | Change |
|---|---|
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv` (AAF inputs) | per-stream `sil_si_r` marks a pending unlock as the watchdog's; the unlock walk then queues STREAM_INTERRUPTED through the ordinary yielding RMW; the bind decode clears it with the era. (Round 2: the mark is set at the expiry only for a bound, started stream, and a later Unbind no longer clears it) |
| `hdl/ieee1722/crf/KL_crf_rx.sv` (CRF input) | the 100 ms timeout of a locked sink counts `cnt_intr_o` when bound (`en_i`) and started (`!stop_i`) |
| `tb/verilator/avtp_rxmon` | lockstep `[SI]`: silence, resume, gap, unbind; three mutants (silence, gap, unbind). The frozen M6 reference gains the same lines so the cycle comparison stays exact; #762 is graded by count, not against it. `[H3]` reads its SI wrap before an interval wait that outlasts the silence timeout. N=4 stack `[G6-762]`. (Round 2 replaces the unbind sweep with the boundary sweep and adds the stop cases) |
| `tb/verilator/crf_rx` | replica model counts the silence; `[762-a]`/`[762-b]`, `[UNB-d0b]`, `[UNB-d5]` (unbind on the timeout edge); four mutants through a new `unit-build` target |
| `tb/verilator/milan_dp` `[CTRS-CRF]` | the root event arm grades the silence's STREAM_INTERRUPTED; the plan keeps ten distinct counts |
| docs | `REGISTER_MAP.md` CRF counter paragraph, compliance matrix 5.4.2.25, `TESTING.md` |

No register map, top-level port or parameter changes.

## Authoritative references

- IEEE 1722-2016 4.4.4.3: `mr` toggles each time a media clock restart is needed, for a change in the source of the
  media clock, and for a CRF stream's disruption; 10.4.3 for the CRF talker.
- Milan v1.2 5.3.8.10 Table 5.6: STREAM_INTERRUPTED counts each interruption of playback for any reason other than a
  Controller Unbind; 5.4.2.25 Table 5.16: served for each Stream Input.
- Milan v1.2 5.3.8.7 (a stopped Stream Input discards its AVTPDUs), 5.4.2.19 / 5.4.2.20 (START_STREAMING /
  STOP_STREAMING change the started state), and the
  [#762 scope ruling](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6260976223): a silence on a
  stopped input counts nothing, in both receive engines; its
  [extension](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6265746720): a sequence gap on a
  stopped input counts nothing either, a started input's gap counts once, and after START a gap counts again.
- Issues #761 and #762; the assignment is comment 6256482625 on #761; the round-2 assignment is comment 6260976498 on
  #767; round 2b follows the extended ruling, comment 6265746720 on #762.

## How to get into the same state

```sh
git fetch origin 761-762-mr-interrupt
git checkout f3fef856dbf7f8e559fa9066f6fc9af1ea091c9d
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
```

Verilator 5.050, sv2v 0.0.12, CPython 3.12.3 with `pyyaml` and `tools/markdown/requirements.txt`, tsn-gen
`deca300c` at `TSN_GEN_ROOT`.

## How to validate

```sh
make -C tb/verilator/milan_dp_mclk
make -C tb/verilator/avtp_rxmon
make -C tb/verilator/crf_rx
make -C tb/verilator/milan_dp
make -C tb/verilator/milan_dp_render ltn_rom.hex ucode.hex tdm8r_aemi.bin
make -C tb/verilator/capture_coherence ltn_rom.hex ucode.hex
make -C tb/verilator/milan_dp dynmap-mutants
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_case_receipts_selftest.py
make -C tb/verilator/milan_dp_gm_steps gmstep-mutants
python3 scripts/lint_rtl.py --check
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
syn/yosys/run.sh
python3 sw/builder/test_builder.py --require-rv32
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1
```

Expected result / pass criteria: every command exits 0. The mclk campaign prints `34 checks: 34 PASS` with mutants
17 and 18 caught; avtp_rxmon's lockstep prints 116 checks at N=1 and 119 at N=8 with 0 failures and
`lockstep_mutants.py` 14/14; crf_rx's counter harness 15,202 checks and its mutants 18/18; milan_dp's four broad
`sim_nxn` legs each print 13 `[762-DP]` `[ok]` lines (`obj_nxn4c` 1,981 checks, 0 failures), and `obj_dynmap` prints
15 (199 checks, 0 failures) after its elaborated parameters; `dynmap-mutants` prints `16 checks: 16 PASS`; the receipt selftest
reports `shard 0/35 refused` over `34 driver cases`; the gm-step campaign 22/22. The rest of docs gate_50 is the
fourteen commands of `.github/workflows/docs.yml` step `gate_50`. The route follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.

## Known limitations / out of scope

- A followed AAF stream's return still raises no restart. The issue, the assignment and the 4.4.4.3 shall name the
  CRF only; `MEDIA_CLOCK_FOLLOWING.md` now says so explicitly.
- The flat `KL_avtp_rx_monitor` test instrument keeps the old law; the context engine's banner records the delta.
- The silence walk marks the descriptor dirty at its MEDIA_UNLOCKED write and STREAM_INTERRUPTED lands a few cycles
  later, the ordering the PDU walk already uses for MEDIA_LOCKED and the gap's STREAM_INTERRUPTED.
- `scripts/act_ci.py --selftest` (docs gate_42) fails 16 process-group containment probes in this host's sandbox; the
  file is unchanged by this branch, and an unchanged copy fails the same 16 identically. Hosted CI is the evidence for
  that gate: it succeeded at `d30a208d` (see [Status](#status)).
- A gap's stopped state is read at its PDU's accept verdict (AAF) or on its accept edge (CRF), so a STOP landing in the
  few cycles between a gap PDU's arrival and its verdict already suppresses that gap's count. Both sweeps grade this
  boundary exactly.

## Round 2

Round 2 answers R664-1 (`NEGATIVE`, 2 MAJOR) and R663-1 (`NEGATIVE`, 1 BLOCKER, 2 MINOR) at `4191b098`, under the
round-2 assignment (#767 comment 6260976498) and the
[#762 scope ruling](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6260976223). Three commits:

| Commit | Finding | Change |
|---|---|---|
| `ba9ac06a` | R663-1-F1 (BLOCKER): gate_50's `ci_case_receipts_selftest.py` refused `0/32`, which the mclk driver's 34 cases made legal | the refused over-shard count is derived from the driver's real inventory, `len(names) + 1` (`0/35` now), one past the largest legal split, which the same file still accepts |
| `492207f7` | R664-1-F1 (MAJOR): an Unbind between the silence's MEDIA_UNLOCKED write and the walk's phase 3 erased the interruption | `KL_avtp_rx_monitor_ctx` no longer clears the silence mark on `bind_fall_i`. The watchdog's expiry is the one event boundary for the unlock and the interruption: an Unbind or STOP after it leaves exactly one interruption; one on or before it leaves none; an Unbind's own unlock still adds nothing |
| `492207f7` | R664-1-F2 / R663-1-F2: the stopped input | the ruling in both engines. `KL_avtp_rx_monitor_ctx` gains `stopped_i[N]` (from `acmpl_stopped_v_w`, the vector the accept gate and `KL_aaf_clock_meter` use) and marks a silence only on a started input; `KL_crf_rx` already gated its timeout count on `!stop_i` (comment only). `REGISTER_MAP.md`, the compliance matrix and `TESTING.md` state the rule with 5.3.8.7, 5.4.2.19, 5.4.2.20 and Table 5.6 |
| `492207f7` | R663-1-F3 (MINOR): the unbind law was graded only against the mirrored reference | `[SI]` now grades every #762 rule by count with its own oracle: the harness owns the reset, the 1 ms grid and the observed last accept, so it knows the expiry edge, and sweeps an Unbind and a STOP over every cycle from -12 to +24 of it (plus far points) on an idle engine and on one held or yielding to PDU traffic, at N=1 and N=8. Every #762 mutant is planted in the engine and the reference alike, so only the count oracle can catch it |
| `2cd2750d` | -- | the boundary trial moves into its own function (the C++ 100-line rule) |

New mutants, each caught by its named count check: `consume race` (the Unbind clear reinstated, both copies), `stopped`
(the stop term dropped), `stop at the walk` (the stopped state read at phase 3); CRF `stopped_silence_interrupts`
(`[762-ST-b2]`). R664-1's own `probe_silence_order.py` now passes at every delay 0..8 at both shapes (its call anchor moved
to the new case list); its `probe_stopped_silence.cpp` reads started 1/1 and stopped 1/0, which is the ruling (its
frozen-acceptance oracle exits 1 by design; the ruling-graded copy exits 0).

Not changed: R663-1's S1 (an ungated-edge dynamic row for the mclk suite) stays a suggestion; the builder's exact-initializer
pin still refuses that edit.

Validation at `2cd2750d`, in clean clones:

| Gate | Result |
|---|---|
| docs gate_50 (fourteen commands) | rc 0 x14, at `ba9ac06a` and at the head |
| 63-suite sweep, five shards | 63/63, 2,188,042 checks, 0 failures, 0 timeouts (shard 3 re-run after an unchanged suite's process-lifecycle control failed under host load; the first launch was refused by the runner's own SIGHUP preflight control because it ran under `nohup`) |
| avtp_rxmon / crf_rx / milan_dp | rc 0; lockstep 86 / 88 checks, mutants 11/11; crf_rx mutants 16/16 |
| gm-step full mutant campaign | 22/22 |
| Yosys / xvlog / builder | 58/58 / 0 findings / pass except gate 11 NOT RUN |
| other docs-workflow gates (82 commands) | 80 rc 0; `act_ci.py --selftest` and one `check_todo_ownership.py --selftest` case fail on this host only (unchanged files; an unchanged copy fails identically; 45/45 under another interpreter) |
| route-1x1 | `pp_resource_gate.py check` rc 0: LUT 49,509, FF 52,348, SLICE 15,649, WNS +0.287 ns, WHS +0.036 ns, fully routed; `KL_avtp_rx_monitor_ctx` 777 LUT / 741 FF after place (base 777 / 740) |

## Round 2b

Round 2b follows the [extended #762 scope ruling](https://github.com/kebag-logic/milan-fpga/issues/762#issuecomment-6265746720),
which answers round 2's first open risk: a stopped input has no playback (Milan v1.2 5.3.8.7, 5.4.2.20), so a
sequence gap on it is no interruption either. One commit on `2cd2750d`:

| Commit | Change |
|---|---|
| `eef90b42` | `KL_avtp_rx_monitor_ctx`: the gap term that queues STREAM_INTERRUPTED gains `&& !stopped_i[ev_s_r]`, read at the PDU's accept verdict. `KL_crf_rx`: `w_ev_si_w` gains `&& !stop_i`, read on the gap PDU's accept edge. SEQ_NUM_MISMATCH is unchanged in both. The lockstep reference and the CRF harness's replica carry the same line; `REGISTER_MAP.md`, the compliance matrix and `TESTING.md` state the rule |

New count-graded checks and mutants (each planted in the engine and in the reference or replica, so only the count
check can catch it):

| Engine | Checks | Mutants |
|---|---|---|
| AAF (`tb/verilator/avtp_rxmon` `[SI]`) | a started gap counts once; a stopped gap counts nothing, nor a second one, and unlocks nothing (its SEQ_NUM_MISMATCH still moves); after START a gap counts again; at N=8 another input's STOP leaves the gap counted; a sweep lands a STOP, and a START, on every edge from -4 to +20 of a gap PDU's pulse, idle and with the walker occupied, and the gap counts once exactly when the input is started on its verdict edge | `stopped gap`, `sticky stop` (START never re-arms the gap), `gap stop late` (state read one cycle after the verdict; caught only by the sweep) |
| CRF (`tb/verilator/crf_rx` `[762-SG]`) | started gap +1; stopped gaps +0, no unlock, one SEQ_NUM_MISMATCH interval; after START +1; a STOP or START on the gap's own edge decides it, one an edge later does not | `stopped_gap_interrupts`, `sticky_stop_gap` |

The CRF driver now builds every counter-harness case from a copy of `sim_main.cpp` (`UNIT_CPP`), so a defect can be
planted in the replica as well.

Validation at `eef90b42`, in clean clones:

| Gate | Result |
|---|---|
| docs gate_50 (fourteen commands) | rc 0 x14 |
| 63-suite sweep, five shards | 63/63, 2,188,354 checks, 0 failures, 0 timeouts, no re-runs |
| avtp_rxmon / crf_rx / milan_dp | rc 0; lockstep 116 / 119 checks, mutants 14/14; crf_rx 15,202 checks, mutants 18/18 |
| gm-step full mutant campaign | 22/22 |
| Yosys / xvlog / builder | 58/58 / 0 findings / pass except gate 11 NOT RUN |
| other docs-workflow gates (82 commands) | 80 rc 0; the same two host-only self-test failures as round 2, on files unchanged since the base |
| route-1x1 | `pp_resource_gate.py check` rc 0: LUT 49,597, FF 52,400, SLICE 15,680, WNS +0.189 ns, WHS +0.014 ns, fully routed; `KL_avtp_rx_monitor_ctx` 800 LUT / 741 FF, `KL_crf_rx` 276 / 541 after place; worst setup path in the SoC CPU, worst hold path in the TDM render FIFO |

## Round 3

Round 3 answers R663-2 (`NEGATIVE`, one MINOR and two residues) under the round-3 assignment (#767 comment
6274405031). R664-2 is `POSITIVE`. Three commits on `eef90b42`:

| Commit | Finding | Change |
|---|---|---|
| `cb65d9d7` | R663-2-F2 | the two `stopped_i` port comments (`KL_avtp_rx_monitor_ctx.sv:152`, `milan_datapath.sv:6307`) now name the sequence gap beside the silence, word for word as the review wrote them |
| `336a6f6a` | R663-2-F1 (MINOR, Tests): no bench graded the datapath's `stopped_i` wiring | `[762-DP]` in `tb/verilator/milan_dp/sim_nxn.cpp`, on every broad `sim_nxn` leg: `obj_nxn`, `obj_nxndv` and `obj_nxn4c` on the retired Arty 4x4 entity, and `obj_nxn8` on the AX7101 8x8 entity at the default geometry. None of them is the shipping AX7101 1x1 TDM8 shape, which [Round 4](#round-4) adds. It uses AAF Stream Input 0, STOP_STREAMING and START_STREAMING over the wire, and every count read with `GET_COUNTERS(STREAM_INPUT, 0)`. While stopped, a gap of two lost PDUs moves SEQ_NUM_MISMATCH +1 and STREAM_INTERRUPTED +0, and the 100 ms silence moves MEDIA_UNLOCKED +1 and STREAM_INTERRUPTED +0. After START and a relock, the same gap counts STREAM_INTERRUPTED +1 |
| `d30a208d` | -- | the milan_dp README paragraph for `[762-DP]` |

The silence is the monitor's own watchdog. The harness advances it to 3 ms short of its limit, as the `[CTRS-CRF]`
arm already does for `KL_crf_rx`, and the expiry and every count after it run for real. A guard check requires the
watchdog to be below that point first, so the write can only shorten the silence.

Wiring mutants at `milan_datapath.sv:6308`, each rebuilt through `build-nxn4c` (the retired Arty 4x4 entity at 4 wire
channels) and run:

| Mutant | Fails |
|---|---|
| port tied to `'0` | `[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0` and `[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0` |
| wrong vector: sink 1's level (`acmpl_stopped_v_w[N_STREAMS:1]`) | the same two |
| wrong vector: the bound level (`acmpl_bound_v_w[N_STREAMS-1:0]`) | `[762-DP] 4 started gap: STREAM_INTERRUPTED +1` |

No other check in the leg fails under any of them, and the clean leg passes (1,981 checks, 0 failures).

R663-2-F3: the status lines and roles above are corrected. R663-2-S1 is not assigned and not taken. No RTL logic
changed, so route-1x1 was not re-run.

Validation at `d30a208d`, in a clean clone:

| Gate | Result |
|---|---|
| `make -C tb/verilator/milan_dp` | rc 0, 0 failures on every leg; `obj_nxn` 1,981, `obj_nxndv` 1,983, `obj_nxn8` 3,765, `obj_nxn4c` 1,981 checks (each +13 for `[762-DP]`) |
| `make -C tb/verilator/avtp_rxmon` | rc 0; lockstep 116 / 119 checks, mutants 14/14 |
| docs gate_50 (fourteen commands) | rc 0 x14 |
| other docs-workflow gates (82 commands) | 80 rc 0; the same two host-only self-test failures as rounds 2 and 2b, on files unchanged since the base, with the same failure lines |
| builder bank | pass except gate 11 NOT RUN |

## Round 4

Round 4 answers R663-3 and R664-3 (each `NEGATIVE` on the same MINOR, R663-3-F1 / R664-3-F1, under Conformance,
Robustness, Tests and Docs) and R663-3-R1, under the round-4 assignment (#767 comment 6283915359). Two commits on
`d30a208d`, no RTL change:

| Commit | Finding | Change |
|---|---|---|
| `16358b62` | R663-3-F1 / R664-3-F1: `[762-DP]` ran on no elaboration of the shipping AX7101 shape | `[762-DP]` also runs at the end of `obj_dynmap`, whose recipe is the `obj_ax1x1` argv on `endstation_ax7101_1x1_tdm8`. After `[DYNMAP]` the leg boots afresh, prints its elaborated stream, audio and prune parameters (opened as constants by `dynmap_probes.vlt`), checks one AAF input and the CRF Media Clock Input at sink `N_STREAMS`, then runs the TRAP-1 bind, the 5.3.8.7 discard section and `[762-DP]` unchanged. The existing legs are kept |
| `f3fef856` | -- | the milan_dp README: the `obj_dynmap` row, its section intro and the `[762-DP]` paragraph |

Why this leg: the broad legs run the case in the broad flow, and the two `sim_nxn` legs on the AX 1x1 shape return
before it. Of those two, only the dynmap recipe carries the shipping geometry; the notify recipe keeps the datapath's
default 2 wire channels. A new leg would add a binary and an argv to the reviewed CI command table; this change leaves
the dynmap argv, and so the table, as they were.

The elaborated parameters against the entity definition (the config's generated design argv, mapped as
`sw/litex/milan_soc.py` maps it, and its generated `adp_shape_defaults.svh`): 19 of 22 are the same, including
`N_STREAMS` 1, `CRF_SNK_IDX_C` 1, `ADP_LISTENER_SINK_C` 2, `TALKER_WIRE_CHANS_P` 8, `AUDIO_IF_SLOTS_P` 8,
`AUDIO_IF_MASTER_P` 1, `LOOPBACK_P` 1, `I2SPB_P` 0 and `LPF_P` 0. Three are the verification substitutes every
`obj_ax1x1`-geometry leg shares, named in the README:

| Parameter | Leg | Shipping | Substitute |
|---|---:|---:|---|
| `MILAN_CLK_FREQ_HZ` | 100,000,000 | 50,000,000 | the verification fabric clock, which the case's 1 ms step assumes |
| `GPTP_PLANE_EN_P` | 0 | 1 | gPTP option OFF; the plane is graded on `obj_gptp` and `obj_ax1x1gptp` |
| `AUDIO_IF_RENDER_SLOTS_P` | 0 | 8 | the render lane is pruned in the `obj_ax1x1` argv; it is graded in `tb/verilator/milan_dp_render` |

Wiring mutants at `milan_datapath.sv:6308` on that elaboration. Each is built through `dynmap-build` with `DP_SRC`
overridden, and each run logs the same elaborated parameters. At `N_STREAMS` 1, sink 1 is the CRF Media Clock Input:

| Mutant | Fails (and nothing else) |
|---|---|
| port tied to `'0` | `[762-DP] 2 stopped gap: STREAM_INTERRUPTED +0` and `[762-DP] 3 stopped silence: STREAM_INTERRUPTED +0` |
| wrong vector `acmpl_stopped_v_w[N_STREAMS:1]` (the CRF sink's level) | the same two |
| wrong vector: the bound level (`acmpl_bound_v_w[N_STREAMS-1:0]`) | `[762-DP] 4 started gap: STREAM_INTERRUPTED +1` |

The clean leg passes, 199 checks with 0 failures.

Wording: the Round 3 rows above now name each leg's entity. `obj_nxn4c` is the retired Arty 4x4, and no broad leg is a
shipping shape. The round-3 mutant script's header is corrected the same way. R663-3-R1: Status and Known limitations
cite the hosted run at `d30a208d`, with `Physical gPTP` skipped.

Validation at `f3fef856`, in clean clones:

| Gate | Result |
|---|---|
| `make -C tb/verilator/milan_dp` | rc 0, 0 failures on every leg; `obj_dynmap` 199 checks (15 `[762-DP]`), `obj_nxn` 1,981, `obj_nxndv` 1,983, `obj_nxn8` 3,765, `obj_nxn4c` 1,981 |
| `[762-DP]` wiring mutants on `obj_dynmap` | 3/3, each failing exactly its named checks |
| `make -C tb/verilator/milan_dp dynmap-mutants` | rc 0, 16/16: three clean controls pass and the 13 planted controls are caught (run after the render and coherence suites' generated inputs exist; the campaign does not make them) |
| docs gate_50 (fourteen commands) | rc 0 x14 |
| other docs-workflow gates (82 commands) | 80 rc 0; the same two host-only self-test failures as rounds 2 to 3, with the same failure lines |
| builder bank | pass except gate 11 NOT RUN |

Not re-run: avtp_rxmon, crf_rx, the 63-suite sweep, Yosys and route-1x1. Nothing of theirs changed since `d30a208d`.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

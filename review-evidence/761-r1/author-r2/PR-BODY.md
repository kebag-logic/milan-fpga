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
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally (round 2b) -- 63/63 suites, 2,188,354 checks, 0 failures; docs gate_50 14/14; Yosys 58/58; xvlog 0
findings; builder bank pass (one arm NOT RUN, gate 11); route-1x1 gate pass (WNS +0.189 ns, LUT -16 against the
record) -- `761-762-mr-interrupt` -> `dev`, head `eef90b4238b6c19b679b44adc6f09362809be153`, six commits on dev
`e9cbb676`. Hosted CI and the act replica have not run this head (not pushed).

## Linked Issue / roles

Closes #761, closes #762

Executor: `[A652]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

Two defects in the AVTP receive and media-clock path, one commit each, then a second round answering R664-1 and
R663-1 and the #762 scope ruling (see [Round 2](#round-2) below), then round 2b for the ruling's extension to
sequence gaps (see [Round 2b](#round-2b)).

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
git checkout eef90b4238b6c19b679b44adc6f09362809be153
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
`lockstep_mutants.py` 14/14; crf_rx's counter harness 15,202 checks and its mutants 18/18; the receipt selftest
reports `shard 0/35 refused` over `34 driver cases`; the gm-step campaign 22/22. The rest of docs gate_50 is the
fourteen commands of `.github/workflows/docs.yml` step `gate_50`. The route follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.

## Known limitations / out of scope

- A followed AAF stream's return still raises no restart. The issue, the assignment and the 4.4.4.3 shall name the
  CRF only; `MEDIA_CLOCK_FOLLOWING.md` now says so explicitly.
- The flat `KL_avtp_rx_monitor` test instrument keeps the old law; the context engine's banner records the delta.
- The silence walk marks the descriptor dirty at its MEDIA_UNLOCKED write and STREAM_INTERRUPTED lands a few cycles
  later, the ordering the PDU walk already uses for MEDIA_LOCKED and the gap's STREAM_INTERRUPTED.
- `scripts/act_ci.py --selftest` (docs gate_42) fails 16 process-group containment probes in this host's sandbox; the
  file is unchanged by this branch, and an unchanged copy fails the same 16 identically. Hosted CI and the act replica
  were not run: the head is not pushed.
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

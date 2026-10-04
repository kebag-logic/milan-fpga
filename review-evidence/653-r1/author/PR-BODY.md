[A529]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN for this change -- `653-unbind-order` -> `dev`, head `77ea6cb4`, four commits on dev `fea346e7` (processor pin `631eeb34`, unchanged). Seven touched suites 52761/0 checks; every touched campaign passes except two whose failures reproduce identically at dev (Known limitations).

## Linked Issue / roles

Relates to #653

The hardware report in #653 stays open for a capture at the DUT's port, a manager bench item.
This PR fixes what the simulation trace proves, per the [re-scope ruling](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-5980290102).

Executor: `[A529]`
Internal cleared-context reviewer: `[R470]`
External reviewer: `[R471]`

## Description

**The fix (ruling item 1).** At dev `fea346e7` an unbind of a locked CRF STREAM_INPUT changed nothing in `KL_crf_rx`.
The unlock was counted only by the 100 ms silence timeout.
So for up to 100 ms after the UNBIND_RX response, GET_COUNTERS read MEDIA_LOCKED 1, MEDIA_UNLOCKED 0: "synchronized" (Table 5.6) on an unbound input.
The AAF inputs already count the unbind's unlock at the bind fall (`KL_avtp_rx_monitor_ctx.sv:857`, task #32).

| Piece | Change |
|---|---|
| `hdl/ieee1722/crf/KL_crf_rx.sv:395` | `w_bind_fall_w = !en_i && en_q`, beside the existing bind-rise edge |
| `hdl/ieee1722/crf/KL_crf_rx.sv:627-631` | on the bind fall while locked: `locked_o` falls, `cnt_unlocked_o` +1, `dirty_p_o` (the Table 5.22 push source) |

- The 100 ms silence path (`:540-545`) is unchanged and still unlocks a bound input that goes silent.
  After an unbind it finds `locked_o` low and counts nothing.
  A timeout on the unbind's own edge writes the same +1, so the event counts once.
- STREAM_INTERRUPTED cannot move: it counts accepted PDUs, and `en_i` low accepts none.
- Nothing is reset on the falling edge (5.3.8.10's asymmetry); the bind-rise wipe (`:641-696`) stays the last writer of `locked_o`.
- No port, register field or parameter change.
  The documented behaviour of the RO lock bit `CRF_CTRL[31]` gains the unbind case, and the datapath's two `crf_locked_w` consumers (the 4.4.4.3 restart request when CRF is selected, and the servo reference lock) now see the fall at the unbind instead of up to 100 ms later.

**Trace** (timed `obj_notify` leg, cycles after the UNBIND_RX command's last byte; frame times are last byte at MAC TX):

| Event | AAF input 0 | CRF input 1, dev `fea346e7` | CRF input 1, this head |
|---|---|---|---|
| listener queues its response | +193 | +193 | +193 |
| debounced bind level falls | +199 | +199 | +199 |
| MEDIA_UNLOCKED written at its source | +204 | +9,818,177 (silence timeout) | **+200** |
| UNBIND_RX response leaves | +277 | +277 | +277 |
| source pair as the response leaves (LOCKED/UNLOCKED) | 1/1 | 1/0 (its write is at +9,818,177) | **1/1** |
| GET_COUNTERS push reporting the unlock, to A / B | +2,294 / +3,057 | +9,819,137 / +9,819,900 | +2,294 / +3,057 |

The response leads on both inputs, at dev and at this head: the wire order #653 reports is not reproduced in simulation (the STOP, issuecomment-5980272602).

**Standing tests (ruling item 2).**
- `tb/verilator/milan_dp/sim_nxn.cpp`, section `[UNB]` of the timed `obj_notify` leg, for the AAF and CRF inputs:
  - U1 the UNBIND_RX response is SUCCESS;
  - U2 a push reporting the unlock reaches each controller, and every such push leaves after the response;
  - U3 the source pair reads 1/1 as the response's last byte leaves, GET_COUNTERS right after reads 1/1/0, and every later push reads LOCKED = UNLOCKED;
  - U4 10.5 M cycles after the command, past both receivers' 100 ms timeouts with the talker still streaming, the pair still reads 1/1/0.
- `tb/verilator/milan_dp/unb_mutants.py` (`make unb-mutants`): five planted controls, each required to fail its named checks while named holds still pass.

  | Planted control | Fails | Failures |
  |---|---|---|
  | the processor holds every ACMP frame 6,000 cycles: the push overtakes the response | U2 order to A, AAF and CRF (holds: U1, push arrived) | 4 of 421 |
  | the CRF unbind does not count its unlock (dev behaviour) | CRF U3 as the response left, and right after it | 2 of 421 |
  | the CRF unbind keeps the lock: the timeout counts it again (double count) | CRF U4; CRF U3 every later push | 2 of 421 |
  | the CRF unbind also counts a STREAM_INTERRUPTED | CRF U3 STREAM_INTERRUPTED; CRF U4 | 2 of 421 |
  | the CRF unbind counts its unlock but arms no push | CRF U2 push reached A / B | 2 of 421 |

- `tb/verilator/crf_rx/sim_main.cpp`, section `[UNB]` (20 checks): one unlock on the unbind's own edge, none at the timeout after, none for an unlocked input, one when the unbind and the timeout share an edge, one for a stopped input still holding its lock, and the bound silence still unlocking.
  `[5t-g3]` now expects MEDIA_UNLOCKED +1 across the unbind of its locked input (it pinned the dev behaviour), and `[5t-g3b]` checks LOCKED = UNLOCKED there.
- Recorded in `tb/verilator/milan_dp/README.md` and the `docs/testing/TESTING.md` campaign table.

**Area (ruling item 3).** `KL_crf_rx` out of context, AX 1x1 TDM8 shape:

| Instrument | dev `fea346e7` | this head | Delta |
|---|---|---|---|
| `syn/yosys/ooc.sh KL_crf_rx` (Yosys 0.66, `synth_xilinx -flatten`) | 433 LUT, 544 FF, 1 RAMB18 | 368 LUT, 544 FF, 1 RAMB18 | -65 LUT, +0 FF |
| Vivado 2026.1 `synth_design -mode out_of_context`, xc7a100tfgg484-2, the datapath's binding (100 MHz, 1 s interval) | 373 LUT, 544 FF, 1 RAMB18 | 352 LUT, 544 FF, 1 RAMB18 | -21 LUT, +0 FF |

No new register: the edge reuses the existing `en_q`. Under the 30 LUT / 60 FF STOP bound on both instruments.

**The issue's stale pointer (ruling item 4).** #653's "Related" line cites `KL_crf_rx.sv:597-605`; at dev `fea346e7` that is the rate-ring update.
The arm that counted a CRF unlock was the silence timeout, `KL_crf_rx.sv:533-536`; the bind-rise arm that drops lock without counting is `:619-670`, correctly, because it zeroes all ten tallies first.
At this head those are `:540-545` and `:641-696`, and the new unbind arm is `:627-631`.

## Authoritative references

- Milan v1.2 Section 5.3.8.10 (Table 5.6): Controller Unbind is a MEDIA_UNLOCKED event, never a STREAM_INTERRUPTED; LOCKED = UNLOCKED means "not synchronized".
- Milan v1.2 Section 5.4.5 (Table 5.22): the unsolicited GET_COUNTERS push; Section 5.4.5.3, the departing-controller monitor.
- #653, its lane comment (issuecomment-5980090994), the STOP (issuecomment-5980272602) and the ruling (issuecomment-5980290102).

## How to get into the same state

```sh
git fetch origin 653-unbind-order
git checkout 653-unbind-order          # head 77ea6cb4
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

## How to validate

```sh
export VERILATOR=<Verilator 5.050>
make -C tb/verilator/milan_dp notify          # timed leg incl. [UNB]
make -C tb/verilator/milan_dp unb-mutants     # the five planted controls
make -C tb/verilator/crf_rx                   # unit [UNB] and [5t-g3]
make -C tb/verilator/milan_dp                 # the suite
OOC_SHAPE=configs/generated/endstation_ax7101_1x1_tdm8 syn/yosys/ooc.sh KL_crf_rx
python3 scripts/lint_rtl.py --check
```

Expected result / pass criteria:

- `notify`: `checks: 421   failures: 0`; the two `[i] [UNB] ... trace` lines carry the head column of the trace table (CRF MEDIA_UNLOCKED at +200, response at +277, pushes at +2294 / +3057).
- `unb-mutants`: `6 checks: 6 PASS, 0 FAIL`.
- `crf_rx`: unit `14287 checks, 0 failures`, every `[UNB-*]` and `[5t-g3*]` line PASS; discontinuity, talker_step and the receiver mutants pass.
- `milan_dp`: exit 0, 11877 checks, 0 failures.
- `ooc.sh`: `KL_crf_rx` 368 LUT, 544 FF, 1 RAMB18.
- lint: 90 <= ratchet 90.

Local gates at `77ea6cb4` (rc 0 each; full table in the lane's handoff):

| Gate | Result |
|---|---|
| `milan_dp` (default) | 11877 / 0 |
| `crf_rx` | 16567 / 0 |
| `pp_shadow` | 2169 / 0 |
| `milan_dp_render` | 315 / 0 |
| `milan_dp_mclk` | 168 / 0 |
| `capture_coherence` | 21194 / 0 |
| `aaf_clock_meter` | 471 / 0 |
| `unb-mutants` / `gsi-mutants` / `crflic-mutants` / `gmstep-mutants` / `render-csr-controls` | 6/6, 9/9, 7/7, 22/22, 4/4 |
| `pp_shadow pending-mutant` | killed by K10 and K12; clean passes |
| `milan_dp_render tdm8render-mutants` | rc 2, 28/32: four arms fail identically with the dev `KL_crf_rx` (byte-identical clean outputs); pre-existing, see limitations |
| `milan_dp_gptp` (physical) | rc 2, 139 checks, 3 audio sample-order failures; identical simulation output with the dev `KL_crf_rx` (pre-existing, see limitations) |
| `syn/yosys/run.sh` | 55 / 55 tops |
| `scripts/xvlog_gate.py --check` (Vivado 2026.1) | PASS, 4 findings == ratchet, 0 in `hdl/` |
| `scripts/lint_rtl.py --check` | 90 <= 90 |
| behave (`~@open-finding`) | 404 scenarios passed |
| builder bank (`sw/builder/test_builder.py`) | all gates pass except gate 11, not run (needs a local Arty build report) |
| docs and code-quality gates of the docs workflow, pinned Markdown renderer | all pass; em-dash 0 findings over 108 added lines |

## Known limitations / out of scope

- #653's reported wire order is not reproduced in simulation: the UNBIND_RX response leaves first on both inputs, at dev and here. The capture at the DUT's port and the 20-connect controller session (acceptance 4) are manager bench items, so this PR relates to #653 rather than closing it.
- No processor change: option (b) is out of scope for this round, and the order needs no fix in this RTL.
- The order control is planted in a copy of the processor top (the ACMP TX lane held 6,000 cycles), because the parent cannot reorder two frames of the processor's single TX stream.
- The AAF unbind path is unchanged (task #32 already counts it); `[UNB]` grades it, and the order mutant catches it, but no AAF-only RTL mutant is planted.
- Two gates fail at this head and identically with the dev `KL_crf_rx`, so this change does not cause them; each needs its own Issue:
  - `milan_dp_render` `make tdm8render-mutants` (rc 2, 28/32): the clean ship leg in `--epoch-only` fails four T30 CRF recentre checks, its two clean controls in that mode fail with it, and the "uncounted repeat" mutant survives in `--serial-only`. Clean outputs in both modes are byte-identical with the dev `KL_crf_rx`, and the mutant also survives against it.
  - `milan_dp_gptp` (rc 2, 139 checks, 3 failures): audio sample order in two windows and the total. The leg never enables the CRF input; the dev-RTL run's 268 simulation-output lines are identical.
- Not run here: `act_ci.py` and hosted CI (nothing is pushed), the whole-tree sweep, and the candidate-merge validation.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

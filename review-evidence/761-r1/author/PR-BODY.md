[A652]

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

GREEN locally -- 63/63 suites, 2,187,305 checks, 0 failures; Yosys 58/58; xvlog 0 findings; builder bank pass
(one arm NOT RUN, gate 11); route-1x1 gate pass (WNS +0.161 ns, LUT -202 against the record) -- `761-762-mr-interrupt` -> `dev`, head
`4191b0987d1313abc86c747ad6a9c3c0963f17da`, two commits on dev `e9cbb676`.

## Linked Issue / roles

Closes #761, closes #762

Executor: `[A652]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

Two defects in the AVTP receive and media-clock path, one commit each.

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
| `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv` (AAF inputs) | per-stream `sil_si_r` marks a pending unlock as the watchdog's; the unlock walk then queues STREAM_INTERRUPTED through the ordinary yielding RMW. An unbind clears the mark, even one landing on a pending silence unlock; the bind decode clears it with the era |
| `hdl/ieee1722/crf/KL_crf_rx.sv` (CRF input) | the 100 ms timeout of a locked sink counts `cnt_intr_o` when bound (`en_i`) and started (`!stop_i`) |
| `tb/verilator/avtp_rxmon` | lockstep `[SI]`: silence, resume, gap, unbind, and an unbind swept across the silence unlock; three mutants (silence, gap, unbind). The frozen M6 reference gains the same lines so the cycle comparison stays exact; #762 is graded by count, not against it. `[H3]` reads its SI wrap before an interval wait that outlasts the silence timeout. N=4 stack `[G6-762]` |
| `tb/verilator/crf_rx` | replica model counts the silence; `[762-a]`/`[762-b]`, `[UNB-d0b]`, `[UNB-d5]` (unbind on the timeout edge); four mutants through a new `unit-build` target |
| `tb/verilator/milan_dp` `[CTRS-CRF]` | the root event arm grades the silence's STREAM_INTERRUPTED; the plan keeps ten distinct counts |
| docs | `REGISTER_MAP.md` CRF counter paragraph, compliance matrix 5.4.2.25, `TESTING.md` |

No register map, top-level port or parameter changes.

## Authoritative references

- IEEE 1722-2016 4.4.4.3: `mr` toggles each time a media clock restart is needed, for a change in the source of the
  media clock, and for a CRF stream's disruption; 10.4.3 for the CRF talker.
- Milan v1.2 5.3.8.10 Table 5.6: STREAM_INTERRUPTED counts each interruption of playback for any reason other than a
  Controller Unbind; 5.4.2.25 Table 5.16: served for each Stream Input.
- Issues #761 and #762; the assignment is comment 6256482625 on #761.

## How to get into the same state

```sh
git fetch origin 761-762-mr-interrupt
git checkout 4191b0987d1313abc86c747ad6a9c3c0963f17da
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
```

Verilator 5.050, sv2v 0.0.12, CPython 3.12.3 with `pyyaml` and `tools/markdown/requirements.txt`, tsn-gen
`deca300c` at `TSN_GEN_ROOT`.

## How to validate

```sh
make -C tb/verilator/milan_dp_mclk
make -C tb/verilator/avtp_rxmon
make -C tb/verilator/crf_rx
make -C tb/verilator/milan_dp_gm_steps gmstep-mutants
python3 scripts/lint_rtl.py --check
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
syn/yosys/run.sh
python3 sw/builder/test_builder.py --require-rv32
python3 syn/ooc/pp_resource_gate.py check "$WORK/ax7101/gateware" --endpoint route-1x1
```

Expected result / pass criteria: every command exits 0. The mclk campaign prints `34 checks: 34 PASS` with mutants
17 and 18 caught; avtp_rxmon's lockstep prints 53/53 at N=1 and N=8 and `lockstep_mutants.py` 8/8; crf_rx mutants
15/15; the gm-step campaign 22/22. The route follows `docs/testing/PP_SHADOW_BASELINE_RECIPE.md`.

## Known limitations / out of scope

- A followed AAF stream's return still raises no restart. The issue, the assignment and the 4.4.4.3 shall name the
  CRF only; `MEDIA_CLOCK_FOLLOWING.md` now says so explicitly.
- A STOPPED CRF sink's 100 ms timeout unlocks without counting STREAM_INTERRUPTED (frames may still be arriving, so
  it is not a silence). Table 5.6 excludes only an Unbind, so a ruling may want a Controller stop counted.
- The flat `KL_avtp_rx_monitor` test instrument keeps the old law; the context engine's banner records the delta.
- The silence walk marks the descriptor dirty at its MEDIA_UNLOCKED write and STREAM_INTERRUPTED lands a few cycles
  later, the ordering the PDU walk already uses for MEDIA_LOCKED and the gap's STREAM_INTERRUPTED.

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

[A681]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

**STOP under owner decision D4.** The measured rows miss T_svc = 10 ms at both points, so S2b (a per-pass work cap in `ctrl_loop`) follows.

The harness itself is green:

- the self-test passes 19/19 checks and catches 12/12 grader mutants;
- both full-harness controls are caught;
- every gate is rc 0 at the head, and behave passes 406/406 scenarios.

`665-s2-cpu-budget` -> `dev-soft-core`, head `d58c8e22e9bd96237b9a28ea1ddd55b0426380c4`.

## Linked Issue / roles

Relates to #665 (lane S2). Not every acceptance item is met: the ADP SHUTDOWN row has no input in the fixture, and the rows miss T_svc.
Relates to #397 (re-opened by the Mark II decisions).

Executor: `[A681]`
Internal cleared-context reviewer: `[R703]`
External reviewer: `[R704]`

## Description

This PR adds a sibling CPU-simulation harness, `tb/verilator/ctrl_service_budget/`, and nothing else. No shipping RTL, SoC, firmware, CI or workflow file changes.

It runs the linked split image (`ctrl_srp_image.py --with-aecp --layout split`), unmodified, on a test-only SoC:

- the shipping cacheless VexiiRiscv, with the CPU at 50 MHz and the bus at 100 MHz;
- `CtrlMemory`;
- the harness's own `KL_mbx` behind `KL_mbx_wb`, with the mailbox RX, TX and event inputs driven from the testbench.

It reports measured clock counts, never estimates. Each is graded against T_svc and its FR_NFR 3.4.1 ceiling.

| Piece | Role |
|---|---|
| `split_soc.py` | The test SoC, built through `nvm_capture_cpu/soc.py` (read-only), with each device where the image addresses it |
| `build.py` | Links the image, builds the SoC, generates `budget_config.hpp` and compiles the native model. It also builds the planted firmware mutation and the labelled arm-B variant |
| `sim_main.cpp`, `observe.vlt` | Drives the mailbox's datapath side, and passively observes commits, both CPU buses, the host port, the RX commit and the event ring |
| `frames.py`, `scenario.py` | The stimulus frames and one script per group: ADP, ACMP with H-DISC, AECP, MAAP, SRP, the backlog rows, the control and the fixture |
| `grade.py`, `run.py` | The 3.4.1 markers, the clock conversion, the pass bound and the verdicts. A missing or malformed probe always fails |
| `selftest.py`, `fixture.log`, `oracle.json` | The portable self-test: 19 checks and 12 grader mutants on a committed trace |
| `runtime_ssp.py`, `fixture_variant.py` | The #723 workaround, and arm B's scratch fixture |
| `README.md` | Method, results, findings, controls and limits |

The results are in the README; selected figures follow.

**Per access and per pass.** 1x1 is one interface; 8x8 is two.

| | 1x1 | 8x8 |
|---|---|---|
| Mailbox read / write | 9 / 9 CPU cycles (0.18 us) | same |
| BRAM fetch / flash-window read | 9.1 / 263 CPU cycles | same |
| Fetch share of the CPU's bus transactions | 0.86 to 0.89 | 0.85 to 0.89 |
| Idle pass | 1.31 to 1.45 ms | 2.04 to 3.71 ms |
| Worst pass | 31.04 ms | 59.79 ms |
| Composed maximum, arm A / arm B | 27.83 / 13.70 ms | 42.82 / 26.04 ms |

**Backlog rows (`MAILBOX_SPLIT.md:753-758`), arm A, ms.**

| Row | 1x1 | 8x8 |
|---|---:|---:|
| an event behind 15 others | 14.12 | 40.51 |
| an ACMP command behind a full acmp ring | 60.35 | 101.98 |
| an ENTITY_AVAILABLE behind a full adp ring | 43.90 | 48.63 |
| a response with 7 frames owed ahead | 75.76 | 98.93 |

The decision input follows.

- **D4.** Per-pass CPU work, not mailbox accesses, sets the time. The consumers, in order:
  - the byte-loop `memset` and `memcpy` of the AECP response buffers;
  - lwSRP `mrp_mad` at link-up;
  - the two AECP polls in every pass;
  - software multiply and divide.
- **The admitted backlog is already small.** It is already the token-bucket burst or the ring room, whichever is smaller. No backlog change shortens a single 40 ms pass.
- **#397's one-hart rule fails.** A pass is the loop's only tick opportunity, and single passes reach 31 and 60 ms.
- **D5.** The shipping core already misses, so a smaller core would miss by more until the cap lands.
- **D3 / S14.** A flash-window read costs about 29 times a BRAM fetch, and the core is fetch-bound, so no path inside T_svc may fetch from flash. The hot set is at least 40.5 KB (1x1) and 43.1 KB (8x8).

The measurement also found three defects, each for its own issue:

1. **The CPU generator decodes the split SoC's 224 KiB `rom` wrongly.** Its decode is `(address & 0xfffc8000) == 0`, so the split image faults at its first call above 0x8000. The harness gives the generator power-of-two covers, and `--cpu-regions as-built` reproduces the fault.
2. **The linked image addresses placeholder devices.** The test SoC places its devices there.
3. **#723 is still open.**

## Authoritative references

- [FR_NFR.md 3.4.1](https://github.com/kebag-logic/milan-fpga/blob/dev-soft-core/docs/reference/FR_NFR.md#341-control-service-budget-and-normative-timing): T_svc, the ceilings and the start and end markers. NFR-SCOUT-01 and NFR-SCOUT-03.
- `docs/design/MAILBOX_SPLIT.md:495-502` (ADP paths), `:645-657` (ACMP paths) and `:753-758` (backlog rows).
- [#397 one-hart rule](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5857491046).
- [Lane S2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409745905), and [owner decisions D3, D4 and D5](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6409738976).
- Frames: IEEE 1722.1-2021 (ADP, ACMP, AECP), Milan v1.2 (MVU), IEEE 1722-2016 Annex B (MAAP), IEEE 802.1Q-2018 clauses 10 and 35 (MRP, MSRP).

## How to get into the same state

```sh
git fetch origin dev-soft-core 665-s2-cpu-budget
git checkout d58c8e22e9bd96237b9a28ea1ddd55b0426380c4
git submodule update --init third_party/lwSRP third_party/tsn-c-stack
# The product LiteX tree, its Python environment first on PATH, and the pinned
# RV32 SDK, as tb/verilator/nvm_capture_cpu/README.md#run describes:
export LITEX_ENV_CC_TRIPLE=riscv32-buildroot-linux-gnu
export PYTHONHASHSEED=0 COURSIER_MODE=offline SBT_OPTS=-Dsbt.offline=true
```

## How to validate

```sh
python3 -B tb/verilator/ctrl_service_budget/run.py --self-test
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir /tmp/budget-8x8 --record-budget-findings
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-slow-adp --mutation slow-adp-rx
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-as-built --cpu-regions as-built
python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir /tmp/budget-1x1-ports \
  --variant answering-ports --groups acmp-cmd,acmp-noresp,acmp-notk,acmp-disc,backlog,backlog-adp \
  --record-budget-findings
(cd tests && behave)
```

Expected result / pass criteria:

- The self-test prints `self-test: 0 failures`, and every `MUTANT caught`, with rc 0.
- The 1x1 run prints `15 groups graded, 0 refusals, 10 T_svc misses`, rc 0. The 8x8 run prints `14 groups graded, 0 refusals, 44 T_svc misses`, rc 0. The misses are the measurement; any refusal fails the run.
- The controls print `CONTROL slow-adp-rx caught` (`control.discover.if0` at 24.614 ms) and `CONTROL as-built caught: an instruction access fault (cause 1)`, rc 0 each.
- Arm B at 1x1 prints `6 groups graded, 0 refusals, 3 T_svc misses`.
- The model is deterministic: a rebuild from this head gave byte-identical native models, so the figures repeat exactly.
- The longest groups take about 25 minutes each; `--jobs` runs groups in parallel.
- The docs gates, the Python and C++ idiom gates and the hygiene gate are rc 0 at the head.

## Known limitations / out of scope

- The STOP is D4's: S2b (the per-pass cap) and any backlog change are separate lanes.
- Each probe measures one phase. The reported pass bound covers every phase under the same passes.
- SHUTDOWN has no fixture input, and START_STREAMING calls a port the fixture leaves empty, so neither is run.
- Ends are mailbox commits. Wire, ingress, egress and network time are not measured.
- Flash erase and program waits are zero; S4 owns the target port.
- Arm B (the answering observation callbacks) changes test code only. Its figures are labelled and are not the formal result.
- There is no Makefile and no CI job, because registering the suite is a CI change outside this lane. The self-test is portable for a follow-up.
- The three defects above are reported, not fixed here.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (STOP under D4; SHUTDOWN row not reachable)
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

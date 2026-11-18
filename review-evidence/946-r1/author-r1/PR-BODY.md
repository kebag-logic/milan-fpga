[A797]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN, the half-tile ROM ledger findings below excepted (owed to S14 by the owner's rule): the firmware gate (units and every planted-defect campaign), fw_coverage, the receive stack's suite, the docs workflow steps, and on the composition the sweep (65 of 65 suites, 2,713,122 checks) and the twin with its plants — `946-ctx-fmt` -> `dev-soft-core`. Composes onto the flip train (PR #945, `b1f1161b`) as step 12 with
no conflict.

## Linked Issue / roles

Closes #946
Relates to #665

Executor: `[A797]`
Internal cleared-context reviewer: `[R<n>]` (to be assigned)
External reviewer: `[R<n>]` (to be assigned)

## Description

**The defect (#946, F-G1).** At 8x8/1if, STREAM_INPUTs 1 to 7 bind and report CONNECTED but discard every PDU as
UNSUPPORTED_FORMAT. `KL_avtp_rx_monitor_ctx` judges a PDU of stream 0 against `fmt0_i`, the published format, and a
PDU of any other stream against its LCTX context's FMT_LO/FMT_HI words. The engine writes those words for stream 0
only, and the only other writer is the CSR 0x800 window, which no firmware wrote. So inputs 1 to 7 were compared
against a zero format (Milan v1.2 Table 5.6, 4.4.2.2).

**The fix is firmware-only, in the split platform.** No RTL, no mailbox-contract change, and the AECP face is
unchanged, so no CPU-budget image moves.

| Piece | Change |
|---|---|
| `plat/ctrl_plat_csr.c`, `.h` | `ctrl_plat_csr_sink_format`: the stream window's listener selection of input n, FMT_LO, FMT_HI, then the selection it held written back. The CSR holds that last write off until the engine took FMT_HI. `ctrl_plat_csr_sink_context`: an AAF STREAM_INPUT above 0 on AVB_INTERFACE 0 in the configuration in force has a context, with its current format. |
| `plat/ctrl_plat.c` | Every AAF input above 0 takes its current format: after `ctrl_app_open_aecp`, with every face acknowledged and before ADP starts; for a SET_STREAM_FORMAT, in the face's change port (wrapped), once interface 0 owes nothing after the call (its commit acknowledged); any other change, or one the face could not commit at once (IN_PROGRESS, done again), at the platform's poll once a later commit is acknowledged. The poll takes the console's slot (the poll table is full) and runs the console after. The state is a file static, so `struct ctrl_plat` and its ledgered size are unchanged. |
| `plat/README.md` | The receive monitor's formats among the ports; the `platsinks` arm among the tests. |
| Tests | `test_plat.cpp` C5 (the window's writes) and C6 (which inputs have a context); `test_plat_sinks.cpp` S1 to S5 at 8x8/1if and 1x1/1if (`plat_arms.arm_platsinks`); `sink_mutants.py`, 19 planted defects in the control campaign. |
| RTL contract test | `tb/verilator/avtp_rxmon/sim_ctxfmt.cpp`: the receive stack at the 8x8 shape's eight contexts, [CF1] to [CF5] (96 checks); `ctxfmt_mutants.py`, 4 planted engine defects; `avtp_rxmon_nx_wrap.sv` sizes its match index by its stream count. |

**Why it is race-free.** A format moves only while its input is unbound: SET_STREAM_FORMAT and SET_CONFIGURATION
refuse a bound one (STREAM_IS_RUNNING). A PDU reaches a context only once its binding's stream_id is published, after
the probe's response. The formats are written before ADP starts, and for a change only once its commit is
acknowledged, so the monitor never judges a PDU against a format no controller sees. An unbind keeps the format: it is
the STREAM_INPUT's, not the binding's.

## Authoritative references

- Milan v1.2 Table 5.6 and 4.4.2.2: only a PDU not in the current format is UNSUPPORTED_FORMAT and discarded.
- IEEE 1722.1-2021 8.2 (each sink binds independently) and 7.4.16 (GET_STREAM_INFO's current format); 7.4.9
  (SET_STREAM_FORMAT); Table 7-126 (IN_PROGRESS, STREAM_IS_RUNNING).
- IEEE 1722-2016 Table 6 (the AAF subtype).
- `docs/reference/REGISTER_MAP.md`, the 0x800 stream window (LCTX words 2 and 3).
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv` (the LCTX record and its window port contract), `aecp/aecp_face.h`
  (`applied`), `aecp/aecp.h` (`AECP_WAITS`, the change done again after IN_PROGRESS).

## How to get into the same state

```sh
git fetch origin 946-ctx-fmt dev-soft-core
git checkout 946-ctx-fmt
git submodule update --init gptp-processor protocol-processor third_party/lwSRP third_party/tsn-c-stack third_party/verilog-axis
# the repository's pinned toolchain and RV32 SDK (sw/firmware/gtest/README.md, docs/testing/CI_WORKFLOWS.md)
```

## How to validate

```sh
# the firmware: units, every arm, and the planted-defect campaigns (platsinks among them)
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
python3 sw/firmware/gtest/fw_coverage.py --check
# the receive stack's suite, the new N=8 format contract and its planted engine defects among it
make -C tb/verilator/avtp_rxmon
# the two-placement simulation and its plants
make -C tb/verilator/milan_dp twin twin-plants
```

Expected result / pass criteria: every arm PASS; `Sinks.S1` to `S5` and `Plat.C5`, `C6` pass at both shapes; the
campaign reports every defect caught, `sink-*` and `set-format-bound-accepted` among them; `CTXFMT N=8: 96 checks, 0
failures` and `5 checks: 5 PASS, 0 FAIL`; the twin `0 finding(s)` and every plant refused by its words.

## Known limitations / out of scope

- **F-G2 (one stream bound to two inputs) is not this cause.** The stream parser classifies a PDU to one context, the
  highest matching enabled entry (`avtp_stream_parser.sv:193-196`), so with this fix the higher input receives and
  the lower one still does not. Fan-out needs RTL and a ruling; for its own ticket.
- **F-G3 (a running output's `stream_dest_mac` 0) is #943's**, the datapath's GSI face; unchanged here.
- **The all-fabric image shares F-G1 and is unchanged.** Its firmware writes none of these words, and its AECP is the
  fabric's, so a firmware write could not follow SET_STREAM_FORMAT; the fix there is RTL. For its own ticket.
- **ROM.** The platform code is about 1 KB of RV32 text. By the owner's loose-BRAM rule this is debt owed to S14:
  the ledger finds one point half a RAMB36 past on each base. On dev-soft-core the 8x8/1if image plans 56.5 RAMB36
  (the 56 budget; the flip train already carries an 8x8/1if entry at 58.0). On the flip train the 8x8/2if image
  plans 63.0, past its 62.5 entry, which needs raising when this composes. The ledger is left untouched here, so the
  branch merges onto the train with no conflict.
- The platform's new work runs only in the product image, which no CPU-budget row measures (the rows' images are the
  size fixture's and are byte-identical). Its cost is measured in the split boot simulation: at 8x8 the product image writes the
  seven contexts before ready (28 window writes, 2,858 bus cycles) and reaches ready 0.107 ms later than the train head
  (67.241 against 67.134 ms); at 1x1 it writes nothing and is 0.042 ms later (the model's scan).
- At dev-soft-core alone the two-placement simulation reports one finding, the owed row `split-talker-failed`, which
  dev-soft-core `cb96336d` reports itself with byte-identical captures; the flip train restates that row, and its twin
  passes with this change.
- The register map's design note for FMT_LO/FMT_HI lives in the train's regenerated reference; who writes these words
  is documented in `sw/firmware/ctrl/plat/README.md`.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the bench's stream, power-cycle and soak items at 8x8/1if are
      the gating run's, after this change is composed)
- [x] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

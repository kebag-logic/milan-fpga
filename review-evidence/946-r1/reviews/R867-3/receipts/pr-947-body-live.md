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

GREEN at `fe297847` (round 3, tests and docs only) — `946-ctx-fmt` -> `dev-soft-core`:
- run again at this head, on the branch and on the composition: the firmware gate (units and every planted-defect
  campaign), fw_coverage, the docs workflow steps, the ROM ledger with its controls and the product images' bytes
  (unchanged), and the CPU-budget images (hash-equal);
- carried from round 2 (`9f4f3de0`; composition `d98dd322`), whose inputs round 3 does not change: the memory test,
  the receive stack's suite, the split boot simulation, the two-placement simulation and, on the composition, the
  full sweep (65 of 65 suites). The two-placement simulation reports dev-soft-core's own result on the branch, and 0
  findings on the composition.

It composes onto the flip train (PR #945, `b1f1161b`) as step 12 with one composition step. The ROM ledger's files
take the train's side, and the train's `platform-8x8-two-interfaces` entry is raised from 62.5 to 63.0 (below).

Author packets: [`review-evidence/946-r1/author-r1` to `author-r3`](https://github.com/kebag-logic/milan-fpga/tree/946-review-evidence/review-evidence/946-r1) on branch `946-review-evidence` (archive `57588db2`).

## Linked Issue / roles

Closes #946
Relates to #665

Executor: `[A797]`
Internal cleared-context reviewer: `[R867]`
External reviewer: `[R868]`

## Description

**The defect (#946, F-G1).** At 8x8/1if, STREAM_INPUTs 1 to 7 bind and report CONNECTED but discard every PDU as
UNSUPPORTED_FORMAT. `KL_avtp_rx_monitor_ctx` judges a PDU of stream 0 against `fmt0_i`, the published format, and a
PDU of any other stream against its LCTX context's FMT_LO/FMT_HI words. The engine writes those words for stream 0
only, and the only other writer is the CSR 0x800 window, which no firmware wrote. So inputs 1 to 7 were compared
against a zero format (Milan v1.2 Table 5.6, 4.4.2.2).

**The fix is firmware-only, in the split platform.** No RTL, no mailbox-contract change, and the AECP face's and the
core's sources are unchanged, so no CPU-budget image moves.

| Piece | Change |
|---|---|
| `plat/ctrl_plat_csr.c`, `.h` | `ctrl_plat_csr_sink_format`: the stream window's listener selection of input n, FMT_LO, FMT_HI, then the selection it held written back. The CSR holds that last write off until the engine took FMT_HI. `ctrl_plat_csr_sink_context`: an AAF STREAM_INPUT above 0 on AVB_INTERFACE 0 in the configuration in force has a context, with its current format. |
| `plat/ctrl_plat.c` | Every AAF input above 0 takes its current format: after `ctrl_app_open_aecp`, every face acknowledged and before ADP starts; then in each change the core keeps, inside the face's change port (wrapped), before the core answers it: a SET_STREAM_FORMAT writes its input's context, a SET_CONFIGURATION every one. The core keeps a change the face applied at once, and one it does again after IN_PROGRESS; the face's applied port, also wrapped, tells the change port which. That applied port answers false for a waiting change that would move the context of an input bound meanwhile, so the core keeps the values in force and answers ENTITY_MISBEHAVING at `AECP_WAIT_MS`, its documented timeout. No poll: no pass with no change writes anything. The state is a file static, so `struct ctrl_plat` and its ledgered size are unchanged. |
| `plat/README.md` | The receive monitor's formats among the ports; the `platsinks` arm among the tests; the 8x8 images' ROM. |
| Tests | `test_plat.cpp` C5 (the window's writes) and C6 (which inputs have a context). `test_plat_sinks.cpp` S1 to S11 at 8x8/1if and 1x1/1if (`plat_arms.arm_platsinks`), every mailbox access watched: whenever an input's binding has a stream published, its context holds the input's current format, from the access that publishes it, and no SET_STREAM_FORMAT's SUCCESS leaves before its context holds it. S11 drives a change of another type or kind at a bound input's own index: its STREAM_OUTPUT's waiting SET_STREAM_FORMAT and its SET_NAME are taken, and neither writes a context. S1 checks that every format an input with a context advertises is AAF. `sink_mutants.py`: 28 planted defects in the control campaign. |
| RTL contract test | `tb/verilator/avtp_rxmon/sim_ctxfmt.cpp`: the receive stack at the 8x8 shape's eight contexts, [CF1] to [CF5] (96 checks), [CF4] the first PDU after a bind whose format was written the cycle before; `ctxfmt_mutants.py`, 4 planted engine defects; `avtp_rxmon_nx_wrap.sv` sizes its match index by its stream count. |
| ROM ledger | `sw/litex/ctrl_memory.py` LEDGERED: `platform-8x8-two-interfaces` 60.5 -> 61.0, and a new `platform-8x8-one-interface` at 56.5, by the owner's rule of 2026-11-15 (#665); their cases in `ctrl_memory_ledger.py` and `test_ctrl_memory.py`; `plat_ledger.py` links the 8x8/1if point with its entry, with a control for it; `boot_soc.PLATFORM_LEDGERED`; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3 and 5. |

**Why it is race-free.** A context's format moves only while its input is unbound:

- SET_STREAM_FORMAT and SET_CONFIGURATION refuse a bound input (STREAM_IS_RUNNING).
- A change that waited (IN_PROGRESS) is not applied while an input whose context it moves is bound. A BIND_RX taken during the wait makes that possible. The change stays undone and is answered ENTITY_MISBEHAVING at the wait's bound (IEEE 1722.1-2021 7.4.9; `aecp.h`, `applied`).
- Every change the core keeps writes its contexts in the change port. The port first forwards the change to the face, whose publication makes its own mailbox accesses (the face block's writes, its commit and its status reads). Unless the core is doing a waiting change again, the port then reads the face's applied state. Only then does it write the contexts. All of it runs before the core answers the command and before control returns to the event loop. So no ACMP input is processed between the change (or, for a waiting change, the applied port's bound check) and the write. The affected input stays unbound throughout, and no stream can be published for it meanwhile.
- A PDU reaches a context only once its binding's stream_id is published, after the probe's response.

So whenever a stream is published, its context holds the input's current format. An unbind keeps the format: it is
the STREAM_INPUT's, not the binding's. Round 1 said formats move only while unbound; that was false on the deferred
path, where a change waiting for its acknowledgement was done again onto an input bound meanwhile (R868-1-F1). It is
now enforced.

## Authoritative references

- Milan v1.2 Table 5.6 and 4.4.2.2: only a PDU not in the current format is UNSUPPORTED_FORMAT and discarded.
- IEEE 1722.1-2021 8.2 (each sink binds independently), 7.4.9 (SET_STREAM_FORMAT, refused for a bound input) and
  7.4.16 (GET_STREAM_INFO's current format); Table 7-126 (IN_PROGRESS, ENTITY_MISBEHAVING, STREAM_IS_RUNNING).
- IEEE 1722-2016 Table 6 (the AAF subtype).
- `docs/reference/REGISTER_MAP.md`, the 0x800 stream window (LCTX words 2 and 3).
- `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv` (the LCTX record and its window port contract), `aecp/aecp_face.h`
  (`applied`), `aecp/aecp.h` (`AECP_WAITS`, `AECP_WAIT_MS`, a waiting change done again or kept undone).
- The owner's decision of 2026-11-15 on #665 (issuecomment-6892332745): an image past its ROM entry raises it to its
  measured half tile, as named debt owed to S14.

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
# the platform image at every ledger point, and the memory test's ledger cases
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir <dir> --self-test
python3 sw/litex/test_ctrl_memory.py
# the receive stack's suite, the N=8 format contract and its planted engine defects among it
make -C tb/verilator/avtp_rxmon
# the two-placement simulation and its plants
make -C tb/verilator/milan_dp twin twin-plants
```

Expected result / pass criteria:
- every arm PASS; `Sinks.S1` to `S11` and `Plat.C5`, `C6` pass at both shapes;
- the campaign reports every defect caught, the 27 `sink-*` and `set-format-bound-accepted` among them;
- `plat_ledger: PASS (0 finding(s))` with every control as required, and `test_ctrl_memory: 0 failure(s)`;
- `CTXFMT N=8: 96 checks, 0 failures` and `5 checks: 5 PASS, 0 FAIL`;
- the twin's plants each refused by their words.

## Known limitations / out of scope

- **F-G2 (one stream bound to two inputs) is #948.** The stream parser classifies a PDU to one context, the
  highest matching enabled entry (`avtp_stream_parser.sv:193-196`), so with this fix the higher input receives and
  the lower one still does not. Fan-out needs RTL and a ruling.
- **The release image's F-G1 is #949.** The all-fabric image shares the zero-format defect and is unchanged here: its
  firmware writes none of these words, and its AECP is the fabric's, so a firmware write could not follow
  SET_STREAM_FORMAT; the fix there is RTL. #946's scope is the split image.
- **F-G3 (a running output's `stream_dest_mac` 0) is #943's**, the datapath's GSI face; unchanged here.
- **A change that waited, refused because its input was bound meanwhile, is answered ENTITY_MISBEHAVING** at the
  wait's bound (100 ms after the command), the core's documented answer for a change not applied, not
  STREAM_IS_RUNNING: the core's sources are unchanged.
- **The datapath's copy of the face during that wait.** The face committed the change before the core undid it, and
  the datapath takes that commit when it acknowledges it. So until the face publishes the values in force again, its
  per-input format (`F_FMT_IN`, the map's channel clip for inputs above 0) may hold the refused value. The face's
  existing rollback path ends this, at most the wait's bound.
- **Input 0, the CRF input and STREAM_OUTPUTs have no context here.** For those, the core still does a waiting change
  again without repeating its bound or running check (`aecp.c`, the waiting command); for input 0 the face's own
  commit carries the format to `fmt0_i`. Repeating the check there is the core's own change, which moves every
  CPU-budget image. It is not this issue's receive-context defect: it is #950, which also carries the clause's
  status for a refused change. The face copy's exposure above, the map's channel clip, is #950's to cover too, with
  delayed-acknowledgement tests for input 0, the CRF input and STREAM_OUTPUTs.
- **ROM, by the owner's rule of 2026-11-15** (debt owed to S14):
  - On dev-soft-core the platform's 8x8/2if image plans 61.0 RAMB36: 133,224 B of rom, 104 B past the 133,120 B
    that 60.5 holds. Its entry is raised from 60.5 to 61.0.
  - Its 8x8/1if image, a product image, plans 56.5: 131,656 B, 584 B past 56.0. It takes its own entry,
    `platform-8x8-one-interface`, at 56.5.
  - On dev-soft-core the product SoC build names no entry, so an 8x8/1if product build there is still held to 56.
    The flip train plans product images at their own entry (`own_point`).
  - **At composition onto the train**, these ledger files conflict with the train's. They take the train's side,
    where `platform-8x8-one-interface` is already 58.0 and the composed 8x8/1if image fits it at 138,624 B. The
    train's `platform-8x8-two-interfaces` entry is raised from 62.5 to 63.0: the composed image plans 140,200 B of
    rom, 936 B past the 139,264 B that 62.5 holds.
- The platform's new work runs only in the product image, which no CPU-budget row measures; the rows' images are the
  size fixture's and are byte-identical to the train's recorded ones (1x1 `55484254e638ed7f`, 8x8/1if
  `175418f4b5b1a9d4`). In the split boot simulation on the composition at 8x8, the product image writes the seven
  contexts before ready: 28 window writes in 3,022 bus cycles. It reaches ready at 67.328 ms against the train head's
  67.134. At 1x1 it writes nothing and reaches ready at 27.936 ms against 27.981; that run does strictly more work yet
  is sooner, so these figures bound the cost and do not resolve it below a few thousand cycles. Neither is near the
  20,000 ms bound.
- At dev-soft-core alone the two-placement simulation reports the owed row `split-talker-failed`, and its plant
  `srp-plus-k` escapes, exactly as dev-soft-core `cb96336d` does with byte-identical captures. The flip train restates
  that row; on the composition the twin reports 0 findings and refuses every plant.
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


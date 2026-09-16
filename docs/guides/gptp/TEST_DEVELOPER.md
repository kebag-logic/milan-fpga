<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Fabric gPTP test-developer guide

Use this page for verification changes.

## Contents

- **[Choose a language](#choose-a-language)** — Match tools with observable boundaries.
- **[Choose a suite](#choose-a-suite)** — Start with the smallest useful layer.
- **[Build an oracle](#build-an-oracle)** — Detect failures independently.
- **[Publish evidence](#publish-evidence)** — Make every result reproducible.

## Choose a language

| Language | Current gPTP role |
|---|---|
| Python | Microcode generation, models, fuzzing, gates |
| C | No first-party gPTP harness |
| C++ | Verilator clocks, stimulus, and assertions |
| SystemVerilog | DUT wrappers and production RTL |
| Make | Reproducible suite entry points |

C firmware never judges gPTP correctness.

Python models must not mirror implementation blindly.

Read the [engine test guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/c1b617435824929a790739ea8585c3fe1a328cc0/docs/TEST_DEVELOPER.md).

## Choose a suite

| Suite | Boundary |
|---|---|
| Donor `ucpu` | Arithmetic and instruction execution |
| Donor `parser` | Byte parsing and refusal paths |
| Donor `engine` | Protocol behavior and servo |
| Donor `gaskets` | Bench MII gasket loopback and FIFO wedge |
| Parent `ptp` | PHC accumulator arithmetic |
| Parent `ptp_ts` | Stand-alone record stamper, absent from the product |
| Parent `gptp_shadow` | Transport, pairing, publication, ledger laws |
| Parent `gptp_plane` | Closed-loop PHC steering |
| Parent `gptp_txts` | Egress launch time over the converted product MAC |
| Parent `clkvalid` | Discontinuity and holdover |
| Parent `milan_dp` | Product wiring and public consumers |
| Parent `tsn_fuzz` | Independent wire-model campaigns |

Begin with the narrowest failing suite.

Finish with complete donor and parent gates.

## Build an oracle

- Name one requirement or defect.
- Drive only public DUT interfaces.
- Compare accepted transfers only.
- Build expected protocol fields independently.
- Include positive controls.
- Include malformed and truncated inputs.
- Include backpressure and timeouts.
- Include reset during activity.
- Convert product software rather than modelling it.
- Then prove the conversion behaves like its source.
- `sw/litex/test_gptp_tx_timestamp.py` is that proof.
- Record the defects a suite cannot see.
- `tb/verilator/gptp_shadow/mutants.py` carries such a record.
- Withhold and reorder timestamp returns.
- Plant one deliberate mutation.
- Confirm that mutation fails.
- Restore production code afterward.

## Publish evidence

- Record the exact commit.
- Record each complete command.
- Record every exit status.
- Preserve the first failure log.
- Separate simulation from physical evidence.
- State uncovered boundaries explicitly.

Use the [traceability table](../../traceability/ieee8021as.md).

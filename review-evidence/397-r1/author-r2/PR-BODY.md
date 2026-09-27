[A363]

## Status

Round-2 author validation complete; independent re-review pending.
`397-service-budget` targets `dev`. Candidate commit: `ff75a70807c151517860c73a06d7ea36e2a46008`.
This is measurement evidence, including negative budget margins.

## Linked Issue / roles

Refs #397. Related firmware repair: #590.
The author and independent internal/external reviewers are assigned in the
[round-2 contract](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5855879265).
Bench items and the complete architecture decision remain open.

## Description

Measure boot, AEM copy/CRC, binding restore, journal erase/commit and every
registered product console command on the unchanged shipping CPU at 50 MHz.
External UART, SPI, CSR and backend markers delimit elapsed intervals.
The sibling harness reuses the capture SoC read-only and records the flash
wait contribution separately from service work.

## Round 2

- Observe retired heartbeat-function entries passively and report each duty's longest no-tick span, the 250 ms phase and UART TX allowance, with margins against 500 ms and 2,000 ms.
- Name the immediate, UART-paced, queued-input and device-wait plans. Retain actual heartbeat-gap endpoints, right-censored tails and printed backing-state samples.
- Reproduce the public queued-input and long-WIP probes unchanged. Both shipped shapes lose backing under queued status input; #590 owns the firmware repair.
- Start AEM timing at the first accepted read address at its flash offset. Restore the 20-second ADP validity comparison for simulated boot, with the BIOS and physical-I/O exclusions explicit.
- Support independent erase/page waits through the 3 s / 5 ms device corner and reject unsupported values before a build starts.
- Pin complete analysis against three fixed traces and explicit counter controls. Repair the busy-refusal test so deleting the busy predicate makes it fail.
- Move raw run receipts out of the product tree into the handoff evidence packet; record their SHA-256 values in the findings page. State that the SPI substitution understates physical transfer cost.

| Observed result | 1x1 | 8x8 |
| --- | ---: | ---: |
| Longest boot to entity enable, ms | 373.97461 | 1094.48517 |
| Margin against 20,000 ms ADP comparison, ms | 19626.02539 | 18905.51483 |
| Longest AEM envelope, ms | 57.99594 | 137.01392 |
| Longest NVM status envelope, ms | 233.64297 | 814.07889 |
| Device-max whole commit, ms | 3339.59461 | 4307.68299 |
| Queued heartbeat tail, ms | 2569.49201 | 2513.33593 |
| Final queued backing sample | 0 | 0 |

The complete duty, opportunity and schedule tables are in
[the findings](docs/findings/397_SERVICE_BUDGET.md).
Firmware, RTL, submodule pins and every capture-harness file are unchanged.

## Authoritative references

- [Round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5855879265)
- [Product-CPU re-scope](https://github.com/kebag-logic/milan-fpga/issues/397#issuecomment-5854787465)
- [Firmware contract](docs/integration/BAREMETAL_FIRMWARE.md)
- [Saved-state deadlines](docs/design/SAVED_STATE_FASTCONNECT.md#94-the-deadlines) and [remaining persistence duties](docs/design/SAVED_STATE_FASTCONNECT.md#122-where-they-go-today)
- Milan v1.2 sections 5.6.2/5.6.3: ADP `valid_time = 10` in two-second units.
- [Requirements](REQUIREMENTS.md); IEEE 1722.1-2021 section 9.3.2.6's response timing remains fabric-owned.

## How to get into the same state

Use the candidate worktree with initialized dependencies and the
[capture prerequisites](tb/verilator/nvm_capture_cpu/README.md#run).
Use the configured BIOS-build environment and set its compiler prefix through
`LITEX_ENV_CC_TRIPLE`; keep system build utilities ahead of SDK utilities.
Keep build trees outside the checkout.

```sh
export PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-1x1 --build-only
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/service-8x8 --build-only
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_1x1_tdm8 --build-dir /tmp/service-1x1 --reuse-build --populated --record-budget-findings
python3 -B tb/verilator/fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-dir /tmp/service-8x8 --reuse-build --populated --device-wait-us 1000 --program-wait-us 1000 --record-budget-findings
```

Repeat each shape with `--plan uart-paced` and `--plan queued-input`, using zero waits.
For `--plan device-wait`, use `--device-wait-us 3000000 --program-wait-us 5000`.
Keep `--populated --record-budget-findings`; use separate directories for concurrent scenarios.
Append `--regrade` with identical scenario arguments to verify an existing bound log.

## How to validate

```sh
python3 -B tb/verilator/fw_service_budget/run.py --self-test
python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
python3 -B scripts/check_nvm_capture.py
python3 -B scripts/check_feature_status.py --self-test
python3 -B scripts/pp_srcs.py --check
python3 -B scripts/check_baremetal_only.py --check
python3 -B scripts/check_entity_shape.py --self-test
python3 -B scripts/docs_check.py
python3 -B scripts/check_doc_paths.py
python3 -B scripts/check_doc_style.py
python3 -B scripts/check_archive.py
python3 -B scripts/gen_toc.py --check
python3 -B scripts/check_em_dash.py --base ac18b50968b12efe4d15c0a06301264b35656b31
python3 -B scripts/check_py_idiom.py
python3 -B scripts/check_cpp_idiom.py
python3 -B scripts/check_hygiene.py --check
python3 -B scripts/measure_test_evidence.py --check
python3 -B sw/builder/test_builder.py --require-elaboration
git diff --check ac18b50968b12efe4d15c0a06301264b35656b31
```

All 19 local gates and all eight bound-log measurement regrades returned zero. The portable gate passes 30 oracle controls and 14 flash controls. The unchanged public mutation suites reject 11/11 and 15/15 mutants; the unchanged control passes. The builder bank returns zero with one calibration arm not run because its physical utilization report is absent; all elaboration arms ran. Capture integrity and feature-status checks remain green. Success in reporting mode retains the documented budget overruns.

## Known limitations / out of scope

The duty-period calculation assumes service opportunities outside the measured duty.
Queued input suppresses the idle hook and invalidates that isolated-duty assumption.
Printed backing samples are observations, not a continuous-liveness proof.
The final heartbeat tail ends at the final prompt and is right-censored.
The paced mode rounds frame spacing upward; the unchanged public pacing probe rounds down.

The SPI substitution is optimistic. DDR is simulated, packet traffic is absent,
and only one clock phase is measured. Boot excludes BIOS CRC, startup delays
and memory testing; immediate UART runs also exclude physical serialization.
Device-max commit runs are executed evidence, not physical twofold-margin proof.
Future firmware duties, board torture and the complete hart decision remain open.
The evidence packet is prepared for manager publication; this author handoff does not push or alter the PR.

## Definition of Done

- [x] Round-2 measurement changes and self-checking controls implemented
- [x] Required local assignment gates pass; results and limitations recorded
- [x] Findings and authoritative firmware documentation updated
- [x] No firmware, RTL, submodule or capture-harness change
- [ ] Evidence packet and replacement body published by the manager
- [ ] Internal and external re-reviews, including acceptance of finding resolutions
- [ ] Review coverage ledger accepted at the candidate head
- [ ] Candidate merge validation, hosted gates and authorized merge
- [ ] Post-merge containment
- [ ] Remaining issue #397 bench and architecture work

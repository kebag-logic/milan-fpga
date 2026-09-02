<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# IEEE 802.1AS traceability

Milan selects the 2011 wire profile.

Corrigenda one and two also apply.

Hardware-assist context may cite the 2020 edition.

Decision #139 records that edition split.

## Contents

- **[Status key](#status-key)** — Interpret each concise evidence verdict.
- **[Clause mapping](#clause-mapping)** — Map clauses into source and tests.
- **[Requirement mapping](#requirement-mapping)** — Connect product requirements with rows.
- **[Open evidence](#open-evidence)** — Keep physical gaps explicit.

## Status key

| State | Meaning |
|---|---|
| Covered | Executable evidence exists |
| Partial | Some required evidence remains open |
| Missing | Required capability or evidence remains absent |
| Not applicable | Product media excludes that clause |

Simulation never becomes physical evidence.

## Clause mapping

| ID | Clause | Product obligation | Source owner | Evidence | State |
|---|---|---|---|---|---|
| AS-1 | 8.2 | Adjustable nanosecond PHC | `timestamp_counter` | `ptp` | Covered |
| AS-2 | Annex B.1 | Accurate adjustable local clock | PHC and board clock | `ptp`; board records | Partial |
| AS-3 | 8.4.3 | Correct timestamp reference planes | `KL_gptp_shadow`; `KL_gptp_txstamp` | `gptp_shadow` | Covered |
| AS-4 | 8.4.3 | Per-unit latency calibration | Issue #64 | No complete procedure | Missing |
| AS-5 | 11.3 | Timestamp event messages only | Engine parser and timestamp paths | Donor; `gptp_shadow` | Covered |
| AS-6 | 10.2–10.3 | Best-master selection | Imported engine | Donor; `tsn_fuzz` | Partial |
| AS-7 | 11.1–11.2 | Sync and Follow_Up operation | Imported engine and PHC | Donor; `gptp_plane` | Covered |
| AS-8 | 11.2.19 | Peer delay and `asCapable` | Imported engine | Donor; `tsn_fuzz` | Covered |
| AS-9 | 8.1, 10.6 | Domain zero and profile intervals | Generated microcode | Donor; `tsn_fuzz` | Covered |
| AS-10 | 11.4 | Milan-selected message formats | Imported engine | `tsn_fuzz` | Covered |
| AS-11 | 12–16 | Non-Ethernet media layers | None | Product scope | Not applicable |
| AS-12 | 10.3, 10.6 | Traffic-independent receipt timing | Imported engine timers | Donor; `tsn_fuzz` | Partial |

The [fabric guide](../design/GPTP_PLANE.md) defines boundaries.

The [engine ledger](../../gptp-processor/docs/SOURCE_EVIDENCE.md) maps internals.

## Requirement mapping

| Requirement | Primary rows |
|---|---|
| `REQ-PTP-01` | AS-1 |
| `REQ-PTP-02` | AS-1 |
| `REQ-PTP-03` | AS-3, AS-5 |
| `REQ-PTP-04` | Standalone timestamp-record scope |
| `REQ-PTP-05` | AS-6 through AS-12 |
| `REQ-PTP-06` | AS-3, AS-4 |
| `REQ-PTP-07` | AS-3, AS-6 through AS-9 |
| `REQ-PTP-08` | AS-7, AS-12 |
| `REQ-PTP-09` | AS-6 through AS-12 |

[`REQUIREMENTS.md`](../../REQUIREMENTS.md) remains normative.

## Open evidence

- Issue #64 owns physical latency calibration.
- Issue #117 owns two-board product acceptance.
- AS-6 needs the physical winner variant.
- AS-12 needs physical traffic-load repetition.

Option-off evidence proves safe absence only.

It never represents another product implementation.

The detailed predecessor remains [archived](../history/v1/traceability/ieee8021as.md).

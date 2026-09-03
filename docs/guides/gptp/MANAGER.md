<!-- SPDX-FileCopyrightText: 2026 Kebag Logic -->
<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->

# Fabric gPTP manager guide

Use this page for delivery decisions.

## Contents

- **[Value](#value)** — Understand product ownership and benefits.
- **[Status](#status)** — Separate implementation from acceptance.
- **[Risks](#risks)** — Keep unresolved evidence visible.
- **[Release evidence](#release-evidence)** — Require exact-head proof before delivery.

## Value

- Protocol work stays inside programmable logic.
- One plane owns synchronization and public health.
- Hardware timestamps avoid processor scheduling latency.
- Atomic publication prevents contradictory consumer state.
- Direct health drives every AVTP uncertainty bit.

Read the [engine manager guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/f5ba2db636112d1292671b49a047c9fd9daacf7e/docs/MANAGER.md).

## Status

| Area | Current state | Evidence |
|---|---|---|
| Product owner | Implemented | Feature-status ledger |
| Protocol engine | Implemented | Donor suites |
| Parent transport | Implemented | `gptp_shadow` |
| Public consumers | Implemented | `milan_dp` |
| Physical calibration | Incomplete | Issue #64 |
| Two-board acceptance | Incomplete | Issue #117 |
| Media clock selection | Implemented | Feature-status ledger |

No external approval is claimed.

Simulation remains necessary but insufficient.

## Risks

- New boards lack complete timestamp calibration.
- Physical grandmaster-winner evidence remains open.
- Imported revisions require independent review.
- Engine timestamp capacity has an upstream issue.
- Engine receive errors have an upstream issue.
- Issue #74 media-clock bench acceptance remains open.

Open upstream risks appear in the [engine guide](https://github.com/Mister-M-alt/FPGA-gPTP/blob/f5ba2db636112d1292671b49a047c9fd9daacf7e/docs/MANAGER.md).

## Release evidence

- Review the exact imported commit.
- Run every donor suite.
- Run every parent integration suite.
- Confirm documentation and diagram gates.
- Confirm exact-head hosted checks.
- Require independent five-lens review.
- Require issue #117 physical acceptance.

Read the [parent architecture](../../design/GPTP_PLANE.md).

[A298]

Closes #443

## Status

Ready for independent review at `c9bbb03cc3d4da9c6ee28996b91addbb081efa7e`.

## Description

Expose render setpoint state at `RENDER_STAT` (`0x8DC`). The existing listener selector chooses fill, prefill and convergence; the upper half reports global saturating rails. Absent stages supply structural zero. The register map, production class and latency documentation define the layout and semantics.

## How to reproduce

Select a listener through `STRM_SEL` and read `0x8DC` while receiving media.

## How to validate

Integration checks compare bus reads with source taps through prefill, convergence and a rail. The absent-stage control reads zero; the wrong-fill mutant fails its named check. Two-listener selection and the full regression pass. All requested gate commands return zero. Builder gate 11 is NOT RUN because the calibration placement report is absent.

Generic cell counts, base to head: `milan_csr` 70,355 to 70,466; `milan_datapath` 1,633,435 to 1,631,783.

## DoD

Acceptance items 1, 2, 3 and 5 are met locally. Item 4 follows the manager decision: no `STREAM_INTERRUPTED` wiring. Independent review remains pending.

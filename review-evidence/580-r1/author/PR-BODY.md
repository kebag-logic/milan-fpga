[A366]

Closes #580

## Status

Local validation complete at `499b15f97eb0a469b7cd1308fbba7af3c64d1851`. Independent review pending.

## Description

Adopt processor `16be6768`, including descriptor body/key refusal from `493e5e4b`.
Record the new ROM digests while retaining earlier rows, classify the packer unit
test, update the F7 ownership record and pin references, regenerate the boundary
diagram, and refresh the capture receipt's processor pin.

## How to reproduce

Generate all five shipping configurations at `870ff88a` and `16be6768`, then pack
their AEM overlays with a 576-byte line limit. The five images and all 50 builder
output files are byte-identical. The handoff includes per-file sizes and hashes.

## How to validate

All assigned gates returned zero: the full builder bank in both compiler modes,
ROM digests, capture receipt, test evidence, port contracts, default wrapper and
datapath suites, documentation, and whitespace checks. Both builder modes ran
all 86 top-level tests in the normal order. The existing calibration arm lacks
its external report; absent mode additionally marks compiler-dependent checks
as not run.

The capture checker does not use the recorded pin as a measured input.
Its census, clocks, firmware and harness hashes remain valid. The retained
8x8 maximum is 24.30246 ms; no remeasurement was required.

## DoD

- [x] Adopted pin and accompanying records updated.
- [x] Five-configuration output equality measured.
- [x] Assigned local gates complete.
- [ ] Independent review complete.

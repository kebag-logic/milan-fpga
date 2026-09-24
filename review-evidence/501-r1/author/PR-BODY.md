[A282]

## Status

Local implementation prepared on `501-outmap-record` for `dev`.
Required local validation commands completed successfully, with the calibration
skip disclosed below. Independent review remains pending.

## Linked Issue / roles

Closes #501
Relates to #70 and #500.

Executor: [A282]. Internal reviewer: [R312]. External reviewer: [R313].

## Description

At 8x8, accepted output fan-out can exceed nine mapping entries.
Dynamic output records now derive capacity from stream/channel keys.
Each port receives `9 * 8 = 72` entries: 576 payload bytes.
Firmware programs the existing per-port backend tables with those lengths.
The complete journal grows by 4,032 bytes to 12,680 bytes.
The record count remains 156, with highest ID `0xE2`.
The complete 1x1 journal remains byte-identical to the base.

The gate retains its image-and-readback checks and adds two controls.
Old output lengths and a changed 1x1 digest each require refusal.
Tests also cover full-span backend operations and capacity boundaries.
The saved-state documents record the allocation and donor adoption requirement.

## Authoritative references

- Issue #501's frozen assignment and 2026-09-23 decision.
- `REQUIREMENTS.md` section 1; Milan v1.2 section 5.3.10.1.
- `docs/design/SAVED_STATE_FASTCONNECT.md` sections 4.2, 4.3 and 6.1.
- `docs/design/SAVED_STATE_MATERIALIZATION.md`.

## How to get into the same state

Base: `573f0052a0e4412e81f0845438fcec2086ce5d55`.
Candidate: `b5ee412cdc0fd771d3df1f7fda49031409cf11fa`.
Use the recorded submodule pins and repository dependencies.

## How to validate

Run the record-space gate and its self-test, backend suite,
firmware writer checks, builder regression, and default datapath sweep.
Run the documentation, source-list, traceability and idiom gates.
Expected: every positive gate exits zero; planted defects are detected.

## Known limitations / out of scope

The processor writer remains processor #61/#83 work.
No donor or synthesizable RTL changes are included.
The existing backend tables already hold the larger lengths.
Area measurement is therefore inapplicable to this parent change.

The builder regression exits zero, but its physical calibration arm reports
NOT RUN because the required existing utilization report is absent.

D3 evidence replays K16 and both capacity boundaries from cleared maps.
The product permits 64 audio keys at the current 8x8 shape.
The 72-slot storage test uses a synthetic final stream format.
That case proves record capacity, not new command-time mapping permission.
Hardware persistence acceptance remains with #70.

## Definition of Done

- [x] Parent scope items 1-6 implemented and documented.
- [x] Changed behavior has self-checking tests.
- [x] Required local commands complete; calibration skip disclosed.
- [ ] Self-test evidence posted with the future PR.
- [ ] Independent internal and external reviews positive.
- [ ] Reviewer-owned lens ledger accepted.
- [ ] Hosted checks and candidate merge validation complete.
- [ ] Merge authorized and post-merge containment complete.

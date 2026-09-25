2026-09-25T00:19:52Z
[A292]

## Status

Round 4 correction is committed locally on `501-outmap-record` for `dev`.
Every assigned Round 4 gate passes. Earlier validation limits remain below.
Round 4 delta reviews from [R312] and [R313] remain pending.

## Round 4

Removed the single sentence assigning capture-hold measurement to processor #61/#83.
Stage-3 release does not depend on that measurement.
[Issue #559](https://github.com/kebag-logic/milan-fpga/issues/559) owns measurement and resolution.
Every other repository line remains unchanged, including capacity-adoption requirements.
Both unchanged reviewer scripts return zero with no capture-hold ownership residue.
The text check retains only the capacity reference at `FASTCONNECT:457`.
The [Round 4 assignment](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5824399821)
explicitly requires preserving that line.

## Round 3

Section 18 and UNRESOLVED 6 now describe the current capture.
Every CLOSED record is copied, whether materialized or not.
RELOAD closes every allocated record. At 8x8, the copy spans 12,634 bytes
across 156 records, including 4,672 output-map bytes.
The doubled-cost model gives 63.8 ms against 50 ms: 0.78x today.
[Issue #559](https://github.com/kebag-logic/milan-fpga/issues/559) owns measurement
and resolution under the [corrected decision](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5824117439).
Void and retry preserve safety; shipping 1x1 remains unchanged.
Both reviewers' unchanged capture and hold probes reproduce their archived results.
Only these two documentation passages change in Round 3.

## Round 2

The writer contract now uses the derived output entry capacity.
Current image, deadline, memory, and copy-budget figures agree with the gate.
At 8x8, copying takes 31.9 ms nominally and 63.8 ms at doubled costs;
the 50 ms hold has 1.57x and 0.78x margins respectively.
The corrected decision keeps the hold unchanged; #559 owns measurement
and resolution of the existing copy. Shipping 1x1 is unchanged.
Void and retry preserve safety; sustained activity risks liveness at 8x8.

Every self-test control now requires its named finding and rejects tracebacks.
The unchanged reviewer crash probe makes `--self-test` exit 1 as required.
The unchanged figure comparison passes; both hold probes reproduce the margins.
The unreachable cleared-store guard is removed. `nvm_cosim` is identified as
the check that detects a wrong firmware output-length table.

References: [assignment](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5823589125),
[corrected capture-hold decision](https://github.com/kebag-logic/milan-fpga/issues/501#issuecomment-5824117439),
and `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18 / UNRESOLVED 6.

## Linked Issue / roles

Closes #501
Relates to #70 and #500.

Executor: [A292]. Internal reviewer: [R312]. External reviewer: [R313].

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
Candidate: `efcabc379b1e0be1366bfc05bdcc05a759b55616`.
Use the recorded submodule pins and repository dependencies.

## How to validate

For Round 4, run the record-space gate and its self-test, both documentation
modes, em-dash checks against `573f0052a0e4412e81f0845438fcec2086ce5d55`,
style, TOC, path and whitespace checks. All return zero.
Run the unchanged `r3_text_check.py` with its archived Round 3 input receipts,
and the unchanged `residual_search.sh`. Both return zero.
The text check passes 23 required and 14 forbidden-text checks.
Neither script finds a capture-hold obligation assigned to the donor.
The remaining capacity-only reference is preserved as assigned.

For Round 3, run the record-space gate and its self-test, both documentation
modes, em-dash checks against `573f0052a0e4412e81f0845438fcec2086ce5d55`,
style, TOC, path and whitespace checks. All return zero.
Run both reviewers' unchanged `capture_copy_probe.py` and `hold_margin.py`;
all four return zero and match the archived outputs.
The no-metadata documentation mode omits inventory parity as designed.
Capture times remain modelled; #559 owns their measurement and resolution.

For Round 2, run the record-space gate and its self-test, backend and
`nvm_cosim` suites, firmware writer checks with and without self-test,
builder regression, both documentation modes, and style, TOC, path,
traceability, and idiom gates. Run the unchanged reviewer probes.
The default datapath sweep remains Round 1 evidence at `b5ee412c`.
Expected: every positive gate exits zero; planted defects are detected.

## Known limitations / out of scope

The processor writer remains processor #61/#83 work.
No donor or synthesizable RTL changes are included.
The existing backend tables already hold the larger lengths.
Area measurement is therefore inapplicable to this parent change.

The builder reports exactly one NOT RUN arm: gate 11 physical calibration,
because its required existing utilization report is absent. The RV32
compiled census and available elaboration arms executed successfully.

D3 evidence replays K16 and both capacity boundaries from cleared maps.
The product permits 64 audio keys at the current 8x8 shape.
The 72-slot storage test uses a synthetic final stream format.
That case proves record capacity, not new command-time mapping permission.
Hardware persistence acceptance remains with #70.

## Definition of Done

- [x] Parent scope items 1-6 implemented and documented.
- [x] Changed behavior has self-checking tests.
- [x] Required local commands complete; calibration skip disclosed.
- [ ] Round 2, Round 3 and Round 4 evidence copied from #501 into this PR.
- [ ] Independent internal and external reviews positive.
- [ ] Reviewer-owned lens ledger accepted.
- [ ] Hosted checks and candidate merge validation complete.
- [ ] Merge authorized and post-merge containment complete.


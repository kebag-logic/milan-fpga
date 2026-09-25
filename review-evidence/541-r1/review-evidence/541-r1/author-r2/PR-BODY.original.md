[A304] Document and test CRF validation-error lock retention

Closes #541

## Status

Local author work complete; all assigned gates pass. Independent review pending.

## Description

The receiver header and CRF_CTRL row incorrectly claimed that a validation
error clears lock. They now describe the existing 100 ms timeout and the
UNSUPPORTED_FORMAT observation-interval count, including its full-width
output and truncated CRF_STATUS view. Synthesizable behavior is unchanged.

Milan v1.2 Section 5.3.8.10 / Table 5.6 leaves synchronization criteria to
the manufacturer. Sections 7.3.2-7.3.4 define the CRF profile without
requiring immediate unlock on a format error. IEEE 1722-2016 Clause 10.6
describes free-wheeling through packet loss. The 100 ms duration is the
existing implementation policy. The clause evidence is recorded on #541.

## How to reproduce

Lock a bound, started CRF sink with valid PDUs, then deliver a matching
PDU whose type violates the audio-sample profile. Lock stays asserted;
UNSUPPORTED_FORMAT increments once when the observation interval closes.
Valid traffic resumes without another lock event. Silence still unlocks.

## How to validate

The receiver suite adds direct public-output assertions for that sequence,
including lock on the rejection edge, lock through the counter commit,
exactly one format count, no accepted-frame count, no lock/unlock event,
and timeout behavior on either side of 100 ms. Its campaign rebuilds a
mutant that clears lock on format rejection and requires the named failure.
The existing discontinuity and connected servo cases remain enabled.

All 16 assigned gate invocations returned zero. The mutation campaign
passed nine controls, including the new mutant's required named failure.
Reproducible results are recorded in the author handoff on #541.

## DoD

- [x] Clause checked and the conditional stop requirement evaluated.
- [x] Header and CRF_CTRL row match existing behavior.
- [x] Locked-sink rejection and timeout checks added.
- [x] Named unlock-on-error mutant added.
- [x] All assigned local gates pass.
- [ ] Independent review completed.

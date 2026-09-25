[A306]

Document and test CRF validation-error lock retention

Closes #541

## Status

Round 2 author work complete; all assigned local gates pass. Independent re-review pending.

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
Validation errors arriving every 2 ms also allow the 100 ms timeout to
expire after the last accepted PDU.

## How to validate

The receiver suite adds direct public-output assertions for that sequence,
including lock on the rejection edge, lock through the counter commit,
exactly one format count, no accepted-frame count, no lock/unlock event,
and timeout behavior on either side of 100 ms. Its campaign rebuilds a
mutant that clears lock on format rejection and requires the named failure.
The existing discontinuity and connected servo cases remain enabled.

All 16 assigned gate invocations returned zero. The mutation campaign
passed ten controls, including both validation-error mutants' required
named failures.
Reproducible results are recorded in the author handoff on #541.

## DoD

- [x] Clause checked and the conditional stop requirement evaluated.
- [x] Header and CRF_CTRL row match existing behavior.
- [x] Locked-sink rejection and timeout checks added.
- [x] Named unlock-on-error and refresh-on-error mutants added.
- [x] Both unchanged reviewer refresh mutants detected.
- [x] Testing index and evidence description name both mutants.
- [x] All assigned local gates pass.
- [ ] Independent review completed.

## Round 2

Addresses R322-1 F1, R323-1 F1, and the assigned R323-1 F2 documentation
update. The decision, RTL, receiver header and CRF_CTRL text are unchanged.

A locked sink receives only matched, wrong-type PDUs every 2 ms. The check
requires lock to remain through 99.96 ms, clear by 100.06 ms, and score
exactly one MEDIA_UNLOCKED. Rejections continue through 200.06 ms; the sink
must stay unlocked without another unlock or lock event.

The campaign adds `validation_error_refreshes_timeout`, which must fail
`reject stream cannot refresh the 100 ms timeout`. Both published reviewer
mutants, `P2_error_refreshes_timeout` and `uf_refreshes_timeout`, were run
unchanged against this head and are DETECTED by that same check. Their
clean controls pass.

The testing index names `validation_error_unlocks` and
`validation_error_refreshes_timeout`; the evidence description agrees.
The receiver results are 13,836 unit checks, 2,201 discontinuity checks,
69 connected talker-step checks and ten mutation controls, all passing.
The servo results are 85 unit, eight playback and 113 PHC-step checks,
all passing. All 16 assigned gate invocations returned zero, including
both documentation modes. Detailed receipts are in the author handoff.

Local round-2 head: `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c`.
Publication and independent re-review remain pending.

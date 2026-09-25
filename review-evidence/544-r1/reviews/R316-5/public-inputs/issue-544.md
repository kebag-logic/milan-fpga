[A10] Recorded at the request of R272-1 and R273-1 (PR #535, #408/#409); pre-existing on dev.

## Observed
A plain function-like macro that overwrites the CSR identity sample inside the boot path is accepted by gate 1b both with and without the pinned RV32 compiler. PR #535 states it as a bound of the gate. R273-S3 (the verifier group's #else deleted) is related and also unchanged.

## Authority
AGENTS.md boot contract; docs/integration/BAREMETAL_FIRMWARE.md gate 1b (identity sample and mismatch guard); #408/#409 acceptance 4 (no reduction), which this issue does not reopen.

## Acceptance
1. A hostile firmware whose function-like macro overwrites the identity sample before its mismatch guard is refused, with the compiler and without it (or stated as NOT RUN without it).
2. The refusal names the rule; a control fails when the new check is removed.
3. Gate 1b and the builder tests pass; the BAREMETAL_FIRMWARE cost table names the instrument.

Hot files: sw/builder/test_builder.py and BAREMETAL_FIRMWARE.md are held by #408/#409 until PR #535 merges. Backlog.

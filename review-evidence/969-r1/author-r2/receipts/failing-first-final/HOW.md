# Failing first at the final head: round 2's regression tests and both reviewers' probes

Two clean clones of `f863258d` (PR #971's reviewed head), each with this round's final `srp_mbx.cpp` (`ecd5bf41`), the external round's
probe file as `review_probes.cpp` (it includes `srp_mbx.cpp`) and the internal round's `stale_count_probe.cpp`
appended to `srp_mbx.cpp`:

- `cnew-*`: the final adapter (`srp_mbx.c`, `srp_mbx.h` as at `f02d44cd` and since), the fix;
- `cold-*`: the adapter of `f863258d`.

Each log is one arm of the firmware harness (`srp_arms.arm_srp`) at 1x1 and 8x8, one and two interfaces:
`srp_mbx.cpp` filtered to `SrpEarlyTalker.*:SrpStaleCountProbe.*`, and `review_probes.cpp` to
`SrpEarlyTalker.Review*`.

With the fix every arm passes: 21 tests (18 `SrpEarlyTalker`, 3 `SrpStaleCountProbe`) and the 5 external probes.
At `f863258d` every arm fails on exactly the stale count: `AResetLeavesNoKeptRegistrationCounted`,
`AKeptRegistrationWhoseBlockIsFreedIsCountedNoMore`, `AKeptLeaveOfAStreamNeverRegisteredIsCountedNoMoreOnceFreed`,
`ZProbeResetThenOneReceiveOfEveryInput`, `ZProbeReclaimThenOneReceiveOfEveryInput`,
`ReviewResetRestoresFullAdmissionCapacity` and `ReviewFreedBelowBoundRestoresFullAdmissionCapacity`. The controls
pass at both: the fresh registrar (`OneReceiveOfEveryInputIsKeptWholeIntoAFreshRegistrar`, `ZProbeFresh...`,
`ReviewFreshFullBatchControl`), the flood, UNBIND_RX then BIND_RX, and the refresh counted once (`f863258d` lists a
kept registration, so it needs the plant `feedback-early-refresh-counted-again` to fail).

Probe sources (the reviewers' packets): `stale_count_probe.cpp` sha256 a64a4b8401b1aa6e05a499e65cf24193fae56bbf7a5bcdecb03cde0771aa68cc, 2063 B;
`probes.cpp` sha256 5c8880716d5f094f45d98fffac2258612507fb2a789a0b0dec014c70ff2e38c1, 3178 B.

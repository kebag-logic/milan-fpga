# Failing first, at the final head

The final head's tests (`4c5018eb`) built against the base's SRP adapter (`sw/firmware/ctrl/srp/srp_mbx.c` and
`srp_mbx.h` checked out from `dd163e41`), every other file at the head: `srp_mbx.cpp` at 1x1 and 8x8, one and two
interfaces, and `test_plat_sinks.cpp` (platsinks) at 8x8/1if and 1x1/1if. Each log is one arm of the firmware harness
(`srp_arms.arm_srp`, `plat_arms.arm_platsinks`). `../failing-first/` is the first such run, at `bd08d206`.

Failing at every arm: `SrpEarlyTalker` registration then binding on every input, rebind while bound, the latest of
two kinds, the JoinIn replacement, the bound, a kept registration that left, a full held table; the restated
`Srp.ReadyFailedAndUninterestingStreamsAreSeparated`; `Early.S13` and `Early.S14` at both shapes.

Passing at the base, as they should: binding then registration (the order that always worked), a registration that
ended before the binding, an unbinding's registration bound again (the issue's UNBIND_RX then BIND_RX control), and
the count past the bound (vacuous at the base, which keeps nothing).

[A279]

Closes #548

## Status

Ready for independent review at `e41703b2948ef53e5cb0dd01a1e13c5632637615`. All assigned local gates pass.

## Description

`CTLR_DIAG` at `0x6F4` always reads zero, but its documentation described live probe, reply and eviction counts. Mark it **STRUCTURAL ZERO** in the register row, explanatory paragraph, group gloss and RTL comments. The departing-controller monitor lives in the protocol processor and exports no count for this word.

Correct the #117 evidence page: the DUT answered registration and deregistration with SUCCESS, while the zero diagnostic cannot establish controller presence or eviction. Add one AXI-Lite assertion after the timed notification leg proves controller probes, retry and eviction. Functional RTL is unchanged.

## How to reproduce

Run `make -C tb/verilator/milan_dp`. The timed notification leg reads `0` at `0x6F4` after controller traffic.

## How to validate

The focused leg passes all 147 checks. Replacing only the diagnostic tie with `32'h01001001` in a temporary source makes the same leg exit 1: exactly the new zero check fails. The mutation campaign returns 0. This leg has no existing mutant runner.

The complete default integration sweep passes, including its existing render mutations. Both documentation inventory modes, documentation style, contents, paths, traceability, RTL analysis, source lists, language idioms, committed em-dash and diff checks return 0. RTL analysis matches its existing ratchet.

## DoD

- [x] Apply the recorded STRUCTURAL ZERO decision.
- [x] Correct current documentation and RTL comments.
- [x] Pin the CSR behavior and demonstrate the failing mutation.
- [x] Complete all assigned local gates.
- [ ] Independent review.

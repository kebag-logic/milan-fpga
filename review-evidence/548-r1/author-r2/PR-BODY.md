[A285]

Closes #548

## Status

Ready for delta review at `8544472a19a4b4d3853d64b15dea22f999372a32`. All assigned Round 2 local gates pass.

## Round 2

Correct both remaining live-count comments in the CSR address table and read mux (R308-1 F1 and R309-1 F1). Both now state STRUCTURAL ZERO, the deleted counter source, processor ownership and ABI retention. Preserve the reserved-word note.

The current-tree search finds no remaining live-count claim for this word. All 137 tracked RTL files remain comment-free identical to the base. All assigned Round 2 gates return 0. The behavioral results below are retained Round 1 evidence; delta reviews are pending.

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

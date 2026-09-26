[A337] REVIEW READY
Commit: `0a506fa8f0032d21e9614a617b75b0a57dc5f2e4` (local and unpushed), branch `231-pp-shadow-baseline`.

All five items in the round-two assignment are addressed; independent re-review remains pending. No RTL or donor files changed.

- Separate boundary-preserving attribution retains the default whole-design fit baseline. Wrapper LUTs, default / attribution: 23,272 / 22,314 at 1x1 synthesis; 22,441 / 20,655 at 1x1 route; 37,809 / 29,489 at 8x8 synthesis.
- The unchanged public boundary/load probes return rc 0 at all three attribution endpoints. At 8x8, dynamic-state raw LUT cells fall from 8,817 to 607, and cells with only external loads fall from 5,922 to zero. The load histograms are empty at all three attribution endpoints. Remaining wrapper-level external loads and the probe's reverse-relocation limit are documented.
- Complete LUT and FF rankings contain 328 rows across eight endpoints, with zero threshold, own logic and reconciled parent totals. Timing subsets are labelled.
- Equivalent-geometry hierarchical mapping identifies the dominant raw logic differences. Disjoint contributions plus the flattening residual reconcile the 16,317 / 33,374 raw LUT gaps exactly.
- Real preparation, inventory and CLI self-tests pass. All ten maintained enforcement-removal mutants fail; the original public mutant driver also kills all five mutants. The clean-export path gate passes with builder output absent.

Validation: both full `python3 sw/builder/test_builder.py` modes return rc 0 (verified pinned SDK and target compiler absent); both `python3 -B scripts/docs_check.py` CI modes return rc 0. Every other requested gate returns rc 0: firmware self-test, NVM capture, baremetal check, event-contract check/self-test, em-dash check against `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`, document style, TOC check/anchors, document paths, module matrix, HDL front end/source lists/idioms/lint, C++/Python idioms, port contracts, naming, test evidence, Behave and `git diff --check`.

Evidence limits: both builder modes lack the historical calibration report; compiler-absent mode additionally skips the target compiled CSR census. The SDK run records 855 compiler invocations. Existing timing-constraint limitations remain documented. The attribution 1x1 route has final setup/hold slack +0.041/+0.015 ns and no failing setup, hold or pulse-width endpoints. Boundary preservation adds three DSPs in the 8x8 NVM scope; attribution totals remain separate from default results.

`HANDOFF.md` contains file:line changes, the default/attribution comparison, complete ranking, mutant table and gate table. `PR-BODY.md` preserves the current PR body with a Round 2 update. The prepared PR body has not been applied; no push or merge was performed.

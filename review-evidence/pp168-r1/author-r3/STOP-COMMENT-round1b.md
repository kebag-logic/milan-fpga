[A567] STOP

Head: `ba3f3f31e8fda01c3ef5271ff8005f3cf92ab4de`.

The six assigned corrections and clause-based checks are committed locally. All 33 processor suites, the five processor gates, all 13 affected campaigns at base and head, and all 17 scratch-parent consumer commands return 0. All 18 added planted defects fail their named checks. The historical parent report-calibration arm remains unrun at both revisions because its required report is absent.

The isolated 1x1 comparison is 21,442 → 21,620 LUT (+178) and 18,890 → 18,908 FF (+18). The LUT increase exceeds the +40 limit, so acceptance is unmet and REVIEW READY is unavailable.

HANDOFF.md and PR-BODY.md are updated with clauses, expectation changes, failing mutants, record comparisons, parent results and area evidence. The processor tree is clean. No push, PR operation, parent commit, top-level port/parameter change or register-map change was made.

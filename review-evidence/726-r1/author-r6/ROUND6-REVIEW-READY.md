[A605] REVIEW READY

Round 6 local head: `12f00129349c889e6dbbb7de11529ab38c9d164d`.
New commits: `3bf3dbaafa14ced2cc1d36a580cab698e2fb50d0` and `12f00129349c889e6dbbb7de11529ab38c9d164d`. No push.

R628-5-F1: every consecutive gap and final wait is graded against the fixed 1025 ms limit from ruling 6134121887. The 25 ms service allowance cannot be enlarged by the run. Per-descriptor measured service is retained for information only. Spacing and start-shift invariance remain checked.

The standing 900 ms parent-egress stall runs at both shapes: 8/36 CADENCE failures, then clean escapes with CADENCE alone omitted. The unchanged review probes (`sched-1600`, `sched-2000`, `egress-stall`) each fail only CADENCE at both shapes and pass omission controls. Previously published escapes reached 1601.867, 2012.027 and 1900.660/1900.632 ms; the new grade rejects them.

R628-5-R1 through R6 and R629-5-R01 are applied. Counter comments distinguish packet totals from six anomaly intervals, both clause tags are consistent, and the proposed PR body identifies the published Round 5 head separately from this local head. No assertion or production logic changed in those corrections.

Validation: all final applicable drivers return 0. The recursive counters target prints all four RESULT: PASS lines; fifteen standing mutation/omission pairs and six unchanged review-probe pairs pass. Receive and CRF regressions and their mutation campaigns pass. Behavior: 406 scenarios / 1,977 steps; grader: 80 tests. Source inventories, strict closure and its 50-case self-test, lint, naming/evidence/language gates, all five documentation gates, capture guard and committed-range whitespace checks pass. Budgets are unchanged.

| Shape | Consecutive gaps per corrected condition | Minimum | Maximum | Measured service maximum |
|---|---:|---:|---:|---:|
| Shipping | 28 | 1001.000 ms | 1001.867 ms | 3.263 ms |
| Largest | 126 | 1000.982 ms | 1012.029 ms | 14.058 ms |

Every corrected descriptor/recipient row meets the fixed bound. Frames-only output TU/MR counters and wire bits stay zero. Baseline controls reproduce 12/54 named failures. Mailbox gaps remain 1000-1002 ms under their stricter 1003 ms fixture ceiling. These are finite compressed-time measurements with two recipients.

Production RTL and firmware implementation are unchanged. Non-comment image inputs match the retained routed measurement: 49,427 LUT (+35 against dev c6bd08c6's 49,392), 53,378 FF, 87.5 BRAM; constrained WNS/WHS +0.451/+0.036 ns. No image or capture remeasurement was triggered and no STOP condition arose.

HANDOFF.md and PR-BODY.md contain the Round 6 response, file/line changes, exact gate ledger, named plants and omission escapes, 660 per-second rows, 132 gap rows, per-descriptor service, and artifact sizes/hashes. Sampled service memory peaked at 6,539,780,096 bytes, below 9 GB, with no OOM events. All lane-owned jobs finished; worktree and initialized submodules are clean.

Independent re-review, authorized publication with the trusted current-dev workflow replica before hosted inspection, current-dev candidate validation and merge-turn physical cadence/reference-peer reset/controller-display acceptance remain required. Relates to #726; complete acceptance is not claimed. No push, PR edit, rebase, amend, merge, submodule edit, existing-comment edit or physical action occurred.

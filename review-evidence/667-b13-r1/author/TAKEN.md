[A549] TAKEN

Branch: `667-b13-bench`, base `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`.
Executor: [A549]. Reviewers: [R510] internal and [R511] external.
Authoritative references: the B13 assignment above; REQUIREMENTS.md; IEEE 1722-2016; IEEE 1722.1-2021; Milan v1.2; B12 evidence and PR #666.
Interpreted scope: findings-only measurements on the assigned dev `28f9666f` image. Verify identity, record as-found state, run the two-hour bidirectional AAF/CRF soak with periodic counters and rolling captures, then 100 two-second DUT talker binds. Apply the listener-format rule before every bind. Stop on identity mismatch or soak error-class increase, retain the trace, and restore every changed control with readback.
Validation plan: bounded foreground bench actions under the shared lock; independently decoded startup headers and per-cycle counter tables; the seven assigned documentation and whitespace gates. Local commit only.
Blockers: none established; identity gate pending.

[A383] TAKEN
Branch: `602-phc-step-mr`, base `6d5ebd7357c1e468e446f18a61527c5be6118a04`.
Authoritative references: #602 ruling 5859297355 and assignment 5859299480; #387 decisions as partially superseded.
Interpreted scope: remove only the PHC re-base restart contribution, preserve render re-base and tu, add simulation controls and mutation evidence, update the named documentation, and measure both datapath shapes. Executor [A383]; reviewers [R366] and [R367].
Validation plan: assigned restart/CRF/gmstep suites and mutants; RTL lint; datapath ooc synthesis before/after at AX 1x1 and 8x8; full ci_scope self-test bank; baremetal-only and docs checks; five-configuration artifact identity; git diff --check. Gates will run at the committed head.
Blockers: none. Delivery is local commits and review artifacts under the assignment restrictions.

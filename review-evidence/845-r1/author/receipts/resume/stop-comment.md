[A738] STOP
Head: d8e95dd992d1ffe8dff0127a9c1f88c5813a19a9
The resumed receipt audit found an existing failure: make -C tb/verilator/milan_dp unb-mutants exited 2, reporting 6 checks: 5 PASS, 1 FAIL. The first planted arm matches zero occurrences in protocol_processor_top.sv instead of one; the diagnostic states that the mutant is no longer mutating anything. The release instruction accepts no failure, including a failure that predates this adoption. No test was weakened and no unrelated repair was made.
The stored passing sweep and other gates cover 0d9c942e, not this head. The stored shipping route covers a29a7411; an exact-current-head repeat is not evidenced. The docs workflow record includes 24 skipped steps. Current-head acceptance is therefore incomplete.
HANDOFF.md and the local PR draft now state STOP/BLOCKED and do not claim closure. The branch is clean; no push or PR action was taken. The existing TAKEN comment was not duplicated.

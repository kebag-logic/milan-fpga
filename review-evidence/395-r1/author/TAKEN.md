[A387] TAKEN
Branch: `395-timing-grade`, base `8bc97021f28fb7f729418d3a00851c84ea0b50fd`.
Authoritative references: #395 owner decision of 2026-09-23 and assignment; REQ-VER-02/05; BUILDING section 5, RUNNING_TESTS section 5 and LITEX_SOC section 7.
Interpreted scope: items 1, 2 and 5. Declare commercial-grade conditions once, derive candidate analysis from them, pin the declaration in builder validation, and report the read-only shipping checkpoint at the supported process/temperature corners. Report negative slack with paths; items 3 and 4 and timing fixes remain outside this lane.
Validation plan: full builder bank in both compiler modes, CI scope self-test, documentation gates and diff whitespace check, all at the committed head; record each timing-analysis exit code and report summaries.
Executor: [A387]. Independent reviewers: [R372] and [R373].
Blockers: none identified during initial checkout and public-scope verification.

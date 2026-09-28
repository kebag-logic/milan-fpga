[A393] TAKEN
Branch: `395-timing-grade`, starting head `3a0cb4cf4fed2d71436a43f4b96cb375f9178342`.
Authoritative references: #395 owner decision, margin decision and correction, round-3 assignment 5860820812; both round-2 reviews on PR #605; #607; REQ-VER-02/05.
Interpreted scope: answer the round-2 bare-metal gate blocker and accepted S1-S4, including the retained findings-index suggestion. Preserve crossing meaning, identify both generic false-path classes and endpoints, run the PLL test from the standalone entry, align the margin and manual-seed wording, and publish the crossing-evidence locator. Items 3 and 4 stay open; no timing or constraint fix.
Validation plan: full builder bank in both compiler modes with required elaboration, CI scope self-test, documentation gates including bare-metal check/self-test, Python idiom gates and diff whitespace checks, all at the committed head. Retain exact commands, exit codes and limits.
Executor: [A393]. Independent reviewers: [R372] and [R373].
Blockers: none.

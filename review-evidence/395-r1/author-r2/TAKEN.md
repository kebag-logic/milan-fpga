[A390] TAKEN
Branch: `395-timing-grade`, starting head `66001a307ce5de57577e66d6e3a18b9f4020764b`.
Authoritative references: #395 owner decision, margin decision and round-2 assignment; both round-1 reviews on PR #605; #607; REQ-VER-02/05 and the timing documentation.
Interpreted scope: answer R372-1 F1/F2/F3 and R373-1 F1/S2 for items 1, 2 and 5. Record rejected crossing constraints, retained warning census and measured intended-bound slack; strengthen planted-fault tests; apply WNS >= +0.03 ns and WHS >= 0; derive PLL speed grade from the shared declaration. Items 3 and 4 remain open. No timing or constraint fix.
Validation plan: full builder bank in both compiler modes, CI scope self-test, documentation gates and diff whitespace check, all at the committed head; record timing-analysis exit codes and logs and each required planted fault.
Executor: [A390]. Independent reviewers: [R372] and [R373].
Blockers: none.

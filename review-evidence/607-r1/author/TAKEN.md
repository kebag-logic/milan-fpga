[A408] TAKEN
Branch: `607-xdc-clock-names`, base `54ce877371ee6e8878cf67294e86c2a8481b62f6`.
Authoritative references: #607 assignment and acceptance 1-4; linked #605 F1 findings; #395 margin decision; REQ-VER-02/03/04 and the integration/testing documentation.
Interpreted scope: derive constraints from clock objects, make the intended Ethernet crossing bound effective, move unsupported XDC control flow into a supported hook, fail shipping builds on implementation-log warnings 12-4739 and 20-1307, and validate a fresh AX7101 1x1 TDM8 sweep with at most 16 threads. No RTL, firmware or installed-package edits.
Validation plan: full builder bank set and documentation gates at the committed head; planted wrong-clock-name refusal; per-seed timing, crossing-bound and clock-interaction reports against WNS >= +0.03 ns and WHS >= 0.
Executor: [A408]. Independent reviewers: [R382] and [R383], as assigned.
Blockers: none identified. The assignment settles scope; the project card currently still reads Backlog.

[A368] TAKEN - round 2
Branch: `580-pp-pin-16be6768`, starting head `499b15f97eb0a469b7cd1308fbba7af3c64d1851`.
Executor: [A368]. Independent reviewers: [R352] and [R353].
Authoritative references: this issue and every [A10] scope comment, especially the round-2 decision; R352-1 F1/S1/S2 and R353-1 S1/S2; capture README and snapshot ownership section 18; REQ-VER-03/04.
Interpreted scope: remeasure all six capture points at the adopted processor pin with 16 captures each, refresh receipt provenance and section 18, and make the assigned documentation corrections. The 24.5 ms 8x8 STOP condition applies before proceeding. Firmware, RTL and the gate remain unchanged.
Validation plan: new receipt check; full builder bank with compiler present and absent; OOC ROM digest check; test-evidence and port-contract checks; pp_shadow and milan_dp default suites; documentation gates and whitespace checks. Commands run in the physical lane, in the foreground. Local commit and handoff only; no push or PR edits.
Blockers: none identified; checking offline measurement prerequisites.

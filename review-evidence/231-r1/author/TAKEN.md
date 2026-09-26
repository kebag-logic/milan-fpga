[A328] TAKEN
Branch: `231-pp-shadow-baseline`, base `7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a`.
Authoritative references: #231 assignment decision, #229, REQUIREMENTS.md, AREA_BUDGET.md, BUILDING.md and the repository synthesis recipes.
Interpreted scope: measurement only, with standalone Vivado 1x1/8x8 at 100 MHz, integrated shipping 1x1 placement/routing and integrated 8x8 synthesis, equivalent-geometry Yosys, and a committed reproducible baseline. Historical substitution measurements remain explicitly historical. No RTL changes.
Reviewers: [R332] internal; [R333] external, as assigned.
Validation plan: verify every ROM input and reject Synth 8-4445; record hierarchy and timing with exact geometry and synthesis options; run the full requested builder, firmware, documentation, style, source, lint and behavior gate set.
Blockers: none. The assignment marks the issue Ready; the stale Backlog card is now In progress. Existing branch and initialized submodules retained. No push or PR actions in this assignment.

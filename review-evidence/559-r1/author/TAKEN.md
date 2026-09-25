[A307] TAKEN

Branch: `559-capture-copy`, base `a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4`.
Executor: [A307]. Independent reviewers: [R324] internal and [R325] external.
Authoritative references: this issue's assignment, PR #557 R312-2 and its public capture-copy probe, REQUIREMENTS section 1, SAVED_STATE_SNAPSHOT_OWNERSHIP sections 5, 7, 18 and 20.

Interpreted scope: establish the product CPU simulation route first. Measure the full firmware record walk and closed-record copy at both shapes, including repeated 8x8 captures under controller traffic. Apply the assigned remedy order against the half-hold bar, then update section 18 and UNRESOLVED 6. If the product CPU route cannot run with the installed environment, stop and report here.

Validation plan: the assigned builder runs with the pinned SDK and without a compiler; focused NVM co-simulation, backend and host suites; bare-metal, documentation, traceability, idiom, port, naming and evidence gates; whitespace checks; OOC if RTL changes. No push, PR mutation, merge, other checkout, hardware, donor edit, download or delegated work.

Route preflight: offline CPU metadata generation, cacheless RV32I netlist elaboration, BIOS compilation with the pinned SDK, and simulator compilation succeed. CPU execution has reached DDR initialization. These are prerequisite checks, not capture timing measurements.

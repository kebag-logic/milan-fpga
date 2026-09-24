[A259] REVIEW READY

Head: `73a5478784bd861f8c8d33c0d1619594390b9529` (local branch `112-stale-grant`, base `939c143333d11e2378a514f1c7b6abd4c3259bfd`).

Current-declaration admission is implemented with no top-level port change. Cold/growing refused TSpecs never pulse a grant; shrink and identical declarations grant after 8/16/24 clocks at the default shape. Tests cover all phases and multiple sources; both stale-evaluation mutants fail.

All workflow gates pass (rc 0), including the full 33-suite bank: 739421 checks, 0 failures. Both assigned parent consumer checks pass at this head; the consumer suite has 371 checks, 0 failures. Default-shape SRP area is 7566 → 7334 LUTs and 10485 → 10464 registers, with RAM/DSP unchanged. Behaviour, latency, ACTIVE/window and slope sampling are documented.

HANDOFF.md and PR-BODY.md are prepared in the assigned output directory. No push, PR change, parent commit, merge or hardware action was performed.

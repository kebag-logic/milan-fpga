# Round 3 checks

Head: `cd659eb5e93c4da5e97fcbd6282b1efba16e565d`.

- All 17 published commands executed. Sixteen returned rc 0; the link checker returned rc 1.
- Sentences: rc 0; 760 prose units; zero over 25 words.
- References: rc 0; zero detected bare references. Self-test: rc 0; 79 cases.
- Links: 290 local occurrences; eight missing licence-file targets. Eighteen external URLs; six authenticated successes, eleven anonymous successes, one anonymous ISO HTTP 403.
- Graphs: rc 0; 22 renders; 2–11 nodes; all inspected; no unrelated-node crossings.
- Configured/direct/isolated unit runs: rc 0; nine tests and 1690 assertions.
- Scenarios: rc 0; three scenarios and ten steps. Dry run: rc 0; matching only.
- Wrong-disable probe: configure/build/scenarios rc 0; all three scenarios still pass.
- Identity, scope, whitespace, privacy, snapshot equality, and artifact audits pass.
- No push. No source/build/test changes.

See [HANDOFF.md](HANDOFF.md) for per-page coverage, per-graph inspection, complete command rc records, and verification limits.

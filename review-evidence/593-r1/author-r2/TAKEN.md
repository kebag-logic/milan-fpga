[A380] TAKEN
Branch: 593-mr-tu-soak at 95bea7cf82fcf7cf034c156ef7aa6800ee769e05.
Authoritative references: #593 round-2 assignment; #396 correction; #602; REQ-VER-06; TESTING 6d; Milan v1.2 Annex B.1.1/B.1.2 and Table 5.4; IEEE 1722-2016 4.4.4.3/4.4.4.7.
Interpreted scope: address the six required round-2 items and the two accepted suggestions in the planner, its self-tests, and documentation. Reviewers: [R362] and [R363].
Validation plan: replay both round-1 review packets, prove checks and assertion text with killed mutants, then run the planner self-test, builder scope self-test, bare-metal boundary, documentation gates, and git diff --check at the committed head.
Blockers: none. The PHC-step decision remains #602; the assigned owner rule applies meanwhile.

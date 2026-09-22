[A10] Closing fences now accept only trailing spaces or tabs, and any literal type-1 HTML closing tag ends the block using ASCII case folding. A malformed closer can no longer grant a copied Contents label to a hidden heading; valid cross-name closers expose their headings correctly. The existing character-refusal and container policies remain in force.

The change adds I440 controls and documents the CR normalization boundary. Author measurements compare the same 205 synthetic fixtures at base/head against GitHub gfm; normalized head agreement is 205/205, while 100 rows remain globally refused. All 163 tracked pages keep identical headings and generated Contents. Eleven deliberately weakened variants fail behavioral controls.

Closes #440.

Validation: author TOC 683/683, em-dash 51/51, paths/docs/idiom/source guards pass; 42 manager static, documentation, lint and Vivado parsing commands have passed. Full builder, parent/processor suites, Yosys, behave, trusted local replicas and hosted checks are in progress. This PR remains draft until the full required bar is ready. R225 internal Codex and R226 external Opus are assigned for cold review after the current donor review round. Standing maintainer merge authorization is recorded; two independent positives, clean five-lens coverage, candidate validation and post-merge containment remain required.

Evidence: https://github.com/kebag-logic/milan-fpga/tree/4d9e15fa501c279ecd871ca53e95c3fb6a354532/review-evidence/440-r1 . The historical sweep instrument was unavailable, so the author reconstructed its public population and published exact fixtures, HTML receipts, measurements and mutation definitions. Test evidence is not review approval.

[A172] Named mutation receipts

Exact source head `b5e6c23e1b9802b5cacbc62db212064d7e429862`. Source bytes preserved. All edits are isolated under mutants/.

| Mutant | Required failing property arms | TOC exit | Em-dash exit |
|---|---|---|---|
| tag-paragraph-reversion | R238 C01; R238 C04; R238 P01; R238 P04 | 1 | 2 |
| tag-column-too-narrow | resumed tag column 2 open; first tag column 2 open then fence | 1 | 2 |
| tag-column-ignored | resumed tag column 1 open; first tag column 1 open | 1 | 2 |
| quote-release-removed | R238 D01; R238 D03 | 1 | 2 |
| footnote-release-removed | R238 D02; R238 D04 | 1 | 2 |
| block-marker-only | R237 fenced-marker-indented-closer; R237 comment-marker-indented-closer; R237 HTML-marker-indented-closer | 1 | 2 |
| prior-drop-context | two spaces | 1 | 2 |
| prior-forget-on-blank | two spaces | 1 | 2 |
| prior-blanket-indent | one space outside item | 1 | 2 |
| prior-strict-column | two spaces | 1 | 2 |
| prior-fixed-column | ordered outside | 1 | 2 |
| prior-characters-not-columns | tab padding columns | 1 | 2 |
| prior-no-code-padding | code padding uses one | 1 | 2 |
| prior-four-is-code-padding | four padding columns | 1 | 2 |
| prior-empty-never-ends | empty item ends at blank | 1 | 2 |
| prior-empty-stays-empty | empty item gains content | 1 | 2 |
| prior-empty-uses-padding | empty item ignores padding | 1 | 2 |
| prior-lose-outer-column | nested item retains outer column | 1 | 2 |
| prior-stale-sibling-column | sibling replaces column | 1 | 2 |
| prior-stale-context | fresh dedented paragraph ends item | 1 | 2 |
| prior-no-lazy-hold | lazy line retains item | 1 | 2 |
| prior-markers-in-blocks | R237 fenced-marker-indented-closer; R237 comment-marker-indented-closer; R237 HTML-marker-indented-closer | 1 | 2 |
| prior-no-ordinal-interruption-check | noninterrupting ordinal is no item | 1 | 2 |

The narrow block-marker-only mutation fails exactly three arms in each consumer. Real-Git receipts independently report exactly the same three failed label decisions. Broader-mutant extra failures do not substitute for these names. Full exact replacements, command argv, source hashes and all failing lines are in mutations.json; complete logs and mutated sources are retained per mutant.

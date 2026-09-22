[A172] Per-finding response at `b5e6c23e1b9802b5cacbc62db212064d7e429862`

Every finding retains its reviewer-assigned severity and ALL lenses. Author evidence below is not reviewer-confirmed resolution.

| Finding | Severity | Original lenses | Author disposition |
|---|---|---|---|
| R237 F1 | MAJOR | Conformance / Robustness / Tests | Named counterexamples corrected; independent re-review required |
| R237 F2 | MAJOR | Conformance / Tests / Docs | OPEN: AC1 correspondence unproven |
| R237 F3 | MAJOR | Conformance / Tests | Observable controls added; independent re-review required |
| R238 F1 | MAJOR | Conformance / Robustness / Tests / Docs | Named counterexamples corrected; independent re-review required |
| R238 F2 | MAJOR | Conformance / Robustness / Tests / Docs | Named counterexamples corrected; independent re-review required |
| R238 F3 | SUGGESTION | Conformance / Robustness | NOT adopted; optional #495 follow-up, unchanged |

R237 F1 and R238 F1: the opener receives paragraph context only for a nonempty live item at or beyond its content column. Outside tags retain the intended type-7 opening. First/resumed paragraphs, zero-through-four tag columns, opening/closing/attribute forms, column-zero fences/comments/pre blocks, ordered/bullet/empty/lazy/sibling boundaries have measured fixtures. The 15 R237 public matrix pages and 17 R238 C/D/P counterexample/boundary pages are byte-identical to their public factual inputs (`public-input-preservation.json`). R238 P01 and P04 are now correct at the same mechanism: P01 returns Real rather than Old; P04 returns Old/Real rather than Real. Both are pre-existing at the original baseline. `tag-paragraph-reversion`, `tag-column-too-narrow` and `tag-column-ignored` fail their named arms in both consumers.

R238 F2: a dedented quote or footnote ends the item's stored context. A contained quote/footnote still keeps the outer item; blank, fresh-paragraph, heading, sibling and lazy boundaries remain tested. D01/D02 return Old/Real and permit copied labels; D03/D04 return Real and refuse copied labels. Independent quote/footnote release reversions each fail their own D rows. Source state commentary and CONTRIBUTING state the tested behavior and remaining limitations.

R237 F3: exact public fenced/comment/raw-HTML fixtures preserve the erroneous seeded item through a two-space closer. The narrow mutation `label == TEXT and after == HELD` to `label != TEXT or after == HELD` fails exactly R237 fenced-marker-indented-closer, comment-marker-indented-closer and HTML-marker-indented-closer in both selftests (exits 1/2). In `consumers-marker-mutant.json`, exactly these three real-Git cases lose their legitimate exemption, each for mirrors-no-heading, with no unrelated added-heading finding. The unmodified source passes them. Source bytes are unchanged by scratch mutations. The broader old marker mutant also fails these new arms; its additional thematic/ordinal failures are not substituted as evidence.

R237 F2: see HISTORICAL.md. No originating archive was recovered. The public report describes nine shapes and collectively names eleven IDs without an unambiguous per-ID association. No ID is silently assigned, no plus/custom probe replaces an original, and no equal-count argument is made. Fresh renderer, navigation and real-Git evidence validates nine reconstructions only. AC1 remains unproven; no acceptance-policy change was requested or taken. R238's differing assessment is not clearance of R237 F2.

Additional observation remains open: twelve outside-tag/unclosed-comment variants are wrong at the starting and corrected heads, and six resumed variants regress from the original base. This is distinct from the named contained-tag correction and is publicly recorded for manager decision in comment5778541581. It is not reviewer-reclassified or hidden under optional R238 F3. No all-escape-closed or whole-AC1-complete claim is made.

Full acceptance and review coverage remain the manager's and reviewers' decisions. This response supplies no POSITIVE verdict and clears no finding or lens.

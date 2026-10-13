[A603] REVIEW READY (B16, findings round 10)

Head: `f1b2489f5b1c929e81eeae79a469b2b27c47e340` on `629-b16-tone`, one new commit after `cb5ff79f`, with no rebase or amend. Not pushed. Refs #629.

Documents only under the [round 10 assignment](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6134101205), answering [R624-9](https://github.com/kebag-logic/milan-fpga/pull/725#issuecomment-6134093761). No bench action or bench-lock acquisition. Bench figures and verdicts are unchanged.

The checker now refuses a whole block at its first covered line when a node has no source start, except soft/hard breaks. It also renders each covered block with the pinned renderer and compares its visible digit multiset with the digits read. Missing starts on blocks and enclosing structures are refused too. The findings and index state these rules and their limits; the packet map adds round 9 at `author-r9/`, source `cb5ff79f`, evidence `4ab00ba5`, and names `author-r10/` for the manager's publication.

| Run | Result | Receipt |
|---|---|---|
| Unchanged page and index | 1,960/1,960 rows equal their receipts; 15,597 digits, 12,988 claimed by rows and 2,609 by identifiers; zero uncovered and zero blocks refused | `r10/figures-check.stdout`, rows and coverage TSVs |
| R624-9 unchanged probe | Original passes; all 14 altered cases exit 1, named or refused; no escape. Introduction refusals at line 18, index at README.md:15; later-line email refuses its paragraph, while positioned figures are named on their own line | `r10/r624-9-autolink-probe-rerun.json` |
| Standing controls | 117/117 PASS, including the 97 unchanged round 9 controls and 20 new controls | `controls/r10-controls.json` |
| New controls on round 9's checker/page | 97 earlier and 6 new controls pass; 14 new controls fail, proving defect detection | `controls/r10-controls-on-r9-check.json` |
| Earlier runners, unchanged | 5/5, 7/8, 21/22, 38/39, 48/50, 73/73, 97/97. Failures are only the manager-superseded diagnostics; these historical runners are not called wholly green | `controls/r10-rerun-r3-controls.json` through `r10-rerun-r9-controls.json`; [decision](https://github.com/kebag-logic/milan-fpga/issues/629#issuecomment-6132293481) |
| Parser audit | 37 earlier plus 22 position cases meet their expectations | `r10/parser-extents.json` |
| Parser-output mutations | 15/15: missing starts on inline, block and enclosing nodes; lost, duplicated and substituted digits | `r10/reader-controls.json` |
| Further forms | 172/172 meet expectations: 134 rejected, 38 stated passes | `r10/self-probes.json` |
| Earlier review probes | All 14 preserve probe hashes, exit statuses and outcomes. Only the appended footnote locator moves, from 4426 to 4604; its reference remains at 3011 | `r10/probe-comparison.json` |
| Reader compatibility | Round 10 reader with round 9 rows reproduces round 9's rows, coverage and output byte for byte | `r10/reader-on-r9.json` |
| Rebuild and row-key scan | Checker regenerates byte for byte; no unread variable in 547 row-key loops | `tools/r10_figures_build.py`, `r10/key-scan.json` |

R624-9-R1 is corrected in `PR-BODY.md`: the prior probes preserved exit statuses, verdicts and named lines, with the stated footnote movement; their complete bytes also contain changed summary counts and the check's hash. The manager's R625-9 corrections remain exactly “99.6 ms after the unbind command” and “line 4426”. The PR itself was not edited.

All 14 gate entries are rc 0 at this head, unpiped, from the physical worktree. Markdown commands used the assigned pinned environment:

- `docs_check.py`, `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_em_dash.py --base e8454e27`, `check_doc_paths.py`;
- `scripts/ci_scope.py --selftest`, `scripts/check_baremetal_only.py --check` and `--selftest`, `scripts/check_feature_status.py --self-test`;
- `git diff --check` and `git diff --check c20c85bd HEAD`, plus the two interpreter-version checks.

Evidence: `gates/r10/results.json` and individual logs. No RTL, firmware or repository tooling changed. The two changed files are the findings page and its index.

| Packet file | Bytes | SHA-256 |
|---|---|---|
| `tools/check_b16_figures.py` | 199,268 | `a9f36f9d9ff3bfd6c7f7ce86f64ef1ac9531f1cf594d68d3a06437f8e8d0e540` |
| `tools/r10_figures_spec.py` | 167,841 | `407817bdd7a516d297141a430f69c6b63f0c38c416da8b4b52c586c5e57a4816` |
| `tools/r10_figures_build.py` | 6,603 | `d2075750721d7acfbb475d66f0dc60b9141aabec2ae1d1cd6faf465331c47005` |
| `controls/r10-controls.json` | 42,065 | `fc38bcaac78dddda91f042ee2e5305d2d9a656780c2bffa2e5e7007507e5ce12` |
| `r10/figures-rows.tsv` | 132,519 | `ccaae4a09ddf0459b4e988fac6fe7b98253eb665b1a20b35cffc97072b2f91a1` |
| `r10/figures-coverage.tsv` | 90,016 | `f8cc3827506305db4996450b19fcc6dcb03f276036a0da3e6a0262aa698213d7` |
| `r10/probe-comparison.json` | 11,198 | `fab09bd87d35b36d8142fd9fc1627442d4489ad61de8109cf81e499875e62967` |

`HANDOFF.md`, `PR-BODY.md` and `MANIFEST.sha256` are updated in packet `629-b16-a603`. No packet file exceeds 200 KB. No push, PR edit, merge or bench action occurred. Independent re-review and publication remain with the manager.

Still open: Direction B's INTERNAL mismatch control, lane B6's timed ratio for B-CRF and B-AAF, and #645. Refs #629.

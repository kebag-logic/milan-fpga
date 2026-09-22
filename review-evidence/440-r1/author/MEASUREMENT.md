[A158] issue #440 closing-condition measurement

Base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`.
Head: `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba`.

Authority is the settled [issue decision](https://github.com/kebag-logic/milan-fpga/issues/440#issuecomment-5771170243), [CommonMark 0.31.2 4.5](https://spec.commonmark.org/0.31.2/#fenced-code-blocks), [4.6](https://spec.commonmark.org/0.31.2/#html-blocks), [R86-9](https://github.com/kebag-logic/milan-fpga/pull/428#issuecomment-5651750010), and [R85-8](https://github.com/kebag-logic/milan-fpga/pull/428#issuecomment-5651704309). The reports name local instruments, without downloadable sources. The public tree at their reviewed head contains none of those instruments. This is a reconstruction of their documented population, not a rerun of the original instrument or its entire 504-row/106-row campaigns.

The 205-row sweep uses the same source strings, in the same order, on both engines. Each fixture has one `## Probe` after the tested delimiter. GitHub received synthetic text only, via `gh api markdown --method POST --input -` with `mode: gfm`. Exact UTF-8 fixtures, requests, HTML, timestamps and SHA-256 receipts are under `renderer/`; the compact public bundle also contains them. `fixtures.json` is the readable population; `comparisons.tsv` and `comparisons.json` contain every row.

Population: 58 fence rows (backticks and tildes), 58 type-1 character rows (later and opening line), 64 name rows (all four opener/closer pairs, uppercase/lowercase, both positions), eight Unicode-fold rows, and 17 boundary/precedence/CR rows. Each character sweep includes an empty trailer, space, tab, and the historical 26 characters including CR: U+000B, U+000C, U+000D, U+001C..U+001F, U+0085, U+00A0, U+1680, U+2000..U+200A, U+2028, U+2029, U+202F, U+205F, U+3000. Thus the historical 25 non-CR fence rows and 27 non-CR type-1 rows are represented explicitly. Unicode rows use U+017F, U+0131 and U+0130; all eight already agree at this base and remain unchanged.

| Instrument | Agree | Escape | Withhold | Refused by current policy |
|---|---:|---:|---:|---:|
| Base raw helper | 90 | 62 | 53 | 108 |
| Head raw helper | 200 | 0 | 5 | 108 |
| Base after Path.read_text normalization | 93 | 60 | 52 | 100 |
| Head after Path.read_text normalization | 205 | 0 | 0 | 100 |

Escape means the walk lists a heading the renderer hides. Withhold means the renderer emits a heading the walk omits. Counts after normalization describe the helper on the text the reader supplies, before applying refusal; the 100 refused rows are not claimed as accepted shipped pages. The global refusal set and its application to both provenance and base authority are unchanged. Existing ASCII folding already restricts Python `\s` at type-1 closers to ASCII whitespace, so the current base has fewer type-1 escapes than the historical Unicode-flag head. This fix changes 116 raw answers and 112 normalized answers, all in the enumerated closing-condition/CR rows; every row is listed in `summary.json` and `comparisons.tsv`.

The five remaining raw divergences are `F-backtick-U000D`, `F-tilde-U000D`, `B-fence-crlf`, `B-fence-cr`, and `B-type1-cr`. Each withholds a heading and carries CR, which the raw policy refuses. Raw helpers split only on LF; actual generator `Path.read_text` and the gate's Git text-mode reader normalize CR/CRLF. All five agree after normalization. Type-1 internal CR does not become a valid closer: normalization separates the name from `>` across lines. No unrefused normalized disagreement remains.

An additional 18 renderer receipts cover the exact 17 base pages and shared head used by the shipped-gate experiment (`e2e-fixtures.json`). Both versions run as actual CLIs in disposable repositories, with per-page judgments and exact added-line lists retained. Four internal-blank cases change from 0 findings/1 exempt label to 1/0; the valid cross-name cases change from 1/0 to 0/1. ASCII capitals, already-fixed Unicode names, refused FF/NBSP, and CR normalization controls retain their intended answers. The CR-only fence correctly exempts its label but still reports the heading itself as added: Git diff uses LF-delimited lines even though the subsequent reader normalizes CR. Both aggregate CLIs exit 1 because the corpus deliberately contains disallowed labels; these are expected negative controls, not a failed author gate.

All 163 tracked pages were dumped with both engines on both base and head populations (`blocks`, `line_kinds`, headings, ownership, refusals and generated blocks). Engines agree byte-for-byte on each population. All headings and generated Contents remain identical between revisions; 105 pages retain provenance. No parser correction affects a tracked page. The only Markdown content change is the enumerated source-rule explanation in `docs/DOC_GENERATION.md`; no generated Contents was rewritten.

The permanent suite retains the original 279 TOC arms and adds 404 I440 arms, reaching 683/683. The em-dash suite retains 34 arms and adds 17, reaching 51/51. Existing site-count and negative source controls remain; the shipped-site kind expectation strengthens from both kinds to single-source only, with 25 sites still required. A new case module keeps the existing three modules below the unchanged 1,000-line quality limit. No budget changes occur.

Eleven bounded mutations run on disposable copies, with exact patches, stdout, exit codes and source SHA-256 receipts under `sensitivity/`. Every mutant fails behavioral I440 arms. They cover Python strip restoration, a wider named fence class, tab removal, internal blanks, matching-name-only closing, Unicode folding, case sensitivity, omission at either call site, line-start anchoring, and restoration of the old type-1 implementation. The first two remain silent through the shipped em-dash gate because the existing character refusal masks them; their raw behavioral arms fail independently. All tracked sources are hash-checked unchanged after mutation runs.

Portable reproduction from this candidate checkout, with this evidence directory bound to `AUTHOR_EVIDENCE`:

```sh
python3 -B "$AUTHOR_EVIDENCE/measure.py" snapshot
python3 -B "$AUTHOR_EVIDENCE/measure.py" renderer
python3 -B "$AUTHOR_EVIDENCE/measure.py" observe --scripts "$AUTHOR_EVIDENCE/base/scripts" --label base
python3 -B "$AUTHOR_EVIDENCE/measure.py" observe --scripts scripts --label head
python3 -B "$AUTHOR_EVIDENCE/measure.py" compare
python3 -B "$AUTHOR_EVIDENCE/e2e.py" --scripts "$AUTHOR_EVIDENCE/base/scripts" --label base
python3 -B "$AUTHOR_EVIDENCE/e2e.py" --scripts scripts --label head --render
python3 -B "$AUTHOR_EVIDENCE/mutations.py"
```

`renderer` reuses exact cached HTML if present. To obtain fresh observations, use a new evidence directory or move that cache aside. Only synthetic fixture text is transmitted.

Manager-owned and not run by A158: complete native RTL/lint/elaboration, processor suites, builder tests, Yosys, behave, complete milan_dp sweep, trusted act, hosted CI, independent reviews, candidate merge validation and containment. No Docker, installation, privilege, hardware, unrelated lane edit, push, PR, review, merge or subagent action occurred.

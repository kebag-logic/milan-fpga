# A158 author handoff: issue 440

Head: `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba`.
Base: `b17580b91deb11f3441dfc5d7f9fafe539d929b8`.
Branch: `440-markdown-closers`.
Checkout: `$CANDIDATE`.
One commit, one-line subject, no trailers. No push or PR created.

The two closing decisions now follow the settled renderer rules. Fence trailers use `CLASSES["blank"]`; `_type_1_end` matches any literal `pre`, `script`, `style`, or `textarea` closer with the existing ASCII fold and no blanks. Both call sites use that rule. No other classification function body changed. Global character refusal, all non-tally constants, provenance/gate runtime logic and the existing Unicode-fold controls are unchanged, as checked by `scope_guard.py`.

Six changed files: `scripts/gen_toc.py`, `scripts/gen_toc_cases.py`, `scripts/gen_toc_guards.py`, `scripts/gen_toc_closer_cases.py`, `scripts/check_em_dash.py`, `docs/DOC_GENERATION.md`. The new fixture module keeps existing modules under the unchanged long-module limit. The original 279 TOC controls and 34 em-dash controls remain; 404 I440 raw controls and 17 real-Git controls are added. Two existing guard expectations reflect the eight families and the now exclusively single-source sites; the site count remains 25. No RTL, workflow, ci_events, builder, version, budget or gitlink change.

Acceptance evidence is in `MEASUREMENT.md`. The original historical instrument was not obtainable through its linked public reports/tree, so `measure.py` reconstructs the documented population. The same 205 exact synthetic inputs were observed at base/head with GitHub gfm. Normalized helper results are 205 agree, zero escapes and zero withholding at head, versus 93/60/52 at base. The 100 normalized refused rows remain refused. Raw head results are 200 agree and five CR withholdings, all explicitly named and refused; both shipped readers normalize those to agreement. Eight Unicode-fold rows were already correct at base and stay correct. Eighteen additional HTML receipts cover the exact end-to-end gate pages. Four inner-blank label escapes are rejected; two cross-name labels become valid. The CR-only diff nuance is retained, not mislabeled as a refusal or closer defect.

All 163 tracked Markdown pages were compared using both engines on both populations. Engine outputs are identical for each population. Headings, generated Contents, ownership and refusal results remain identical across revisions; 105 pages carry provenance. No tracked parser correction occurs. The only Markdown content change is the 32-line explanation in `docs/DOC_GENERATION.md`.

| Author validation | Result |
|---|---|
| `python3 -B scripts/gen_toc.py --selftest` | 683/683 |
| `python3 -B scripts/gen_toc.py --check` | 105 TOCs; 17 below threshold |
| `python3 -B scripts/gen_toc.py --verify-anchors` | 144 links reproduced |
| `python3 -B scripts/gen_toc.py --sites` | 25 single-source sites; no guard notes |
| `python3 -B scripts/check_em_dash.py --selftest` | 51/51 |
| `python3 -B scripts/check_em_dash.py --base b17580b91deb11f3441dfc5d7f9fafe539d929b8` | 0 findings, 32 added lines, 1 changed page |
| `python3 -B scripts/docs_check.py` and `--selftest` | 0 findings across 163 Markdown/827 text files; 23 scrub + 4 routing arms |
| `python3 -B scripts/check_doc_paths.py` | 824 cited paths resolve |
| `python3 -B scripts/check_doc_style.py` | 22 current documents pass |
| `python3 -B scripts/check_py_idiom.py` and `--selftest` | unchanged ratchets pass; 54/54 controls |
| `python3 -B scripts/check_hygiene.py --check` | 706 files, 3 populations pass |
| `python3 -B scripts/check_rtl_source_lists.py` | 103-file closure; 4/4 lists; processor 32/38 with 6 recorded omissions |
| `mutations.py` | 11/11 mutants fail behavioral I440 arms; source bytes preserved |
| `scope_guard.py`, `compare_pages.py` | exact permitted diff; per-page equality |
| `git diff --check`, Git/submodule status | clean |

`commands.jsonl` contains exact executable arguments, working directory, timestamp, duration, exit and log path; `logs/` retains full output. Early documentation paragraph-style failure was fixed before the final passing run. During development a CR-only control incorrectly expected Git to retain the heading line; the final control measures its added-heading finding separately from the valid copied-label exemption. The first public bundle attempt exceeded the single-comment limit; the exact payload was split into two verified parts. No unresolved validation failure remains in the author scope. Expected negative fixture CLI exits and mutation failures are evidence of sensitivity.

Portable evidence: `portable-receipts.json.gz` (950 UTF-8 files in JSON), SHA-256 `4f826e84ed800957e26966002319d69766d7f5ce563a6966eb05b1f8a2addd20`; `renderer/`, `sensitivity/`, full per-page dumps, raw/normalized row dumps, and replay scripts remain here. The compressed public payload contains fixtures, exact HTML/requests/receipts, all comparison rows, sensitivity patches/logs, per-page hashes and instruments. Full page dumps and command logs remain in this management directory. All synthetic data is outside tracked Markdown.

Public takeover: https://github.com/kebag-logic/milan-fpga/issues/440#issuecomment-5771587303.
Portable receipts: https://github.com/kebag-logic/milan-fpga/issues/440#issuecomment-5771717445 and https://github.com/kebag-logic/milan-fpga/issues/440#issuecomment-5771717582.
The issue measurement summary is saved as `PUBLISH-MEASUREMENT.md`; its published URL is recorded in `public/author-measurement-url.txt`.

A10 owns publication, complete native RTL/lint/elaboration/processor/builder/Yosys/behave validation, trusted act and hosted CI, independent R225/R226 reviews, candidate merge validation, merge and containment. Those are not run or claimed here. No full milan_dp sweep, Docker/act, privileged operation, dependency install, hardware, unrelated lane edit, push, PR, review, merge or subagent action occurred. This is a focused author handoff, not the repository's full completion claim.

Final initialized submodules are clean and at their pins: gptp-processor `c1b617435824929a790739ea8585c3fe1a328cc0`, protocol-processor `424c688fa2205b934a7689a58f2aa766420f2326`, verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. `external` remains uninitialized at its unchanged gitlink, as at takeover. The author branch stops at the named committed head.

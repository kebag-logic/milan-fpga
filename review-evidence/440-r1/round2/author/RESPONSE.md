[A164] RESPONSE TO R226-F1

Finding: MINOR Tests and Docs, unchanged reviewer-assigned lenses.
Source: https://github.com/kebag-logic/milan-fpga/pull/507#issuecomment-5772986192
Accepted scope: https://github.com/kebag-logic/milan-fpga/pull/507#issuecomment-5772995412
Settled rule: https://github.com/kebag-logic/milan-fpga/issues/440#issuecomment-5771170243
The four literal names follow [CommonMark 4.6](https://spec.commonmark.org/0.31.2/#html-blocks).

Implemented at `9d6109ccf924c03308cb8aa202ce68a435cd4f8d`, tree `1d322d866da6b8d19ccd46cfd7ef5f405e9dadb4`. Production behavior did not change. The new raw fixtures put a heading after a closing tag of another ASCII name and require HTML classification. They cover `pre`, `script`, `style`, and `textarea` openers, each with later-line and opening-line closer placement. Six real-Git controls unwrap old hidden headings into valid generated navigation and require the copied labels to be refused. They call the existing gate's judge_page; no parser or gate is duplicated. Existing positive literal/cross-name controls remain intact.

| Exact closer-site mutation | Starting TOC / em-dash exits | Corrected TOC / em-dash exits | Named controls |
|---|---|---|---|
| R15: add div only at closer | 0 / 0 | 1 / 2 | I440-T-other-name */div; I440-E-other-div and -inline |
| R16: add title only at closer | 0 / 0 | 1 / 2 | I440-T-other-name */title; I440-E-other-title and -inline |
| X04: add xmp only at closer | 0 / 0 | 1 / 2 | I440-T-other-name */xmp; I440-E-other-xmp and -inline |

Each mutation leaves RAW_HTML_TAGS exactly the original four. Each corrected mutation fails eight raw arms and two label rows. The label harness emits two diagnostics per failed row, so its unchanged summary reports four failed arm diagnostics. See original/results/mutants/ and corrected/results/mutants/ for exact unified patches, complete logs, named failures and source-integrity digests. reproduce.py loads the unchanged public r226_mutants.py, selects R15/R16, and supplies the exact X04 edit from public r226_mutants_extra.py. Other reviewer mutations and optional suggestions were not rerun or changed.

The real CLI instrument is public r226_e2e.py, selected to E03, E14, E15, plus an equivalent xmp fixture. It creates disposable real Git base/head commits, calls the real gen_toc --write and --check, and invokes check_em_dash --base. No selftest was bypassed. Every scenario completed; source scripts were copied into temporary repositories and never patched in the implementation lane.

At the starting head, the unmutated engine rejects all three hidden labels and exempts only E03. Each mutant instead exempts its corresponding hidden label; the combined run still exits 1 because the other negative fixture pages produce findings. That nonzero result does not mean the escaped label was detected. At the corrected head, the unmutated result is unchanged (three findings, one exemption, exit 1). All widened engines exit 2 on the new permanent label controls before page judgment. The public instrument's per-page false flags at exit 2 mean no judgment occurred, not that labels were exempted. Every unwrapped head page passes gen_toc --check.

Archived E14/E15 HTML requests and responses were fetched from the public R226 evidence commit `26f9c8675a5a1f8ab746f15087a13e722e68bb0b`. Request source bytes equal the independently replayed fixture pages. Request/HTML SHA-256 values match their public receipts. Both gfm and markdown responses contain zero h2 headings. public-html/verification.json records the exact source URLs. This is verification of attributed archived renderer evidence; no live Markdown rendering requests were sent. The extra xmp CLI example uses the settled four-name rule and the review's existing measurement; no new xmp renderer measurement is claimed.

Retention and maintenance: all 683 original TOC cases remain by family/name/fixture hash; all original 51 em-dash controls remain. Added populations are nonempty and distinct: 24 raw cases, six label cases. The existing TOC floor rises to 707. M01 removes all new raw cases and fails the floor at 683; M02 drops one and fails at 706; M03 adds a valid literal cross-name case and passes at 708. The unchanged shipped positive E03 remains exempt on both unmutated snapshots. See maintenance/ and fixture-retention.json.

DOC_GENERATION.md now names fence-trailer and literal closer boundaries, with explicit other-ASCII-name raw/shipped coverage. No snapshot counts or optional wording changes were included. All requested focused checks passed; COMMANDS.md and REVIEW-READY.md record them. Reviewers own re-review and any coverage acceptance.

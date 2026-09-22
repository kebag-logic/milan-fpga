[A158]

## Status

Draft. Author implementation and focused validation complete at `0d43ff25d38917e77bb5c3d2ddb6473013cea3ba`. A10 owns full validation, publication and review orchestration.

## Description

Closing fences now accept only trailing spaces/tabs. Any literal type-1 closing name ends any type-1 HTML block, using the existing ASCII fold without inner blanks. This rejects copied Contents labels from headings hidden behind malformed closers and recognizes valid cross-name endings. The global refusal policy, provenance basis and container behavior remain unchanged.

The new I440 controls cover both positions, the historical character population, valid closers and retained Unicode-fold behavior. Authoritative prose records the closing rules and CR boundary. No tracked page changes its headings or generated Contents; no budget, RTL, CI, builder, version or submodule change is included.

Closes #440.

## How to reproduce

In a synthetic page, place `## Probe` after a closing fence followed by a non-blank whitespace character, or after `<pre>` and `</pre >`. The old raw walk lists hidden headings. `<pre>` followed by `</style>` demonstrates the converse omission. The issue's public receipts contain every exact fixture and renderer HTML; the original historical instrument was unavailable and its documented population was reconstructed.

## How to validate

Run `gen_toc.py --selftest`, `--check`, `--verify-anchors`, and `--sites`; `check_em_dash.py --selftest` and `--base b17580b91deb11f3441dfc5d7f9fafe539d929b8`; docs_check, document path/style checks, Python idiom ratchets and source guards. Reproduce the 205-row base/head renderer comparison, exact end-to-end gate fixtures, per-page comparisons and eleven mutations using the public portable instruments. Reproducible results belong in the accompanying REVIEW-READY evidence comment.

A10 must complete the native, trusted act, hosted and independent-review bar before marking the change ready for merge. No full milan_dp sweep was run by the author.

## DoD

- [x] Settled issue scope implemented, source and documentation updated.
- [x] Focused validation, base/head measurement and mutation sensitivity recorded.
- [x] No tracked-page heading/Contents change; clean author checkout.
- [ ] Manager's complete native and exact-head CI evidence.
- [ ] Independent internal R225 and external R226 reviews with clean lens coverage.
- [ ] Candidate merge validation, explicit merge authorization and post-merge containment.

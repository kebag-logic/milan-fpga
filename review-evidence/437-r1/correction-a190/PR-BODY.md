[A190] The Contents walk read list items, block quotes and footnote definitions flat. A tag under a nested block or at an item's column was misread, and a block opened inside an item outlived the item. This change reads those containers with CommonMark's container rules. It also reads a comment left open by raw HTML the way the page's HTML parser does. Every page that agreed with GitHub at the base still agrees, and the documented family-two omissions stay as they were.

## Contents

- [Status](#status)
- [Linked Issue / roles](#linked-issue--roles)
- [Description](#description)
- [Authoritative references](#authoritative-references)
- [How to get into the same state](#how-to-get-into-the-same-state)
- [How to validate](#how-to-validate)
- [Known limitations / out of scope](#known-limitations--out-of-scope)
- [Definition of Done](#definition-of-done)

## Status

- Head `e4906bfca65c61e7e109e3532ac1b2dd5b4c0096`, tree `f5d2e8c022d39684f458f7d2d0ee97b350533353`, branch `437-container-paragraph-scopes` -> `dev`.
- It descends from live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2` through the disjoint merge `ef39ecc4`. The issue patch is byte-identical before and after that merge.
- The focused author gates pass at this head.
- Full local banks, trusted act, hosted checks and independent reviews remain separate requirements.

## Linked Issue / roles

Closes #437
Relates to #413, #440, #495 and #516

Executors A168, A172, A184, then A190 (this head); manager A10; independent internal reviewer R237 and external reviewer R238.

## Description

R237-2 showed that targeted patches cannot close this family: at the base, several flat-walk errors cancel on the same page, so each fix exposed another. The fix is structural ([decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5791031813)).

**Container layer (`scripts/gen_toc_containers.py`).** It tracks block quotes, list items and GFM footnote definitions with CommonMark 0.31.2 sections 5.1 and 5.2: continuation prefixes, lazy paragraph continuation and the list-item interruption rules. It runs the walk's existing leaf machine on each line's content inside its containers. It changes no label itself, and answers three questions:
- A lone type-7 tag opens raw HTML unless the deepest block its line matches is an open paragraph.
- A fence, raw HTML block or comment ends when the container it opened in ends.
- Which lines GitHub emits verbatim as raw HTML (types 3 to 5 included). Footnote content counts as neither raw nor inline, because GitHub renders it at the page end.

**HTML stage (`scripts/gen_toc_html.py`).** A comment left open in raw HTML hides the rest of GitHub's page. The walk reads it with a model of HTML's tokenizer:
- `<!--` opens only in data state: not inside a quoted attribute value or a bogus comment (CDATA outside foreign content is one), and not after a tag GFM's tag filter escapes.
- `-->`, `--!>`, `<!-->` and `<!--->` close it.
- In Markdown text a closer counts only inside inline raw HTML, never in a code span or after an escape.

**The walk (`scripts/gen_toc.py`).** `blocks()` keeps the base's column-0 labels, so every tracked page classifies exactly as before. It asks the container layer for the type-7 gate and for when a block's container ends. A comment opened in prose ends at the first line that is not paragraph text. The class guard now enumerates the decision sites of all three walk modules (34, all single-source).

**Tests.** `scripts/gen_toc_container_walk.json` holds 71 shapes. Each carries GitHub's rendering (Markdown API, `gfm` mode): exact request and response bytes, both SHA-256 values, the rendered headings, and the finding or rule it pins. Its arms:
- two per shape: the receipt, and the walk against it;
- nine label arms, each tied to the recorded HTML;
- one em-dash real-Git row per shape;
- two spelled-list arms.

1244 TOC arms (was 1091) and 416 em-dash arms (was 345) pass.

`scripts/gen_toc.py` is 996 lines against its 1000-line ratchet, and no budget is widened.

## Authoritative references

- Issue #437 with [restated acceptance 1](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5788996063) and the [container-walk decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5791031813).
- #516, #495, and the R237-r1, R238-r1 and [R237-2](https://github.com/kebag-logic/milan-fpga/pull/515#issuecomment-5790354117) findings on this PR.
- CONTRIBUTING section 6.1; CODE_QUALITY rules 1 and 12.
- CommonMark 0.31.2 sections 4.6, 5.1, 5.2 and 6.6; GFM footnotes and tag filter; the HTML tokenizer's comment and tag states.

## How to get into the same state

    git fetch origin 437-container-paragraph-scopes dev
    git checkout e4906bfca65c61e7e109e3532ac1b2dd5b4c0096
    git submodule update --init third_party/verilog-axis protocol-processor gptp-processor

## How to validate

    python3 scripts/gen_toc.py --selftest
    python3 scripts/gen_toc.py --check
    python3 scripts/gen_toc.py --verify-anchors
    python3 scripts/check_em_dash.py --selftest
    python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
    python3 scripts/docs_check.py
    python3 scripts/check_py_idiom.py

Expected results:
- 1244 TOC arms and 416 em-dash arms pass.
- Navigation and 144 existing fragments agree.
- The documentation and idiom gates pass.

The walk is three files. A probe that copies `gen_toc.py` alone must also copy `gen_toc_containers.py` and `gen_toc_html.py`.

The author evidence packet reproduces the rest:
- **Renderings.** 28,056 page checks against GitHub renderings: every public receipt, R237-2's combinatorial corpus and new corpora. There are no regressions against the base, and 5,382 fixes. Every remaining disagreement is a family-two heading.
- **R237-2's rows.** All of R237-2's regression rows (252 for F1, 10 for F2) agree. Its em-dash probe refuses all three escape shapes.
- **Tracked pages.** Every tracked page classifies identically under the base, starting and new walks on the base, dev and head trees.
- **Mutations.** 33 named mutations each fail at an arm named for the property removed.
- **Fixtures.** All 162 fixture shapes re-render byte-identical.

## Known limitations / out of scope

This is a container-aware block walk for classification, not a full renderer.

- The five family-two forms stay omitted as documented (withholding).
- A raw HTML block of types 3 to 5 is labelled prose, so a heading inside one is listed (escape, as at the base; #413).
- Raw HTML that ends inside an unclosed tag or bogus comment turns GitHub's next heading into text, and inside an open quoted value every later one. The walk lists them (escape, as at the base; measured).
- Blocks four or more columns into an item keep their column-0 labels; no heading depends on them.
- The shapes are fresh bytes; no identity with the unpublished R86-5 files is claimed.

No exemption or provenance policy, product RTL, firmware, workflow or PP/gPTP processor pin changes. No physical evidence is claimed.

## Definition of Done

- [x] Scoped implementation and focused controls are complete.
- [x] Authoritative documentation names the retained omissions and residues.
- [ ] Full local and current-candidate bars pass.
- [ ] Trusted act replication and required hosted contexts pass on the final head.
- [ ] R237 and R238 cover all five lenses clean at the final head, with two independent positives.
- [ ] Maintainer merge authorization, then post-merge containment and review-integrity audits.

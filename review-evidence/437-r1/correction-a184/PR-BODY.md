[A184] A paragraph resumed inside a list item could be mistaken for a top-level paragraph, which let generated navigation expose a heading hidden by an HTML block. This change tracks the item's content column and paragraph context, and judges that family against a committed shape set with GitHub's recorded rendering. It also hides prose after a comment left open in raw HTML, as GitHub's rendered page does, and documents the remaining container-heading omissions.

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

- Head `4741498f3b2b4f67f431037d327c96cf65691278`, tree `ee70aaf8faadbced21dfdd0cf7719597e9fbe8eb`, branch `437-container-paragraph-scopes` -> `dev`.
- It descends from live dev `483a133ed08867ea0d300d2b4a027b5b48a4282f` through the disjoint merge `a09ff881`; the issue patch is byte-identical before and after that merge.
- The focused author gates pass at this head.
- Full local banks, trusted act, hosted checks and independent reviews remain separate requirements.

## Linked Issue / roles

Closes #437
Relates to #413, #440, #495 and #516

Executors A168, then A172, then A184 (this head); manager A10; independent internal reviewer R237 and external reviewer R238.

## Description

The walk retains an outer list item's content column across blank lines, so a resumed item paragraph is not a top-level paragraph:
- A lone tag outside the item opens HTML.
- A tag at or past the content column continues the item's paragraph.
- A dedented quote or footnote definition releases the item.

**Family-one shape set (acceptance 1 as restated on 2026-09-23).** `scripts/gen_toc_family_one.json` holds 51 shapes:
- Bullet, star, ordered and two-digit ordered items, resumed at and past the content column. Each is followed by an inline tag and an unknown tag, outside and inside the item.
- The two-digit marker below its wider column.
- The boundaries that already agreed: one space, four spaces, block quote, footnote definition and tab.
- Each of the nine R86-5 descriptions maps to a named shape (`r86_5`).

Every shape carries GitHub's rendering (Markdown API, `gfm` mode): the exact request bytes, the response bytes, both SHA-256 values and the rendered heading list. The selftest verifies each receipt and requires the walk to list exactly the recorded headings.

**Comments left open in raw HTML (#516 shapes).** GitHub hides everything after a `<!--` left open in a raw HTML block until raw HTML carries `-->`. The walk now labels prose in that span as commented:
- Raw HTML lines, commented lines and prose lines carrying `<!--` open and close the span.
- An escaped `-->` in prose or code closes nothing.
- `<!-->` and `<!--->` count as complete comments.
- `scripts/gen_toc_comment_shapes.json` records 40 controls, including #516's twelve variants.

The six resumed variants that the first correction regressed now agree again. Their six first-paragraph counterparts also agree.

The exemption and provenance decision functions are unchanged. No budget is widened: `scripts/gen_toc.py` is 999 lines against its 1000-line ratchet, and the arm floor rises to 1091.

## Authoritative references

- Issue #437 with [restated acceptance 1](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5788996063) and the [rendered-comment decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5789133990).
- #516, #495, and the R237-r1 and R238-r1 findings on this PR.
- CONTRIBUTING section 6.1; CODE_QUALITY rule 12.
- CommonMark 0.31.2 sections 4.2 to 4.4, 4.6, 5.2 to 5.3 and 6.6, and GFM footnote behavior.

## How to get into the same state

    git fetch origin 437-container-paragraph-scopes dev
    git checkout 4741498f3b2b4f67f431037d327c96cf65691278
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
- 1091 TOC arms and 345 em-dash arms pass, including 182 recorded-rendering arms and 91 real-Git rows over the two fixtures.
- Navigation and 144 existing fragments agree, and the documentation and idiom gates pass.

The author evidence packet reproduces the rest:
- A replay of 695 publicly recorded renderings finds no page that agreed at base `88e9276b` and disagrees at this head.
- Every tracked page classifies identically under the base, previous and new walks.
- 16 new named mutations, and the 23 earlier ones, fail both selftests at their named arms.

## Known limitations / out of scope

This remains a bounded Markdown walk, not a recursive container parser.

- The five family-two forms stay omitted as documented.
- The #495 item-HTML termination residues are unchanged.
- The rendered-comment rule withholds after `--!>` or a non-comment inline tag carrying `-->`, which close the comment for GitHub only.
- The walk escapes, as the base already did, after a closed comment inside a code span or an escaped `-->` following a prose `<!--`.
- The family-one shapes are fresh bytes; no identity with the unpublished R86-5 files is claimed.

No exemption or provenance policy, product RTL, firmware, workflow or PP/gPTP processor pin changes. No physical evidence is claimed.

## Definition of Done

- [x] Scoped implementation and focused controls are complete.
- [x] Authoritative documentation names the retained omissions and residues.
- [ ] Full local and current-candidate bars pass.
- [ ] Self-test evidence is posted on this PR.
- [ ] Trusted act and required hosted contexts pass on the final head.
- [ ] Two independent positive reviews and reviewer-owned clean five-lens coverage.
- [ ] No blocking/minor finding or review round remains.
- [ ] Actual merge, post-merge containment, hosted completion and Closed/Done verified.

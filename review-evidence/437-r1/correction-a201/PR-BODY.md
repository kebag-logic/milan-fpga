[A201] The Contents walk read list items, block quotes and footnote definitions flat. A tag under a nested block or at an item's column was misread, and a block opened inside an item outlived the item. This change reads those containers with CommonMark's container rules. Comments are read as the base walk reads them. A comment that raw HTML leaves open on GitHub's page is a documented escape limitation owned by #516, as the 2026-09-23 14:15 owner decision directs.

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

- Head `34f124f9b0dabeb74c655052f0a0858620a09037`, tree `bb9b3dbc70a81af453f47c4c72aeb8433d927d91`, branch `437-container-paragraph-scopes` -> `dev`.
- It descends from live dev `ede8d48ecd7c7f589a14b957951f040d92c99c70` through the conflict-free merge `070ef51e`. The issue patch keeps its patch-id across that merge.
- The focused author gates pass at this head.
- Full local banks, trusted act, hosted checks and independent reviews remain separate requirements.

## Linked Issue / roles

Closes #437
Relates to #413, #495 and #516

Executors A168, A172, A184, A190, then A201 (this head); manager A10; independent internal reviewer R237 and external reviewer R238.

## Description

**Container layer (`scripts/gen_toc_containers.py`).** It tracks block quotes, list items and GFM footnote definitions with CommonMark 0.31.2 sections 5.1 and 5.2: continuation prefixes, lazy paragraph continuation and the list-item interruption rules. It runs the walk's leaf machine on each line's content inside its containers. It changes no label itself, and answers two questions:
- A lone type-7 tag opens raw HTML unless the deepest block its line matches is an open paragraph.
- A fence or raw HTML block ends when the container it opened in ends.

An item continues over a blank line only while it holds a block. A nested container counts as one. A paragraph made only of link reference definitions counts only while it is open, because the renderer drops it when it closes. A raw HTML block of types 3 to 5 holds no container and ends at its end marker. Inside one, the type-7 gate is left to the walk, which labels those lines text (#413).

**The walk (`scripts/gen_toc.py`).** `blocks()` keeps the base's column-0 labels, so every tracked page classifies exactly as before. Comments are read as at the base: `<!--` outside a fence, raw HTML block or code opens one until the next `-->`. The class guard enumerates the decision sites of both walk modules: 29, all single-source.

**Removed under the owner decision.** The rendered-comment emulation of the previous head is gone: `scripts/gen_toc_html.py`, the rendered-comment flag, the prose-comment end rule, a comment ending with its container, and `<!-->` closing a comment.

**Tests.** Three committed fixtures carry GitHub's rendering (Markdown API, `gfm` mode) of every shape: the exact request and response bytes, both SHA-256 values and the rendered headings.
- `gen_toc_family_one.json`: acceptance 1's 51 shapes.
- `gen_toc_comment_shapes.json`: 38 shapes.
- `gen_toc_container_walk.json`: 86 shapes.

A shape the walk answers differently from GitHub carries `limitation`: its owner, its direction, the walk's answer and whether the base agreed. Its arm pins that answer and direction instead of claiming agreement. 1269 TOC arms (was 707 on dev) and 429 em-dash arms pass.

`scripts/gen_toc.py` is 999 lines against its 1000-line ratchet, and no budget is widened.

## Authoritative references

- Issue #437 with acceptance 1 as amended 2026-09-23 14:15, the [owner decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5794734885) and the [container-walk decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5791031813).
- #516, which owns the unclosed raw-HTML comment family and the findings moved there.
- The R237-3 and R238-2 findings on this PR, and every earlier round.
- CONTRIBUTING section 6.1; CODE_QUALITY rules 1 and 12.
- CommonMark 0.31.2 sections 4.6, 4.7, 5.1, 5.2 and 6.6.

## How to get into the same state

    git fetch origin 437-container-paragraph-scopes dev
    git checkout 34f124f9b0dabeb74c655052f0a0858620a09037
    git submodule update --init third_party/verilog-axis protocol-processor gptp-processor

## How to validate

    python3 scripts/gen_toc.py --selftest
    python3 scripts/gen_toc.py --check
    python3 scripts/gen_toc.py --verify-anchors
    python3 scripts/check_em_dash.py --selftest
    python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
    python3 scripts/docs_check.py
    python3 scripts/check_doc_style.py
    python3 scripts/check_py_idiom.py

Expected results:
- 1269 TOC arms and 429 em-dash arms pass.
- 106 navigation pages and 144 existing fragments agree.
- The em-dash gate finds nothing in the added lines.
- The documentation and idiom gates pass.

The author evidence packet reproduces the rest:
- **Fixtures.** Family one agrees 51/51, and nine shapes map the R86-5 descriptions. No receipt byte of a kept shape changed.
- **Tracked pages.** Every tracked page classifies identically under the base walk and this walk on the base, dev and head trees (164 pages each).
- **Mutations.** 14 named mutations each fail at an arm named for the property removed.
- **Renderings.** 6,760 public rendered pages were replayed, and 60,000 generated pages were swept, with every page that differs from the base rendered. 25 pages that agreed at the base disagree here:
  - 10 are the #516 family;
  - 15 are residues that the base's unended block hid by accident, each named below.

## Known limitations / out of scope

This is a container-aware block walk for classification, not a renderer.

- The five family-two forms stay omitted as documented (withholding).
- **Unclosed raw-HTML comments (#516, escape).** GitHub leaves such a comment open, and it hides the rest of its page. The walk lists those headings when the opener is in a raw HTML block or four columns into an item, or when GitHub prints a closer as text.
- **The comment reading (as at the base).** It withholds after an opener that GitHub prints as text, or after an empty comment. It lists a fence's headings when such a comment covers the fence and a `-->` inside the fence ends it.
- **Other HTML-parse escapes, shared with the base.** Raw HTML ending inside an open tag, bogus comment or quoted value hides the next heading or every later one, and `<select>` hides those inside it. A raw HTML block of types 3 to 5 is labelled prose (#413).
- **Uncovered residues.** Where the base left a raw HTML block or fence open past its list item, a residue above that the base hid by accident now shows, in its own direction.
- **Link reference definitions.** One outside the recognised one-line form keeps its item.
- The shapes are fresh bytes; no identity with the unpublished R86-5 files is claimed.

No exemption or provenance policy, product RTL, firmware, workflow or PP/gPTP processor pin changes. No physical evidence is claimed.

## Definition of Done

- [x] Scoped implementation and focused controls are complete.
- [x] Authoritative documentation names the retained omissions and residues.
- [ ] Full local and current-candidate bars pass.
- [ ] Trusted act replication and required hosted contexts pass on the final head.
- [ ] R237 and R238 cover all five lenses clean at the final head, with two independent positives.
- [ ] Maintainer merge authorization, then post-merge containment and review-integrity audits.

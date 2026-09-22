# A168 handoff: issue #437

Implementation complete for independent review; source clean and committed, not pushed.

- Worktree: $CANDIDATE
- Branch: 437-container-paragraph-scopes
- Base: `88e9276b2a220c716f64a843f7e1eb8f9265e896`
- Base tree: `c23dff6c0eafdf5ae89bb3e8a9416c55533a2332`
- Head: `65df1df50a80cd5f540a93d8f0cfabc97da3da75`
- Head tree: `da06c8609b7a574e3df121fbcb8a1fc8f207dcb7`
- Commit: Fix list content-column paragraph context and document heading limits
- Changed files: CONTRIBUTING.md, scripts/gen_toc.py, scripts/gen_toc_cases.py, scripts/gen_toc_container_cases.py, scripts/check_em_dash.py

The walk retains an outer list item's content column and empty/nonempty state across paragraph boundaries. A resumed paragraph in that item remains HELD, so a following unindented type-7 tag opens HTML and cannot invent the hidden heading. Content-column, padding, tab, empty-item, nesting, sibling, lazy-line and reset boundaries are held by renderer-checked fixtures. The gate only gains test integration; its policy functions are AST-identical. No helper extraction was required. gen_toc.py is 976 lines, gen_toc_cases.py and check_em_dash.py each 995, new case module 124; no function/module ratchet widened.

## Acceptance

| AC | Author evidence and boundary |
|---|---|
| 1 | 11 fresh escape reconstructions agree with GitHub GFM; six original-boundary reconstructions remain agreeing; 25 additional context controls agree on Old. The original report names 11 historical IDs without publishing their JSON/HTML; archival byte identity and one-to-one historical ID mapping are NOT claimed. |
| 2 | All five measured withheld forms named with direction in blocks() docstring and CONTRIBUTING 6.1; preserved omission arms. No new headings/anchors. |
| 3 | 47 new TOC arms (42 context, five omission), 42 real-Git gate cases; 17 non-equivalent bounded parser mutants each fail both shipped selftests by named I437 controls. |
| 4 | 163 original-base input pages and 163 current-head input pages compared separately under base/head parsers: zero differences in blocks, line_kinds, headings/anchors, generated_block and refusals. |
| 5 | All 25 focused commands exit 0, including requested TOC/gate/doc/idiom/ratchet/integration checks; no budget changed. Full manager-owned bars remain outstanding. |

## Actual-head evidence

TOC 754/754, em-dash 99/99; Contents check 105 pages plus 17 below threshold; anchor check 144; em-dash base gate zero findings across nine added lines. Docs zero findings over 163 Markdown pages and 828 text files. All 25 focused commands exit 0. All 707 prior arm inputs classify identically, #507 closer module byte-identical. The gate's only changed function is selftest. Seventeen mutants are killed by both selftests, and 50 exotic-character base/head cases plus an invalid-base case refuse correctly. Corpus comparison has zero differences on both input versions.

Preliminary `base`, `first-edit`, `work`, and `staged` receipts deliberately record base HEAD plus dirty status; they are development evidence, not mislabeled committed-head validation. All final `head` receipts name the committed head above. One preliminary invocation incorrectly gave check_py_idiom.py --check (exit 2); the documented bare command corrected it and passed, including on the committed head. An initial renderer extractor looked for absent anchor attributes; final receipts instead parse actual h1-h6 text from cached HTML and make no API-anchor claim.

Run from the candidate worktree using this external evidence directory:

```sh
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-author/gates.py replay
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-author/receipt.py corpus replay
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-author/receipt.py render replay
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-author/mutations.py replay
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-author/refusal_controls.py
rtk proxy python3 -B $WORKSPACE_HOME/milan-fpga-management/2026-09-22/437-author/preservation.py
```

`receipt.py render` uses cached exact synthetic GitHub requests/HTML. Preserve that dated cache; to request fresh responses, back it up and remove renderer-cache.json first. The checked-in fixtures are in scripts/gen_toc_container_cases.py. `gates.py` contains the exact 25 command argument lists. Individual `head-*.json` records carry command, exit, UTC, actual execution head/tree and status; corresponding `.log` files hold full output. `mutations-head.json` records every exact replacement, both commands/exits and named failures. Its sibling directory holds all 34 failure logs. Mutation copies are disposable and never alter checkout source. Receipt command exits: gates 0, corpus 0, render 0, mutation campaign 0 (expected child exits 1/2), refusal controls 0, preservation 0.

## Public record

- Decision: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775771538
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775813779
- Renderer fixtures/results: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5775985191
- Validation/mutations/preservation: https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5776027743
- Original R85-4: https://github.com/kebag-logic/milan-fpga/pull/428#issuecomment-5644713074
- Original R86-5: https://github.com/kebag-logic/milan-fpga/pull/428#issuecomment-5644834363

## Limits and manager responsibilities

Remaining scope limits: this is not a recursive Markdown container parser. Setext and container heading listing stays withheld, as selected publicly. Existing quote/item non-paragraph holding and four-column container indentation residues remain; no provenance, exemption or refused-character policy changed. One additional context fixture (`text` over `-`) retains the documented extra setext heading omission, so its full heading list differs while the Old probe agrees. CR normalization remains in the unchanged #507 controls. Product PP/gPTP behavior was neither changed nor tested here.

No full RTL/Yosys/processor or parent sweep, native builder bank, Docker/act, hosted inspection, hardware, installs, privilege, push, PR create/metadata, merge, other lane/checkout edit, or agent delegation occurred. The three public submodules remain at their original pins. The absent private external submodule is unchanged.

Manager A10 owns independent cleared-context R237/R238 review, reviewer-accepted lens ledger, full native and trusted-dev act/hosted bars, the live candidate merge, merge authorization and post-merge containment. These author results apply only to the head named here; a later manager merge does not relabel them.

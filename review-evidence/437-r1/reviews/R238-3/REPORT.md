[R238] NEGATIVE - exact head 34f124f9b0dabeb74c655052f0a0858620a09037

# [R238] round 3: issue #437 / PR #515, external cleared-context review

## Head under review

- Head `34f124f9b0dabeb74c655052f0a0858620a09037`, tree `bb9b3dbc70a81af453f47c4c72aeb8433d927d91`. This is the PR #515 head (`headRefOid`), not a draft.
- Base and merge base: live dev `ede8d48ecd7c7f589a14b957951f040d92c99c70`. Reviewed range: `git diff ede8d48e..34f124f9`, 10 files, 4,672 insertions, 48 deletions. Every changed file is a script, a fixture or a documentation page (`receipts/product_scope.txt`).
- Lane history: five non-merge commits and four merges from `65df1df5` to `34f124f9`. The correction commit is `34f124f9`, after `070ef51e` merged `ede8d48e`. Every commit is one line with no trailer (`receipts/commit_shape.txt`).
- Round start: https://github.com/kebag-logic/milan-fpga/pull/515#issuecomment-5796363205.

## What was read, in order

1. AGENTS.md; CONTRIBUTING.md sections 3, 5 and 6.1; docs/README.md; docs/DOC_GENERATION.md.
2. Issue #437 body, including acceptance 1 as restated and as amended on 2026-09-23 14:15. Then the manager and owner comments 5775771538, 5778773475, 5788996063, 5789003484, 5794734885 and 5795309062, and the author's public takeover (5795467933) and REVIEW READY (5795921214).
3. Issue #516 body and its owner decision 5794735214.
4. PR #428 R86-5 (5644834363): the source of the nine family-one descriptions.
5. The diff and history above. `gen_toc.py`, `gen_toc_containers.py`, `gen_toc_container_cases.py`, the three fixtures, and the `check_em_dash.py`, CONTRIBUTING and DOC_GENERATION hunks were read in full.
6. Prior review findings on PR #515, read only after an independent pass over the diff. That pass recorded a preliminary NEGATIVE before any prior finding was read. It covered F1, the table hold and the non-regex definition forms of F2, and F3. The lazy-definition case in F2(b) and the prior-row replay came afterwards. R237-r1, R238-r1, R237-2, R237-3 and R238-2 were then read. Their public probe files were fetched read-only from the evidence tree at `ccc7b2b1`.
7. R237-4, the internal reviewer's round on this same head, was not read before this verdict and ledger were written; only its listing header was seen.
8. Hosted check-run conclusions at the exact head were listed. No logs were read.

## Summary

The owner decision is carried out as far as it reaches.

- The rendered-comment emulation is gone:
  - `gen_toc_html.py` is deleted.
  - `_comment_after` is byte-identical to the base.
  - `blocks()` ends only FENCE and HTML with their container, never COMMENT.
  - Restoring either removed rule fails named arms (M04, M06).
- The unclosed raw-HTML comment family is stated as a directed limitation owned by #516. It appears in the `blocks()` docstring, CONTRIBUTING 6.1 lines 591-604 and DOC_GENERATION, and every comment and HTML-escape claim probed this round matches GitHub. The definition claim at 6.1:584 does not (F2).
- Family one agrees 51/51. The nine R86-5 descriptions map verbatim to named shapes. All 175 committed receipts re-render byte-identically today.
- Acceptance 2, 4 and 5 hold, and no ratchet is widened.
- On pure Markdown the container walk is strong: 1,910/1,910 changed pages are fixes, and 300/300 sampled unchanged pages agree.

The verdict is NEGATIVE for three reasons:

- **F1 (MAJOR).** The head regresses base-agreeing shapes outside the one family the amendment excludes. The author discloses this and asks for a decision; none has been recorded. This round's sweep finds 66 such regressions with no comment delimiter on the page at all, every one an escape.
- **F2 (MAJOR).** Two container-walk regression classes are not covered by any disclosure or decision:
  - a table hold that outlives an indented line;
  - definition-only items in definition forms outside `LINK_DEFINITION_RE`, including a lazy one-line bare definition that 6.1 says is handled.

  Both escape through the real em-dash gate where the base refused.
- **F3 (MINOR).** A new container-layer property has no failing arm.

## Findings

```text
[R238] MAJOR Conformance, Robustness - #437 acceptance 1 as amended 2026-09-23 14:15; scripts/gen_toc.py:423 (a fence or raw HTML block ends with its container), CONTRIBUTING.md:591-603; scripts/gen_toc_container_walk.json shapes "item block ends before a code span", "... before an escape", "... before an inline attribute", "item end uncovers an open quoted value", "item end uncovers a type-3 block", "item end uncovers a comment over a fence"; receipts/fixture_drift/SUMMARY.txt, receipts/fuzz/COMMENT-FREE-REGRESSIONS-4371.txt, receipts/fuzz/CLASSIFY-4371.txt, receipts/replay_prior_SUMMARY.txt, receipts/emdash_e2e_f1.txt - F1: shapes that agreed at the base regress outside the amended family, and no public decision accepts them
```

Requirement/evidence:

- **The amendment.** AC1's no-regression clause ("every shape that agreed at the base still agrees") now excludes only "shapes whose rendering depends on a raw-HTML comment the renderer leaves open" (issue body; 5794734885).
  - The owner's rationale places the remaining MAJOR "in the emulation ..., not in the container walk".
  - The #516 decision (5794735214) moves R237-3 F1/F3 and R238-2 F1/F3 there for modelling.
  - Neither text accepts regressions that the kept container walk causes outside the comment family.
- **The mechanism.** The container walk correctly ends a raw HTML block or fence with its list item (gen_toc.py:423). Where the base's unended block hid a residue by accident, the residue now shows. 6.1 says so at lines 602-603. The author's REVIEW READY counts 15 such pages outside the #516 family and asks "the reviewers and the owner" to decide.
- **Committed evidence.** Six fixture shapes carry `limitation` with `base_agreed: true` and are not among the six #516 resumed variants. Three are withholds: an opener GitHub prints as text, in a code span, after an escape and in an attribute. Three are escapes: an open quoted value, a type-3 block, and `<!-->` over a fence. Their renderings are byte-identical today (receipts/fixture_drift/).
- **Independent sweep.** Seed 4371 is a container, HTML, fence and comment vocabulary: 58,600 distinct pages. 1,359 differ between the base and head walks, and all were rendered: 1,082 fixes, 121 regressions and 156 wrong at both. These counts are not population rates.
  - 66 of the 121 regressions are on pages with no `<!--` and no `-->` at all, so none can depend on a comment. All 66 are escapes:
    - 24 open quoted value;
    - 23 type 3-5;
    - 10 `<select>`;
    - 8 mixed among those three;
    - 1 table hold (F2).
  - The rest carry comment tokens. Among single-class pages, 12 are `<!-->` withholds and 11 are openers GitHub prints as text.
- **Prior rows.** A replay of 2,825 recorded rows from R238-2 and R237-3 against the head leaves five that agreed at the base and disagree now:
  - R237-2 F2's three in-item rows (code span, escape, attribute): withholds. R237-2 F2 is not in the #516 owner move.
  - R238-2 sweep rows #668 and #672: type 3-5 escapes, uncovered when a raw HTML block ends with its item (type 1 `<script>` in #668, type 6 `<div>` in #672).
- **End to end, with real Git.** For the open-quoted-value, type-3 and comment-over-a-fence shapes, the head's `check_em_dash.judge_page` exempts the copied label `Old <U+2014> heading` (findings 0, exempt 1). GitHub renders no such heading. The base refuses it (findings 1, exempt 0).

Impact:

- A Contents label mirroring a heading GitHub does not render obtains the em-dash exemption and links to an anchor the page lacks. This is the escape direction #413 and #437 exist to close. The withhold rows drop real sections.
- Reach: 0 of 164 tracked pages (AC4). The triggers are malformed or unusual raw HTML.

Required change: one of these must be true.

- A public owner decision accepts these classes as named residues. It must state their direction, their boundary, and the fact that they regress base-agreeing shapes: an amendment of AC1, or an explicit exclusion recorded with an owning Issue. The classes are: open quoted value, types 3 to 5, `<select>`, an opener GitHub prints as text, `<!-->`, and any class F2 leaves in place.
- Or the head keeps the base's answer on them.

An author statement alone does not suffice (AGENTS.md section 2).

Verification:

- The decision text names each class above.
- Or `tools/fixture_drift.py`, `tools/fuzz_diff.py` (seed 4371) with `tools/classify.py`, and `tools/replay_prior.py` report zero base-agreeing regressions outside the amended family.

```text
[R238] MAJOR Conformance, RTL, Robustness, Tests, Docs - scripts/gen_toc_containers.py:190-206 (`_open` reads the leaf's paragraph state to decide whether a list item may interrupt), scripts/gen_toc.py:481-484 (`_paragraph_after` holds a table through any TEXT line), scripts/gen_toc_containers.py:163-166 and :236-239 with scripts/gen_toc.py:237-244 (definition-only items), CONTRIBUTING.md:579 and :583-586; probes/table_hold.json, probes/definitions.json, probes/lazy_definition.json, receipts/probe_table_hold.json, receipts/probe_definitions.json, receipts/probe_lazy_definition.json, receipts/emdash_e2e.txt, receipts/mutations.txt row M25 - F2: two container-walk classes regress base-agreeing shapes in both directions; one is undocumented, the other is documented inaccurately, and neither is pinned or disclosed
```

Requirement/evidence:

- **The bar.** AC1's no-regression clause, which the amendment does not relax for the container walk: the owner keeps the container walk in #437. CONTRIBUTING 6.1:579 says the container rules "are CommonMark's (sections 5.1 and 5.2)". 6.1:583-584 says an item holding only one-line definitions "with a bare destination and an optional double-quoted title" is empty once they close.

**(a) Table hold.**

- GFM ends a table at a line indented four or more columns, which starts indented code. `_paragraph_after` keeps the table's HELD state through that line and through the next plain line (gen_toc.py:484).
- `_open` then treats HELD as "no paragraph", so a list marker GitHub reads as a setext underline, or as paragraph continuation (`2. z`), opens an item (gen_toc_containers.py:193, :202).
- A fence at that item's column then ends with the phantom item. GitHub's fence runs on.

Fresh renders; each row gives the ATX headings listed by GitHub / the base walk / the head walk:

| Page | GitHub | Base | Head |
|---|---|---|---|
| T3 `\| a \| b \|\n\|---\|---\|\n    code\nTitle\n-\n  ```\n## Old\n```\n\n## Real\n` | Real (Old is code) | Real | Old |
| T4 `text\n\|-\|\n    x\ny\n2. z\n   ```\n## Old\n```\n\n## Real\n` | Real | Real | Old |
| T8 the T3 shape after `## Top` and a body row | Top, Real | Top, Real | Top, Old |
| T2 `text\n\|-\|\n    x\ny\n-\n   ~~~\n\n## H1\n` | none | none | H1 |
| control T5 (no indented line) | H1 | none | H1 |

- T3's response is: `<table>...</table>`, `<pre><code>code`, `<h2>Title</h2>`, `<pre><code>## Old`, `<h2>Real</h2>`.
- The head lists a heading GitHub renders as code and omits the one GitHub renders.
- The seed-4371 sweep hit this class once (s4371-56012), and it was its only regression carrying no documented hazard.
- 6.1, the docstrings and the author's inventory do not name it.

**(b) Definition-only items.**

- `LINK_DEFINITION_RE` reads only a one-line definition with a bare destination and an optional double-quoted title, on the item's own content line.
- The lazy branch fills the item unconditionally (gen_toc_containers.py:165).
- So each of these keeps a definition-only item open, where GitHub empties it and ends it at the second blank line:
  - a single-quoted title;
  - a parenthesized title;
  - an angle-bracket destination;
  - a title on the next line;
  - a one-line bare definition on a lazy line (`- [a]: /u\n[b]: /v`).
- All ten probes, a fence form (escape) and a tag form (withhold) for each of the five, agree at the base and disagree at the head. The double-quoted and indented bare controls agree at both.
- The lazy bare case contradicts 6.1:584.
- No committed shape pins any of these forms, so mutation M25 (accept a single-quoted title) survives both self-tests.
- The author's REVIEW READY inventory of "15 regressions outside the #516 family" omits this class and (a).

**End to end, with real Git** (receipts/emdash_e2e.txt). T3, T4, the angle-destination, single-quoted and lazy-definition escapes are each exempt at the head (findings 0, exempt 1). The base refuses each (1, 0). The handled double-quoted control is refused at both.

Impact:

- Escape: a copied em-dash label is exempt for a heading GitHub renders as code, and the generated Contents links a missing anchor.
- Withhold: a rendered section is dropped from the list.
- Reach: 0 tracked pages, and the shapes are uncommon.
- This defect is in the container walk itself, the part the owner decision keeps in #437 and expects to close with MINORs only.

Required change: either the walk agrees with GitHub on (a) and (b), or a public owner decision accepts them as named residues with direction and boundary (joining F1's decision). Either way:

- 6.1 states only what holds, at 579 and 583-586, and names (a) if it remains;
- a committed shape or arm pins each remaining class;
- an arm fails when the new rule is reverted.

Verification:

- `tools/probe.py` over probes/table_hold.json, probes/definitions.json and probes/lazy_definition.json: every base-agreeing row agrees, or is pinned under the recorded decision.
- `tools/emdash_e2e.py` refuses every escape row at the fix head.
- `tools/mutate.py` shows M25 killed or equivalent.

```text
[R238] MINOR Tests - scripts/gen_toc_containers.py:230-231 (in the container layer an inline comment starts no block), scripts/gen_toc_container_cases.py; receipts/mutations.txt row M21, receipts/survivor_equivalence.json, receipts/probe_m21.json - F3: a new container-layer property has no arm that fails when it is removed (acceptance 3)
```

Requirement/evidence:

- Acceptance 3: "Each new property carries an arm that fails when the property is removed."
- Mutant M21 deletes the rule that a comment opened after text, or four columns in, starts no block in the layer's leaf machine. It passes `gen_toc.py --selftest` 1269/1269 and `check_em_dash.py --selftest` 429.
- It is not equivalent. Over 135,550 sweep and fixture pages it changes the headings of three. All three were rendered:
  - on `text \<!-- more\n1) item\n  [b]: /v\n- - x\n-->\n\n    text\n  ```\n    text\n\n## H1\n`, GitHub and the head list H1 and the mutant lists none;
  - on a second page the mutant escapes;
  - on a third it happens to agree where the head withholds (a shared base comment-reading withhold).

Impact: a later edit can drop the rule with every gate green, which changes navigation in both directions.

Required change: an arm fails when the rule is removed.

Verification: `tools/mutate.py` reports M21 KILLED at an arm named for the property, and M01-M29 other than the equivalent survivors stay killed.

```text
[R238] SUGGESTION Docs - CONTRIBUTING.md:587 - S1: "`<!--` opens one until the next `-->`, wherever it sits" omits the qualifier the docstring carries (gen_toc.py:395-396: "outside a fence, raw HTML block or code")
```

A reader could take a `<!--` inside a fence to open a comment. The walk does not, and the probe "comment wherever it sits: in a fence opens none" agrees with GitHub. This is optional wording, and no lens is affected.

```text
[R238] SUGGESTION Tests - receipts/removed_shapes.txt - S2: the ten removed closure-rule controls could stay as `limitation` shapes
```

At this head both walks withhold on all ten, identically, where GitHub shows both headings. The fixture's own rule marks every shape the walk answers differently as `limitation`; keeping them would pin the base comment reading's withhold on those exact bytes. Other shapes and M06 already pin the rule, so this is optional.

## Clean results that support the ledger

These are recorded in the finding format for the artifacts examined. They do not clean the lenses F1 to F3 leave open.

```text
[R238] PASS Conformance (partial, AC1 family one) - scripts/gen_toc_family_one.json, receipts/fixture_drift/SUMMARY.txt - 51 shapes: bullet, star, ordered and two-digit ordered at and past the content column; inline and unknown tag; outside and inside the item; the two-digit below-column boundary; one space, four spaces, block quote, footnote at two and four, tab. Nine `r86_5` fields quote R86-5's nine descriptions verbatim, one per named shape. 175/175 committed requests reproduced by an independent encoder and re-sent: responses byte-identical today; head agrees 51/51; every family-one shape that agreed at the base still agrees (36), 15 fixed
[R238] PASS Conformance (partial, owner decision) - scripts/gen_toc.py:423 and :487-539, deleted scripts/gen_toc_html.py, receipts/mutations.txt rows M04 and M06 - the emulation is removed: `_comment_after` and `_still_open` bodies are byte-identical to the base; COMMENT never ends with its container; restoring either rule fails named arms; every limitation record in the three fixtures matches the measured head walk and its `base_agreed` matches the measured base walk
[R238] PASS Conformance (partial, container walk on Markdown) - receipts/fuzz/SUMMARY-5162.txt, SUMMARY-5162-same.txt, receipts/probe_hardcoded_rows.json - Markdown-only sweep seed 5162: 1,910/1,910 changed pages are fixes, 0 regressions; 300/300 unchanged pages agree; all 197 hard-coded `probe_rows()`/`correction_rows()` expectations match fresh GitHub renders
[R238] PASS Conformance (AC2) - receipts/probe_doc_claims.json rows F2*, scripts/gen_toc_container_cases.py:294-301, CONTRIBUTING.md:572-577 - the five family-two forms render as headings on GitHub; both walks omit them; the limitation names each with its direction
[R238] PASS Conformance (AC4) - receipts/ac4_tracked_pages.txt - 164 tracked pages, 46,734 lines: 0 blocks() label and 0 headings() differences between the base and head walks
[R238] PASS Conformance (AC5) - receipts/gates/SUMMARY.txt and 01-28 - gen_toc --selftest 1269/1269, --check 106 pages, --verify-anchors 144; check_em_dash --selftest 429, --base ede8d48e 0 findings over 39 added lines; docs_check and --selftest, check_doc_style and --selftest, check_py_idiom (long module 10<=10, long function 9<=9, parameters 7<=7, over-long line 0<=0) and --selftest, hygiene, TODO ownership, control flow, cohesion, naming, fail fast, test evidence, doc paths, DOC_MAP, archive, git diff --check: all exit 0; no budget file in the diff; gen_toc.py 999 lines (<= 1,000)
[R238] PASS RTL (product scope) - receipts/product_scope.txt, receipts/hosted_check_runs.tsv - no HDL, testbench, constraint, workflow, synthesis, budget, .gitmodules or gitlink change; four gitlinks identical at base and head; clock, reset, CDC, width and backpressure have no artifact here. The lens stays UNCLEAN through F2's architecture scope (the layer and leaf-machine paragraph-state contract)
[R238] PASS Tests (partial) - receipts/mutations.txt, receipts/mutations_extra.txt - 29 reviewer mutations: 24 killed at arms named for their property (e.g. `I437 rendered R238-2 F2 C17 ...`, `I437 rendered R237-3 F4 a blank line ends a quote`, `I437 rendered type-3 block leaves the gate to the walk`, `I437 rendered R237-3 F2 definition-only item ends at a second blank`, `I437 two spaces`); survivors M13, M14 and M26 change no heading on 135,550 pages (equivalent as measured); M21 is F3; M25 is F2(b)
[R238] PASS Docs (partial) - receipts/probe_doc_claims.json, CONTRIBUTING.md:586-604, scripts/gen_toc.py:385-416, docs/DOC_GENERATION.md:30,60-61 - the unclosed raw-HTML comment limitation is stated with owner (#516), direction (lists, ESCAPE) and boundary (an opener in a raw HTML block or four columns into an item, a closer GitHub prints as text; a comment closed in its own block agrees); unclosed tag, bogus comment, open quoted value, `<select>`, type 3-5 and empty-comment claims each match GitHub; the lists are stated as measured, not exhaustive
```

## Acceptance at this head

| Criterion | Result | Evidence |
|---|---|---|
| AC1 (as amended) | NOT MET | Family one 51/51 and the nine mappings hold. The no-regression clause fails outside the amended family (F1, F2) |
| AC2 | MET | five forms named with direction; GitHub renders each; both walks omit |
| AC3 | NOT MET | M21 behavioural and unarmed (F3); F2's classes unpinned (M25) |
| AC4 | MET | 0 differences over 164 pages |
| AC5 | MET for the named gates | 28 focused commands exit 0; no ratchet widened |

## Prior public findings at this head

| Finding | Severity; lenses | Disposition at 34f124f9 | Evidence |
|---|---|---|---|
| R237-r1 F1: tag inside the resumed item paragraph | MAJOR; Conformance, Robustness, Tests | RESOLVED | family one 51/51; the column 0-4 open, close and attribute rows match GitHub; M05 killed at `I437 two spaces` |
| R237-r1 F2: eleven historical cases | MAJOR; Conformance, Tests, Docs | RESOLVED against amended AC1 | 51 shapes, nine verbatim R86-5 mappings, 175/175 byte-identical re-renders |
| R237-r1 F3: block-marker inertness unarmed | MAJOR; Conformance, Tests | RESOLVED | three `R237 ...-marker-indented-closer` rows match GitHub; M27 killed |
| R238-r1 F1: content-column tag, C01-C08, P01, P04 | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED | all rows match fresh renders (receipts/hardcoded_rows_SUMMARY.txt) |
| R238-r1 F2: dedented quote or footnote, D01-D07 | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED | all rows match fresh renders |
| R238-r1 F3: item HTML outlives the item | SUGGESTION; Conformance, Robustness | RESOLVED | M01-M03 killed; 1,082 seed-4371 fixes |
| R237-2 F1: gate whatever holds the item; in-item block never ends | MAJOR; all five | RESOLVED | batch4_prior rows agree apart from R237-2 F2's; M01-M05 killed |
| R237-2 F2: flag on any `<!--` substring | MAJOR; all five | RETAINED IN PART under this round's F1 | 7 of 10 published rows agree. The three in-item rows (code span, escape, attribute) withhold where the base agreed. They are neither in the amended family nor in the #516 owner move |
| R237-2 F3: empty-item guard unarmed | MINOR; Tests | RESOLVED | M07, M08 killed |
| R237-2 S1: opener four columns into an item | SUGGESTION; Conformance, Robustness | documented limitation owned by #516 | 6.1:594; fixture shape pinned as `limitation` |
| R237-3 F1: rendered-comment model regressions | MAJOR; all five | RESOLVED for its published rows; modelling moved to #516 by the owner | emulation removed. Replay of 1,524 R237-3 rows: 0 base-agreeing rows disagree. E1, E1b, E2, E2b, E5, E5b, E6, E6b, E8 and E9 answer as at the base |
| R237-3 F2: definition-only item outlives a second blank | MINOR; Conformance, RTL, Robustness, Tests | RESOLVED for E7 and one-line bare forms; the same mechanism for other forms is RETAINED as this round's F2(b) | E7 agrees; M09 killed; ten probes regress |
| R237-3 F3: escape inventory incomplete | MINOR; Conformance, Robustness, Docs | docs RESOLVED; modelling moved to #516 by the owner | 6.1:597-604 names the classes and says the list is measured |
| R237-3 F4: quote end at a blank line unarmed | MINOR; Tests | RESOLVED | M22 killed at `I437 rendered R237-3 F4 a blank line ends a quote` |
| R238-2 F1: comment rules regress the base | MAJOR; all five | RESOLVED for published rows (a) to (d); sweep rows #668 and #672 still regress and are carried in F1 | replay of 1,301 R238-2 rows: 5 regress, 3 of them R237-2 F2's; (d) M18 killed |
| R238-2 F2: C17, H06, H10 unarmed | MINOR; Conformance, Tests | RESOLVED | C17 = M19 killed at its arm; H06 and H10 left with the HTML stage |
| R238-2 F3: "Two escapes remain" is false | MINOR; Docs | docs RESOLVED; modelling moved to #516 by the owner | the claim is gone; `<select>` named; list stated as measured |
| R238-2 S1: per-call registration and import | SUGGESTION; RTL | not adopted (optional) | gen_toc.py:418-419 |
| #516 twelve variants | manager-tracked | inside the amended family | six resumed regress and are pinned `base_agreed: true`; six first-paragraph disagree at both |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | issue #437 AC1-AC5 as amended, #516 decision, R86-5; three fixtures (175 re-sends); seeds 4371 and 5162 (3,569 renders); 2,825 replayed prior rows; 164 tracked pages; gates 01-28 | none clean; applied by R238-3 | 34f124f9b0dabeb74c655052f0a0858620a09037 |
| RTL | UNCLEAN (F2) | `blocks()` owner/gate contract gen_toc.py:418-434; gen_toc_containers.py in full; product-scope raw diff and gitlinks; hosted contexts listed | none clean; applied by R238-3 | 34f124f9b0dabeb74c655052f0a0858620a09037 |
| Robustness | UNCLEAN (F1, F2) | malformed and unterminated raw HTML, tables, definitions, lazy lines, empty items, tabs, blank-line boundaries across both sweeps and probe sets | none clean; applied by R238-3 | 34f124f9b0dabeb74c655052f0a0858620a09037 |
| Tests | UNCLEAN (F2, F3) | gen_toc_container_cases.py in full; 29 mutations; survivor equivalence over 135,550 pages; 197 hard-coded rows against GitHub; the em-dash consumer through real Git | none clean; applied by R238-3 | 34f124f9b0dabeb74c655052f0a0858620a09037 |
| Docs | UNCLEAN (F2) | CONTRIBUTING.md:572-606, gen_toc.py docstring :385-416, gen_toc_containers.py:4-42, DOC_GENERATION.md:30,60-61, fixture `about` fields, author REVIEW READY inventory; doc claims probed against GitHub | none clean; applied by R238-3 | 34f124f9b0dabeb74c655052f0a0858620a09037 |

No lens is covered clean at this head, so the completion bar of AGENTS.md section 7 is not met.

## Hosted evidence at this head (list only, logs not read)

- 22 check runs are recorded at `34f124f9`. 21 executed and concluded `success`:
  - rtl-fast, changes, docs-check, docs-check-no-git, elaborate, verilator-lint, bdd-conformance, wire-accountability;
  - Verilator shards 0-4 and verilator-suites;
  - Yosys shards 0-3, yosys-elaboration and yosys-portability;
  - full-ci-gate.
- One context, `Physical gPTP (nightly and manual)`, is SKIPPED. It is not hardware proof.
- The manager owns hosted and local-replica acceptance (receipts/hosted_check_runs.tsv).

## Real limits

- Sweep counts are stratified toward pages where the walks differ, so they are not population rates. The vocabularies are this round's own, and other classes may exist.
- Hazard classes are assigned by token. F1's 66 comment-free rows are certain to fall outside the comment family. The attribution of the other 55 regressions among comment classes is by token and was not ablated.
- The prior-row replay uses the renderings those rounds recorded. The byte-identical re-send of all 175 fixtures is the evidence that GitHub's responses are stable. Those rows were not re-rendered.
- Only the named focused gates were run. The manager's full static, builder and native banks, act, and the current-candidate build were not run and are not claimed. Verilator was not used, because no RTL changed.
- Physical calibration was NOT RUN. No field skip is hardware proof.
- One reviewer gate run left an ignored `scripts/__pycache__/` in the clone. It was removed, and the clone re-verified:
  - status is empty;
  - the index tree equals `bb9b3dbc`;
  - there are no assume-unchanged or skip-worktree flags;
  - 0 raw-byte blob mismatches;
  - modes intact;
  - four gitlinks at stage 0 unchanged (receipts/clone_integrity.txt).

## Pending manager duties

- Obtain and publish an owner decision on F1's classes, and on F2's if they are not fixed, or assign a correction.
- Run the full source static, builder and native banks at this head. Build the current-dev candidate at the merge turn.
- Accept or refuse the hosted contexts and the local replica.
- Keep the #516 and #495 dispositions.
- Publish this packet: REPORT.md and the MANIFEST.sha256 entries.

## Reproduction

`tools/` holds portable scripts; `probes/` holds every probe page.

- `run_gates.sh <checkout> <out> <base>`: the focused gates.
- `fixture_drift.py`: re-send and score the fixtures.
- `fuzz_diff.py <head-scripts> <base-scripts> <out> <seed> <count> <cap>` with `FUZZ_VOCAB=markdown` for seed 5162, and `classify.py`.
- `probe.py`, `replay_prior.py`.
- `mutate.py`, `equivalence.py`.
- `emdash_e2e.py`.

Renders go through GitHub's Markdown API (`POST /markdown`, mode `gfm`, context `kebag-logic/milan-fpga`) and are cached by request hash in `receipts/renders/`.

R238-3 FINISHED

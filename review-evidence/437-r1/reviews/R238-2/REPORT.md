[R238] NEGATIVE - exact head e4906bfca65c61e7e109e3532ac1b2dd5b4c0096

# [R238] round 2: issue #437 / PR #515, external cleared-context review

## Head under review

- Commit `e4906bfca65c61e7e109e3532ac1b2dd5b4c0096`, tree
  `f5d2e8c022d39684f458f7d2d0ee97b350533353` (receipts/head.txt,
  receipts/integrity_final.json).
- Source base and merge base: `574c29fa111c74e5e5ed63e4670aff1f492e28e2`. The
  lane's original base is `88e9276b2a220c716f64a843f7e1eb8f9265e896`. Its
  `scripts/gen_toc*.py` and `check_em_dash.py` are byte-identical to
  `574c29fa`'s, so "the base walk" below means both.
- Integration merge `ef39ecc4` is disjoint. No path is in both sets. The
  issue patch is byte-identical before and after it: SHA-256
  `1bd01330338539eb11432a1c05e064ac11ebe9080cf7014a388abbec0a0afb9b` for
  both `483a133e..4741498f` and `574c29fa..ef39ecc4`. Every commit has a
  one-line subject and no body or trailer.
- Diff `574c29fa..e4906bfc`: 11 paths. They are CONTRIBUTING.md,
  docs/DOC_GENERATION.md, scripts/check_em_dash.py (self-test wiring only),
  scripts/gen_toc.py and scripts/gen_toc_cases.py, three new modules
  (scripts/gen_toc_containers.py, scripts/gen_toc_html.py and
  scripts/gen_toc_container_cases.py), and three new fixtures. There is no HDL,
  testbench, workflow, constraint, budget, `.gitmodules` or gitlink change.
- Live refs at 2026-09-23T12:07Z: the branch is at this head. `dev` is at
  `ede8d48ecd7c7f589a14b957951f040d92c99c70`, 12 commits past the source
  base (receipts/remote_refs.txt, receipts/live_dev_delta.txt).

## What was read, in order

1. AGENTS.md, CONTRIBUTING.md (sections 2, 3, 5, 6 and 6.1), docs/README.md,
   and docs/development/CODE_QUALITY.md rules 1 and 12.
2. Issue #437: the body, including restated acceptance 1 and its original
   wording. Then every [A10], [A168], [A172], [A184] and [A190] comment,
   including:
   - the implementation choice 5775771538;
   - the maintainer restatement 5788996063;
   - the rendered-comment decision 5789133990;
   - the container-walk decision 5791031813;
   - REVIEW READY 5791751430.
3. CommonMark 0.31.2 sections 4.6, 5.1, 5.2 and 6.6. The GFM tag filter.
   HTML's tokenizer states for comments, bogus comments and attribute values.
4. The diff `574c29fa..e4906bfc` and its history.
5. Executable evidence:
   - the author packet `review-evidence/437-r1/correction-a190/` at evidence
     commit `d2e01fec`, with its scripts, receipts and handoff;
   - the manager's issue and PR comments;
   - the exact-head hosted check-run list.
6. Only after my independent pass over the diff, with F1 and F2 already
   measured: the published text of R237-r1 (5777954062), R238-r1 (5778167234)
   and R237-2 (5790354117). Those are read solely to give their dispositions.
   Before that point, the only view of them was the title-level summaries in
   the issue's manager and author comments. No reviewer archive under
   `review-evidence/437-r1/reviews/` was opened, and no concurrent round-3
   material was read.

**Oracle.** GitHub's Markdown API (`POST /markdown`, mode `gfm`, context
`kebag-logic/milan-fpga`) was sent synthetic pages only, on 2026-09-23 between
11:23 and 12:10 UTC.

- Every receipt row keeps the page and the exact request. Rows from
  `probe.py`, the fixture re-render and the sweeps also keep the response
  bytes and both SHA-256 values.
- Requests rejected by the API's secondary rate limit were re-sent one at a
  time until each succeeded (scripts/rerender_failed.py). No row in a
  published receipt is a failed render.
- Heading presence is read from the returned HTML. The API returns no anchor
  `id` attributes, so anchors were not measured.

**Terms.** A regression is a page that agreed with GitHub at the base and
disagrees at the head. An escape is a heading GitHub does not render that the
walk lists. Withholding is the opposite: a heading GitHub renders that the
walk omits.

## Summary

The container layer is sound on everything the lane set out to fix.

- Restated acceptance 1's shape set:
  - 51 family-one shapes, each of the nine R86-5 descriptions mapped;
  - 40 comment controls, including the twelve #516 variants;
  - 71 container-walk shapes.
  All 162 re-render byte-identical today, and the head walk agrees with each.
- An independent 2,052-page container, tag-column and follower matrix has
  0 regressions and 750 fixes.
- A 60,000-page seeded sweep without type 3 to 5, processing-instruction or
  CDATA fragments has 0 regressions and 1,490 fixes.
- Every published shape of every prior finding agrees at this head.
- AC2, AC4 and AC5 are met.

The rendered-comment and prose-comment rules added in this round regress the
base, though, in the escape direction. Where the base agreed with GitHub, this
head lists headings GitHub hides after these constructs:

- an inline processing instruction or CDATA section in prose;
- raw HTML pieces from different containers;
- the declared type 3 to 5 blocks.

It also withholds headings after a tag line inside a type 3 to 5 block. A seeded
1,200-page sweep with those fragments finds 303 regressions, and the copied
em-dash label is exempt end to end (F1). Three new properties of the HTML stage
and the container layer have no arm that fails when they are removed (F2). The
documentation states a closed list of remaining escapes, and that list is
measured false (F3).

## Findings

```text
[R238] MAJOR Conformance, RTL, Robustness, Tests, Docs - scripts/gen_toc.py:414-427 (the prose-comment end rule at :416 and :425, the gate at :422), scripts/gen_toc_html.py:24-27 and :121-139, scripts/gen_toc_containers.py:169-178, CONTRIBUTING.md:526-539; probes/batch1.jsonl, probes/batch2.jsonl, probes/fuzz_seed238_complete.jsonl, receipts/fuzz_regression_summary.txt, receipts/emdash_probe_{base,head}.jsonl, receipts/emdash_probe2_{base,head}.txt, receipts/emdash_probe3_{base,head}.txt, receipts/navigation_consumer_pi.txt - F1: the rendered-comment and prose-comment rules regress shapes the base answered correctly; the head lists headings GitHub hides behind a comment opened by inline raw HTML, by raw pieces from different containers, and inside the declared type 3-5 blocks, and it withholds headings after a tag line inside a type 3-5 block; the copied em-dash label is exempt on every escape
```

Requirement/evidence:

- **The bar.** Restated AC1 requires that "every shape that agreed at the
  base still agrees" (#437, 5788996063). The manager holds that bar beyond
  the shape set: R238-r1 F1/F2 "stay open MAJOR" under it. The author's own
  takeover commits to "Every page that agreed with GitHub at the base must
  still agree" (5790805814). REVIEW READY claims "0 regressions" over 28,056
  checks (5791751430).
- **The renderer.** CommonMark 0.31.2 section 6.6 accepts
  `<? ... ?>` and `<![CDATA[ ... ]]>` as inline raw HTML, which GitHub emits
  verbatim. HTML's tokenizer ends each as a bogus comment at the first `>`.
  A later `<!--` then opens a real comment, and that comment hides the rest
  of the page.
- **Four measured mechanisms, with fresh renders.** Each row gives the
  headings listed by GitHub / the base walk / the head walk.

(a) Inline raw HTML opens a comment. The head ends a prose-opened column-0
comment at the first line that is not paragraph text (gen_toc.py:416 and :425).
`hidden_lines` then assumes Markdown text "can open nothing"
(gen_toc_html.py:24-27, :132-133). The base kept the comment open to `-->`.

| Page | GitHub | Base | Head |
|---|---|---|---|
| `text <? > <!-- ?>\n\n## X\n\n## Y\n` | none | none | X, Y |
| `text <![CDATA[ > <!-- ]]>\n\n## X\n\n## Y\n` | none | none | X, Y |
| `- text <? > <!-- ?>\n\n## X\n\n## Y\n` | none | none | X, Y |
| `text <? > <!-- ?>\n## X\n\n## Y\n` | none | none | X, Y |
| control: `text <? <!-- ?>\n\n## X\n\n## Y\n` | X, Y | none | X, Y |

GitHub's response for the first row is `<p dir="auto">text  </p>`.

(b) Raw pieces from different containers are read as one run
(gen_toc_html.py:130-131, :135-136). GitHub emits `</li>\n<li>` or
`</ul>\n<blockquote>` between the pieces. That `>` ends the bogus comment, so
the `<!--` opens a comment. The model's bogus comment swallows the opener
instead.

| Page | GitHub | Base | Head |
|---|---|---|---|
| `- <!X y\n- <!--\n\n## X\n\n## Y\n` | none | none | X, Y |
| `- <? x\n- <!--\n\n## X\n\n## Y\n` | none | none | X, Y |
| `- <![CDATA[ x\n> <!--\n\n## X\n\n## Y\n` | none | none | X, Y |
| control: `- <!X y>\n- <!--\n\n...` | none | none | none |

(c) The declared type 3 to 5 residue appears where the base agreed. The
container layer knows these lines are inside a raw type 3 to 5 block
(gen_toc_containers.py:227-230). `blocks()` still labels them prose. The new
prose rule, the owner rule and the `<!-->` change remove the base's agreement.

| Page | GitHub | Base | Head |
|---|---|---|---|
| `<? x\n- <!--\n## X\n\n## Y\n` | none | none | X, Y |
| `<? x\n<!-->\n## X\n\n## Y\n` | none | none | X, Y |
| `<![CDATA[\n> <!--\n## X\n\n## Y\n` | none | none | X, Y |
| control: `<? x\n## X\n\n## Y\n` | none | X, Y | X, Y |

The control is the residue as declared, identical at base and head.

(d) A tag line inside a type 3 to 5 block opens a type-7 block. This is
withholding. `_inside` answers `gate` NO_PARAGRAPH for every line inside a raw
block (gen_toc_containers.py:178). `blocks()` passes that gate to the column-0
leaf machine (gen_toc.py:422). That machine labels the type 3 to 5 line prose,
so it opens type 7 on the tag and swallows the next heading.

| Page | GitHub | Base | Head |
|---|---|---|---|
| `<!X y\n<b>\n## X\n\n## Y\n` | X, Y | X, Y | Y |
| `<? x\n<span>\n?>\n## X\n\n## Y\n` | X, Y | X, Y | Y |
| `<![CDATA[\n<span>\n]]>\n## X\n\n## Y\n` | X, Y | X, Y | Y |
| control: `<? x\ntext\n?>\n## X\n\n## Y\n` | X, Y | X, Y | X, Y |

- **Sweep with all fragments (seed 238).** 39,784 unique pages, of which
  7,595 differ between the walks. 1,200 of those were rendered: 303
  regressions, 858 fixes and 39 wrong at both. The 303 break down as 277
  escapes carrying the inline-PI fragment, 23 type 3-5 escapes and 3 type 3-5
  withholdings (receipts/fuzz_regression_summary.txt).
- **Sweep without type 3-5, PI or CDATA fragments (seed 4372).** 1,500
  rendered: 0 regressions. So the regressions are confined to these
  constructs.
- **The author's corpora.** They carried the PI, CDATA and declaration
  openers only as raw lines (correction-a190/scripts/gen_probes.py:97-101,
  :204-205). They never placed them inline after prose, and never split them
  across containers.

Impact:

- **Em-dash exemption, real Git.** For every escape shape in (a), (b) and (c),
  the head's `check_em_dash.judge_page` exempts the copied label
  `Old <U+2014> heading`: `findings=0 exempt=1`. The base refuses it with
  `mirrors no heading`: `findings=1 exempt=0`. In (d) the head refuses a
  legitimate label that the base exempts.
- **Navigation.** On the inline-PI page, the head's `gen_toc.apply()` writes a
  Contents block linking `#alpha`, `#beta` and `#gamma`. GitHub renders none
  of those headings. The base writes nothing (receipts/navigation_consumer_pi.txt).
- **Documentation.** The docstring claim that text "can open nothing"
  (gen_toc_html.py:27) is false. So is CONTRIBUTING.md:526-527 ("Otherwise it
  opens raw HTML") for lines inside a type 3-5 block. CONTRIBUTING.md:536
  ("Two escapes remain, both already in the base walk") is false for (a) to
  (c).
- **Reach.** The tracked corpus is not reached today. 0 lines in 164 pages
  carry `<?`, `<![CDATA[` or `<!` plus an uppercase letter
  (receipts/census_types35.txt), and AC4 is unchanged.
- **Severity.** MAJOR, not MINOR: the change itself introduces escapes that
  obtain the exemption, on shapes the base answered correctly. That is the
  same class and rationale as R238-r1 F1/F2 and R237-2 F1. It is not a
  BLOCKER because no tracked page reaches it.
- **Lenses.** RTL covers this defect through its architecture scope:
  - the prose-comment transition (a);
  - the raw-run model (b);
  - the `gate` contract between the container layer and the leaf machine (d).
  Product RTL is untouched.

Required outcome:

- No page that agreed with GitHub at the base disagrees at the fix head. At
  minimum, (a) to (d) above and the 303 regression rows of
  probes/fuzz_seed238_complete.jsonl must agree.
- For (a), (b) and (d): the rendered comment must be opened by inline PI or
  CDATA as GitHub opens it. Raw pieces must be read with the container
  boundary GitHub emits between them. A line inside a raw type 3-5 block must
  not open a type-7 block.
- For (c), which touches the residue #437 declares out of scope, there are
  two routes:
  - keep the base's answer on these shapes, for example by treating lines the
    layer marks as inside a type 3-5 block as raw;
  - or publish the conflict, and have a public maintainer decision accept
    these specific regressions. An author decision alone does not suffice
    (AGENTS.md section 2).
- The docstrings and CONTRIBUTING.md 6.1 state only what holds.
- Arms fail when each repair is reverted.

Verification:

- Rerun scripts/probe.py over probes/batch1.json and probes/batch2.json: every
  row where the base agreed also agrees at the fix head.
- Rerun scripts/fuzz_diff.py with seed 238, then scripts/rerender_failed.py:
  zero `regression` rows.
- Rerun scripts/emdash_probe.py with probes/emdash_cases.json and
  probes/emdash_cases2.json: every escape case reads `findings=1 exempt=0` at
  the fix head.
- Rerun scripts/corpus_compare.py: still 0 differences.
- A mutant restoring each current rule fails a named arm.

```text
[R238] MINOR Conformance, Tests - scripts/gen_toc_containers.py:173-174 (a type 3-5 block ends at its end marker), scripts/gen_toc_html.py:50 (`<?` is a bogus comment) and :130-131 (a raw run is read whole across its lines); receipts/mutations_r238.json rows C17, H06, H10; probes/batch3.jsonl - F2: three new properties carry no arm that fails when the property is removed (acceptance 3)
```

Requirement/evidence:

- Acceptance 3: "Each new property carries an arm that fails when the
  property is removed." I ran 35 mutations, designed independently, in
  disposable copies (scripts/mutate.py). 30 are killed by both shipped
  self-tests, each at an arm named for its property.
- Three survive both self-tests: `gen_toc.py --selftest` 1244/1244 and
  `check_em_dash.py --selftest` 416. Each is observable against fresh GitHub
  renders, and the head is right on each (probes/batch3.jsonl):
  - **C17, a type 3-5 block never ends:**
    `<? x\n?>\n<div>\n<!--\n\n## X\n\n## Y\n`. GitHub renders none; the head
    lists none; the mutant lists X, Y (an escape).
  - **H06, `<?` is not a bogus comment:**
    `<div>\n<? a <!-- ?>\n</div>\n\n## X\n\n## Y\n`. GitHub, base and head
    list X, Y; the mutant lists none.
  - **H10, a raw run is read line by line:**
    `<div title="a\n<!--\nb">\n\n## X\n\n## Y\n` and
    `<div\ntitle="<!--">\n\n## X\n\n## Y\n`. GitHub, base and head list X, Y;
    the mutant lists none.
- Two further survivors, C03 and C06, changed no heading on any page I
  constructed. They are recorded as limits, not findings.

Impact: a later edit can remove any of the three properties with every gate
green. H06 and H10 would then regress base-agreeing pages, and C17 would
reintroduce an escape.

Required outcome: an arm fails for each of C17, H06 and H10, at the fix head.

Verification: rerun scripts/mutate.py. C17, H06 and H10 are killed at arms
named for their property, and the other 32 stay killed.

```text
[R238] MINOR Docs - CONTRIBUTING.md:536-539, scripts/gen_toc_html.py:30-34; probes/batch1.jsonl rows "select" and "raw open then link destination closer", probes/fuzz_seed4372_no35_complete.jsonl (a `both-wrong` row carrying `[x](<a-->)`) - F3: the documentation states a closed list of remaining escapes ("Two escapes remain") that is measured false even apart from F1
```

Requirement/evidence:

- CONTRIBUTING.md 6.1 now says "Two escapes remain, both already in the base
  walk". It names type 3-5 blocks labelled prose, and raw HTML that ends
  inside an unclosed tag, bogus comment or quoted value.
- The HTML stage's "What it does not model" (gen_toc_html.py:30-34) adds only
  foreign content's CDATA and DOCTYPE identifiers.
- Two further escapes exist at both base and head, so they are not
  regressions:
  - `<select>\n\n## X\n\n</select>\n\n\n## Y\n`: GitHub renders only Y, and
    both walks list X, Y. This is HTML tree construction inside `<select>`.
  - `<div>\n<!--\n\n[x](<a-->)\n\n## X\n\n## Y\n`: GitHub renders none, and
    both walks list X, Y. `inline_closes` reads a link destination as inline
    raw HTML carrying a closer, though GitHub emits `href="a--"`. The same
    reading escapes in the seed-4372 sweep.
- CONTRIBUTING.md:533 says a closer counts "in inline HTML within prose". The
  walk also counts one inside a link destination.

Impact: a reader is told the escape direction is bounded to two named classes
when it is not. This is the documentation half of the concern R238-r1 F1/F3
raised: residues must be named with direction and boundary, not implied
closed.

Required outcome: the residue statements name what the walk still escapes,
with direction and boundary, or say plainly that the list is the measured set
and not exhaustive. F1's classes must not be described as closed.

Verification: read CONTRIBUTING.md 6.1 and the module docstrings at the fix
head against probes/batch1.jsonl and F1's rows.

```text
[R238] SUGGESTION RTL - scripts/gen_toc.py:406-408, scripts/gen_toc_containers.py:42-45 - S1: `blocks()` registers its module under `gen_toc` and imports the layer on every call, and the layer imports the leaf machine's private names (`_opens`, `_paragraph_after`, `_still_open`)
```

This is optional. A public leaf-machine entry point would make the module
contract explicit. So would a registration done once at import. The author
already notes that a probe copying `gen_toc.py` alone breaks. No lens is
affected.

## Clean results that support the ledger

These are recorded in the finding format for the artifacts examined. They do
not clean the lenses F1 to F3 leave open.

```text
[R238] PASS Conformance (partial) - scripts/gen_toc_family_one.json, receipts/fixtures_rerender_head.jsonl, receipts/fixture_base_check.txt - restated AC1's shape set: 51 shapes; bullet, star, ordered and two-digit ordered at and past the content column; inline and unknown tag; outside and inside the item; the two-digit below-column boundary; one space, four spaces, block quote, footnote at two and four, and tab; nine r86_5 descriptions mapped one to one; 162/162 fixture receipts hash-verified and byte-identical on fresh re-send; the head agrees with all 162; no fixture shape that agreed at the base disagrees
[R238] PASS Conformance (partial) - probes/matrix_base_vs_head.jsonl, probes/fuzz_seed4372_no35_complete.jsonl, probes/batch5_family_two.jsonl - the container layer against CommonMark 0.31.2 sections 5.1 and 5.2 as GitHub renders them: 2,052-page matrix (798 differ; 750 fixes, 0 regressions, 48 wrong at both, all the documented family-two setext heading); 1,500 rendered sweep pages, 0 regressions; the five family-two forms render as headings and both walks omit them, as documented (AC2)
[R238] PASS RTL (product scope) - `git diff --raw 574c29fa e4906bfc`, `git ls-files -s` gitlinks, receipts/integrity_final.json, receipts/hosted_check_runs.tsv - no HDL, testbench, constraint, workflow, synthesis, budget, .gitmodules or gitlink object changes; four gitlinks unchanged; the seven required contexts concluded success at this head with Verilator shards 0-4 and Yosys shards 0-3 executed, not skipped, so clock, reset, CDC, width and backpressure questions have no artifact here. The lens stays UNCLEAN through F1's architecture scope
[R238] PASS Tests (partial) - receipts/mutations_prior_r238.json - ten mutations restoring the root cause of each prior finding are all killed by the TOC self-test at named arms (for example `I437 R237 fenced-marker-indented-closer`, `I437 R238 D01`, `I437 labels nested quote, tag opens HTML`, `I437 rendered double-quoted attribute`, `I437 empty item ends at blank`); nine are also killed by the em-dash self-test
[R238] PASS Conformance (AC4) - receipts/ac4_{88e9276b,574c29fa,e4906bfc}_base_vs_head.json - refusals, blocks, line_kinds, headings with anchors, plan, existing() and generated_block are identical under the base and head walks on all 163, 164 and 164 tracked pages of the three trees
[R238] PASS Conformance (AC5) - receipts/exits.txt, receipts/py_idiom.log - 22 focused commands exit 0: gen_toc --selftest 1244/1244, --check 106 pages, --verify-anchors 144, --sites 34; check_em_dash --selftest 416, --base 574c29fa 0 findings over 28 lines, --base 88e9276b 0 over 377; docs, doc style, doc paths, Python idiom (long module 10<=10, long function 9<=9, parameters 7<=7, over-long line 0<=0), hygiene, test evidence, fail fast, cohesion, control flow, TODO ownership, git diff --check; no budget file changed; gen_toc.py 996, gen_toc_cases.py 992 and check_em_dash.py 995 lines, all under the 1,000-line module ratchet
```

## Prior public findings at this head

The published shapes are re-rendered at base, previous head `4741498f` and this
head in probes/batch4_prior.jsonl, 55 rows. The root-cause mutations are in
receipts/mutations_prior_r238.json.

| Finding | Severity, lenses | Disposition at e4906bfc | Evidence |
|---|---|---|---|
| R237-r1 F1: tag inside the resumed item paragraph | MAJOR; Conformance, Robustness, Tests | RESOLVED | 15 rows (col 0-4 x open, close, attribute) agree; mutation P06 killed at `I437 two spaces` |
| R237-r1 F2: eleven historical cases | MAJOR; Conformance, Tests, Docs | RESOLVED against restated AC1 | nine R86-5 descriptions mapped one to one; 51/51 re-render identical and agree (receipts/fixture_base_check.txt) |
| R237-r1 F3: block-marker inertness unarmed | MAJOR; Conformance, Tests | RESOLVED | three marker rows agree; P01 killed at `I437 R237 fenced-marker-indented-closer`, P02 and P03 at named precedence arms |
| R238-r1 F1: content-column tag, C01-C08, P01, P04 | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED | all ten agree; P06 killed |
| R238-r1 F2: dedented quote or footnote, D01-D07 | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED | all seven agree; P04 killed at `I437 R238 D01`, C07 at `I437 R238 D02` |
| R238-r1 F3: HTML block in an item outlives it (P02, P03, F09) | SUGGESTION; Conformance, Robustness | RESOLVED | P02, P03 and an F09-shaped page agree; P07 killed |
| R237-2 F1: gate whatever holds the item; in-item block never ends | MAJOR; all five | RESOLVED | three published pages agree; independent matrix 0 regressions; P05 and P07 killed |
| R237-2 F2: flag on any `<!--` substring | MAJOR; all five | RESOLVED for its ten published pages | all ten agree; P08 killed at `I437 rendered double-quoted attribute` and four more. F1 of this round is a different trigger and root cause (inline PI or CDATA, raw pieces across containers, type 3-5) |
| R237-2 F3: empty-item guard unarmed | MINOR; Tests | RESOLVED | the guard is gone and the property is structural (`_Box.filled`); both pages agree; P09 killed at `I437 empty item ends at blank` |
| R237-2 S1: opener four columns into an item | SUGGESTION; Conformance, Robustness | RESOLVED | both pages agree; P10 killed |
| #516 twelve variants | manager-tracked | RESOLVED | 12/12 agree at head; the six that agreed at the base still agree (receipts/issue516_variants.txt) |

## Acceptance at this head

| Criterion | Result | Evidence |
|---|---|---|
| AC1 restated: committed shape set, renderings recorded at the fix head, bullet, ordered and two-digit coverage, five agreeing boundaries, nine R86-5 shapes mapped, every shape agrees | met | family-one fixture, fresh re-render, fixture_base_check |
| AC1: every shape that agreed at the base still agrees | NOT met | F1 |
| AC2: five family-two forms named with direction | met | CONTRIBUTING.md:518-523, gen_toc.py docstring; batch5 renders |
| AC3: each new property has a failing arm | NOT met | F2 (C17, H06, H10) |
| AC4: tracked classification unchanged | met | 0 differences on three trees |
| AC5: gates pass, no ratchet widened | met locally | 22 commands exit 0; no budget change |

## Reviewer-owned ledger

Every lens was applied at this exact head. None is covered clean.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MINOR) | restated AC1-AC5 and the #437 decisions; CommonMark 0.31.2 sections 4.6, 5.1, 5.2 and 6.6 against 162 fixture re-sends and fresh renders (106 named probes, 1,200 + 1,500 sweep pages, 798 matrix pages); the base, previous-head and head walks | none; applied by R238-2 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |
| RTL | UNCLEAN (F1 MAJOR) | product scope: `git diff --raw 574c29fa e4906bfc`, gitlinks, integrity receipt, hosted shard list. Architecture scope: the `blocks()` state machine (gen_toc.py:406-428), the `Scope` contract and `_step`/`_inside`/`_leaf_line` (gen_toc_containers.py:57-251), `hidden_lines` (gen_toc_html.py:121-139) | none; applied by R238-2 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |
| Robustness | UNCLEAN (F1 MAJOR) | inline PI, CDATA and declarations; raw pieces across list items and quotes; type 3-5 blocks with tags and comments; lazy lines; empty items; tabs; nested containers; adversarial long pages (receipts/timing_probe*.txt, no super-linear case found) | none; applied by R238-2 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |
| Tests | UNCLEAN (F1 MAJOR, F2 MINOR) | every arm family in gen_toc_container_cases.py; 35 independent and 10 root-cause mutations; selftests 1244/1244 and 416; the author's probe generators | none; applied by R238-2 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |
| Docs | UNCLEAN (F1 MAJOR, F3 MINOR) | CONTRIBUTING.md:518-539; docs/DOC_GENERATION.md:29-30, :60-61; the gen_toc.py docstring :383-405; the gen_toc_containers.py and gen_toc_html.py docstrings; #437 decision and REVIEW READY comments | none; applied by R238-2 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |

A commit that touches the walk modules, their case tables or fixtures, or
CONTRIBUTING.md 6.1 un-covers every lens except, possibly, the product scope
of RTL.

## Hosted evidence at this head (list only, logs not read)

- All seven required contexts concluded `success`: rtl-fast, docs-check,
  wire-accountability, docs-check-no-git, elaborate, verilator-suites and
  yosys-portability.
- Verilator shards 0-4 and Yosys shards 0-3 executed. `full-ci-gate`,
  `changes`, `verilator-lint`, `yosys-elaboration` and `bdd-conformance`
  also succeeded.
- `Physical gPTP (nightly and manual)` is `skipped`, and a skipped context is
  not hardware evidence.
- The hosted gates run the shipped self-tests, which pass at this head, so
  they cannot see F1 or F2.
- Hosted and act acceptance stay with the manager
  (receipts/hosted_check_runs.tsv, listed 2026-09-23T12:07Z).

## Limits

- **Oracle.** The oracle is GitHub's sanitised Markdown API output as of
  11:23 to 12:10 UTC today. Anchors were not measured.
- **Sweeps.** The sweeps are seeded and bounded. Only pages where base and
  head differ were rendered, so escapes identical at both walks are
  characterised only where a named probe hit them (F3).
- **Untested survivors.** Mutations C03 (a whitespace-only line continues a
  footnote) and C06 (a type 3-5 opener counts as lazy) survive. They changed
  no heading on any page I constructed, and I claim nothing about them.
- **Not run.** No Verilator, Yosys, native, processor, gPTP or builder bank
  was run, because the change carries no RTL. The scoped Verilator binary was
  not used, so its identity was not checked.
- **Manager banks.** The manager's source static/builder and native banks
  for this head were still running. Nothing is claimed or inferred from them.
- **Candidate.** The final current-dev candidate was not built. Live dev
  `ede8d48e` touches `CONTRIBUTING.md` (a section 2 hunk near line 205;
  6.1 is near line 515), so the path intersection with this issue is not
  empty.
- **Hardware.** Physical calibration is NOT RUN. Field skips are not
  hardware proof.

## Pending manager duties

1. Return F1, F2 and F3 to the author lane. Where F1(c) touches the declared
   type 3-5 residue, obtain the public decision it requires. A new head needs
   all five lenses applied again.
2. Publish the manager's source static/builder and native bank results for
   the final head. Complete trusted act replication and the required hosted
   contexts on that head.
3. Build and gate the candidate against live dev at the merge turn. `dev` is
   now `ede8d48e`, and it touches CONTRIBUTING.md.
4. Obtain the internal and external positive reviews, then explicit
   maintainer merge authorisation.
5. After merge: containment and review-integrity audits, issue closure and
   Done.

## Boundaries observed

- **GitHub was read-only.** I made GETs, one `git ls-remote`, a shallow fetch
  of the public evidence commit into scratch, and the render endpoint with
  synthetic pages. I made no comment, review, label, metadata change, push or
  merge.
- **The review clone was not edited.** Gates ran there with `python3 -B` and a
  scratch TMPDIR. Walk revisions, mutants and fixture repositories lived only
  under scratch/, and each mutant was deleted after scoring.
- **Final integrity** (receipts/integrity_final.json):
  - HEAD and tree are exact;
  - 867 index records, and every blob matches the bytes on disk with the
    correct mode (821 regular, 42 executable, 4 gitlinks);
  - the index equals the HEAD tree, every `ls-files -v` flag is `H`, and no
    path is untracked or ignored;
  - the three required submodules sit clean at their gitlinks, and `external`
    is uninitialised.
- **Not used.** No Docker, act, `act_ci` or its self-test, install, privilege,
  hardware or sub-agent, and no author contact. At most 8 jobs ran at once.

## Reproduction

Run `scripts/reproduce.sh` with `CLONE` (a clean checkout of this head) and
`PACKET` (this directory). It reruns everything in order. `MANIFEST.sha256`
lists every published file.

| Script | What it does |
|---|---|
| `run_gates.sh` | focused gates |
| `corpus_compare.py` | AC4 on three trees |
| `probe.py` | named probes at base, previous head and head |
| `fuzz_diff.py`, `rerender_failed.py` | seeded sweeps |
| `matrix_diff.py` | container matrix |
| `emdash_probe.py` | real-Git em-dash gate |
| `rerender_fixtures.py`, `fixture_base_check.py` | fixture receipts |
| `mutate.py`, `mutate_prior.py`, `make_mutant.py` | mutations |
| `timing_probe.py` | adversarial timing |
| `integrity.py` | review-clone integrity |

R238-2 FINISHED

[R237] NEGATIVE - exact head e4906bfca65c61e7e109e3532ac1b2dd5b4c0096

Round R237-3, internal cleared-context review of issue #437 / PR #515.
Head `e4906bfca65c61e7e109e3532ac1b2dd5b4c0096`, tree
`f5d2e8c022d39684f458f7d2d0ee97b350533353`. Source base
`574c29fa111c74e5e5ed63e4670aff1f492e28e2`. The base's `scripts/gen_toc.py`
is the same blob as at `483a133e` and `88e9276b` (`b2013963`), so "the base
walk" below means all three. All five lenses were applied: Conformance, RTL,
Robustness, Tests and Docs. One MAJOR and three MINOR findings are open, so
every lens is UNCLEAN at this head. This is not merge approval.

Reconstructed from, in this order: AGENTS.md; CONTRIBUTING.md (2, 3, 5,
6.1); docs/README.md; issue #437 (body with restated acceptance 1, the
maintainer decision 5788996063, the assignments 5775771538, 5789003484 and
5790500052, the A190 DECISION 5791031813 and REVIEW READY 5791751430, the
tracking note 5778773475); issue #516; CommonMark 0.31.2 sections 4.6, 5.1,
5.2 and 6.6, and HTML's tokenizer states for comments, bogus comments and
attribute values; then `git diff 574c29fa..e4906bfc` and its history; then
executable evidence, including the author packet `correction-a190/` at
evidence commit `d2e01fec`. The verdict, findings and ledger below came from
this round's own pass over the diff. The prior public findings on PR #515
were read only after that pass, to give their dispositions. The concurrent
R238-2 round was not read.

## Summary

The container layer is sound on its core domain. The committed shape sets
hold: all 162 recorded shapes re-render byte-identical today, the head agrees
with every one, and no shape in them regresses. The five family-two forms
stay named. No tracked page changes classification. All 785 recorded pages
behind the prior public findings agree at this head. On a fuzz vocabulary of
containers, tags, comments, fences and tables, 1,000 fresh renders show 0
regressions, with 422 escaped headings and 1,229 withheld headings fixed.

The bar is still "no regression against the base" (#437 comments 5788996063
and 5789003484). The rendered-comment model breaks it in the escape
direction:

- F1: raw HTML that HTML's tokenizer reads differently from CommonMark leaves
  a comment open, and the head now lists the headings it hides. The first
  case is an inline processing instruction or CDATA section carrying `>`
  before `<!--`. The second is the two "base" escapes the docs declare. The
  base walk omitted these headings correctly, and the em-dash gate refused
  the copied label; the head exempts it.
- F2: a withholding regression. A list item holding only a link reference
  definition outlives a second blank line.
- F3: the escape inventory in CONTRIBUTING.md 6.1 is incomplete. The base
  shares these further escapes, but 6.1 says only two remain.
- F4: a load-bearing container rule has no failing arm.

## Findings

```text
[R237] MAJOR Conformance, RTL, Robustness, Tests, Docs - scripts/gen_toc_html.py:24-27 and :121-139 (Markdown text may only close the rendered comment), scripts/gen_toc.py:415-417 and :425 (a prose comment ends at the first non-paragraph line), scripts/gen_toc_html.py:30-33 and CONTRIBUTING.md:536-539 (the declared escapes "already in the base walk") - F1: headings GitHub hides are listed on pages the base walk answered correctly, and their copied labels are exempt
Requirement/evidence: the lane's bar is no regression against the base. The
  maintainer decision says "every shape that agreed at the base must still
  agree" (5788996063), and the assignment says "no regression against the
  base" (5789003484). CONTRIBUTING.md 6.1 grants the exemption only to a
  heading the base page renders. GitHub emits inline raw HTML verbatim
  (CommonMark 0.31.2 section 6.6), and the page's HTML parser then tokenizes
  it. That parser ends a bogus comment (`<?`, `<![CDATA[` outside foreign
  content) at the first `>`, and it ends a comment at `--!>`. After that it is
  back in data state, so a later `<!--` opens a comment that hides the rest of
  the page. Fresh gfm renders, with base and head walks
  (receipts/minimal.json, receipts/minimal2.json):
    E1  "Text <?p > <!-- ?> more.\n\n## Old\n"   GitHub `<p>Text  </p>` (no heading); base []; head [Old]
    E1b same with the heading on the next line      GitHub []; base []; head [Old]
    E2  "Text <![CDATA[ > <!-- ]]> more.\n\n## Old\n"   GitHub []; base []; head [Old]
    E2b "- item <?p > <!-- ?>\n\n## Old\n"            GitHub []; base []; head [Old]
    E8  "## A <?p > <!-- ?>\n\n## Old\n"              GitHub [A]; base omits Old; head lists Old
    E9  the PI in a table cell                       GitHub []; base []; head [Old]
  Mechanism: `hidden_lines` lets Markdown text only close the rendered
  comment ("it can open nothing, every inline comment being closed",
  gen_toc_html.py:27, :133). `blocks()` now ends the prose comment at the next
  non-paragraph line (gen_toc.py:416, :425). The base's flat toggle held that
  comment open and omitted the heading.
  The same exposure turns the two declared escapes into regressions:
    E5  "<![CDATA[\nx <!---> y\n\n## Old\n"          GitHub emits the rest raw (`" y\n\n## Old"`); base []; head [Old]
    E5b "t <!--\n\n<?x\n\n## Old\n"                   GitHub []; base []; head [Old]
    E6  "t <!--\n\n<div title='\n\n## Old\n"          GitHub []; base []; head [Old]
    E6b the same after "`x <!--`"                     GitHub []; base []; head [Old]
  CONTRIBUTING.md:536 says of these two classes "Two escapes remain, both
  already in the base walk", and gen_toc_html.py:32-33 says "as the base did".
  On these pages the base did not list the heading. One further path: when
  the container layer marks a heading line raw (inside a type-3 to type-5
  block) while `blocks()` labels it prose, `hidden_lines` never reads the raw
  run before it ("a heading is one line of its own", gen_toc_html.py:124-127).
  A comment already open above then fails to hide it (fuzz page
  s437-004979, receipts/fuzz1.json).
  Scale (receipts/fuzz1.json, fuzz1.per_heading.txt): the full-vocabulary
  fuzz rendered 1,500 pages, stratified toward pages where the walks differ,
  so these are not population rates. 125 pages are ESCAPE at head and AGREE
  at base. Per heading there are 232 new escapes: 189 involve an inline PI or
  CDATA carrying `>` then `<!--`, 36 a type-3 to type-5 block, 6 an open
  quoted value and 1 an image description. Against those, 444 escapes and
  1,367 withholds are fixed. The core-only vocabulary shows 0 regressions in
  1,000 renders (receipts/fuzz_core.json). The REVIEW READY and the author
  sweep claim "0 regressions" (5791751430,
  correction-a190/receipts/final-sweep.log). That holds for the author's
  corpora only. Their vocabulary places `<? a > <!-- ?>` and
  `<![CDATA[ a > <!-- ]]>` at line starts, where they open raw blocks the
  model reads (correction-a190/scripts/gen_probes.py:99-100). No committed
  fixture page carries either one inline after text.
Impact: end to end, through the shipped gate with real Git base and head
  commits (receipts/emdash_e2e.txt), a label copied from `Old` is refused at
  the base (1 finding, 0 exempt) and exempt at the head (0, 1). This holds on
  E1, E2, E5 and E6, where GitHub renders no such heading. The generator also
  writes navigation to a section that does not render. This is the escape
  direction #413 and #437 exist to close. It is MAJOR and not BLOCKER because
  no tracked page reaches it (AC4: 0 classification differences) and the
  triggers are uncommon in prose.
Required outcome: no page that agreed at the base disagrees at the fix head
  in the escape direction. That covers E1, E1b, E2, E2b, E5, E5b, E6, E6b, E8,
  E9 and the 125 fuzz rows. The alternative is a public maintainer decision
  that accepts a named residue with its direction, its boundary and the fact
  that it regresses base-agreeing shapes. Either way, the docs and docstrings
  state only what holds. They must not call a residue "already in the base
  walk" where the base answered correctly. Arms fail when the property is
  removed.
Verification: rerun scripts/compare.py over receipts/pages/minimal.json,
  minimal2.json and fuzz_full_sample.json at the fix head. There must be zero
  head-ESCAPE/base-AGREE rows, and per_heading.py must report "new escape: 0".
  emdash_e2e.py must refuse E1, E2, E5 and E6 at the fix head. Controls C2 and
  C3 keep their answers.
```

```text
[R237] MINOR Conformance, RTL, Robustness, Tests - scripts/gen_toc_containers.py:108 and :221-223 (`_Box.filled`) - F2: a list item whose only content is a link reference definition outlives a second blank line in the walk, but not on GitHub (withholding regression)
Requirement/evidence: the same no-regression bar. The renderer removes a
  paragraph made only of reference definitions when it closes, so the item
  then holds no child. A blank line continues an item only while it holds
  one (CommonMark 0.31.2 section 5.2: an item begins with at most one blank
  line). `_Box.filled` stays True once any content was seen. Fresh render
  (receipts/minimal.json):
    E7  "- [r]: /u\n\n\n    <!--\n\n## Old\n"   GitHub `<ul><li></li></ul><pre><code>&lt;!--</code></pre><h2>Old</h2>`; base [Old]; head []
  The head reads the four-column line inside the item as a comment block. Its
  raw `<!--` then hides the rest. Controls E7b (one blank line) and E7c (an
  ordinary item and two blank lines) agree at the head. Fuzz page
  s437-018851 is the same mechanism.
Impact: withholding only. The generator drops a rendered section, and the
  gate refuses a legitimate copied label: 0 findings and 1 exempt at the base
  become 1 and 0 at the head (receipts/emdash_e2e.txt). A contributor sees it
  at once. It is MINOR because the trigger is narrow and fail-safe, but it
  breaks the stated bar.
Required outcome: E7 agrees at the fix head, or the residue is named with its
  direction and accepted publicly. An arm fails when the behaviour is
  removed.
Verification: scripts/compare.py over receipts/pages/minimal.json gives E7
  AGREE, and emdash_e2e.py exempts E7 at the fix head.
```

```text
[R237] MINOR Conformance, Robustness, Docs - CONTRIBUTING.md:533-536, scripts/gen_toc_html.py:24-34 and :71-76 (INLINE_HTML_RE) - F3: the documented escape inventory is incomplete; further escapes, shared with the base, are neither modelled nor named
Requirement/evidence: CONTRIBUTING.md:536 states "Two escapes remain". :533
  says a closer counts "in inline HTML within prose". gen_toc_html.py:24-27
  says Markdown text carries a closer only inside inline raw HTML and "can open
  nothing". Fresh renders show four more escapes. GitHub hides `Old` in each,
  and both walks list it (receipts/minimal.json, minimal2.json):
    E3  "<div>\n<!--\n\n![<b title=\"-->\">](u)\n\n## Old\n": an image description reaches the page as plain `alt` text, so its inline tag closes nothing, but the walk closes the comment.
    E4  "<div>\n<!--\n\n[r]: /u '<b title=\"-->\">'\n\n## Old\n": a reference definition's title is never emitted.
    E10 "Text <?p > <b title=\" ?> more.\n\n## Old\n": the PI's first `>` ends the bogus comment, and the tag's quoted value stays open.
    E12 "Text <!-- a --!> <b title=\"-->\"> more.\n\n## Old\n": HTML closes the comment at `--!>`, then the quoted value opens.
  These are not regressions: the base lists `Old` too, and E3 and E4 are
  exempt at both (receipts/emdash_e2e.txt). But the inventory this PR writes
  into the authoritative page is wrong.
Impact: a reader of 6.1 believes only two escape classes remain. Labels
  mirroring such headings keep an exemption no rule names.
Required outcome: 6.1 and the module docstring name these classes with their
  direction and boundary, or the walk handles them. If they remain, the
  inventory records an owning Issue (the manager's call).
Verification: each class is named. scripts/compare.py over minimal.json and
  minimal2.json shows the stated direction.
```

```text
[R237] MINOR Tests - scripts/gen_toc_containers.py:101-104 (a block quote ends at any line without `>`, a blank line included), scripts/gen_toc_container_cases.py - F4: the block-quote end at a blank line has no failing arm
Requirement/evidence: acceptance 3 requires that each new property carries an
  arm that fails when the property is removed. Mutation R28 lets a blank line
  continue a block quote. It passes `gen_toc.py --selftest` 1244/1244 and
  `check_em_dash.py --selftest` 416/416 (receipts/r28_selftests.txt). It is
  not equivalent. Over 60,000 fuzz pages, 13 heading listings change. All 13
  were rendered: the head agrees 13/13, and the mutant escapes on 11 and
  withholds on 2 (receipts/r28_survivor.txt). Minimal page Q1,
  "> ```\n\n> <!--\n\n## Old\n": GitHub [], head [], mutant [Old]
  (receipts/minimal2.txt).
Impact: a later edit can drop the rule with every gate green, and doing so
  reintroduces escapes.
Required outcome: an arm fails when the rule is removed.
Verification: scripts/mutate.py R28 is KILLED at an arm named for the
  property.
```

## Prior public findings at this head

| Finding | Severity, lenses | At e4906bfc | Evidence |
|---|---|---|---|
| R237-r1 F1: tag inside the resumed item paragraph | MAJOR; Conformance, Robustness, Tests | RESOLVED | 42/42 R237-r1 recorded pages agree (receipts/prior_findings.json); mutation R26 (gate ignored) killed at the family-one probe arms |
| R237-r1 F2: eleven historical cases | MAJOR; Conformance, Tests, Docs | RESOLVED against restated AC1 | 51 family-one shapes; `r86_5` maps the nine R86-5 descriptions one to one; 162/162 fixtures re-render byte-identical; the head agrees with all |
| R237-r1 F3: block-marker inertness unarmed | MAJOR; Conformance, Tests | RESOLVED | a mutation that lets fenced, commented or HTML-held lines open containers fails the three `R237 ...-marker-indented-closer` arms (receipts/mutation_block_marker.txt) |
| R238-r1 F1: content-column tag, C01-C08, P01, P04 | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED | 62/62 R238-r1 recorded probes agree |
| R238-r1 F2: dedented quote or footnote, D01-D07 | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED | D rows agree; R02 (footnote column) is killed at D02 and D04 |
| R238-r1 F3: item HTML outlives the item | SUGGESTION; Conformance, Robustness | RESOLVED | fixture shapes `R238 P02`, `P03` and `F09` agree |
| R237-2 F1: gate whatever holds the item; in-item block never ends | MAJOR; all five | RESOLVED | 252/252 regression rows and 654/654 rows of its corpus agree; its three em-dash escape shapes read 1 finding, 0 exempt at the head (receipts/emdash_e2e_r237_2.txt) |
| R237-2 F2: flag on any `<!--` substring | MAJOR; all five | RESOLVED | 10/10 regression probes agree. F1 and F3 above are different triggers, not this finding's shapes |
| R237-2 F3: empty-item guard unarmed | MINOR; Tests | RESOLVED | the guard is gone; the empty-item rule is structural and armed: R21 and R23 are killed at `empty item ends at blank` and related arms |
| R237-2 S1: opener four columns into an item | SUGGESTION; Conformance, Robustness | RESOLVED | fixture shapes `R237-2 S1 ...` agree |
| #516: twelve variants (six resumed regressions) | manager-tracked | RESOLVED at this head | the 12 `#516 ...` fixture shapes re-render byte-identical and agree. #516 stays open as Backlog; this is not its closure |

## Acceptance at this head

| Criterion | Result | Evidence |
|---|---|---|
| AC1: shape set committed, GitHub rendering recorded | met | `gen_toc_family_one.json` 51 shapes; 162/162 fixture receipts re-render byte-identical (receipts/fixture_rerender.txt) |
| AC1: bullet, ordered and two-digit items, at and past the column, inline and unknown tags, the five boundaries | met | fixture names and pages |
| AC1: nine R86-5 shapes mapped | met | `r86_5` on nine shapes, one to one |
| AC1: every shape agrees; every base-agreeing shape still agrees | met within the set | head 51/51. All 36 base-agreeing shapes agree; the 15 base-disagreeing shapes are fixed |
| The lane's no-regression bar (5788996063, 5789003484) | NOT met | F1 (escape), F2 (withhold) |
| AC2: five family-two forms named with direction | met | CONTRIBUTING.md:518-523, gen_toc.py:400-405, `I437 limitation ...` arms |
| AC3: each new property has a failing arm | NOT met | F4. F1 and F2 are also unarmed |
| AC4: tracked classification unchanged | met | 0 differing pages under base and head walks on the head (164 pages), 574c29fa (164), 88e9276b (163) and live dev ede8d48e (164) trees (receipts/ac4_summary.txt) |
| AC5: gates pass, no ratchet widened | met locally | 23 focused commands exit 0 (below); no `.budget` file in the diff; `MIN_ARMS` rises 707 to 1244 |

## Reviewer-owned completion ledger

Every lens was applied at this exact head. None is covered clean.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | restated AC1-AC5 and the no-regression decision; CommonMark 0.31.2 sections 4.6, 5.1, 5.2 and 6.6 and HTML tokenizer states; 162 fixture re-renders; 2,531 fresh synthetic renders; 785 prior recorded pages | none; applied by R237-3 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |
| RTL | UNCLEAN (F1, F2) | `git diff --stat 574c29fa..e4906bfc`: 11 files, CONTRIBUTING.md, docs/DOC_GENERATION.md and 9 under scripts/; no HDL, constraint, testbench, workflow, budget or gitlink path; four gitlinks at their pins. The walk's state machines are `blocks()` (gen_toc.py:407-428), the container layer (gen_toc_containers.py:146-251) and the HTML stage (gen_toc_html.py:80-139). Product RTL is unchanged. The lens is unclean only through the walk state-model defects F1 and F2, as in R237-2 | none; applied by R237-3 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |
| Robustness | UNCLEAN (F1, F2, F3) | inline PI, CDATA, declarations, open quoted values, reference-only items, image descriptions, tabs, nested and lazy containers, empty items; 60,000 fuzz pages walked and 2,500 rendered (receipts/fuzz1.json, fuzz_core.json) | none; applied by R237-3 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |
| Tests | UNCLEAN (F1, F2, F4) | gen_toc_container_cases.py and the three fixtures; selftests 1244/1244 and 416/416; 30 reviewer mutations plus one block-marker mutation (receipts/mutations.txt) | none; applied by R237-3 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |
| Docs | UNCLEAN (F1, F3) | CONTRIBUTING.md:518-541; docs/DOC_GENERATION.md:28-29, :59-60; docstrings gen_toc.py:383-405, gen_toc_containers.py:1-37, gen_toc_html.py:1-35; REVIEW READY 5791751430 and the author packet claims | none; applied by R237-3 | e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 |

## Also verified at this head

- Gates run in the review clone all exit 0 (receipts/gen_toc_*.txt,
  em_dash_*.txt, gates/SUMMARY.txt):
  - `gen_toc.py`: `--selftest` 1244/1244; `--check` 106 pages (17 below
    threshold); `--verify-anchors` 144; `--sites` 34 single-source sites.
  - `check_em_dash.py`: `--selftest` 416 arms; `--base 574c29fa` gives
    0 findings over 28 added lines, 0 exempt.
  - `docs_check`, `check_doc_style` and its selftest, `check_doc_paths`.
  - `check_py_idiom` and its selftest: long module 10 <= 10, long function
    9 <= 9, too many parameters 7 <= 7. No walk module appears in `--list`.
  - hygiene `--check` and its selftest; TODO ownership and its selftest;
    feature status and its self-test; test-evidence, naming and fail-fast
    `--check`; control-flow and cohesion selftests.
- `gen_toc_closer_cases.py` and `gen_toc_guards.py` are unchanged.
  `check_em_dash.py` changes only in its self-test integration.
  `gen_toc_cases.py` changes only in the guard expectations: nine families,
  three new spelled classes, and 25 to 34 sites.
- Mutations (receipts/mutations.txt): 28 of 30 are killed at arms named for
  their property. R19 (lazy-line gate) is equivalent: 0 heading and 0 label
  differences over 60,000 pages (receipts/survivor_equivalence.txt). R28 is
  F4.
- Hosted check runs at the exact head, listed only with no logs read
  (receipts/hosted-check-runs.tsv):
  - 22 runs. The seven required contexts concluded success: rtl-fast,
    docs-check, wire-accountability, docs-check-no-git, elaborate,
    verilator-suites and yosys-portability.
  - Verilator shards 0-4 and Yosys shards 0-3 executed and succeeded.
  - `Physical gPTP (nightly and manual)` is skipped. That is not hardware
    evidence.
  - Hosted and act acceptance remains with the manager.

## Limits

- Oracle: GitHub's Markdown API (`POST /markdown`, mode gfm). Headings are
  read from its sanitised HTML; anchor ids are not in that output and were not
  measured.
  - 2,531 synthetic pages were rendered between 11:20:53 and 12:02:05 UTC on
    2026-09-23, without a context parameter.
  - The 162 fixture requests were re-sent with their exact recorded bytes.
  - One batch hit a rate limit and completed after back-off. Every page in the
    tables was rendered: 1,500/1,500 and 1,000/1,000.
- The fuzz is bounded and stratified toward pages where the walks differ. Its
  counts are not population rates, and pages where both walks answer alike
  were only sampled (300 of the 1,500).
- The prior dispositions compare the head walk with the prior rounds' public
  recorded renderings; those pages were not re-rendered. The 162 fixture
  re-renders, which were re-rendered, came back byte-identical.
- No Verilator, Yosys, native, processor, gPTP or builder bank was run. The
  change carries no RTL, so the scoped Verilator binary was not used and its
  identity was not checked.
- The manager's source static, builder and native banks for this head are
  running separately. They are neither claimed nor inferred here.
- Physical calibration is NOT RUN, and field skips are not hardware proof.
- The final current-dev candidate (source base 574c29fa, live dev ede8d48e)
  was not built or gated. Only its tracked-page classification was compared
  (AC4 row).

## Pending manager duties

1. Return F1 to F4 to the author lane. Every lens must be applied again at
   the next head, because the fix scope is the walk and its case tables.
2. Decide publicly whether any residue from F1 or F2 is accepted as a named
   limitation instead of repaired, and whether F3's shared escapes and the
   two declared escapes need an owning Issue. The #516 and #495 dispositions
   remain open.
3. Collect the manager source banks at the final head; run trusted act
   replication; confirm the hosted contexts at the final head.
4. Build and validate the current-dev candidate at the merge turn.
5. Obtain two independent positives, one of them external, then explicit
   maintainer merge authorisation.
6. After merge: containment and review-integrity audits, issue closure and
   project Done.

## Reproduction

From the packet root, with `<clone>` a clone holding both revisions:

```sh
scripts/reproduce.sh <clone>
```

- `reproduce.sh` extracts the base and head `scripts/` trees. It then reruns
  the fixture re-render, the minimal and fuzz comparisons with their
  per-heading analysis, the em-dash end-to-end probe, the mutations and the
  AC4 comparison.
- Renders are cached under receipts/renders as exact request and response
  bytes, named by the request's SHA-256. With the cache present, no page is
  sent again.
- The fuzz page sets came from scripts/gen_pages.py: seed 437 with the full
  vocabulary and seed 4371 with `core`, 30,000 pages each. The rendered
  samples are in receipts/pages.
- scripts/prior_findings.py replays the prior rounds' public receipts, fetched
  from evidence commit `d2e01fec` under `review-evidence/437-r1/reviews/`.
- scripts/integrity.py checks the review clone.

## Boundaries observed

- GitHub access was read-only: GETs, and the render endpoint with synthetic
  pages. One dry-run fetch wrote no ref and no FETCH_HEAD. No comment, review,
  label, metadata change, push or merge.
- The review clone received no source edit or commit. The round's gate run
  had created an ignored `scripts/__pycache__/`, which was removed.
  Mutations, extracted trees and probe copies ran only under the packet's
  scratch directory.
- Final integrity (receipts/integrity-final.json):
  - HEAD is the exact head.
  - 867 tree entries (821 regular, 42 executable, 4 gitlinks) match their
    blob bytes, modes and stage-0 index records, with only `H` flags.
  - `git status --porcelain --ignored` is empty.
  - `gptp-processor`, `protocol-processor` and `third_party/verilog-axis`
    are clean at their gitlinks, and `external` is uninitialised, as
    expected.
- No Docker, act, `act_ci` or its selftest, installs, privilege, hardware,
  sub-agents or author contact. At most eight jobs ran at once.

R237-3 FINISHED

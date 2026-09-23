[R237] NEGATIVE - exact head 4741498f3b2b4f67f431037d327c96cf65691278

Round R237-2, internal cleared-context review of issue #437 / PR #515.
Head `4741498f3b2b4f67f431037d327c96cf65691278`, tree
`ee70aaf8faadbced21dfdd0cf7719597e9fbe8eb`. Source base
`483a133ed08867ea0d300d2b4a027b5b48a4282f`. Its `scripts/gen_toc.py` is
byte-identical to the lane's original base `88e9276b`
(SHA-256 `ffdd8207...6eb3`), so "the base walk" below means both. All five
lenses were applied: Conformance, RTL, Robustness, Tests, Docs. Two MAJOR
findings and one MINOR finding are open, so every lens is UNCLEAN at this
head. This is not merge approval.

Reconstructed from, in this order: AGENTS.md, CONTRIBUTING.md (2, 3, 5,
6.1), docs/README.md, issue #437 (body, restated acceptance 1, the
maintainer decision 5788996063, the assignments 5775771538, 5778277123 and
5789003484, the tracking note 5778773475), the author's material decision
5789133990 and REVIEW READY 5789254166, PR #428 R86-5 (comment 5644834363),
CommonMark 0.31.2 sections 4.6, 5.2 and 6.6, then the diff
`483a133e..4741498f` and its history, then executable evidence. The verdict,
findings and ledger were written before this reviewer read any prior review
report on PR #515. The prior round-1 findings and issue #516 were then read
to give their dispositions below. No concurrent round-2 report was read.

## Summary

The committed family-one shape set meets restated acceptance 1 on its own
terms. There are 51 family-one shapes and 40 comment controls. All 91
recorded renderings re-render byte-identical at this review. The head walk
agrees with every one. Each of the nine publicly described R86-5 shapes maps
one to one to a named shape. No shape in the set regresses from the base.
AC2, AC4 and AC5 are met.

The restated criterion also requires that every shape that agreed at the
base still agrees. The maintainer decision and the assignment state it as
"no regression against the base". This head breaks that in two independent
families, both measured against fresh GitHub renderings:

- F1: the new list-paragraph state regresses 270 generated pages that agreed
  at the base. In 90 of them the head lists a heading GitHub renders as code
  inside a fence, and `check_em_dash.py` at this head exempts a label copied
  from it. The base refuses that label.
- F2: the new rendered-comment flag hides the rest of the page after
  raw-HTML bytes that open no comment for GitHub. The triggers are `<!--`
  inside a quoted attribute value, `--!>`, a CDATA section, and a Markdown
  `<!--` on a line the flat walk labels raw HTML. Every probe in this family
  agreed at the base.

F3 is a Tests gap: one new guard has no arm.

## Findings

```text
[R237] MAJOR Conformance, RTL, Robustness, Tests, Docs - scripts/gen_toc.py:399-402, :477-478 (the content-column continuation and the outer-column retention in _list_paragraph_after) - F1: a tag at the item's content column is read as continuing a live paragraph whatever holds the item, and a block it then opens never ends with the item; shapes that agreed at the base now disagree, including escapes that obtain the em-dash exemption
Requirement/evidence: restated acceptance 1 and the maintainer decision
  (#437 comments 5788996063, 5789003484): every shape that agreed at the base
  still agrees, with no regression against the base. CommonMark 0.31 sections
  4.6 and 5.2 as GitHub applies them: a type-7 start line is refused only when
  the deepest container the line matches is an open paragraph.
  The head sets `opening_para = PARAGRAPH` for any line at or past the outer
  item's content column while `para == HELD` (gen_toc.py:399-402). HELD also
  comes from a nested block quote, a nested list item, a footnote definition,
  a table, a setext underline, or an item whose content starts with a quote.
  `_list_paragraph_after` keeps the OUTER column for nested content
  (:477-478, docstring :469). GitHub opens a raw HTML block in each of those
  holds. Its recorded HTML carries `<span> ``` </span>` as raw text inside the
  item. The head reads the tag as paragraph text and then opens a fence or
  type-1 block on the next in-item line. There is a second case where the
  item's paragraph really is live (`- item`, `1. item`, a task item, `-`
  gaining text). There the head's tag class is right. But the fence or
  `<pre>` it then opens inside the item never ends with the item, because
  the walk is flat and nothing closes it. At the base the tag wrongly opened
  HTML and swallowed that line, which cancelled the flat-block error.
  Measured: scripts/gen_corpus.py generates 2070 pages. The base and head
  walks differ on 654. All 654 were rendered with GitHub's Markdown API
  (mode gfm) and recorded in receipts/combinatorial-render.json. Results:
  360 fixes and 252 regressions, plus 18 more regressions once documented
  family-two headings are set aside. That is 270 in total: 207 from the
  non-paragraph hold and 63 from the live paragraph's in-item block. The tag
  sits at column 2 or 3 in every one. In 90 of them the head lists `Old`,
  which GitHub renders inside a fenced code block
  (receipts/combinatorial-summary.txt). Minimal pages, with base, head and
  GitHub results. The first two are in receipts/regression-seed-render.json.
  The third is combinatorial row
  `bullet | tag col 2 <span> | fence then real fence`:
    "- item\n  > quote\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n\n## Real\n"
      GitHub [Real]; base [Real]; head [Old]
    "- item\n  - nested\n  <span>\n  ```\n\n## Old\n\n## Real\n"
      GitHub [Old, Real]; base [Old, Real]; head []
    "- item\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n\n## Real\n"
      GitHub [Real]; base [Real]; head [Old]
  End to end: scripts/emdash_probe.py replays the head's own em-dash arm
  construction with real Git base and head commits
  (receipts/emdash-escape-probe.txt). At 483a133e each of the three escape
  shapes gives `findings=1 exempt=0`. At this head each gives
  `findings=0 exempt=1`. The plain-fence and plain-heading controls agree at
  both revisions.
  No arm covers a nested container or an in-item block after the tag. The
  public REVIEW READY claim of "0 regressions" (#437 comment 5789254166)
  holds only for the author's replay corpus. The docstring (gen_toc.py:368)
  and CONTRIBUTING.md:525 say a tag at the content column "continues the
  item's live paragraph". The walk cannot tell whether that paragraph is
  live. Neither place states that a fence or type-1 block opened in an item
  outlives the item.
Impact: a Contents label copied from a heading that GitHub renders as code
  gets the CONTRIBUTING.md 6.1 exemption and points at an anchor the page does
  not have. This is the escape direction #437 exists to close, reintroduced
  in shapes where the base refused it. In the withholding shapes, the
  generator drops sections the page renders. No tracked page is affected
  today: all 163 pages classify identically under both walks at 88e9276b,
  483a133e and this head (receipts/ac4-corpus.txt).
Required outcome: no page that agreed at the base disagrees at the fix head.
  Either the continuation applies only while the line reaches an open
  paragraph at that container depth, or the change is bounded so that no
  base-agreeing shape regresses. Any residue that remains is named in the
  docstring and in CONTRIBUTING.md 6.1 with its direction and boundary,
  including in-item fences and type-1 blocks. Arms fail when either root
  cause returns.
Verification: rerun scripts/probe.py render over scripts/gen_corpus.py output
  (at least over the REGRESSION rows of receipts/combinatorial-render.json)
  against the fix head: zero REGRESSION rows. scripts/emdash_probe.py must
  read `exempt=0` for the three escape shapes at the fix head.
```

```text
[R237] MAJOR Conformance, RTL, Robustness, Tests, Docs - scripts/gen_toc.py:406-409 (rendered_comment), CONTRIBUTING.md:531-535 - F2: the rendered-comment flag treats every `<!--` substring on a flat-walk raw-HTML line as an HTML comment opener; pages that agreed at the base now lose every heading after it
Requirement/evidence: the same no-regression bar as F1. GitHub's rendering
  is the reference, and it tokenises raw HTML as HTML does. A `<!--` inside a
  quoted attribute value, or inside a CDATA section, opens no comment, and
  `--!>` closes one. The flag is set by `_comment_after` over the whole text
  of every line the walk labels raw HTML or commented, and over prose carrying
  `<!--` (gen_toc.py:407-408). Once set, it relabels all later prose as
  commented until a raw line carries `-->`. The walk's raw-HTML labels are
  flat (#495): a Markdown line the renderer reads outside an item can still
  be labelled raw HTML. Fresh renders in receipts/comment-rule-render.json
  show 10 of 17 probes REGRESSION. In each GitHub shows `Old` and `Real`,
  the base lists both, and the head lists neither:
    '<div title="<!--">\n\n## Old\n\n## Real\n'
    '<span title="<!--">\n\n## Old\n\n## Real\n'
    '<div>\n<img alt="<!-- x">\n</div>\n\n## Old\n\n## Real\n'
    '<div>\n<![CDATA[<!--]]>\n</div>\n\n## Old\n\n## Real\n'
    '<div>\n<!-- a --!>\n</div>\n\n## Old\n\n## Real\n'
    '<div>\n<!--\n--!>\n</div>\n\n## Old\n\n## Real\n'
    '<div>\n<!--\n</div>\n\ntext <a title="-->"> more\n\n## Old\n\n## Real\n'
    '- item\n\n  <div>\ntext `<!--` more\n\n## Old\n\n## Real\n'
    '- item\n\n  <div>\ntext \\<!-- more\n\n## Old\n\n## Real\n'
    '- item\n\n  <div>\ntext <a title="<!--"> more\n\n## Old\n\n## Real\n'
  The same file carries the controls: textarea, style, `-- >` and a code-span
  arrow after a raw comment are fixes, and a flat item block without `<!--`
  agrees at both revisions. The author's material decision (#437 comment
  5789133990) says the renderer "passes raw HTML block content through" and
  that "A `<!--` left open there hides the rest of the page". That holds only
  where the HTML tokeniser is in its data state. "The rule only removes
  headings" is true, but removing headings the base listed correctly is a
  regression under the bar. CONTRIBUTING.md:534 documents `--!>` and the
  inline-tag closer as withholding. It does not say that those shapes agreed
  at the base. The attribute-value, CDATA and flat-item-HTML triggers are
  documented nowhere. No arm covers any of them. The `<!-->`/`<!--->` change
  to `_comment_after` (gen_toc.py:518) matches CommonMark 0.31.2 section 6.6
  and GitHub (fixture rows "abrupt ..."), and is not part of this finding.
Impact: a page that renders every section gets a Contents block with every
  section after the trigger missing. A copied label is refused where the
  base exempted it correctly. This is the withholding direction, with no
  exemption leak. No tracked page is affected (receipts/ac4-corpus.txt).
Required outcome: no base-agreeing page loses a heading. A `<!--` opens the
  rendered comment only where GitHub would open one. Any residue that
  remains is stated with its direction, and with the fact that it regresses
  base-agreeing shapes if so, and is accepted by a public decision rather
  than by the author's decision alone. Arms cover the attribute-value, CDATA,
  `--!>` and flat-item-HTML triggers.
Verification: rerun scripts/probe.py render over the pages in
  receipts/comment-rule-render.json at the fix head: zero REGRESSION rows,
  and the four fixes stay fixes.
```

```text
[R237] MINOR Tests - scripts/gen_toc.py:400 (`not item_context[1]`), scripts/gen_toc_container_cases.py:97-228 - F3: the empty-item guard on the content-column continuation has no arm; removing it survives both selftests while changing observable output, including an escape
Requirement/evidence: acceptance 3 requires that each new property carries an
  arm that fails when the property is removed. gen_toc.py:222-223 states the
  property: "A live nonempty list's content column supplies PARAGRAPH".
  scripts/mutate.py runs 18 exact mutations of the new code in a disposable
  clone (receipts/mutation-probe.txt, -2.txt, -3.txt). 17 are killed by
  `gen_toc.py --selftest` and `check_em_dash.py --selftest`, each at arms
  named for its own property. M10 survives both: the condition
  `if para == HELD and item_context and not item_context[1]` becomes
  `if para == HELD and item_context`. It is not an equivalent mutant.
  receipts/fixture-rerender-compare.txt records, against fresh GitHub
  renderings:
    "-\n  <span>\n  ```\n\n## Old\n\n## Real\n"  GitHub [Old, Real]; head
      [Old, Real]; mutant []
    "-\n  <span>\n  ```\n\ntext\n\n```\n## Old\n```\n\n## Real\n"  GitHub
      [Real]; head [Real]; mutant [Old] (escape)
Impact: a later edit can drop the guard with every gate green, and doing so
  reintroduces an escape.
Required outcome: an arm fails when the empty-item guard is removed.
Verification: rerun `scripts/mutate.py <tree> M10`: KILLED.
```

```text
[R237] SUGGESTION Conformance, Robustness - pre-existing, identical at base and head - S1: a comment opener at four or more columns inside a list item, after a blank line, is read as indented code, so the walk lists headings GitHub hides
Evidence: '- item\n\n    <!--\n\n## Old\n\n## Real\n' and
  '- item\n\n    <div><!--\n\n## Old\n\n## Real\n' both render with no
  headings, and both walks list both (receipts/comment-rule-render.json,
  both-disagree-same). scripts/emdash_probe.py gives `exempt=1` at both
  483a133e and this head. The base docstring gave the four-column container
  reading the withholding direction only, and the head docstring keeps "a tag
  at four columns inside an item" as withholding with no owning Issue.
Suggested: open one follow-up Issue that owns the four-column container
  reading in both directions. R238-r1 F3 asked for the same owner for the
  retained withholding residues. It is outside restated acceptance 1 and is
  not a regression, so it does not affect lens coverage here.
```

## Prior public findings on PR #515 at this head

| Finding | Severity, lenses | Disposition at 4741498f | Evidence |
|---|---|---|---|
| R237-r1 F1: tag inside the resumed item paragraph hides a heading | MAJOR; Conformance, Robustness, Tests | RESOLVED | rows `resumed tag column 2/3 open/close/attribute` agree with fresh renders (receipts/test-rows-render.json); M1 and M11 are killed at the R238 C-row arms |
| R237-r1 F2: eleven historical cases not accounted for | MAJOR; Conformance, Tests, Docs | RESOLVED against restated AC1 | maintainer decision 5788996063; nine R86-5 descriptions (PR #428 comment 5644834363 lines 56-59) map one to one to `r86_5` shapes; all 91 fixture receipts re-render byte-identical and the head agrees with each |
| R237-r1 F3: block-marker inertness not protected | MAJOR; Conformance, Tests | RESOLVED | that round's own mutation (`label != TEXT or after == HELD`, M18 here) is KILLED at the three `R237 ...-marker-indented-closer` arms (receipts/mutation-probe-3.txt); those rows agree with GitHub |
| R238-r1 F1: content-column tag under a resumed paragraph | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED for C01-C08, P01 and P04 | all agree with fresh renders; M1 and M11 are killed at the C-row arms. The mechanism's repair over-applies, which is the new F1 above, with different shapes and a different root cause |
| R238-r1 F2: item context survives a dedented quote or footnote | MAJOR; Conformance, Robustness, Tests, Docs | RESOLVED | D01-D07 agree; M5 is killed at D01-D04; the `quote/footnote column 0-2` rows agree |
| R238-r1 F3: HTML block in an item outlives the item (pre-existing) | SUGGESTION; Conformance, Robustness | RETAINED as SUGGESTION, partly addressed | the docstring (gen_toc.py:375-377) and CONTRIBUTING.md:528-530 now name it with direction under #495; the retained four-column withholding residues still have no owning Issue (see S1) |
| #516 six resumed unclosed-comment regressions | tracked by the manager | RESOLVED at this head | all twelve #516 variants agree (fixture rows, receipts/fixture-rerender.json) |

## Acceptance at this head

| Criterion | Result | Evidence |
|---|---|---|
| AC1 restated: shape set committed, renderings recorded | met | `scripts/gen_toc_family_one.json` 51 shapes, `gen_toc_comment_shapes.json` 40; 91/91 byte-identical fresh re-renders (receipts/fixture-rerender-compare.txt) |
| AC1: bullet, ordered and two-digit items, at and past the column, inline and unknown tag, five agreeing boundaries | met | fixture names. The two-digit shapes at or past column 4 are decided by the four-column code reading at base and head alike. The wider column is held by the below-column shapes |
| AC1: nine R86-5 descriptions mapped | met | `r86_5` field on nine shapes, one to one |
| AC1: every shape agrees with its rendering | met | the head agrees 91/91 |
| AC1: every shape that agreed at the base still agrees | NOT met | F1 (270 generated pages), F2 (10 probes) |
| AC2: five family-two forms named with direction | met | gen_toc.py:385-390, CONTRIBUTING.md:518-523; GitHub renders all five and both walks omit all five (receipts/family-two-render.json) |
| AC3: each new property has a failing arm | NOT met | F3 (M10 survives); 17 of 18 mutations killed |
| AC4: tracked classification unchanged | met | 0 of 163 pages differ at 88e9276b, 483a133e and 4741498f (receipts/ac4-corpus.txt) |
| AC5: gates pass, no ratchet widened | met | receipts/gates/summary.txt, all 23 exit 0; no budget file in `git diff 483a133e..4741498f` |

## Reviewer-owned completion ledger

Every lens was applied at this exact head. None is covered clean.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2 open) | restated AC1-AC5; PR #428 R86-5 text; both fixtures against 91 fresh gfm renders; 654 + 17 + 10 + 5 + 197 + 4 further fresh gfm renders; CommonMark 0.31.2 sections 4.6, 5.2 and 6.6 | none; applied by R237-2 | 4741498f3b2b4f67f431037d327c96cf65691278 |
| RTL | UNCLEAN (F1, F2 open) | the `blocks()` state machine gen_toc.py:392-410, `_list_paragraph_after` :464-492, `_comment_after` :495-519, the `_opens` gating :552-583; the path sets of merge a09ff881; four gitlinks and `.gitmodules` identical to 483a133e; no HDL, workflow, constraint or budget path in the diff | none; applied by R237-2 | 4741498f3b2b4f67f431037d327c96cf65691278 |
| Robustness | UNCLEAN (F1, F2 open) | nested quote, list, footnote, table and setext holds; empty and lazy items; tag columns 0-5; in-item fence, pre and comment followers; attribute, CDATA, `--!>` and flat-HTML comment triggers | none; applied by R237-2 | 4741498f3b2b4f67f431037d327c96cf65691278 |
| Tests | UNCLEAN (F1, F2, F3 open) | every arm in `gen_toc_container_cases.py`; 197 hand-written expectations re-rendered with 0 mismatches; 18 mutations; selftests 1091/1091 and 345/345 | none; applied by R237-2 | 4741498f3b2b4f67f431037d327c96cf65691278 |
| Docs | UNCLEAN (F1, F2 open) | gen_toc.py docstring :365-390 and :217-224; CONTRIBUTING.md:518-536; #437 decision and REVIEW READY comments | none; applied by R237-2 | 4741498f3b2b4f67f431037d327c96cf65691278 |

On the RTL lens: product RTL is untouched at this head, so its scope here is
the walk's state machine and the module contract the em-dash gate relies on.
F1 and F2 are state-model defects, so they are recorded under RTL as well.

## Also verified at this head

- Gates, run from the review clone (receipts/gates/, summary.txt), all exit
  0:
  - `gen_toc.py --selftest` 1091/1091, `--check` 105 pages,
    `--verify-anchors` 144, `--sites`.
  - `check_em_dash.py --selftest` 345. `--base 483a133e` gives 0 findings
    over 20 added lines, and `--base 88e9276b` gives 0 over 32.
  - `docs_check.py` and its selftest; `check_doc_style.py` and its selftest.
  - `check_py_idiom.py` and its selftest: long module 10 <= 10, long
    function 9 <= 9, too many parameters 7 <= 7.
  - hygiene `--check` and its selftest.
  - naming, fail-fast and test-evidence `--check`.
  - control-flow and cohesion selftests; TODO ownership; doc paths; feature
    status.
- Integration: merge `a09ff881` brings only dev's three builder paths. The
  five issue paths relative to `483a133e` are the lane's changes. Both
  commits have one-line subjects with no trailers.
- Hosted check runs at the exact head (receipts/hosted-check-runs.tsv, list
  only; logs not read):
  - The latest run of each of the seven required contexts concluded
    `success`: rtl-fast, docs-check, wire-accountability, docs-check-no-git,
    elaborate, verilator-suites and yosys-portability.
  - Earlier `failure` and `cancelled` entries belong to a superseded first
    run.
  - `Physical gPTP` is `skipped`, which is not hardware evidence.
  - Hosted and act acceptance remains with the manager.

## Limits

- The oracle is GitHub's Markdown API, POST /markdown in mode gfm, context
  kebag-logic/milan-fpga. It was queried 978 times on 2026-09-23 between
  06:28:25 and 06:39:50 UTC. It returns sanitised HTML, and headings are
  read from that HTML. Anchors (id attributes) are not in the API output and
  were not measured.
- The combinatorial corpus is bounded: 23 prefixes, 6 tag columns, 3 tags
  and 5 followers. Only pages where the two walks differ were rendered, so
  residues identical at base and head outside the probes above are not
  characterised.
- The tree carries no Verilog change. No Verilator, Yosys, native, processor,
  gPTP or builder bank was run. The scoped Verilator binary was not used,
  so its identity was not checked. The manager's source validation (PR
  comment 5789833078, evidence e8b18a06) was not re-executed. Physical
  calibration is NOT RUN and field skips are not hardware proof.
- The final current-dev candidate (live dev 574c29fa) was not built or
  gated. This review covers the source head at base 483a133e only.

## Pending manager duties

1. Return F1, F2 and F3 to the author lane. All five lenses must be applied
   again at the next head, because the fix scope is the walk and its case
   tables.
2. Decide publicly whether the author's rendered-comment rule is accepted
   as a contract, and dispose of #516 accordingly.
3. Decide the follow-up Issue for S1 and the retained four-column residues
   (R238-r1 F3).
4. Run trusted act replication and required hosted contexts at the final
   head.
5. Build and validate the candidate against live dev at the merge turn.
6. Obtain the external review and two independent positives, then explicit
   maintainer merge authorisation.
7. After merge: containment and review-integrity audits, then issue closure
   and project Done.

## Reproduction

Commands run from the packet root. `<clone>` is a clean checkout at the head.
`<tree>` is a disposable clone at the head.

```sh
B=483a133ed08867ea0d300d2b4a027b5b48a4282f H=4741498f3b2b4f67f431037d327c96cf65691278
python3 scripts/gen_corpus.py > corpus.json
python3 scripts/probe.py walk   --repo <clone> --base $B --head $H corpus.json
python3 scripts/probe.py render --repo <clone> --base $B --head $H corpus.json out.json
python3 scripts/emdash_probe.py --repo <clone> --rev $B
python3 scripts/emdash_probe.py --repo <clone> --rev $H
python3 scripts/corpus_ac4.py --repo <clone> --base $B --head $H 88e9276b2a220c716f64a843f7e1eb8f9265e896 $B $H
python3 scripts/mutate.py <tree>            # M1-M18; M10 survives
python3 scripts/integrity.py <clone> $H
```

`probe.py render` accepts any `{name, page}` list. Every render receipt
carries the exact page, request bytes, response bytes, both SHA-256 values,
the rendered headings, both walks' headings and the class.

## Boundaries observed

- GitHub access was read-only: GETs, and the render endpoint with synthetic
  pages only. No comment, review, label, metadata, push or merge.
- The review clone was not edited. Mutations ran in a disposable clone under
  scratch/, and each restore was hash-checked.
- Final integrity (receipts/integrity-final.txt): HEAD is the exact head.
  854 tracked files match their blobs and modes, 858 index records equal
  the tree with no stage or flag, and the status is clean. The three required
  submodules are clean at their gitlinks. `external` is uninitialised, as
  expected.
- No Docker, act, `act_ci` or its selftest, installs, privilege, hardware,
  sub-agents or author contact. Fewer than eight jobs ran at once.

R237-2 FINISHED

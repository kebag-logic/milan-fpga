[R238] NEGATIVE - exact head 65df1df50a80cd5f540a93d8f0cfabc97da3da75

# [R238] round 1: issue #437 / PR #515, external cleared-context review

## Head under review

- Commit `65df1df50a80cd5f540a93d8f0cfabc97da3da75`, tree
  `da06c8609b7a574e3df121fbcb8a1fc8f207dcb7`. It is one commit whose only
  parent is `88e9276b2a220c716f64a843f7e1eb8f9265e896`, with a one-line
  message and no trailers.
- Live refs at 2026-09-22T14:08:57Z: `dev` = `88e9276b…`,
  `437-container-paragraph-scopes` = `65df1df5…`
  (receipts/remote-refs.txt). The head tree is therefore the current
  candidate merge tree.
- The diff touches five files: `CONTRIBUTING.md`, `scripts/check_em_dash.py`,
  `scripts/gen_toc.py`, `scripts/gen_toc_cases.py` and the new
  `scripts/gen_toc_container_cases.py` (+194/-31). The `hdl`, `sw`, `syn`,
  `tb`, `.github`, `docs` and `third_party` trees, `.gitmodules` and all four
  gitlinks are the same objects at base and head (receipts/rtl-lens.txt).
- Review checkout (`$REVIEW_CHECKOUT`) integrity was identical at the start
  and the end of this round: 856 entries (810 regular, 42 executable,
  4 gitlinks). Every blob, mode and kind matched its index record (stage 0,
  `ls-files -v` flag `H`). The three required submodules were at their pins
  with clean worktrees and `external` was uninitialised. No path was
  untracked or ignored. See receipts/integrity-start.json,
  receipts/integrity-reproduce-post.json and receipts/integrity-final.json.

## What was read

- **Repository rules:** AGENTS.md, CONTRIBUTING.md (sections 2, 3, 5 and
  6.1), docs/README.md, REQUIREMENTS.md as the normative entry point, and
  docs/development/CODE_QUALITY.md rule 12.
- **Issue #437:** the body, the [A10] implementation decision
  (issuecomment-5775771538), and the public [A168]/[A10] receipts on it.
- **PR #515:** metadata through explicit `--json` fields only, with no status
  rollup, plus its two [A10] comments.
- **Originating measurements:** R85-4 and R86-5 on PR #428
  (issuecomment-5644713074 and 5644834363).
- **Specification:** CommonMark 0.31.2 sections 4.6, 5.1 and 5.2.
- **The change and its evidence:** the diff `88e9276b..65df1df5`, and the
  manager packet at evidence commit `e6013980`
  (review-evidence/437-r1/manager: full-native results, builder results,
  final tree integrity, one suite log, builder log 43).
- **Not read:** the author packet's narrative files (HANDOFF, NEW-FINDINGS,
  PR-BODY, R21, R22), any R237 material, and any local lane directory.

**Oracle.** GitHub's renderer (`gh api markdown --input -`, `POST /markdown`,
gfm mode) was sent synthetic pages only. It received 243 requests between
13:52 and 14:08 UTC on 2026-09-22, and every one exited 0. Each exact request
and response is in receipts/renderer-cache.json and, per probe, in
receipts/probes.jsonl. Verdicts below compare each walk's `headings()` with
the renderer's headings among the probe words `Old`/`Real`:

- **INVENT:** the walk lists a heading GitHub does not render (the escape
  direction).
- **WITHHOLD:** GitHub renders a heading the walk omits.

## Findings

```text
[R238] MAJOR Conformance, Robustness, Tests, Docs - scripts/gen_toc.py:458-459 (reached from :389, consumed by the type-7 gate at :549-550, state defined at :217-223), scripts/gen_toc_container_cases.py:19-77, CONTRIBUTING.md:524-525, receipts/probes-table.txt rows C01-C08, receipts/e2e-table.txt - F1: a lone tag at or past a live item's content column under a resumed item paragraph now opens a type-7 block GitHub does not open, so a following column-0 fence, comment or type-1 opener is swallowed and a heading GitHub renders as code is listed and its copied label exempt (regression: the base walk agreed on all eight shapes)
Requirement/evidence: CONTRIBUTING.md 6.1 exempts a copied label only when
  the base page already had that heading. #437's objective is to tell a
  container's own paragraph from a top-level one by the content column.
  Inside a list item, a line at the content column belongs to the item, and
  there the item's own paragraph is open. A lone tag at that column is
  therefore paragraph continuation (CommonMark 0.31.2 sections 5.2 and 4.6).
  GitHub agrees. C01 to C03 (`- item`, blank, `  text`, then the tag at
  column 2 or 3; and `1. item` with the tag at column 3) render `Old`. C04 to
  C08 (C01 followed by a column-0 fence, comment or `<pre>`, a blank line and
  `## Old`; also after a lazy line and for a column-3 item) render no `Old`.
  The head holds the resumed paragraph as HELD (:458-459). The state table
  defines HELD as "none is open" (:219-222). `_opens` opens type 7 on any
  tag line while HELD (:549-550). So at this head C01 to C03 WITHHOLD `Old`,
  and C04 to C08 INVENT it; C04, C07 and C08 also lose `Real` to the stray
  fence. At the base all eight AGREE. The first-paragraph form of the same
  mechanism is identical at base and head (P01 INVENT, P04 WITHHOLD). The
  class therefore existed for an item's first paragraph, and this change
  extends it to every resumed paragraph.
Impact: Through the shipped gate with real Git (receipts/e2e-table.txt),
  the head exempts the copied label `Old <U+2014> heading` on C04 to C08,
  where the base page renders that heading only as code, a comment or raw
  HTML. The base gate refuses all five. In the navigation consumer, the
  generator writes `- **[Old](#old)**` into Contents for a heading GitHub
  does not render (receipts/navigation-consumer.txt, C04). In the safe
  direction, C01 to C03 withhold a rendered heading. End to end, C01 refuses
  a legitimate label, and the generator drops C01's rendered section
  (receipts/navigation-consumer.txt, C01). The tracked corpus is not reached
  today: there are 0 type-7 tag
  lines in 163 pages, and classification is unchanged. The precondition,
  a resumed item paragraph the head now holds, is already on 46 lines of 9
  tracked pages (receipts/census.txt). No arm can see this: every I437 probe
  puts its tag at column 0 (gen_toc_container_cases.py:76), so all 754 TOC
  and 99 gate arms pass on this head. They also pass on a walk that answers
  C01 to C08 correctly (receipts/candidate-repair.txt). CONTRIBUTING.md:525
  ("This corrects the escaping HTML classification") and the docstring at
  gen_toc.py:364-371 describe no remaining escape. This is MAJOR, not
  MINOR, because the change itself introduces these escapes, in the
  direction #413 and #437 exist to close, on shapes the base answered
  correctly. It is not BLOCKER because no tracked page reaches it.
Required change: A lone type-7 tag line at or past a live item's content
  column, while that item's paragraph is open, is answered as GitHub answers
  it. C01 to C08 then AGREE, and no shape the base walk answered correctly
  regresses. P01 and P04, the first-paragraph form, close with it if the
  repair is made at the mechanism; otherwise they belong with F3. An arm
  holds the tag line's column boundary in both directions (a tag at the
  content column and one column below it, under a first and a resumed item
  paragraph, with a following column-0 fence), and fails when reverted to
  this head's rule. The docstring (:364-371), the state table (:217-223) and
  CONTRIBUTING.md:524-525 state only what holds. Any container escape still
  in the tree is named with its direction and boundary, not implied closed.
  The frozen #437 contract allows the declared-limitation route for family
  two only, so declaring this escape instead of repairing it needs a
  published manager decision.
Verification: Rerun scripts/probe_render.py: C01 to C08 AGREE, and A01 to
  A20, B01 to B06, D05 to D07 and F01 to F12 stay AGREE. Rerun
  scripts/e2e_gate.py: at head, C01 reads `exempt ok` and C04 to C08 read
  `refused ok`. A mutant restoring this head's rule fails a named arm.
  scripts/corpus_compare.py still reports 0 differing pages, and no budget
  file moves.
```

```text
[R238] MAJOR Conformance, Robustness, Tests, Docs - scripts/gen_toc.py:469-470 and its docstring :451-452, scripts/gen_toc_container_cases.py:19-64, receipts/probes-table.txt rows D01-D04, receipts/e2e-table.txt, receipts/mutants-table.txt row N01 - F2: an item context survives a column-0 block quote or footnote definition that ends the list for GitHub, so after a blank line a top-level paragraph is held as the item's and a column-0 tag opens a block GitHub does not open (regression; contradicts the helper's own docstring)
Requirement/evidence: A block quote marker or a footnote definition is not
  paragraph continuation text. At column 0 under an item it is therefore no
  lazy line, and the item ends (CommonMark 0.31.2 section 5.2 laziness,
  section 5.1; GFM footnote definitions as the renderer reads them). GitHub
  agrees. In D01 (`- item`, `> quote`, blank, `  text`, then the column-0
  tag) and D02 (`[^1]: note` in place of the quote), `  text` is a top-level
  paragraph, the tag continues it, and `Old` renders. With a column-0 fence
  after the tag (D03, D04), `Old` is code. `_paragraph_after` answers HELD
  for a quote or footnote line, and :469-470 keeps the context for every
  HELD-to-HELD line, so the context outlives the list. The head WITHHOLDS
  `Old` in D01 and D02 and INVENTS it in D03 and D04. The base walk keeps no
  context and agrees on all four. The helper's docstring says "a fresh
  dedented paragraph or block releases the item" (:451-452), which is false
  for these two blocks. The head is right on a quote after a blank line
  (D05) and a quote inside the item (D06). It is also right on D07, a
  dedented quote followed by four-column text that both walks read as code,
  where the stale context has no effect.
Impact: End to end, the head gate exempts the copied label on D03 and D04,
  which the base gate refuses. It refuses the legitimate label on D01 and D02
  (receipts/e2e-table.txt). The generator lists `Old` for D03
  (receipts/navigation-consumer.txt). The tracked corpus is not reached: no
  context is kept by a dedented quote or footnote line
  (receipts/census.txt). No arm holds the release. Mutant N01, which releases
  the item on such a line, passes 754/754 and 99/99
  (receipts/mutants-table.txt), so the arms accept either behaviour. MAJOR
  for F1's reason: this change introduces an escape on shapes the base
  answered correctly.
Required change: A dedented line that ends the list for GitHub releases the
  item context. D01 to D04 then AGREE, while D05 to D07 and the shipped
  lazy-line, heading, sibling and fresh-paragraph controls keep their
  answers. An arm fails when that release is removed. The docstring states
  what the helper does.
Verification: Rerun scripts/probe_render.py: D01 to D07 AGREE. Rerun
  scripts/e2e_gate.py: at head, D01 and D02 read `exempt ok` and D03 and D04
  read `refused ok`. An N01-style reversion fails a named arm.
  scripts/corpus_compare.py still reports 0 differing pages.
```

```text
[R238] SUGGESTION Conformance, Robustness - scripts/gen_toc.py:517-520 (`_still_open`: a type-6 or type-7 block ends only at a blank line), :369-371, receipts/probes-table.txt rows P02, P03, F09 - F3 (pre-existing, identical at base and head): an HTML block opened at a list item's content column ends for GitHub when the item ends, but the walk holds it to the next blank line
Requirement/evidence: GitHub ends a block inside a list item when a column-0
  line ends the item. P02 (`- item`, blank, `  <span>`, then a column-0
  fence, blank, `## Old`) and P03 (`  <div>`) render no `Old`. Both walks
  swallow the fence inside the HTML block and list `Old`, and end to end P02
  is exempt at base and head (receipts/e2e-table.txt). F09 is the
  withholding twin: a heading right after such a block renders, and both
  walks hide it. Neither docstring declares this shape.
Impact: This is an escape of the same kind as #437's family one, but outside
  the families #437 enumerates and outside this change. It is unreached by
  the tracked corpus (0 type-7 tag lines). Once `Closes #437` lands, the two
  withholding residues the head docstring keeps (:369-371) also have no
  owning Issue. The base docstring said they were carried by #437.
Required change: None for this PR. Open a public follow-up Issue for P02, P03
  and F09 and the two retained withholding residues, plus P01 and P04 if F1
  is repaired without them, each with direction and boundary. Until then, the
  documentation must not imply the escape direction is closed (the Docs part
  of F1).
Verification: The follow-up Issue cites these rows, and scripts/probe_render.py
  rows P02, P03 and F09 reproduce them.
```

## Clean lens

```text
[R238] PASS RTL - receipts/rtl-lens.txt (git diff --name-status and tree-object comparison 88e9276b..65df1df5), receipts/gates-head/ci-events.log and ci-events-selftest.log, manager packet e6013980 review-evidence/437-r1/manager/full-native/results.json, manager-builder/results.json and builder-final-tree-integrity.json - no HDL, constraint, firmware, workflow, synthesis, testbench, suite inventory, .gitmodules or gitlink object changes; ci_events --check 1505 items and --selftest 1144 arms identical at base and head; the manager's five native groups and 43 builder commands are attributed to this exact head and exit 0, so clock, reset, CDC, FSM, width and backpressure questions have no artifact in this change
```

## Verified at this head

These results support the ledger but do not bank the four open lenses.

- **Family one repaired.** A01 to A20 are independent respellings of R86-5's
  nine described shapes, plus `+`, `1)`, `0.`, custom, closing,
  self-closing and attribute tags, and tags one or two columns below the
  content column. All INVENT at base and AGREE at head. End to end, A01, A04
  and A07 are exempt at base and refused at head (receipts/probes-table.txt,
  receipts/e2e-table.txt).
- **Named boundaries hold.** B01 to B06 (one space, four spaces, block quote,
  footnote at two and four spaces, tab) AGREE at base and head. B01 and B03
  are exempt end to end at both.
- **Shipped arms are true.** All 47 I437 page arms agree with GitHub
  (receipts/arms-vs-github.txt). All 47 rows of the author's published
  renderer receipt are byte-identical to independent renders today, and
  their base and head answers reproduce (receipts/author-receipt-check.txt).
- **Family two documented.** GitHub renders each of G01 to G05 as a heading.
  Both walks omit them, and the head gate refuses each copied label
  (receipts/e2e-family-two.txt). This is documented at gen_toc.py:373-378
  and CONTRIBUTING.md:518-523, with its direction (withholding) and its
  boundary (the five forms; setext and container headings outside the
  listing domain).
- **AC4 corpus.** The comparison covers 163 tracked pages: the base tree has
  46,252 lines and the head tree 46,261. `blocks`, `line_kinds`,
  `headings` (with anchors), `plan`, `generated_block`, `owns` and
  `refusals` are identical under both walks on both trees. Digests are
  `3b53cfe1…` and `c9ad15f6…` (receipts/corpus-compare.txt).
- **Prior classifications and #507 controls preserved.** All 707 base arm
  pages classify identically under both walks.
  `gen_toc_closer_cases.py` and `gen_toc_guards.py` are byte-identical.
  `gen_toc_cases.py` differs only in the two guard expectations (8 to 9
  families, 25 to 27 sites) (receipts/prior-arms.txt). `check_em_dash.py`
  differs only in its self-test integration. `base_labels`, `judge_page`,
  `generated_block` and `refusals` are unchanged.
- **Gates.** At the head, 17 commands exit 0 (receipts/gates-head/summary.txt):
  - TOC self-test 754/754, `--check` 105 pages, `--verify-anchors` 144.
  - em-dash self-test 99 arms; `--base 88e9276b` gives 0 findings over 9
    added lines, 0 exempt.
  - `docs_check` 0 findings over 163 + 828 files.
  - `check_py_idiom`: long function 9 <= 9, long module 10 <= 10, too many
    parameters 7 <= 7, over-long line 0 <= 0.
  - hygiene, doc-style, doc-paths and ci_events.
  - No budget file changed. At the base: 707/707 and 57 arms
    (receipts/gates-base/summary.txt).
- **Mutation controls fail for their own defect.** I ran 18 independent
  mutants (M01 to M18). They cover the 17 defect names the author published,
  plus one more. Each fails both self-tests with named I437 arms. None is
  caught by a guard alone: M01 also trips the site-count guard, but fails 18
  I437 arms. See receipts/mutants-table.txt and receipts/mutants.json.
- **Code quality.** The new helper and case functions carry complete
  signatures and docstrings (CODE_QUALITY rule 12). `REFUSED` and
  `refusals()` are unchanged.

## Acceptance criteria against the frozen contract

- **AC1 - met for every determinable member, with a recorded evidence
  limit.** R86-5 names eleven rows (H01 H02 H05 H06 H10 H13 H25 H28 H29 H31
  G02) and describes nine shapes. The shapes archive is not public, so two
  rows cannot be determined from any public artifact, and byte identity is
  neither assumed nor claimed.
  - All nine described shapes and eleven further respellings agree at head.
  - By R86-5's statement, every original row is a shape the base walk
    invents and GitHub hides. Such a row could still fail at head only if the
    head missed the item context.
  - A bounded search found no such shape. Of 300 pages carrying the family's
    precondition that both walks still invent, a seeded sample of 40 was
    rendered, and GitHub shows `Old` in all 40
    (receipts/unfixed-family-one.txt).
  - The only shapes the head newly invents are F1 and F2's. The base walk
    answers those correctly, so they cannot be original rows.
  - The six boundary rows agree.
- **AC2 - met** through the selected limitation path, with direction and
  boundary.
- **AC3 - partly met.** The implemented properties are armed (M01 to M18).
  The tag line's column boundary (F1) has no arm, and the release of an item
  at a dedented quote or footnote (F2), which the docstring claims, has none.
- **AC4 - met.** No tracked page changes classification, and no family-two
  heading is added.
- **AC5 - met locally.** The named gates pass and no ratchet is widened.
  Hosted and act contexts are outstanding.
- The five omissions stay documented. No exemption or provenance rule
  changed. Product RTL, firmware, workflows and the PP/gPTP pins are
  unchanged.

## Both consumers

- **Navigation (`apply`, `plan`, `--check`):**
  - On the C04 and D03 pages, the head writes `[Old](#old)` for a heading
    GitHub does not render.
  - On C01, the head drops a rendered section and falls below the
    three-section threshold.
  - Corpus navigation is unchanged: `--check` is OK and 144 anchors
    reproduce (receipts/navigation-consumer.txt).
- **Real-Git em-dash provenance:** `judge_page` ran on fixture repositories
  built with the gate's own helpers, with a head page produced by
  `gen_toc.apply()`.
  - Family one is repaired, and the boundaries stay exempt.
  - C04 to C08 and D03 to D04 are newly exempt; C01, D01 and D02 are newly
    refused.
  - Only the label decision is scored. The table's other column is an
    added-heading finding caused by this fixture's own diff alignment,
    identical at base and head (receipts/e2e-table.txt).

## Lens ledger

| Lens | Covering round | Head | Result |
|---|---|---|---|
| Conformance | [R238] r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | not covered clean: F1, F2 (MAJOR) open |
| RTL | [R238] r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | covered clean |
| Robustness | [R238] r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | not covered clean: F1, F2 (MAJOR) open |
| Tests | [R238] r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | not covered clean: F1, F2 (MAJOR) open |
| Docs | [R238] r1 | 65df1df50a80cd5f540a93d8f0cfabc97da3da75 | not covered clean: F1, F2 (MAJOR) open |

All five lenses were applied in this round. F3 is a SUGGESTION and affects
no lens. A later commit touching `scripts/gen_toc.py` or its case tables
un-covers every lens except, possibly, RTL. RTL too is un-covered if that
commit reaches its scope.

## Open findings

- **F1 MAJOR** (Conformance, Robustness, Tests, Docs): content-column tag
  under a resumed item paragraph.
- **F2 MAJOR** (Conformance, Robustness, Tests, Docs): item context
  survives a dedented block quote or footnote definition.
- **F3 SUGGESTION** (Conformance, Robustness): pre-existing HTML block
  inside a list item, plus the follow-up Issue.

## Limits of this round

- **Deferred, not inferred:**
  - No hosted run or check was inspected (prohibited this round).
  - No act, Docker, native RTL, Yosys, processor or builder rerun was
    made.
  - Native evidence is the manager's, attributed to `65df1df5`. The host
    reports Verilator 5.052; hosted and act runs use the workflow-pinned
    5.050. Builder gate 11 is NOT RUN. The manager reports four field-campaign
    skips, which contribute zero checks.
  - None of that is physical evidence, and none of it counts as a hosted or
    act pass here.
- **Oracle time window:** the oracle is GitHub's renderer as of 13:52 to
  14:08 UTC, 2026-09-22.
- **Bounded sweep:** receipts/sweep.txt covers 173,375 walked pages; 90 of
  the 720 divergent pages were rendered. The head is wrong on 50 of those 90
  and the base on 40. All of the head's errors are F1 or F2, and the
  feasibility walk is right on all 90. The sweep is not exhaustive.
- **Feasibility control only:** scripts/candidate_repair.py is not a
  proposed patch. It was checked only against the two self-tests, the corpus
  comparison and the probes.
- **Historical archive:** the R86-5 archive remains unavailable (see AC1).

## Outstanding manager duties

1. Trusted act replication on the final head is queued; its start was not
   observed. Pending.
2. Required hosted contexts on the final head are pending and were not
   inspected by R238.
3. R237's internal review is independent of this round and was not read.
4. Answer F1 and F2 on a new head. A new round must then re-cover
   Conformance, Robustness, Tests and Docs at that head, and RTL too if the
   commit's scope reaches it.
5. Decide on F3's follow-up Issue before `Closes #437` lands.
6. Current-candidate validation is needed if `dev` moves.
7. Maintainer merge authorization; post-merge containment and
   review-integrity audits; Issue closure and Done.

## Boundaries observed

- **GitHub access was read-only:** GETs, `git ls-remote`, and the render API
  with synthetic pages. I made no comment, review, label, project change,
  push, merge or other write. I called no run, check or Actions API. PR
  metadata came only through explicit fields.
- **Local isolation:**
  - The review checkout was never edited.
  - All work happened in scratch clones under this directory. Their
    submodules were populated from the review checkout's local copies,
    without network.
  - Mutants and the feasibility walk ran only in disposable scratch
    worktrees.
- **Not done:** I did not execute the candidate's `act_ci` or its
  self-test. I used no Docker, act, install, privilege, hardware or
  subagent, and made no author contact. At most 8 jobs ran at once.

## Reproduction

`scripts/reproduce.sh` reruns every measurement in order from the renderer
cache; no request leaves the host when the cache is present. The last run
completed 17 steps, every one exit 0 (receipts/reproduce-exits.txt).

| Script | What it does |
|---|---|
| `probe_render.py` | 62 probes |
| `e2e_gate.py`, `e2e_gate_worker.py` | real-Git gate at base and head |
| `e2e_family_two.py` | the five documented forms |
| `arms_vs_github.py` | shipped arms against GitHub |
| `author_receipt_check.py` | author receipt bytes |
| `corpus_compare.py` | AC4 comparison |
| `census.py` | corpus reach |
| `prior_arms.py` | 707 prior arms |
| `mutate.py` | M01 to M18 and N01 |
| `candidate_repair.py` | feasibility control |
| `sweep.py`, `unfixed_family_one.py` | bounded search |
| `navigation_consumer.py` | generated Contents |
| `run_gates.sh` | focused gates |
| `integrity.py` | review-checkout integrity |

MANIFEST.sha256 lists every file.

R238-r1 FINISHED

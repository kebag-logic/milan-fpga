[R237] NEGATIVE - exact head 34f124f9b0dabeb74c655052f0a0858620a09037

Round R237-4, internal cleared-context review of issue #437 / PR #515.
Head `34f124f9b0dabeb74c655052f0a0858620a09037`, tree
`bb9b3dbc70a81af453f47c4c72aeb8433d927d91`. Merge base and live dev
`ede8d48ecd7c7f589a14b957951f040d92c99c70`. The base's `scripts/gen_toc*.py`
and `check_em_dash.py` are byte-identical at `ede8d48e` and `88e9276b`, so
"the base walk" below means both. All five lenses were applied: Conformance,
RTL, Robustness, Tests and Docs. Two MAJOR and two MINOR findings are open, so
every lens is UNCLEAN at this head. This is not merge approval.

Reconstructed in this order: AGENTS.md; CONTRIBUTING.md (2, 3, 5, 6, 6.1);
docs/README.md; issue #437 (body with acceptance 1 as restated and as amended
2026-09-23 14:15, the owner decision 5794734885, the assignments 5775771538,
5789003484, 5790500052 and 5795309062, the A190 decision 5791031813, A201
TAKEN 5795467933 and REVIEW READY 5795921214); issue #516 (body and owner
decision 5794735214); the PR body; CommonMark 0.31.2 sections 4.6, 4.7, 5.1,
5.2 and 6.6; then `git diff ede8d48e..34f124f9` and its history; then the
exact-head hosted check list and the author packet `correction-a201/` at
evidence commit `ccc7b2b1`. The verdict, findings and ledger came from this
round's own pass. They were written into this file (stage 1) before any prior
review report was opened. Prior findings were then read only to give their
dispositions below.

## Summary

The split correction does what the owner decision asked of it:

- The rendered-comment emulation is gone. `gen_toc_html.py` is deleted, and
  `_comment_after` and `_still_open` are byte-identical to the base.
  `blocks()` ends only a fence or raw HTML block with its container, never a
  comment. Both removed rules are armed: a mutant ending a comment with its
  container, and one closing `<!-->`, are each killed.
- The unclosed raw-HTML comment family is stated as a directed escape
  limitation owned by #516, with its boundary, in the `blocks()` docstring,
  CONTRIBUTING.md 6.1 and DOC_GENERATION. 24 shapes, one per stated sentence,
  were rendered fresh. 23 show the stated direction. The `--!>` probe shape
  agreed instead: GitHub's raw HTML block never ends there and the walk's
  comment never closes, so both hide the rest. That is a limit of the probe,
  not an error in the text.
- The container walk holds against GitHub on its core domain:
  - 1,931 fresh probe renders show 1,221 fixes against the base;
  - every family-one shape agrees (51/51), and the nine R86-5 descriptions
    are mapped;
  - all 175 fixture receipts re-render byte-identical;
  - tracked-page classification is unchanged;
  - an item-lifetime matrix (1,044 pages) has 0 regressions.

Two regression classes outside the amended carve-out remain, and neither has an
owner decision:

- F1 (new): an item holding a link reference definition that is not in the
  recognised one-line form is kept open. Eight valid CommonMark 4.7 forms
  regress against the base, mostly in the escape direction. End to end, the
  copied em-dash label is exempt at the head and refused at the base.
- F2: the residues the author disclosed, where ending a block with its list
  item uncovers what the base hid by accident. Six committed fixture shapes
  regress against the base, three in the escape direction. They are labelled
  `#516`, but the amendment excludes only the unclosed-comment family.

F3: four new properties have no failing arm (acceptance 3). F4: stale fixture
metadata still names the removed rules.

## Findings

```text
[R237] MAJOR Conformance, RTL, Robustness, Tests, Docs - scripts/gen_toc_containers.py:236-239 (a line fills its item unless it is a LINK_DEFINITION_RE line), scripts/gen_toc.py:237-244 (LINK_DEFINITION_RE: one line, bare destination, optional double-quoted title), scripts/gen_toc.py:423-424 (a fence or raw HTML block ends with the container it opened in), CONTRIBUTING.md:583-585; receipts/probes/run1.json (family L), link_def_examples.txt, link_def_tally.txt, emdash_e2e_link_def.txt - F1: a list item holding a link reference definition in any other valid form is kept open; a fence or raw HTML block opened in it after two blank lines is then ended at the late item end, and the walk lists a heading GitHub and the base walk both hide
```

Requirement/evidence:

- **The bar.** Amended acceptance 1 keeps "every shape that agreed at the base
  still agrees" and excludes only shapes whose rendering depends on a raw-HTML
  comment the renderer leaves open. The maintainer restatement 5788996063
  holds that bar beyond the family-one set.
- **CommonMark 4.7 and 5.2.** A paragraph made only of definitions is removed
  when it closes. A blank line then continues an item only while it holds a
  block. The head applies this only to lines matching `LINK_DEFINITION_RE`.
  These valid definition forms are read as content, so the item stays open:
  - an angle-bracket destination (`[a]: <u>`, `[a]: <>`);
  - a single-quoted or parenthesised title;
  - a destination or title on the next line;
  - a backslash in the label;
  - nested parentheses in the destination.
- **Fresh renders.** 80 of 80 probes regress against the base: 8 forms, a
  bullet or an ordered marker, and 5 follower blocks at the item's column
  after two blank lines. 64 of them escape and 16 withhold. The pages carry
  no `<!--`, so none is in the carve-out. Examples, with the headings listed
  by GitHub / the base walk / the head walk:

| Page | GitHub | Base | Head |
|---|---|---|---|
| `` - [a]: <u>\n\n\n  ```\n## Old\n```\n\n## Real\n `` | Real | Real | Old |
| `- [a]: /u 't'\n\n\n  <div>\n## Old\n\n## Real\n` | Real | Real | Old, Real |
| `1. [a]:\n   /u\n\n\n   <pre>\n## Old\n</pre>\n\n## Real\n` | Real | Real | Old, Real |
| `- [a]: /u (t)\n\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n` | Old, Real | Old, Real | Real |
| control `` - [a]: /u\n\n\n  ```\n## Old\n```\n\n## Real\n `` (recognised form) | Real | Real | Real |

  GitHub's HTML for the first row is `<ul><li></li></ul>`, then a code block
  holding `## Old`: the item is empty. With one blank line the same 80 item
  shapes are fixes (80/80). In a block quote the base and head walks answer
  alike, so no regression is possible there.
- **Not decided.** The author's handoff names this as a limitation ("can list
  or withhold a heading"). Its regression census (25 pages: 10 of #516 and 15
  residues) and the PR body do not count it as a regression against the base,
  and no owner decision covers it. No fixture shape or arm pins any of these
  forms, either as agreement or as a `limitation`.
- **State model.** The item's emptiness is decided by a recognizer narrower
  than CommonMark 4.7, and the default path keeps the item open. The rule
  that ends a block with its container then fires at the wrong line. This is
  the same mechanism as R237-3 F2, with the escape direction now measured.

Impact:

- End to end through the shipped gate, with real Git base and head commits
  (receipts/probes/emdash_e2e_link_def.txt), a copied label
  `Old <U+2014> heading` gives these results on the angle-destination,
  single-quoted, multi-line and parenthesised shapes:
  - base gate: `findings=1 exempt=0`, reason `mirrors no heading`;
  - head gate: `findings=0 exempt=1`.
  The recognised-form control is refused by both.
- The generator also plans navigation to a section GitHub does not render.
- No tracked page reaches it: acceptance 4 shows 0 differences. That, and
  the uncommon syntax, is why this is MAJOR and not BLOCKER.

Required outcome: no page that agreed with GitHub at the base disagrees at the
fix head for items holding link reference definitions. That covers at least
the 80 family-L rows of receipts/probes/run1.json. The alternative is a
recorded owner decision that accepts this named regression class, with its
direction, its boundary and an owning Issue. Then 6.1, the docstring and the
PR state that it regresses base-agreeing shapes. Either way, an arm pins each
definition form's answer, and it fails when the behaviour changes.

Verification: rerun `scripts/probe_run.py receipts/probes/corpus1.json` at the
fix head: zero `regress` rows in family L. `scripts/emdash_e2e.py` against the
fix head's scripts refuses the four escape shapes. A mutant that removes the
new handling is killed at a named arm.

```text
[R237] MAJOR Conformance, Robustness, Docs - scripts/gen_toc_container_walk.json:629, :656, :683, :1837, :1860, :1883 (shapes "item block ends before a code span / an escape / an inline attribute", "item end uncovers an open quoted value / a type-3 block / a comment over a fence", each marked `limitation` owner "#516"), scripts/gen_toc.py:423-424, CONTRIBUTING.md:597-603; receipts/triage/fixture_triage.json, receipts/prior/per_heading_new_escapes.txt, receipts/prior/dispositions_check.txt - F2: shapes that agreed at the base disagree at this head outside the amended carve-out, and are labelled as #516's without an owner decision covering them
```

Requirement/evidence:

- **The carve-out.** Amended acceptance 1 excludes only "shapes whose
  rendering depends on a raw-HTML comment the renderer leaves open".
  - The three withhold rows fall outside it. GitHub shows `<!--` in a code
    span, after an escape and in an attribute as text: nothing is left open.
  - The quoted-value and type-3 rows involve no comment.
  - `<!-->` is a closed, empty comment on GitHub.
  - The six rows regress in fixture triage: GitHub agrees with the base, and
    the head differs. Three escape (quoted value, type-3, `<!-->` over a
    fence) and three withhold.
- **Prior rounds' recorded pages.** The replay of all 6,687 unique pages
  finds the same classes outside the #516 family:
  - R238-2 seed-238 rows #668 and #672 escape: a type-3 block is uncovered
    when the item's block ends;
  - R237-2 F2's three in-item rows withhold.
- **The author asked for this decision.** REVIEW READY 5795921214 and the
  handoff say that 15 regressions outside the #516 family "need a public
  decision". None has been published. The #516 owner comment 5794735214 moves
  modelling of the named R237-3 and R238-2 findings. It does not amend the
  no-regression clause for these classes.
- **The labels.** The fixture and the arm names still say `#516`. The
  type-3 row's reason says #413, and 6.1 attributes type 3 to 5 to #413.

Impact:

- Three escape rows are in the direction that grants the em-dash exemption to
  a label with no anchor on the page. The fixture's own em-dash rows pin the
  walk's answer.
- A cold reader of the fixture or of 6.1 would take these as #516's accepted
  limitation, and that decision does not exist.
- MAJOR, not BLOCKER: no tracked page reaches these shapes, and the author
  disclosed them.

Required outcome: either base agreement is restored on these shapes, or a
recorded owner decision accepts each named class. That decision states its
direction, its boundary, that it regresses base-agreeing shapes, and its
owning Issue. The fixture `limitation.owner` fields, the arm names and 6.1 then
name that owner. R237-2 F2's three rows are retained until then.

Verification: `scripts/fixture_triage.py` shows no `regress` row whose owner
lacks a matching decision. `scripts/replay_prior.py` shows seed-238 #668 and
#672 and R237-2 F2's rows either agreeing or covered by that decision.

```text
[R237] MINOR Tests, Conformance - scripts/gen_toc_containers.py:123 (`_lazy` treats an ATX heading and a thematic break as no lazy line), :230-231 (the container layer reads a `<!--` after text, or four or more columns in, as no comment block), scripts/gen_toc.py:241-244 (LINK_DEFINITION_RE's negative boundary); receipts/mutation/mutants_round2.json, mutants_round3.json, mutants_round4.json, survivor_impact*.txt - F3: four new properties have no arm that fails when they are removed (acceptance 3)
```

Requirement/evidence:

- **Acceptance 3** requires that each new property carries an arm that fails
  when the property is removed. Every mutant below passes
  `gen_toc.py --selftest` 1269/1269 and `check_em_dash.py --selftest` 429.
- **What each survivor changes.** Each was measured over this round's three
  corpora plus that mutation round's extra pages (4,507 to 4,518 pages), with
  every page where the mutant differs from the head rendered:

| Mutant | Pages that change | Head agrees with GitHub | Mutant escapes |
|---|---|---|---|
| a heading may be a lazy line (`ATX_HEADING_RE` dropped from `_lazy`) | 3 | 3 | 2 |
| a thematic break may be a lazy line | 2 | 2 | 2 |
| the container layer's inline-comment rule removed | 9 | 9 | 0 (withholds) |
| the rule kept only after text (four columns in removed) | 3 | 3 | 0 (withholds) |
| `LINK_DEFINITION_RE` accepts any trailing token as a title | 22 | 12 | 10 |

  For example, `` - a\n## H\n  ```\n## Old\n```\n `` gives GitHub H; head H;
  mutant H, Old. And `text <!-- c\nmore -->\n<span>\n## Old\n` gives GitHub
  and head Old; mutant nothing.
- **Guard-only kills.** Two first-round mutants were killed only by the class
  guard, because they spelled a class inline. Respelled through the shipped
  helpers and classes, both survive. One of them is the widened definition
  regex above. The other, whitespace-only footnote continuation, changed no
  heading on any page.

Impact: a later edit can remove any of these rules with every gate green. Two
of the removals reintroduce escapes, one loses measured fixes, and the widened
recognizer lists headings GitHub hides, the direction in which the em-dash
exemption follows the walk.

Required outcome: an arm fails when each of the four properties is removed or
widened as above.

Verification: `scripts/mutate_rounds.py` at the fix head kills these four
mutants at arms named for the property.

```text
[R237] MINOR Docs - scripts/gen_toc_container_walk.json `pins` fields at :631, :658, :685, :712, :739, :799, :826, :875, :902, :942 to :1497 (25 limitation shapes), `limitation.owner` at :1860's shape - F4: fixture metadata names rules the walk no longer applies
```

Requirement/evidence:

- The fixture's own `about` says that "pins names the finding or rule each
  shape holds".
- 25 limitation shapes still carry pins that name removed emulation rules:
  - "R237-2 F2: a comment opener outside HTML's data state opens nothing";
  - "raw HTML the walk reads as the page's HTML parser does";
  - "a closer in Markdown text counts only inside inline raw HTML".
  Each of these shapes now pins the walk's recorded limitation answer, and
  the walk no longer applies the named rule.
- The type-3 shape names owner `#516`, while its reason and CONTRIBUTING.md
  6.1 say #413.

Impact: a reader or a failing arm is pointed at a rule and an owner that do
not hold at this head.

Required outcome: every `pins` states what the shape holds at the fix head,
and every owner field names the Issue that owns the class, consistent with F2's
decision.

Verification: re-read the fields against `scripts/fixture_triage.py` output
at the fix head.

```text
[R237] SUGGESTION Docs - scripts/gen_toc.py:395-410 (blocks() docstring), CONTRIBUTING.md:587 - S1: after a comment closes, the type-7 gate follows the container layer's CommonMark reading (an inline or four-column `<!--` is paragraph text), also on pages without containers
```

On pages without containers the head differs from the base on 27 measured
probe pages, and every one is a fix: 9 follow a closed inline or four-column
comment, and 18 follow a raw type 3 to 5 line (receipts/probes/doc_claims.txt).
For example, `text <!-- c\nmore -->\n<span>\n## Old\n`: the base withholds,
and GitHub and the head list Old. "Comments are read as before" is true of
the labels. Saying that the gate after a closed comment is the container
layer's would remove the ambiguity. Optional.

## Evidence that holds at this head

These are recorded in the clean-result format for the artifacts examined. They
do not clean any lens F1 to F4 leave open.

```text
[R237] PASS Conformance (partial) - scripts/gen_toc_family_one.json; receipts/triage/fixture_triage.json, rerender_fixtures.json, family_one_listing.txt - amended AC1's shape set: 51 shapes (bullet, star, ordered and two-digit ordered at and past the column, inline and unknown tag, inside and outside, two-digit below its column, one space, four spaces, quote, footnote at two and four, tab); nine `r86_5` descriptions mapped; 51/51 agree at the head (36 agreed at base, 15 fixed); 175/175 fixture receipts hash-verified, request bytes carry the page, and fresh re-sends are byte-identical
[R237] PASS Conformance (removal) - scripts/gen_toc.py (`_comment_after`, `_still_open` byte-identical to ede8d48e), `git ls-tree` (no gen_toc_html.py), receipts/mutation/mutants.json (comment-ends-with-container, empty-comment-closes killed) - the rendered-comment emulation is removed and comments are read as at the base
[R237] PASS Conformance (AC4) - receipts/triage/ac4.txt - blocks, line_kinds, headings with anchors, plan, refusals and generated_block identical under base and head walks on 164, 164 and 163 tracked pages of 34f124f9, ede8d48e and 88e9276b
[R237] PASS Docs (limitation statements) - receipts/probes/doc_claims.txt - one shape per sentence of the comment reading, the #516 limitation and the HTML-parse escapes in 6.1 and the docstring, each rendered fresh; 23 of 24 show the stated direction, and the `--!>` probe shape agreed instead (a limit of that probe, not of the text)
[R237] PASS Robustness (partial) - receipts/triage/crash_fuzz.txt, receipts/probes/run3.txt - 60,000 seeded pages, 0 exceptions, slowest page 4.8 ms; item-lifetime matrix 1,044 pages, 550 differ from base, 502 fixes, 0 regressions, 48 wrong at both (all family-two headings)
[R237] PASS Tests (partial) - receipts/mutation/mutants.json, mutants_round2.json, mutants_round3.json, mutants_round4.json - 28 of 41 mutants killed (two only by the class guard), 26 at arms named for the property: among them the gate, block end with container, R237-3 F4's quote end, R238-2 F2 C17's type-3 end, the type 3-5 gate, lazy quote/footnote/item/type-3 lines, content column, nested fill and definition-only emptiness; of the 13 survivors, six changed no heading on over 4,500 pages and five are F3
[R237] PASS Conformance (AC5) - receipts/gates/EXITS.txt - 22 focused commands exit 0: gen_toc --selftest 1269/1269, --check 106 pages, --verify-anchors 144, --sites 29; check_em_dash --selftest 429, --base ede8d48e 0 findings over 39 added lines, 0 exempt; docs_check and selftest, doc style and selftest, doc paths, Python idiom and selftest (long module 10<=10, long function 9<=9), hygiene, TODO ownership, naming, fail fast, test evidence, control-flow and cohesion selftests, feature status, git diff --check; no budget file in the diff; gen_toc.py 999 lines under its 1000-line ratchet
```

## Prior public findings at this head

Each row was re-checked against the prior round's recorded GitHub renderings
(receipts/prior/replay_prior.json, 6,804 rows from evidence commit `ccc7b2b1`)
and, where named, against this round's mutants.

| Finding | Severity; lenses | Disposition at 34f124f9 | Evidence |
|---|---|---|---|
| R237-3 F1: rendered-comment model regressions | MAJOR; all five | RESOLVED by removal; the owner decision moves further modelling to #516 | E1, E1b, E2, E2b, E5, E5b, E6, E6b and E9 agree as at the base; on E8 both walks omit Old as GitHub does (heading A's text differs at both, as before); the model is deleted |
| R237-3 F2: definition-only item outlives a second blank | MINOR; Conformance, RTL, Robustness, Tests | RESOLVED for E7 and its stated shapes; the class continues as R237-4 F1 | E7 agrees; mutants link-definition-ignored and open-paragraph-not-held killed; other definition forms regress (F1) |
| R237-3 F3: escape inventory incomplete | MINOR; Conformance, Robustness, Docs | RESOLVED under its own required outcome; modelling moved to #516 by owner decision 5794735214 | 6.1 names open tag, bogus comment, quoted value and `<select>`, says the list is measured and not exhaustive, and records #516; E3 and E4 now fall in the #516 family, and E10 and E12 in the named quoted-value class |
| R237-3 F4: quote end at a blank line unarmed | MINOR; Tests | RESOLVED | mutant blank-continues-quote killed at `I437 rendered R237-3 F4 a blank line ends a quote` |
| R238-2 F1 (a) to (d): comment rules regress the base | MAJOR; all five | (a) to (d) RESOLVED: the rules are removed, and (d) the type 3-5 gate is armed. Two seed-238 rows RETAINED under R237-4 F2 | batch1 and batch2 rows agree or are wrong at both as at the base; tag-in-type-3/4/5 rows agree; seed-238: 301 of 303 regression rows agree, #668 and #672 still escape (type-3 uncovered, no comment involved); mutant raw-3-5-gate-not-none killed |
| R238-2 F2: C17, H06, H10 unarmed | MINOR; Conformance, Tests | RESOLVED | C17 mutant killed at `I437 rendered R238-2 F2 C17 ...`; H06 and H10 were properties of the removed HTML stage; batch3 rows agree or are wrong at both as at the base |
| R238-2 F3: "two escapes remain" is false | MINOR; Docs | RESOLVED for the documentation; modelling moved to #516 by owner decision 5794735214 | the claim is gone; `<select>` is named; the link-destination closer row falls in the #516 family |
| R238-2 S1: per-call import, private names | SUGGESTION; RTL | not adopted; optional, no lens effect | - |
| R237-2 F1: gate whatever holds the item; in-item block never ends | MAJOR; all five | RESOLVED | 252/252 base-agreeing combinatorial rows agree; mutants gate-ignored, no-end-with-container and owner-always-page killed |
| R237-2 F2: flag on any `<!--` substring | MAJOR; all five | RETAINED for its three in-item rows under R237-4 F2 | 7 of 10 rows agree; the three flat-item rows (code span, escape, attribute) agree at the base and withhold at the head |
| R237-2 F3: empty-item guard unarmed | MINOR; Tests | RESOLVED | holds-always killed at `I437 empty item ends at blank`; empty-item-content-at-marker killed |
| R237-2 S1: opener four columns into an item | SUGGESTION; Conformance, Robustness | inside the #516 limitation, as at the base | both rows answer as the base does; 6.1 names "four columns into a list item" |
| R237-r1 F1, F2, F3; R238-r1 F1, F2, F3 | MAJOR (F3 of R238-r1 a SUGGESTION) | RESOLVED | batch4_prior: every published shape agrees at the head; family-one fixture 51/51 with nine R86-5 mappings |
| #516 twelve variants | manager-tracked | excluded by amended AC1; documented limitation | the six resumed variants agreed at the base and escape at the head; the six first-paragraph variants were already wrong at the base. All twelve are pinned as `#516` limitation shapes |

## Acceptance at this head

| Criterion | Result | Evidence |
|---|---|---|
| AC1: shape set committed, rendering recorded at the fix head, coverage list, nine R86-5 mappings, every family-one shape agrees | met | family-one fixture; 175/175 fresh re-sends identical; 51/51 agree |
| AC1 (amended): every shape that agreed at the base still agrees, outside the unclosed-comment family | NOT met | F1 (80 probe rows), F2 (6 fixture rows; seed-238 #668, #672; R237-2 F2's 3 rows) |
| AC2: five family-two forms named with direction | met | CONTRIBUTING.md:572-577; gen_toc.py:412-416; `I437 limitation` arms; wrong-at-both rows are all family-two headings |
| AC3: each new property has a failing arm | NOT met | F3 |
| AC4: tracked classification unchanged | met | 0 differences on three trees |
| AC5: gates pass, no ratchet widened | met locally; hosted docs-check at this head passed 1269/1269 and 429/429 | receipts/gates; hosted check list |

## Reviewer-owned completion ledger

Every lens was applied at this exact head. None is covered clean.

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | amended AC1 to AC5 and the owner decisions; CommonMark 0.31.2 4.6, 4.7, 5.1, 5.2 and 6.6 against 175 fixture re-sends, 1,931 fresh probe renders and 6,687 prior recorded pages; base, previous-head and head walks | none; applied by R237-4 | 34f124f9b0dabeb74c655052f0a0858620a09037 |
| RTL | UNCLEAN (F1) | product scope: `git diff --stat ede8d48e..34f124f9` has 10 paths (CONTRIBUTING.md, docs/DOC_GENERATION.md, 8 under scripts/), with no HDL, testbench, constraint, workflow, budget, `.gitmodules` or gitlink change, and the required gitlinks sit at their pins. Architecture scope: the `blocks()` state machine (gen_toc.py:418-433), `Scope`, `_step`, `_inside`, `_open` and `_leaf_line` (gen_toc_containers.py:62-252), the two leaf machines' comment readings (S1), the class guard over both walk modules (29 single-source sites) and the import registration | none; applied by R237-4 | 34f124f9b0dabeb74c655052f0a0858620a09037 |
| Robustness | UNCLEAN (F1, F2) | link-definition forms, item lifetime (empty, padded, tabbed, nested, lazy, sibling, table, footnote items), fences and types 1, 3, 4, 5, 6 and 7 in containers, footnote blank and whitespace lines, top-level comment and raw-HTML interplay; 60,000-page crash fuzz | none; applied by R237-4 | 34f124f9b0dabeb74c655052f0a0858620a09037 |
| Tests | UNCLEAN (F1, F3) | gen_toc_container_cases.py, the three fixtures and their limitation arms, check_em_dash.py self-test wiring; 41 mutants in four rounds with survivor measurement; hosted docs-check self-test counts | none; applied by R237-4 | 34f124f9b0dabeb74c655052f0a0858620a09037 |
| Docs | UNCLEAN (F1, F2, F4) | CONTRIBUTING.md:572-606; docs/DOC_GENERATION.md:30, :60-61; the gen_toc.py docstring :385-416 and the gen_toc_containers.py docstring :1-41; fixture `about`, `pins`, `limitation`; PR body; issue REVIEW READY and the author handoff | none; applied by R237-4 | 34f124f9b0dabeb74c655052f0a0858620a09037 |

A commit touching the walk modules, their case tables or fixtures, or
CONTRIBUTING.md 6.1 un-covers every lens except, possibly, RTL's product
scope.

## Hosted evidence at this head (list only)

These were listed at 2026-09-23T14:48Z (receipts/hosted-check-runs.tsv). Only
the docs-check job log was read, for its self-test counts.

- All seven required contexts concluded `success`: rtl-fast, docs-check,
  wire-accountability, docs-check-no-git, elaborate, verilator-suites and
  yosys-portability.
- Verilator shards 0-4 and Yosys shards 0-3 executed and succeeded, as did
  `full-ci-gate`, `changes`, `verilator-lint`, `yosys-elaboration` and
  `bdd-conformance`.
- `Physical gPTP (nightly and manual)` is `skipped`. That is not hardware
  evidence.
- The hosted docs-check ran on ubuntu-24.04 and reported
  `TOC selftest: PASS (1269/1269 arm(s))` and em-dash `arms 429/429`. So the
  fixture arms parse the recorded HTML the same way on that runner's Python.
  The hosted gates run the shipped self-tests, which cannot see F1 to F3.
- Hosted and act acceptance remain with the manager.

## Limits

- **Oracle.** GitHub's Markdown API (`POST /markdown`, mode gfm, context
  `kebag-logic/milan-fpga`) was sent synthetic pages only, between 14:13 and
  14:41 UTC on 2026-09-23.
  - The API returns sanitised HTML, so a raw comment is already resolved in
    it. Headings are read from that HTML with a standard HTML parser.
  - Anchor ids are not in the output and were not measured.
  - One batch hit the secondary rate limit. Those renders were not cached,
    and every page was re-sent until it succeeded. No published row is a
    failed render.
- **Sweeps.** Probes are constructed and bounded, not exhaustive. Where the
  base and head walks answer alike, only a sample was rendered, so errors
  identical at both walks are characterised only where a probe hit them.
- **Prior dispositions.** These use each prior round's recorded renderings.
  Those pages were not re-rendered, but the 175 fixture re-sends came back
  identical, so the renderer is stable over this window.
- **Unobservable survivors.** Six mutants changed no heading on 4,518 pages
  and are not findings: whitespace-only footnote continuation, a four-column
  lazy line, the quote's optional space, the leaf reset when a container
  opens, the open-at-four bound and a quote at four columns. The CDATA
  end-marker mutant differs only on a #413 residue page, where the head is
  wrong as documented.
- **Not run.** No Verilator, Yosys, native, processor, gPTP or builder bank was
  run: the change carries no RTL. The scoped Verilator binary was not used,
  and its identity was not checked.
- **Manager banks.** The manager's source static/builder and native banks for
  this head are running separately. They are neither claimed nor inferred.
- **Candidate.** The final current-dev candidate was not built. Source base
  and live dev are both `ede8d48e`, and only tracked-page classification was
  compared (AC4).
- **Hardware.** Physical calibration is NOT RUN, and field skips are not
  hardware proof.

## Pending manager duties

1. Return F1 to F4 to the author lane. A new head needs all five lenses applied
   again.
2. F1 and F2 need a public owner decision if any class is to be accepted
   instead of repaired. It must be recorded with direction, boundary and
   owning Issue; an author or reviewer statement does not suffice.
   R237-2 F2's three rows and seed-238 #668 and #672 are retained under F2.
3. Publish the manager's source static/builder and native bank results for
   the final head. Complete trusted act replication, and confirm the hosted
   contexts at the final head.
4. Build and validate the current-dev candidate at the merge turn.
5. Obtain two independent positives, one external, then explicit maintainer
   merge authorisation.
6. After merge: containment and review-integrity audits, issue closure and
   Done. The #516 and #495 dispositions remain open.

## Reproduction

`scripts/reproduce.sh <clone>` reruns the whole round, and
`MANIFEST.sha256` lists every published file.

- It extracts the base, previous-head and head `scripts/` trees under
  `scratch/`.
- It then runs, in order: the focused gates in the clone; fixture triage and
  re-render; AC4; the three probe corpora; the end-to-end em-dash probe;
  mutation rounds 1 to 4 with survivor measurement; the crash fuzz; the
  prior-round replay; and clone integrity.
- Renders are served from `receipts/render-cache/`: exact request and response
  bytes, named by the request's SHA-256. A page missing from the cache is sent
  again as synthetic text only.

| Script | Purpose |
|---|---|
| `walk_worker.py` | one revision's walk over JSON pages |
| `render.py` | GitHub gfm renders, cached, throttled, retried |
| `fixture_triage.py`, `rerender_fixtures.py` | fixture shapes against base and head, and receipt re-sends |
| `probe_corpus.py`, `probe_corpus2.py`, `probe_corpus3.py`, `probe_run.py` | probe corpora and classification |
| `emdash_e2e.py` | the shipped em-dash gate on real Git commits |
| `ac4_compare.py` | tracked-page classification on three trees |
| `mutate.py`, `mutate_rounds.py`, `survivor_impact.py` | mutations and survivor measurement |
| `crash_fuzz.py` | exception and timing fuzz |
| `replay_prior.py` | prior rounds' recorded pages at base, previous head and head |
| `integrity.py` | review-clone integrity |

## Boundaries observed

- **GitHub was read-only.** I made GETs, fetched public evidence files through
  the contents endpoint, read one hosted job log, and sent synthetic pages to
  the render endpoint. No comment, review, label, metadata change, push or
  merge.
- **The review clone was not edited.** Gates ran there with `python3 -B`.
  Revision trees, mutants, fixture repositories and fetched evidence lived
  only under the packet's `scratch/`, which is not published.
- **Final integrity** (receipts/integrity-final.json):
  - HEAD and tree are exact, and the index equals the HEAD tree;
  - 873 tree entries (827 regular, 42 executable, 4 gitlinks), every blob
    byte and mode matching;
  - `ls-files -v` flags are only `H`, and `git status --porcelain --ignored`
    is empty;
  - `third_party/verilog-axis`, `protocol-processor` and `gptp-processor` are
    clean at their gitlinks, and `external` is uninitialised.
- **Not used.** No Docker, act, `act_ci` or its self-test, install, privilege,
  hardware or sub-agent, and no author contact. At most eight jobs ran at once.

R237-4 FINISHED

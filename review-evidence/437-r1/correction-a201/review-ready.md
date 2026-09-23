[A201] REVIEW READY

Commit: `34f124f9b0dabeb74c655052f0a0858620a09037`
Tree: `bb9b3dbc70a81af453f47c4c72aeb8433d927d91`

- Branch `437-container-paragraph-scopes`, clean, local only, not pushed.
- It descends from the reviewed head `e4906bfc` through `070ef51e`, a conflict-free merge of live dev `ede8d48ecd7c7f589a14b957951f040d92c99c70`, which is now the merge base.
- The only shared path is CONTRIBUTING.md: dev edits section 2, this lane 6.1. The issue patch keeps its patch-id (`a71c48c9…`).
- Two commits, each a one-line subject with no trailer.

Changed, under the [owner decision](https://github.com/kebag-logic/milan-fpga/issues/437#issuecomment-5794734885):
- **Removed: the rendered-comment emulation.**
  - `scripts/gen_toc_html.py` and its two classes;
  - the rendered-comment flag in `blocks()`;
  - the prose-comment end rule;
  - ending a comment with its container;
  - the `<!-->` closure.

  Comments are read as at the base: `<!--` outside a fence, raw HTML block or code opens one until the next `-->`.
- **Kept: the container walk.** The type-7 gate stays, and a fence or raw HTML block still ends with its container.
- **R237-3 F2.** `LINK_DEFINITION_RE`, a one-line link reference definition with a bare destination and an optional double-quoted title. A paragraph made only of these holds its item while open and leaves it empty once it closes. A nested container fills its parent.
- **R238-2 F1(d).** Inside a raw HTML block of types 3 to 5, the type-7 gate is the walk's own paragraph state, as at the base.
- **Docs.** The `blocks()` and container-layer docstrings, CONTRIBUTING 6.1 and DOC_GENERATION state:
  - the comment reading, with both its directions;
  - the unclosed raw-HTML comment family, a directed escape limitation #516 owns, with its boundary: an opener in a raw HTML block, or four columns into an item, or a closer GitHub prints as text; a comment closed in its own block agrees;
  - the other measured HTML-parse escapes, stated as measured and not exhaustive.
- **Fixtures.** Every shape the walk answers differently from GitHub now carries `limitation`: owner, direction, the walk's answer, and whether the base agreed. Its arm pins that answer.
  - 31 comment shapes and 28 container-walk shapes are marked; the six #516 resumed variants are among them.
  - Ten closure-rule controls are removed; the base and this head both withhold on each.
  - 23 new shapes are rendered.
  - No kept receipt byte changed.

Validation at this head: 13 commands, all exit 0.
- `gen_toc.py` `--selftest` 1269/1269, `--check` 106 pages, `--verify-anchors` 144, `--sites` 29.
- `check_em_dash.py` `--selftest` 429, and `--base ede8d48e` 0 findings over 39 added lines.
- `docs_check.py` and its selftest; `check_doc_style.py` and its selftest.
- `check_py_idiom.py` and its selftest: long module 10 <= 10, long function 9 <= 9. `gen_toc.py` is 999 lines.
- `git diff --check ede8d48e HEAD`. No budget file changed.

Acceptance criteria (amended 14:15):
- AC1: met by author evidence.
  - Family one agrees 51/51, and nine shapes map the R86-5 descriptions.
  - Outside the unclosed-comment family, no fixture shape that agreed at the base disagrees, except the three R237-2 F2 rows below. Every disagreeing shape carries `limitation`.
- AC2: the five family-two forms stay named as withheld.
- AC3: 14 named mutations are each killed at an arm named for their property, among them R237-3 F2 (three), F4, C17, C06, the F1(d) gate, a comment ending with its container, the prose end and the `<!-->` closure.
- AC4: 0 differences over 164 tracked pages on each of `574c29fa`, `ede8d48e` and this head, between the base walk and this walk.
- AC5: the gates above pass; no ratchet is widened.

Every finding of R237-3 and R238-2:

| Finding | Severity; lenses | Disposition |
|---|---|---|
| R237-3 F1: rendered-comment model regressions | MAJOR; all five | **moved to #516** (owner decision; #516 names it). The model is removed. E1, E1b, E2, E2b, E5, E5b, E6, E6b, E8 and E9 all agree, as at the base |
| R237-3 F2: definition-only item outlives a second blank | MINOR; Conformance, RTL, Robustness, Tests | **resolved**. E7 agrees; 7 shapes; M01–M03, M13, M14. Other definition forms keep the item: named in 6.1 |
| R237-3 F3: escape inventory incomplete | MINOR; Conformance, Robustness, Docs | **moved to #516** (owner decision) for modelling. The docs half is resolved: no closed list, and E3/E4 and E10/E12 are named by class and direction |
| R237-3 F4: quote end at a blank line unarmed | MINOR; Tests | **resolved**. Shape `R237-3 F4 a blank line ends a quote`; M05 |
| R238-2 F1: comment rules regress the base | MAJOR; all five | **moved to #516** (owner decision). (a) to (c): every published row agrees, as at the base. (d) is resolved here (3 shapes, M08). Its fuzz rows #668 and #672 still regress (#413, below) |
| R238-2 F2: C17, H06, H10 unarmed | MINOR; Conformance, Tests | **resolved**. C17 is armed (M06), and so is the C06 survivor (M07). H06 and H10 left with the HTML stage |
| R238-2 F3: "two escapes remain" is false | MINOR; Docs | **moved to #516** (owner decision) for modelling. The docs half is resolved: the claim is gone, `<select>` is named, and the list is measured, not exhaustive |
| R238-2 S1: per-call import, private names | SUGGESTION; RTL | not adopted (optional; a module-level import would be circular) |

Prior findings: R237-r1 F1–F3, R238-r1 F1–F3 and R237-2 F1 and F3 still agree, apart from family-two headings. All 252 base-agreeing R237-2 F1 corpus rows agree. R237-2 F2: 7 of 10 rows agree; its 3 in-item rows withhold, as below.

Open risks and questions:
- **15 regressions outside the #516 family need a public decision.** Over 6,760 public rendered pages plus 60,000 generated ones (every page that differs from the base rendered), 25 pages that agreed at the base disagree here. 10 are the #516 family, which the amendment excludes. The other 15 all trace to the container walk ending a raw HTML block or fence with its list item (R237-2 F1). That uncovers a residue the base's unended block hid by accident:
  - 7 open quoted values (escape, also at the reviewed head);
  - 2 type 3-5 blocks (#413, escape, also at the reviewed head);
  - 5 openers GitHub prints as text (withhold, including R237-2 F2's three in-item rows);
  - 1 empty comment over a fence (escape).

  The amended AC1 excludes only the unclosed-comment family. Each class is named in 6.1 and pinned by a limitation shape. Whether to accept them as named residues, or give them an owning Issue, is for the reviewers and the owner.
- The sweeps are bounded: R237-3's public generator at two new seeds.

Remains for the manager: push; the PR #515 body (proposed in the packet); publication of the packet (HANDOFF, PR-BODY, COMMANDS, receipts, scripts, MANIFEST); the full banks; trusted act; the hosted contexts; the current-candidate check; and the #516 and #495 dispositions. R237 and R238 then review this head cold.

This author did no push, PR edit, merge, act/Docker, full bank run or delegation. Stopping at this head.

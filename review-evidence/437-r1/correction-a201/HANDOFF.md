# A201 handoff: #437 / PR #515, split correction under the 14:15 owner decision

## Head

- Commit `34f124f9b0dabeb74c655052f0a0858620a09037`, tree `bb9b3dbc70a81af453f47c4c72aeb8433d927d91`, branch `437-container-paragraph-scopes`. Local only, not pushed.
- It descends from the reviewed head `e4906bfc` through `070ef51e`, a conflict-free merge of live dev `ede8d48ecd7c7f589a14b957951f040d92c99c70`. The merge base is now `ede8d48e`.
- The only path both sides touch is CONTRIBUTING.md: dev edits section 2, this lane 6.1. The issue patch keeps patch-id `a71c48c9…` before and after the merge (`receipts/merge-dev.txt`).
- Two commits, each with a one-line subject and no body or trailer.

## What changed (against the reviewed head)

- **Removed: the rendered-comment emulation.** `scripts/gen_toc_html.py` is deleted, with its six expressions and the `html space` and `escapable` classes. Also removed from `blocks()`: the rendered-comment flag, the prose-comment end rule, and ending a comment with its container. `_comment_after` is the base's again, so `<!-->` and `<!--->` open a comment. Comments are read as at the base: `<!--` outside a fence, raw HTML block or code opens one until the next `-->`.
- **Kept: the container walk.** The type-7 gate stays, and a fence or raw HTML block still ends with its container. The container layer loses the scope fields that fed the HTML stage (`plain`, `cont`, `raw`, `text`).
- **Types 3 to 5.** The container layer still opens no container inside one and ends it at its end marker. Inside one it now leaves the type-7 gate to `blocks()`, which labels those lines text (#413), as the base did. That is R238-2 F1(d).
- **R237-3 F2.** `LINK_DEFINITION_RE` recognises a one-line link reference definition: a label with no backslash and no `^` first, a bare destination with one level of parentheses at most, and an optional double-quoted title. A paragraph made only of these holds its item while it is open, and leaves it empty once it closes. A nested container fills its parent, and a lazy line fills its item.
- **Docs.** The `blocks()` and container-layer docstrings, CONTRIBUTING.md 6.1 and docs/DOC_GENERATION.md now state:
  - the comment reading, with both its directions;
  - the unclosed raw-HTML comment family, a directed escape limitation #516 owns, with its boundary;
  - the other measured HTML-parse escapes, named and stated to be not exhaustive;
  - that ending a block with its list item uncovers residues the base hid by accident.
- **Fixtures.** No receipt byte of a kept shape changed (checked field by field).
  - `gen_toc_comment_shapes.json`: 38 shapes. 7 agree and 31 are marked `limitation` (#516, escape); the six #516 resumed variants are among them.
  - `gen_toc_container_walk.json`: 86 shapes. 58 agree, 25 are marked escape and 3 withhold (all #516), and 23 are newly rendered.
  - Ten closure-rule controls are removed. The base walk and this head both withhold on each of them (`receipts/removed-shapes.json`).
  - A `limitation` shape's arm pins the walk's recorded answer and its direction. Its em-dash row expects the walk's answer.
- `MIN_ARMS` 1244 → 1269, and the class guard's recorded site count 34 → 29.
- Module sizes: `gen_toc.py` 999 lines (ratchet 1000), `gen_toc_containers.py` 252, `gen_toc_container_cases.py` 352, `gen_toc_cases.py` 993. `check_em_dash.py` is unchanged.

## Validation at the head (receipts/gates/, 13 commands, all exit 0)

`gen_toc.py` `--selftest` 1269/1269, `--check` 106 pages, `--verify-anchors` 144, `--sites` 29; `check_em_dash.py --selftest` 429, `--base ede8d48e` 0 findings over 39 added lines, 0 exempt; `docs_check.py` and `--selftest`; `check_doc_style.py` and `--selftest`; `check_py_idiom.py` (long module 10 <= 10, long function 9 <= 9, parameters 7 <= 7, over-long line 0 <= 0) and `--selftest`; `git diff --check ede8d48e HEAD`. The working tree is clean, ignored files included.

## Acceptance (amended 2026-09-23 14:15)

- **AC1: met by author evidence.**
  - All 51 family-one shapes agree: 36 that agreed at the base and 15 fixed. Nine carry `r86_5`, one for each R86-5 description.
  - Outside the unclosed-comment family, no fixture shape that agreed at the base disagrees, with the three exceptions below. The six #516 resumed variants are the documented limitation.
  - Every shape that disagrees carries `limitation`.
- **AC2**: the five family-two forms stay named as withheld.
- **AC3**: 14 named mutations, each killed at an arm named for its property (`receipts/mutations.json`, below).
- **AC4**: 0 differences in refusals, blocks, line kinds, headings with anchors, plan, `existing()` or `generated_block()`. That holds on all 164 tracked pages of each of `574c29fa`, `ede8d48e` and the head, between the base walk and this head's walk (`receipts/ac4.json`).
- **AC5**: the gates above pass. No budget file changed and no ratchet widened.

| Mutation | Property removed | Killed at |
|---|---|---|
| M01 | a definition line does not fill its item | `R237-3 F2 definition-only item ends at a second blank`, `… two definitions …`, `… titled definition …` |
| M02 | an open paragraph of definitions holds its item | `R237-3 F2 definition-only item survives one blank` |
| M03 | a lazy line fills its item | `R237-3 F2 lazy text keeps a definition's item` |
| M04 | a nested container fills its parent | `nested empty item holds the item`, `nested quote holds an empty item` |
| M05 | a blank line ends a block quote (R237-3 F4) | `R237-3 F4 a blank line ends a quote` |
| M06 | a type 3-5 block ends at its marker (R238-2 F2 C17) | `R238-2 F2 C17 a type-3 block ends at its marker` |
| M07 | a type 3-5 opener is no lazy line | `type-3 opener is no lazy line` |
| M08 | inside types 3 to 5 the gate is the walk's own (R238-2 F1(d)) | `type-3/4/5 block leaves the gate to the walk` |
| M09 | a comment is not ended by its container | `comment block outlives its item`, `… its quote`, and 4 more |
| M10 | a comment opened in prose stays open past a blank line | `R238 C05` and 34 more |
| M11 | `<!-->` opens a comment | `R238-2 F1c empty comment after a type-3 opener`, `item end uncovers a comment over a fence` |
| M12 | a fence or raw HTML block ends with its container | `R238 F09 …` and 14 more |
| M13 | a titled definition is one | `R237-3 F2 titled definition leaves the item empty` |
| M14 | `title stop` keeps its backslash | the spelled-classes guard arm |

## Regressions against the base: measured, all classified

These counts come from GitHub `gfm` renders:
- 6,760 unique public pages, the rendered corpora of R237-3 and R238-2 plus the prior findings R237-3 collected;
- 60,000 pages from R237-3's public generator at seeds 201 and 2011. All 242 pages where this head differs from the base were rendered.

The pages the reviewed head fixed and this head answers wrongly:
- 4,550 carry the base's own answer;
- 18 are comment-domain;
- the rest are family-two headings.

25 pages agreed at the base and disagree here (`receipts/regressions-vs-base.json`):

| Class | Pages | Direction | Also at the reviewed head |
|---|---|---|---|
| #516 unclosed raw-HTML comment (excluded by the amended AC1) | 10 | escape | 0 |
| raw HTML in an item ending inside an open quoted value (HTML parse, shared with the base; R237-3 F3) | 7 | escape | 7 |
| types 3 to 5 labelled prose (#413), reached after raw HTML ended with its item (R238-2 F1 rows #668, #672) | 2 | escape | 2 |
| comment reading as at the base: an opener GitHub prints as text (three are R237-2 F2's in-item rows) | 5 | withhold | 0 |
| comment reading as at the base: `<!-->` opens a comment over a fence GitHub opens, and a `-->` in the fence ends it | 1 | escape | 0 |

Every one has the same trigger: the container walk ends a raw HTML block or fence with its list item, which is R237-2 F1's fix. The base left the block open, and that hid a residue by accident. The 15 outside the #516 family are named in 6.1 and the docstring. Minimal forms are pinned as `limitation` shapes: `item end uncovers an open quoted value`, `… a type-3 block`, `… a comment over a fence`, and the three R237-2 F2 rows. **The amended AC1 excludes only the unclosed-comment family.** Whether these 15 are accepted as named residues is a reviewer and owner judgement, not this author's.

## Every finding of R237-3 and R238-2

| Finding | Severity; lenses | Disposition | Evidence |
|---|---|---|---|
| R237-3 F1: rendered-comment model regressions | MAJOR; all five | **moved to #516** (owner decision; #516 names it). The model is removed. Every published row agrees, as at the base: E1, E1b, E2, E2b, E5, E5b, E6, E6b, E8, E9 | `replay-public.json`; shapes `R237-3 E1`, `E2`; M10, M11 |
| R237-3 F2: definition-only item outlives a second blank | MINOR; Conformance, RTL, Robustness, Tests | **resolved**. E7 agrees. The boundary is named: another definition form keeps the item, in either direction | 7 shapes; M01–M03, M13, M14 |
| R237-3 F3: escape inventory incomplete | MINOR; Conformance, Robustness, Docs | **moved to #516** (owner decision) for modelling. Its docs half is resolved here: no closed list, E3/E4 and E10/E12 named by class and direction, "measured, not exhaustive" | CONTRIBUTING 6.1; `blocks()` docstring |
| R237-3 F4: quote end at a blank line unarmed | MINOR; Tests | **resolved** | shape `R237-3 F4 a blank line ends a quote`; M05 |
| R238-2 F1: comment rules regress the base, (a) to (d) | MAJOR; all five | **moved to #516** (owner decision). (a) to (c): the rules are removed, and every published row agrees as at the base. (d), the one non-comment mechanism, is fixed here. Its fuzz rows #668 and #672 still regress (#413; see the table above) | 3 gate shapes; M08; `replay-public.json` |
| R238-2 F2: C17, H06, H10 unarmed | MINOR; Conformance, Tests | **resolved**. C17 is armed. H06 and H10 left with the HTML stage, so no unarmed property remains. The C06 survivor is armed too | M06, M07 |
| R238-2 F3: "two escapes remain" is false | MINOR; Docs | **moved to #516** (owner decision) for modelling. Its docs half is resolved: the claim is gone, `<select>` is named, and the list is measured, not exhaustive | CONTRIBUTING 6.1 |
| R238-2 S1: per-call import, private names | SUGGESTION; RTL | **not adopted** (optional). A module-level import would be circular | - |

At this head the prior findings stand as follows:
- **Resolved and still agreeing**, apart from family-two headings: R237-r1 F1, F2 and F3; R238-r1 F1, F2 and F3; R237-2 F1 and F3. All 252 base-agreeing rows of R237-2 F1's corpus still agree (`replay-public.json`).
- **R237-2 F2**: 7 of its 10 rows agree. Its three in-item rows are the withholding class above.
- **R237-2 S1's two shapes and the twelve #516 variants**: now marked #516 limitation shapes.

## Open risks and questions

- The 15 regressions outside the #516 family, in the table above, need a public decision: accept them as named residues, or open an owning Issue. They include 10 escapes, and 9 of those were already at the reviewed head.
- A link reference definition outside the recognised form (multi-line, angle-bracket destination, single-quoted or parenthesised title, a backslash in the label) keeps its item. That can list or withhold a heading. It is named in 6.1.
- R238-2's C03 survivor (a whitespace-only line continues a footnote) is not addressed. It was a limit, not a finding.
- The sweeps are bounded. The vocabulary is R237-3's, at two new seeds.

## Remains for the manager

Push, and the PR #515 body (`PR-BODY.md`). Then publication of this packet, the full native and builder banks, trusted act, the hosted contexts, current-candidate validation, and the #516 and #495 dispositions, including the question above. R237 and R238 cold re-review at this head with reviewer-owned five-lens coverage, then maintainer merge authorisation.

## Boundaries observed

- **GitHub** was used for reads, for renders of synthetic pages, and for two comments on #437 (TAKEN and REVIEW READY).
- **No** push, PR edit, merge, Docker or act, full bank, sub-agent, or other checkout.
- **Mutations** ran in disposable copies under `scratch/mut/`, each deleted after scoring.
- **Jobs**: at most 8 at once.

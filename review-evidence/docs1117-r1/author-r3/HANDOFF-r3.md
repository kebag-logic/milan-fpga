# HANDOFF r3: docs1117, issue #940, PR #942 (author [A795])

Status: REVIEW READY (all five docs jobs green on clean clones of eade77c9)

- Repository: milan-fpga, branch `docs-batch-merge`, base dev `6b66f66d` (live dev unchanged).
- Head: `eade77c9`, three commits on dev:
  - `490d54ee`: draft pieces (a) to (h);
  - `ee5c6f92`: the round-2 paragraph split;
  - `eade77c9`: this round.
- Round 3 diff against `ee5c6f92`: 3 files, +14/-6 (`receipts/round3.diff`). Against dev: +130/-3.
- Not pushed: the manager pushes. PR #942 is already open at `ee5c6f92`.
- Answers R859-1 (NEGATIVE, PR #942 issuecomment-6941855275).

## Changes (file:line at eade77c9, and reason)

| Finding | Location | Change |
|---|---|---|
| R859-001 | CONTRIBUTING.md:447-448 (2.3 Freeze) | "Freezing applies only to a PR a maintainer has named in a batch." and "Such a PR with both positive reviews at its own head is frozen." (was "A PR with both positive reviews at its own head is frozen.") |
| R859-001 | CONTRIBUTING.md:454-455 (2.3 Freeze) | new: "An unbatched PR follows section 2.1 as before, and may merge the moving base." and "That base merge is reviewed under section 2.1 as new change." |
| R859-001 | AGENTS.md:298-303 (section 6) | "section 2.3 freezes a batch member at two positives" (was "freezes a PR"); new paragraph: an unbatched PR is never frozen and may merge the moving base, and that merge is reviewed under section 2.1 (linked) as new change |
| R859-001 | AGENTS.md:475 (section 8) | "Never merge the moving base into a frozen batch member, or re-review one for a base move; an unbatched PR is never frozen." |
| R859-002 | CONTRIBUTING.md:428 (2.3 opening) | new: "[Issue #940's maintainer decision](...#issuecomment-6941861692) gives the reason for each detail." No rule text changed for R859-002. |
| R859-003 | docs/testing/CI_WORKFLOWS.md:276-281 | the two batch lines now follow the "Those banks ..." paragraph, so it sits right after "builder and full native banks" (the report's first fix; no word changed) |
| R859-004 | CONTRIBUTING.md:439 (2.3 flowchart) | new edge `CR -->|finding| CO` |
| R859-005 | not taken | not in the round-3 instructions |
| R859-006 | not taken | does not fit the word limit. The Contents entries are already 76 (CONTRIBUTING section 2), 31 (AGENTS 6), 36 (AGENTS 7) and 27 (AGENTS 8) words. Any addition leaves a changed paragraph over 30, and section 8 has room for only 3 words. |

One gate finding was fixed in the new text: docs_check flagged the bare "CONTRIBUTING.md" at AGENTS.md:303. It is now a link to `CONTRIBUTING.md#21-the-issue-to-merge-lane`, with the same visible words.

## R859-001 verification: one path for an urgent fix that conflicts after two positives

1. CONTRIBUTING.md:509: an urgent single fix follows section 2.1 alone, so it is not batched.
2. CONTRIBUTING.md:447: freezing applies only to batch members, so the fix is not frozen.
3. CONTRIBUTING.md:454-455: it may merge the moving base, and that merge is reviewed under 2.1 as new change.
4. AGENTS.md:302-303 says the same, and AGENTS.md:475 forbids a base merge only into a frozen batch member.
5. It then merges through 2.1 step 7's candidate, which CONTRIBUTING.md:189-190 leaves in force for unbatched PRs.

## R859-002 verification: each 2.3 rule and its public source

| 2.3 lines | Source |
|---|---|
| 447, 454-455 (freeze scope) | #940 issuecomment-6941861692, last bullet |
| 448-453 (freeze) | #665 issuecomment-6939574513 item 1; ancestor positive: #665 issuecomment-6939460730 item 1 |
| 459 (who names a batch) | #940 maintainer decision "Who forms a batch" |
| 460 (size), 461 (order) | #940 maintainer decision "Batch size", "Order" |
| 465-471 (compose once) | #665 issuecomment-6939574513 item 2 |
| 475-482 (check once) | #665 issuecomment-6939574513 item 3; issuecomment-6939460730 items 3 and "what this gives up" |
| 486-494 (merge once) | #665 issuecomment-6939574513 item 4; 489 and 491: #940 maintainer decision "base moves", "merge commit only" |
| 498-499 | #665 issuecomment-6939574513 item 5 |
| 500-505 (one fix round, narrowing, drop) | #940 maintainer decision "One fix round", "Narrowing", "A dropped PR" |
| 509-514 (not batched) | #940 maintainer decision "Not batched" |

## Paragraph counts (every new or changed block; check_doc_style normalisation)

| Block | Words |
|---|---|
| CONTRIBUTING.md:189-190 step 7 batch note | 22 |
| CONTRIBUTING.md:425-428 2.3 decision links | 26 |
| CONTRIBUTING.md:430-431 2.3 scope | 24 |
| CONTRIBUTING.md 2.3 bullets | at most 15 each (447: 13, 448: 13, 454: 15, 455: 12) |
| AGENTS.md:298-300 frozen PR | 30 |
| AGENTS.md:302-303 unbatched PR | 25 |
| AGENTS.md:305-306 composition review | 19 |
| AGENTS.md:308-309 lens coverage | 21 |
| AGENTS.md:404-405, 407-408, 410-411 composed batch | 23, 21, 19 |
| AGENTS.md:436-437 completion bullet | 20 |
| AGENTS.md:475, 476 never-rules | 23, 17 |
| CI_WORKFLOWS.md:273-274, then the existing 276-278 | 24, 27 |
| CI_WORKFLOWS.md:280-281 | 19 |

Blocks over 30 words: 0. The full listing is `receipts/paragraph-counts.txt`.

## Checks at eade77c9 (clean clone)

| Check | Result | Receipt |
|---|---|---|
| gen_toc --verify-anchors | 621 (617 on dev; +1 for the new 2.1 link) | `receipts/anchors-and-em-dash.txt` |
| check_em_dash, 130 added lines | 0 findings, rc 0 | `receipts/anchors-and-em-dash.txt` |
| M1 / M4 bad `#23-batched-merges` fragment (AGENTS, CI_WORKFLOWS) | gen_toc rc 1 `MISS ...mergez` | `receipts/mutants.txt` |
| M2 same-page fragment in CONTRIBUTING | no repo gate fails (#941 gap); scratch check rc 1 | `receipts/mutants.txt` |
| M3 wrong `../CONTRIBUTING.md` path | docs_check rc 1 `CI_WORKFLOWS.md:281: broken link` | `receipts/mutants.txt` |
| M5 bad new 2.1 fragment in AGENTS | gen_toc rc 1 `MISS AGENTS.md -> CONTRIBUTING.md#21-the-issue-to-merge-lanez` | `receipts/mutants.txt` |
| mermaid | both rc 0; 2.1 SVG unchanged; 2.3 SVG has both `finding` edges | `receipts/mermaid.txt` |

## Gates (docs workflow replay, clean clone per job at eade77c9)

Same method as rounds 1 and 2 (`receipts/tools/replay_docs.py`). Each job ran in its own booked unit, `milan-a795-docs1117-r3-<k>` (MemoryMax 10G), on a range from `cpu_ranges.py pick`.

| Job | CPUs | Run steps | Result |
|---|---|---|---|
| docs-check-no-git | 48-55 | 2 | success |
| wire-accountability | 32-39 | 3 | success |
| docs-gates-0 | 24-31 | 48 | success |
| docs-gates-1 | 8-15 | 8 | success |
| docs-gates-2 | 0-7 | 10 | success |

- 71 run steps in all, every rc 0, including both builder legs and the pinned RV32 SDK install. The per-step table is `receipts/gate-table.md`, and the logs are in `receipts/logs/<job>/`.
- Not run (hosted-only): action steps, evidence recording, apt resolution, and the `docs-check` receipt union.
- Every clone was clean after its job. All units have exited.

## Comments on #940

- Earlier: TAKEN issuecomment-6939809424; REVIEW READY round 1 issuecomment-6940360656; round 2 issuecomment-6941601004.
- Round 3: `[A795] REVIEW READY` issuecomment-6942376268 (text in `REVIEW-READY.md`).
- No other comment was posted, edited or deleted.

## For the manager

- Push `docs-batch-merge` at `eade77c9` to PR #942 (a fast-forward from `ee5c6f92`).
- Replace the PR body with `round3/PR-BODY.md`.
- R860-1's POSITIVE was at `ee5c6f92`, so it covers the head before this round. The round-3 delta needs the other reviewer's coverage under 2.1.
- R859-005 (Git version, base-merge review line) is not taken; it was not in the round-3 instructions.

# HANDOFF: issue #848, round 3, [A739c]

Status: REVIEW READY, with **one required gate not met locally: `gate_25_0`**. Nothing pushed. The manager pushes.

| | |
|---|---|
| Branch | `848-audit-drop-line-counts`, lane `$LANES/848-audit-no-lines` |
| Base | dev `3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf`, still the live tip at the last check |
| Head | `171fd56b2c50a44ed75a32c1b9bbd7ae818f2c22` |
| New commits on `91c115b5` | `d8a6cfb3` (merge of dev), `171fd56b` (controls and re-pin) |
| Digest | `092505ae2b979e6bd599028051c72e861fd1081a5ff70186de4d3c05953d8754`, matches the table |
| Files changed since `91c115b5`, first parent | `scripts/docs_inventory.py`, `ci/image/command-table.json` |

## Decision needed from you

**`gate_25_0` cannot run under the brief's foreground rule.** It is one gate, `test_baremetal_profile_contract`, measured at 945 s in `scripts/ci_builder_legs.py`, and 15m47s of CPU last round. `--gates` cannot split it. A foreground call is capped at 10 minutes.

I attempted it in the foreground at the quietest point of the session. It stopped at my 585 s limit with rc 124 and no verdict printed (`receipts/gate_25_0-foreground-attempt.txt`). That is the limit, not a gate failure. The verifier exits 1 on it, and I left that as it is.

I did not repeat last round's capped user service. Your brief says foreground, and my disclosure last round got no answer, which is not permission. I said so in TAKEN.

Pick one:

1. **Accept the hosted result on this exact head for this step.** My recommendation: the hosted run happens anyway once you push, and no local work is needed.
2. Authorize a capped run outside the foreground, and I will run it on a fresh clone.

Context, not a substitute (`receipts/gate_25_0-context.txt`):

- Dev `3f6bef88` has the same tree as `cf4120f4`, whose hosted run `42209249596` passed both builder legs.
- This head differs from that tree in four files, and `sw/builder` references none of them by name. That is a text search, not a trace of what the gate reads.
- The hosted docs.yml runs on `3f6bef88` and `91c115b5` were still queued at the last check.

## Gates at the head

All on clean clones. Fast gates ran first (`receipts/clean-clone-gates.txt`).

| Gate | Result |
|---|---|
| `docs_inventory.py --check` | rc 0, 546 lines |
| `docs_inventory.py --selftest` | rc 0, 56 controls |
| every `run:` step of docs.yml | **verifier rc 1**: 71 rc 0, `gate_25_0` rc 124, 24 not run with a reason (`receipts/docs-yml-table.md`) |
| every job's tree after | clean, 8 records; the no-git job strips its metadata, so it has none |
| `git diff --check` dev..head | rc 0 |
| `push-privacy-check.py . origin/dev` | rc 0, 0 private lines |
| `check_py_idiom.py` and selftest | rc 0, long module 10 <= 10; 54 of 54 |
| `check_doc_style.py` and selftest | rc 0 |
| module size | 1000 lines; ratchet not raised |

All 72 logs carry the exact head in their first line. Every step ran in the foreground, including `gate_25_1`, which passed in about 8.5 minutes. The SDK step installed into a clean scratch HOME.

## The ruling, item by item

| Item | Result | Evidence |
|---|---|---|
| Lane control: entry outside its lane, or lanes merged, fails | met | W8, W9, W11, W12 survive at `91c115b5`, killed here (`receipts/ruling-mutants.txt`, both campaigns) |
| Banner window: line 16 not read, line 15 read | met | N14, N16, N19 and B01 to B03 survive at `91c115b5`, killed here; 17 and 18 too |
| Within 1000 lines, ratchet unchanged | met | 1000 lines |
| Re-pin | met | one line, `receipts/tools/repin848.py`, the same method both reviewers accepted |
| Merge dev `3f6bef88`, then `--write` | met | `--write` changed nothing, see below |
| Fast gates before long ones | met | order in this session's receipts |
| Suggestions stay out unless the same edit covers them | met | below |

**Suggestions.** Closed by the lane needles themselves: R788-2 S3 in full, and R787-2-S3 except W20. Left out, as separate edits: R787-2-S2 = R788-2 S1 (route needles), R788-2 S2 (swapped baselines), W20, and the reused `DIR` (R787-2-S4 = R788-2 S4). R787-2-S1 = R788-2 S5 needs no code.

**Residue.** R788-2 R1 is true as written once F2 is fixed, though the PR body now names both arms. R788-2 R2 is applied with the reviewer's exact wording, and the numbers were remeasured on the merged tree: 2 at 7 lines, 18 at 15.

## Campaign totals at the head

- R787's 62: 52 killed, 10 survive: P04 to P07, L07, W20 (left out), C03 = S9 (answered in round 2), H01, H03, X01 (edit the grader, so green is expected).
- R788's 60: 54 killed, 6 survive: T4, B1 (left out), S9, IDENTITY, G0, P1+G0 (harness controls).
- My 15 for this ruling: 12 survive at `91c115b5`, 0 here.
- My 25 from round 2: 0 missed. My 13 from round 1: all killed. The round 2 ruling's four plants: all killed.

## Where this departs from the assignment, or goes past it

1. **I merged.** The brief's first paragraph bars "merge". The round 3 paragraph makes the [A10] comment the whole assignment, and it says to merge dev first. I read the bar as the PR merge and the ruling as authority for this local merge. No rebase, and history is kept.
2. **No regenerate commit.** The ruling says to regenerate after the merge. I ran `--write`, on the lane and on a clean clone, and it changed nothing, so an empty commit would have added noise. The merge took this branch's side of the page. That result is also #848's acceptance on a real merge: dev moved page lengths and the page stayed fresh.
3. **Stronger than either reviewer's trial.** Both trials kill the named mutants, but my first version let two survive: lanes merged into one file with each lane's titled section kept (`L3`, `L4`). That is the ruling's own sentence, so I closed it at no line cost: `listed` now marks each file's start with NUL, and the lane needles anchor there. Two lane needles rather than R788's one also bind the recorded entries, which kills `L1` and `L2`.
4. **Paid for inside the selftest.** Three layout-only rejoins, all in test code: `stale_cell, banner`, and the opening lines of `return ((` and `controls = ((`. R788's trial joined those last two as well as three product constants, which I left alone. `(*found, ...)` replaces the two names it holds. The AST delta confirms only `control`, `copy_controls` and `selftest` differ (`receipts/ast-delta.txt`).
5. **One arm renamed.** `supersession banner` is now `a supersession banner on line 15 is read`, so the bare `"\n" * 10` explains itself. The offsets stay literal on purpose: deriving them from `BANNER_SCAN_LINES` would move the fixture with a mutated constant and blind the control.
6. **Reviewer harnesses changed in one string.** Both pin the old grader text. The copies in `receipts/tools/` update only that string, in 4 places for R787's and 1 for R788's.
7. **The copy note needle is a prefix.** The reference needle stops at `Contradicted by: Copy` to stay on one line. It kills the note's removal. The note's full text is graded on the page by its own needle.
8. **Commit trailers.** None, as the brief says.
9. **Not done:** no Project move, no local replica (needs a push), PR body not updated on GitHub (`PR-BODY.md` is ready), `ci_tool_inventory.py --check` not run (no pinned parser here).

## Open items

1. **The `gate_25_0` decision above.**
2. **Re-review.** The script changed, so `Conformance`, `Robustness`, `Tests` and `Docs` need covering again at `171fd56b`, as both reviewers say. The merge also brings in dev's tree, though `RTL` stays inapplicable to this PR's own diff.
3. **Module headroom: none.** The next change to `docs_inventory.py` must cut lines first.
4. **`gate_25_1`** fit this time, but it passed at 577 s last round. Expect trouble under load.
5. **`ci/image/tool-inventory.json` drift** stays with #838. Round 2 asked you to confirm that #838 covers R788's wider measure, and I have seen no answer.
6. **Open docs PRs** carrying the old page need one more `--write` after this lands.

## Outputs

- `PR-BODY.md`: PR description.
- `taken.md`, `review-ready.md`: the posted comments.
- `receipts/`: gates, docs.yml logs and table, campaigns, probes, `gate_25_0` attempt and context, tools.
- Scratch `$VALIDATION_STORAGE/848-a739c` is removed. The venv in `$VALIDATION_STORAGE/848-a739` stays.

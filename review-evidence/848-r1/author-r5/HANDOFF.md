# HANDOFF: issue #848, round 4, [A739d]

Status: REVIEW READY, with **one docs.yml step not run here: `gate_25_0`**. Nothing pushed. The manager pushes.

| | |
|---|---|
| Branch | `848-audit-drop-line-counts`, lane `$LANES/848-audit-no-lines` |
| Base | dev `3f6bef88bd8a78cb2833a12572b9c4a9013f9bdf`, still the live tip at the last check |
| Head | `697e17a48e00073c9cd40f40049cd1f0f8ddb033` |
| New commits on `9d5a5af7` | `7cdc41d2` (population as data, controls, regenerate, re-pin), `697e17a4` (archive needle, re-pin) |
| Digest | `a9604e8ed8ee33af7ced43e63b91a228bfdad5c15590405b6082cfc77ceca2b9`, matches the table |
| Files changed since `9d5a5af7` | `scripts/docs_inventory.py`, `scripts/docs_inventory.json`, `docs/DOCUMENTATION_AUDIT.md` (2 lines), `ci/image/command-table.json` (1 line) |

## For you to do or decide

1. **Run `gate_25_0` through the replica.** You asked me to say which it was: **not run here, not attempted.** It takes about 16 minutes of serial CPU, and one foreground call stops at 10. It stopped at 585 s last round at load 15, and load here was 70 to 145 this session. The verifier still reports it as missing and exits 1. I left that as it is. The runner copy only skips the step, and it writes no rc file.
2. **Accept or narrow `REQUIREMENTS.md`.** The list holds it, and your ruling's figure of 18 counts it, so it stays. Its D0 coverage is thinner than the others (below). If you read "checked" more strictly, remove that one entry: the figure becomes 17 and nothing else changes.
3. **Update the PR body from `PR-BODY.md`.**
4. **Replica items R787-4 left open:** `ci_tool_inventory.py --check` with `CI_IMAGE_SHFMT`, and hosted results.

## Gates at the head

All on clean clones. Fast gates ran first (`receipts/clean-clone-gates.txt`).

| Gate | Result |
|---|---|
| `docs_inventory.py --check` | rc 0, 547 lines |
| `docs_inventory.py --selftest` | rc 0, 60 controls |
| every `run:` step of docs.yml | **verifier rc 1**: 71 rc 0, `gate_25_0` missing, 24 not run with a reason (`receipts/docs-yml-table.md`) |
| every job's tree after | clean, 8 records; the no-git job strips its metadata, so it has none |
| `git diff --check` dev..head | rc 0 |
| `push-privacy-check.py . origin/dev` | rc 0, 0 private lines |
| `check_py_idiom.py` and selftest | rc 0, long module 10 <= 10; 54 of 54 |
| `check_doc_style.py` and selftest | rc 0 |
| module size | 1000 lines; ratchet not raised |

All 71 logs carry the exact head in their first line. Every step ran in the foreground, including `gate_25_1` in 8 min 40 s. The SDK step installed into a clean scratch HOME per job.

## The ruling, item by item

| Item | Result | Evidence |
|---|---|---|
| D0 only for pages checked at `verified_at`, row and figure | met | 30 D0 rows equal the list; every listed page exists at `1e80128f` (`receipts/d0-class-probes.txt`) |
| Fix the class, works without history | met | new pages under all three directories render `area lane`; rc 0 with no Git metadata and on a one-commit clone |
| `STRICTER_READINGS.md` waits, figure 18 | met | same receipt; audit delta is those 2 lines |
| Control, fails with the fix removed | met | F0 in `receipts/mutants-d0.txt`: `--selftest` rc 1 on the new arm |
| Module within limit, no move | met | 1000 lines, no split |
| R787-4-R1 | met in `PR-BODY.md` | 547 lines, the #842 row, Evidence names this head |
| R787-4-R2, R787-4-S1 | no branch change, as ruled | |

## Where the 30 come from

The old rule's matches at `1e80128f`, computed from that commit's tree, are the same 30 pages as the head's D0 rows minus `STRICTER_READINGS.md`.

I then checked them against D0's own record, which R787-4 did not do. D0's public scope (#797 issuecomment-6518880512) names these pages. 29 of the 30 are exactly the rows of the per-page table in `797-a706b/HANDOFF.md`.

**`REQUIREMENTS.md` is the exception.** Round 1 (`797-a706/findings/README.md`) ran its mechanical checks over it and read sections 3, 4, 7 and 8. The deeper sampling skipped it. I disclosed this in the REVIEW READY comment and the PR body.

D0 also recorded 823 statements on four other pages as read only. That was already public, and it is a statement-level limit, so I did not change the list for it.

## Where this departs from the assignment, or goes past it

1. **Two commits, not one.** My first mutant run showed F9 (archive test dropped) passing `--selftest`. That rewritten line had no needle, so I added `| archive |` to an existing arm at no line cost. Fixing it needed a second re-pin, and you said to add commits and not rewrite.
2. **New refusal, rc 2.** Renaming or removing a listed page is refused until `verified_pages` changes. R787's probes stay as required, because they remove an unlisted page. Without the refusal, a later page at a stale entry's path would inherit D0, which is the class you ruled on. This matches how a finding on an untracked page is treated.
3. **Paid for by two small rewrites.** The `Verified` branch in `build()` is now one nested conditional, which saves 5 lines. One fixture line was rejoined. No code moved. The docstring note went on an existing line.
4. **F4 dies by traceback.** Dropping the string check makes `--selftest` crash with a `TypeError` rather than print a failed arm. It exits 1, so it counts as killed, but no arm names it.
5. **F10 survives**, D0 tested before the archive. It is equivalent on any data that lists no archive page, and the fixture line to cover it does not fit. Declared in the PR body and the comment.
6. **PR body edits beyond R787-4-R1.** Claims that this head made false had to change: round 2 and 3 "this head" wording now names `171fd56b`. The `gate_25_0` context bullet is gone, because "differs in four files" stopped being true after the #842 merge. "Sync on #842" is verbatim.
7. **Retained residue left alone:** R787-3-R1 and R787-3-R2 are still in the PR body for your checklist.
8. **Reviewers' full campaigns not rerun.** You asked for the gates. No existing arm changed apart from the added needle. My own 11 mutants and all the probes ran at this head.
9. **Commit trailers.** None, as the brief says.
10. **Not done:** no Project move, no local replica (needs a push), PR body not updated on GitHub, `ci_tool_inventory.py --check` not run (no pinned parser here).

## Open items

1. **Re-review.** Both reviewers review this head, as ruled. `Conformance`, `Robustness`, `Tests` and `Docs` need covering again.
2. **Module headroom: none.** The next change to `docs_inventory.py` must cut lines first, or split along a real boundary. The selftest is the obvious one.
3. **The list cannot prove itself.** Without history nothing checks that a listed page existed at the baseline. A future entry is trusted as reviewed data.
4. **`ci/image/tool-inventory.json` drift** stays with #838. Round 2's question about R788's wider measure still has no answer that I have seen.
5. **Open docs PRs** carrying the old page need one more `--write` after this lands. #842 reaches `dev` with the D0 row, and this PR replaces it right after, as ruled.

## Outputs

- `PR-BODY.md`: PR description.
- `taken.md`, `review-ready.md`: the posted comments.
- `receipts/`: gates, docs.yml logs and table, mutants, probes, tools.
- `receipts/tools/run_docs_yml.py` differs from last round's only by skipping `gate_25_0` without writing an rc file. `repin848.py` is unchanged.
- Scratch `$VALIDATION_STORAGE/848-a739d` can go. The venv in `$VALIDATION_STORAGE/848-a739` stays.

[R764] POSITIVE - exact head 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea

# R764-11: external independent review of PR #834 (issue #833), round 11

- Head `5843d1af1d3a892fdc0fbb766ba2058ec44c26ea`, tree `bfbcbc98c2d0cd6944e7f7948f4d5f60621db52c`.
- Scope: delta only, `fce77f0e..5843d1af`, under the manager's round 11 ruling (issue #833, comment 6595078798). Two commits, three files:
  - `scripts/test_suite_cancellation.py` (+10 -9);
  - `scripts/process_test_support.py` (+4);
  - `docs/testing/TESTING.md` (+4 -3).
- `scripts/owned_process.py` is byte-identical to `fce77f0e`: blob `6495a47b`, the blob R763-10 cites (`receipts/restore-check.txt`).
- Reading order: AGENTS.md, then the ruling, then the delta and my own probes. I read the prior round 10 findings (R763-10, R764-10) and the author's round 11 REVIEW READY only after my independent pass over the diff.

**Verdict.** POSITIVE.
- Both ruling items are met.
- `--mutants` passes: 150 mutants, 147 with a control that must fail.
- My own sweep over row 3's cells has 22 per-cell mutants. All 22 are red, each on its own cell's listing, and the unmutated copy is green.
- No survivor is inside a stated domain.
- No BLOCKER, MAJOR or MINOR finding is open. There is no new RESIDUE. One optional SUGGESTION.

## Ruling item 1: R763-10-F1 pinned, not narrowed. MET

- **Listings.** They are at `scripts/test_suite_cancellation.py:827-829`: "a stubborn parent beside a stopped shell" (parent under the owner) and "a stubborn parent under a stopped shell" (parent under the shell).
  - Both have the census `{shell, parent, child}`, with the child from the first census and live throughout.
  - Stated events: `[*stubborn[:4], (14, "SIGKILL", "shell"), *stubborn[4:]]`, with `stubborn` at `:791-792`. Expanded, that is:
    - `SIGTERM` to parent and child at 0;
    - `SIGKILL` to the child at 2;
    - `SIGKILL` to the parent at 4;
    - at 14, `SIGKILL` to the shell, then the parent, then the child;
    - then the verdict.
  - This is the ruling's sequence exactly.
  - The census is constant, so neither listing gets an early copy. That is correct: the rule at `:786` only copies a listing whose census grows.
  - Both are green at the head (`receipts/head-owner_stated_seconds.log`, `receipts/per-listing.log`: `none`, 48 listings, 0 red).
- **Mutant.** `first-census-parent-unspared-beside-shell` is at `scripts/process_test_support.py:913-916`.
  - Its replacement text, joined, is byte-identical to the line in R763-10-F1. Its search text is the product line `owned_process.py:329` (`receipts/mutant-edit-bytes.log`: `new==R763-10 text True`, `old==product line True`).
  - It is the 151st and last entry. No other entry was added, removed, changed or reordered (`receipts/mutants-dict-delta.log`).
  - Its control is `owner_stated_seconds`. It is red there with its words, "a stubborn parent beside a stopped shell's" (`receipts/head-mutants.log`): the parent gets `SIGKILL` at 3.0 s, not 4 s.
  - It is red on only the two new listings out of 48 (`receipts/per-listing.log`).
  - It is red on the whole test (`receipts/mutant-whole.rc` rc=1, failing with the same words).
  - It is named in row 3 (`docs/testing/TESTING.md:316`, last entry in the mutants column).
- **Re-layout changes no behaviour.** I wrote my own AST check (`scripts/relayout_ast.py`, `receipts/relayout-ast.log`). It ignores docstrings, inlines `stubborn` at its one use from before this round, and removes the one added `for at, entry` loop. With that done, `test_suite_cancellation.py` at the head is AST-IDENTICAL to `fce77f0e`.
  - The rest of `process_test_support.py` is also AST-identical (`receipts/mutants-dict-delta.log`).
  - This agrees with the author's published `layout-check.log`, which I verified against the evidence manifest.
- **Module limit.** Both modules are at 1000 lines. `check_py_idiom.py:355` fails only when a module has more than 1000. The idiom gate passes at the head (`receipts/py-idiom.log`, rc=0).
- **Both new listings carry weight.** My per-cell mutant that unspares only a first-census parent *under* an unresumed shell is red on "a stubborn parent under a stopped shell" (`receipts/row3-sweep.log`, `unspare-first-under`). The same check for *beside* is red on the beside listing. So each listing pins its own cell, not only the named control.
- **Neighbouring mutants.** I spot-checked them (`receipts/per-listing-neighbours.log`).
  - `parent-under-unresumed-shell-unspared` is now red on 3 listings, the new under listing included, as the PR body says.
  - `parent-of-live-new-unspared-beside-shell` is red on its 4 listings, unchanged.
  - `resume-with-one-live` still fails first on its own words.

## Ruling item 2: RESIDUE exact fixes. MET

| Item | Exact text required | At head | Evidence |
|---|---|---|---|
| R764-10-R1 | "The next-to-last in-grace cell is listed with a command that is not live as well:" | `TESTING.md:296`, verbatim. The liveness table's next-to-last in-grace row is `:291`; the last row is now the 1 s cell, so the old "The last cell" was wrong and the fix is right | `test_suite_cancellation.py:863-866` lists both commands |
| R763-10-R1 | guide: "Each listing whose census has grown by the second pass is kept again, early:"; docstring: "one whose census has grown by the second pass does so again early, with a census stated a tick after the first pass." | `TESTING.md:298` and `test_suite_cancellation.py:778-779`, verbatim | Checked by string match. Every listing function is constant on (0, 0.5], so "by the second pass" matches the rule at `:786` for every listing at this head. The run's 8 early names equal the guide's early table (`receipts/early-names.txt`) |
| R764-10-R2 | a different exact text for the same two lines | Taken through R763-10-R1, as the ruling allows. The R763-10-R1 text is accurate (above), so R764-10-R2's defect is resolved at its cause | as above |
| R764-10-S1 | optional | Not taken, at the author's judgement. Reason: neither the assert nor the split fits under the 1000-line limit, and every growing listing's words start with "a ". I checked that reason: all 8 early names are well formed (`receipts/early-names.txt`). Accepted | — |

**Comment rule.** I grepped the delta's added lines for lane labels, rounds, reviewer IDs and comment IDs: no match. The new source text adds no comment at all. There is no new instance.

## Row 3 sweep (my own, re-run at this head)

The script is `scripts/row3_sweep.py`; its output is `receipts/row3-sweep.log` (rc 0).
- Row 3's domain (`TESTING.md:316`) is a parent whose live child outlives its own `SIGKILL`, crossed two ways:
  - the child is from the first census, or new since it;
  - there is no cancelled shell, the parent is under one never resumed, or it is beside one.
- That gives six cells. For each cell I wrote mutants confined to it:
  - `unspare`: the parent is not spared for that child;
  - `tick-early`: `kill_all` is applied 2^-19 s early;
  - `pass-late`: the parent is spared at exactly `kill_all`.
- For the four shell cells, I added `shell-killed-at-kill-all`: the never-resumed shell gets `SIGKILL` at 4 s.
- Results:
  - The unmutated copy is green.
  - All 22 mutants are red. Each is red on its own cell's listing:
    - "a stubborn parent" and "a live new descendant" for the no-shell cells;
    - the two new listings for the first-census shell cells;
    - "a live new descendant beside a shell never resumed" and "a parent beside a stopped shell and its live new descendant" for the new-child shell cells.
  - Survivors: none.
- `--mutants` at the head, 16 jobs, 37.6 s (`receipts/head-mutants.log`, rc 0):
  - `none` is green on all ten owner controls;
  - all 147 mutants that have a control are red with their words;
  - the result is `owned-process mutants: PASS (150 mutants, 147 with a control that must fail)`.
  - The three mutants without a control (`sigterm-checks-parent`, `no-sigcont-after-send`, `no-leaf-first`) are unchanged, closed classes.
- Whole test at the head: `suite cancellation: PASS` (`receipts/head-whole.log`, rc 0).

## Findings

None at BLOCKER, MAJOR, MINOR or RESIDUE.

**R764-11-S1 - SUGGESTION - Tests, Docs - `scripts/test_suite_cancellation.py:827` - the new loop has no comment of its own**
- **Evidence:** most nearby listing groups carry a one-line comment that states the cell, for example `:860-861` and `:867`. The new `for at, entry` loop does not.
- **Impact:** none on behaviour. A reader finds the cell's intent only in the guide (`TESTING.md:283`).
- **Optional change:** if room appears under the module limit, add a line such as "# A parent from the first census, beside or under a shell never resumed, is spared while its first-census child lives, to 4 s (#833)."
- **Verification:** reading the source. The idiom gate stays rc 0.

## Prior findings at this head

| ID | Severity | Status at 5843d1af | Evidence |
|---|---|---|---|
| R763-10-F1 | MINOR | RESOLVED at its cause: pinned with both listings and the mutant, named in row 3 | Item 1 above |
| R763-10-R1 | RESIDUE | TAKEN, exact text | Item 2 |
| R763-10-R2 | RESIDUE | RETAINED as residue for #495. These are out-of-domain sweep classes, and no action is asked for this PR | Ruling "anything else is residue" |
| R764-10-R1 | RESIDUE | TAKEN, exact text | Item 2 |
| R764-10-R2 | RESIDUE | RESOLVED through R763-10-R1 | Item 2 |
| R764-10-R3 | RESIDUE | RETAINED. The out-of-domain survivors are re-run by the author unchanged: 24 green on the whole test of 25 | author `receipts/final/r764-10-cell-sweep.log`, `r764-10-whole-rerun.log`, hash-verified |
| R764-10-S1 | SUGGESTION | NOT TAKEN, with a reason. Accepted | Item 2 |
| R764-6-S1 | SUGGESTION | RETAINED, not taken. It is outside #833 | PR body round 11 table |

## Published evidence checked

- I fetched nine author round 11 receipts from evidence commit `a0ae7348`. All nine match their `published_sha256` in `review-evidence/833-r1/MANIFEST.json`. The author's round 11 `PR-BODY.md` also matches (`d8dfacaa…`) (`receipts/evidence-spotcheck.txt`).
  - The receipts I checked: `layout-check.log`, `a726k-byte-f1.log`, `item1/mutants.log`, `item2/mutants.log`, `per_listing_none.log`, `r764-10-cell-sweep.log`, `r764-10-whole-rerun.log`, `ready.md` and `833-r764-10.manifest-check.txt` (empty).
- GitHub reports the evidence commit itself as `unsigned`. The integrity I verified is the manifest hash match, not a commit signature.
- The PR body's round 11 section matches what I found. That includes the claim of "on those two listings alone of 48" and the `parent-under-unresumed-shell-unspared` count of 3.

## Lens results

- [R764] PASS Conformance - `TESTING.md:283,296,298,316`; `test_suite_cancellation.py:791-793,827-829`; `process_test_support.py:913-916`; round 11 ruling items 1-2 - both items are met as stated. The listings' events equal the ruling's sequence. Row 3's six cells each have a listing (`receipts/row3-sweep.log`).
- [R764] PASS RTL - `scripts/owned_process.py` blob `6495a47b`, byte-identical to `fce77f0e` (`receipts/restore-check.txt`). There is no HDL in the delta.
  - The parent rule at `owned_process.py:324-330` gives the stated events in both new cells under `none` (`receipts/per-listing.log`).
  - That rule is the leaf-first spare to 3 s, then the live-child spare to `kill_all`, with the root shell skipped while unresumed.
- [R764] PASS Robustness - `owned_process.py:296-338`, unchanged; `receipts/head-whole.log`. The new cells cover a stopped shell never resumed beside a tree whose leaf outlives `SIGKILL`.
  - The product holds both shell and parent to their stated times.
  - At the 14 s verdict it sends `SIGKILL` to every remaining process.
  - The whole test passes, with its timeout, HUP and facility paths.
- [R764] PASS Tests - `test_suite_cancellation.py:776-829`; `process_test_support.py:913-916`; `receipts/head-mutants.log` (150/147 PASS); `row3-sweep.log` (22/22 red, identity green); `per-listing.log`; `per-listing-neighbours.log`; `relayout-ast.log` (IDENTICAL); `mutant-whole.log` (red); `head-whole.log` (PASS); `py-idiom.log` (rc 0).
- [R764] PASS Docs - `TESTING.md:283,296,298,316`; docstring `test_suite_cancellation.py:778-779`; author `PR-BODY.md` round 11 section, hash-verified.
  - The exact texts are verbatim.
  - The new guide sentence describes the two listings.
  - Row 3 names the mutant.
  - There is no comment-rule instance in the delta.
  - S1 is optional.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Round 11 ruling items 1-2; `TESTING.md:283,296,298,316`; `test_suite_cancellation.py:791-793,827-829`; `process_test_support.py:913-916`; `receipts/row3-sweep.log`, `mutant-edit-bytes.log` | R764-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |
| RTL | CLEAN | `scripts/owned_process.py` blob `6495a47b`, unchanged since `fce77f0e` (the round 10 RTL verdict carries; the delta changes nothing it depends on); `owned_process.py:324-330` against the new listings under `none` | R764-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |
| Robustness | CLEAN | `owned_process.py:296-338`, unchanged; `receipts/head-whole.log` (PASS); new never-resumed-shell cells (`per-listing.log`) | R764-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |
| Tests | CLEAN | `test_suite_cancellation.py:776-829`; `process_test_support.py:913-916`; `receipts/head-mutants.log`, `row3-sweep.log`, `per-listing*.log`, `relayout-ast.log`, `mutants-dict-delta.log`, `mutant-whole.log`, `py-idiom.log` | R764-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |
| Docs | CLEAN (S1 optional) | `TESTING.md:280-316`; docstring `:778-779`; author round 11 `PR-BODY.md` (manifest-verified); delta comment-rule grep | R764-11 | 5843d1af1d3a892fdc0fbb766ba2058ec44c26ea |

## Real limits

- **Delta only, per the ruling.** Code the delta does not touch keeps its round 10 lens verdict. I did not re-sweep row 3 beyond the six parent cells and the shell-spared-past-4 s clause, and I did not re-sweep rows 2 and 4 to 8.
- **What I ran.** Only `owner_stated_seconds`, `--mutants` (no `--matrix`), the whole cancellation test twice, and the Python idiom gate. I did not run the parent, PP, gPTP, Yosys, builder, docs.yml, behave or Verilator banks.
- **Hosted checks at the head** were mostly queued or in progress when I looked (`receipts/hosted-checks.txt`). `Physical gPTP` is skipped. I claim no hosted result.
- **Hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Manager source bank.** No manager source bank exists at this head, and I claim or infer none. Execution evidence at the source head is the author's published receipts, which I spot-checked by hash, plus my own runs above.
- **Clone state.** After the probes the clone is at the exact head. Worktree and index both equal tree `bfbcbc98`, there are no untracked files, and all six submodule gitlinks are unchanged (`receipts/restore-check.txt`).

## Pending manager duties

- Publish this report.
- Carry R763-10-R2 and R764-10-R3 (out-of-domain survivors, #495) and the SUGGESTIONs to the residue checklist.
- Validate the current-dev merge candidate with the builder and native banks at the merge turn, and link the receipts. Source base is `1f29f189279f9fc0132f4918e47342b87d22f33a`; live dev is `e61a4afaa54a598ceec08b7b5879285256cc60b6`.
- Hosted and act acceptance at the final head.
- Merge only with explicit maintainer authorization.

R764-11 FINISHED

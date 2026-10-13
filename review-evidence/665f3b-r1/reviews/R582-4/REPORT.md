[R582] POSITIVE - exact head 6b4feeca5d2fab0ec35cf071322cc775a5b15cb5

Round R582-4. Internal cleared-context review of PR #736 for issue #665, delta `532ab871..6b4feeca` (one documentation commit). Tree `4358f8ec29f0e104c8fe32dcd01dc719104ea44f`.

The verdict is POSITIVE. Every round-4 assignment item is met at this head. One PR-body wording item from R583-3-R1 was not applied. It is carried as RESIDUE (R582-4-R1). It does not affect the verdict or any lens.

## Scope and method

The round-4 assignment ([#665 comment 6156987825](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6156987825)) asks for three things:

1. Drop the count at `docs/testing/CI_WORKFLOWS.md:179`.
2. Name the new head as the published head in the PR body (R582-3-R1).
3. Change nothing else.

The assignment also requires `scripts/ci_events.py --check`, `scripts/check_doc_style.py` and `scripts/docs_check.py` to stay rc 0.

This round judges only those items, plus the hosted checks at the exact head. Earlier rounds stand for everything else.

I made my own pass over the delta before reading R582-3 and R583-3. No probe touched the review clone. The parent-tree control ran on a `git archive` extraction under `scratch/`.

## Assignment items, judged

| Item | Result | Evidence |
|---|---|---|
| `CI_WORKFLOWS.md:179` states no count, or the right one | **Met.** Line 179 now opens "These pages under `docs/` are relevant because Python in a classifier-gated job names them." It contains no number. | `receipts/delta.txt`; `receipts/check_paragraph.log` (opening line, no count word) |
| The paragraph still lists every `GATE_READ_DOCS` page | **Met.** `GATE_READ_DOCS` (`scripts/ci_scope.py:69-78`) has eight pages. The paragraph (`CI_WORKFLOWS.md:179-210`) links all eight, and it links no other `docs/` page. | `check_paragraph.py`, rc 0 (`receipts/check_paragraph.{log,rc}`). Negative control: the same script on `532ab871`'s two files returns rc 1, "count word present: ['Seven'] vs 8 pages" (`receipts/check_paragraph_parent.{log,rc}`). |
| `scripts/ci_events.py --check` rc 0 | **Met.** "ci_events: OK (2169 contract item(s) across 4 workflow files and docs/testing/CI_WORKFLOWS.md)" | `receipts/ci_events.{log,rc}` |
| `scripts/check_doc_style.py` rc 0 | **Met.** "documentation style: OK (22 current documents)" | `receipts/check_doc_style.{log,rc}` |
| `scripts/docs_check.py` rc 0 | **Met.** "docs_check: 0 finding(s) across 206 md files + 1287 scrubbed text files, scrub self-test 23/23, routing arms 4/4" | `receipts/docs_check.{log,rc}` |
| PR body names the new head as published (R582-3-R1) | **Met.** Body line 25: "`6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` is the published head of PR #736." The API reports `headRefOid` = `6b4feeca…`, not draft, base `dev`. | `receipts/pr736.json`, `receipts/pr736_body.md:22,25` |
| Nothing else changed | **Met.** `git diff --stat 532ab871..6b4feeca` reports one file, one line changed (+1/-1). No gitlink moved. The commit message is one line with no trailers, and its parent is `532ab871`. | `receipts/delta.txt` |

Additional checks:

- **Classifier self-test.** `scripts/ci_scope.py --selftest` returns rc 0. All eight gate-read arms print `ok`, and so does the removal mutation (`receipts/ci_scope_selftest.{log,rc}`).
- **Author's published check.** I re-ran `author-r4/round4/gate_read_paragraph.py` from evidence commit `8ab95062`, isolated, against this clone. It returns rc 0 and 6/6 controls refused, including a restored "Seven", a stated "Eight" and a stated "8". Its output is byte-identical to the published `gate-read-paragraph.log` (`receipts/author_gate_read_paragraph_rerun.{log,rc}`).

## Hosted checks at 6b4feeca (read, not accepted)

Snapshot: `receipts/check_runs_final.{json,txt}`, 27 check runs, all on head_sha `6b4feeca`.

**Docs workflow**

- `docs-check` (job 115586874121) completed `success`, 2026-10-13T23:05:55Z to 23:33:00Z. Every step concluded `success`, with none skipped (`receipts/docs-check-job.json`, `receipts/docs-check-summary.txt`).
- Its log (`receipts/docs-check-115586874121.log`) shows the same three results as the local runs:
  - `:715` docs_check: 0 findings
  - `:748` documentation style: OK
  - `:3160` ci_events: OK (2169 items)
- That job checked out the merge ref, `3bf924ce1 Merge 6b4feeca… into 0136de16…` (`:563`). Its environment is the hosted PR merge, not the bare source tree.
- `docs-check-no-git` and `wire-accountability` completed `success`.

**rtl-fast**

- The `rtl-fast` aggregate (job 115592290167) completed `success`.
- Its log (`receipts/rtl-fast-115592290167.log:60-70`) reports `success` for these 11 result lines: CHANGES, VERILATOR_LINT, BDD_CONFORMANCE, YOSYS_ELABORATION, PUBLICATION_CENSUS, FIRMWARE_UNIT, FIRMWARE_CONTROL_MUTANTS, FIRMWARE_AECP_MUTANTS, FIRMWARE_SRP_MUTANTS, FIRMWARE_BOUNDARY and FIRMWARE_VERILATOR.
- Each of those jobs is a check run concluding `success`, not `skipped`.

**Other runs**

- Yosys shards 0-3/4 and `full-ci-gate` completed `success`.
- `Physical gPTP (nightly and manual)` is `skipped`. That is a skipped context, not execution and not hardware proof.
- Still in progress at the snapshot: Verilator shards 0-4/5 and `elaborate`. I read no conclusion for them. Their acceptance is the manager's.

## Findings

### R582-4-R1 - RESIDUE - Docs (PR body only) - PR #736 body, "Status", line 30

This is the retained second half of R583-3-R1.

- **Evidence.** R583-3-R1 prescribed replacing "exact-head hosted acceptance follows the manager's push." with "exact-head hosted acceptance is the manager's." The round-4 assignment did not carry that half, and the body still reads "Round 4 local checks pass; exact-head hosted acceptance follows the manager's push." (`receipts/pr736_body.md:30`). The push of `6b4feeca` has happened, and the hosted runs are executing at that head.
- **Why RESIDUE.** This is pure wording in the PR body. It changes no figure, test, code, verdict or conformance claim, and it touches no privacy rule.
- **Exact fix.** In the "Status" section, replace "exact-head hosted acceptance follows the manager's push." with "exact-head hosted acceptance is the manager's."
- **Verification.** Read the PR body.

No BLOCKER, MAJOR or MINOR finding at this head.

## Prior public findings at this head

| Finding | Status at 6b4feeca | Evidence |
|---|---|---|
| R582-3-F1 (MINOR, Docs): "Seven pages" with eight registered | **Resolved** | No count at `:179`; all eight pages linked; parent control rc 1 |
| R583-3-F1 (MINOR, Docs): the same stale count | **Resolved** | As R582-3-F1 |
| R582-3-R1 (RESIDUE, PR body): stale published-head sentence | **Resolved** | Body line 25 names `6b4feeca…` |
| R583-3-R1 (RESIDUE, PR body): the same sentence, plus "follows the manager's push" | **Partly resolved.** The first half is applied. The second half is retained as R582-4-R1. | `receipts/pr736_body.md:25,30` |
| R583-3-S1 (SUGGESTION): mechanically check the count | **Moot.** The prose no longer states a count, and the body says so (lines 195-196). | `receipts/delta.txt` |
| Earlier findings (R582-1/2, R583-1/2) and the optional suggestions R582-1-S2, R582-1-S3, R582-2-S1 test options | **Unchanged.** Resolved ones stay resolved; the optional ones stay optional. The delta touches no artifact of theirs. | `receipts/delta.txt` |

## Per-lens results

- `[R582] PASS Conformance` — `docs/testing/CI_WORKFLOWS.md:179` and `scripts/ci_scope.py:69-78`, PR body lines 25/30, hosted check runs at `6b4feeca`. Checked against round-4 items 1-3 and against AGENTS.md section 7 (exact-head `rtl-fast` `success`; `verilator-suites` still running, so the manager owns it).
- `[R582] PASS RTL` — `receipts/delta.txt`. The delta touches no file under `hdl/`, `syn/`, `tb/` or `sw/`, and no gitlink, so no RTL artifact is in scope. Coverage from earlier rounds at `532ab871` stands, since nothing in RTL scope changed after it. Hosted Yosys shards 0-3 and `yosys-elaboration` are `success`.
- `[R582] PASS Robustness` — `receipts/delta.txt`. No input-handling, reset, timeout or configuration artifact changed. The prose change cannot go stale: it states no count, so a future `GATE_READ_DOCS` edit cannot invalidate the sentence. I confirmed this with the author's "correct count stated" and "digit count" controls (`receipts/author_gate_read_paragraph_rerun.log`).
- `[R582] PASS Tests` — `receipts/ci_scope_selftest.log` (8/8 gate-read arms `ok`, plus the removal mutation), `receipts/check_paragraph{,_parent}.log` (live rc 0, parent rc 1), and `receipts/author_gate_read_paragraph_rerun.log` (6/6 controls refused, byte-identical to the published log). The delta changes no test. The new author check can fail for the defect it targets: it returns rc 1 on `532ab871`.
- `[R582] PASS Docs` — `docs/testing/CI_WORKFLOWS.md:179-210` against `scripts/ci_scope.py:69-78`, plus the three doc checkers locally and in hosted `docs-check`, plus the PR body. R582-4-R1 is RESIDUE, so it leaves the lens clean.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `CI_WORKFLOWS.md:179`, `ci_scope.py:69-78`, PR body lines 25/30, `receipts/check_runs_final.txt` | R582-4 | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |
| RTL | CLEAN | `receipts/delta.txt` (no RTL, script or gitlink changed); hosted Yosys/`yosys-elaboration` `success` | R582-4 (no RTL-scope change since R582-3 at `532ab871`) | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |
| Robustness | CLEAN | `receipts/delta.txt`; author count controls rerun | R582-4 | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |
| Tests | CLEAN | `ci_scope.py --selftest`; reviewer paragraph check, live and parent control; author paragraph check rerun | R582-4 | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |
| Docs | CLEAN (R582-4-R1 RESIDUE carried) | `CI_WORKFLOWS.md:179-210`; `ci_events --check`, `check_doc_style`, `docs_check`, local and hosted; PR body | R582-4 | `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` |

## Real limits

- This is a delta review. Everything outside the round-4 items rests on earlier rounds, as the assignment directs.
- `CI_WORKFLOWS.md:214` still says "six pages under `docs/`" for `sw/builder/test_builder.py`. That is a different claim: it concerns the pages test_builder reads, not the gate-read list. The delta does not touch it, and I did not re-verify it this round.
- No manager source bank ran at this head, and I infer none. Source-head execution evidence is the author's published receipts plus my focused local checks.
- Hosted Verilator shards 0-4/5 and `elaborate` were still in progress at my snapshot. I read no conclusion for them.
- The hosted docs and rtl-fast jobs ran on the merge ref `3bf924ce1` (head merged into live dev `0136de16`), not on the bare source tree.
- Physical calibration NOT RUN. The skipped `Physical gPTP` context is not hardware proof.
- Clone integrity after review: HEAD `6b4feeca`, tree `4358f8ec`, zero status lines, index and worktree match HEAD. All six gitlinks were recorded, including `third_party/tsn-c-stack` at `70936b77` (`receipts/clone_integrity.txt`).

## Pending manager duties

- Accept the exact-head hosted `verilator-suites` (Verilator shards 0-4/5) and `elaborate` once they conclude, together with the other exact-head contexts.
- Carry R582-4-R1 to the residue checklist.
- Run the current-dev merge candidate (builder and native banks) at the merge turn and link the receipts. Then collect the external re-review at this head, run post-merge containment, and handle the maintainer merge authorization.

R582-4 FINISHED

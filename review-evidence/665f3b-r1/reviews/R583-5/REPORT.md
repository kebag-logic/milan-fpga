[R583] POSITIVE - exact head 7032bca5a51d8d97fcb73d7fc106ca4af21de38e

# R583-5: external cleared-context review of PR #736 (issue #665, lane F3b), merge-only delta

- Head: `7032bca5a51d8d97fcb73d7fc106ca4af21de38e`, tree `f1c1f47cb4fefb8a6c68418d03dc762f72cbee15`.
- Parents: `6b4feeca5d2fab0ec35cf071322cc775a5b15cb5` (lane, POSITIVE in R582-4 and R583-4) and dev `fa7347fc59173f90e4feec2df207692e6e6e72ec` (adds #696 via PR #706 and #734 via PR #735).
- Scope: the round-5 assignment (issue #665, comment 6158656140). Only the merge is judged here. Earlier rounds still cover everything else.
- Verdict: POSITIVE. No BLOCKER, MAJOR or MINOR finding is open. There are two new PR-body RESIDUE items and one retained one. None of them affects the verdict or any lens.

## Assignment items

| Item (comment 6158656140) | Result | Receipt |
|---|---|---|
| 1. A merge commit of `origin/dev` `fa7347fc`, not a rebase | **Met.** Two ordered parents, `6b4feeca` then `fa7347fc`. Subject: "Merge dev fa7347fc into F3b parent lane". | `receipts/merge_shape.txt` |
| 1. `git merge-tree` reports a clean merge with tree `f1c1f47c` | **Met.** `git merge-tree --write-tree 6b4feeca fa7347fc` returns `f1c1f47c…`, rc 0. HEAD's tree is the same. The parents have one merge base, `d40e4e98`. | `receipts/merge_shape.txt` |
| 2. `ci_scope.py --selftest` | **Met.** PASS, 202 `ok` arms, 0 FAIL. This includes #734's scope-history arms and both `MAILBOX_SPLIT.md` arms (relevant page, and refusal when filed as docs-only). | `receipts/campaign/ci_scope_selftest.{log,rc}` |
| 2. `ci_events.py --check` | **Met.** "OK (2174 contract item(s) across 4 workflow files and docs/testing/CI_WORKFLOWS.md)", rc 0. | `receipts/campaign/ci_events_check.{log,rc}` |
| 2. `act_ci.py --selftest` | **Not run by this reviewer.** The assignment forbids host act_ci and its self-test, so this rests on the author's receipt (`author-r5/round5/evidence/act-selftest.log`) and on the manager's act replica. | n/a |
| 2. `MAILBOX_SPLIT.md` still in `GATE_READ_DOCS` | **Met.** It is in the imported table (8 pages), and `ci_scope.py docs/design/MAILBOX_SPLIT.md` prints `true`. | `receipts/gate_read_docs.txt` |
| 3. Tree equals `f1c1f47c`, and the PR body says so | **Met.** See PR body lines 23-25 and 221-223. | `receipts/pr736_body.md` |

## Independent pass over the merge

- **Sides and overlap.** The lane changed 46 paths since `d40e4e98` and dev changed 28. Three paths changed on both sides: `scripts/ci_scope.py`, `docs/testing/CI_WORKFLOWS.md` and `sw/firmware/ctrl/maap/README.md`. Every other path carries exactly one side's blob. No mode changed, and `git diff fa7347fc HEAD` is exactly the lane's 46 paths. Receipts: `receipts/merge_sides.txt`, `receipts/per_path_origin.txt`, `receipts/gitlinks_modes.txt`.
- **Both-sided files.** In all three files, each side's `-U0` hunk set is present verbatim at the merge (hashes match per side). Nothing was hand-resolved. Receipt: `receipts/both_sided_hunks.txt`.
  - `ci_scope.py`: dev hooked `ci_scope_history.selftest` into `selftest()`. The lane added the `MAILBOX_SPLIT.md` table entry and its case. Neither touched the other's lines.
  - `maap/README.md`: dev rewrote the differential sweep sentences (`:219-223`). The lane's adapter and service-bound hunks sit at `:19` and `:109-164`, and the merged page reads coherently.
- **Gitlinks.** All six gitlinks equal the lane's. Only `third_party/tsn-c-stack` differs between the parents (lane `70936b77`, dev `405dc683`), and the lane's pin is kept. Receipt: `receipts/gitlinks_modes.txt`.
- **Semantic interaction (the one real cross-side risk).** #696 changes `hdl/ieee1722/maap/KL_maap.sv` and the shared-stimulus differential (`sw/firmware/ctrl/test/maap_differential.py`, `test_maap_differential.cpp`, 1,024-MAC sweep). That differential builds the stack's `maap.c` at the gitlink, which is the lane's `70936b77`, not the `405dc683` that #696 was validated against.
  - At the merge, using the pinned Verilator 5.050, the differential passes 12/12 checks. Its self-test catches 17/17 planted mutants, including `parent-ignores-mac` and the parent bound and count controls. Receipt: `receipts/campaign/maap_differential.{log,rc}`.
- **HDL.** The lane's only HDL delta is comment text in `hdl/milan/mailbox/KL_mbx_pkg.sv`; with comments stripped, the delta is empty. `KL_mbx` and `KL_maap` lint without errors under the pinned Verilator 5.050. `sw/mailbox/gen_mailbox.py --check --crosscheck` reports 0 findings. Receipts: `receipts/hdl_lint.txt`, `receipts/gen_mailbox_check.{log,rc}`.
- **Firmware.** Shard 0/4 of `test_ctrl_firmware.py --require-rv32 --self-test` runs as `firmware-unit` runs it. Its 61/61 arms pass, including `service_bounds` (47 checks, the reader of `MAILBOX_SPLIT.md`) and the RV32 arms, ending "test_ctrl_firmware: PASS", rc 0. Receipt: `receipts/campaign/fw_shard0.{log,rc}`.
- **Documentation gates at the merge.**
  - `docs_check.py`: 0 findings across 206 md files.
  - `check_em_dash.py --base 6b4feeca`: 0 findings over the 2960 added lines, 339/339 arms.
  - `check_doc_style.py`: OK.
  - `DOC_MAP.gen.py --check`: OK.
  - A reviewer-owned check resolves all 34 relative `.md#anchor` links from the 7 Markdown pages in the lane's delta, so none targets an anchor that #734's rewrite of `CI_WORKFLOWS.md` removed.
  - Receipts: `receipts/campaign/*.log`, `receipts/anchor_check.{log,rc}`, `scripts/anchor_check.py`.

## Hosted evidence at the exact head (snapshot 2026-10-14 02:00 UTC; acceptance is the manager's)

`receipts/hosted_checks_7032bca5.tsv` lists 27 check runs on `7032bca5`.

- **Executed and successful (19):**
  - `rtl-fast`, `changes`, `full-ci-gate`, `wire-accountability`, `docs-check-no-git`, `bdd-conformance`, `verilator-lint`, `publication-census`.
  - `firmware-unit`, `firmware-control-mutants`, `firmware-aecp-mutants`, `firmware-srp-mutants`, `firmware-boundary`, `firmware-verilator`.
  - `yosys-elaboration` and Yosys shards 0-3/4.
- **Skipped by design (1):** "Physical gPTP (nightly and manual)". This skip is not hardware evidence.
- **Still in progress (7):** `docs-check`, `elaborate`, Verilator shards 0-4/5.
- **Not yet emitted:** the `verilator-suites` and `yosys-portability` aggregates. The combined commit status is `pending`.
- **Act receipts:** none published at the time of writing.

## Findings

### R583-5-R1 - RESIDUE - Docs - PR #736 body line 224; author `REVIEW-READY-ROUND5.md:5`

- **Evidence.** The body says "Nothing else changes: every path keeps one side's bytes", and the author's receipt says "Each path keeps one side's bytes". Three paths are byte-equal to neither parent: `docs/testing/CI_WORKFLOWS.md`, `scripts/ci_scope.py` and `sw/firmware/ctrl/maap/README.md` (`receipts/per_path_origin.txt`, "MERGED-BOTH").
  - The next bullet in each document names exactly those three files.
  - The author's `round5/integrity.py` checks the correct rule (one side's bytes "unless both sides changed it").
- **Why RESIDUE.** This is pure wording in a PR body and a prose receipt. The check, the tree, the figures and the verdict are all right.
- **Exact fix.** Replace "every path keeps one side's bytes" with "every path changed on one side only keeps that side's bytes; the three paths both sides changed keep both sides' hunks verbatim".
- **Verification.** Read the PR body.

### R583-5-R2 - RESIDUE - Docs - PR #736 body line 29

- **Evidence.** The "Status" section says "`7032bca5…` is the head to publish on PR #736". The head is already published: GitHub `headRefOid` is `7032bca5…` (`receipts/pr736.json`), and hosted runs are executing on it. Round 4 fixed the same sentence (R582-3-R1, R583-3-R1), and round 5 reintroduced it.
- **Why RESIDUE.** This is pure wording in the PR body.
- **Exact fix.** Change it to "`7032bca5a51d8d97fcb73d7fc106ca4af21de38e` is the published head of PR #736."
- **Verification.** Read the PR body.

### R582-4-R1 (retained) - RESIDUE - Docs - PR #736 body line 34

- **Evidence.** The body still says "Round 5 local checks pass; exact-head hosted acceptance follows the manager's push." The push has happened.
- **Exact fix (unchanged).** Replace "exact-head hosted acceptance follows the manager's push." with "exact-head hosted acceptance is the manager's."

No BLOCKER, MAJOR or MINOR finding at this head. No SUGGESTION.

## Prior public findings on PR #736 at this head

I read these only after the independent pass above.

| Finding | Status at `7032bca5` | Evidence |
|---|---|---|
| R582-1..3 and R583-1..3 BLOCKER/MAJOR/MINOR (incl. R582-3-F1, R583-3-F1, the stale gate-read page count) | **Still resolved.** The merge changes no lane path except three both-sided files whose lane hunks survive verbatim. `CI_WORKFLOWS.md:179` still states no count, and all 8 registered pages are linked in `:179-204`. | `receipts/both_sided_hunks.txt`, `receipts/gate_read_docs.txt` |
| R582-3-R1 / R583-3-R1 (RESIDUE): stale published-head sentence | **Regressed in wording.** Carried as R583-5-R2. | `receipts/pr736_body.md:29` |
| R582-4-R1 (RESIDUE): "follows the manager's push" | **Retained.** | `receipts/pr736_body.md:34` |
| R583-3-S1 (SUGGESTION) | Moot, as R4 recorded. | n/a |
| R582-1-S2, R582-1-S3, R582-2-S1 (SUGGESTION) | Retained, optional. The merge touches no test or firmware they concern. | `receipts/merge_sides.txt` |

## Lens results

- `[R583] PASS Conformance` - `receipts/merge_shape.txt`, `receipts/gate_read_docs.txt`, `receipts/pr736_body.md:23-25,221-223`.
  - All three round-5 assignment items were checked against comment 6158656140: merge commit not rebase, tree `f1c1f47c` equal to the `merge-tree` prediction, `MAILBOX_SPLIT.md` registered, tree stated in the body.
  - The MAAP Annex B timing contract (B.3.4.2 strict 500/600 ms draws, Table B.7 four PROBEs) still holds between the lane's stack pin and #696's parent: `receipts/campaign/maap_differential.log`.
- `[R583] PASS RTL` - `receipts/hdl_lint.txt`, `receipts/per_path_origin.txt`, `receipts/campaign/maap_differential.log`.
  - Every HDL path at the merge equals one parent's blob. The lane's `KL_mbx_pkg.sv` delta is comments only.
  - `KL_mbx` and `KL_maap` lint without errors under Verilator 5.050.
  - The merged `KL_maap.sv` elaborates in the differential with the lane's firmware core.
  - Hosted `verilator-lint`, `yosys-elaboration` and Yosys shards 0-3 succeeded at this head.
- `[R583] PASS Robustness` - `receipts/both_sided_hunks.txt`, `receipts/gitlinks_modes.txt`, `receipts/merge_sides.txt`.
  - Of the paths that could collide, only three were changed on both sides, and none overlaps line-wise. Both sides' hunks survive verbatim.
  - Gitlinks keep the lane's stack pin, and no mode changed.
  - The differential's 1,024-MAC sweep and its mutants pass against the lane's pin.
- `[R583] PASS Tests` - `receipts/campaign/ci_scope_selftest.log`, `receipts/campaign/maap_differential.log`, `receipts/campaign/fw_shard0.log`.
  - 202 scope arms, including #734's history arms and the lane's gate-read refusal arms.
  - The differential's 17/17 planted mutants are caught, so the cross-side test can fail.
  - Firmware shard 0 passes 61/61 arms, including the 47-check service-bounds reader.
  - The hosted firmware jobs and mutation campaigns succeeded at this head.
- `[R583] PASS Docs` - `docs/testing/CI_WORKFLOWS.md:179-204`, `sw/firmware/ctrl/maap/README.md:196-226`, `receipts/campaign/{docs_check,em_dash,doc_style,doc_map,ci_events_check}.log`, `receipts/anchor_check.log`, and the PR body.
  - The merged pages read coherently, the gates pass, and the cross-page anchors resolve.
  - Three PR-body wording items are RESIDUE, which leaves the lens clean.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Merge parents and tree, `merge-tree` prediction, `GATE_READ_DOCS`, PR body tree statement, MAAP differential (Annex B B.3.4.2 / Table B.7) | R583-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |
| RTL | CLEAN | `KL_mbx_pkg.sv` (comment-only), `KL_maap.sv` (dev bytes), Verilator 5.050 lint, differential elaboration, hosted lint and Yosys | R583-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |
| Robustness | CLEAN | Per-path origin, both-sided hunk preservation, gitlinks and modes, 1,024-MAC sweep at the lane's pin | R583-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |
| Tests | CLEAN | `ci_scope --selftest` (202), `ci_events --check` (2174), differential 12/12 + 17/17, firmware shard 0 61/61 | R583-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |
| Docs | CLEAN (R583-5-R1, R583-5-R2, R582-4-R1 RESIDUE carried) | `CI_WORKFLOWS.md`, `maap/README.md`, docs gates, 34 anchor links, PR body | R583-5 | `7032bca5a51d8d97fcb73d7fc106ca4af21de38e` |

## Real limits

- **Not run by this reviewer:** host `act_ci.py` and its self-test, which the assignment forbids, and Docker/act. Firmware shards 1-3/4 (the control, AECP and SRP mutation campaigns) were not rerun locally either; I rely on their hosted success at this head.
- **No full banks.** No full parent, protocol-processor, gPTP, Yosys, Verilator-sweep or builder bank was run. No manager source bank exists at this head, and none is claimed or inferred.
- **Hosted runs incomplete at the snapshot.** `docs-check`, `elaborate` and Verilator shards 0-4 were still in progress, and the `verilator-suites` and `yosys-portability` aggregates had not been emitted.
- **Candidate `c585f506` not inspected.** It is not fetchable from the public remote, so its tree equality with `f1c1f47c` and its builder bank are the manager's statement, not checked here.
- **Base naming.** The assignment names `a0f39ad4` as source base. That commit is an ancestor of dev `fa7347fc`, not of the lane parent `6b4feeca`; the lane's fork point and the merge's single merge base is `d40e4e98`, which dev absorbed through PR #705 (`0136de16`). The review used the two parents and that merge base. The `a0f39ad4..7032bca5` diff (118 files) includes dev's own changes.
- **No hardware evidence.** Physical calibration was NOT RUN, and the skipped Physical gPTP context is not hardware proof. Local runs used CPython 3.14.7, GCC 16.2.1, GoogleTest 1.18.0 and the pinned Verilator 5.050, not the hosted CPython 3.12 image.
- **Earlier collided runs.** Two background attempts of firmware shard 0 were invalidated because I deleted their build directory while they were running. Their rc 2 logs are kept under `receipts/campaign/superseded/`. The counted result is the single clean foreground run in a fresh directory.
- **Clone restored.** The clone is back at exact head bytes: no tracked change, no untracked or ignored file, and `ls-files -s` hash unchanged. Only the index stat cache was refreshed. Submodules are clean at their gitlinks. Receipt: `receipts/final_state.txt`.

## Pending manager duties

- Hosted acceptance at `7032bca5`: `docs-check`, `elaborate`, the Verilator shards, and the `verilator-suites` and `yosys-portability` aggregates.
- Run the act replica for this head and publish its receipts.
- Current-dev candidate-merge validation, with the builder and native banks, at the merge turn.
- The residue checklist: R583-5-R1, R583-5-R2 and R582-4-R1.
- Confirm the second positive review is independent.
- Explicit maintainer merge authorization.
- Post-merge containment, then move the card to Done.

R583-5 FINISHED

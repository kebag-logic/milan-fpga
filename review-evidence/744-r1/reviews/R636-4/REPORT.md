[R636] POSITIVE - exact head 20cd16e18f9b7cd41d597495c785e61443c62b87

Round R636-4, internal independent review of issue #744 / PR #745. Head `20cd16e18f9b7cd41d597495c785e61443c62b87`, tree `d8e0a4837a772543b834148127ac70d7dbb991bf`. Reviewed in a cleared context from a detached clone at that head, non-root.

- **Scope:** a merge-only delta, `7997eeb3..20cd16e1`. It is one merge commit. Parent 1 is the PR head `7997eeb348c3af302079c7273d1b3092eee4dc6c`, which R636-3 found POSITIVE. Parent 2 is dev `734eb780dc93896a5961cd95180f79475a401650`, which carries PR #749 for #748 and PR #747. The merge base is `84f9e3001b7d9b77835c4a9a599dbe6230a8031b`.
- **Prior verdicts that stand:** R636-3 (POSITIVE at `7997eeb3`) and R637-2 (POSITIVE at `43a25fa7`) still cover the PR's own changes, because the merge leaves every PR-side file byte-identical. Proof is below.
- **Result:** no BLOCKER, MAJOR or MINOR is open. One RESIDUE is recorded. It comes from dev, not from this PR. It does not change the verdict and leaves every lens clean.

## Inputs, in reading order

1. `AGENTS.md` §§3-8 and the review lenses it names. `CONTRIBUTING.md` was not re-read beyond the lens and merge rules those sections cite.
2. Issue #744 body. It names two defects: the slot OOM report is false, and the census self-test can exhaust the slot. Also read the assignment and clarification comments (`6197842304`, `6197855588`) and the round-2 and round-3 manager comments. I read only their first lines, because the scope of this round is merge-only.
3. The review-start comment `6206577903`.
4. `git log 84f9e300..734eb780` (17 commits) and `git diff --stat` for both sides of the merge.
5. The full dev-side diff of the two files both sides touched, and the PR-side diff of the same files.
6. R636-3 (`6202239330`) and R637-2 (`6200862558`). I read their findings sections only after my own pass over the merge was done.
7. A listing of the evidence tree `7b102ada:review-evidence/744-r1/`. It holds author rounds r1-r3 and the review packets for R636-1/2 and R637-1/2. It holds no receipt at `20cd16e1`.
8. The hosted check runs at the exact head, as a snapshot.

## (1) The merge introduces no change of its own

Receipts: `receipts/01_merge_tree_reproduction.txt`, `receipts/02_merge_parent_identity.txt`, `receipts/03_merge_identity_script.txt`. The portable script is `scripts/merge_identity.sh`.

- **The tree replays exactly.** `git merge-tree --write-tree 7997eeb3 734eb780` gives `d8e0a4837a772543b834148127ac70d7dbb991bf` with rc 0 and no conflict. That is the head tree, so no byte was resolved or edited by hand.
- **The file sets match.** The files changed in `HEAD^1..HEAD` are exactly those in `base..dev` (18 files). The files changed in `HEAD^2..HEAD` are exactly those in `base..PR` (9 files).
- **Single-side files are untouched.** All 23 files that only one side touched have the same blob at the head as on the side that touched them: 16 from dev, 7 from the PR.
- **Shared files carry both patches unchanged.** For the two files both sides touched, each side's patch reappears on the other parent with a stable patch-id: `scripts/ci_events.py` dev `a3d94a02…` and PR `4e9e6494…`, `docs/testing/CI_WORKFLOWS.md` dev `10f62872…` and PR `7d9fdd56…`. All four are EQUAL.
- **No gitlink moved.** The six submodule gitlinks are identical across both parents and the head.

## (2) The two shared files compose

**`scripts/ci_events.py`**

- **What each side changed:**
  - The PR side is one line, `:2488`, in the `publication-census` step of `RTL_STEP_LISTS`. It changes `--jobs "$CI_CAMPAIGN_JOBS"` to `--jobs "$CI_CENSUS_JOBS"`.
  - The dev side adds the `elaborate` writer `Put a job-private Python environment on PATH` (`:569-577`) and its carrier step (`:1219`).
  - It adds three #748 mutation arms (`_private_interpreter_arms`, `:7453`, wired in at `:8348`).
  - It also bumps the `elaborate` step count from 20 to 21 in four expected messages.
- **The hunks are disjoint.** No dev token (`litex-venv`, toolcache, setup-python, elaborate) appears in the PR side's changes to `scripts/` or `.github/`, and no PR token (OOM, `memory.events`, `memory.peak`, `CI_CENSUS_JOBS`, census) appears in dev's. That leaves one place where they could interact: the PR's census budget step must stay unique to `publication-census` after `elaborate` gains a step.
- **The census budget step is still unique.** `ci_gate_workflows_selftest.py:342-350` asserts exactly that by generating all four workflows at the head. It passes: `receipts/17_ci_gate_workflows_selftest.log:73`, "only publication-census sets CI_CENSUS_JOBS, before its census".
- **The contract and arms hold.** At the head, `ci_events.py --check` reads OK, 2199 contract items across 4 workflow files and `CI_WORKFLOWS.md`. `--selftest` reads PASS: 2199 items, 5236 arms. The three #748 arms are caught (`receipts/11_ci_events_selftest.log:2597-2599`), and so are all of the PR's census and slot items.

**`docs/testing/CI_WORKFLOWS.md`**

- The dev hunk sits at `:1424-1466`, in the Elaboration section: the job-private interpreter and the `ci_toolcache_isolation.py` control.
- The PR hunks sit at `:307-320` (census `CI_CENSUS_JOBS`), `:2013+` and `:2070-2080` (memory-derived census workers), and the slot OOM accounting sections. They are far apart and in different subjects.
- No sentence of either side refers to the other's content. `ci_events.py --check` reads this page as part of its contract, and it passes.

## (3) Head gates

Receipts are in `receipts/1*.log` and `receipts/1*.rc`. All commands were run from the clone root.

| Command | rc | Result |
|---|---|---|
| `python3 scripts/ci_events.py --check` | 0 | OK, 2199 contract items |
| `python3 scripts/ci_events.py --selftest` | 0 | PASS, 2199 items, 5236 arms (196 s) |
| `python3 scripts/check_baremetal_only.py --check` | 0 | OK, 0 findings across 1345 tracked first-party files |
| `python3 scripts/ci_gate_workflows.py --check` | 0 | quiet pass |
| `python3 scripts/ci_install_workflows.py --check` | 0 | quiet pass |
| `python3 scripts/ci_runtime_workflows.py --check` | 0 | quiet pass |
| `python3 scripts/ci_suite_workflows.py --check` | 0 | quiet pass |
| `python3 scripts/ci_gate_workflows_selftest.py` (extra) | 0 | "gate workflow and union controls: PASS" |

These agree with the manager's statement that all of them return rc 0.

## Findings

### R636-4-R1 RESIDUE (Docs): "That command" now follows the wrong command

- **Origin:** dev, from PR #749 / #748. The merge did not introduce it, and it is not this PR's change.
- **Where:** `docs/testing/CI_WORKFLOWS.md:1468`, which reads "That command runs in two measured legs (#737)."
- **Problem:** #748 inserted two paragraphs and a three-line `ci_toolcache_isolation.py` code block between this sentence and the command it refers to: `sw/builder/test_builder.py --require-elaboration --require-rv32`, at `:1419`. "That command" now reads as the isolation control, which has no legs. Dev `734eb780` has the same adjacency at `:1466`, so the merge only carries it.
- **Impact:** wording only. No measurement, figure, verdict, test or contract item changes.
- **Exact fix:** replace "That command runs in two measured legs (#737)." with "The builder command, `sw/builder/test_builder.py --require-elaboration --require-rv32`, runs in two measured legs (#737)."
- **Where to fix it:** on dev, as a #748 follow-up or in the residue checklist. Not in this lane, because AGENTS.md §4 forbids an opportunistic scope expansion.
- **Verification:** read the sentence in context, then run `ci_events.py --check`.

### Observation, not a finding: lane labels in dev's source comments

The merge brings dev's #645 changes into the PR's diff against its base. Those changes carry bench-lane labels ("bench lane B17", and others) in source comments in `hdl/milan/milan_datapath.sv` and `tb/verilator/follow_ring/*` (`receipts/31_comment_rule_scan.txt`).

These are not new instances in the reviewed delta:

- every one of those files is blob-identical to dev `734eb780`;
- they come from `4e6b5398` and later commits, which are already on dev;
- #746 lists them as known instances at dev `9ef71772`.

The merge adds no source comment of its own, as the tree replay in (1) shows. So no RESIDUE is raised.

## Prior findings, resolved or retained at this head

| Prior item | Status at `20cd16e1` | Why |
|---|---|---|
| R636-3-S1 SUGGESTION: three cross-declared-file pairings skipped by the new arms | **Retained, optional** | `scripts/check_baremetal_only.py` is blob-identical to `7997eeb3`, so nothing changed. |
| R636-3-S2 SUGGESTION: re-wrap a shortened comment | **Retained, optional** | Same file, unchanged. |
| R636-3-S3 SUGGESTION: the MemTotal reason also covers a zero value | **Retained, optional** | `.github/workflows/rtl-fast.yml`, `scripts/ci_runtime_workflows.py` and `scripts/ci_gate_workflows_selftest.py` are blob-identical to `7997eeb3`. |
| R636-2-F1 to F4, R636-1 / M1 BLOCKER, R637-1-F1 and F2 MAJOR, earlier R636-2 and R636-3/4 items as resolved in R637-2 | **Still resolved** | R636-3 and R637-2 resolved them at their causes. The merge changes none of the files those resolutions cite: `check_baremetal_only.py`, `ci_runtime_workflows.py`, `ci_gate_workflows_selftest.py`, `act_ci.py`, `rtl-fast.yml`, and the PR's `CI_WORKFLOWS.md` hunks, whose patch-id is equal. |

## What was checked, per lens

```text
[R636] PASS Conformance — receipts/01_merge_tree_reproduction.txt, 02_merge_parent_identity.txt; scripts/ci_events.py:2488, .github/workflows/rtl-fast.yml:432-463,551 — issue #744 items 1-2 rest on PR-side files that are blob-identical to 7997eeb3 (R636-3/R637-2 POSITIVE); the merge tree replays exactly and adds nothing of its own
[R636] PASS RTL — receipts/02_merge_parent_identity.txt (hdl/milan/milan_datapath.sv blob == dev 734eb780) — the PR's delta has no HDL; the only RTL in the merge is dev's #645 change, carried byte for byte with no conflict, no resolution and no gitlink move
[R636] PASS Robustness — scripts/ci_gate_workflows_selftest.py:342-350 at head, receipts/17_ci_gate_workflows_selftest.log:57-73 — the census budget's refusal and pass cases still hold, and its step stays unique to publication-census after elaborate gains a step
[R636] PASS Tests — receipts/10..17 (ci_events --check/--selftest 2199 items/5236 arms, #748 arms log:2597-2599; check_baremetal_only --check 1345 files; four generators --check; gate selftest), all rc 0 at head
[R636] PASS Docs — docs/testing/CI_WORKFLOWS.md:307-320,1424-1466,2070-2080 at head — the hunks are disjoint and the page passes ci_events --check; the one dev-originated wording residue is R636-4-R1 (RESIDUE, does not unclean the lens)
```

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | merge-tree replay; parent identity of 23 files; `ci_events.py:2488`; `rtl-fast.yml:432-463` | R636-4 (merge delta); R636-3 for the PR's own changes, unchanged since | `20cd16e18f9b7cd41d597495c785e61443c62b87` |
| RTL | CLEAN | `hdl/milan/milan_datapath.sv` blob equals dev; no PR-side HDL; gitlinks unchanged | R636-4 | `20cd16e18f9b7cd41d597495c785e61443c62b87` |
| Robustness | CLEAN | `ci_gate_workflows_selftest.py:235-350` executed at head | R636-4 | `20cd16e18f9b7cd41d597495c785e61443c62b87` |
| Tests | CLEAN | `ci_events` `--check`/`--selftest`, `check_baremetal_only --check`, four generators `--check`, gate selftest | R636-4 | `20cd16e18f9b7cd41d597495c785e61443c62b87` |
| Docs | CLEAN (R636-4-R1 RESIDUE carried) | `CI_WORKFLOWS.md` both sides' hunks; contract check | R636-4 | `20cd16e18f9b7cd41d597495c785e61443c62b87` |

## Real limits

- **No parent-side counts.** I did not re-run `ci_events.py` at the base or at either parent to show item and arm counts adding up across the merge. That probe was not permitted in this session. Composition rests on the exact tree replay, the patch-id identity, and the passing head gates.
- **No suite reruns.** As assigned, I re-ran no Verilator, Yosys, builder, parent, PP or gPTP suite, and no act or Docker job. The census and slot behaviour at runtime rests on the author's published receipts at earlier heads, which the prior rounds reviewed, and on the manager's act replay.
- **No receipt at this head.** I found no manager act-replay receipt at `20cd16e1` in the evidence tree I inspected (`7b102ada`). I do not claim one.
- **Hosted checks were still running.** At 2026-10-16T02:25:50Z every hosted check run on the exact head was `queued` or `in_progress` (`receipts/30_hosted_checks_snapshot.txt`), and none had concluded. I draw no hosted verdict.
- **No hardware.** Physical calibration was NOT RUN. Field skips are not hardware proof.
- **Clone restored.** The clone is unchanged: HEAD and tree match, the status is clean, the index equals the tree, and all six gitlinks are at their recorded commits (`receipts/40_restore_verification.txt`).

## Pending manager duties

- Publish and accept the full act replay at `20cd16e1` as the census and slot receipt.
- Accept the hosted `rtl-fast`, `verilator-suites` and `yosys-portability` contexts on this exact head once they conclude.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn, and run post-merge containment.
- Obtain the external positive review this round does not replace.
- Carry R636-4-R1 (dev-originated) to the residue checklist, or to a #748 follow-up. Carry R636-3-S1 to S3 as optional.
- Get the maintainer's authorization before any merge.

## Packet

`REPORT.md`, `scripts/merge_identity.sh` and `receipts/*`, as listed in `MANIFEST.sha256`.

R636-4 FINISHED

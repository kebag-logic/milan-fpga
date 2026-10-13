[R632] POSITIVE - exact head 59354ffe75697e17a16fd117d9ba853e104394bc

# R632-4 internal independent review: issue #734 / PR #735

- **Head**: `59354ffe75697e17a16fd117d9ba853e104394bc`, tree `e732e9f65636bfd49cb9af9844f27077ce037df7`. Source base and live dev are both `a0f39ad4f4bfc9ed4805bac049c4f2b926a94ec0`. Round delta: `97907c2e..59354ffe` (2 commits). Full diff reviewed: `a0f39ad4..59354ffe`, 10 files, +947/-135, 8 one-line commits with no trailers.
- **Sources, in order**:
  - AGENTS.md, CONTRIBUTING.md (sections 2.1 and 3), docs/README.md, and REQUIREMENTS.md REQ-VER-04.
  - Issue #734: the body, the assignment (6151273761), and the round 2, 3 and 4 decisions (6151933918, 6152693618, 6153494016), plus the executor's TAKEN and four REVIEW READY comments.
  - The PR #735 body.
  - The full diff and all eight commits.
  - `docs/testing/CI_WORKFLOWS.md` and `docs/testing/TESTING.md`.
  - The author's published receipts at `beeb9d6c:review-evidence/734-r1/author-r4`.
  - The hosted `changes` job log at this exact head.
- **Independence**: the verdict and ledger below were formed from my own pass over the diff, gates and probes before I opened any earlier review. Prior findings are reconciled in their own section, after that pass.
- **Result**: all five lenses were applied, and all five are CLEAN. No BLOCKER, MAJOR or MINOR is open.
  - **R632-3-F1 is resolved.** CI now runs the documented flat isolated install. A sibling import planted in a different unrelated self-test function fails the exact CI step.
  - **The live-base rule is unchanged and sound.** REV, REV+E and B16 keep their outcomes, and all five linked images are byte-identical base-to-head.
  - I found no path where a PR's own RTL change, or an RTL file restored after a merge, is classified docs-only by a hosted run. The only such path needs a source-head checkout without the replay marker; that is retained as SUGGESTION S1.
  - Two prose-only RESIDUE items are in the PR body.

## Findings

### R632-4-R1 RESIDUE - Docs - PR body still says the Round 4 commits are local

- **Location**: PR #735 body, section "Status", line 2: "The two Round 4 commits remain local; publication is pending."
- **Evidence**: the PR's `headRefOid` is `59354ffe…`. Hosted runs 38457132837/788/832/795 execute at that sha (`receipts/hosted-runs-59354ffe.txt`). This is the same class as R633-2-D1.
- **Impact**: stale publication wording only. It changes no measurement, gate, verdict, code or clause claim.
- **Exact fix**: replace the sentence with "Round 4 head `59354ffe` is published."
- **Verification**: read the published body.

### R632-3-R2 / R633-3-R1 RESIDUE (retained) - Docs - duplicate closing keyword

- **Location**: the PR body, "Linked Issue / roles", lines 1-2. `Closes #734` still appears twice. The "Round 4" section's claim that "The prepared body has one closing keyword" is therefore not true of the published body.
- **Exact fix**: delete one of the two `Closes #734` lines.
- **Verification**: read the published body.

### S1 SUGGESTION (retained R632-2-S2 / R632-3-S1) - Robustness - hosted branch does not assert the merge shape

- **Location**: `.github/workflows/rtl.yml:123`, `rtl-fast.yml:55`, `elaborate.yml:112`.
- **Evidence**: diagnostic D1 in `receipts/probe_r632_4.log` runs the hosted branch with `GITHUB_SHA` set to a bare multi-commit PR head (RTL first, three docs commits after). All three bodies answer `rtl=false` with `README.md` only.
- **Reachability**: no real path to this was found.
  - GitHub's `pull_request` sha is a two-parent merge even when the head can fast-forward. PR #735 itself gets `Merge 59354ffe… into a0f39ad4…`, with parents `a0f39ad4 59354ffe` (`receipts/merge-ref-735.txt`).
  - The hosted `changes` job checked out that merge (`receipts/hosted-rtl-fast-changes-59354ffe.log:564`).
  - The replay branch is selected by the `ACT` marker that the replay tool sets itself.
- **Optional fix**: before the hosted diff, add `[ "$(git rev-parse "$GITHUB_SHA^2")" = "$PR_HEAD_SHA" ]`. That fails closed both for an unexpected source-head checkout and for a replay that lacks its marker.
- **Status**: optional. It does not unclean a lens.

### Observation, outside this diff (no finding)

`elaborate.yml:115` publishes `rtl=$(python3 scripts/ci_scope.py …)` inside an `echo`, so a classifier crash there would publish an empty `rtl` rather than fail the step.

This line is unchanged by the PR, and it is pinned as canonical by `ci_events.py`. The classifier self-test runs first in the same `set -e` step. It is listed for the manager to decide whether a separate Issue is wanted.

## Evidence (all at the exact head unless noted)

### Gates (`receipts/gates/*.log` and `*.rc`)

All of these exit 0:

- **Scope classifier**: `ci_scope.py --selftest` PASS, 197 assertions, 93 of them scope-history.
- **Contract gate**: `ci_events.py --check` OK with 2021 contract items, and `--selftest` PASS with 2860 arms.
- **Documentation gates**: `docs_check` and its selftest; `check_doc_paths`; `check_doc_style`; `gen_toc --check`, `--selftest` and `--verify-anchors`; `check_em_dash --base a0f39ad4` and its selftest.
- **Source and evidence gates**: `check_py_idiom` and `check_sh_idiom` with their selftests; `pp_srcs --check` and `--selftest`; `measure_test_evidence --check` and `--selftest`.

The Markdown gates used an existing interpreter environment that satisfies the hash-locked renderer requirements; I modified nothing in it. The first idiom and evidence-reader attempts refused with rc 2 because the scratch clone had no submodules. They were re-run after local initialisation at the recorded pins, and the receipts are the re-runs.

### Runner self-tests (bootstrap rule)

Neither form ran in the host process space. Each ran inside an unprivileged namespace sandbox (bubblewrap): no network, the host filesystem read-only, throwaway `/tmp`, `/home` and `HOME`, and no credentials (`scripts/run_act_selftests_sandboxed.sh`).

- **Ordinary form**: `python3 scripts/act_ci.py --selftest` PASS, 566 ok and 0 FAIL. That count includes its complete isolated flat child.
- **Documented flat form**: `install -m 0555 …; python3 -I <dir>/act_ci.py --selftest --worktree <checkout>` PASS, 564 ok.

### The exact docs.yml step (R632-3-F1)

`scripts/run_docs_step_mutation.sh` reads the "Local act runner contract gate" body from `docs.yml:389-395` with a YAML parser and runs it unchanged in the same sandbox.

| Step and tree | Result | Receipt |
|---|---|---|
| Pristine head | rc 0, two `selftest: PASS` | `docs-step-exact-pristine` |
| Head with `import ci_scope` planted in `selftest_dry_run_cpu_ranges`, a function outside both the scope-event graph and the history-wiring function | rc 1: the ordinary form FAILs `flat isolated full selftest uses the explicit shipping worktree` | `docs-step-exact-planted` |
| The flat command alone on the planted tree | rc 1, `ModuleNotFoundError: No module named 'ci_scope'` | `flat-only-planted` |

The planted module exists in `scripts/`, so only the isolated flat form can see the defect. CI now runs that form, through both the ordinary self-test's child and the direct third command.

### Independent scope probe (`scripts/probe_r632_4.py`)

The probe reads the three bodies with PyYAML and asserts their env bindings. Only the recursive `ci_scope.py --selftest` is replaced, by `:`. It builds 16 lane histories with hermetic Git and runs each in two modes:

- **Hosted**: a two-parent merge with the live base as first parent, and `ACT` unset.
- **Replay**: `ACT=true`, the head checked out, and `refs/remotes/origin/dev` set to the live base.

Results (`receipts/probe_r632_4.{log,json,rc}`, rc 0):

- **102 of 102 graded executions match their path and verdict oracle**, in all three bodies and both modes. Every case except the empty net delta has dev moved past the fork point; C5, C6 and C11 merge newer dev into the lane.
  - **Relevant, and must stay so**: C2 own RTL on a stale base; C3 `protocol-processor` pointer; C3b documentation-shaped gitlink; C4 empty net delta; C5 REV; C6 REV+E; C7 RTL buried under three later docs commits; C8 RTL deletion; C9 RTL renamed into `docs/`; C10 RTL mode-only change; C11 merge conflict resolved to the lane's RTL; C13 non-ASCII (quoted) RTL path; C14 `.gitmodules` only; C15 dev renames a page into a gate-read path.
  - **Docs-only, as they should be**: C1 stale-base docs; C12 lane merged dev cleanly, own change docs.
- **Replay refusals**: replay refuses criss-cross ancestry (C16) and merge conflicts (C17), with no output.
- **Push events keep their behaviour**:
  - `rtl-fast` diffs before to after, and falls back to `git ls-files` for a zero before-sha.
  - `rtl` and `elaborate` answer `rtl=true`.
- **27 of 27 mutations are killed**, in each of the three bodies:
  - MH1, the two-dot frozen base;
  - MH2, the frozen merge-base;
  - MH3, the head's first parent only;
  - MR1, a frozen recorded base in replay;
  - MR2, a head-only merge-base in replay (killed by C15);
  - MR3, a live-to-head two-dot comparison;
  - MC1, `hdl/` treated as docs;
  - MC2, the submodule rule removed (killed by C3b);
  - MC3, the empty-diff rule removed.
- **B16 on the real objects**:
  - Recorded base `49da9fd9` to head `f1b2489f`: 64 paths two-dot with default renames, 65 with `--no-renames`, and 2 paths merge-base.
  - The landed merge `6c810c45` and its live first parent `e81ce82f` give exactly `docs/findings/629_MEDIA_CLOCK_FOLLOWING_BENCH.md` and `docs/findings/README.md`, `rtl=false`. That holds in all six executed shipping bodies (hosted from the real merge; replay against the live first parent).

### Hosted evidence at this head (observed, not accepted)

- `rtl-fast` `changes` checked out `276928faf Merge 59354ffe… into a0f39ad4…`. It ran the history self-test (93 checks) and listed exactly the 10 PR files that I computed from `merge^1..merge`. Its verdict was `RTL/tooling relevant: true`.
- `rtl-full` `full-ci-gate` succeeded, and its shards were running.
- `docs-check`, which carries the new flat step, and `elaborate` were still in progress when I read them (`receipts/hosted-runs-59354ffe.txt`).

### Five linked images (`scripts/run_images.sh`, `receipts/prior/images.log`, `receipts/image-comparison.json`)

`ctrl_image.py --base a0f39ad4` rebuilt `endstation_arty_4x4`, `endstation_arty_8ch`, `endstation_arty_current`, `endstation_ax7101_1x1_tdm8` and `endstation_ax7101_8x8`. The build used the pinned SDK archive (sha256 `d42680e9…`, `receipts/sdk-archive-sha256.txt`), inside the sandbox.

- All five base/head pairs are byte-identical.
- Their sizes match the author's (50752, 50752, 50744, 50768 and 50776 bytes).
- Their absolute hashes differ from the author's, which came from a different compiler build. Only pairwise identity is claimed.
- No gitlink, HDL, firmware, configuration or synthesis input is in the diff (`receipts/hygiene.txt`).

### Exact-head restoration (`receipts/exact-head-restoration.txt`)

- HEAD and tree are exact, and `write-tree` equals the tree.
- 1308 tracked files rehashed with 0 blob mismatches and 0 executable-mode mismatches.
- Index entries (mode, blob, path) equal the HEAD tree.
- There are no unmerged, assume-unchanged or skip-worktree entries.
- The submodule gitlinks are at their pins, and the initialised ones are clean.
- All probes and mutations ran on scratch copies.

## Prior public findings at this head

Every prior probe below was re-run unchanged, from `beeb9d6c:review-evidence/734-r1/reviews`. Receipts are in `receipts/prior/`.

| Prior ID | Disposition | Evidence |
|---|---|---|
| R632-1-F1 BLOCKER (REV and REV+E docs-only) | RESOLVED | `probe_scope.py` (sha256 `3e18e600…`) unchanged at its hard-coded round-1 head still shows the original defect, as it should historically. Its unchanged functions, rebound to this head through R632-2's unchanged wrapper, give REV and REV+E `rtl=true` in all three bodies. B16 at its landed merge gives 2 docs paths and `rtl=false`, with two-dot counts of 65 and 64 (`r632-1-probe-*`). |
| R632-1-F2 MINOR (contract bindings in prose) | RESOLVED | `CI_WORKFLOWS.md:676-705`, `:792`, `:892-894` and `:964-966` match `DECIDE_STEP_ENV` (`ci_events.py:397`), `FAST_SCOPE_STEP_ENV` (`:1298`) and the elaborate carrier. `ci_events --check` passes. |
| R632-1-F3 / R632-2-S1 SUGGESTION (history wiring) | RESOLVED | `act_ci.py:6453-6474`. R632-3 mutation R01 fails both runner forms (`mut-R01_*`). |
| R633-1-D1 RESIDUE | RESOLVED | Same passages as R632-1-F2. |
| R633-2-F1 MAJOR (flat isolated install) | RESOLVED | Flat form PASS, 564 ok (`gates/act_ci-selftest-flat`). |
| R633-2-D1 RESIDUE (stale publication wording) | RESOLVED for its sentence; the same class recurs as R632-4-R1 | PR body. |
| R632-2-F1 MINOR (ambient Git in fixtures) | RESOLVED | `ci_scope_history.py:18-45`, `act_ci.py` `scope_fixture_environment`. R632-3's unchanged `hostile_env_check.sh`: both runs PASS and the victim `.git` bytes are unchanged. R633-3's `environment_probe.py`: PASS. |
| R632-2-F2 MINOR (replay set differs from hosted) | RESOLVED | `probe_r632_2.py` unchanged reports 3 MISS, all `identical-on-dev`, where hosted equals replay equals `false`. Its old oracle wanted a replay superset, which the round-3 decision retired. R633-3's `recheck_prior.py round2`: PASS, 39 pairs. `rename`: PASS. |
| R632-2-R1 RESIDUE | RESOLVED | `CI_WORKFLOWS.md:231-233`, `elaborate.yml:80-81`. |
| R632-2-S2 / R632-3-S1 SUGGESTION (merge-shape guard) | RETAINED as S1 | See above. |
| R632-3-F1 MINOR (sibling-import control coverage) | RESOLVED | `docs.yml:389-395`, `act_ci.py:6477-6508`. R632-3 mutations R01, R02 and R03 each fail both the ordinary and flat forms (`mut-*-{ordinary,flat}`). My own planted import in a different unrelated function fails the exact CI step. |
| R632-3-R1 RESIDUE (TESTING.md fail-safe sentence) | RESOLVED | `TESTING.md:1417-1418` now reads "an empty diff comes back RTL-relevant, and on a pull request an unresolvable revision or merge base fails the scope step". |
| R632-3-R2 / R633-3-R1 RESIDUE (duplicate `Closes #734`) | RETAINED | Live PR body. |

R632-3's unchanged `build_real_lanes.sh` with `probe_r632_3.py`, on real history with `R=49da9fd9`, `DEV=a0f39ad4` and `HEAD=59354ffe`, gives:

- B16 at its landed merge, and composed on its recorded base: 2 docs paths, `false`.
- B16 against current dev: empty, `true`.
- This PR against dev: relevant.
- REV, REV+E and evil-merge on real commits: `KL_link_guard.sv` listed, `true`.
- Dev reverted D while the lane kept D: docs only, which is correct because landing changes no RTL.
- Docs-only on a stale base: `false`.
- The own-RTL lane conflicts with E: hosted would not run, and replay refuses with rc 1.

Hosted equals replay in every row. R633-3's `independent_scope.py`: PASS, 81 selector executions, with the B16 counts reproduced.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #734 acceptance 1-5 and the round 2-4 decisions, checked against `rtl.yml:97-139`, `rtl-fast.yml:35-75`, `elaborate.yml:83-115`, `docs.yml:389-395`; `act_ci.py:2376` `build_event` and `:6416` `selftest_scope_event` (stale-base docs is docs-only in hosted and replay). Hosted `changes` log at this head; merge-ref shape (`receipts/merge-ref-735.txt`); B16 real-object reproduction; REV/REV+E. | R632-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |
| RTL | CLEAN | CI and runner architecture: `act_ci.py:1822-1909` live-base fetch and verification unchanged, the payload unchanged apart from its docstring, the trust boundary unchanged, the flat install with no sibling import. `ci_events.py` canonical scope scripts and `ACT_CI_SELFTEST_SCRIPT` (`:694`). No HDL, firmware, configuration or synthesis input in the diff; gitlinks unchanged; five linked images byte-identical base to head (`receipts/image-comparison.json`). | R632-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |
| Robustness | CLEAN (S1 retained, optional) | `probe_r632_4.py`: C1-C17 including deletion, rename-out, mode-only, quoted path, conflict-kept RTL, buried RTL, doc-shaped gitlink, empty delta, criss-cross and conflict refusals, and push fallback. `ci_scope_history.py:195-266`. Hostile environment re-checks (R632-3, R633-3). | R632-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |
| Tests | CLEAN | `ci_scope.py:500-527` with `ci_scope_history.py:268-353` (197 assertions); `act_ci.py:6416-6508` (566 and 564); `ci_events.py:6424-6452` and the docs arms (2860). My 27 killed mutations; R632-3 R01-R03 in both forms; the planted unrelated-function import failing the exact CI step. | R632-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |
| Docs | CLEAN (RESIDUE R632-4-R1 and R632-3-R2/R633-3-R1 carried) | `CI_WORKFLOWS.md:168-213` (rule, frozen-base hazard, why it is safe: candidate builder and native banks before every merge), `:228-236`, `:674-705`, `:792`, `:892-894`, `:1545-1561`, `:1600-1608`; `TESTING.md:1414-1421`; the `build_event` docstring; the `elaborate.yml:77-82` comment; the PR body. Documentation gates rc 0. | R632-4 | 59354ffe75697e17a16fd117d9ba853e104394bc |

## Real limits

- **No act or Docker.** The replay's selection of its branch depends on the replay tool setting `ACT=true`. That is the tool's documented behaviour, and I did not execute it.
- **Sandbox, not a CI job container.** The runner self-tests and the exact CI step ran in an unprivileged namespace sandbox.
- **Hosted runs were incomplete.** The hosted contexts at this head were still running; I read only the `changes` scope log. The new flat step in hosted `docs-check` had not finished when I read it.
- **Merge-ref shape verified once.** It was verified on PR #735 only, a fast-forwardable head.
- **No manager source bank** at this head is claimed or inferred.
- **No physical calibration was run.** Desk image comparisons are not hardware proof.
- **Unchanged prior probes carry observational mismatches by design.** R632-1's probe is hard-coded to the round-1 head, and R632-2's carries the retired superset oracle. Their dispositions above use the rebound and re-graded forms.
- **My own probe needed three corrections.** Two fixture-construction errors were mine. A first complete run let MC2 survive because no fixture pointer was documentation-shaped, so C3b was added. The shipped classifier was not at fault, and the receipts are from the final run.
- **Receipts are lightly redacted.** Local account names in `ls -l` lines were replaced by `<user>`.

## Pending manager duties

- Publish this report.
- Run the trusted live-dev runner replay for this head (bootstrap rule).
- Accept the hosted contexts at this exact head: `docs-check`, including the new flat step; `rtl-fast`; `elaborate`; `verilator-suites`; `yosys-portability`.
- Build the current-dev candidate and run its builder and native banks at the merge turn.
- Keep the stated sequencing: merge after 697c, then 696.
- Carry the two RESIDUE items to the residue checklist.
- Decide on S1 and on the elaborate-step observation.
- Run post-merge containment, then close the Issue.

R632-4 FINISHED

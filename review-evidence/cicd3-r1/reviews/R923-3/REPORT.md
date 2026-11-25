[R923] POSITIVE - exact head b0f2bc1a784d9f006204491c883ac2b1783e970a

# R923-3: internal independent re-review of PR #1003 (Relates to #998)

- Round: R923-3, internal cleared-context review. This is the third round by this reviewer identity, and it is a narrow re-review.
- Head: `b0f2bc1a784d9f006204491c883ac2b1783e970a`, tree `bb0c6d59a6e22c499de562a642978b73c998c653`.
- Source base: `fcbc31f3807a2a7353ab19bfe5aa7f3e56e58c0f` (the head of #1001, since merged). Live `dev`: `e275d7950ef3385753e6a15d2e191ba855b171ed`.
- Delta judged: `9c625393..b0f2bc1a`, three commits (`468c7e47`, `222362ff`, `b0f2bc1a`), 11 files, +48 −25.
- Code outside the delta keeps its R923-2 lens verdict unless the delta changes what it depends on. The delta touches:
  - the capture matrix's `strategy`;
  - two follow_ring recipe lines;
  - comments and prose.
  It changes no RTL, no firmware, no test expectation, no figure and no deal.

## Verdict

**POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head.

- **R924-2-F1 is RESOLVED.** The capture matrix keeps `fail-fast: true`. Four artifacts changed together:
  - the template;
  - the generated workflow;
  - the contract constant;
  - its regression arms.
  A planted disabled or defaulted configuration fails the contract check. So does a template or workflow edited alone.
- **R923-2-F1 is RESOLVED.** Both follow_ring fine-build lines start with `+`.
  - `make -n run` is byte-identical to the base's again.
  - The pipe-jobserver probe prints no warning at the head. It printed 1 at `9c625393`.
  - `exec-pullin-small` still rebuilds nothing.
- **The residues R924-2-R1, R924-2-R2 and R923-2-R1 are APPLIED.** No added comment line carries a lane label, round, reviewer ID or comment ID.
- **Hosted runs at the exact head:** all four workflows succeeded on attempt 1. Every job this PR touches finished within 30 minutes.
- Recorded below: one new wording RESIDUE (R923-3-R1) and the suggestions. None of them affects the verdict.

## Findings

No BLOCKER, MAJOR or MINOR finding.

### RESIDUE (wording only; changes no figure, code, test or verdict)

- **R923-3-R1 - RESIDUE - Docs - `sw/firmware/ctrl/README.md:631`.**
  - Today: "Those standalone builders run in firmware-boundary-capture; firmware-boundary still runs its owned image builders, the stack gate and controls, then judges the joined captures."
  - Problem: the sentence is R924-2-R2's text, applied verbatim, and it is accurate. Per `ctrl_runs.py:5-31`, the owned image builders and the stack gate run in the judge, and every other builder runs in the legs.
    - But the README never introduces "standalone": the word is `ctrl_runs.py`'s. So "Those" has no antecedent. Its nearest candidate is the previous line's "those that need Verilator", which is the wrong set.
    - The job names are also not in backticks, though the README backticks them on the next line.
  - Exact fix: "The standalone builders (`ctrl_runs.py`: every builder but the owned image builders) run in `firmware-boundary-capture`; `firmware-boundary` still runs its owned image builders, the stack gate and the controls, then judges the joined captures."

### SUGGESTIONS (optional)

- **S1 to S4 are retained from R923-2. The author did not adopt them, which is allowed.**
  - S1: `ci_make_cases.py` serial order under `MILAN_COUNTER_FRAME_OUT`.
  - S2: least-privilege `permissions: {contents: read}` on `verilator-preflight` and `firmware-boundary-capture`.
  - S3: the preflight's "beside the workers" benefit needs free runners.
  - S4: publish the derivation walls at full precision.
- **S5 (new):** `docs/testing/CI_WORKFLOWS.md:124` says "as every hosted matrix does (below)". The rule it points to is about 2360 lines further down, at `:2484`. Name the section or link it, instead of writing "(below)".
- **S6 (new):** the `ctrl_boundary.py:79-80` reflow leaves a two-word line ("stack's own gate, its"). Re-fill the paragraph. This is cosmetic.
- **S7 (new; tracked by #1008, not this PR):** at this head the rtl-fast "Fail fast across this head" watcher ran 110.9 minutes against its `timeout-minutes: 120` (`.github/workflows/rtl-fast.yml:1690`).
  - Almost all of that time was runner queueing. `firmware-boundary-capture (1)` started 34.5 minutes after leg 0 (`receipts/hosted/jobs-45550366444.tsv`).
  - #1008 exempts the watchers by design. The headroom is now 9 minutes, so #1008, or the manager's acceptance, should record what a watcher timeout does to the run's conclusion.

## Prior public review findings on this PR

I read R924-2's published findings only after my own pass over the delta and my probes. My own R923-2 report is this identity's output.

| Finding | Status at `b0f2bc1a` | Evidence |
|---|---|---|
| R924-2-F1 MINOR (Conformance, Robustness, Tests, Docs): the capture matrix disables the fork-safe native cancellation | **RESOLVED** | Details in the next table. |
| R923-2-F1 MINOR (Conformance, RTL, Robustness, Tests, Docs): follow_ring's fine build was not a recursive make line | **RESOLVED** | `tb/verilator/follow_ring/Makefile:133` `+$(if $(LEG_BUILD),$(FINE_BUILD))` and `:158` `+$(FINE_BUILD)`; the comment at `:95-99` states the reason. Probe results are in the table after next. |
| R924-2-R1 RESIDUE: attribution missing on the new explanatory blocks | **APPLIED** | All 13 listed blocks now end `Issue #998; REQ-VER-01 and REQ-VER-04.` (13 added lines, `receipts/gates/comment_rule_scan.txt`): `Makefile:95-99`, `small_pulls.py:77-78`, `settle_control.py:181-182`, template `:566-576`, `ctrl_boundary.py:79`, `ctrl_configs.py:111`, `ctrl_runs.py:31-32`, `ci_events.py:270-271`, `:1362-1363`, `:2267-2268`, `:2614-2615`, `:3890-3893`, `:8410`. REQ-VER-01 and REQ-VER-04 exist (`REQUIREMENTS.md:326`, `:333`). |
| R924-2-R2 RESIDUE: README "That job runs no builder itself" | **APPLIED** verbatim | `sw/firmware/ctrl/README.md:631`. Its twin in `docs/testing/CI_WORKFLOWS.md:121` now reads "runs none of their builders itself". That is correct: the judge runs `owned()` and `stack_gate()`, per `ctrl_runs.py:5-17`. The verbatim text leaves an antecedent residue, R923-3-R1. |
| R923-2-R1 RESIDUE: "is recorded on #998" | **APPLIED** verbatim | `docs/testing/CI_WORKFLOWS.md:651` |
| R923-2-S1 to S4 | Retained as S1 to S4 | — |

**R924-2-F1 evidence:**

- **The four artifacts changed together:**
  - `.github/ci-templates/rtl-fast.yml:583` and the generated `.github/workflows/rtl-fast.yml:1154` both read `fail-fast: true`;
  - `scripts/ci_events.py:1366` sets `FIRMWARE_BOUNDARY_STRATEGY` with `"fail-fast": True`;
  - the arms at `:8416` ("cancellation disabled", `False`) and `:8419` ("left to the default", key removed) both expect the strategy finding.
- **Planted configurations** (`scripts/cancellation_plant_probe.sh`, `receipts/gates/cancellation_plant_probe.txt`; render check, then contract check):

  | Planted configuration | Render check | Contract check |
  |---|---|---|
  | Control (unchanged) | rc 0 | rc 0 |
  | `false` in both files | rc 0 | rc 1, strategy item |
  | Key removed from both files | rc 0 | rc 1, strategy item |
  | `false` in the template only | rc 1 | rc 1 |
  | `false` in the workflow only | rc 1 | rc 1, generated-jobs item |

- **Self-test:** `ci_events.py --selftest` PASS, 2378 items and 5968 arms. That is one arm more than at `9c625393`. All 7 boundary-leg arms are caught (`receipts/gates/ci_events_selftest.log:2866-2872`).
- **Why a failed fork leg cancels its sibling without a write token:**
  - `strategy.fail-fast` is applied by the Actions service to the matrix itself, so it needs no job and no token.
  - The only write-token job, `ci-fail-fast` (`permissions: actions: write`), is still guarded to `push` and same-repository `pull_request` (`rtl-fast.yml:1691-1692`, unchanged by the delta).
  - After a leg fails, the matrix's `needs` result is `failure`. So `firmware-boundary` is skipped. The aggregate (`if: always() && !cancelled()`, `:1506`) still runs, and its `case` (`:1582-1585`) rejects anything but `success` or `skipped`. The capture result fails the aggregate.
  - The watcher counts a cancelled sibling as a failure (`scripts/ci_fail_fast.py:26`), so a same-repository run is also stopped.
  - No hosted leg failure was injected. That limit is listed below.

**R923-2-F1 evidence** (`scripts/follow_ring_make_probe.sh`, re-run with `b0f2bc1a78` added; GNU make 4.4.1; `receipts/cases/follow_ring_make_probe.txt`):

| Tree | `make -n run` vs the base `13e6d869` | Jobserver warnings under `-j4 --jobserver-style=pipe small-pullin` | `make -n exec-pullin-small` rebuild lines |
|---|---|---|---|
| `13e6d869` (base) | — | 0 | (no such target) |
| `9c625393` | DIFFERS | 1 | 0 |
| `b0f2bc1a` | **IDENTICAL** | **0** | **0** |

At the head:

- `make -s ci-list` prints `b8 pullin-small bind-settle` (`receipts/cases/follow_ring-ci-list.txt`).
- Both CI pieces ran in a disposable shared clone at the head with the pinned Verilator 5.050, under `MAKEFLAGS=-j1`:
  - `--shard 0/2`: rc 0, 372 s.
  - `--shard 1/2`: rc 0, 489 s.
- Their three case digests (`receipts/cases/follow_ring-piece-digests.txt`) equal the author's published local receipts for `b0f2bc1a`, digit for digit. The author's packet reports those as equal to the `9c625393` local receipts and to hosted run 45528738040's.

## Hosted evidence at the exact head (Actions API, read-only)

All four runs succeeded on attempt 1, `pull_request`, created 2026-11-25T04:58:37Z: rtl-fast 45550366444, rtl-full 45550366428, elaborate 45550366332 and docs 45550366343 (`receipts/hosted/runs-b0f2bc1a.tsv`).

Minutes are `completed_at − started_at` (`receipts/hosted/job-minutes-b0f2bc1a.txt`, from `scripts/job_minutes.py`).

**Jobs this PR touches (all within 30 minutes):**

| Job | Minutes |
|---|---|
| `firmware-boundary-capture (0)` | 15.3 |
| `firmware-boundary-capture (1)` | 11.0 |
| `firmware-boundary` | 5.0 |
| `rtl-fast` aggregate | 0.3 |
| Verilator preflight | 1.9 |
| Slowest Verilator worker (shard 2/26) | 25.0 |
| Unions | ≤ 0.5 |
| `verilator-suites` | 0.5 |

**Untouched jobs over 30 minutes (tracked in #1008):**

| Job | Minutes |
|---|---|
| `publication-census` | 36.7 |
| `firmware-srp-mutants` | 30.5; #1008 lists it at 1377 s |
| `firmware-control-mutants` | 30.1 |
| The two "Fail fast across this head" watchers | 110.9 and 90.9; #1008's by-design exception; see S7 |

These figures match the author's published `minutes-b0f2bc1a.tsv` summary.

## Lens coverage at `b0f2bc1a784d9f006204491c883ac2b1783e970a`

```text
[R923] PASS Conformance - .github/ci-templates/rtl-fast.yml:573-583, .github/workflows/rtl-fast.yml:1154, :1506-1585, docs/testing/CI_WORKFLOWS.md:2484, tb/verilator/follow_ring/Makefile:92-99,133,158, receipts/cases/make-n-run.*.txt - the capture matrix now meets the hosted-matrix fail-fast rule (#998 scope: the cancellation contract is unchanged); #998 acceptance 1's serial-run claim ("make -n run is the same") holds against base 13e6d869; acceptance 2's bound holds for every touched job at the exact head (hosted jobs API)
[R923] PASS RTL - delta file list (no hdl/ file) and tb/verilator/follow_ring/Makefile:133,158 interface contract - no RTL changed; the suite's make interface (ci-list inventory, exec-% no-rebuild contract, recursive-make and jobserver behaviour) matches the base, per the probe receipts and the two pieces' case digests
[R923] PASS Robustness - receipts/gates/cancellation_plant_probe.txt, rtl-fast.yml:1691-1692 (fork guard), scripts/ci_fail_fast.py:26, receipts/cases/small-pullin-pipe.*.txt - failure path: a failed leg cancels its sibling natively on every event, and the aggregate fails closed; disabled, defaulted and one-file-only cancellation edits are all refused; under a pipe jobserver the fine build keeps the jobserver (0 warnings); an empty LEG_BUILD leaves a bare '+' line, which rebuilds nothing
[R923] PASS Tests - scripts/ci_events.py:8410-8422, receipts/gates/ci_events_selftest.log:2866-2872, receipts/gates/plant-*.log - the replaced arm and the two new arms are caught at the head, and each can fail for its defect (my plants of the same configurations fail the real check); ci_events --check and ci_gate_workflows --check rc 0; check_py_idiom, check_doc_style and check_doc_paths rc 0; both follow_ring pieces pass with digests equal to the published ones
[R923] PASS Docs - docs/testing/CI_WORKFLOWS.md:121-125,651, sw/firmware/ctrl/README.md:631-632, the 13 attribution lines, the live PR body (head b0f2bc1a: items 10-11, the disposition table, the fail-fast mechanism section), receipts/gates/comment_rule_scan.txt - the changed contracts are stated where they are enforced; the prior residues are applied; no lane, round, reviewer or comment ID appears in any added line; one wording RESIDUE (R923-3-R1) is carried and leaves the lens clean
```

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #998 acceptance 1-2 and the rulings from R923-2; capture-matrix `strategy` in the template and the workflow; aggregate result logic; CI_WORKFLOWS.md:2484 rule; follow_ring `make -n run` vs base; hosted jobs at head | R923-3 | `b0f2bc1a784d9f006204491c883ac2b1783e970a` |
| RTL | CLEAN | no `hdl/` in the delta; follow_ring Makefile interface (recursive lines, `exec-%`, `ci-list`); pinned-Verilator piece builds | R923-3 | `b0f2bc1a784d9f006204491c883ac2b1783e970a` |
| Robustness | CLEAN | five-way cancellation plant; fork guard; watcher cancelled-as-failure; pipe-jobserver probe; empty `LEG_BUILD` path | R923-3 | `b0f2bc1a784d9f006204491c883ac2b1783e970a` |
| Tests | CLEAN | `ci_events --check` and `--selftest` (5968 arms); `ci_gate_workflows --check`; boundary-leg arms; style gates; follow_ring pieces 0/2 and 1/2 with digest equality | R923-3 | `b0f2bc1a784d9f006204491c883ac2b1783e970a` |
| Docs | CLEAN (RESIDUE R923-3-R1 carried) | CI_WORKFLOWS.md:121-125, :651; ctrl README:631; 13 attribution lines; live PR body; comment-rule scan | R923-3 | `b0f2bc1a784d9f006204491c883ac2b1783e970a` |

## Real limits

- No hosted capture-leg failure was injected. Native fork cancellation is argued from these:
  - the Actions `strategy.fail-fast` semantics;
  - the exact contract check and my plants;
  - the unchanged watcher guard.
  It is not observed.
- I did not run these:
  - a full source bank;
  - the serial follow_ring `run` sweep;
  - an act replay;
  - make 4.3.
  The author reports make 4.3 as also 0 warnings and IDENTICAL; I did not reproduce that. My pipe probe uses 4.4.1's `--jobserver-style=pipe`, which is the same pipe protocol.
- `check_em_dash.py` could not judge here: the pinned Markdown renderer is not installed, and I made no shared install. The author's packet carries its receipt.
- Physical calibration was NOT RUN. Field skips are not hardware proof.
- The author's open note stands. `ci/image/tool-inventory.json` and `exec-audit-receipt.json` still name `firmware-boundary`'s old step indices. The delta does not touch them, so they keep their R923-2 standing.
- The clone was restored and verified:
  - the index tree equals `bb0c6d59…`;
  - the status is empty, including ignored files;
  - all six gitlinks equal HEAD's.

## Pending manager duties

- Build and validate the current-dev merge candidate. The source base is `fcbc31f3`; live `dev` is `e275d795`. Link the builder and native bank receipts.
- Accept the hosted/act evidence at the exact head.
- Carry R923-3-R1 to the residue checklist.
- Decide S7's watcher-timeout headroom under #1008.
- Obtain the external positive review. This internal POSITIVE is one of the two required.

R923-3 FINISHED

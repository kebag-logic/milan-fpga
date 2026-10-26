[R705] POSITIVE - exact head 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0

# R705-1: internal cleared-context review of PR #788 (issue #784, step 2)

- Head `847eb4dd031eb3891b61773f4a8324cb2ed6cdc0`, tree `05ae0179dbffa852651aa7ec8367758b380672d0`. One commit on dev `a8594bb95631fa5c49d18fa0bbc9530e31ad59aa`, 20 files, +179/-164.
- Reconstructed in this order: AGENTS.md, CONTRIBUTING.md, docs/README; #784 body (Decision, Acceptance step 2); the step-2 assignment (#784 issuecomment-6409728491); the ruleset comment (6400810252); the author's TAKEN and REVIEW READY comments; R697-1-01's exact wording fix on PR #785; then the diff, then executable evidence.
- The author's public evidence is at `review-evidence/784s2-r1` on `042bf69d`: 227 manifest entries covering gates on both interpreters, mutants, bootstrap and census. I fetched `census.md` and `imageos-readers.md`, and their sha256 values match the manifest. The author's census agrees with mine, which I produced independently. My execution evidence is my own reruns, not the author's logs.
- The verdict, findings and ledger below were written before I read any other review of PR #788 (see "Prior public findings" at the end).
- No open BLOCKER, MAJOR or MINOR. One RESIDUE, one SUGGESTION.
- The hosted acceptance item (every required check green) is **not yet met** at this head. The cause is a cold-cache timeout that predates this change (see R705-1-02 and the pending manager duties).

## Findings

### R705-1-01: RESIDUE (Docs)

- **Where:** `docs/testing/TESTING.md:331`, "used a hosted `ubuntu-latest` runner, then the `ubuntu-24.04` image, and sequential `make -C` invocations."
- **Evidence:** the job ran once. Job 113696564335 (run 37892515345, head `8e4b1e53`) has the label `ubuntu-latest`, and its set-up log line `2026-10-09T06:15:18Z Image: ubuntu-24.04` names the image that label resolved to (`receipts/historical-job-images.txt`). "then" makes the image read like a second step after the runner.
- **Impact:** wording only. Both facts are correct, and no figure, window, verdict or test depends on the sentence.
- **Exact fix:** "used a hosted `ubuntu-latest` runner, which resolved to the `ubuntu-24.04` image, and sequential `make -C` invocations."
- **Verification:** reread the line against the job log, then run `check_em_dash.py --base a8594bb9`, `check_doc_style.py` and `docs_check.py`.

### R705-1-02: SUGGESTION (Robustness, Conformance). A predating defect for a new Issue, outside this delta

- **Where:**
  - `.github/ci-templates/rtl-fast.yml:134-138` / `.github/workflows/rtl-fast.yml:254-258`: `yosys-elaboration` has `timeout-minutes: 30`.
  - `.github/ci-templates/rtl-fast.yml:153`: its Yosys cache key hashes `.github/workflows/*.yml`.
  - This delta changes neither line.
- **Evidence** (`receipts/hosted-cancel-cause.txt`, `receipts/yosys-elaboration-history.tsv`):
  - Every workflow edit misses that cache.
  - At this head, job 121450772865 shows `Cache not found for input keys: yosys-v0.66-...-Linux`. The cold build ran 07:32:00 to 07:48:33, and the job was cancelled at 08:02:01, 30 minutes after it started.
  - The `ci-fail-fast` watcher then reported `{"first_failure": "yosys-elaboration", "conclusion": "cancelled"}` and cancelled all four runs (`Cancelled runs: [40286249776, 40286249788, 40286249845, 40286249749]`).
  - The same cold-build cancellation happened at `43a25fa7` (run 38794077148), an earlier head that changed `rtl-fast.yml`.
  - A warm-cache run at `d385b38e` (run 40187422747) took 11.5 minutes and passed.
- **Impact:**
  - The first hosted run of any head that touches a workflow cannot make `rtl-fast` green.
  - Here, that cascaded into a cancelled `rtl-fast` and failed `verilator-suites` and `yosys-portability`.
  - The image move itself caused no failure. All 62 jobs that ran report `Image: ubuntu-24.04`, and the pip installs that failed on 26.04 now pass.
- **Optional outcome:** a new Issue for the cold-cache budget of `yosys-elaboration`. Not required for this PR: the template timeout and key are unchanged, and the defect is not in this delta.

## Lens results (clean-lens format, at the exact head)

- **[R705] PASS Conformance** — `.github/workflows/*.yml` (46 jobs), `.github/ci-templates/*.yml` (22 jobs), the three `runs-on` generators, and the label checks in `scripts/act_ci.py` (lines 92, 2061-2066 and 4828). Checked against #784 Decision/Acceptance step 2 and assignment items 1-5:
  - **Census** (`receipts/census-ubuntu-latest.txt`, `receipts/census-labels.txt`). Exactly three modules write a `runs-on` value: `scripts/ci_gate_workflows.py:165`, `scripts/ci_runtime_workflows.py:127,145,159` and `scripts/ci_suite_workflows.py:44,76`. All emit `ubuntu-24.04`. `ci_gate_workflows.py` is the only entry point that writes `.github/workflows/`. `yosys_shards.py` and `ci_install_workflows.py` write no label.
  - **No `ubuntu-latest` left where the assignment forbids it.** `git grep ubuntu-latest` at the head finds it nowhere in `.github/`, the templates or the generators. The only hits are:
    - the deliberate refusal arms and the reason comment in `act_ci.py`;
    - the policy prose in `CI_WORKFLOWS.md`;
    - `TESTING.md:331` and two Makefile comments, which record the label of past run 37892515345.
  - **Every job is on the label.** Each of the 46 jobs, parsed with BaseLoader, has `runs-on == 'ubuntu-24.04'`.
  - **Runner.** `RUNS_ON_LABELS = ("ubuntu-24.04",)` is the only source for both the sandbox check and the `--platform` words. `ubuntu-latest`, `ubuntu-26.04` and `ubuntu-22.04` are refused by name.
  - **R697-1-01.** The exact sentence is present once, whitespace-normalised, and the old sentence is gone (`receipts/r697-1-01-verbatim.txt`).
  - **Hosted evidence.** Every executed job shows `Image: ubuntu-24.04`. The "every required check green" item is not yet met; it is recorded under pending manager duties, not as a defect of this head.
- **[R705] PASS RTL** — artifact `receipts/full.diff` (file list) and `scripts/act_ci.py:5975-6000`.
  - No HDL, CDC, FSM, width or interface artifact is in the delta, so the hardware side does not apply.
  - On the architecture side, `run_validation` still runs `validate_workflow_sandbox` before job-volume scope, CPU ranges, submodules and the Docker boundary.
  - The generator architecture is unchanged: the workflows are pure products of the templates and generators (`receipts/regeneration.txt`, B).
- **[R705] PASS Robustness** — artifacts `receipts/runner-mutants/summary.txt`, `receipts/bootstrap-probe.txt`, the label-variant arms at `scripts/act_ci.py:6719-6738`, and `receipts/tree-mutants/summary.txt`:
  - **Refused labels.** The sandbox refuses each of the following, and the arms prove it under mutation:
    - `ubuntu-latest`, `ubuntu-26.04` and `ubuntu-22.04`;
    - `Ubuntu-24.04`, `ubuntu-24.04-arm` and `[ubuntu-24.04]`;
    - `self-hosted`, a missing label, and `${{ matrix.os }}`.
  - **Refusal order.** A refused label stops before any Docker boundary or act command (the replay arms at `:6809-6832`).
  - **Bootstrap, offline function call only.**
    - dev's trusted `act_ci.py` (blob `904d4fda`, labels `ubuntu-latest`, `ubuntu-24.04`) accepts all head workflows, so this PR's act replay can run on the trusted runner.
    - The head runner accepts the head workflows and refuses dev's workflows, naming `wire-accountability runs on 'ubuntu-latest'`.
  - **Gate coverage.** Every tree mutant is caught by at least one gate in the required docs job:
    - a template or generator job put back on `ubuntu-latest`/`ubuntu-26.04` and regenerated is caught by the contract gate's shipping-workflows arm;
    - not regenerated, it is caught by the generator check and `ci_events`;
    - a hand-edited workflow is caught by all three;
    - the physical contract is caught by `ci_events`.
  - The cold-cache timeout is recorded as R705-1-02, outside the delta.
- **[R705] PASS Tests** — artifacts `scripts/act_ci.py:6719-6832` and `:13275-13366`; `receipts/gates-py314/` and `receipts/gates-py312/` (35 gates each, all rc 0); `receipts/runner-mutants/` (control rc 0, plus 10 own mutants, all rc 1 with named FAILs); `receipts/tree-mutants/`:
  - **`act_ci.py --selftest`** reports 623 ok / 0 FAIL, and the 0555 flat-install contract gate reports 621 ok / 0 FAIL, on CPython 3.14.8 + PyYAML 6.0.3 and on CPython 3.12.13 + PyYAML 6.0.2.
  - **`ci_events`.** `--check` covers 2199 items and `--selftest` 5236 arms.
  - **Generator.** `ci_gate_workflows.py --check` and its self-test pass, and so do the other 12 CI scheduling and evidence controls.
  - **Mutants I planted.** Each is killed by a named arm:
    - re-admit `ubuntu-latest`: 3 FAIL;
    - `ubuntu-latest` only: 8;
    - drop the platform entry: 3;
    - platform names the wrong label: 3;
    - platform maps to the `node:16` image: 3;
    - the sandbox also admits `ubuntu-latest`: 3;
    - the sandbox admits any `ubuntu-` prefix: 7;
    - the label check removed: 12;
    - a refusal that does not name the label: 8;
    - the container refusal deleted: 2.
  - **Reason fragments.** The sandbox-policy arms now require their own reason fragment. Without that, a fixture on a refused label would pass a Refusal-only arm vacuously; the container-refusal mutant proves the strengthened arm discriminates.
  - **Fixtures.** No fixture is left on a refused label: the census of `act_ci.py` finds `ubuntu-latest` only in the deliberate arms.
  - **Hosted.** `docs-gates-2` ran the same self-test and contract gate on `ubuntu-24.04`, reporting `selftest: PASS` with the four named arms ok (`receipts/hosted-docs-gates-excerpt.txt`).
- **[R705] PASS Docs** — artifacts:
  - `docs/testing/CI_WORKFLOWS.md:7-13`, `:565` and `:2036-2048`;
  - `docs/testing/TESTING.md:174` and `:331`;
  - `tb/verilator/milan_dp/README.md:355`, `tb/verilator/milan_dp_gptp/README.md:27`, `sw/firmware/gtest/README.md:442`, `scripts/yosys_shards.py:21`;
  - the docs gates in `receipts/gates-py31{2,4}/`.

  What I checked:
  - **The pinned image and the reason.** `CI_WORKFLOWS.md` states the image and why: hosted `ubuntu-latest` moved to 26.04, and the pinned CPython 3.12 wheels (`ci/constraints-ci.txt:1`, cp312 PyYAML 6.0.2) do not install there. `TESTING.md` names the label where it describes the current job.
  - **The historical images**, against public job logs:
    - 113696564335 shows `Image: ubuntu-24.04`;
    - 96546610543 shows `Image: ubuntu-24.04` with noble `yosys 0.33-5build2`;
    - 121179871493 shows `Image: ubuntu-26.04` and `ResolutionImpossible`.
  - **Stale wording.** No two-label sentence is left from step 1.
  - **Gates.** `docs_check`, `check_em_dash --base a8594bb9` (26 added lines, 0 findings), `check_doc_style`, `gen_toc` (`--selftest`, `--verify-anchors`, `--check`), `check_doc_paths`, `check_archive`, `check_baremetal_only`, `check_feature_status`, `DOC_MAP.gen.py --check` and `check_gptp_docs` all pass.
  - **Comment rule.** Scanning the 178 added lines for lane labels, review rounds, reviewer IDs and comment IDs gives 0 matches (`receipts/comment-rule-scan.txt`).
  - The only defect is the wording in R705-1-01 (RESIDUE).

## Brief checks (1) to (5)

1. **Generators and regeneration:**
   - My census finds three `runs-on` writers, all on `ubuntu-24.04`.
   - Regenerating at the head leaves a scratch copy clean (0 status lines).
   - Exporting dev `a8594bb9`, substituting only the label in its 4 templates and 3 generators, and regenerating gives **byte-identical** copies of all four head workflows. The head templates equal that substitution, except one `rtl.yml` comment, which no longer names the label (`receipts/regeneration.txt`).
2. **Runner:**
   - Only `ubuntu-24.04` is accepted. `ubuntu-latest` and every other label are refused by name.
   - `act_ci.py --selftest` and the contract gate pass.
   - My mutants (re-admit `ubuntu-latest`; drop the platform entry; and 8 more) are all killed.
3. **`ci_events` and workflow behaviour:**
   - `ci_events.py --check` and `--selftest` pass.
   - The workflow diff against dev is exactly 46 `-runs-on: ubuntu-latest` / `+runs-on: ubuntu-24.04` line pairs and nothing else, with no generator-recorded digest (`receipts/workflows.diff`).
   - `generate_ci_evidence_pins.py --check` passes.
4. **Docs:** see Docs above. R697-1-01 is applied verbatim. One RESIDUE.
5. **Hosted run at this head** (`receipts/hosted-images-final.tsv`, `receipts/required-checks.txt`):
   - All 65 jobs carry the label `ubuntu-24.04`, and all **62 executed jobs** show `Image: ubuntu-24.04`, runner image version `20261012.334.1`.
   - Two cancelled jobs (the `rtl-fast` aggregate and `Yosys shard 2/4`) never started a runner: 0 steps, no set-up log. `Physical gPTP` was skipped by its schedule condition. None of these three is evidence.
   - Required checks: `docs-check`, `wire-accountability`, `docs-check-no-git` and `elaborate` are **success**. `rtl-fast` is **cancelled**. `verilator-suites` and `yosys-portability` are **failure**, because their shard inputs were cancelled by the fail-fast cascade in R705-1-02.
   - So the issue's hosted acceptance item is **not met yet**. The image half is met; the green half is not.

## Reviewer-owned ledger

| lens | state | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | 46 workflow jobs and 22 template jobs; `ci_gate_workflows.py:165`, `ci_runtime_workflows.py:127,145,159`, `ci_suite_workflows.py:44,76`; `act_ci.py:92, 2061-2066, 4828`; `receipts/census-*.txt`; R697-1-01 verbatim check; hosted image census | R705-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |
| RTL | CLEAN | delta file list (no HDL); `act_ci.py:5975-6000` validation order; regeneration equivalence | R705-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |
| Robustness | CLEAN (R705-1-02 SUGGESTION, outside the delta) | label-variant arms `act_ci.py:6719-6738`; `receipts/runner-mutants/`; `receipts/tree-mutants/`; `receipts/bootstrap-probe.txt`; `receipts/hosted-cancel-cause.txt` | R705-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |
| Tests | CLEAN | `act_ci.py:6719-6832, 13275-13366`; `receipts/gates-py314/`, `receipts/gates-py312/` (35 gates each, rc 0); control plus 10 runner mutants killed; 7 tree mutants caught | R705-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |
| Docs | CLEAN (R705-1-01 RESIDUE carried) | `CI_WORKFLOWS.md:7-13, 565, 2036-2048`; `TESTING.md:174, 331`; three READMEs; `yosys_shards.py:21`; historical job logs; docs gates; `receipts/comment-rule-scan.txt` | R705-1 | 847eb4dd031eb3891b61773f4a8324cb2ed6cdc0 |

## Real limits

- **Offline only.** No Docker, act, host act_ci replay, privilege or hardware. The bootstrap probe imported the two runner copies and called only `validate_workflow_sandbox`. The live act replay belongs to the manager.
- **No manager source bank** ran at this head, and I claim none. Source-head execution evidence is my own gate reruns and the author's receipts. The current-dev candidate build is the manager's, at the merge turn.
- **Hosted pair.** My 3.12 environment is CPython 3.12.13 + PyYAML 6.0.2, not the hosted 3.12.3. The hosted `docs-gates-*` jobs on `ubuntu-24.04` cover 3.12.3 for the docs gates (`receipts/hosted-docs-gates-excerpt.txt`).
- **`ImageOS`.** I did not audit the `actions/setup-python@v5` bundle for `ImageOS`, which act sets to `ubuntu24` for this label. The author's public receipt `author/receipts/imageos-readers.md` reports 0 occurrences in `a26af69b`'s `dist/setup` and `dist/cache-save`; I did not reproduce that. In this repository, setup-python is used twice (`elaborate.yml:105` and `:340`, `python-version: '3.12'`, no `cache` input), and no `.github/`, `scripts/` or `ci/` file reads `ImageOS`. Cache keys use `runner.os`. This matters only for the act replay.
- **No Verilator, Yosys or Vivado run.** There is no RTL change, and full banks are not allowed in this round.
- **Physical calibration NOT RUN.** Skipped hosted contexts are not hardware proof.

## Pending manager duties

- **Hosted green at this head.** Re-run the hosted workflows of this head, or obtain an equivalent exact-head green run.
  - The Yosys key `yosys-v0.66-86f2dd...-e3388d3a...-Linux` is now saved on `refs/pull/788/merge` (07:48:36Z, 19.7 MB), written by rtl-full's `Prepare pinned Yosys`. A re-run of `yosys-elaboration` should therefore restore it instead of building.
  - Then confirm `Image: ubuntu-24.04` on every executed job and all seven required checks green.
- **Post-merge dev push run.** It will miss the same keys on `refs/heads/dev`, because PR-ref caches are not visible to dev, so its first `rtl-fast` can hit the same 30-minute cancellation. Plan a re-run after the cache is saved before treating that run as the ruleset-restore evidence (#784 comment 6400810252).
- **Act replay** of this PR on the trusted dev runner. The offline probe shows the trusted runner accepts every head job.
- **Carry R705-1-01** to the residue checklist. Consider a new Issue for R705-1-02.
- **Consequence of merging.** Once this merges and becomes the trusted runner, any open branch whose workflows still say `ubuntu-latest` is refused by name until it merges dev. That is the intended behaviour of #784.

## Prior public findings

I read these only after the verdict, findings and ledger above were written. None of them changes this verdict.

- **On PR #788.** The only prior review is the external review at https://github.com/kebag-logic/milan-fpga/pull/788#issuecomment-6411099737 (POSITIVE at this head). It files **no** BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION, so nothing needs to be resolved or retained at this head (`receipts/pr-comment-index.tsv`). No submitted reviews or inline review comments exist.
- **Its hosted section is a 07:40-07:41 UTC snapshot**, taken before the 08:02 `yosys-elaboration` cancellation and the fail-fast cascade, and it claims no all-green result. My later observation (brief check 5, R705-1-02) supersedes that snapshot as a description of the run's outcome. It does not contradict the snapshot.
- **R697-1-01 (PR #785, RESIDUE, Docs)** is **resolved** at this head. The exact replacement sentence is present once and the old sentence is absent (`receipts/r697-1-01-verbatim.txt`). This agrees with the external review's disposition.

R705-1 FINISHED

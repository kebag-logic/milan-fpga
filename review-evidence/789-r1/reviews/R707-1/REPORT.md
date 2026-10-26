[R707] NEGATIVE - exact head fddf3671ebc96a953755fa1b9a3ecec5f071a350

# R707-1: internal cleared-context review of PR #794 (issue #789)

- **Head:** `fddf3671ebc96a953755fa1b9a3ecec5f071a350`, tree `d758e8963591f123d3398719f0a331f9cc9bbf91`. It is one commit on dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`, changing 5 files.
- **Role:** internal independent reviewer, round R707-1. All five lenses were applied.
- **Verdict:** NEGATIVE. Two MINOR findings are open: R707-1-01 and R707-1-02. There is one SUGGESTION, and no BLOCKER or MAJOR.
- **What works:** the change does what it is for.
  - On this PR's own hosted run, the cold `yosys-tool` built and saved the new key in 16 min 17 s.
  - `yosys-elaboration` restored that exact key in 5 s, ran no build, and passed every check in 10 min 28 s.
- **Why NEGATIVE:** two gaps in what the key and the tests guarantee.
  - **R707-1-01:** the key does not bind every input that changes the built tool. I planted one such edit, and the restore served the old tree.
  - **R707-1-02:** no check holds `yosys-elaboration`'s retained steps after the derivation.

## Findings

### R707-1-01: MINOR (Conformance, Robustness, Tests). The tool key binds only the template build step, so a build-environment edit restores a tree built under the old recipe

- **Where:**
  - `scripts/ci_gate_workflows.py:197-207` (`recipe_digest`, `fast_tool_key`): the digest covers the template's `Build Yosys from source on cache miss` step and nothing else.
  - `scripts/ci_gate_workflows.py:240-260` (`fast_yosys_tool`): the tool job copies the consumer's `needs`, `if` and `runs-on`, but not its job-level `env`.
  - `scripts/ci_gate_workflows_selftest.py:234-260` (`fast_tool_key_inputs`): its docstring says the key follows the recipe and image "and nothing else the template says". It plants only a step-text edit, a recipe edit and an image edit.
- **Authority:**
  - #789 Decision: the key "depends only on the pinned Yosys version, its build recipe and the runner image".
  - Brief check (1): the key includes exactly what changes the built tool, and a restore can never serve a tool built from a different recipe or version.
  - `docs/testing/CI_WORKFLOWS.md` "Source-tool cache provenance": "No fallback restores another version, source, or recipe."
- **Evidence** (`receipts/key_inputs/key_inputs.txt`, `.json`; `scripts/probe_key_inputs.py`): each edit was planted in the head's template or generator in memory. The script then read the generated tool key, resolved as the hosted runner resolves it.
  - **The pristine key** resolves to `yosys-v0.66-86f2ddeb…-recipe-06e5a02f…-ubuntu-24.04-Linux`. That is byte-for-byte the key the hosted tool job saved (`receipts/hosted/tool-job-log-excerpt.txt`).
  - **Edits that change the key:** the pinned version, the asserted source commit, two recipe edits (`ENABLE_PLUGINS`, one more apt package) and the runner image.
  - **Edits that leave it unchanged, as intended:** an edit outside the recipe, and an unrelated workflow env name.
  - **STALE-SERVED, workflow env `CXXFLAGS: -O0`:** the generated tool job's build runs under it, and the key is unchanged. The pinned Yosys Makefile at `86f2ddeb` reads `CXXFLAGS := $(CXXFLAGS) …` at line 107 (`receipts/key_inputs/yosys_makefile_env_lines.txt`).
  - **STALE-SERVED, workflow env `CXXSTD: c++23`:** same result. The Makefile reads `export CXXSTD ?= c++20` at line 106.
  - **STALE-SERVED, generator-side rewrite:** the install-cache transform (`scripts/ci_install_workflows.py:49`) rewrites the build body, and the template stays unchanged. The generated build that runs differs, and the key does not.
  - **The banner records the flags:** the hosted `yosys -V` banner prints the compile flags: `Yosys 0.66 (git sha1 86f2ddebc, g++ 13.3.0-6ubuntu2~24.04.1 -fPIC -O3)` (`receipts/hosted/consumer-job-log-excerpt.txt`). A changed `CXXFLAGS` does change the tool, and the consumer's version proof (`grep -F "Yosys 0.66"`) cannot tell the two trees apart.
  - **What the old key covered:** before this delta, the key's workflow-file digest covered all three inputs.
- **Impact:** a future edit can change how Yosys is built without rebuilding it. Such an edit is a workflow env entry, an export added to the generated job-budget step, or a change to a generator transform of the build body. Every head then silently restores the tree built under the old recipe. A cold rebuild after eviction would produce a different binary under the same key. No such edit exists at this head, so this is latent and not live, hence MINOR.
- **Required outcome:**
  - The tool key's recipe digest covers every input the generated tool job feeds the build. As a minimum, that is the workflow-level `env` and the tool job's own `env`, plus the generated build step as executed (the `ci_packages_<n>` index normalised), or the step together with the transform that produces it.
  - Alternatively, the generator refuses a template or derivation in which such an input lies outside the digest.
  - A job-level `env` on the template consumer is either carried into the tool job and digested, or refused.
  - An edit that changes no build input still leaves the key unchanged.
  - The docs at `docs/testing/CI_WORKFLOWS.md:322-326` and `:3286-3290` state exactly what the digest covers.
- **Verification:**
  - Rerun `scripts/probe_key_inputs.py <export> <out>` on the fixed head: there is no `STALE-SERVED` row, and the "edit outside the recipe" row keeps `key-changed=False`.
  - The selftest plants a workflow-env edit and a generator-side build rewrite, and requires the key to change or the generator to refuse.

### R707-1-02: MINOR (Tests, Docs). Nothing holds `yosys-elaboration`'s retained checks after the derivation; a generator that drops one passes every judge

- **Where:**
  - `scripts/ci_gate_workflows_selftest.py:114-165` (`fast_tool_findings`) and `:308-327` (`fast_tool_controls`) check the consumer's build, need and restore. They require every other job to equal the template, but never the consumer's remaining steps.
  - `scripts/ci_events.py:4414-4429` (`project_gate_templates`) runs the step-list pins on the template projection. The generated jobs are only compared with the generator's own output (`check_generated_workflow`, `:4399-4411`).
  - `docs/testing/CI_WORKFLOWS.md:1157-1162` says every job in the four files "now carries the sequence pin of item 4". `:778-790` says the checker refuses any job of the two RTL files whose whole step list nothing records.
- **Authority:**
  - Brief check (2): `yosys-elaboration` keeps every check it ran before.
  - AGENTS.md section 6, Tests: each test can fail for the defect it claims to detect.
  - Docs: changed contracts are reflected in authoritative docs.
- **Evidence** (`receipts/mutants/mutants.txt`, `.json`; `scripts/probe_mutants.py`): each mutant mutates the generator in a disposable copy of the exported head (submodules at their gitlinks) and regenerates the workflow. It then runs `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py` and `ci_events.py --check`.
  - **The control passes all three.**
  - **SURVIVED by all three judges** (rc 0 each):
    - G03 drops `Fetch RTL dependencies`.
    - G04 drops `Prove the result cache refuses a planted entry`.
    - G05 drops `Install the pinned sv2v release`.
  - **Caught only incidentally:**
    - G01 (drop `Elaborate the integration-heavy tops`) by the key-input control's text edit of that step.
    - G02 (drop the version proof) by a `list.index` crash, not a named refusal.
  - **At this head the retention is correct** (`receipts/consumer/compare.txt`): the four build-side steps are removed, one restore is added, and the other 13 steps are kept in order with byte-identical bodies (step ids aside). The gap is that nothing holds this.
  - **The new job is outside the pin, too.** The new `yosys-tool` job in `rtl-fast.yml` is not in `RTL_SEQUENCE_PINS`, and the rewritten `yosys-elaboration` is pinned only through its template. So the docs' "every job in the four files" claim is newly untrue for these two jobs. rtl-full's generated jobs already had the same shape before this delta; that part predates it.
- **Impact:** a later generator change can delete a self-test from the hosted fast gate (G04) while every check stays green. That is the "a refusal nothing runs is a refusal that rots" failure the template's own comment warns about (`.github/ci-templates/rtl-fast.yml:202-205`).
- **Required outcome:**
  - A control requires the derived `yosys-elaboration` steps to equal the template's, with exactly the cache-and-build pair replaced by the one restore at the same position.
  - It also requires the tool job's steps to be exactly the checkout plus the two moved steps.
  - Each deviation is refused by name.
  - `docs/testing/CI_WORKFLOWS.md:778-790` and `:1157-1162` either state that generated `rtl-fast` jobs are held by the generator comparison plus that control, or the pin reaches them.
- **Verification:** the mutants G01 to G05 in `scripts/probe_mutants.py` are each refused by name, and the control passes.

### R707-1-S1: SUGGESTION (RTL). The tool job downloads the whole tree on a hit

- **Where:** `.github/workflows/rtl-fast.yml:281-287`. The tool job's `actions/cache@v4` step restores `/opt/yosys` on every hit, and nothing in that job reads it.
- **Suggestion:** `lookup-only: true` on the tool job's cache step would skip the download on a hit and keep the miss path identical. This is optional; it saves seconds per run.

## Brief checks (1) to (5)

1. **Generated, not hand-edited; the key.**
   - At the head, `ci_gate_workflows.py --check` passes (rc 0) and `ci_events.py --check` reports OK over 2199 items.
   - The templates and the other three workflows are byte-identical to dev (`receipts/consumer/compare.txt`).
   - The three generated-workflow hand edits I planted (W01 to W03) are refused by both check modes.
   - The key contains no `hashFiles`, and it binds the version, source commit, recipe digest and image.
   - A planted version, source, recipe or image change moves the key. A planted workflow env change that alters the build does not (R707-1-01).
2. **Consumer.**
   - `yosys-elaboration` needs `[changes, yosys-tool]`. It has no build step and no `/tmp/yosys-src`.
   - It restores with `fail-on-cache-miss: true` and no `restore-keys` (`.github/workflows/rtl-fast.yml:370-377`). A miss fails that step by its name, with the key.
   - Every check it ran before is kept, in order, with identical bodies.
   - Timeouts: `yosys-tool` 30 and `yosys-elaboration` 30. No job's timeout differs from dev's. The pre-existing timeouts over 30 (`publication-census` 45, the firmware jobs 45 and 40, `ci-fail-fast` 120) are unchanged and outside this delta.
   - The aggregate needs and reads `yosys-tool`. `ci-fail-fast` compares `EXPECTED_JOBS` as a set (`scripts/ci_fail_fast.py:230`).
   - The retention is not tested (R707-1-02).
3. **Gates.**
   - I ran 23 gates at the exact head, concurrently (`receipts/gates/*.log`, `*.rc`), and all 23 exit 0:
     - `ci_gate_workflows.py --check` and the full "CI scheduling and evidence controls" list (14 commands);
     - `ci_scope.py --selftest`, `ci_events.py --check` and `ci_events.py --selftest` (PASS, 2199 contract items, 5258 arms);
     - the docs gates `docs_check`, `check_em_dash --base 76de691e` (0 findings over 39 added lines), `check_doc_style`, `gen_toc --check` and `check_doc_paths`;
     - `check_py_idiom`.
   - The host interpreter lacks the pinned Markdown renderer, so its first runs of `check_em_dash` and `gen_toc` exited 2. All five docs gates were rerun under a private venv with `tools/markdown/requirements.txt` installed by hash, and pass (`*.venv.rc`).
   - `act_ci.py --selftest` and the 0555 runner contract gate were not run by me (excluded by the brief). The author's published receipts at this head show both `selftest: PASS`, with 623 and 621 `ok` lines and 0 `FAIL` lines, on CPython 3.14 and 3.12 (`review-evidence/789-r1/author/receipts/gates-py31{4,2}/act_ci*.log` at `787d005e`).
   - The act mapping is offline in the author's `act-offline-mapping.txt`. Dependency stage 1 runs `yosys-tool`, stage 2 `yosys-elaboration`, stage 3 `rtl-fast`, and the plan names "Prepare pinned Yosys". `act_ci.py` is unchanged against dev. The live replay is the manager's.
4. **R705-1-01.** `docs/testing/TESTING.md:331` reads exactly "used a hosted `ubuntu-latest` runner, which resolved to the `ubuntu-24.04` image, and sequential `make -C` invocations.", the exact fix in PR #788 issuecomment-6411351133. That is the only change to the file.
5. **Hosted, this PR's own run** (rtl-fast run 40309456540, attempt 1, head `fddf3671`; `receipts/hosted/`).
   - **Cold `yosys-tool`, the first run of the new key.** Job 121533283966 ran 11:08:10 to 11:24:27 UTC, **16 min 17 s** of its 30. Its build step ran 11:08:21 to 11:24:21, 16 min 00 s. The log reads "Cache not found for input keys: yosys-v0.66-…-ubuntu-24.04-Linux", then "Cache saved with key:" with that key.
   - **`yosys-elaboration`, on a head that edits a workflow** (this head edits `rtl-fast.yml`), after the cache existed. Job 121544696739 ran 11:28:34 to 11:39:02, **10 min 28 s** of its 30. The restore took 5 s ("Cache restored from key:" with the same key), no build ran, and all checks passed. The post step skipped the save on the primary-key hit.
   - **Before this delta:** at `847eb4dd` the cold build alone took 16 min 33 s inside `yosys-elaboration` (job 121450772865), and the job was cancelled at 30. I rechecked the docs' figures (16 min 33 s, 13 min 26 s) against those jobs' step times.
   - **Still running at 11:41 UTC:** the `docs` and `elaborate` runs are completed and green at this head. `publication-census` (its own cold build, a known limitation) was in progress, so the `rtl-fast` aggregate, `ci-manifest` and `rtl-full` had not finished. I judge only the two measured jobs.

## Lens ledger (reviewer-owned)

| lens | result | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R707-1-01) | #789 Decision and Acceptance; assignment issuecomment-6413044539; `.github/workflows/rtl-fast.yml:254-377, 1262-1318, 1361, 1467`; `scripts/ci_gate_workflows.py:38-49, 197-272`; hosted jobs 121533283966 and 121544696739; `receipts/key_inputs/`, `receipts/consumer/compare.txt` | R707-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |
| RTL | CLEAN | Architecture of the job graph: `needs`, `if`, ordering, timeouts and the critical path (`receipts/consumer/compare.txt`, author `act-offline-mapping.txt`). The delta has no HDL, `syn/` or constraint file (`git diff --stat 76de691e..fddf3671`: 5 files under `.github/`, `scripts/`, `docs/`). The RTL-facing steps (`Elaborate the integration-heavy tops`, the OOC and synthesis self-tests) have bodies identical to dev's and passed on hosted job 121544696739. S1 only. | R707-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |
| Robustness | UNCLEAN (R707-1-01) | Cache-miss refusal (`fail-on-cache-miss`, no `restore-keys`); failed tool job versus skipped consumer through the real verdict script (selftest arms); docs-only skip; save-failure re-run rule (`CI_WORKFLOWS.md:3293-3296`); configuration-dependent build inputs (`receipts/key_inputs/`) | R707-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |
| Tests | UNCLEAN (R707-1-01, R707-1-02) | `scripts/ci_gate_workflows_selftest.py:93-327`; 23 exact-head gates (`receipts/gates/`); 21 generator and workflow mutants plus a control (`receipts/mutants/`); author receipts at `787d005e` for the runner self-tests | R707-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |
| Docs | UNCLEAN (R707-1-02) | `docs/testing/CI_WORKFLOWS.md:170-173, 317-344, 778-790, 1157-1162, 3270-3296`; `docs/testing/TESTING.md:331` against PR #788 issuecomment-6411351133; hosted step times of jobs 121450772865 and 121450783569; docs gates; PR #794 body; comment-rule scan of the 419 added source and workflow lines (`receipts/comment-rule/scan.txt`: none) | R707-1 | fddf3671ebc96a953755fa1b9a3ecec5f071a350 |

**Comment rule.** The added source comments and docstrings name only issue `#789` and state behaviour. I found no lane label, lane name, review round, reviewer ID or issue-comment ID, so there is no RESIDUE.

## Prior public review findings on this PR

I read the PR conversation only after the verdict and ledger above were written. Besides the two review-start notices, it holds the external review R708-1 (POSITIVE at this head). That review files no BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION, and the PR has no review threads or review comments. So there is no prior finding to resolve or retain. R707-1-01 and R707-1-02 are new in this round.

## Real limits

- **No act, Docker or host runner.** I ran no act, Docker, host `act_ci.py` or its self-test, and none of the 0555 contract gate. For those I rely on the author's published receipts at this head. The live act replay is not run. With a miss now fatal, that replay must show act's cache server saving in `yosys-tool` and restoring in `yosys-elaboration`.
- **No source bank.** No manager source bank ran at this head, and I claim none. My execution evidence is my own gate reruns and probes, plus the author's receipts.
- **Hosted coverage.** I measured only the two jobs above. The `rtl-fast` aggregate's reading of a real `yosys-tool` result is shown by the selftest arms, not by a hosted failure.
- **The planted env edits are models.** R707-1-01's planted edits are in-memory template and generator edits. I did not build Yosys with them; the Makefile lines and the hosted banner show that the inputs reach the binary.
- **Interpreters.** The host is CPython 3.14.8 with PyYAML 6.0.3. The 3.12 pair is the author's receipts.
- **No hardware.** Physical calibration was NOT RUN, and field skips are not hardware proof. No RTL changed.

## Pending manager duties

- Hosted acceptance:
  - the final `rtl-fast` aggregate, `ci-manifest`, `publication-census` and `rtl-full` results at this head;
  - recording the two measured figures in the PR body.
- The live act replay of this head, including the cache save and restore across the two jobs.
- The current-dev merge candidate and its banks at the merge turn.
- The re-review of fixes for R707-1-01 and R707-1-02 at a new head.

R707-1 FINISHED

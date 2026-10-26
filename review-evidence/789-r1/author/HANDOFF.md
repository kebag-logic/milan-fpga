# HANDOFF: issue #789, executor [A682]

Status: **REVIEW READY locally at `fddf3671ebc96a953755fa1b9a3ecec5f071a350`.** Every local gate is rc 0. The two
hosted measurements are **OWED**: no PR or remote branch exists, and this lane may not push before the manager
opens the PR.

- Lane: branch `789-yosys-tool-job`, one commit on dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`.
  - Subject: "Build rtl-fast's pinned Yosys once in its own cached job keyed by version, recipe and image, and
    restore it in yosys-elaboration (#789)".
  - One line, no body, no trailers.
  - Tree diff vs dev: 5 files, +458/-31 (`receipts/full.diff`).
- Origin: `https://github.com/kebag-logic/milan-fpga.git` (confirmed). No submodule git command was run.
- Assignment: issue #789 comment 6413044539. TAKEN: issuecomment-6413216080. REVIEW READY: issuecomment-6414006124.
- STOP condition (the cold tool build cannot fit 30 minutes): **not triggered** on the hosted evidence that exists.
  - The identical cold build step took 13 min 26 s in rtl-full's tool job: job 121450783569, 13 min 51 s for the
    whole job.
  - It took 16 min 33 s inside rtl-fast's `yosys-elaboration`: job 121450772865, at `847eb4dd`.
  - Receipt: `receipts/prior-hosted-cold-builds.tsv`.
  - The new job's own cold time is still owed (see "Hosted measurement").

## Design in one paragraph

**What the generator does.** It derives a new rtl-fast job, `yosys-tool` ("Prepare pinned Yosys"), from
`yosys-elaboration`'s template cache and build steps, as rtl-full's `separate_yosys_build` does for its own tool job.
The templates are unchanged.

**The moved cache key.** It keeps `${{ env.YOSYS_VERSION }}` and the source commit `86f2ddeb...`. It replaces
`${{ hashFiles('.github/workflows/*.yml') }}` with `recipe-<sha256 of the template build step>-<runs-on label>`, and
keeps `${{ runner.os }}`. The digest is computed over the step as sorted, compact JSON, every key included.
- Key: `yosys-${{ env.YOSYS_VERSION }}-86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51-recipe-06e5a02fa8b585ca1b3cc3153245cd97f8b1009666d3b15728f325ed9bd22279-ubuntu-24.04-${{ runner.os }}`.
- Reproduced independently in `receipts/recipe-digest.txt`.

**The consumer.** `yosys-elaboration` needs `[changes, yosys-tool]`. Its two build steps are replaced by one
`actions/cache@v4` restore of the same path and key, with `fail-on-cache-miss: true` and no `restore-keys`. It never
builds Yosys.

**The verdict.** The `rtl-fast` aggregate gains `yosys-tool` in `needs`, its `YOSYS_TOOL_RESULT` binding and its
pair in the verdict loop. Without that, a failed build would skip `yosys-elaboration`, and the verdict counts a
skipped job as a pass.

**Timeouts.** The tool job's timeout is 30 minutes. No timeout was raised (`receipts/job-delta.txt`).

**The act runner.** `act_ci.py` is unchanged. The job uses only `actions/checkout@v4` and `actions/cache@v4` on the
pinned `ubuntu-24.04` label, so dev's trusted runner accepts and orders it (`receipts/act-offline-mapping.txt`).

## Changes

| file:line | change | reason |
|---|---|---|
| `scripts/ci_gate_workflows.py:38-49` | constants `FAST_TOOL_JOB`, `FAST_TOOL_CONSUMER`, `FAST_AGGREGATE`, `FAST_TOOL_TIMEOUT = 30`, `YOSYS_BUILD_STEPS`, `WORKFLOW_FILES_DIGEST`, with the #789 reason comment | one named source for the derivation; the 30-minute owner budget stated once |
| `scripts/ci_gate_workflows.py:197-199` `recipe_digest` | SHA-256 of the template build step as sorted compact JSON | "the build recipe" is that step, every key included (env or condition edits count) |
| `scripts/ci_gate_workflows.py:202-207` `fast_tool_key` | replaces the one workflow-file digest by `recipe-<digest>-<image>`; refuses a template key without exactly one | key = pinned version + recipe + runner image only (Decision); a template the derivation cannot read is refused, never half-derived |
| `scripts/ci_gate_workflows.py:210-212` `result_binding` | the verdict's `<JOB>_RESULT` name and `needs.<job>.result` value | same convention as the template verdict |
| `scripts/ci_gate_workflows.py:215-237` `require_fast_tool` | inserts `yosys-tool` before `yosys-elaboration` in the aggregate's `needs`, env and verdict loop; refuses a verdict without its one elaboration pair | closes the skip-as-pass hole a failed tool job would open |
| `scripts/ci_gate_workflows.py:240-272` `fast_yosys_tool` | builds the job (checkout, moved cache step with the new key, unchanged build step; `needs`/`if`/`runs-on` from the consumer; timeout 30); rewires the consumer to `needs: [changes, yosys-tool]` and an exact restore with `fail-on-cache-miss`; places the job just before its consumer; refuses a missing, reordered or interposed recipe, or a checkout that is not first | Decision: build once in a dedicated job; the consumer restores the tree and never builds |
| `scripts/ci_gate_workflows.py:284-285` | `gate_graph` dispatches rtl-fast to `fast_yosys_tool` | through the generator, never a hand edit (Acceptance 1) |
| `.github/workflows/rtl-fast.yml:254-338` | generated `yosys-tool` job | regenerated by `python3 scripts/ci_gate_workflows.py` only |
| `.github/workflows/rtl-fast.yml:339-376` | generated consumer: `needs` gains `yosys-tool`; the "Restore the pinned Yosys build" step replaces the cache and build steps | as above |
| `.github/workflows/rtl-fast.yml:1265,1302,1318` | the verdict's `needs`, env binding and loop pair | as above |
| `.github/workflows/rtl-fast.yml:1364,1470-1471` | the collector's `needs` and the watcher's `EXPECTED_JOBS` gain the new job (runtime generator, automatic) | evidence collection and fail-fast cover the new job |
| `scripts/ci_gate_workflows_selftest.py:93-111` | `HOSTED_BUDGET_MINUTES = 30` (held here, not read from the generator), `named_step`, `verdict_exit` (runs the real verdict script under bash) | independent oracle; behaviour, not text |
| `scripts/ci_gate_workflows_selftest.py:114-165` `fast_tool_findings` | each #789 property refused in its own words | the checker the planted arms and mutants judge against |
| `scripts/ci_gate_workflows_selftest.py:168-327` | `fast_tool_planted` (17 planted defects in the generated graph), `fast_tool_key_inputs` (key unchanged by an edit outside the recipe; changed by a recipe or image change), `fast_tool_template_refusals` (5 template defects), `fast_tool_controls` (pristine pass; only the consumer and the verdict change at the derivation; docs-only stays green) | tests that can fail for each defect claimed |
| `scripts/ci_gate_workflows_selftest.py:773` | `main` runs `fast_tool_controls()` | wired into the hosted "CI scheduling and evidence controls" step (docs-gates) |
| `docs/testing/CI_WORKFLOWS.md:173` | docs-only skip list names `yosys-tool` | completeness |
| `docs/testing/CI_WORKFLOWS.md:317-338` | new paragraph: the tool job, the key's inputs and digest, the exact restore, the verdict's need, the before/after evidence, and the self-test's defects | changed contract in the authoritative page |
| `docs/testing/CI_WORKFLOWS.md:342-344` | `publication-census` no longer "the same cache key as yosys-elaboration": it keeps its own build under the workflow-bound key and does not need `yosys-tool` | the old sentence became false; that job's behaviour is unchanged by assignment |
| `docs/testing/CI_WORKFLOWS.md:3286-3295` | "Source-tool cache provenance": the one key that differs, how it is held, and the re-run-all rule after a failed cache save | the section said every recipe digest covers the workflow files |
| `docs/testing/TESTING.md:331` | R705-1-01's exact wording: "which resolved to the `ubuntu-24.04` image" | assignment item |

## New checks and planted mutants

All the controls live in `scripts/ci_gate_workflows_selftest.py` and run in the hosted docs workflow's "CI scheduling
and evidence controls" step. The campaign runs the self-test against a mutated copy of the generator, on a scratch
copy outside the tree (`receipts/scripts/mutants.py.txt`). Logs: `receipts/mutants/`. Summary:
`receipts/mutants/summary.tsv`. The control (the unmutated generator) passes, rc 0. **20/20 code mutants and 4/4
tree mutants (8/8 checks) are caught.**

| mutant (generator code) | check that refuses it | failing words |
|---|---|---|
| M01 key keeps the workflow-file digest | key inputs | `tool key binds the workflow files` |
| M02 key drops the runner image | key inputs | `tool key lacks the runner image` |
| M03 key drops the recipe digest | key inputs | `tool key lacks the build recipe` |
| M04 recipe digest is a constant | key follows recipe/image | `tool key does not follow its build recipe and runner image` |
| M05 digest over the whole consumer job | key unchanged outside recipe | `tool key changed by an edit outside the build recipe` |
| M06 consumer keeps its build | consumer never builds | `yosys-elaboration builds Yosys` |
| M07 restore accepts a miss (`fail-on-cache-miss: false`) | exact restore | `yosys-elaboration does not restore exactly the tool tree` |
| M08 restore with `restore-keys` | exact restore | `yosys-elaboration does not restore exactly the tool tree` |
| M09 consumer does not need the tool job | consumer needs | `yosys-elaboration does not need the tool job` |
| M10 verdict not wired to the tool job | verdict run under bash with tool `failure` | `rtl-fast verdict accepts a failed tool job` |
| M11 verdict script lacks the tool pair | same | `rtl-fast verdict accepts a failed tool job` |
| M12 verdict env lacks the tool binding | verdict run all-green (`set -u`) | `rtl-fast verdict refuses an all-green run` |
| M13 tool timeout 45 | budget | `timeout changed or above the hosted budget: yosys-tool` |
| M14 tool job `if: always()` | tool job condition | `tool job if differs from yosys-elaboration's` |
| M15 tool job needs nothing | tool job condition | `tool job needs differs from yosys-elaboration's` |
| M16 tool job on `ubuntu-22.04` | tool job condition | `tool job runs-on differs from yosys-elaboration's` |
| M17 tool job appended last | placement | `tool job not just before its consumer` |
| M18 template key without the digest accepted | template refusal | `accepted a template key without its workflow-file digest` |
| M19 a step between cache and build moved as the build | template refusal (arm added after this mutant first survived) | `accepted a template step between the cache and its build` |
| M20 tool job without its build step | tool job carries the recipe | `tool job does not carry the template cache and build steps` |

| mutant (hand edit of the generated tree, scratch export) | `ci_gate_workflows.py --check` | `ci_events.py --check` |
|---|---|---|
| T1 tool key bound to the workflow files again | rc 1 `regenerate the gate jobs` | rc 1 `generated gate jobs must match` |
| T2 verdict without `yosys-tool` in `needs` | rc 1, same words | rc 1, same words |
| T3 restore without `fail-on-cache-miss` | rc 1, same words | rc 1, same words |
| T4 `rtl-fast.yml` left at dev's | rc 1, same words | rc 1, same words |

The self-test also plants these 17 defects in the generated graph in-process, each refused by name. The output is in
the self-test log (26 "Fast Yosys tool" lines).

- Key bound to the workflow files.
- Key without its version, source, recipe or image.
- A tool-cache fallback.
- A tool job without its build.
- A tool timeout of 45, or a consumer timeout of 45.
- A tool job on another condition.
- A consumer that builds.
- A consumer without the need.
- A restore that accepts a miss, has a fallback, or restores another key.
- A verdict without the need, or without the pair.

It also plants 5 template defects, each refused by the generator: a key without its digest, a missing build, a build
before its cache, an interposed step, and a verdict without its elaboration pair.

## Gate table

Exact head `fddf3671ebc96a953755fa1b9a3ecec5f071a350`, clean tree. Every command ran unpiped, and every rc is 0.
- CI-tooling gates ran on CPython 3.14.8 + PyYAML 6.0.3 and on CPython 3.12.3 + PyYAML 6.0.2, the latter installed
  in a scratch venv from `ci/requirements-evidence.txt` with `--require-hashes`.
- Docs gates ran under the pinned Markdown renderer environment.
- Logs: `receipts/gates-py314/`, `receipts/gates-py312/` and `receipts/gates-docs/`, each with a `summary.tsv`. The
  two `ci_events --selftest` logs are over 200 KB; they are kept as excerpts with the full log's sha256 and size.

| gate | 3.14 | 3.12 | result |
|---|---|---|---|
| `python3 scripts/ci_gate_workflows.py --check` | 0 | 0 | no drift |
| `python3 scripts/ci_gate_workflows_selftest.py` | 0 | 0 | `gate workflow and union controls: PASS`, 26 fast-tool lines |
| ci_case_receipts, ci_make_cases, ci_maap_cases, ci_capture_cases, ci_suite_pieces, ci_suite_collect, ci_fail_fast, ci_runtime_evidence, ci_install_cache, ci_workflow_plan, ci_manifest self-tests | 0 | 0 | PASS |
| `python3 scripts/generate_ci_evidence_pins.py --check` | 0 | 0 | pins unchanged |
| `python3 scripts/ci_scope.py --selftest` | 0 | 0 | PASS |
| `python3 scripts/ci_events.py --check` | 0 | 0 | OK, 2199 items |
| `python3 scripts/ci_events.py --selftest` | 0 | 0 | PASS, 2199 items, 5258 arms (34 arms on the generated `yosys-tool`) |
| `python3 scripts/act_ci.py --selftest` | 0 | 0 | PASS, 623 ok |
| 0555 flat install `python3 -I <dir>/act_ci.py --selftest --worktree <worktree>` | 0 | 0 | PASS, 621 ok |

| docs / quality gate (renderer env, or system 3.14 for the code ratchets) | rc |
|---|---|
| `docs_check.py`; `check_em_dash.py --base 76de691e5625cc4ea2f9a19def9e07c1183a14ee` (0 findings over 39 added lines) | 0, 0 |
| `check_doc_style.py` and `--selftest`; `check_gptp_docs.py` and `--selftest` | 0 x4 |
| `docs/DOC_MAP.gen.py --check` and `--selftest`; `check_doc_paths.py`; `check_archive.py` and `--selftest` | 0 x5 |
| `gen_toc.py --selftest`, `--verify-anchors`, `--check`; `check_feature_status.py --self-test`; `check_baremetal_only.py --check` | 0 x5 |
| `check_py_idiom.py` and `--selftest`; `check_sh_idiom.py`; `check_hygiene.py --check`; `measure_fail_fast.py --check`; `measure_test_evidence.py --check`; `check_todo_ownership.py`; `measure_naming.py --check` | 0 x8 |
| docs-check-no-git replica (`git archive HEAD`, no `.git`): `docs_check.py`, `check_feature_status.py` | 0, 0 |

Not run, and why:
- **No Verilator sweep, Yosys sweep or Vivado run.** There is no RTL change (instruction).
- **No `cd tests && behave`.** It reads `REGISTER_MAP.md` and the Milan audit page, and this change touches neither.
- **`ci_tool_inventory.py --check`.** This is an image-build tool, run only by `ci/image/build.py`. It refuses with
  `CI_IMAGE_SHFMT must name the checksum-pinned Bash parser` identically at dev `76de691e`, and its
  `tool-inventory.json` already carries stale workflow digests at dev.
- **No live act replay**, by the bootstrap rule. The live replay is the manager's.

## Act mapping (offline)

`receipts/act-offline-mapping.txt`. dev's trusted `scripts/act_ci.py` is blob `865867c3`, identical to the
candidate's. Imported offline, it gives these results on the candidate workflows:
- `validate_workflow_sandbox`: accepted, all four workflows.
- Job-volume scope: unchanged.
- rtl-fast concurrency: 4.
- Actions: four of the five audited ones, nothing else.
- `RUNS_ON_LABELS ('ubuntu-24.04',)`: mapped to the runner image.

**Ordering.** The dependency stages put `yosys-tool` in stage 1, `yosys-elaboration` in stage 2 and `rtl-fast` in
stage 3. `ci_workflow_plan` plans `.github/workflows/rtl-fast.yml:yosys-tool` under the label "Prepare pinned
Yosys", and the local manifest maps act events to plan entries generically by job id.

**Effect.** act runs stages in sequence, so the replay's wall clock grows by about one `yosys-elaboration` run. Each
replay has a fresh cache server, so the tool job builds cold there (about 6 min at 16 CPUs per the policy page).

## Hosted measurement

OWED. No PR exists (`gh pr list --head 789-yosys-tool-job` is empty) and no remote branch exists. Once the manager
opens the PR, record the following in the PR body:
1. **Cold tool job.** On the first rtl-fast run at `fddf3671`, the new key exists nowhere yet.
   - Record "Prepare pinned Yosys": job id, start/end and the build step's window.
   - Confirm `Cache not found` for the new key and a successful "Post Cache the pinned Yosys build".
   - STOP if the job alone cannot finish inside 30 minutes.
2. **`yosys-elaboration` on a head that edits a workflow, after the tool cache exists.** This head edits
   `rtl-fast.yml`.
   - In the same run, the cache is saved before `yosys-elaboration` starts. Record its job time, and confirm
     "Restore the pinned Yosys build" logs `Cache restored from key: yosys-v0.66-...-recipe-06e5a02f...-ubuntu-24.04-Linux`
     and that no build step exists.
   - For the strongest form, take any later head that changes a workflow file but not the recipe (a review fix, or
     a dev merge). It must show the tool job restoring the same key, with its build skipped, and
     `yosys-elaboration` restoring it.
   - A whole-workflow re-run of the first head shows the warm tool job.
3. **Post-merge dev push.** It misses once on `refs/heads/dev`, because PR-scoped caches are invisible to dev. The
   cold build then happens in the tool job, inside its own 30 minutes, and every later run restores it.

## Open risks

1. **`publication-census` still builds Yosys cold on every workflow edit.** It used 26 min 55 s of its 45-minute
   timeout at `847eb4dd` (job 121450772909, `receipts/prior-rtl-fast-847eb4dd-jobs.tsv`). The assignment forbids
   changing other jobs. A follow-up Issue could let it restore from `yosys-tool`.
2. **A failed cache save.** If the tool job's save does not complete (reservation or eviction), `yosys-elaboration`
   refuses on the miss: fail-closed and visible. Re-running only the failed jobs repeats the refusal; re-run all
   jobs. This is documented at `CI_WORKFLOWS.md:3294-3295`.
3. **What "the runner image" means in the key.** It is the pinned label `ubuntu-24.04` with `runner.os`, not the
   weekly `ImageVersion`. A binary built on one 24.04 image update is reused on later ones, as before #789, when only
   `runner.os` was keyed. A label move rebuilds automatically, because the generator takes the label from the job's
   `runs-on`.
4. **What holds the generated properties.** They are held by `ci_gate_workflows_selftest.py` and by `ci_events`'
   generated-graph equality, not by a `ci_events` template step list. That is the same way rtl-full's generated
   `yosys-tool` is held. The templates and `ci_events.py` are unchanged.
5. **A slower cold recipe change.** On a recipe change, the cold rtl-fast critical path is the tool job (about
   14-17 min) plus `yosys-elaboration` (about 11.5 min warm, run 40187422747). Each job is within its own 30 minutes.
   A workflow edit alone no longer causes a cold build.

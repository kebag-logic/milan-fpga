# HANDOFF: [A682b], issue #789, PR #794, round 2

Status: REVIEW READY. Round-2 implementation and hosted measurements complete; independent re-review and the live act replay remain pending.

- **Head:** `1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086`, two commits on round-1 head
  `fddf3671ebc96a953755fa1b9a3ecec5f071a350` (dev `76de691e5625cc4ea2f9a19def9e07c1183a14ee`).
  - `b45573c1b7826ce9b4971b023c765644c8c39a5e` Bind rtl-fast's Yosys tool key to every build input of the
    generated tool job and hold both derived jobs whole against the template (#789)
  - `1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086` Name a refused step after rtl-fast's Yosys build by its step
    name, not its generated id (#789)
- **Pushed** to `origin/789-yosys-tool-job` (fast-forward, push-privacy-check 0 private lines before each push).
  No force-push, no other branch.
- **Assignment:** issue #789 issuecomment-6415180907, answering R707-1 (PR #794 issuecomment-6415176398).
- **TAKEN:** issue #789 issuecomment-6415219697.

## Items

| item | state |
|---|---|
| 1. R707-1-01: the key binds every build input; an environment edit misses | done, plants fail on `fddf3671` |
| 2. R707-1-02: a check holds `yosys-elaboration`'s retained steps; a dropped one fails a named judge | done, mutants survive on `fddf3671`, killed by name at head |
| 3. Hosted measurements in the PR body | see [Hosted](#hosted) |
| S1 (`lookup-only` on the tool job's cache) | declined, reason below |

## Changes (file:line at `1e0c5c09`)

### `scripts/ci_gate_workflows.py` (generator)

- `:50` `FAST_TOOL_RESTORE`: the restore step's name, spelled once (used at `:263`, `:327`).
- `:55` `FAST_TOOL_RECIPE`: the derivation now writes a stand-in (`recipe-{build-inputs}`) where the digest
  goes. Reason: the build the tool job runs is only final after `ci_install_workflows` (package-index steps,
  rewritten install line) and `ci_runtime_workflows` (job budget step) have run, so the digest has to be
  taken over the emitted job, not over the template step (R707-1-01 "generator-side rewrite" row).
- `:57` `FAST_TOOL_SCHEDULING` (`name`, `needs`, `if`, `timeout-minutes`): the only tool-job keys left out
  of the digest. Reason: they schedule the job and never reach the build; every other job key (today
  `runs-on`; any `env`/`defaults` carried, any key a later transform adds) is digested.
- `:60` `FAST_TOOL_CARRIED` (`runs-on`, `env`, `defaults`) and `:311-314` the refusal of any other
  consumer job key; `:322` the tool job carries the consumer's `env`/`defaults`. Reason: R707-1-01 required
  outcome "a job-level env on the template consumer is either carried into the tool job and digested, or
  refused". The moved build ran under them, so it keeps running under them; `container`, `services`,
  `strategy` and the rest are refused by name rather than silently dropped from the build.
- `:63` `FAST_TOOL_EVIDENCE` and `:237-241`: the only steps allowed after the build are the runtime evidence
  pair (`ci_record`, `ci_upload`); anything else is refused by name. Reason: every step runs before the
  cache action's post-job save, so a step after the build could change the saved tree outside the key.
- `:66` `REPOSITORY_READ` and `:249`: repository files the build's steps name by relative path. Today that
  is `scripts/ci_install_cache.py` (it runs `apt-get update` for the index the build installs from), bound
  by `${{ hashFiles('scripts/ci_install_cache.py') }}` (assignment: "every script or pinned file the step
  reads"). Never a workflow file.
- `:215` `recipe_digest(inputs)`: now digests the build-inputs mapping.
- `:220` `fast_tool_key(cache, image)`: template key, workflow-file digest replaced by the stand-in.
- `:228-249` `fast_tool_inputs(workflow)`: the inputs are the workflow's `env` and `defaults` (whole, since
  make reads every environment variable as a make variable of the same name), the tool job's keys but the
  scheduling ones, and every step up to and including the build as generated, minus the moved cache step's
  own key.
- `:252-268` `bind_fast_tool_key(workflow)`: replaces the stand-in in exactly the tool cache and the one
  restore (refuses otherwise), appending the `hashFiles` binding.
- `:389-390` `generate()`: binds the key for `rtl-fast` after both transforms, before
  `check_inventory_dependencies`.

### `scripts/ci_fast_tool_selftest.py` (new, 477 lines)

The fast-tool controls moved here from `scripts/ci_gate_workflows_selftest.py`. Reason: the selftest
crossed Rule 12's 1000-line module limit (`check_py_idiom`: "long module 11 > ratchet 10"). The original
selftest is now dev's file plus two lines (`:27` import, `:537` call), so the hosted "CI scheduling and
evidence controls" step runs it unchanged.

- `:41` `key_reads`, `:46` `scripts_run`: the selftest's own reading of the key's `hashFiles` paths and of
  the `python3`/`bash`/`sh` scripts a run body executes, independent of the generator's regex.
- `:72` `fast_tool_findings` now also requires the tool job's `env` and `defaults` to equal the consumer's.
- `:91-96`: "tool key binds the workflow files" now refuses only a `hashFiles` path that matches the
  generated workflow or lies under `.github/`; new "tool key does not bind the scripts its build steps
  run: <paths>".
- `:201` `fast_tool_retention(template, derived)`: R707-1-02's judge. `yosys-elaboration` after the
  derivation must run every template step but the moved pair, in order and unchanged, with the one exact
  restore in the pair's place and its other job keys unchanged; `yosys-tool` must run exactly the checkout
  and the two moved steps.
- `:239` `fast_tool_retention_planted`: the plants for that judge (below).
- `:309` `fast_tool_key_inputs`: the key must change on each build-input edit and must not change on an
  edit outside the build or of the tool job's `if`; a step after the build is refused by the generator.
- `:406` `fast_tool_template_refusals`: adds the refused `container` consumer.
- `:454` `fast_tool_controls`: runs the retention judge and the findings on the pristine head first.

### `.github/workflows/rtl-fast.yml` (regenerated only)

- `:286-287` and `:374-375`: the two key lines. New key:
  `yosys-${{ env.YOSYS_VERSION }}-86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51-recipe-e15c97b1c78fe65063d60516fd3cc9f594e30beee1e2862da7554b41692ebc1b-${{ hashFiles('scripts/ci_install_cache.py') }}-ubuntu-24.04-${{ runner.os }}`.
  Nothing else in any workflow changed against `fddf3671`.

### `docs/testing/CI_WORKFLOWS.md`

- `:322-354` (Fast feedback): exactly what the digest covers, the `hashFiles` binding, the after-build
  refusal, that a `VERILATOR_VERSION` bump rebuilds Yosys once, and that distribution package versions
  (the compiler's among them) follow the image label only (R707-1-01 required outcome, docs `:322-326`).
- `:360-380`: the selftest's plants, the key-input edits, and `fast_tool_retention`.
- `:827-829` and `:844-855` (item 4): the checker reads the source contracts (templates); a job or step list
  only the generator produces is held by `check_generated_workflow`, plus `fast_tool_retention` for
  `rtl-fast.yml`'s two jobs; for `rtl.yml`'s derived jobs the comparison is the only whole-list hold
  (pre-existing, stated, not changed here) (R707-1-02 required outcome, docs `:778-790`).
- `:1211-1213`: "every job in the four files' source contracts", pointing at item 4 (docs `:1157-1162`).
- `:3341-3351` (Source-tool cache provenance): what the digest covers (docs `:3286-3290`).

## New checks: plant, failing words, and the result on `fddf3671`

Receipts: `receipts/probes/new_checks-*.txt`, `mutants-*.txt`, `key_inputs-*.txt`, and
`receipts/gates-py314/ci_gate_workflows_selftest.log` (the printed refusals).

### R707-1-01 (key)

| plant | words at head | at `fddf3671` |
|---|---|---|
| workflow `env` gains `CXXFLAGS: -O0` | key changes (else "tool key unchanged by an edit of its build inputs: the workflow env") | key unchanged: FAIL, named |
| `yosys-elaboration` job `env` `CXXSTD: c++23` | key changes, and the tool job carries the env | unchanged: FAIL, named |
| install transform rewrites the build's compile line (`CXXFLAGS=-O0`) | key changes | unchanged: FAIL, named |
| job budget step exports `CXXFLAGS` | key changes | unchanged: FAIL, named |
| template build runs `python3 scripts/ci_scope.py` | key changes and binds `hashFiles('scripts/ci_scope.py')` | binding absent |
| template build recipe edit; runner image | key changes | key changes (unchanged behaviour) |
| edit outside the build; tool job `if` edit | key unchanged | key unchanged |
| a step between the build and the cache save | generator: "yosys-tool: steps after the build that its key does not bind: Touch the built tree" | accepted: FAIL |
| generated key without its script binding | "tool key does not bind the scripts its build steps run" | pristine already fails: "...: scripts/ci_install_cache.py" |
| generated tool job under another `env` | "tool job env differs from yosys-elaboration's" | (new judge) |
| template consumer in a `container` | generator: "yosys-elaboration: job keys the tool job does not carry into the build: container" | accepted: FAIL |

`fast_tool_key_inputs` at `fddf3671` fails with exactly: "tool key unchanged by an edit of its build inputs:
the workflow env, yosys-elaboration's job env, an install-transform rewrite of the build, an export added to
the job budget step" (`receipts/probes/new_checks-fddf3671.txt`).

Resolved key table (`receipts/probes/key_inputs-*.txt`, hashFiles resolved as the runner does):
at `fddf3671` 8 rows are STALE-SERVED (workflow env `CXXFLAGS`, `CXXSTD`, an unrelated workflow env name,
consumer job env, install-transform rewrite, budget export, `scripts/ci_install_cache.py` content, a step
after the build). At `1e0c5c09` 0 rows are STALE-SERVED; the edit outside the build and the `if` edit keep
the key; the after-build step is REFUSED. The pristine key at `fddf3671` resolves byte-for-byte to the key
the hosted tool job saved there (as R707-1 also showed).

### R707-1-02 (retention)

| plant (on the derived jobs) | failing words |
|---|---|
| each of the 9 retained steps dropped in turn (checkout, Fetch RTL dependencies, the version proof, sv2v, Elaborate, OOC read sets, ooc.sh, synthesis guards, result cache) | "yosys-elaboration drops <step>" |
| a retained body rewritten | "yosys-elaboration changes Elaborate the integration-heavy tops" |
| a step added | "yosys-elaboration adds Planted step" |
| two retained steps swapped; one repeated | "yosys-elaboration reorders or repeats its retained steps" |
| the restore moved last; the restore accepting a miss | "yosys-elaboration's one exact restore is not in its build's place" |
| a consumer job key added | "yosys-elaboration's job keys differ from the template's" |
| a tool job step added; the tool build rewritten | "tool job steps are not the checkout and the two moved steps" |
| the real derivation patched to drop the result-cache self-test | "yosys-elaboration drops Prove the result cache refuses a planted entry" |

Generator mutants through all three hosted judges (`receipts/probes/mutants-*.txt`; each mutant edits
`fast_yosys_tool` in a fresh copy, regenerates, then runs `ci_gate_workflows.py --check`,
`ci_gate_workflows_selftest.py`, `ci_events.py --check`):

| mutant | `fddf3671` | `1e0c5c09` |
|---|---|---|
| control | PASS | PASS |
| G01 drop Elaborate | killed incidentally ("tool key changed by an edit outside the build recipe") | "yosys-elaboration drops Elaborate the integration-heavy tops" |
| G02 drop the version proof | killed by a crash (`list.index`) | "yosys-elaboration drops Install the pinned Yosys and prove the version" |
| G03 drop Fetch RTL dependencies | SURVIVED | "yosys-elaboration drops Fetch RTL dependencies" |
| G04 drop the result-cache self-test | SURVIVED | "yosys-elaboration drops Prove the result cache refuses a planted entry" |
| G05 drop sv2v | SURVIVED | "yosys-elaboration drops Install the pinned sv2v release" |
| G06 to G08 drop each ooc/guard self-test | SURVIVED | "yosys-elaboration drops <step>" |
| G09 swap the two ooc self-tests | SURVIVED | "yosys-elaboration reorders or repeats its retained steps" |
| G10 extra tool-job step | SURVIVED | refused by the generator: "steps after the build that its key does not bind: Planted step" |

## Gate table (exact head `1e0c5c09`)

Run by `tools/run-gates.sh` (concurrent, one log and rc per gate) on CPython 3.14.8 + PyYAML 6.0.3
(`receipts/gates-py314/`) and CPython 3.12.13 + PyYAML 6.0.2 by hash from `ci/requirements-evidence.txt`
(`receipts/gates-py312/`). Docs gates under the pinned Markdown renderer venv in both runs. Every rc is 0
(64 of 64). The same 64 also passed at `b45573c1` (`receipts/at-b45573c1/`).

| gate | py3.14 | py3.12 |
|---|---|---|
| `ci_gate_workflows.py --check` | 0 | 0 |
| `ci_gate_workflows_selftest.py` (50 "Fast Yosys" lines, ends `gate workflow and union controls: PASS`) | 0 | 0 |
| the other 12 commands of "CI scheduling and evidence controls" (`ci_case_receipts`, `ci_make_cases`, `ci_maap_cases`, `ci_capture_cases`, `ci_suite_pieces`, `ci_suite_collect`, `ci_fail_fast`, `ci_runtime_evidence`, `ci_install_cache`, `ci_workflow_plan`, `ci_manifest` selftests, `generate_ci_evidence_pins.py --check`) | 0 | 0 |
| `ci_scope.py --selftest` | 0 | 0 |
| `ci_events.py --check` (OK, 2199 items) | 0 | 0 |
| `ci_events.py --selftest` (PASS, 2199 items, 5258 arms) | 0 | 0 |
| runner contract gate: `act_ci.py --selftest` then the 0555 install `--selftest --worktree` (PASS, 623 and 621 ok) | 0 | 0 |
| `check_py_idiom.py` and `--selftest` | 0 | 0 |
| `check_baremetal_only.py --check`, `check_hygiene.py --check`, `check_todo_ownership.py` | 0 | 0 |
| `measure_naming.py --check`, `measure_test_evidence.py --check`, `measure_fail_fast.py --check` | 0 | 0 |
| `docs_check.py`, `check_em_dash.py --base 76de691e` (0 findings over 101 added lines), `check_doc_style.py`, `gen_toc.py --check`, `gen_toc.py --verify-anchors`, `check_doc_paths.py` | 0 | 0 |

`act_ci.py` is unchanged (same blob as dev); it was run offline only (its `--selftest` and the 0555 copy's
`--selftest --worktree`), never with `--sudo`, against a PR, or through the host act slots. The change
reaches nothing `bdd-conformance` reads (`tests/`, the processor models), so `behave` was not run. No RTL
changed: no Verilator sweep, Yosys or Vivado bank, no lock taken.

## S1 (optional): declined

`lookup-only: true` on the tool job's cache would skip a download of about 5 s on a hit. It would make the
moved cache step differ from the template's, which `fast_tool_findings` ("tool cache restores more than its
exact key") and `fast_tool_retention` deliberately refuse, and act's cache server support for it is
unverified offline. The miss path, which is what the 30-minute budget is about, is unchanged either way.

## Hosted

At head `1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086`,
[rtl-fast run 40321654840](https://github.com/kebag-logic/milan-fpga/actions/runs/40321654840), attempt 1:

| job | UTC start -> end (2026-10-26) | duration | result |
|---|---|---|---|
| [Prepare pinned Yosys](https://github.com/kebag-logic/milan-fpga/actions/runs/40321654840/job/121571465201), cold new key | 12:29:23 -> 12:42:10 | **12 min 47 s** | success |
| build step within that job | 12:29:37 -> 12:42:03 | 12 min 26 s | success |
| [yosys-elaboration](https://github.com/kebag-logic/milan-fpga/actions/runs/40321654840/job/121577793452), cache present | 12:45:02 -> 12:57:47 | **12 min 45 s** | success |
| restore step within that job | 12:45:09 -> 12:45:11 | 2 s | success |
| [rtl-fast aggregate](https://github.com/kebag-logic/milan-fpga/actions/runs/40321654840/job/121585176676) | 13:09:01 -> 13:09:09 | 8 s | success |

The tool log records `Cache not found for input keys:` followed by `Cache saved with key:` for the
new `recipe-e15c97b1…-19cd9b6e…-ubuntu-24.04-Linux` key. The consumer records `Cache restored from key:`
for that exact key, runs no build, and passes every retained check. This head changes the generated
workflow's key lines. Both jobs finish within their unchanged 30-minute timeouts; STOP is not triggered.

The separate package-download cache emitted a save warning for its lock and partial entries.
The Yosys tree cache saved successfully and the consumer restored it. No unrelated job was changed.

Receipts: `receipts/hosted/run-40321654840.json`, `receipts/hosted/tool-job-121571465201-excerpt.txt`,
and `receipts/hosted/consumer-job-121577793452-excerpt.txt`. The excerpts record full-log byte sizes and
SHA-256 digests; the large full build log is not retained.

The docs and elaborate workflows completed successfully (`receipts/hosted/run-40321654936.json`
and `receipts/hosted/run-40321654818.json`). At the final snapshot, the fast aggregate is green but
its manifest job and the rtl-full workflow remain queued; this is not an all-required-checks-green claim.
`receipts/hosted/run-40321654737.json` records the latter. The manager retains the live act replay,
remaining hosted contexts, independent re-review, and merge-candidate validation.


## Not done / limits

- The live act replay of this head (manager's; with a miss now fatal it must show act's cache server saving
  in `yosys-tool` and restoring in `yosys-elaboration`).
- `rtl.yml`'s derived jobs are held whole only by the generated-graph comparison (pre-existing; now stated in
  the docs). Candidate follow-up Issue, not opened.
- `publication-census` still builds Yosys under its own workflow-bound key (unchanged by assignment).
- Distribution package versions (the compiler's included) are bound only through the image label.

## Resume verification and receipt index

The resumed tree was clean at the recorded head; origin and the merge base match the assignment
(`receipts/resume-provenance.txt`). All 64 final-head gate rc files are 0. No repository edit or further
push was needed during resume. The existing TAKEN comment was not duplicated.

A fresh offline data-only check accepts all four workflow sandboxes and places `yosys-tool` in stage 1,
`yosys-elaboration` in stage 2 and `rtl-fast` in stage 3 (`receipts/act-offline-mapping.txt`).
No act execution, Docker access, hardware activity or submodule Git command was used during resume.

`RECEIPTS-INDEX.md` is generated from files actually present, with relative names, sizes and SHA-256.
`PR-BODY.md` retains `Relates to #789` because the live act replay is still owed.

REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/789#issuecomment-6416853353

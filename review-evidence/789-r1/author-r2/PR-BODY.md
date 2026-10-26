[A682b]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally, round 2 answering R707-1. `789-yosys-tool-job` -> `dev`, three commits on dev `76de691e`.
Head: `1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086`.

- **Gates: 32 of 32, rc 0, on two interpreters (64 runs).** CPython 3.14.8 with PyYAML 6.0.3, and CPython
  3.12.13 with PyYAML 6.0.2 installed by hash from `ci/requirements-evidence.txt`. They include the whole
  "CI scheduling and evidence controls" list, `ci_events.py --check` and `--selftest` (2199 items, 5258 arms),
  the runner contract gate (623 ok, plus 621 ok in the 0555 flat install), the code-quality gates the new
  module reaches, and the docs gates under the pinned Markdown renderer.
- **R707-1-01:** each build-input plant fails on `fddf3671` and passes here. A resolved-key probe finds
  8 stale-served edits at `fddf3671` and none at this head.
- **R707-1-02:** of 10 generator mutants that drop, reorder or add a step, 8 survive all three hosted judges
  on `fddf3671`. Here every one is refused by name.
- **Hosted:** cold tool job **12m47s**, cached consumer **12m45s**, both success at this head; `rtl-fast` aggregate success. See the measurements below.

## Linked Issue / roles

Relates to #789
<!-- The live act replay is still owed; this PR does not yet claim all acceptance items. -->

Executor: `[A682]` (round 1), `[A682b]` (round 2)
Internal cleared-context reviewer: `[R707]` (R707-1 NEGATIVE at `fddf3671`; re-review of this head owed)
External reviewer: `[R708]` (R708-1 POSITIVE at `fddf3671`; this head is new)

## Description

**The problem (#789).** `rtl-fast`'s `yosys-elaboration` built pinned Yosys itself, under a cache key that hashed
`.github/workflows/*.yml`.
- Every head that edits a workflow rebuilt it cold inside the job's 30 minutes. At `847eb4dd` the build took
  16 min 33 s (job 121450772865), then the job was cancelled at 30 minutes.
- `ci-fail-fast` then cancelled every run of the head (PR #788 review R705-1-02).

This PR builds Yosys once, in a job of its own (`yosys-tool`, "Prepare pinned Yosys"), under a key that no
workflow edit changes unless the edit reaches the build.

| piece | change |
|---|---|
| `scripts/ci_gate_workflows.py` | rtl-fast's derivation `fast_yosys_tool`, modelled on rtl-full's `separate_yosys_build`. It moves `yosys-elaboration`'s template "Cache the pinned Yosys build" and "Build Yosys from source on cache miss" steps into `yosys-tool`. That job has the consumer's `needs`, `if`, `runs-on`, `env` and `defaults`, and `timeout-minutes: 30`. Any other consumer job key is refused. The templates are unchanged. |
| the tool key | `yosys-${{ env.YOSYS_VERSION }}-86f2ddebce7e98ce7cacc27e8a5c14cb53b51b51-recipe-e15c97b1c78fe65063d60516fd3cc9f594e30beee1e2862da7554b41692ebc1b-${{ hashFiles('scripts/ci_install_cache.py') }}-ubuntu-24.04-${{ runner.os }}`. The pinned version and source commit come first. Then `recipe-` and the SHA-256 of the build's inputs, taken over the generated tool job (see below). Then `hashFiles` of the repository script the build's steps run, the runner image label, and `runner.os`. No workflow file is named. |
| the recipe digest (round 2, R707-1-01) | It covers the workflow's `env` and `defaults`, whole. It covers the tool job's keys other than `name`, `needs`, `if` and `timeout-minutes`. It covers every step up to and including the build, as generated: the checkout, the job budget step and its exports, the package-index steps, the rewritten install line and the build, minus the cache step's own key. The derivation writes a stand-in that `generate()` replaces after both transforms, so a generator-side rewrite of the build changes the key. Only the runtime evidence pair may follow the build; any other step there is refused, since it would run before the cache save. |
| `yosys-elaboration` | needs `[changes, yosys-tool]`. Its two build steps are replaced by one `actions/cache@v4` restore of `/opt/yosys` under the same key, with `fail-on-cache-miss: true` and no `restore-keys`. It never builds Yosys. Its timeout stays 30. |
| `rtl-fast` aggregate | gains `yosys-tool` in `needs`, `YOSYS_TOOL_RESULT` and its pair in the verdict loop. A failed build skips `yosys-elaboration`, and the verdict counts a skipped job as a pass, so without this the verdict would stay green. |
| `.github/workflows/rtl-fast.yml` | regenerated by the generator only. Against dev, the jobs that differ are `yosys-tool` (new), `yosys-elaboration` and `rtl-fast` (above), `ci-manifest` (`needs` gains the job) and `ci-fail-fast` (`EXPECTED_JOBS` gains "Prepare pinned Yosys"). Every other job, `publication-census` included, and the other three workflows are byte-identical to dev. Round 2 changes only the two key lines. |
| `scripts/ci_fast_tool_selftest.py` (new) | the fast-tool controls, run by `scripts/ci_gate_workflows_selftest.py` in the hosted "CI scheduling and evidence controls" step. They moved out of that file because it crossed the 1000-line module limit; it is now dev's file plus one import and one call. See [New checks](#new-checks). |
| `docs/testing/CI_WORKFLOWS.md` | the tool job, exactly what its digest covers, and its evidence. Also: `publication-census`'s key sentence, the one key that differs under "Source-tool cache provenance", and the re-run-all rule after a failed cache save. Item 4 of the sequence pin, and its #406 summary, now state that a job or step list only the generator produces is held by the generated-graph comparison. For `rtl-fast.yml`'s two jobs it is also held by `fast_tool_retention`. |
| `docs/testing/TESTING.md:331` | R705-1-01's exact wording: "used a hosted `ubuntu-latest` runner, which resolved to the `ubuntu-24.04` image, and sequential `make -C` invocations." |

### Round 2 (R707-1)

- **R707-1-01 (MINOR): fixed at its cause.** Round 1 digested the template build step only. A workflow
  `env` entry, a job `env` on the consumer, a generator rewrite of the build or a budget-step export changed
  the build under an unchanged key. The digest is now taken over the emitted tool job, as described above.
  Make reads every environment variable as a variable of the same name. So the workflow `env` is digested
  whole: no entry can be shown unrelated, and a `VERILATOR_VERSION` bump rebuilds Yosys once.
- **R707-1-02 (MINOR): fixed at its cause.** `fast_tool_retention` holds both derived step lists whole
  against the template. `yosys-elaboration` must run every template step but the moved pair, in order and
  unchanged, with the one exact restore in the pair's place. `yosys-tool` must run exactly the checkout and
  the two moved steps.
- **R707-1-S1 (SUGGESTION): declined.** `lookup-only: true` would save about 5 s per hit on the tool job.
  It would make the moved cache step differ from the template's, which two judges deliberately refuse. act's
  cache server support for it is also unverified offline. The miss path is unchanged either way.

### New checks

`fast_tool_controls()` runs in the hosted "CI scheduling and evidence controls" step. "At `fddf3671`" means
the new control run against the round-1 generator.

**The key follows every build input.** Each edit must change the key, and the control names any edit that
does not.

| plant | at this head | at `fddf3671` |
|---|---|---|
| workflow `env` gains `CXXFLAGS: -O0` | key changes | unchanged: refused, named |
| `yosys-elaboration` job `env` `CXXSTD: c++23` | key changes; the tool job carries it | unchanged: refused, named |
| install transform rewrites the build's compile line | key changes | unchanged: refused, named |
| job budget step exports `CXXFLAGS` | key changes | unchanged: refused, named |
| the build runs `python3 scripts/ci_scope.py` | key changes and binds `hashFiles('scripts/ci_scope.py')` | no binding |
| template recipe edit; runner image | key changes | key changes |
| edit outside the build; edit of the tool job's `if` | key unchanged | key unchanged |

At `fddf3671` that control fails with "tool key unchanged by an edit of its build inputs: the workflow env,
yosys-elaboration's job env, an install-transform rewrite of the build, an export added to the job budget
step".

**Refusals by the generator:**
- a step between the build and the cache save: "yosys-tool: steps after the build that its key does not
  bind: Touch the built tree";
- a template consumer in a `container`: "yosys-elaboration: job keys the tool job does not carry into the
  build: container".

**On the generated graph:**
- a key without its script binding: "tool key does not bind the scripts its build steps run". At
  `fddf3671` the pristine head already fails this, naming `scripts/ci_install_cache.py`.
- a tool job under another `env`: "tool job env differs from yosys-elaboration's".
- A key `hashFiles` that names a workflow file or anything under `.github/` is still "tool key binds the
  workflow files".

**Retention (R707-1-02)**, on the derived jobs:

| plant | failing words |
|---|---|
| each of the 9 retained steps dropped in turn | "yosys-elaboration drops <step>" |
| a retained body rewritten | "yosys-elaboration changes Elaborate the integration-heavy tops" |
| a step added | "yosys-elaboration adds Planted step" |
| two retained steps swapped; one repeated | "yosys-elaboration reorders or repeats its retained steps" |
| the restore moved last, or accepting a miss | "yosys-elaboration's one exact restore is not in its build's place" |
| a consumer job key added | "yosys-elaboration's job keys differ from the template's" |
| a tool job step added; the tool build rewritten | "tool job steps are not the checkout and the two moved steps" |
| the real derivation patched to drop a self-test | "yosys-elaboration drops Prove the result cache refuses a planted entry" |

**Generator mutants, through all three hosted judges.** Each mutant edits `fast_yosys_tool` in a fresh
copy and regenerates. Then it runs `ci_gate_workflows.py --check`, `ci_gate_workflows_selftest.py` and
`ci_events.py --check`.

| mutant | `fddf3671` | this head |
|---|---|---|
| control | passes | passes |
| drop "Elaborate the integration-heavy tops" | killed incidentally | "drops Elaborate the integration-heavy tops" |
| drop the version proof | killed by a `list.index` crash | "drops Install the pinned Yosys and prove the version" |
| drop "Fetch RTL dependencies" | survives | "drops Fetch RTL dependencies" |
| drop "Prove the result cache refuses a planted entry" | survives | "drops Prove the result cache refuses a planted entry" |
| drop "Install the pinned sv2v release" | survives | "drops Install the pinned sv2v release" |
| drop each of the three ooc and guard self-tests | survives | "drops <step>" |
| swap the two ooc self-tests | survives | "reorders or repeats its retained steps" |
| an extra tool-job step | survives | refused by the generator |

**Resolved keys.** The planted edits were resolved as the runner resolves them, with `hashFiles` computed
over the files.
- At `fddf3671`, 8 edits change the build under an unchanged key: workflow `env` `CXXFLAGS`, `CXXSTD` and
  a new unrelated name; a consumer job `env`; an install-transform rewrite; a budget export; an edit of
  `scripts/ci_install_cache.py`; and a step after the build.
- At this head none does. The edit outside the build and the `if` edit keep the key, and the step after the
  build is refused.

Round 1's checks all remain. A key bound to the workflow files or missing its version, source, recipe or
image is refused. So are a tool-cache fallback, a tool job without its build, a raised timeout, a tool job on
another condition, a consumer that builds or lacks the need, a restore that accepts a miss, has a fallback or
restores another key, and a verdict without the need or the pair. The five template refusals also remain.
Hand edits of the generated `rtl-fast.yml` are still refused by `ci_gate_workflows.py --check` ("regenerate
the gate jobs") and `ci_events.py --check` ("generated gate jobs must match").

### Act replay

`scripts/act_ci.py` is unchanged; it is the same blob as dev's trusted runner. Rechecked offline at this head (`receipts/act-offline-mapping.txt`),
without Docker:
- the trusted runner's `validate_workflow_sandbox` accepts all four candidate workflows;
- the new job uses only `actions/checkout@v4` and `actions/cache@v4` on the pinned `ubuntu-24.04` label;
- the dependency stages place `yosys-tool` before `yosys-elaboration`, and that before `rtl-fast`;
- the plan names the job "Prepare pinned Yosys".

Round 2 adds a `hashFiles` call over one repository file to the key, which act evaluates on the checkout
like every other `hashFiles` key in these workflows. The live act replay of this head is owed to the merge
turn. With a miss now fatal, it must show act's cache server saving in `yosys-tool` and restoring in
`yosys-elaboration`.

### Hosted measurement

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


## Authoritative references

- #789 Decision and Acceptance. The assignment comments are issuecomment-6413044539 (round 1) and
  issuecomment-6415180907 (round 2).
- R707-1 (PR #794 issuecomment-6415176398) and R708-1 (issuecomment-6414349885).
- PR #788 review R705-1 (issuecomment-6411351133): R705-1-01 (the wording fix) and R705-1-02 (this defect).
- [CI workflow policy](../docs/testing/CI_WORKFLOWS.md): "Fast feedback", item 4 of the sequence pin,
  "Source-tool cache provenance", and "Act-first local replication".
- rtl-full's `yosys-tool` derivation, `separate_yosys_build` in `scripts/ci_suite_workflows.py`, as the model.
- The owner's 30-minute hosted budget (2026-10-14), as cited by #789.

## How to get into the same state

```sh
git fetch origin 789-yosys-tool-job
git switch --detach 1e0c5c09f6d5e41c8a80ec5e6179c1c762b94086
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
python3 -m pip install --require-hashes --no-deps -r ci/requirements-evidence.txt
python3 -m pip install --require-hashes -r tools/markdown/requirements.txt
```

## How to validate

```sh
python3 scripts/ci_gate_workflows.py --check
python3 scripts/ci_gate_workflows_selftest.py
python3 scripts/ci_install_cache_selftest.py
python3 scripts/generate_ci_evidence_pins.py --check
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/act_ci.py --selftest
install_dir="$(mktemp -d)"
install -m 0555 scripts/act_ci.py "$install_dir/act_ci.py"
python3 -I "$install_dir/act_ci.py" --selftest --worktree "$PWD"
rm -rf "$install_dir"
python3 scripts/check_py_idiom.py
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base 76de691e5625cc4ea2f9a19def9e07c1183a14ee
python3 scripts/check_doc_style.py
python3 scripts/gen_toc.py --check
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/check_doc_paths.py
```

Expected result / pass criteria:
- Every command exits 0.
- `ci_gate_workflows_selftest.py` prints 50 "Fast Yosys tool" lines, among them every refusal above. They
  end with `Fast Yosys tool: one cached build, an exact restore, a verdict that reads it PASS`, then
  `gate workflow and union controls: PASS`.
- `ci_events.py --selftest` prints `selftest: PASS (2199 contract items, 5258 arms)`.
- Both runner self-tests print `selftest: PASS`.
- `check_em_dash.py` reports 0 findings over 101 added lines.
- The rest of the "CI scheduling and evidence controls" list in the docs workflow also passes.

On the hosted run:
- "Prepare pinned Yosys" logs `Cache not found` for the new key on its first run, builds, and saves within
  30 minutes.
- `yosys-elaboration`'s "Restore the pinned Yosys build" logs `Cache restored from key:` with the same key
  and runs no build.

## Known limitations / out of scope

- **`publication-census` is unchanged**, by assignment ("do not touch any other job's behaviour"). It still
  builds Yosys under its own workflow-bound key, so a workflow edit rebuilds it cold. That took 26 min 55 s of
  its 45-minute timeout at `847eb4dd` (job 121450772909). Restoring from `yosys-tool` there is a candidate
  follow-up Issue.
- **Package versions follow the image label.** The image in the key is the pinned label `ubuntu-24.04` with
  `runner.os`, not the weekly image version. The distribution's package versions, the compiler's among them,
  are therefore not in the key. A binary built on one 24.04 image update is reused on the next, as before.
- **The digest over-approximates on purpose.** Any workflow `env` edit, a `VERILATOR_VERSION` bump included,
  rebuilds Yosys once, because make reads every environment variable. So does an edit of the job budget step
  or of `scripts/ci_install_cache.py`. A repository file the build's steps reach other than by a relative
  path in a run body is not detected; none does today.
- **`rtl.yml`'s derived jobs** are held whole only by the generated-graph comparison: its `yosys-tool`, the
  case-union jobs, and the rewritten shard workers and aggregate. A change to the generator regenerates past
  that comparison. This predates #789, is now stated in item 4 of the docs, and is a candidate follow-up
  Issue.
- **A failed cache save fails closed.** If the tool job's cache save does not complete, `yosys-elaboration`
  refuses on the miss. Re-run all jobs; re-running only the failed one repeats the refusal.
- **A build-input change is slower cold.** The rtl-fast critical path is then the tool job followed by
  `yosys-elaboration`, each inside its own 30 minutes. A workflow edit that reaches no build input no longer
  causes a cold build.
- **First dev push after merge.** It misses the new key once on `dev`, because PR-scoped caches are invisible
  to `dev`. The cold build then runs in the tool job.
- **The act replay is slower.** act runs dependency stages in sequence, so the replay adds about one
  `yosys-elaboration` run to its wall clock, and builds the tool cold in each replay.
- **No RTL changed**, so no Verilator, Yosys or Vivado bank was run.
- **`ci/image/tool-inventory.json` is not regenerated.** It already records stale workflow digests at dev, and
  its `--check` belongs to the image build.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (the live act replay is owed)
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

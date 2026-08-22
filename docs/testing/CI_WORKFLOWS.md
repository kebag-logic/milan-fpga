# CI workflow policy

The repository separates rapid pull-request feedback from exhaustive RTL
validation. This changes when hosted runners execute the long gates; it does not
reduce the local verification bar in [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Contents

- **[Fast feedback](#fast-feedback)** -- What runs on every pull-request update and why docs-only changes avoid RTL tool setup.
- **[Exhaustive validation](#exhaustive-validation)** -- When the full Verilator and Yosys inventories run and how exact-head evidence is preserved.
- **[Nightly and manual dispatch](#nightly-and-manual-dispatch)** -- The cron on the tip of `dev`, how to start a run by hand, and the two situations in which an agent should.
- **[One authoritative SHA](#one-authoritative-sha)** -- How every job of a run is pinned to one tree, what the workers record, what the aggregates refuse, and the gate that holds the files to this page.
- **[Elaboration](#elaboration)** -- The one job that installs LiteX and observes what elaboration hands the datapath Instance, and what makes it red.
- **[Pull-request state](#pull-request-state)** -- How draft and ready states control hosted long jobs without changing local responsibilities.
- **[Issue closing on merge](#issue-closing-on-merge)** -- What `Closes #N` does now that `dev` is the default branch, and what still waits for containment.
- **[Local commands](#local-commands)** -- The serial commands that remain the authoritative developer-side gates.
- **[Failure and cancellation semantics](#failure-and-cancellation-semantics)** -- How missing artifacts, superseded commits, and resumed work are handled.

## Fast feedback

[The fast RTL workflow](../../.github/workflows/rtl-fast.yml) runs on every
pull-request update and on every push to `dev`. It produces one stable
`rtl-fast` verdict from:

- conservative change classification;
- ratcheted whole-tree Verilator lint for RTL/tooling-relevant changes;
- BDD conformance;
- a Yosys/sv2v elaboration smoke for `milan_datapath`, `KL_pp_shadow`, and
  `KL_gptp_shadow` when RTL or its tooling changes.

A change containing only living documentation or an Issue template skips the
Verilator and Yosys setup jobs. The aggregate still completes, so a docs-only PR
does not leave a required verdict pending. Mixed changes are treated as RTL
relevant. An empty or unresolvable diff is also treated as RTL relevant. A
submodule pointer (`protocol-processor`, `gptp-processor`, `external`,
`third_party/...`, read from `.gitmodules`) or `.gitmodules` itself is never
docs-only: it moves the RTL the sweep elaborates without touching a file under
`hdl/`, and `scripts/ci_scope.py --selftest` proves a classifier that files
any one of them as documentation is rejected.

The elaboration smoke proves that the integration-heavy source lists lower and
resolve. It does not replace generic synthesis and must not be reported as a
portability pass.

## Exhaustive validation

[The exhaustive RTL workflow](../../.github/workflows/rtl.yml) runs when:

- a non-draft PR is opened or updated;
- a draft PR is marked ready for review;
- `dev` receives a push;
- the nightly schedule fires, at 01:17 UTC (`17 1 * * *`), on the tip of `dev`;
- someone dispatches it by hand, on any branch.

`dev` has been the repository default branch since 2026-08-22 (#174, decision
3; `main` is the release branch, fast-forwarded deliberately). GitHub runs
scheduled workflows from the default branch only, so the cron validates the
tip of `dev` as it stands at 01:17 UTC, and `workflow_dispatch` is launchable
for any branch. Both paths are in
[Nightly and manual dispatch](#nightly-and-manual-dispatch). Until 2026-08-22
the default was `main`, which carried neither trigger, and no scheduled or
dispatched run had ever occurred; the first scheduled run is recorded on #174.

The workflow keeps the public aggregate names `verilator-suites` and
`yosys-portability`.

Verilator runs the complete suite inventory on four workers. The aggregate
rejects missing, unexpected, or duplicate suite logs before it trusts the
combined tally. Specialized dependencies are installed only by their stable
owners: `tsn_fuzz` owns the pinned packet generator, and `chmap_capture` owns
the Yosys/sv2v netlist leg. The shard selector self-test pins both assumptions.

Yosys runs the complete top inventory on four weighted workers. The measured
heavy tops are isolated, while smaller tops are assigned with deterministic
longest-processing-time scheduling. Each worker uploads one result record per
top. The `yosys-portability` aggregate rejects:

- missing, duplicate, or unexpected top evidence;
- malformed or unreadable evidence;
- any failed or timed-out worker;
- a missing or failed blocking tied-input gate;
- structural-gate ownership that appears more than once.

The tap-purity report remains informational in the combined Yosys script, which
preserves the existing local policy. Its result is still recorded exactly once.

## Nightly and manual dispatch

**The nightly** validates whatever `dev` points at when the cron fires. Its
value is environment drift: the Verilator cache, the apt Yosys, the pinned
`tsn-gen` revision and the LiteX pins all move under a tree that did not, and
without the nightly the next pull request is the first thing to find out. A
red nightly on a tree whose last push was green is therefore a toolchain or
dependency finding, not a regression of the tree; file it as an Issue against
the pin or cache it names. `gh run list --workflow rtl.yml --event schedule`
lists the scheduled runs.

**Manual dispatch** starts the exhaustive workflow on the tip of a branch:

```sh
gh workflow run rtl.yml --ref <branch>
gh run list --workflow rtl.yml --event workflow_dispatch --limit 3
```

The run uses the `rtl.yml` of that branch and validates that branch's tip,
pinned as `GITHUB_SHA` like every other event; there are no inputs. Its
concurrency group is the branch ref, so a dispatched run neither cancels nor
is cancelled by a pull-request run of the same branch.

An agent uses dispatch in two situations:

1. **A draft head that needs exhaustive evidence without flipping ready.** The
   draft state is the cost lever: hosted workers stay idle while a PR is
   changing. When a draft needs the full inventory once, for example to
   measure a sweep before asking for review, dispatch on the branch instead of
   marking the PR ready and back.
2. **Recovery after a cancelled or expired run.** A ready PR whose last full
   run was cancelled by a later push that never completed, or whose artifacts
   have passed their 3-day retention, is re-validated on its exact head
   without an empty commit.

The merge bar reads exact-head evidence. A dispatched run names the SHA it
validated in its gate output and in both aggregate verdicts, so a reviewer
compares that line with the PR head before counting it.

**The default-branch assertion.** The cron was inert for three weeks because
the default branch was `main`, and no gate that reads files can see that
repository setting. So `full-ci-gate` reads it live on every run, with
`gh api repos/<owner>/<repo> --jq .default_branch` handed to
`scripts/ci_events.py --require-default-branch`, and prints
`default_branch=<observed> expected=dev event=<event>`. A scheduled or
dispatched run refuses to continue unless the observed value is `dev`, naming
the branch it saw; a value it could not read refuses too, since an unknown is
not agreement. A pull-request or push run prints the value and carries on:
those runs are about the tree, not the setting, and a contributor's PR must
not go red for a repository setting it cannot change. A drift is therefore
visible on every run and fatal on the first run it would misdirect, instead
of surfacing as a nightly that silently stopped. `ci_events.py --check` holds
the assertion in its fail-closed shape, which is exactly these four things:

1. **The script text.** The step's `run:` is pinned verbatim (whitespace
   aside) to three lines: `set -euo pipefail`, one unconditional
   `observed="$(gh api ...)"` read, one verifier call after it. A substring
   recognizer was fooled by a decoy, a literal `observed=dev` beside a
   `gh api` inside `if false`; the pin refuses it, and the structural reasons
   name what a deviation did: a second assignment, a value not sourced from
   the live call, control flow around the read, a comment line, the call
   before the read.
2. **The step keys.** The step carries exactly `name`, `env` and `run`, and
   its `env` exactly `GH_TOKEN`. A key beside a canonical script decides
   whether, on which events, or by which interpreter it runs: `if: false`,
   an `if:` naming only the events the assertion does not govern,
   `shell: bash -n {0}` (parsed, never executed), `continue-on-error`, a
   `working-directory`, or a `GH_HOST` / `GH_CONFIG_DIR` that points `gh`
   away from this repository. Each refusal names the key.
3. **The job keys.** `full-ci-gate` carries no `if`, no `continue-on-error`
   and no `defaults`, and the workflow carries no top-level `defaults` (a
   `defaults.run.shell: bash -n {0}` parses every script and executes none).
4. **The verifier steps.** Each aggregate's `--require-target-sha` step
   carries exactly `name`, `if`, `env` and `run`; its `if` is exactly
   `${{ always() }}` (any other condition can skip the verification, and a
   skipped step passes the job); its `env` exactly `GATE_SHA`; and its
   script equals a canonical form derived from the job's own download step
   and the worker matrix, so `--expect` is the shard count and no line can
   reassign a source before the call. The aggregate jobs keep their
   documented `if` verbatim and carry no `continue-on-error` or `defaults`.

`--selftest` covers, one at a time: the step removed, the token missing, the
live read replaced by an echo, the event not passed, `|| true`, the decoy
itself, a literal after the real read and after the call, `gh api` in a
comment only, `observed` from another command, two assignments, the call
before the read, an extra line, a missing `set` line; each key escape above
on the step, on the job, on the workflow and on the verifier steps; a
verifier that reassigns `GATE_SHA`, passes the wrong `--expect`, passes none,
or keeps `--expect` while the matrix grows; an aggregate `if` loosened or
dropped; a whitespace-only reformatting of both scripts that must still pass;
and the decision itself for every event class.

## One authoritative SHA

GitHub pins `GITHUB_SHA` once per run, for every event: the pushed commit, the
merge commit of a pull request, the tip of `dev` for a schedule, the tip of
the chosen ref for a dispatch. Every `actions/checkout` step that does not
override `ref` checks out that commit, so every job of an exhaustive run
validates one tree. The workflow makes that explicit and machine-checked
(#174, decision 2):

- the `full-ci-gate` job prints `event=... ref=... sha=...`, refuses a
  checkout whose `HEAD` is not `GITHUB_SHA`, and exports the SHA as its
  `target_sha` output;
- every Verilator and Yosys worker refuses to start unless its checkout, its
  `GITHUB_SHA` and the gate's `target_sha` are one value, then writes that
  value into a `TARGET_SHA` file beside its evidence, inside the artifact it
  uploads. The file is neither a `*.log` nor a `*.result`, so neither tally
  reads it;
- both aggregates run `scripts/ci_events.py --require-target-sha` over the
  downloaded shards before they tally anything, passing `--expect 4` (the
  worker matrix size) and exactly three sources, `--sha gate="$GATE_SHA"`
  (the gate's `target_sha` through the step env), `--sha run="$GITHUB_SHA"`
  and `--sha checkout="$(git rev-parse HEAD)"`, and print the SHA in their
  verdict. The verifier refuses any other source set, a dropped source or an
  unknown label included, and any shard-directory count but `--expect`, so
  an aggregate cannot quietly stop proving that the gate, the run and its
  checkout agree, or tally three shards as four.

The aggregates refuse, and the check fails rather than skips:

- a shard directory without a `TARGET_SHA` record, including the empty
  placeholder the aggregate creates when the download produced nothing;
- a record that is not a 40-digit hexadecimal commit id;
- a record naming any tree but this run's;
- a gate `target_sha`, aggregate `GITHUB_SHA` and aggregate checkout that are
  not one value, or a source set that is not exactly those three;
- fewer or more shard directories than the worker matrix produces.

`scripts/ci_events.py --check` holds the workflow files to this contract and
to the trigger contract above: no `actions/checkout` step in `rtl.yml`
overrides `ref`, every job that uploads an artifact records the SHA first,
every job that downloads artifacts verifies it, the gate carries the
default-branch assertion in its fail-closed shape, the trigger lists, the
`cancel-in-progress` rule and the public check names `rtl-fast`,
`verilator-suites`, `yosys-portability` and `elaborate` are what this page
says, and the cron time string on this page matches the YAML. Its
`--selftest` removes or alters each item on in-memory copies and requires
the check to catch every one, and fails if the checker is stubbed to find
nothing. Both run in the hosted docs job.

## Elaboration

[The elaboration workflow](../../.github/workflows/elaborate.yml) runs on every
pull-request update, on every push to `dev` and `main`, and on manual dispatch.
It is the one job that installs LiteX. It exists because no other job can
observe what elaboration hands `Instance("milan_datapath")` (#154): every
argv-to-parameter chain used to be proven by source-text greps against
`sw/litex/milan_soc.py`, and a flag severed on its way to the parameter it
names read green at two independent hops.

It uses the same change classification as the fast workflow. A docs-only
change skips every step after the classification and the `elaborate` check
still completes. A relevant change installs the pinned LiteX of
[`sw/litex/litex_pins.txt`](../../sw/litex/litex_pins.txt), places the
VexiiRiscv source at the revision LiteX itself pins, applies the patch series
in [`sw/litex/patches/`](../../sw/litex/patches/) with its `apply.sh`, and runs
`sw/builder/test_builder.py --require-elaboration`: gates 23f, 23g and 23h and
their mutation arms. Upstream LiteX elaborates no configuration in this tree
(#185), so the series is a required install step and gate 23h proves the
installed trees are upstream plus exactly that series.

Two caches, deliberately split. The Scala toolchain is content-addressed and
keeps a broad fallback. The generated CPU metadata does not: its key hashes the
configs, `milan_soc.py`, `build.sh`, `sweep.sh`, the pins and the patch series,
with no prefix fallback, because LiteX names those files from the CPU
arguments alone and skips the generator whenever the file exists, so a stale
entry would elaborate metadata built by the previous toolchain while reporting
green.

The `elaborate` check fails when no interpreter can import LiteX, when the
interpreter's VexiiRiscv rejects the `--l2-*` arguments the series adds, and
when any gate fails. A recipe recorded as unrunnable (#184's Arty leg) skips
only when it fails with exactly the recorded diagnostic, and the verdict names
every arm that did not run rather than claiming every arm ran.

## Pull-request state

Open implementation PRs as drafts while work is changing. The fast workflow
runs on each commit, while the hosted exhaustive jobs remain skipped.

Before marking a PR ready:

1. run the applicable focused tests;
2. run the complete local gates required by
   [CONTRIBUTING.md](../../CONTRIBUTING.md);
3. post exact commands and results on the PR;
4. ensure the current commit is the one intended for review.

Marking the PR ready starts the hosted exhaustive jobs on that exact head. A
later commit to a ready PR cancels obsolete work and starts a new full run.
Convert the PR back to draft before resuming exploratory implementation. Do not
claim hosted long-gate success for a commit other than the current PR head. A
draft that needs the exhaustive gates once is dispatched by hand (see
[Nightly and manual dispatch](#nightly-and-manual-dispatch)) rather than
flipped ready and back.

A docs-only ready PR remains cheap: the long workflow starts, classifies the
diff, and skips its RTL workers with explicit skipped results.

## Issue closing on merge

Since `dev` became the default branch on 2026-08-22, a PR body carrying the
GitHub keyword form `Closes #N` closes Issue N when the PR merges into `dev`.
The PR template therefore carries separate `Closes #` and `Relates to #`
lines; its former `Closes/relates to: #` line was not a form GitHub reads, and
a body written that way leaves the Issue open.

A closed Issue is not a finished one. The project board's Done transition
still waits for the post-merge containment check that
[CONTRIBUTING.md](../../CONTRIBUTING.md) requires, run when the branch has
stopped moving; an Issue the merge closed whose card is not Done is in that
window. `scripts/check_merge_review_integrity.py` keeps reporting a merged PR
whose linked Issue is open, for bodies in a form GitHub does not read and for
the history before 2026-08-22, when every PR merged into a non-default branch
and the keyword never fired.

## Local commands

Sharding is a hosted-runner scheduling detail. The no-option commands remain
complete serial local gates:

```sh
suite_logs=$(mktemp -d)
scripts/run_all_suites.sh "$suite_logs"
syn/yosys/run.sh
```

Useful read-only inspection commands are:

```sh
scripts/run_all_suites.sh --shard 0/4 --list
syn/yosys/run.sh --list
syn/yosys/run.sh --shard 0/4 --list
```

The elaboration gates run locally against any interpreter that imports
LiteX; without one they skip and the verdict says so:

```sh
MILAN_LITEX_PYTHON=$HOME/litex-milan/venv/bin/python3 \
  python3 sw/builder/test_builder.py --require-elaboration
```

The fast Yosys mode is diagnostic only:

```sh
syn/yosys/run.sh --mode elaborate --no-structural \
  --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
```

## Failure and cancellation semantics

A worker is not trusted merely because an aggregate job was able to download
something. Both aggregate jobs refuse evidence recorded for any tree but the
run's own (see [One authoritative SHA](#one-authoritative-sha)), compare
artifacts with the live repository inventory, and separately require every
worker result to be `success`.

Workflow concurrency is scoped to the PR or branch. A new commit cancels older
runs because their evidence no longer describes the current head. Converting a
PR to draft starts a no-op run in the same group, which releases hosted runners
from obsolete exhaustive work. A dispatched run and a scheduled run are scoped
to their branch ref, and a push to that branch cancels them the same way.

Push validation on `dev` checks the actual merge result. It complements, but
does not replace, the explicit post-merge containment check required by
[CONTRIBUTING.md](../../CONTRIBUTING.md).

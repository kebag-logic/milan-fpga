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
- **[Protected merge bar](#protected-merge-bar)** -- The active `dev` ruleset, its seven exact required contexts, and why its update policy is loose.
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
  `KL_gptp_shadow` when RTL or its tooling changes;
- the source-list checkers' own self-tests, and the two out-of-context read
  sets expanded for real, so a source `syn/yosys/run.sh` names and the tree no
  longer carries fails here rather than inside Vivado. Those read sets are
  printed by `run.sh --emit` rather than read out of it, and nothing in the
  record is filtered: a token that is not a `.sv`/`.v` source is refused, not
  dropped. The declaration of the top is resolved through `sv2v --top`, which
  this job installs, and through nothing else -- three models of the directive
  layer were each accepted and then broken by a construct they did not model
  ([R0] on PR #240, rounds one to three), so a missing front end is a refusal
  with no flag to soften it.

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
`yosys-portability`. Both are required contexts on `dev`: an RTL/tooling-
relevant PR must run them successfully, while a docs-only PR emits them as
explicit successful skipped results.

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
the assertion in its fail-closed shape. That shape is not only what the step
says: a check that reads a step's contents and nothing about the conditions
under which it runs holds the wrong perimeter, which is what #209 found. So it
is exactly these ten things:

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
3. **The job's run conditions.** `full-ci-gate` carries no `needs`, no `if`,
   no `continue-on-error` and no `defaults`, and the workflow carries no
   top-level `defaults` (a `defaults.run.shell: bash -n {0}` parses every
   script and executes none). `needs` is one of them because a job that needs
   another job is a dependent, and a dependent of a skipped job is skipped,
   taking every assertion inside it: a `noop` job carrying
   `if: ${{ github.event_name != 'schedule' }}` plus a `needs: [noop]` on the
   gate leaves every pinned character in place and stops the assertion running
   on the one event it exists for.
4. **The step sequence.** The gate job carries exactly four steps, in this
   order: the checkout with `fetch-depth: 0`, the pin step (`id: target`), the
   default-branch step, and the decision step (`id: gate`). The order is part
   of the contract, because the assertion runs the `ci_events.py` the checkout
   brought and the decision diffs the tree that checkout produced; the count is
   part of it too, because a step inserted anywhere runs before everything
   after it and can change what those steps read, and an entry appended to
   `GITHUB_PATH` puts another `gh` ahead of the runner's. A refusal names the
   position, what belongs there, and what it found.
5. **The sibling steps' keys.** The pin step, the decision step and the
   checkout are pinned to their own key sets exactly as the default-branch
   step is, so `if: false`, an `if:` naming only some events, a `shell:`, a
   `continue-on-error` or a `working-directory` on any of them is refused by
   name; the decision step's `env` is exactly `EVENT_NAME`, `PR_DRAFT` and
   `PR_BASE_SHA`, each bound to the source expression item 6 requires, and
   the checkout keeps `fetch-depth: 0` (the decision step
   diffs against the pull request's base commit, which a shallow clone does
   not carry). `if: false` on the pin step or on the decision step leaves the
   assert step's script canonical and publishes no `run_full` at all.
   Additionally, neither the workflow's top-level `env` nor `full-ci-gate`'s
   own names any `GH_*` variable: the step's `env` is pinned to exactly
   `GH_TOKEN`, but a `GH_HOST` or `GH_CONFIG_DIR` set at either level above it
   reaches the same `gh` without appearing anywhere in the step.
6. **The env bindings.** A pinned step's `env` is held as a name *and* the
   source expression that name is bound to, because the name is not the
   contract. The decision step carries
   `EVENT_NAME: ${{ github.event_name }}`,
   `PR_DRAFT: ${{ github.event.pull_request.draft }}` and
   `PR_BASE_SHA: ${{ github.event.pull_request.base.sha }}`; the
   default-branch step carries `GH_TOKEN: ${{ github.token }}`; each verifier
   step binds `GATE_SHA` to `full-ci-gate`'s `target_sha` output, derived from
   that job and output rather than restated. Names alone held nothing where it
   mattered: `PR_DRAFT: "true"` is valid workflow YAML that keeps all three
   names and all four keys and makes a ready RTL pull request publish
   `run_full=false`, on which both worker matrices skip, both aggregates skip
   under the no-op exception in item 8, and the skipped required contexts
   satisfy the ruleset -- a false green, not a refusal.
   `PR_BASE_SHA: ${{ github.sha }}` (a commit diffed against itself, so
   `rtl=false`) and `EVENT_NAME: pull_request` (a push, schedule or dispatch
   run taking the pull-request branch) arrive at the same place. A refusal
   names the step, the variable, the expression required and the one found.
7. **The decision step's script.** Pinned verbatim after whitespace
   normalization, the way the default-branch step's is, and refused by naming
   the first line that differs rather than dumping the script. The bindings in
   item 6 hold what the step reads; this holds what it does with what it read,
   because `run_full=true` rewritten to `run_full=false` changes no pinned
   name and no pinned key and publishes the explicit no-op on every ready RTL
   pull request. The structural reason is checked first: the selector's
   `--selftest` runs exactly once and before the script reads the selector's
   answer, so a selector is never trusted to decide a run without its own
   proof. Re-indenting the script or wrapping a continuation differently is
   the same script and still passes.
8. **The verifier steps.** Each aggregate's `--require-target-sha` step
   carries exactly `name`, `if`, `env` and `run`; its `if` is exactly
   `${{ always() }}` (any other condition can skip the verification, and a
   skipped step passes the job); its `env` exactly `GATE_SHA`; and its
   script equals a canonical form derived from the job's own download step
   and the worker matrix, so `--expect` is the shard count and no line can
   reassign a source before the call. The aggregate jobs keep their
   documented fail-closed `if` verbatim and carry no `continue-on-error` or
   `defaults`: they skip only when `full-ci-gate` succeeded and explicitly
   published `run_full=false`; any other selector result runs the aggregate
   into the SHA/shard refusal path.
9. **The published outputs.** `full-ci-gate`'s `outputs` map is a
   NAME to EXPRESSION mapping exactly as a step's `env` is, and it is held by
   the same comparison: exactly `run_full`, `rtl` and `target_sha`, bound to
   `${{ steps.gate.outputs.run_full }}`, `${{ steps.gate.outputs.rtl }}` and
   `${{ steps.target.outputs.target_sha }}`, each derived from the step that
   computes it rather than restated. This is the publication path, and it is
   not the same object as item 7: no downstream job reads the decision step's
   output, they read `needs.full-ci-gate.outputs.run_full`, which is this
   map. Checking only that `target_sha` existed therefore held nothing where
   it mattered, because `run_full: ${{ 'false' }}` is valid job-output YAML
   that leaves every pinned step key, every env binding and every character
   of the decision script in place while the job exports the literal `false`:
   both worker matrices skip, both aggregates skip under the item 8 no-op
   exception, and the skipped required contexts satisfy the ruleset. A
   refusal names the job, the output, the expression required and the one
   found.
10. **The consumers of that decision.** Every job that needs `full-ci-gate`
    carries a pinned `if`, with no residue. The workflow's aggregate is the
    job whose display name is the public required check the merge bar reads,
    and it carries the fail-closed `if` of item 8; every other job that needs
    the gate is a consumer, and carries exactly
    `${{ needs.full-ci-gate.outputs.run_full == 'true' }}` and no
    `continue-on-error` or `defaults`. A job added later that depends on the
    gate lands in the consumer class and is refused until it carries that
    `if`, so this perimeter is closed under addition rather than being a
    list of the escapes earlier rounds happened to find. The closure runs in
    both directions ([R2] on PR #239): every job an aggregate lists in its
    own `needs` is classified too, as the selector, as a consumer, or as a
    held contributor that carries no `needs`, `if`, `continue-on-error` or
    `defaults` of its own. A job wired straight into an aggregate without
    needing the selector, as `bdd-conformance` is, previously landed in no
    class, so an `if: false` on it retired the specification suite with
    every hosted context green and the aggregate accepting the skip.
    Separately, no expression anywhere in either RTL workflow may read an
    output a job does not publish, and no static `needs` chain of any kind,
    `.result` as well as `.outputs.<name>`, may name a job the reader does
    not list in `needs`: each mistake evaluates to the empty string, so
    every comparison against it is false and every step or job gated on it
    skips. The audit resolves GitHub's dotted, bracket and mixed static
    spellings --
    `needs.<job>.outputs.<name>`, `needs['job'].outputs.name` and
    `needs['job']['outputs']['name']` -- as the same reference. A dynamic
    `needs[...]` access is refused because the producer and output cannot be
    proved statically.

    `rtl-fast.yml` publishes the same shape, from its `changes` job to
    `verilator-lint` and `yosys-elaboration`, and is held by the same check.
    Its aggregate counts a skipped consumer as a pass on purpose, since a
    docs-only change legitimately runs no RTL lint. Therefore the producer is
    held too: `changes` carries no `needs`, `if`, `continue-on-error`,
    `defaults` or job-level `env`; the workflow carries no top-level
    `defaults`; and its exact
    two-step sequence is `actions/checkout@v4` with full history followed by
    the `scope` step. That step's keys and three env bindings are pinned, and
    its normalized canonical script must self-test `ci_scope.py`, derive the
    conservative changed-file set, read the selector answer and publish that
    answer. An empty or forced-false publication can no longer skip both RTL
    consumers into the accepted docs-only path.

    The verdict half of the fast lane is held the same way ([R2] on PR
    #239). Because the aggregate runs under `always() && !cancelled()`, its
    one verdict step is the entire conversion of four job results into the
    required `rtl-fast` context, and an `if` on that step, a result binding
    rebound to the literal `success`, or a `case` widened to
    `success|skipped|failure` each turned a FAILED fast job into a green
    required context while every job key stayed canonical. So the aggregate
    must list every other job of the workflow in its `needs`, which also
    refuses an entry quietly dropped from the verdict; its single step
    carries exactly `name`, `env` and `run`; its env is derived from that
    `needs` list, one `<JOB>_RESULT` name per needed job bound to
    `${{ needs.<job>.result }}`; and its normalized script equals the
    canonical form derived from the same list, whose `case` accepts exactly
    `success` and `skipped`. Each public check name (`verilator-suites`,
    `yosys-portability`, `rtl-fast`, `elaborate`) must be carried by exactly
    one job, so a second job renamed to a required name cannot make the
    ruleset's binding ambiguous.

`--selftest` covers, one at a time: the step removed, the token missing, the
live read replaced by an echo, the event not passed, `|| true`, the decoy
itself, a literal after the real read and after the call, `gh api` in a
comment only, `observed` from another command, two assignments, the call
before the read, an extra line, a missing `set` line; each key escape above
on the step, on the job, on the workflow and on the verifier steps; the gate
given a `needs` on a job that skips on `schedule`; `if: false`, an event-only
`if`, a `shell:`, a `continue-on-error`, a `working-directory` and a dropped
env key on the pin and decision steps; `PR_DRAFT` forced to `true`,
`PR_BASE_SHA` rebound to `${{ github.sha }}`, `EVENT_NAME` hard-coded to
`pull_request`, `GH_TOKEN` rebound to another token and a verifier's
`GATE_SHA` rebound to its own run; the decision script rewritten to publish
`run_full=false` always and stripped of the selector's self-test; the assert
step moved before the
checkout; a `GITHUB_PATH` step inserted before it; the pin step removed; the
pin and assert steps swapped; a checkout without `fetch-depth: 0`; a `GH_HOST`
on the job and on the workflow; a shard denominator restated below its matrix
size, restated while the matrix grows, and stale in a worker's display name; a
verifier that reassigns `GATE_SHA`, passes the wrong `--expect`, passes none,
or keeps `--expect` while the matrix grows; an aggregate `if` loosened or
dropped; the gate's `run_full` and `rtl` outputs each rebound to a literal
`false`, `run_full` rebound to the scope answer, `target_sha` rebound to the
run's own SHA, each of the three dropped, the whole map dropped and a surplus
output added; a worker gated on an output nobody publishes, on `if: false`, on
a value the decision never takes, made `continue-on-error`, given a
`defaults.run.shell`, or reading the gate's output without needing the gate; a
new job that depends on the gate and gates on nothing; in `rtl-fast.yml`, the
`changes` selector's `rtl` output rebound to a literal and dropped, and its two
consumers gated on a misspelt output and on `if: false`; the `changes` job and
scope step each given `if: false`, the job made `continue-on-error`, the scope
env rebound, the scope script made to export `rtl=false` and stripped of its
self-test, checkout/scope swapped, checkout made shallow, and a workflow
`defaults.run.shell` inserted; dotted/bracket, all-bracket and mixed
`needs...outputs` references to missing dependencies or outputs, plus a
dynamic bracket reference; the fast verdict step given `if: false`, a
`shell` and a `continue-on-error`, its lint result binding rebound to the
literal `success`, and its `case` widened to accept `failure`;
`bdd-conformance` dropped from the aggregate's `needs` and a new fast job
left outside them; `bdd-conformance` itself given `if: false`, a
`continue-on-error` and a `defaults.run.shell`; a `.result` read from a job
outside `needs`, in the dotted and in the bracket spelling; `verilator-lint`
renamed to the public name `rtl-fast`; a job-level `env` on the fast
selector; a whitespace-only reformatting of all five
canonical scripts that must still pass; and the decision itself for every
event class.

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

The shard count is stated once, by each worker's `strategy.matrix.shard` list.
The worker passes `--shard ${{ matrix.shard }}/${{ strategy.job-total }}` and
names itself the same way, so growing that list moves the split with it, and
`--check` derives the aggregate's `--expect` from the same list rather than
reading a number written beside it. A restated denominator is refused, whether
it appears in a script or in a job name: with a matrix of five and a literal
`/4`, shard 4/5's suites and tops are never produced while `--expect`, the
uploaded artifact count and the downloaded shard count all still agree.

The aggregates refuse, and the check fails rather than skips:

- `full-ci-gate` fails, is cancelled, or does not publish an explicit
  `run_full` result (only a successful `run_full=false` decision may skip an
  aggregate);
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
`cancel-in-progress` rule and the public aggregate names `rtl-fast`,
`verilator-suites`, `yosys-portability`, and `elaborate` are what this page
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
diff, and skips its RTL workers with explicit skipped results. The two stable
aggregate contexts are still emitted, so the ruleset never waits for a check
name that the pull request cannot produce.

## Protected merge bar

The active repository ruleset named `dev merge bar` applies only to
`refs/heads/dev`. It has no bypass actor and enforces four rules:

- changes arrive through pull requests;
- branch deletion is forbidden;
- non-fast-forward updates are forbidden;
- these seven exact status-check contexts are required: `rtl-fast`,
  `docs-check`, `wire-accountability`, `docs-check-no-git`, `elaborate`,
  `verilator-suites`, and `yosys-portability`.

Required checks use the loose policy: an intervening merge to `dev` does not
force the PR to rerun the 23--26 minute `milan_datapath` Yosys job merely to
become current with the base. Reviewers still own exact-head and candidate-
merge validation under [CONTRIBUTING.md](../../CONTRIBUTING.md).

Conditional job skipping is part of the contract. A documentation-only PR
must emit the two exhaustive aggregate checks as skipped and must complete the
fast aggregate and `elaborate` check after their expensive steps skip. That is
permitted only when `full-ci-gate` itself succeeds and explicitly publishes
`run_full=false`; a gate failure, cancellation, or missing output makes both
aggregates run and fail on absent evidence, because a skipped required job
would otherwise satisfy the ruleset. Do not add workflow-level `paths`,
`paths-ignore`, or branch filtering to any required context: a workflow that
never starts leaves its required name pending. The three documentation jobs
are independent required siblings, so a failure in `wire-accountability` or
`docs-check-no-git` blocks the PR even when `docs-check` itself succeeds.

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

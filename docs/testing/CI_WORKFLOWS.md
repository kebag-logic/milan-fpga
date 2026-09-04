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
- **[Act-first local replication](#act-first-local-replication)** -- The required exact-head local response while hosted Actions runs in parallel.
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

Yosys runs the complete top inventory on four weighted workers, under the
pinned toolchain the workflow declares: `YOSYS_VERSION` names the one Yosys
the gate's verdict is taken with, built from the upstream tag with its bundled ABC
submodule on a cache miss and proved by a version step that fails on any
other binary, and the sv2v release install is verified against the SHA-256
recorded in the workflow text (#287). The measured
heavy tops are isolated, while smaller tops are assigned with deterministic
longest-processing-time scheduling. Each worker uploads one result record per
top. The `yosys-portability` aggregate rejects:

- missing, duplicate, or unexpected top evidence;
- malformed or unreadable evidence, including a PASS top record without a
  numeric `cells` count (`cells=?` was every CI record's value for as long
  as the column existed, and nothing refused it — #287);
- any failed or timed-out worker;
- a missing or failed blocking tied-input gate;
- structural-gate ownership that appears more than once.

The tap-purity report remains informational in the combined Yosys script, which
preserves the existing local policy. Its result is still recorded exactly once.

## Nightly and manual dispatch

**The nightly** validates whatever `dev` points at when the cron fires. Its
value is environment drift: the Verilator and Yosys build caches (both tools
are pinned and version-verified, so the drift a nightly can find is the
cache or its build inputs, not the version), the jemalloc preload (a speed
choice `syn/yosys/run.sh` makes only when the
library is installed, never a pass criterion), the hash-locked HDL reference
parser install,
the pinned `tsn-gen` revision and the LiteX pins all move under a tree that
did not, and
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
is exactly these twelve things:

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
4. **The step sequence.** The gate job carries exactly five steps, in this
   order: the checkout with `fetch-depth: 0`, the pin step (`id: target`), the
   default-branch step, the contract step, and the decision step
   (`id: gate`). The order is part
   of the contract, because the assertion runs the `ci_events.py` the checkout
   brought and the decision diffs the tree that checkout produced; the count is
   part of it too, because a step inserted anywhere runs before everything
   after it and can change what those steps read, and an entry appended to
   `GITHUB_PATH` puts another `gh` ahead of the runner's. A refusal names the
   position, what belongs there, and what it found. The contract step is
   this gate's SECOND hosted runner (#261, maintainer review on PR #293):
   its script is exactly `python3 -m pip install --quiet pyyaml` followed by
   `python3 scripts/ci_events.py --check`, its keys exactly `name` and `run`,
   and it is refused when removed, given an `if`, a `continue-on-error`, a
   `|| true`, or moved behind the decision. It exists because `docs-check`
   cannot police itself: every job-level lever that neuters that job
   (`if: false`, a `needs` on a skipped job, `continue-on-error`,
   `defaults.run.shell: bash -n`) also prevents or neuters the one step in
   docs.yml that would have refused it, and a skipped or falsely green
   required context satisfies the ruleset. This job cannot be neutered the
   same way: a gate that is skipped or fails makes both required aggregates
   fail closed (item 8), so the finding reaches the merge bar from a job
   docs.yml does not gate. Measured under act: `if: false` on `docs-check`
   fails the contract step, `full-ci-gate` fails, and both aggregates fail on
   the absent gate.
5. **The sibling steps' keys.** The pin step, the contract step, the
   decision step and the
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
   reaches the same `gh` without appearing anywhere in the step. Item 12 widens that from `GH_*` to every name at every level.
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
    `yosys-portability`, `rtl-fast`, `elaborate`, `docs-check`,
    `wire-accountability`, `docs-check-no-git`) must be carried by exactly
    one job, so a second job renamed to a required name cannot make the
    ruleset's binding ambiguous. The rule reads a job's `name` as a literal,
    and GitHub evaluates it as an expression, so a `name` containing `${{`
    is held too ([R4] on PR #293): it may reference nothing but
    `${{ matrix.<key> }}` lists of the job's own literal `strategy.matrix`
    -- the sharded workers' `Verilator shard ${{ matrix.shard }}/${{
    matrix.total }}` is the shape this tree carries -- every rendering is
    enumerated and refused if it equals a required name in any file, and
    any other expression (`${{ 'docs-check' }}`, a `github`, `vars` or
    `needs` context, a matrix carrying `include`/`exclude` or built by
    `fromJSON`, a referenced key that is not a non-empty list of literal
    scalars, a `${{` the expression scan does not match) is refused
    outright because it cannot be enumerated here. The lists must be
    literal to the last character: the runner evaluates `strategy` before
    the matrix expands, so `n: ["${{ 'docs-check' }}"]` under
    `name: ${{ matrix.n }}` publishes the required name while an
    enumeration would see the text ([R3] round 4 on PR #293).
    `name: ${{ 'docs-check' }}` on a `run: true` job published a second
    check run under a required name that no literal comparison saw, in all
    four workflow files. And the count is per name, not per file: a job in
    any of the four files whose display name is a required name another
    workflow owns is refused, because the merge bar binds the name and a
    docs.yml job literally named `elaborate` is a second `elaborate` on
    every pull request the two workflows share ([R4] round 2 on PR #293).
    Nor is it per inventory (maintainer review on PR #293): the reader
    lists every `.yml`/`.yaml` under `.github/workflows/`, inventoried or
    not, parses each, and builds one map from required name to
    `(file, job id)` over all of them; each of the seven names must map to
    exactly one entry, in its owning file, under its own id, and a job in
    an un-inventoried file may carry no expression `name` at all, because
    nothing outside the inventory is legitimately named by one. A fifth
    file carrying `docs-check` -- which GitHub runs and binds all the same
    -- was invisible to the four-file inventory and is refused naming the
    file and the job.
11. **The non-RTL required contexts.** `docs-check`, `wire-accountability`,
    `docs-check-no-git` and `elaborate` are four of the seven names the merge
    bar reads, and their workflows have no aggregate: the carrier job IS the
    required context, and a skipped required context satisfies the ruleset.
    Both workflows sat outside items 1--10 (#261, found by the round-6 review
    of PR #239): `if: false` on `docs-check` retired this gate itself, since
    docs.yml was then the only workflow that ran `--check` (the gate job of
    rtl.yml is the second runner since PR #293, item 4), and
    `continue-on-error` on `elaborate` retired the elaboration gate, each
    with `checked=171 findings=0`. So the job carrying each of those names is
    held at the job level exactly as an RTL contributor is: no `needs`, no
    `if`, no `continue-on-error`, no `defaults`, and no top-level `defaults`
    on the workflow, each refusal naming the job and the key. The builder
    contract already held `docs-check` and `elaborate` for its own reason;
    the rule now reaches `wire-accountability` and `docs-check-no-git`,
    which no builder step touches, and the three documentation names join
    the one-carrier rule of item 10. The name and the content are held on
    ONE job ([R3] on PR #293): the merge bar binds a display name, the
    content checks read `docs-check` and `elaborate` by job id, and held
    apart the real job renamed to `docs-check-real` beside a `run: true`
    job named `docs-check` passed with no finding -- the unique carrier had
    no neuter key, the id-named job kept its pinned steps, and the required
    context ran nothing. So the job whose id is the public name must carry
    it. The gate step inside each of the four jobs is pinned too (#295,
    the [R3] measured levers on PR #293): `docs-check`'s ci_events step,
    `wire-accountability`'s gate step and `docs-check-no-git`'s single
    step each carry exactly `name` and `run` and a script equal to its
    canonical form after whitespace normalization, so a step-level `if`,
    `shell`, `continue-on-error` or `working-directory`, and a `|| true`
    or any other rewrite beside the call, is refused naming the step;
    `elaborate`'s scope step is held as the decide step is (item 7, the
    #209 precedent) -- keys exactly `name`, `id`, `env` and `run`, its two
    env bindings pinned to their source expressions, `ci_scope.py
    --selftest` exactly once and before the script reads the selector's
    answer, and the whole script canonical -- so `if: false` on the step
    that publishes the output every elaboration gate's guard reads, a
    script rewritten to publish a literal `rtl`, and a dropped self-test
    are each refused. Each gate step must also be PRESENT exactly once in
    the job of the required id: a job body replaced wholesale by
    `run: true` with the real body's id renamed away, a removed gate
    step, or an appended duplicate `X:` mapping -- which PyYAML parses
    last-wins, so the id-named job IS the stub -- is refused naming the
    job, and the self-test proves the last-wins parse on a real appended
    duplicate on disk. And each carrier's whole step list is pinned the
    way item 4 pins the gate job's: count, order, each step's identity
    (its literal `name`, or its `uses`), each step's exact key set and
    env bindings, each recorded `if` verbatim (the scope guard on
    `elaborate`'s gated steps, `always()` plus the guard on its cache
    write-back) and each recorded `with` mapping exactly, so a `run:` or
    `uses:` step inserted anywhere in the four jobs -- a `BASH_ENV`
    written to `$GITHUB_ENV`, a `$GITHUB_PATH` prepend, a third-party
    action, or any content at all -- is refused naming the job and the
    position, as are a removed, reordered or renamed step, a loosened
    step `if`, and a rewritten cache or upload `with`.
12. **The inherited execution environment.** None of the keys above is
    `env`, and a name set at the workflow or job level reaches every step's
    shell before any pinned script runs: `BASH_ENV` names a file bash
    sources at the start of every non-interactive shell -- which a `run:`
    step is -- so `env: BASH_ENV: scripts/ci-bypass.sh` with a checked-in
    file holding `python3() { return 0; }` turned every python gate of every
    protected job, the gate's contract step included, into a no-op with
    every pinned key and script character in place and the required context
    green (maintainer [R0] on PR #293). A blacklist of known names is the
    wrong shape, because the runner's shell honours more than this page can
    enumerate, so the environment is held by exact allowlist at all three
    levels, in every one of the four files: the workflow-level `env` names
    exactly what the tree carries today (`VERILATOR_VERSION` and
    `TSN_GEN_REV` in the exhaustive workflow, `VERILATOR_VERSION` in the fast
    one, nothing in the other two); no job carries a job-level `env`; and
    the names a job's steps bind stay inside that job's recorded set (the
    gate's four, the workers' shard and target names, the aggregates'
    `GATE_SHA` and `SHARD_RESULT`, the selectors' event names, the verdict
    step's result bindings, `elaborate`'s scope pair, and nothing in the
    documentation jobs). Each refusal names the scope, the job or step, and
    the surplus names. Measured under act: a job-level `BASH_ENV` on
    `docs-check` makes that job's own gates green and `full-ci-gate`'s
    contract step refuse it, so both required aggregates fail. Declared
    `env` is not the only key that reaches those shells ([R4] round 6 on
    PR #293): `jobs.<id>.container` carries its own `env` map and chooses
    the image every step's `python3` comes from, `services` starts more of
    them, a step's `shell` picks the interpreter, and GitHub can add a key
    tomorrow. So the KEY SETS are held the same way: a workflow may carry
    only `name`, `on`, `concurrency`, `env` and `jobs`; a job only `name`,
    `runs-on`, `timeout-minutes`, `steps`, `needs`, `if`, `outputs` and
    `strategy` -- and that rule reaches EVERY job, an added standalone one
    included: `defaults` and `continue-on-error` are refused here as well
    as by the per-class rules, because those classify only the jobs they
    know, and a new job carried either with no finding (maintainer [R0]
    round 4 on PR #293); a step only `name`, `run`, `uses`, `with`, `id`, `env`,
    `if`, `continue-on-error` and `working-directory` -- what the tree
    carries today -- and a surplus key is refused by name whatever it does.
    The runner sets the same inherited environment from INSIDE a job too
    ([R3] round 8 on PR #293): any `run:` step may write `$GITHUB_ENV` or
    prepend `$GITHUB_PATH` for every later step, and a local `./` or
    third-party `uses:` runs code this page never reads; one added line in
    any job without a pinned sequence set `BASH_ENV` at run time with every
    declared level clean. So those are held by allowlist as well: exactly
    four recorded steps may mention either file (the two Verilator PATH
    steps, the tsn-gen `TSN_GEN_ROOT` export, the sbt PATH step), each
    bound by its normalised SCRIPT and appearing exactly once in its job --
    a name alone let the writer's own script gain a hostile line, and an
    added step under a recorded name write anything ([R3] round 9 on PR
    #293) -- every other mention is refused naming the step, a `uses:`
    outside the five recorded `actions/*` versions is refused, every
    checkout's `with` may carry nothing but `fetch-depth: 0`, a job may
    carry `outputs` or `strategy` only where the tree records it, a step may
    carry `working-directory` only on the one step that records it and
    only with its recorded value -- the behave step, `tests`; anywhere else
    the key, and on that step any other value, redirects a gate to a
    checked-in decoy tree ([R4] round 7, [R3] round 10 on PR #293) -- and a
    non-mapping `env` is refused at every level. #295 closed the step-list
    class for the four non-RTL carriers (item 11): their step lists are
    pinned by count, order, identity, key set, recorded `if` and recorded
    `with`, so an inserted step of ANY content -- one reaching the
    runner's environment file without spelling its name included (the
    `_runner_file_commands` glob, an indirect expansion, a checked-in
    script) -- is refused there naming the job and the position, and so is
    an `if: false` on any of their steps. What this still cannot hold is
    the same class in the seven RTL jobs whose step lists are not pinned
    the way the gate's is (item 4) -- the two shard workers, the two
    exhaustive aggregates, `verilator-lint`, `yosys-elaboration` and
    `bdd-conformance` -- where an inserted step that stays inside every
    allowlist above still passes, and the CONTENT of the recognised
    non-gate steps in the four carriers: `docs-check`'s gates other than
    the ci_events step (`docs_check`, `check_feature_status`, the
    traceability matrix, the builder gates and the rest) can still be
    rewritten or swallowed with the context green, and the second runner
    backs up only `ci_events --check`. A sequence-and-content pin on
    every job closes that; it is #295's widened acceptance row and stays
    open there.

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
on the job and on the workflow; a shard denominator missing or stale in its
matrix carrier, restated while the shard list grows, and stale in a worker's
display name; a
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
selector; each of `docs-check`, `wire-accountability`, `docs-check-no-git`
and `elaborate` given a job-level `if: false`, a `continue-on-error` and a
`needs`, the two the builder contract never touches given a
`defaults.run.shell` too, a second job carrying each of the four names,
each documentation carrier renamed, each of the four carriers renamed
away while a `run: true` job takes its name, a fifth workflow file carrying
`docs-check` by name and `elaborate` by job id and naming a job by an
expression -- in the parsed world and, for the directory scan itself, as a
real file beside copies of the five, with an unparseable one refused as
cannot-run -- the gate's contract step removed, given `if: false`, given a
`continue-on-error`, made to swallow its exit status and moved behind the
decision, a job-level `BASH_ENV` on `docs-check`, `wire-accountability`,
`elaborate` and `full-ci-gate`, a benign job-level name, a workflow-level
`BASH_ENV` on docs.yml and rtl.yml, a benign workflow-level name on
rtl-fast.yml, a step-level `BASH_ENV` on the docs ci_events step, the
elaborate builder call and the wire-accountability gate step, a `container`
with its own `BASH_ENV` on `docs-check`, `full-ci-gate` and `elaborate`,
`services`, an `Env:` spelling, a benign job key, a workflow-level
`defaults`, a step `shell` and a benign step key, an inserted step writing
`$GITHUB_ENV` or `$GITHUB_PATH` in a documentation job and in an RTL
worker, a write added to an existing step, a recorded writer renamed, a
local and a third-party `uses:`, a recorded writer's script given a hostile
line and the tsn-gen export rewritten, an added step under a recorded name,
a recorded writer duplicated, a checkout given `ref` and `repository`, a
`strategy` and an `outputs` on a documentation job, a `working-directory`
on the docs ci_events step and on the other behave-job step, the behave
step pointed at a decoy tree, a non-mapping `env` at
the workflow and step level, a fifth workflow file on disk under both
suffixes as a literal pair, a decoy whose `name` is an
expression evaluating to a required name in each of the four files, a
matrix job whose `name` renders one (its own file's and another file's), and
the enumeration's edges - a matrix value that is itself an expression, an
unmatched `${{`, `include`, a `fromJSON` matrix, a missing key, an empty
list - and a literal decoy carrying a required name another file owns, in
each of the four files; each of the four non-RTL gate steps (`docs-check`'s
ci_events step, `wire-accountability`'s gate step, `docs-check-no-git`'s
single step, `elaborate`'s scope step) given an `if: false`, a
`continue-on-error`, a `shell`, a `working-directory` and a `|| true`, and
each removed; the elaborate scope script made to publish a literal
`rtl=false`, stripped of its `ci_scope.py --selftest`, running the
self-test after the answer is read, and its two env bindings rebound; each
of the four carriers' bodies replaced by a `run: true` stub behind a
renamed-away id and by a duplicate mapping's last-wins parse, plus an
appended duplicate `wire-accountability:` and `elaborate:` mapping as a
real file on disk; a `BASH_ENV`-writing, a `$GITHUB_PATH`-prepending, a
third-party-`uses:` and a benign step inserted into the four carriers, a
recognised step removed, swapped and renamed, a non-gate carrier step
given `if: false`, a gated `elaborate` step's `if` loosened, and a cache
and an upload `with` rewritten; a whitespace-only reformatting of all
nine canonical scripts that must still pass; and the decision itself for
every event class.

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

The shard count is defined by each worker's `strategy.matrix.shard` list and
carried into the jobs by the singleton `matrix.total` dimension. The worker
passes `--shard ${{ matrix.shard }}/${{ matrix.total }}` and names itself the
same way. `--check` requires that singleton to equal the shard-list length and
derives the aggregate's `--expect` from the list. It refuses a missing or stale
total and any literal or `strategy.job-total` denominator in a script or job
name. With a matrix of five and a stale total of four, the check fails before
shard 4/5's suites or tops can be omitted while the artifact counts agree.

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
nothing. `--check` runs in the hosted docs job and, since PR #293, in the
gate job of the exhaustive workflow (item 4 below); `--selftest` runs in the
docs job only, so the vacuity control has one hosted runner.

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
in [`sw/litex/patches/`](../../sw/litex/patches) with its `apply.sh`, and runs
`sw/builder/test_builder.py --require-elaboration`: gates 23f, 23g and 23h and
their mutation arms. Upstream LiteX elaborates no configuration in this tree
(#185), so the series is a required install step and gate 23h proves the
installed trees are upstream plus exactly that series.

After those gates the same job runs `scripts/run_litex_sims.sh`, the one
aggregate that owns the standalone LiteX simulations in `sw/litex/` (#297):
its inventory is pinned in the runner and reconciled against the directory in
both directions, so a deleted test cannot vanish silently and an unlisted new
one is a red run, and its `--selftest` executes first - it plants a failing
simulation, a masked verdict, a missing member and an unlisted extra in a
sandbox and requires red each time. The aggregate reuses the interpreter this
job just installed and patched; locally the same command runs against any
interpreter that imports `migen` + `litex` and otherwise declares its skips
(exit 90), see [TESTING.md section 2](TESTING.md#2-litex-integration-checks---swlitextest_py).

`actions/checkout` does not populate submodules. Both this job and the hosted
`docs-check` job run the full builder, whose source gates consume
`protocol-processor`, `gptp-processor`, and the five shipping primitives under
`third_party/verilog-axis`. Each job therefore initializes exactly those three
trees in one step before its builder call; the elaboration setup step carries
the same live RTL-scope `if` as the call. `scripts/ci_events.py --check` pins
checkout-before-setup-before-call order, the event-pinned checkout shape and
action version, the exact setup and builder commands, their execution controls,
and the complete dependency set. Its mutation suite independently removes every
tree, redirects or disables checkout, moves setup on either side of that order,
and disables or replaces the setup and builder calls. A local run with an
already initialized worktree is not evidence that a fresh hosted checkout has
the sources. The same contract pins one exact sv2v v0.0.12 install per
builder job — release artefact checksum included: the script verifies the
zip against the SHA-256 recorded in the workflow text before installing
(#287) — before the call and under the elaboration job's live RTL-scope
`if`: `dp_srcs.py` refuses to resolve a top without a front end, so a runner
without sv2v turns the builder gate red rather than green, and the mutation
suite drops the install, drifts its version, moves it after the call, and
disables its condition.

Three caches, deliberately split. The Scala toolchain is content-addressed
and keeps a broad fallback. The pip download cache is keyed on the pin file
with a prefix fallback and runs only under the RTL scope, safe because the
pins are full-SHA git revisions: pip keys the wheels it builds from them on
the exact URL and SHA, so a cache entry can only save the rebuild, never
substitute a revision. The generated CPU metadata keeps neither fallback: its key hashes
the configs, `milan_soc.py`, `build.sh`, `sweep.sh`, the pins and the patch
series, because LiteX names those files from the CPU arguments alone and
skips the generator whenever the file exists, so a stale entry would
elaborate metadata built by the previous toolchain while reporting green.

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

## Act-first local replication

After a PR head is pushed, an agent must use `act` instead of waiting for
GitHub Actions to finish. Start the repository-owned runner immediately while
the hosted workflows continue in parallel. The runner's validation base is the
live remote `refs/heads/dev` tip, resolved once at invocation: that is the
commit the trusted worktree must be at, and the commit the fetch must return.
GitHub's recorded PR base oid (`baseRefOid`) is frozen when the PR is opened
and does not track the branch, so the runner prints both SHAs and the recorded
one never refuses a run; re-targeting a PR's base to refresh it (the old
`gh pr edit --base` flip) is no longer needed. The generated event still
carries the **recorded** oid, because its only consumer is scope
classification and the hosted run receives that same value: the three scope
steps compare two trees with `git diff <base> <head>`, so a different base
there would make this replica classify a different file set than the run it
exists to predict. Because the trusted worktree must sit at a moving branch
tip, fast-forward it before invoking; a `dev` push between the resolve and the
fetch refuses the run, and the fix is to fast-forward and re-run. The runner is
host-side
security code: from the candidate worktree, execute only the copy in a
separate, clean worktree at the validation base:

```sh
python3 -I /absolute/path/to/trusted-dev/scripts/act_ci.py --pr <number>
```

Never invoke `scripts/act_ci.py` from the candidate worktree as the host-side
orchestrator. The candidate copy does run its offline `--selftest` inside the
disposable `docs` CI job; that contained check grants it no host or Docker
authority and is not the trusted invocation described here. Python isolated
mode prevents the candidate directory and ambient `PYTHONPATH` from supplying
imports to the host-side runner. The runner verifies that its own worktree and
bytes are clean at the validation base before it reads candidate content. A PR
that introduces the runner cannot bootstrap trust in its own code: an independent
reviewer must first audit the exact file, install that file outside the
candidate worktree with no writable mode bits, record its SHA-256, then use
`--trusted-install-sha256` together with explicit `--repo` and `--worktree`
arguments. That bootstrap is an independently granted trust decision, not an
executor shortcut. Later PRs, including changes to this runner, are validated
by the already-trusted base copy.

The independent bootstrap records both the source commit and file digest, then
uses a non-writable copy; `<candidate>` and `<audited-install>` are absolute
paths chosen by that reviewer:

```sh
install -m 0555 <candidate>/scripts/act_ci.py <audited-install>/act_ci.py
sha256sum <audited-install>/act_ci.py
python3 -I <audited-install>/act_ci.py --selftest \
  --worktree <candidate>
python3 -I <audited-install>/act_ci.py --pr <number> \
  --repo kebag-logic/milan-fpga --worktree <candidate> \
  --trusted-install-sha256 <recorded-64-hex-digest>
```

The audited install may be flat as shown. The offline self-test binds its byte
check to that installed file. It requires no copied repository directory
shape.

The reviewer's audit of those exact installed bytes is the trust anchor. The
runner's check of `--trusted-install-sha256` is self-attestation and detects
drift after that audit; it cannot establish that substituted runner code is
trustworthy by itself.

The `--selftest --worktree <candidate>` command above is the offline construction
and negative-control gate; the explicit worktree tells an installed runner
which shipping workflows to audit. That worktree remains untrusted: the reader
opens every path component without following symlinks, opens the final entry
nonblocking, requires a regular file and checks its size before a bounded read.
The negative controls cover symlinks, FIFOs, devices, and oversized files, so
the host-side bootstrap cannot be redirected into an unbounded candidate read.
The default PR run executes `docs`,
`elaborate`, `rtl-fast`, and `rtl-full` in that order.
Use repeatable `--workflow <name>` options for a focused reproduction, and use
`--dry-run` to perform the trust, fetch, metadata, and byte checks and print the
generated command before consuming containers. The runner requires `gh`, Git,
PyYAML, Docker, and exactly `act` 0.2.89. A newer act is refused until its Docker
mount and cache behavior is audited and the repository pin is deliberately
updated. On a host where the current user cannot open the Docker socket, add
`--sudo`; this is non-interactive. Both the host-side Docker CLI and `act` pass
through the same explicit `env -i` assignments and private empty `HOME`, keeping
them on the same default local daemon without inheriting root's Docker
`currentContext`, `DOCKER_CONFIG`, `DOCKER_CONTEXT`, `DOCKER_HOST`, credential
helpers, or other ambient environment. The offline self-test plants a fake
ambient current context and proves the two sudo prefixes remain identical apart
from their executable.

An audited change to the runner's cache, interruption, or Docker cleanup
boundary must also run the live fault-injection gate. It first writes a marker
through the effective runner tool cache and proves a second fresh run cannot see
it. It then starts a harmless sleeping job, inspects the real cache mount, waits
for the owned container, freezes the `act` process group, delivers `SIGINT` to
the runner, and requires the container, network, tool-cache volume, and run
directory to be absent afterward. With `--sudo`, the probe also requires a root
`act` child distinct from the sudo leader, sends `SIGSTOP` through privileged
`kill`, proves every process-group member is stopped, and proves the complete
group is absent before Docker teardown. Cancellation is serialized with that
STOP transition, and the monitor must signal completion and be joined before
Docker teardown can begin. A separate delayed-mutation probe times out a CLI
whose privileged child would create a labelled volume two seconds later, then
proves the whole CLI group is absent and the mutation never occurs:

```sh
python3 -I <audited-install>/act_ci.py --interrupt-selftest \
  --act-bin <absolute-act-0.2.89> [--sudo]
```

The command reads the open PR from GitHub and refuses before validation when
the base is not `dev`, the head is cross-repository, the candidate worktree is
dirty or at a different SHA, or selected workflow bytes disagree with the
remote commit even when index flags hide the edit. Replacement refs are
refused. The selected-file byte verifier uses the same no-follow, nonblocking,
regular-file-only bounded reader as the workflow sandbox. A credential-free
HTTPS fetch into a new temporary Git repository
materializes the exact same-repository PR head and validation base without
using the candidate's object database, index, configuration, hooks, filters,
or worktree; a `dev` tip that moves between the invocation-time resolve and
that fetch refuses the run, naming both base SHAs. The PR number, state, draft
bit, base ref, head ref/SHA, repository, cross-repository bit, and URL are
queried again immediately before and after every workflow; any change
invalidates the whole run. A recorded base oid that moves is reported and does
not refuse: the runner prints the old and new values and retains the result,
because the validation base was resolved at invocation, those unrelated bytes
were not executed, and the exact PR head did not change.

This local replica validates the exact head tree, not GitHub's synthetic merge
commit. Hosted `pull_request` contexts validate `refs/pull/<number>/merge`, so
they remain the authority for current merge compatibility while the local run
provides earlier evidence about the candidate's own bytes. A later `dev` move
can therefore require new hosted merge-context checks without discarding an
otherwise complete local head-tree run.

Before any candidate-directed network operation, the runner parses the exact
committed `.gitmodules` blob and requires the trusted name/path/URL pairs with
no duplicate or extra configuration. It also requires the matching four
gitlink paths. Git disables every transport by default and enables only HTTPS;
the inactive SSH-only `external` entry must match the trusted manifest but is
never fetched. Only then, and only after selected workflows pass their static
sandbox scan, does the temporary checkout initialize the three allowlisted
public pinned dependencies (`third_party/verilog-axis`, `protocol-processor`,
and `gptp-processor`). This gives act's local checkout copier the submodule-path
parity that a hosted checkout exposes; each workflow's own submodule update
remains the authoritative, idempotent check of those pins.

Every host-side command routed through the runner's capture boundary, including
Git metadata, fetch, checkout, and submodule commands, runs in a distinct
tracked process group with a 30-minute upper bound. An interrupt or timeout
cannot release the caller until that complete group is terminated, reaped, and
proved absent. Offline controls deliver process-directed `SIGTERM` and `SIGHUP`
to a captured child tree, and both signals to a production-shaped Git fetch with
a remote-helper grandchild. Each requires the conventional interrupted status
and proves the helper group absent within a bounded post-exit window. The
helpers do not clean up their own children, so a cleanup implementation that
only signals the group leader cannot satisfy the controls. When the
host exposes the facility, the test harness temporarily becomes a child
subreaper. It, rather than act's bare PID 1, reaps already-exited probe
descendants; the runner must still terminate the executable group, and the
probe allows its complete 25-second escalation. A separate
production-entry control invokes the normal PR command path, interrupts its early
repository lookup, and therefore fails if signal containment is narrowed to
workflow execution again.

The synthetic pull-request event names the exact base and head. A draft uses
`synchronize`, retaining `draft=true`; a ready PR uses `ready_for_review`, so
the real exhaustive selector launches all workers. `act` copies the immutable
temporary checkout rather than fetching through `actions/checkout`. It starts
from an empty invocation directory with private `HOME`/XDG roots, a minimal
allowlisted environment, and explicit empty env, secret, variable, and input
files. `GITHUB_TOKEN` is explicitly empty, so neither the active `gh` credential
nor an SSH agent, proxy credential, runtime token, or other host secret reaches
candidate code.

Candidate jobs must use literal `ubuntu-latest`; reusable workflows and
job/service containers are refused because they can carry container options or
host-volume requests that the trusted scanner cannot safely delegate. Steps may
use only the repository's exact audited non-Docker action set
(`actions/checkout@v4`, `actions/cache@v4`, `actions/setup-python@v5`,
`actions/upload-artifact@v4`, and `actions/download-artifact@v4`). Direct
`docker://` actions, local actions (including `runs.using: docker`), and any
unaudited remote action are refused before `act` starts; otherwise act can build
or reuse a daemon-global action image outside the labelled run boundary. Offline
negative controls cover all three forms, neutral names, and an unapproved
version inside the otherwise trusted `actions/*` namespace. The act command
also disables the container Docker socket, uses an unpredictable
runner-created bridge network instead of the host network, applies the same
unpredictable ownership token as a container label, never bind-mounts the
operator's worktree, and supplies no privileged flag. Candidate workflow code
consequently runs only in the disposable job boundary.

Every run and SHA gets fresh action/workspace, Actions-cache, artifact, event,
configuration, and input directories. `act` 0.2.89 also hard-codes the global
Docker volume name `act-toolcache`; the runner turns that otherwise persistent
slot into an exclusive ephemeral boundary. It refuses if that volume already
exists, creates it empty with the run's unpredictable ownership label, verifies
the label before every workflow, and removes it with an absence check after the
last owned container. The refusal names the
`org.kebag-logic.milan-act-ci.owner` label. Before removing an unlabelled legacy
cache, the operator must serialize every act runner and prove no container uses
it; absence of a label does not prove inactivity. A labelled cache must not be
removed until no runner, container, or network with its owner token remains.
The runner never deletes an
unowned volume. Concurrent runner invocations fail closed because only one can
own the upstream global name. If a Docker create call times out or is
interrupted after the daemon accepted it, the runner inspects the exact global
volume name and unpredictable network name, removes only resources carrying its
token, and verifies their absence before propagating the setup failure. The
offline self-test injects post-accept failures, ownership races, surviving
resources, rollback failures, and a daemon mutation that appears only after an
initial absence check. Each Docker CLI runs in a tracked process group; timeout
or interruption terminates and reaps that complete group (privileged from the
first signal under `--sudo`) before reconciliation begins. Rollback then
requires a continuous half-second absence window, removing a late owned
volume/network if the daemon completes an already-submitted request. The live
interruption self-test writes a
marker through
`RUNNER_TOOL_CACHE` in one run, creates a fresh second boundary, proves the
marker is absent there, inspects the effective container mount, and finally
proves interrupt cleanup removes the volume too.

A freshly created empty tool-cache volume also exposes a Docker daemon race
(#315). Sibling jobs in one workflow start their containers concurrently, and
every container create against an empty volume triggers the daemon's image
copy-up: an emptiness check followed by an unsynchronized directory copy of
the runner image's multi-gigabyte `/opt/hostedtoolcache`. Two creates that
pass the emptiness check together collide inside that copy, and the losing
sibling job dies during container setup with `failed to mkdir
.../act-toolcache/_data/Python: file exists`; a create arriving a moment
later instead sees the winner's first copied entries, skips its own copy, and
runs that job against a partially populated cache. The runner therefore seeds
the cache deterministically: after creating the labelled empty volume and
before `act` may launch any job, one owned seed container with no network
performs the only empty-volume mount, proves through its exit status that the
cache is populated, and is removed with the same owned-only, stable-absence
verification as every other runner resource. Every sibling job container then
mounts a complete non-empty cache and the daemon copy-up can never run
concurrently. Seeding adds that one copy-up (tens of seconds on a warm host)
to boundary creation, including under `--dry-run`, and the seed's own
thirty-minute pull-and-copy budget is bounded separately from ordinary Docker
CLI timeouts. The
offline self-test pins this mechanism as the regression control for the race:
building an act command from an unseeded boundary is refused, the seed must
run exactly once between volume and network creation carrying the ownership
label, the runner image, the exact cache mount, and no network, and a seed
that cannot prove a populated cache refuses the whole boundary and reconciles
both the seed container and the volume. Neutering the seeding call fails
those controls, so the race cannot silently return.

The artifact and cache servers bind only to the gateway address of the
runner-created bridge, so they are reachable by that run's job containers but
not advertised on the host's routable interface. Each workflow also receives a
freshly allocated nonzero artifact-listener port; act treats zero as random only
for its cache server. The offline self-test checks both bind arguments; actual
artifact transport is covered by the mandatory ready-state full run, whose
evidence must show both four-artifact aggregates downloading through that bridge
gateway. The interruption probe tests cleanup and tool-cache separation, not
artifact transfer. `rtl.yml` deliberately orders those aggregates:
`yosys-portability` directly needs `verilator-suites`. This leaves their
verdicts independent because the later job uses `always()` and still checks its
own workers, while serializing their first use of `actions/download-artifact`
under act v0.2.89. Without that edge, act can race initialization through its
shared action cache and one aggregate can observe no artifacts even after all
workers uploaded them. `scripts/ci_events.py --check` pins the edge and its
self-test removes it as a negative control.

Cleanup is restricted to the exact generated directory, the
labeled tool-cache volume, and the network whose ID, name, gateway, and ownership
label the runner recorded at creation. Mutable leases are registered before the
run directory, cache volume, or network can be accepted; post-create inspection
failures and the function-return handoff therefore still reconcile the exact
resource before propagating failure. Act process creation likewise blocks the
parent handler from unwinding until the returned process handle is stored, so
an interrupt cannot strand a process group between spawn and assignment. It
does not block the signal mask: caught parent dispositions reset on `exec`, and
a real-child negative control proves act inherits all three signals unblocked
and terminates on `SIGTERM`.
After every workflow and on every exceptional exit, the runner inventories
Docker, selects only containers carrying that token, attached to that network,
or sharing an owned container's network namespace, then stops and forcibly
removes them. It verifies that no owned container remains, then independently
attempts and verifies removal of both the network and tool-cache volume so a
failure inspecting either cannot suppress teardown of the other. Only then does
sudo ownership recovery and recursive run-directory removal begin. Any
unverifiable absence changes an otherwise green run to exit 2. `SIGINT`,
`SIGTERM`, and `SIGHUP` all unwind through this cleanup and retain their
conventional `128 + signal` exit status after cleanup (`130` for `SIGINT`). The
top-level Python handler only records the first signal and raises the cleanup
request; it does not change a signal mask or disposition during delivery, so a
deferred-signal race cannot escape the handler. Repeats of all three become
harmless until every nested cleanup and absence check completes; a first signal
that arrives after cleanup has already begun is blocked and delivered only after
that cleanup scope exits. The offline self-test injects failures into the mask
and disposition APIs while delivering a real `SIGINT`, and requires the handler
to avoid both APIs, return 130, and print its attributable post-cleanup
diagnostic.
Every runner-created worker inherits those signals blocked, preventing the
Python handler from being dispatched through a monitor thread while main is in
a protected cleanup tail; the offline gate sends a process-directed signal with
a live worker and proves cleanup finishes before the conventional exit status.
The monitor's cancel, join, completion event, and dead-thread proof form another
protected cleanup tail, including when the first signal arrives during a join.
An operator interrupt first terminates and reaps the whole `act` process group.
Sudo launches use
privileged group signaling from the first signal rather than relying on a
partial unprivileged `killpg`, and privileged `kill -0` must prove no root group
member survived before Docker teardown begins. If kill or `kill -0` temporarily
fails, the runner enters a containment hold: bounded commands keep retrying and
Docker teardown remains paused until absence is actually established, with the
PGID and operator recovery action printed. Docker-daemon-owned containers are
independently contained by the same verified cleanup.

The four exhaustive workers carry their checked denominator through the
singleton `matrix.total` dimension. `scripts/ci_events.py` proves that value
equals the `matrix.shard` list length and that every job name and shard command
uses it. Sharded matrices may not use `include` or `exclude`, because either can
change the produced job set independently of that list and carrier. This retains
GitHub's four-worker behavior and avoids the negative `strategy.job-total`
values produced by `act` 0.2.89 without a local workflow edit.

Local success is early exact-head evidence, not a locally manufactured GitHub
status. The runner does not publish commit statuses, and the seven hosted
contexts in the protected merge bar below remain mandatory. Continue useful
local validation or review while they run; do not spend the interval polling
an unfinished hosted run.

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
`scripts/ci_events.py --check` holds each of them, and `elaborate`, to the
same rule as the RTL jobs (#261): the job whose id is the required name
carries it, carries no `needs`, `if`, `continue-on-error` or `defaults`, and
exactly one job carries each name; the gate steps inside those jobs, their
shape and their presence, are pinned too (item 11 — landed by #295).

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

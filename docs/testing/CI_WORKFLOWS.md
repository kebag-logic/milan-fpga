# CI workflow policy

The repository separates rapid pull-request feedback from exhaustive RTL
validation. This changes when hosted runners execute the long gates; it does not
reduce the local verification bar in [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Contents

- **[Fast feedback](#fast-feedback)** — What runs on every pull-request update and why docs-only changes avoid RTL tool setup.
- **[Exhaustive validation](#exhaustive-validation)** — When the full Verilator and Yosys inventories run and how exact-head evidence is preserved.
- **[Pull-request state](#pull-request-state)** — How draft and ready states control hosted long jobs without changing local responsibilities.
- **[Local commands](#local-commands)** — The serial commands that remain the authoritative developer-side gates.
- **[Failure and cancellation semantics](#failure-and-cancellation-semantics)** — How missing artifacts, superseded commits, and resumed work are handled.

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
relevant. An empty or unresolvable diff is also treated as RTL relevant.

The elaboration smoke proves that the integration-heavy source lists lower and
resolve. It does not replace generic synthesis and must not be reported as a
portability pass.

## Exhaustive validation

[The exhaustive RTL workflow](../../.github/workflows/rtl.yml) runs when:

- a non-draft PR is opened or updated;
- a draft PR is marked ready for review;
- `dev` receives a push;
- the nightly schedule starts after this workflow revision reaches the
  repository's default branch;
- a maintainer starts it manually.

GitHub executes scheduled workflows only from the default branch. The repository
currently develops on `dev` while `main` is the default, so the nightly trigger
is staged by this change but does not become active until the same workflow
revision reaches `main`. Pull requests and pushes to `dev` are covered
immediately.

The workflow keeps the public aggregate names `verilator-suites` and
`yosys-portability`.

Verilator runs the complete suite inventory on four workers. The aggregate
rejects missing, unexpected, or duplicate suite logs before trusting the
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
claim hosted long-gate success for a commit other than the current PR head.

A docs-only ready PR remains cheap: the long workflow starts, classifies the
diff, and skips its RTL workers with explicit skipped results.

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

The fast Yosys mode is diagnostic only:

```sh
syn/yosys/run.sh --mode elaborate --no-structural \
  --top milan_datapath --top KL_pp_shadow --top KL_gptp_shadow
```

## Failure and cancellation semantics

A worker is not trusted merely because an aggregate job was able to download
something. Both aggregate jobs compare artifacts with the live repository
inventory and separately require every worker result to be `success`.

Workflow concurrency is scoped to the PR or branch. A new commit cancels older
runs because their evidence no longer describes the current head. Converting a
PR to draft starts a no-op run in the same group, which releases hosted runners
from obsolete exhaustive work.

Push validation on `dev` checks the actual merge result. It complements, but
does not replace, the explicit post-merge containment check required by
[CONTRIBUTING.md](../../CONTRIBUTING.md).

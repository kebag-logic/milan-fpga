# CI workflow policy

The repository separates rapid pull-request feedback from exhaustive RTL
validation. This changes when hosted runners execute the long gates; it does not
reduce the local verification bar in [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Contents

- **[Fast feedback](#fast-feedback)** — What runs on every pull-request update and why docs-only changes avoid RTL tool setup.
- **[Exhaustive validation](#exhaustive-validation)** — When the full Verilator and Yosys inventories run and how exact-head evidence is preserved.
- **[Elaboration](#elaboration)** — The one job that installs LiteX and observes what elaboration hands the datapath Instance, and what makes it red.
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
is staged by this change but does not become active until the workflow revision
reaches `main`. Pull requests and pushes to `dev` are covered immediately.

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
something. Both aggregate jobs compare artifacts with the live repository
inventory and separately require every worker result to be `success`.

Workflow concurrency is scoped to the PR or branch. A new commit cancels older
runs because their evidence no longer describes the current head. Converting a
PR to draft starts a no-op run in the same group, which releases hosted runners
from obsolete exhaustive work.

Push validation on `dev` checks the actual merge result. It complements, but
does not replace, the explicit post-merge containment check required by
[CONTRIBUTING.md](../../CONTRIBUTING.md).

# AGENTS.md — AI agent operating contract

This repository uses GitHub Issues as public work items, the GitHub Project as the
public Kanban, branches and worktrees as isolated implementation lanes, pull
requests as review objects, and repository documentation as durable knowledge.

This file tells AI agents how to work efficiently in that system. It supplements
[CONTRIBUTING.md](CONTRIBUTING.md); when the two differ, [CONTRIBUTING.md](CONTRIBUTING.md) is authoritative.

## Contents

- **[1. Repository model](#1-repository-model)** — What each GitHub and repository artifact is for, and the rule that project state must be public rather than living in a session.
- **[2. Authority and efficient context loading](#2-authority-and-efficient-context-loading)** — The order to read things in, why not to read the whole repository, and what to do when the Issue and a requirement disagree.
- **[3. Agent identities and roles](#3-agent-identities-and-roles)** — Session prefixes, the executor/reviewer split, and the requirement that an executor never approves its own work.
- **[4. Public task contract](#4-public-task-contract)** — What an Issue must contain before work starts, why settled scope rather than size decides readiness, and that new findings become new Issues.
- **[5. Executor procedure](#5-executor-procedure)** — The steps before the first edit, what to do during implementation, and the two public comments an executor owes.
- **[6. Reviewer procedure](#6-reviewer-procedure)** — Reviewing from public state alone, the lenses to cover, and the severity every finding carries, and the requirement that every lens be covered before a task is complete.
- **[7. Completion and merge](#7-completion-and-merge)** — The full bar a task must clear, why lens coverage rather than round count decides when review is done, and the rule that an agent does not merge without explicit maintainer authorization.
- **[8. Non-negotiable rules](#8-non-negotiable-rules)** — The short list that overrides convenience, including never letting two agents edit one branch concurrently, and never weakening a test to obtain a pass.

## 1. Repository model

- **GitHub Issue** — public task contract.
- **GitHub Project** — public scheduling and workflow state.
- **Branch + worktree** — one isolated implementation lane.
- **Pull Request** — implementation, evidence, discussion, and review state.
- **Requirements/docs/tests** — durable technical knowledge.
- **Local gates/CI** — reproducible evidence, not a substitute for review.

All useful project state must be public to both agents. Private scratchpads and
reasoning transcripts are temporary and must not become project dependencies.
Publish conclusions, evidence, decisions, blockers, and review findings instead.

## 2. Authority and efficient context loading

Before changing anything, load context in this order:

1. [CONTRIBUTING.md](CONTRIBUTING.md) for workflow, style, verification, and merge rules.
2. [docs/README.md](docs/README.md) for the map of authoritative documentation.
3. [REQUIREMENTS.md](REQUIREMENTS.md) and every specification clause linked by the Issue.
4. The active Issue for scope, acceptance criteria, dependencies, and decisions.
5. Relevant architecture/interface documents, code, and executable tests.
6. Historical/obsolete material only when the Issue explicitly asks for history.

Do not read the entire repository by default. Start from the Issue and the
authoritative entry points, search for the referenced identifiers, and expand
context only when a dependency requires it.

The Issue defines the work scope, but it cannot silently override a normative
requirement. If the Issue, requirements, documentation, and implementation
conflict, publish the conflict and mark the task as needing a decision rather
than choosing an interpretation privately.

Do not use an agent conversation, memory, or previous reasoning transcript as a
source of truth. A future cold reviewer must be able to reconstruct the task from
GitHub and the repository alone.

## 3. Agent identities and roles

Follow the session prefixes defined in [CONTRIBUTING.md](CONTRIBUTING.md):

- `[A<n>]` — author/executor activity from session `n`.
- `[R<n>]` — reviewer activity from session `n`.
- `[R<n>-a]`, `[R<n>-b]` — lettered halves of one review session running
  separate lenses in parallel (decided on #316: the suffixed form IS the
  supported public dialect; `scripts/check_merge_review_integrity.py` reads
  it). Each suffixed identity publishes its own verdict; a round-status line
  such as `[R<n>] MERGE-ROUND COMPLETE` carries no verdict word and clears
  nothing — the clearing `POSITIVE` must be spelled by a reviewer identity.

Every active Issue must publicly identify an **executor** and an **independent
reviewer** before implementation starts. Roles should rotate across tasks:

- Agent A implements -> Agent B reviews.
- Agent B implements -> Agent A reviews.

An executor never approves its own work.

**The reviewer assigns a finding's lens, and the executor may not re-label it.**
The label decides which lens banks coverage under section 7, so leaving it
unowned puts the completion test in the hands of the party the test is about. An
executor that believes a finding is filed under the wrong lens says so in the
thread and the reviewer re-files it; where the two disagree, both lenses are
recorded and neither is covered clean.

[CONTRIBUTING.md](CONTRIBUTING.md) currently requires two positive reviews, including one external
to the implementation lane. With two AI systems, use a separate cleared-context
review session for the lane's internal review and the other AI system for the
external review. An executor's own verdict does not count as either positive.

## 4. Public task contract

All substantive work must correspond to a public GitHub Issue. The Issue must
contain or link to:

- objective and observed evidence;
- authoritative requirements/specification clauses;
- context entry points;
- in-scope and out-of-scope work;
- acceptance criteria;
- exact validation method and expected result;
- dependencies and possible lane conflicts;
- executor and reviewer;
- unresolved decisions.

Do not start a task with an unresolved design/specification choice. Keep it in
`Backlog` until the decision is recorded. Size does not determine readiness;
settled scope does.

Acceptance criteria are frozen for an active implementation lane. If they are
wrong, contradictory, or incomplete, request a public change; do not rewrite
them merely to make the implementation pass.

Newly discovered work becomes another public Issue. Do not silently expand the
current task or fix unrelated behavior opportunistically.

## 5. Executor procedure

Before the first edit:

1. Confirm the Issue is `Ready` and has no open decision.
2. Set the executor and reviewer.
3. Move it to `In progress`.
4. Create the branch from the Issue with:
   `gh issue develop <N> --base dev`.
5. Use one branch, one worktree, and one PR for the Issue.
6. Post a concise public takeover comment:

```text
[A<n>] TAKEN
Branch: <branch>
Authoritative references: <links/IDs>
Interpreted scope: <one paragraph>
Validation plan: <commands/gates>
Blockers: none | <details>
```

During implementation:

- make the smallest coherent change that satisfies the task;
- preserve documented module and interface contracts;
- add or update self-checking tests for changed behavior;
- test negative, boundary, reset, ordering, and failure paths where relevant;
- update authoritative documentation when behavior or architecture changes;
- make material assumptions public in the Issue or PR;
- follow the HDL, CDC, commit, worktree, and verification rules in
  [CONTRIBUTING.md](CONTRIBUTING.md).

Before handing off to review, post reproducible evidence:

```text
[A<n>] REVIEW READY
Commit: <full SHA>
Changed: <short file/behavior summary>
Validation: <exact commands and results>
Acceptance criteria: <met/not met with evidence>
Open risks/questions: none | <details>
```

Open the PR against `dev` as a draft while implementation is changing. The
`rtl-fast` workflow runs on every update. Before marking the PR ready, run and
record the complete local gates required by [CONTRIBUTING.md](CONTRIBUTING.md).
Marking it ready starts the hosted exhaustive Verilator and Yosys gates on the
exact PR head. A later commit invalidates that evidence and starts them again;
convert the PR back to draft before resuming exploratory work. The detailed
scheduling and cancellation contract is in the
[CI workflow policy](docs/testing/CI_WORKFLOWS.md).

After each pushed PR head, start the repository-owned local replica before
inspecting or polling the hosted run. An agent must use `act` instead of waiting
for GitHub Actions to finish. From the candidate worktree, invoke the runner
from a separate, clean worktree at the PR's current remote `dev` base:

```sh
python3 -I /absolute/path/to/trusted-dev/scripts/act_ci.py --pr <number>
```

Never execute the candidate's copy as the **host-side orchestrator**. The
candidate copy may run its offline `--selftest` only inside the disposable CI
job boundary; that does not grant it host or Docker authority. Select applicable
fast workflows on a draft; the ready default runs all four. The command refuses
a dirty or mismatched candidate, records and rechecks the exact remote head,
and forwards no host credential. Its result is local evidence only; protected
hosted contexts continue in parallel and remain mandatory. The trust boundary,
bootstrap rule for a PR that introduces the runner, prerequisites, and failure
semantics are in [Act-first local replication](docs/testing/CI_WORKFLOWS.md#act-first-local-replication).

Self-test results belong in a PR comment as evidence, not as a review verdict.

## 6. Reviewer procedure

The reviewer must use a cleared context and independently reconstruct the task
from public state. Do not receive the author's private scratchpad or reasoning
transcript. The implementation itself is not evidence that its approach is
correct.

Read, in order:

1. Issue and acceptance criteria.
2. Linked requirements/specification clauses.
3. Authoritative architecture and interface documents.
4. PR diff and commit history.
5. Tests, logs, and validation evidence.

Review at least these lenses. They are named and countable, and section 7
measures completion against them, so record which lens each finding came from
and which lenses a round covered. Each carries a short token, given below its
heading, because the full names run to thirty-six characters and a line already
carrying a severity, a path and a title cannot also carry that. Use the token.

**These five names are the ones a completion ledger counts**, and
[CONTRIBUTING.md](CONTRIBUTING.md) says so where it assigns lenses, so the
precedence rule at the top of this file has nothing to resolve. The angles named
there are examples of what to look at within a lens, not a second list to report
against.

**The lenses overlap on purpose and are not a partition.** A timeout rule is
named under `Conformance`, under `RTL` and under `Robustness`, and a real
missing timeout is honestly all three. So a finding attributable to more than
one lens is recorded under **each** of them, and none of those lenses is
covered clean by the round that found it. Recording it under the closest-looking
single name is what makes mislabelling profitable: the other lenses bank a clean
result they did not earn, and no reader can tell an honest mislabel from a
deliberate one.

### Requirement and protocol conformance

Token: `Conformance`

- Every acceptance criterion is actually satisfied.
- Cited IEEE 1722/1722.1/Milan behavior is interpreted correctly.
- Wire lengths, field values, state transitions, response behavior, and timeout
  rules are correct.

### RTL and architecture

Token: `RTL`

- Clock and reset assumptions are valid.
- CDC uses only approved primitives and patterns.
- FSM transitions and default/error paths are complete.
- Widths, signedness, truncation, overflow, and indexing are correct.
- Backpressure, stalls, latency, and resource/timing effects are understood.
- Existing module/interface contracts remain valid.

### Robustness

Token: `Robustness`

- malformed and truncated input;
- minimum/maximum values;
- invalid ordering/state;
- reset during activity;
- backpressure and timeout paths;
- repeated commands and idempotence where applicable;
- feature-disabled and configuration-dependent behavior.

### Tests

Token: `Tests`

- Each new test can fail for the defect it claims to detect.
- Positive, negative, and boundary behavior is covered.
- Real integration wiring is tested where practical.
- Existing regressions remain green.
- Tests do not merely reproduce implementation assumptions.

### Documentation

Token: `Docs`

- Changed contracts are reflected in authoritative docs.
- Obsolete requirements or documents were not accidentally restored.
- The PR and Issue contain enough evidence for another cold reviewer.

Classify every finding:

- `BLOCKER` — incorrect, unsafe, or non-compliant; must fix before merge.
- `MAJOR` — substantial correctness, design, or test weakness; normally blocking.
- `MINOR` — worthwhile but non-blocking.
- `SUGGESTION` — optional improvement.
- `PASS` — no blocking finding for the assigned review lens.

Use this concise format:

```text
[R<n>] <SEVERITY> <lens> — <path:line or artifact> — <title>
Requirement/evidence: <why this is a finding>
Impact: <failure mode>
Required change: <what must be true, without prescribing unnecessary design>
Verification: <how the fix will be checked>
```

A review round that discovers defects is not approval of later fixes. Re-review
the corrected commit and publish a new verdict.

**The canonical overall verdict** (the #311 decision) is the token `POSITIVE`
or `NEGATIVE` on the reviewer's own `[R<n>]`-led line — typically the round's
opening line, e.g. `[R1] POSITIVE — exact head <sha>` — in a PR comment or
review body. That line is what `scripts/check_merge_review_integrity.py`
reads. A verdict spelled anywhere else does not machine-read: PR #302's
re-reviews wrote `Verdict: PASS across all five review lenses.` on a bare
line under an `[R1] EXACT-HEAD RE-REVIEW` header, and the integrity audit
still reports that merge as open-blocker — correctly, by this decision. Per-
lens `PASS` lines are findings-format, never the overall verdict.

**Every round states which lenses it covered, including those that found
nothing.** A lens is covered when it was applied, not when it was listed. "I
read the RTL against the clause and found nothing" is a result section 7 needs;
silence about a lens is not.

**A clean lens is reported in the same format as a finding, and carries the
same evidence.** Every finding must name a `path:line or artifact`; the clean
result must too, because that is the claim section 7 reads to release a merge.
Requiring evidence for the statements that do not unlock a merge and none for
the one that does is the asymmetry that lets a round bank a lens on its word:

```text
[R<n>] PASS <lens> — <path:line or artifact> — <what was checked and against what>
```

The artifact field names what was actually examined, at the head under review.
"Reviewed the RTL" is not an artifact and neither is a module name on its own;
a second reviewer must be able to open what is named and disagree. A lens whose
scope has no matching file in the diff is still covered by naming the artifact
that made it inapplicable. One line per clean lens, or an equivalent table with
the same three fields.

**Prefer the lens covered least.** A reviewer who keeps applying the lens that
keeps producing findings is doing the most productive-feeling and least
informative thing available: the yield stays high because that artifact is deep,
not because it is the right place to look. Depth in one lens is not coverage,
and a high finding rate is not evidence of good targeting.

The case in Issue #166 is the argument, and it is worth stating exactly, since
an approximation of it would be the same defect the rule is about. On
protocol-processor #13, thirteen consecutive rounds asked whether the harness
proved what it claimed and whether the document describing it was true. Twelve
found something real, every fix was correct, and the thirteenth opens "Thirteen
rounds, and this is the first" positive one. Those rounds ran two lenses,
`Tests` and `Docs`, and the later ones say so in their own first line: seven
consecutive answers are headed "Doc-only".

Three lenses went unapplied for all thirteen. When `RTL` was finally run, as a
separate round on the same head, it found two defects in the shipped RTL that no
further harness review would have reached: `done_seen_r` latched in every state
with no outstanding command, and no timeout or abort, so a silent device wedges
the port forever.

That round published `POSITIVE` and moved both defects to new Issues. The PR
merged. At the merged head `5121dce`, `hdl/packet_engine/KL_pp_nvm_port.sv:153`
still reads `if (dev_done_i) done_seen_r <= 1'b1;`, and both Issues are open.
So the failure was not that review continued too long, and it was not that the
missing lens was never run. It was that thirteen rounds bought depth in two
lenses, and that the round which finally widened was allowed to bank the lens it
widened into while leaving what it found in the tree.

## 7. Completion and merge

A task is complete only when:

- all acceptance criteria are met;
- required tests and local verification gates pass;
- the current PR head has a successful `rtl-fast` verdict;
- an RTL/tooling-relevant PR head has exact-head `verilator-suites` and
  `yosys-portability` evidence after it is marked ready;
- no undocumented requirement/interface change remains;
- the full review bar in [CONTRIBUTING.md](CONTRIBUTING.md) is met;
- blocking and major findings are fixed and re-reviewed;
- **every lens in section 6 has been covered clean**, and the covering round is
  named for each **with the exact head it covered**. A lens is covered clean by
  a round that applied it and left no `BLOCKER`, `MAJOR` or `MINOR` **open under
  that lens**. `SUGGESTION` is optional by definition and does not affect
  coverage.

  **Coverage is banked against a commit, not against a round.** A later commit
  that changes any artifact within a lens's scope un-covers that lens, and it
  must be covered again at a head that includes the change. Otherwise the bar is
  satisfiable by covering lenses early and then rewriting what they covered,
  which is the ordinary shape of a lane answering findings across many commits
  rather than an exotic abuse of the rule. On protocol-processor #13 the round
  that covered the harness ran at `c47ef19b`; twelve commits later the merge head
  carried a new 886-line figure gate and a modified `sim_main.cpp`, so the round
  nameable for `Tests` had never seen the tests that merged.

  So the completion ledger is three columns, not two: **lens, covering round,
  head**. A ledger whose heads are not the merge candidate, or an ancestor of it
  that nothing in that lens's scope has touched since, does not clear this bullet.

  **The ledger is published by a reviewer, or explicitly accepted by one.** Every
  other bullet here is an executor's claim about its own work, which is why
  section 3 says an executor never approves its own work. This one decides
  whether review is finished, so it is the one bullet the party under review
  cannot assemble alone.

  Open, not merely un-blocking. **A finding moved to another Issue is not
  resolved**: the defect is still in the tree, and moving the paperwork does not
  move the code. This is the case the rule exists for and it is not
  hypothetical. On protocol-processor #13 a round applied the RTL lens, found a
  latch held in every state and a missing timeout that lets a silent device
  wedge the port, published **POSITIVE**, and deferred both to new Issues. That
  PR merged, those Issues are still open, and the RTL is unchanged. Under a
  severity test that round covers the lens; under this one it does not.

  Severity therefore cannot be the coverage test on its own, or downgrading a
  finding becomes the cheapest way to bank a lens. Coverage is judged per
  lens, not per round: a round that finds a blocker in one lens still covers
  any other lens it applied cleanly, and findings elsewhere do not un-cover a
  lens already covered. Reading this per round would mean a clean lens never
  counts while any other lens is dirty, which is the unbounded loop again
  wearing a different collar;
- no review round remains in flight;
- the candidate merge result is validated;
- the change lands in `dev`;
- post-merge containment is clean;
- authoritative documentation is current;
- the Issue is closed (by the merge through `Closes #N`, or by hand) and
  moved to `Done`.

The hosted long-gate schedule does not weaken the mandatory local commands in
[CONTRIBUTING.md](CONTRIBUTING.md). Green CI alone is not proof of correctness.
A PR must not be merged by an agent unless a maintainer explicitly authorizes
that merge.

Lens coverage is the bar because it is the one property the motivating failure
lacked. It is enumerable rather than a threshold: the lenses are the list in
section 6, so the bar is read off the contract and no number is chosen. It
cannot be met by repetition, since a thirteenth round of one lens covers
nothing new. And it does not end review early, because a lens that keeps
producing findings keeps the task open.

What it does end is the other failure, which is subtler and was the real one:
review that continues indefinitely while never widening. When the bar is
unstated, the reviewer with the highest finding rate looks the most diligent,
and the lens already yielding findings is always the cheapest to run again.

## 8. Non-negotiable rules

- Never let two agents edit the same branch/worktree concurrently.
- Never change another active lane's branch.
- Never hide a material assumption or specification conflict in code.
- Never weaken a test or acceptance criterion solely to obtain a pass.
- Never re-run a lens already covered CLEAN in place of one never applied, and
  never report a lens as covered without having applied it. Re-running a lens
  to check a fix is required, not discouraged: a lens is not covered clean
  while a finding under it is open.
- Never treat generated prose or an agent summary as more authoritative than the
  linked requirement and executable evidence.
- Never publish private chain-of-thought; publish concise conclusions and evidence.
- Keep commits one-line with no trailers, as required by [CONTRIBUTING.md](CONTRIBUTING.md).
- Follow candidate-merge validation and post-merge containment exactly.

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

Every active Issue must publicly identify an **executor** and an **independent
reviewer** before implementation starts. Roles should rotate across tasks:

- Agent A implements -> Agent B reviews.
- Agent B implements -> Agent A reviews.

An executor never approves its own work.

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

Open the PR against `dev`. Self-test results belong in a PR comment as evidence,
not as a review verdict.

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
and which lenses a round covered.

### Requirement and protocol conformance

- Every acceptance criterion is actually satisfied.
- Cited IEEE 1722/1722.1/Milan behavior is interpreted correctly.
- Wire lengths, field values, state transitions, response behavior, and timeout
  rules are correct.

### RTL and architecture

- Clock and reset assumptions are valid.
- CDC uses only approved primitives and patterns.
- FSM transitions and default/error paths are complete.
- Widths, signedness, truncation, overflow, and indexing are correct.
- Backpressure, stalls, latency, and resource/timing effects are understood.
- Existing module/interface contracts remain valid.

### Robustness

- malformed and truncated input;
- minimum/maximum values;
- invalid ordering/state;
- reset during activity;
- backpressure and timeout paths;
- repeated commands and idempotence where applicable;
- feature-disabled and configuration-dependent behavior.

### Tests

- Each new test can fail for the defect it claims to detect.
- Positive, negative, and boundary behavior is covered.
- Real integration wiring is tested where practical.
- Existing regressions remain green.
- Tests do not merely reproduce implementation assumptions.

### Documentation

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

**Every round states which lenses it covered, including those that found
nothing.** A lens is covered when it was applied, not when it was listed. "I
read the RTL against the clause and found nothing" is a result section 7 needs;
silence about a lens is not.

**Prefer the lens covered least.** A reviewer who keeps applying the lens that
keeps producing findings is doing the most productive-feeling and least
informative thing available: the yield stays high because that artifact is deep,
not because it is the right place to look. Depth in one lens is not coverage,
and a high finding rate is not evidence of good targeting.

The case in Issue #166 is the argument. On protocol-processor #13, twelve
consecutive rounds asked whether the harness proved what it claimed. Every round
found something real and every fix was correct. None asked whether the DUT was
right. When a different angle was finally run it found defects in the RTL itself
that no amount of further harness review would have reached, including a latch
held in every state and a missing timeout that lets a silent device wedge the
port forever. The failure was not that review continued too long. It was that
twenty-one rounds bought depth in one lens and left others untouched.

## 7. Completion and merge

A task is complete only when:

- all acceptance criteria are met;
- required tests and local verification gates pass;
- no undocumented requirement/interface change remains;
- the full review bar in [CONTRIBUTING.md](CONTRIBUTING.md) is met;
- blocking and major findings are fixed and re-reviewed;
- **every lens in section 6 has been covered clean**, and the covering round is
  named for each. A lens is covered clean by a round that applied it and
  produced no `BLOCKER` or `MAJOR` **under that lens**. Coverage is judged per
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
- the Issue is manually closed and moved to `Done`.

Green CI alone is not proof of correctness. A PR must not be merged by an agent
unless a maintainer explicitly authorizes that merge.

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
- Never re-run a covered lens in place of an uncovered one, and never report a
  lens as covered without having applied it.
- Never treat generated prose or an agent summary as more authoritative than the
  linked requirement and executable evidence.
- Never publish private chain-of-thought; publish concise conclusions and evidence.
- Keep commits one-line with no trailers, as required by [CONTRIBUTING.md](CONTRIBUTING.md).
- Follow candidate-merge validation and post-merge containment exactly.

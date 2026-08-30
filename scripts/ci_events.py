#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Hold the CI workflow files to their documented event and SHA contract.

WHY THIS EXISTS (issues #174, #181). The hosted CI contract lives in four
workflow files and one page of prose, docs/testing/CI_WORKFLOWS.md, and for
three weeks they disagreed in ways nothing measured:

  * rtl.yml carried a nightly cron that could not fire. GitHub schedules only
    the default branch, the default was `main`, and main's rtl.yml had no
    `schedule` at all. The page said the cron was "staged".
  * docs.yml ran on `push: [main]` only, so the docs gate never ran on a merge
    result, while CONTRIBUTING.md said "CI does not run on dev at all" after
    rtl-fast.yml and rtl.yml had started running on every push to dev.
  * The public check names the merge bar reads (`rtl-fast`, `verilator-suites`,
    `yosys-portability`, `elaborate`) were held only by convention.

Since 2026-08-22 `dev` is the repository default branch (#174, decision 3), so
the cron and `gh workflow run rtl.yml --ref <branch>` are executable and the
page states the contract. This gate keeps the files and the page from drifting
apart again. `--check` parses the workflow files with pyyaml and asserts every
item the page promises; `--selftest` removes or alters each item, one at a
time, on in-memory copies and requires the check to catch each one, and fails
if the checker is stubbed to find nothing.

THE SHA CONTRACT (#174, decision 2). GitHub pins GITHUB_SHA once per run for
every event: the pushed commit, the merge commit of a pull request, the tip of
the default branch for a schedule, the tip of the chosen ref for a dispatch.
Every checkout that does not override `ref` therefore validates one tree. The
exhaustive workflow makes that explicit: the gate job prints event, ref and SHA
and exports `target_sha`; every worker writes GITHUB_SHA into a TARGET_SHA file
beside its evidence; both aggregates run `--require-target-sha` over the
downloaded shards and refuse a missing record, a record naming another tree, or
a gate/run/checkout SHA that is not one value. An aggregate skips only when the
gate succeeded and explicitly published `run_full=false`; a gate failure,
cancellation or missing output makes the aggregate run into that refusal path.
A missing record is a failure, never a skip. `--check` refuses any
`actions/checkout` step in rtl.yml that overrides `ref`, requires every
artifact-uploading job to record the SHA and every artifact-downloading job to
verify it.

THE DEFAULT-BRANCH ASSERTION ([R1] on PR #204). The cron was inert because of
a repository SETTING, and a gate that reads files cannot see a setting. So the
gate job reads it live on every run (`gh api repos/$GITHUB_REPOSITORY --jq
.default_branch`) and hands it to `--require-default-branch`: a scheduled or
dispatched run refuses to continue unless the default branch is `dev`, naming
the branch it saw, and refuses a value it could not read, since an unknown is
not agreement. A pull-request or push run prints the value and carries on:
those runs are about the tree, not the setting, and a contributor's PR must
not go red for a setting it cannot change. `--check` requires the step, its
token and its fail-closed shape (no `continue-on-error`, no `|| true`).

WHETHER IT RUNS AT ALL (#209). The four items above hold what the gate job
DOES. None of them held the conditions under which it does it, and GitHub has
a separate lever for each of those: a `needs` on the gate makes it a dependent,
and a dependent of a skipped job is skipped; an `if`, a `shell` or a
`continue-on-error` on any step BESIDE the pinned one neuters that step while
every pinned character stays put; a step inserted, removed or reordered
changes what the steps after it read (an entry appended to GITHUB_PATH puts
another `gh` first) or runs the assertion before the checkout has brought the
script it calls; and an `env` on the job or on the workflow reaches the
step's `gh` without appearing anywhere in the step. So `--check` also holds
the gate job's `needs`, its exact step sequence, every step's key set, and
the absence of any `GH_*` above the step. Separately, the worker shard
denominator is carried as `${{ matrix.total }}`. The checker requires that
matrix value to be a singleton equal to the shard list's size and requires
every consumer to derive from it. This preserves one checked count while
avoiding act v0.2.89's broken `strategy.job-total` value.

THE FAST VERDICT ([R2] on PR #239). rtl-fast.yml's aggregate accepts skipped
consumers on purpose, so its one verdict step is the entire conversion of
four job results into the required `rtl-fast` context, and it was outside
the perimeter: an `if` on the step, a result binding rebound to `success`,
or a `case` widened to accept `failure` each made a FAILED fast job a green
required context. So the aggregate must need every other job of that
workflow; every job an aggregate needs is the selector, a consumer, or
itself held; the verdict step's keys, env bindings and script are derived
from that `needs` list; each public check name is carried by exactly one
job; and the reference audit covers every static `needs` chain, `.result`
included, not only `.outputs.`.

THE NON-RTL REQUIRED CONTEXTS (#261). `docs-check`, `wire-accountability`,
`docs-check-no-git` and `elaborate` are four of the seven names the merge bar
reads, and docs.yml and elaborate.yml have no aggregate: the carrier job IS
the context. Both workflows sat outside the perimeter above, so `if: false`
on `docs-check` retired this gate itself and `continue-on-error` on
`elaborate` retired the elaboration gate, each with every required context
satisfied, because a skipped required context satisfies the ruleset. So the
carrier of every public name in every workflow is held to the same rule as
the RTL jobs -- no `needs`, `if`, `continue-on-error` or `defaults` -- the
three documentation names join the one-carrier rule, and the job whose id is
the public name must be the one carrying it ([R3] on PR #293): the content
checks read that job by id, and a stub carrying the name under another id
was the required context with 233 items and no finding. The gate steps
inside those jobs are #295.

    scripts/ci_events.py --check        # the live tree against the contract
    scripts/ci_events.py --selftest     # mutation arms over in-memory copies
    scripts/ci_events.py --require-target-sha --sha gate=<sha> \\
        --sha run=<sha> --sha checkout=<sha> -- <shard-dir>...
    scripts/ci_events.py --require-default-branch --event <event> \\
        --observed <branch>

Exit 0 = clean, 1 = a finding, 2 = cannot run (pyyaml absent, a file missing
or unparseable, usage).
"""

from __future__ import annotations

import argparse
import copy
import itertools
import pathlib
import re
import sys
import tempfile

RC_OK, RC_FINDING, RC_CANNOT_RUN = 0, 1, 2

ROOT = pathlib.Path(__file__).resolve().parent.parent

RTL_FULL = ".github/workflows/rtl.yml"
RTL_FAST = ".github/workflows/rtl-fast.yml"
DOCS = ".github/workflows/docs.yml"
ELABORATE = ".github/workflows/elaborate.yml"
POLICY = "docs/testing/CI_WORKFLOWS.md"
WORKFLOWS = (RTL_FULL, RTL_FAST, DOCS, ELABORATE)
FILES = WORKFLOWS + (POLICY,)

#: The pull-request activity types both RTL workflows subscribe, exactly.
PR_TYPES = ("opened", "reopened", "synchronize", "ready_for_review",
            "converted_to_draft")
#: The branch every workflow must run on when pushed to.
PUSH_BRANCH = "dev"
#: The record every worker writes beside its evidence.
RECORD = "TARGET_SHA"
#: The gate job of the exhaustive workflow and the outputs it exports. A job
#: `outputs` map is a NAME -> EXPRESSION mapping exactly like a step's `env`,
#: and these names are what the rest of this file derives its expressions and
#: its consumer `if` conditions from, never a second literal.
GATE_JOB = "full-ci-gate"
GATE_OUTPUT = "target_sha"
#: The published decision, and the scope answer behind it.
RUN_FULL_OUTPUT = "run_full"
RTL_OUTPUT = "rtl"
#: How an aggregate invokes the verifier (the first token after the script).
VERIFY_FLAG = "--require-target-sha"
#: How the gate invokes the live default-branch assertion, and the events
#: whose run the repository default-branch setting governs: a schedule runs
#: on the default branch's tip, a dispatch exists only because the workflow
#: is on that branch. The expected branch is PUSH_BRANCH, derived, not a
#: second literal: the branch the workflows run on push is the branch that
#: must be the default.
DEFAULT_BRANCH_FLAG = "--require-default-branch"
DEFAULT_BRANCH_EVENTS = ("schedule", "workflow_dispatch")
#: The default-branch step's script, pinned verbatim after whitespace
#: normalization ([R1] on PR #204, second round). A substring recognizer was
#: fooled by a decoy: `observed=dev` beside a `gh api` inside `if false`.
#: So the script is held to exactly these three lines, one unconditional
#: live read into `observed` and one verifier call after it, and the
#: structural reasons in check_default_branch_step name what a deviation
#: did before the whole-script comparison refuses it.
CANONICAL_OBSERVED = ('observed="$(gh api "repos/$GITHUB_REPOSITORY" '
                      '--jq .default_branch 2>/dev/null || echo unreadable)"')
CANONICAL_CALL = ("python3 scripts/ci_events.py --require-default-branch "
                  '--event "$GITHUB_EVENT_NAME" --observed "$observed"')
CANONICAL_DEFAULT_BRANCH_SCRIPT = ("set -euo pipefail", CANONICAL_OBSERVED,
                                   CANONICAL_CALL)
OBSERVED_ASSIGNMENT = re.compile(
    r"(?:^|[;&|(]\s*|\b(?:export|local|declare|readonly|typeset)\s+)"
    r"observed\s*\+?=")
CONTROL_FLOW = re.compile(
    r"(?:^|[;&|(]\s*)(?:if|case|for|while|until|select|function)\b"
    r"|\b(?:then|fi|esac|do|done)\b|\(\)\s*\{")
#: The SHA sources every aggregate passes to --require-target-sha, exactly:
#: the gate's exported target, the aggregate's own run, and its checkout.
#: The verifier refuses any other set ([R1], second round: with `run` and
#: `checkout` dropped from both aggregates, everything stayed green).
REQUIRED_SHA_LABELS = ("gate", "run", "checkout")
REQUIRED_SHA_ARGS = {
    "gate": '--sha gate="$GATE_SHA"',
    "run": '--sha run="$GITHUB_SHA"',
    "checkout": '--sha checkout="$(git rev-parse HEAD)"',
}
SHA_LABEL_RE = re.compile(r"--sha\s+([A-Za-z_]+)=")
EXPECT_RE = re.compile(r"--expect\s+(\S+)")
#: The keys a pinned step may carry, and nothing else ([R1] on PR #204,
#: third round): a key beside the script decides whether, on which events,
#: or by which interpreter the script runs. `if: false`, `if: ${{
#: github.event_name == 'pull_request' }}`, `shell: bash -n {0}`,
#: `continue-on-error: true`, a `timeout-minutes`, a `working-directory`,
#: an extra `GH_HOST` or `GH_CONFIG_DIR` in env: each left the script text
#: canonical and the assertion dead. So the key set is pinned, the env key
#: set is pinned, and the verifier step's one permitted `if` is pinned.
ASSERT_STEP_KEYS = ("name", "env", "run")
VERIFY_STEP_KEYS = ("name", "if", "env", "run")
VERIFY_STEP_IF = "${{ always() }}"
#: Every pinned step's `env`, as the BINDING each name must carry, never the
#: name alone ([R0] on PR #239). Holding the names while leaving the
#: expressions free held nothing where it mattered: `PR_DRAFT: "true"` is
#: valid workflow YAML, keeps all three pinned names and all four pinned
#: keys, and makes a ready RTL pull request publish `run_full=false`. Both
#: worker matrices then skip, both aggregates skip under their documented
#: no-op exception, and a skipped required context satisfies the ruleset, so
#: the run is a false green rather than a refusal. `PR_BASE_SHA:
#: ${{ github.sha }}` (a diff of a commit against itself, so `rtl=false`) and
#: `EVENT_NAME: pull_request` (a push, schedule or dispatch run taking the
#: pull-request branch) reach the same place by the same route. So the
#: mapping is the contract and pinned_step_keys compares the value: there is
#: no longer any way to pin an env name in this file without saying what it
#: must be bound to. GATE_SHA is derived from the job and the output it
#: reads, never restated.
ASSERT_STEP_ENV = {"GH_TOKEN": "${{ github.token }}"}
VERIFY_STEP_ENV = {
    "GATE_SHA": f"${{{{ needs.{GATE_JOB}.outputs.{GATE_OUTPUT} }}}}",
}
#: Job keys that decide whether a job runs at all, or runs as written, each
#: with the reason a refusal names. Before #209 this gate held what the gate
#: job DOES and nothing about the conditions under which it does it, so
#: `needs` is here now: a gate that needs another job is a dependent, and a
#: dependent of a skipped job is skipped, taking every assertion inside it.
#: The gate job carries none of these keys. An aggregate job legitimately
#: needs the gate to read its output and carries its documented fail-closed
#: `if`, and nothing else from this list. The workflow carries no top-level
#: `defaults` (a `defaults.run.shell: bash -n {0}` parses every script and
#: executes none).
JOB_NEUTER_KEYS = {
    "needs": ("it makes the job a dependent, and a dependent of a skipped "
              "job is skipped, taking every assertion in it"),
    "if": "it decides whether the job runs at all",
    "continue-on-error": "it turns the job's failure into a pass",
    "defaults": "it decides by which interpreter every script in the job runs",
}
#: The gate job's steps carry these keys and no others. Pinning the assert
#: step's keys while its siblings were unpinned held the wrong perimeter
#: (#209): `if: false` on the pin step or on the decision step leaves the
#: assert step's script canonical and its output empty.
CHECKOUT_ACTION = "actions/checkout"
CHECKOUT_STEP_KEYS = ("uses", "with")
CHECKOUT_STEP_OPTIONAL = ("name",)
CHECKOUT_FETCH_DEPTH = 0
PIN_STEP_ID = "target"
PIN_STEP_KEYS = ("name", "id", "run")
DECIDE_STEP_ID = "gate"
DECIDE_STEP_KEYS = ("name", "id", "env", "run")
DECIDE_STEP_ENV = {
    "EVENT_NAME": "${{ github.event_name }}",
    "PR_DRAFT": "${{ github.event.pull_request.draft }}",
    "PR_BASE_SHA": "${{ github.event.pull_request.base.sha }}",
}
#: The decision step's script, pinned verbatim after whitespace
#: normalization, exactly as the default-branch step's is. The bindings above
#: hold what this step READS; this holds what it DOES with what it read.
#: `run_full=true` rewritten to `run_full=false`, or the selector's
#: `--selftest` replaced by `true`, changes no pinned name and no pinned key,
#: and each publishes the no-op decision (or drops the selector's own proof)
#: with every other contract item green -- both measured on a copy of the
#: tree while answering [R0] on PR #239. The lines are the NORMALIZED form
#: (continuations joined, runs of blanks collapsed), so a re-indentation or a
#: differently wrapped continuation is the same script and still passes.
CANONICAL_DECIDE_SCRIPT = (
    "set -euo pipefail",
    "python3 scripts/ci_scope.py --selftest",
    'if [ "$EVENT_NAME" != pull_request ]; then',
    'echo "rtl=true" >> "$GITHUB_OUTPUT"',
    'echo "run_full=true" >> "$GITHUB_OUTPUT"',
    'echo "Non-PR event: exhaustive validation required."',
    "exit 0",
    "fi",
    'if [ -n "$PR_BASE_SHA" ] && git cat-file -e "$PR_BASE_SHA^{commit}" '
    "2>/dev/null; then",
    'git diff --name-only "$PR_BASE_SHA" "$GITHUB_SHA" > '
    '"$RUNNER_TEMP/changed-files"',
    "else",
    'git ls-files > "$RUNNER_TEMP/changed-files"',
    "fi",
    'echo "Changed files:"',
    "sed 's/^/ /' \"$RUNNER_TEMP/changed-files\"",
    'rtl="$(python3 scripts/ci_scope.py < "$RUNNER_TEMP/changed-files")"',
    "run_full=false",
    'if [ "$PR_DRAFT" = false ] && [ "$rtl" = true ]; then',
    "run_full=true",
    "fi",
    'echo "rtl=$rtl" >> "$GITHUB_OUTPUT"',
    'echo "run_full=$run_full" >> "$GITHUB_OUTPUT"',
    'echo "draft=$PR_DRAFT rtl=$rtl run_full=$run_full"',
)
#: The selector's own proof, and the line that consumes the selector's
#: answer: the proof runs once, and before the answer is read.
SELECTOR_SELFTEST = "python3 scripts/ci_scope.py --selftest"
SELECTOR_READ = "python3 scripts/ci_scope.py <"
#: `gh` reads its host, its token and its config directory from the process
#: environment. The assert step's own env is pinned to exactly GH_TOKEN, but
#: an `env` on the JOB or on the WORKFLOW reaches that `gh` without appearing
#: anywhere in the step (#209, O11/O12), so neither level names a `GH_*`.
GH_ENV_PREFIX = "GH_"
#: The shard denominator a worker passes and states in its display name.
#: `matrix.total` is the act-compatible carrier. check_shard_denominator proves
#: it is a singleton equal to the `matrix.shard` list's size and that every
#: consumer uses this expression rather than a literal (#209 O9, #268).
DERIVED_SHARD_TOTAL = "${{ matrix.total }}"
_EXPR = r"\$\{\{[^{}]*\}\}"   # one `${{ ... }}`, kept whole while scanning
SHARD_ARG_RE = re.compile(r'--shard\s+"?((?:' + _EXPR + r'|[^\s"])+)"?')
NAME_SHARD_RE = re.compile(r"\$\{\{\s*matrix\.shard\s*\}\}/((?:"
                           + _EXPR + r'|[^\s"])+)')
SHELL_VAR_RE = re.compile(r"^\$\{?([A-Za-z_][A-Za-z0-9_]*)\}?$")
#: A skipped required context satisfies a GitHub ruleset. Therefore an
#: aggregate may skip only the gate's explicit successful no-op decision. A
#: failed/cancelled gate or an absent/malformed output makes the aggregate run;
#: its target-SHA and shard reconciliation then fail closed.
AGGREGATE_JOB_IF = (
    "${{ always() && "
    f"(needs.{GATE_JOB}.result != 'success' || "
    f"needs.{GATE_JOB}.outputs.{RUN_FULL_OUTPUT} != 'false') }}}}"
)
RUNNER_TEMP_PREFIX = "${{ runner.temp }}/"
#: Public check names the merge bar reads (AGENTS.md section 7), per file.
#: The three documentation contexts are here since #261: a name absent from
#: this map is held by nobody, so a second job renamed to `docs-check`, or
#: `docs-check` itself renamed, passed with every hosted context green.
PUBLIC_NAMES = {
    RTL_FULL: ("verilator-suites", "yosys-portability"),
    RTL_FAST: ("rtl-fast",),
    DOCS: ("docs-check", "wire-accountability", "docs-check-no-git"),
    ELABORATE: ("elaborate",),
}
#: act v0.2.89 shares one action cache across concurrent jobs. Its first use
#: of download-artifact can race when both exhaustive aggregates start
#: together, leaving one action invocation with no downloaded evidence. This
#: direct order keeps that local bootstrap serial without weakening either
#: aggregate: the later job carries `always()` and still audits its own shards.
ACT_ARTIFACT_AGGREGATE_ORDER = PUBLIC_NAMES[RTL_FULL]
#: Every required name in every file: a rendered display name equal to any of
#: them, in any file, is a second carrier ([R4] on PR #293).
ALL_PUBLIC_NAMES = frozenset(n for names in PUBLIC_NAMES.values() for n in names)
EXPRESSION_RE = re.compile(r"\$\{\{.*?\}\}")
MATRIX_REF_RE = re.compile(r"\$\{\{\s*matrix\.([A-Za-z_][A-Za-z0-9_-]*)\s*\}\}")


def rendered_names(job):
    """Every display name an expression-valued `name` can render, enumerated
    from the job's own literal `strategy.matrix`; None when the name uses
    anything but `${{ matrix.<key> }}`, when a referenced key is not a
    non-empty list of scalars, or when the matrix carries `include` or
    `exclude` (either can add a combination this enumeration never saw)."""
    name = job.get("name") if isinstance(job, dict) else None
    if not isinstance(name, str):
        return None
    keys = []
    for expr in EXPRESSION_RE.findall(name):
        m = MATRIX_REF_RE.fullmatch(expr)
        if m is None:
            return None
        if m.group(1) not in keys:
            keys.append(m.group(1))
    strat = job.get("strategy")
    matrix = strat.get("matrix") if isinstance(strat, dict) else None
    if not isinstance(matrix, dict) or "include" in matrix or "exclude" in matrix:
        return None
    lists = []
    for key in keys:
        values = matrix.get(key)
        if (not isinstance(values, list) or not values
                or not all(isinstance(v, (str, int, float, bool)) for v in values)):
            return None
        lists.append([str(v) for v in values])
    out = []
    for combo in itertools.product(*lists):
        binding = dict(zip(keys, combo))
        out.append(EXPRESSION_RE.sub(
            lambda m: binding[MATRIX_REF_RE.fullmatch(m.group(0)).group(1)],
            name))
    return out
ACT_CI_SELFTEST = "python3 scripts/act_ci.py --selftest"
#: ``test_builder.py`` invokes both processor-image/source gates and the
#: Vivado datapath-manifest consumer (syn/ooc/dp_srcs.py), which resolves the
#: shipping AXIS primitives by path, so both hosted jobs which call the
#: builder need this complete set before the call. Keep one canonical
#: command: a split or decoy checkout is too easy to place after the builder
#: or behind another condition.
BUILDER_SUBMODULES = (
    "third_party/verilog-axis",
    "protocol-processor",
    "gptp-processor",
)
BUILDER_COMMAND = "git submodule update --init " + " ".join(BUILDER_SUBMODULES)
BUILDER_CALL = "sw/builder/test_builder.py"
BUILDER_IF = "${{ steps.scope.outputs.rtl == 'true' }}"
BUILDER_RUNS = {
    DOCS: (
        "python3 -m pip install --quiet pyyaml",
        "python3 sw/builder/test_builder.py",
    ),
    ELABORATE: (
        "python3 sw/builder/test_builder.py --require-elaboration",
    ),
}
BUILDER_CHECKOUTS = {
    DOCS: {"uses": "actions/checkout@v4"},
    ELABORATE: {
        "uses": "actions/checkout@v4",
        "with": {"fetch-depth": 0},
    },
}
#: dp_srcs.py answers top resolution with the sv2v front end and REFUSES when
#: no front end exists (no model may stand in for the toolchain), and the
#: builder runs that self-test unconditionally. So every builder job installs
#: the same pinned release the portability gate uses, held here as one exact
#: script: an unpinned version is a silent toolchain drift, and a missing
#: install is a red job dressed as a candidate finding.
SV2V_INSTALL = (
    "set -euo pipefail",
    "ver=v0.0.12",
    'url="https://github.com/zachjs/sv2v/releases/download/${ver}/sv2v-Linux.zip"',
    'curl -fsSL "$url" -o /tmp/sv2v.zip',
    "unzip -q -o /tmp/sv2v.zip -d /tmp/sv2v",
    'sudo install -m755 "$(find /tmp/sv2v -name sv2v -type f | head -1)" /usr/local/bin/sv2v',
    "sv2v --version",
)
#: The fast workflow's selector job and the step that computes its answer.
FAST_SELECTOR_JOB = "changes"
FAST_SCOPE_STEP_ID = "scope"
#: #245: syn/yosys/ooc.sh's refusal self-test, pinned VERBATIM in the job
#: that initialises both processor submodules it reads, and after
#: that initialisation. It is the only thing that exercises ooc.sh's
#: refusals anywhere hosted; deleting the whole step (or neutralising the
#: line, or running it before the fetch) left every other contract item
#: green -- measured by [R-parallel] on PR #262. Verbatim equality of the
#: step's normalized script is the neutralisation guard: `true # ...`,
#: `|| true`, an echo, or a second command are all a different script.
OOC_SH_SELFTEST = "python3 syn/yosys/ooc_selftest.py"
OOC_SH_SELFTEST_JOB = "yosys-elaboration"
OOC_SH_SUBMODULE_FETCH = "git submodule update --init"
#: ...and it must NAME the submodule. Holding the bare verb alone let the
#: fetch be trimmed to `third_party/verilog-axis` with the ordering item and
#: every mutation arm still green, while each self-test arm then died on
#: setup - the checker would not have held what its own docstring claims.
OOC_SH_SUBMODULES = ("protocol-processor", "gptp-processor")
#: The fast selector is a second run/no-run decision, not merely a producer
#: of metadata.  Its exact inputs and body are held for the same reason as
#: the exhaustive selector: an empty or forced-false answer skips both RTL
#: consumers, and the aggregate deliberately accepts those skips.
FAST_CHECKOUT_USES = f"{CHECKOUT_ACTION}@v4"
FAST_CHECKOUT_WITH = {"fetch-depth": "0"}
FAST_SCOPE_STEP_KEYS = ("name", "id", "env", "run")
FAST_SCOPE_STEP_ENV = {
    "EVENT_NAME": "${{ github.event_name }}",
    "PR_BASE_SHA": "${{ github.event.pull_request.base.sha }}",
    "PUSH_BEFORE_SHA": "${{ github.event.before }}",
}
CANONICAL_FAST_SCOPE_SCRIPT = (
    "set -euo pipefail",
    "python3 scripts/ci_scope.py --selftest",
    'base=""',
    'if [ "$EVENT_NAME" = pull_request ]; then',
    'base="$PR_BASE_SHA"',
    "else",
    'base="$PUSH_BEFORE_SHA"',
    "fi",
    'if [ -n "$base" ] && [ "$base" != '
    '0000000000000000000000000000000000000000 ] && '
    'git cat-file -e "$base^{commit}" 2>/dev/null; then',
    'git diff --name-only "$base" "$GITHUB_SHA" > '
    '"$RUNNER_TEMP/changed-files"',
    "else",
    "# An unknown base must never turn a real change into docs-only.",
    'git ls-files > "$RUNNER_TEMP/changed-files"',
    "fi",
    'echo "Changed files:"',
    'sed \'s/^/ /\' "$RUNNER_TEMP/changed-files"',
    'rtl="$(python3 scripts/ci_scope.py < "$RUNNER_TEMP/changed-files")"',
    'echo "rtl=$rtl" >> "$GITHUB_OUTPUT"',
    'echo "RTL/tooling relevant: $rtl"',
)
#: The fast workflow's aggregate `if`. It counts a skipped consumer as a pass
#: deliberately (a docs-only change legitimately runs no RTL lint), which is
#: exactly why that workflow's published answer has to be pinned by content
#: too: rebind it and every consumer skips into that pass.
FAST_AGGREGATE_JOB_IF = "${{ always() && !cancelled() }}"
#: The fast aggregate's one verdict step. That step is the entire conversion
#: of four job results into the required `rtl-fast` context ([R2] on PR
#: #239): the job itself runs under `always() && !cancelled()`, so an `if` on
#: the step, a rebound result binding, or a `case` widened to accept
#: `failure` each leaves every job key canonical while a FAILED consumer
#: still yields a green required context. So the step's keys are pinned, its
#: env is derived from the aggregate's `needs` (one `<JOB>_RESULT` name per
#: needed job, bound to `${{ needs.<job>.result }}`), and its script is the
#: canonical form derived from the same list.
FAST_VERDICT_STEP_KEYS = ("name", "env", "run")


def step_output_ref(step_id, name):
    """`${{ steps.<id>.outputs.<name> }}`, built rather than restated."""
    return "${{ steps." + step_id + ".outputs." + name + " }}"


def needs_output_ref(job_id, name):
    """`needs.<job>.outputs.<name>`, built rather than restated."""
    return "needs." + job_id + ".outputs." + name


def needs_result_ref(job_id):
    """`${{ needs.<job>.result }}`, built rather than restated."""
    return "${{ needs." + job_id + ".result }}"


def fast_result_env_name(job_id):
    """The env name the fast verdict step reads one needed job's result
    through, derived from the job id, never a second list:
    `verilator-lint` -> `VERILATOR_LINT_RESULT`."""
    return job_id.upper().replace("-", "_") + "_RESULT"


def canonical_fast_verdict_script(needed):
    """The fast verdict step's script, derived from the aggregate's `needs`:
    one `job:$JOB_RESULT` pair per needed job, in `needs` order, and a `case`
    that accepts exactly `success` and `skipped`."""
    pairs = " ".join('"%s:$%s"' % (j, fast_result_env_name(j))
                     for j in needed)
    return (
        "set -euo pipefail",
        "bad=0",
        f"for pair in {pairs}; do",
        'name="${pair%%:*}"',
        'result="${pair#*:}"',
        "printf '%-24s %s\\n' \"$name\" \"$result\"",
        'case "$result" in',
        "success|skipped) ;;",
        "*) bad=1 ;;",
        "esac",
        "done",
        '[ "$bad" -eq 0 ]',
    )


def consumer_job_if(job_id, name):
    """The exact `if` a job gated on a selector's published decision carries."""
    return "${{ " + needs_output_ref(job_id, name) + " == 'true' }}"


#: THE PUBLICATION PATH, per workflow: the job that publishes the decision,
#: its `outputs` map as NAME -> BINDING, and the output its consumers gate on.
#:
#: Three rounds of [R0] on PR #239 each found one more member of a perimeter
#: nobody had enumerated: the gate's sibling steps, then those steps' env
#: BINDINGS, then this map. Each round pinned the instance and left the
#: perimeter an allow-list written from the last review, so the next unlisted
#: thing was outside it again. A job's `outputs` is the same
#: NAME -> EXPRESSION mapping a step's `env` is, and checking only that
#: `target_sha` existed let `run_full: ${{ 'false' }}` -- valid job-output
#: YAML, every pinned step key, env binding and script character intact --
#: publish the no-op decision: both worker matrices skip, both aggregates
#: skip under their documented no-op exception, and a skipped required
#: context satisfies a GitHub ruleset. The same hole is open a second time in
#: rtl-fast.yml, whose `changes` job gates the two RTL fast checks the same
#: way. So the maps are pinned by content here and check_publication_path
#: closes the path around them: every consumer of a selector carries a pinned
#: `if`, and no `needs.<job>.outputs.<name>` expression anywhere may name an
#: output no job publishes or a job it does not need.
SELECTOR_JOB = {RTL_FULL: GATE_JOB, RTL_FAST: FAST_SELECTOR_JOB}
SELECTOR_OUTPUTS = {
    RTL_FULL: {
        RUN_FULL_OUTPUT: step_output_ref(DECIDE_STEP_ID, RUN_FULL_OUTPUT),
        RTL_OUTPUT: step_output_ref(DECIDE_STEP_ID, RTL_OUTPUT),
        GATE_OUTPUT: step_output_ref(PIN_STEP_ID, GATE_OUTPUT),
    },
    RTL_FAST: {
        RTL_OUTPUT: step_output_ref(FAST_SCOPE_STEP_ID, RTL_OUTPUT),
    },
}
#: The output whose value decides whether the consumers run at all.
SELECTOR_DECISION = {RTL_FULL: RUN_FULL_OUTPUT, RTL_FAST: RTL_OUTPUT}
#: The `if` each workflow's own aggregate carries. WHICH job that is is
#: derived, not listed again: the aggregate is the job whose display name is
#: the public required check the merge bar reads (PUBLIC_NAMES above).
AGGREGATE_IF = {RTL_FULL: AGGREGATE_JOB_IF, RTL_FAST: FAST_AGGREGATE_JOB_IF}
#: A `needs` context reference can use property syntax, index syntax, or mix
#: them: `needs.changes.outputs.rtl`, `needs['changes'].outputs.rtl`, and
#: `needs['changes']['outputs']['rtl']` are the same reference to GitHub.  A
#: regex for only the first spelling made the second invisible to the gate.
#: The small access-chain parser below resolves every static spelling and
#: refuses dynamic brackets, whose producer/output cannot be audited here.
NEEDS_WORD_RE = re.compile(r"\bneeds\b")
CONTEXT_NAME_RE = re.compile(r"[A-Za-z0-9_-]+")

SHA_RE = re.compile(r"^[0-9a-f]{40}$")
CRON_RE = re.compile(r"^\s*(\d{1,2})\s+(\d{1,2})\s+\*\s+\*\s+\*\s*$")


class CannotRun(Exception):
    """An input the check cannot judge: missing, unparseable, no pyyaml."""


# --------------------------------------------------------------------------
# Loading
# --------------------------------------------------------------------------

def load_yaml(text, path):
    try:
        import yaml  # noqa: WPS433  (deliberately late: absence is rc 2)
    except ImportError as exc:
        raise CannotRun("pyyaml is not importable; install python3-yaml "
                        "or `pip install pyyaml`") from exc
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as exc:
        raise CannotRun(f"{path}: does not parse as YAML: {exc}") from exc
    if not isinstance(doc, dict):
        raise CannotRun(f"{path}: top level is not a mapping")
    return doc


def read_tree(root):
    """The five files as text, keyed by their repository-relative path."""
    world = {}
    for rel in FILES:
        path = root / rel
        try:
            world[rel] = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise CannotRun(f"{rel}: cannot read: {exc}") from exc
    return world


def parse_world(world):
    """Text world -> parsed world: YAML mappings for workflows, text for the
    policy page. Raises CannotRun for anything it cannot judge."""
    parsed = {}
    for rel in FILES:
        if rel not in world:
            raise CannotRun(f"{rel}: missing")
        parsed[rel] = (load_yaml(world[rel], rel) if rel in WORKFLOWS
                       else world[rel])
    return parsed


# --------------------------------------------------------------------------
# Helpers over a parsed workflow
# --------------------------------------------------------------------------

def triggers(wf):
    """The `on:` mapping. PyYAML 1.1 reads the bare key `on` as boolean True,
    so accept both spellings; anything else is an empty contract."""
    on = wf.get("on", wf.get(True))
    return on if isinstance(on, dict) else {}


def jobs(wf):
    j = wf.get("jobs")
    return j if isinstance(j, dict) else {}


def steps(job):
    s = job.get("steps") if isinstance(job, dict) else None
    return [x for x in s if isinstance(x, dict)] if isinstance(s, list) else []


def display_name(job_id, job):
    name = job.get("name") if isinstance(job, dict) else None
    return name if isinstance(name, str) and name.strip() else job_id


def step_text(step):
    """Everything a step says: its run script plus its env values, so an
    expression passed through `env:` counts as referenced."""
    parts = []
    run = step.get("run")
    if isinstance(run, str):
        parts.append(run)
    env = step.get("env")
    if isinstance(env, dict):
        parts.extend(str(v) for v in env.values())
    return "\n".join(parts)


def uses(step, action):
    u = step.get("uses")
    return isinstance(u, str) and (u == action or u.startswith(action + "@"))


def step_label(step):
    """What a finding calls a step: its name, its `uses`, or its `id`."""
    if not isinstance(step, dict):
        return "no step at this position"
    for key in ("name", "uses", "id"):
        value = step.get(key)
        if isinstance(value, str) and value.strip():
            return f"`{value.strip()}`"
    return "an unnamed step"


def _is_checkout_step(step):
    return uses(step, CHECKOUT_ACTION)


def _is_pin_step(step):
    return step.get("id") == PIN_STEP_ID


def _is_assert_step(step):
    return DEFAULT_BRANCH_FLAG in step_text(step)


def _is_decide_step(step):
    return step.get("id") == DECIDE_STEP_ID


#: (label, recognizer, what it must be, keys, env keys, optional keys) for
#: every step of the gate job, in the order they must appear. The SEQUENCE is
#: the point: the assertion runs the `ci_events.py` the checkout brought and
#: the decision diffs the tree that checkout produced, so a step moved before
#: the checkout runs without the file it needs, a step inserted anywhere runs
#: before everything after it and can change what they read, and a step
#: removed takes its assertion with it. None of those three touches a single
#: character of the pinned script text.
GATE_STEPS = (
    ("the gate checkout step", _is_checkout_step,
     f"`uses: {CHECKOUT_ACTION}` with `fetch-depth: {CHECKOUT_FETCH_DEPTH}`",
     CHECKOUT_STEP_KEYS, {}, CHECKOUT_STEP_OPTIONAL),
    ("the pin step", _is_pin_step,
     f"the step with `id: {PIN_STEP_ID}` that prints the event and exports "
     f"`{GATE_OUTPUT}`", PIN_STEP_KEYS, {}, ()),
    ("the default-branch step", _is_assert_step,
     f"the step that runs `ci_events.py {DEFAULT_BRANCH_FLAG}`",
     ASSERT_STEP_KEYS, ASSERT_STEP_ENV, ()),
    ("the decision step", _is_decide_step,
     f"the step with `id: {DECIDE_STEP_ID}` that publishes `run_full`",
     DECIDE_STEP_KEYS, DECIDE_STEP_ENV, ()),
)


def cron_time(cron):
    """`M H * * *` -> `HH:MM UTC`, or None for any other shape."""
    m = CRON_RE.match(cron) if isinstance(cron, str) else None
    if not m:
        return None
    minute, hour = int(m.group(1)), int(m.group(2))
    if not (0 <= minute <= 59 and 0 <= hour <= 23):
        return None
    return f"{hour:02d}:{minute:02d} UTC"


# --------------------------------------------------------------------------
# The contract
# --------------------------------------------------------------------------

class Contract:
    def __init__(self):
        self.checked = 0
        self.findings = []
        self.notes = []

    def item(self, ok, path, what):
        self.checked += 1
        if not ok:
            self.findings.append(f"{path}: {what}")


def check_push_and_pr(c, path, wf, exact_types):
    on = triggers(wf)
    push = on.get("push")
    branches = push.get("branches") if isinstance(push, dict) else None
    c.item(isinstance(branches, list) and PUSH_BRANCH in branches, path,
           f"push must subscribe branches including `{PUSH_BRANCH}` "
           f"(found {branches!r})")
    c.item("pull_request" in on, path, "must subscribe pull_request")
    if exact_types:
        pr = on.get("pull_request")
        types = pr.get("types") if isinstance(pr, dict) else None
        ok = (isinstance(types, list) and len(types) == len(PR_TYPES)
              and set(types) == set(PR_TYPES))
        c.item(ok, path, "pull_request.types must be exactly "
               f"{list(PR_TYPES)} (found {types!r})")


def check_cancel_in_progress(c, path, wf):
    conc = wf.get("concurrency")
    cancel = conc.get("cancel-in-progress") if isinstance(conc, dict) else None
    c.item(cancel is True, path,
           f"concurrency.cancel-in-progress must be true (found {cancel!r})")
    group = conc.get("group") if isinstance(conc, dict) else None
    ok = (isinstance(group, str) and "github.event.pull_request.number" in group
          and "github.ref" in group)
    c.item(ok, path, "concurrency.group must scope to the PR number or the "
           f"ref (found {group!r})")


def check_public_names(c, path, wf):
    """Each public check-run name the merge bar reads is carried by exactly
    one job. Existence alone held nothing ([R2] on PR #239): a second job
    renamed to the aggregate's display name publishes a second check run
    under the required name, and which of the two the ruleset binds is
    ambiguous."""
    all_jobs = jobs(wf)
    # A display name is read here as a literal string, and GitHub evaluates
    # `jobs.<id>.name` as an expression ([R4] on PR #293): `name: ${{ 'X' }}`
    # publishes a check run named X that no literal comparison sees, so a
    # `run: true` job spelled that way was a second carrier of every
    # required name with no finding. The only expression names this tree
    # carries are the sharded workers' `... shard ${{ matrix.shard }}/${{
    # matrix.total }}`, so the rule is: a `name` may reference nothing but
    # `matrix.<key>` lists of the job's own literal `strategy.matrix`, every
    # rendering is enumerated and none may be a required name, and any other
    # expression is refused outright, because it cannot be enumerated here.
    for jid, j in all_jobs.items():
        name = j.get("name") if isinstance(j, dict) else None
        if not (isinstance(name, str) and "${{" in name):
            continue
        rendered = rendered_names(j)
        c.item(rendered is not None, path,
               f"job `{jid}` `name` must be a literal or reference only "
               f"`${{{{ matrix.<key> }}}}` lists of its own `strategy.matrix` "
               f"(found {name!r}): any other expression evaluates on the "
               "runner to a display name this rule cannot read, so it can "
               "publish a check run under a required name unseen")
        for got in rendered or ():
            c.item(got not in ALL_PUBLIC_NAMES, path,
                   f"job `{jid}` `name` renders `{got}` for one matrix "
                   "combination, which is a required check name: a matrix "
                   "job publishing that name is a second carrier the "
                   "literal comparison above cannot see")
    for want in PUBLIC_NAMES.get(path, ()):
        carriers = [jid for jid, j in all_jobs.items()
                    if display_name(jid, j) == want]
        c.item(len(carriers) == 1, path,
               f"public check name `{want}` must be carried by exactly one "
               f"job (carried by {carriers or 'none'}, jobs are "
               f"{sorted(all_jobs)}): the merge bar reads this name, and two "
               "jobs publishing it make which run the ruleset binds "
               "ambiguous")


def check_required_context_carriers(c, path, wf, held_by_builder=()):
    """Each public check name is carried by the job of that id, and that job
    runs as written: no `needs`, no `if`, no `continue-on-error`, no
    `defaults` (#261).

    The RTL workflows reach every job through their aggregate's `needs` and
    classify each one as the selector, a consumer or a held contributor. The
    documentation and elaboration workflows have no aggregate: the carrier
    IS the required context, and a skipped required context satisfies the
    ruleset. So `if: false` on `docs-check` retired this gate itself (docs.yml
    is the only workflow that runs `--check`), and the same lever on
    `wire-accountability` or `docs-check-no-git` retired the item-00 record
    or the no-git proof, with `checked=171 findings=0` at `70421f5c`.

    The NAME and the CONTENT must be held on one job ([R3] on PR #293). The
    merge bar binds a display name; the builder contract and the step pins
    below read `docs-check` and `elaborate` by job id. Held apart, the real
    job renamed to `docs-check-real` beside a `decoy` job named `docs-check`
    with one `run: true` step passed with 233 items and no finding: the
    unique carrier had no neuter key and the id-named job kept its pinned
    content, while the required context ran nothing. So the job whose id is
    the public name must carry it. `held_by_builder` names the ids whose
    keys check_builder_dependencies already holds by the same function, so
    each refusal is printed once. An ambiguous carrier is named by
    check_public_names, not here."""
    all_jobs = jobs(wf)
    for want in PUBLIC_NAMES.get(path, ()):
        job = all_jobs.get(want)
        got = display_name(want, job) if isinstance(job, dict) else None
        c.item(got == want, path,
               f"required context `{want}` must be carried by the job of that "
               f"id (found "
               + ("no such job" if got is None else f"job `{want}` named `{got}`")
               + "): the content checks read that job by id, so a job "
               "carrying the name under another id is a stub the merge bar "
               "binds while the real gates run under a name it does not read")
        carriers = [jid for jid, j in all_jobs.items()
                    if display_name(jid, j) == want]
        if len(carriers) != 1 or carriers[0] in held_by_builder:
            continue
        check_job_keys(c, path, carriers[0], all_jobs[carriers[0]])


def check_act_artifact_aggregate_order(c, path, wf):
    """Keep act's shared download-action bootstrap single-file.

    The public-name check separately proves each display name has exactly one
    carrier. Once those carriers are known, require each later aggregate to
    directly need the prior one. A transitive or incidental order is too easy
    to lose while editing unrelated worker dependencies.
    """
    all_jobs = jobs(wf)
    carriers = {}
    for name in ACT_ARTIFACT_AGGREGATE_ORDER:
        found = [jid for jid, job in all_jobs.items()
                 if display_name(jid, job) == name]
        if len(found) == 1:
            carriers[name] = found[0]
    for earlier, later in zip(ACT_ARTIFACT_AGGREGATE_ORDER,
                              ACT_ARTIFACT_AGGREGATE_ORDER[1:]):
        earlier_id = carriers.get(earlier)
        later_id = carriers.get(later)
        if earlier_id is None or later_id is None:
            continue
        c.item(earlier_id in needs_list(all_jobs[later_id]), path,
               f"job `{later_id}` must need `{earlier_id}` before starting "
               "its artifact download: act v0.2.89 shares the action cache, "
               "and concurrent first-use download actions can lose one "
               "aggregate's evidence")


def check_rtl_full(c, wf, policy):
    path = RTL_FULL
    check_push_and_pr(c, path, wf, exact_types=True)
    on = triggers(wf)

    # Dispatch: present, and no inputs. The documented command has none, and a
    # required input would make `gh workflow run rtl.yml --ref <branch>` fail.
    c.item("workflow_dispatch" in on, path, "must subscribe workflow_dispatch")
    dispatch = on.get("workflow_dispatch")
    has_inputs = isinstance(dispatch, dict) and bool(dispatch.get("inputs"))
    c.item(not has_inputs, path, "workflow_dispatch must carry no inputs: the "
           "dispatcher chooses the ref and nothing else")

    # Schedule: exactly one cron of the `M H * * *` shape, stated on the page
    # both as the literal string and as the rendered time.
    sched = on.get("schedule")
    crons = ([e.get("cron") for e in sched if isinstance(e, dict)]
             if isinstance(sched, list) else [])
    c.item(len(crons) == 1, path,
           f"schedule must carry exactly one cron (found {crons!r})")
    cron = crons[0] if len(crons) == 1 else None
    when = cron_time(cron)
    c.item(when is not None, path,
           f"cron must be a daily `M H * * *` entry (found {cron!r})")
    if when is not None:
        c.item(f"`{cron}`" in policy, POLICY,
               f"must state the cron string `{cron}`")
        c.item(when in policy, POLICY,
               f"must state the cron's time as {when}")
        c.notes.append(f"cron `{cron}` renders {when}; the policy page states both")

    check_cancel_in_progress(c, path, wf)
    check_public_names(c, path, wf)
    check_act_artifact_aggregate_order(c, path, wf)

    # One authoritative SHA: no checkout overrides the event's pinned commit.
    for jid, job in jobs(wf).items():
        for n, step in enumerate(steps(job), 1):
            if uses(step, "actions/checkout"):
                with_ = step.get("with")
                overrides = isinstance(with_, dict) and "ref" in with_
                c.item(not overrides, path,
                       f"job `{jid}` step {n}: actions/checkout must not "
                       f"override `ref` (found {with_!r})")

    # The gate prints the event and the SHA, and exports target_sha.
    gate = jobs(wf).get(GATE_JOB)
    c.item(isinstance(gate, dict), path, f"job `{GATE_JOB}` must exist")
    if isinstance(gate, dict):
        prints = any("GITHUB_EVENT_NAME" in step_text(s)
                     and "GITHUB_SHA" in step_text(s) for s in steps(gate))
        c.item(prints, path, f"job `{GATE_JOB}` must print the event name and "
               "GITHUB_SHA in one step")
        check_default_branch_step(c, path, gate)
        check_decide_step(c, path, gate)
        check_gate_steps(c, path, gate)
        check_job_keys(c, path, GATE_JOB, gate)
        check_no_gh_env(c, path, f"job `{GATE_JOB}`", gate.get("env"))
    check_no_gh_env(c, path, "the workflow's top-level", wf.get("env"))
    c.item("defaults" not in wf, path, "the workflow must carry no top-level "
           f"`defaults` (found {wf.get('defaults')!r}): a `defaults.run.shell`"
           " changes how every script runs")

    # Every job that uploads evidence records the SHA first; every job that
    # downloads evidence verifies it against the gate's output.
    ref = f"needs.{GATE_JOB}.outputs.{GATE_OUTPUT}"
    for jid, job in jobs(wf).items():
        ss = steps(job)
        upload_at = next((i for i, s in enumerate(ss)
                          if uses(s, "actions/upload-artifact")), None)
        if upload_at is not None:
            recorded = any(RECORD in step_text(s) and "GITHUB_SHA" in step_text(s)
                           and ref in step_text(s) for s in ss[:upload_at])
            c.item(recorded, path, f"job `{jid}` uploads evidence and must "
                   f"first write GITHUB_SHA into {RECORD}, checked against "
                   f"{ref}")
        if any(uses(s, "actions/download-artifact") for s in ss):
            vsteps = [s for s in ss if VERIFY_FLAG in step_text(s)
                      and "ci_events.py" in step_text(s)]
            verifies = any(ref in step_text(s) for s in vsteps)
            c.item(verifies, path, f"job `{jid}` downloads evidence and must "
                   f"run scripts/ci_events.py {VERIFY_FLAG} against {ref}")
            needs = job.get("needs")
            needs = needs if isinstance(needs, list) else [needs]
            c.item(GATE_JOB in needs, path,
                   f"job `{jid}` must need `{GATE_JOB}` to read its output")
            if vsteps:
                check_sha_sources(c, path, jid, vsteps[0])
                check_verify_step(c, path, wf, jid, job, vsteps[0])

    # A sharded worker states its shard count once, in the matrix.
    for jid, job in jobs(wf).items():
        check_shard_denominator(c, path, jid, job)

    # The decision's publication path: the outputs map that carries it and
    # every job that runs on it. check_job_keys for the aggregates lives
    # there now, beside the same call for the workers.
    check_publication_path(c, path, wf)


def all_scalars(node):
    """Every scalar in a parsed YAML subtree, as text. An expression can sit
    in an `if`, a display `name`, a `run`, an `env` value or a `with` value,
    so the walk is over the subtree rather than over a list of the places
    somebody remembered to look in."""
    if isinstance(node, dict):
        for k, v in node.items():
            yield from all_scalars(k)
            yield from all_scalars(v)
    elif isinstance(node, list):
        for v in node:
            yield from all_scalars(v)
    elif node is not None:
        yield str(node)


def needs_list(job):
    """A job's `needs`, as a list whether it was written as one or not."""
    n = job.get("needs") if isinstance(job, dict) else None
    if isinstance(n, list):
        return [str(x) for x in n]
    return [] if n is None else [str(n)]


def context_bracket_end(text, start):
    """Index of the `]` matching `text[start]`, or None.

    GitHub expression strings use single quotes and escape one quote as two.
    Accounting for them here keeps a `]` inside a dynamic expression's string
    from ending the access early; nested brackets are handled as well.
    """
    depth = 0
    quoted = False
    i = start
    while i < len(text):
        ch = text[i]
        if quoted:
            if ch == "'":
                if i + 1 < len(text) and text[i + 1] == "'":
                    i += 2
                    continue
                quoted = False
        elif ch == "'":
            quoted = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return None


def context_access_chain(text, start):
    """Parse static `.name` / `['name']` accesses after a context word.

    Returns `(parts, dynamic, end)`. A None part is a dynamic bracket. The
    caller refuses it because no static workflow audit can prove which job or
    output it names.
    """
    parts = []
    dynamic = False
    pos = start
    while True:
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos < len(text) and text[pos] == ".":
            pos += 1
            while pos < len(text) and text[pos].isspace():
                pos += 1
            match = CONTEXT_NAME_RE.match(text, pos)
            if match is None:
                dynamic = True
                break
            parts.append(match.group(0))
            pos = match.end()
            continue
        if pos < len(text) and text[pos] == "[":
            end = context_bracket_end(text, pos)
            if end is None:
                dynamic = True
                pos = len(text)
                break
            inside = text[pos + 1:end].strip()
            match = re.fullmatch(r"'([A-Za-z0-9_-]+)'", inside)
            parts.append(match.group(1) if match else None)
            dynamic = dynamic or match is None
            pos = end + 1
            continue
        break
    return parts, dynamic, pos


def needs_context_references(text):
    """Static `needs` context chains in one scalar: `(producer, output)`
    refs, every producer any static chain names, and unresolved chains.

    The producer set covers every second component, `.result` included, not
    only `.outputs.` ([R2] on PR #239): a `needs.<job>.result` read from a
    job outside `needs` is the same empty string the `.outputs.` audit
    exists for, so stopping at `.outputs.` left `.result` a silent skip. A
    bare `needs` with no chain (as in `toJSON(needs)`) names no producer and
    is not audited here."""
    refs = set()
    producers = set()
    unresolved = set()
    for match in NEEDS_WORD_RE.finditer(text or ""):
        parts, dynamic, end = context_access_chain(text, match.end())
        if dynamic:
            shown = text[match.start():end].strip() or "needs[...]"
            unresolved.add(shown)
            continue
        if not parts:
            continue
        producers.add(parts[0])
        if len(parts) >= 2 and parts[1] == "outputs":
            if len(parts) < 3:
                unresolved.add(text[match.start():end].strip())
            else:
                refs.add((parts[0], parts[2]))
    return refs, producers, unresolved


def check_publication_path(c, path, wf):
    """The whole path a selector's decision travels: the step that computes
    it, the job `outputs` map that publishes it, and the jobs that run on it.

    The perimeter here is CLOSED rather than listed. The selector's `outputs`
    map is pinned by content, exactly as a pinned step's `env` is; every job
    that needs the selector is then classified with no residue -- the
    workflow's aggregate is the job carrying the public required check name,
    every other such job is a consumer gated on the decision -- and each
    class carries a pinned `if`. A job added tomorrow that depends on the
    selector lands in the consumer class and reddens until it carries that
    `if`, instead of arriving outside every contract the way both worker
    matrices and both fast-lane consumers did (#209, [R0] rounds 1-3).
    Closure runs in both directions ([R2] on PR #239): every job an
    aggregate needs is also classified, so a contributor wired straight into
    the aggregate without needing the selector is held to run as written
    rather than landing in no class."""
    sel = SELECTOR_JOB[path]
    want = SELECTOR_OUTPUTS[path]
    decision = SELECTOR_DECISION[path]
    all_jobs = jobs(wf)
    selector = all_jobs.get(sel)
    c.item(isinstance(selector, dict), path, f"job `{sel}` must exist: it "
           "publishes the decision the rest of this workflow runs on")
    outputs = selector.get("outputs") if isinstance(selector, dict) else None
    pinned_bindings(c, path, f"job `{sel}` outputs",
                    outputs if isinstance(outputs, dict) else {}, want,
                    "a job output is what `needs.<job>.outputs.<name>` reads, "
                    "so the decision step may write the right value and the "
                    "job still export another one; every consumer then skips, "
                    "and a skipped required context satisfies the ruleset")

    public = set(PUBLIC_NAMES.get(path, ()))
    for jid, job in all_jobs.items():
        if jid == sel or sel not in needs_list(job):
            continue
        aggregate = display_name(jid, job) in public
        check_job_keys(c, path, jid, job, allow_needs=True,
                       allowed_if=(AGGREGATE_IF[path] if aggregate
                                   else consumer_job_if(sel, decision)))

    # [R2] on PR #239: a job wired straight into an aggregate's `needs`
    # without itself needing the selector, as `bdd-conformance` is, landed in
    # no class above, so an `if: false` on it disabled the specification
    # suite with every hosted context green and the aggregate accepting the
    # skip. So every job an aggregate needs is classified: the selector, a
    # consumer (classified above), or itself held to run as written.
    for jid, job in all_jobs.items():
        if display_name(jid, job) not in public:
            continue
        for member in sorted(set(needs_list(job))):
            mjob = all_jobs.get(member)
            if not isinstance(mjob, dict):
                c.item(False, path, f"job `{jid}` needs `{member}`, which "
                       "must exist as a job in this workflow")
                continue
            if member == sel or sel in needs_list(mjob):
                continue
            check_job_keys(c, path, member, mjob)

    for jid, job in all_jobs.items():
        refs = set()
        producers = set()
        unresolved = set()
        for scalar in all_scalars(job):
            found, named, unknown = needs_context_references(scalar)
            refs.update(found)
            producers.update(named)
            unresolved.update(unknown)
        for expression in sorted(unresolved):
            c.item(False, path, f"job `{jid}` uses `{expression}`, a dynamic "
                   "or incomplete `needs` context the gate cannot resolve "
                   "statically: use a dotted or single-quoted static job and "
                   "output name so publication and dependency can be proved")
        for producer, name in sorted(refs):
            pj = all_jobs.get(producer)
            declared = pj.get("outputs") if isinstance(pj, dict) else None
            declared = declared if isinstance(declared, dict) else {}
            c.item(name in declared, path,
                   f"job `{jid}` reads `{needs_output_ref(producer, name)}`, "
                   f"which job `{producer}` must publish (publishes "
                   f"{sorted(declared)}): an expression naming an output no "
                   "job declares is the empty string, so every comparison "
                   "against it is false and every job gated on it skips")
        for producer in sorted(producers):
            c.item(producer in needs_list(job), path,
                   f"job `{jid}` reads the `needs.{producer}` context and "
                   f"must list `{producer}` in its `needs` (found "
                   f"{needs_list(job)}): outside `needs` the expression is "
                   "the empty string, so a `.result` or `.outputs` guard "
                   "built on it is quietly false and the step or job it "
                   "guards skips")


def check_job_keys(c, path, jid, job, allowed_if=None, allow_needs=False):
    """A job that must run as written carries none of the keys that decide
    whether it runs at all: no `needs`, no `if` (or exactly the one
    documented), no `continue-on-error`, no `defaults`. Each refusal names
    the key and what that key does."""
    for key, reason in JOB_NEUTER_KEYS.items():
        if key == "needs" and allow_needs:
            continue
        if key not in job:
            continue
        if key == "if" and allowed_if is not None:
            got = str(job.get("if")).strip()
            c.item(got == allowed_if, path, f"job `{jid}` `if` must be exactly "
                   f"`{allowed_if}` (found `{got}`)")
            continue
        c.item(False, path, f"job `{jid}` must carry no `{key}` "
               f"(found {job.get(key)!r}): {reason}")
    if allowed_if is not None:
        c.item("if" in job, path, f"job `{jid}` must carry its documented "
               f"`if` `{allowed_if}`")


def pinned_step_keys(c, path, what, step, keys, env_keys, optional=()):
    """A pinned step carries exactly `keys` (plus anything in `optional`),
    and its env is exactly `env_keys`, a NAME -> EXPRESSION mapping: the
    names it carries and, for each, the source it is bound to. Every surplus
    key, missing key and rebound value is named. Holding the names alone let
    `PR_DRAFT: "true"` pass every item in this file ([R0] on PR #239), so the
    binding is checked here, once, for every pinned step there is."""
    have = [k for k in step.keys() if isinstance(k, str)]
    extra = sorted(set(have) - set(keys) - set(optional))
    missing = [k for k in keys if k not in have]
    for key in ("if", "shell", "continue-on-error"):
        if key in extra:
            c.item(False, path, f"{what} must carry no `{key}` "
                   f"(found {step.get(key)!r}): it decides whether or how "
                   "the script runs")
    c.item(not extra and not missing, path, f"{what} keys must be exactly "
           f"{', '.join(keys)}" + (f"; surplus: {', '.join(extra)}" if extra
                                   else "")
           + (f"; missing: {', '.join(missing)}" if missing else ""))
    env = step.get("env") if isinstance(step.get("env"), dict) else {}
    pinned_bindings(c, path, f"{what} env", env, env_keys,
                    "the name is not the contract, the source expression "
                    "behind it is, and a rebound value leaves every pinned "
                    "name and key in place while changing what the script "
                    "reads",
                    surplus_note=" (a GH_HOST or GH_CONFIG_DIR redirects gh "
                                 "away from this repository)")


def pinned_bindings(c, path, what, mapping, want, reason, surplus_note=""):
    """A NAME -> EXPRESSION mapping held by CONTENT: exactly these names, and
    for each the exact source expression it is bound to. A step's `env` and a
    job's `outputs` are the same object, and holding either by its key set
    alone holds nothing: both escapes that reached [R0] on PR #239 kept every
    pinned name in place and changed only what the name was bound to. So
    there is one comparison, used by both."""
    have = sorted(str(k) for k in mapping.keys())
    extra = sorted(set(have) - set(want))
    missing = [k for k in want if k not in have]
    c.item(not extra and not missing, path, f"{what} must be exactly "
           f"{', '.join(want) or 'empty'}"
           + (f"; surplus: {', '.join(extra)}{surplus_note}" if extra else "")
           + (f"; missing: {', '.join(missing)}" if missing else ""))
    for name, expr in want.items():
        if name not in mapping:
            continue
        got = str(mapping.get(name)).strip()
        c.item(got == expr, path, f"{what} must bind `{name}` to `{expr}` "
               f"(found `{got}`): {reason}")


def check_gate_steps(c, path, gate):
    """The gate job's steps: which ones exist, in which order, and the keys
    each may carry. check_default_branch_step holds the assert step's script
    TEXT; this holds everything around it, which is what decides whether that
    script runs at all (#209)."""
    ss = steps(gate)
    c.item(len(ss) == len(GATE_STEPS), path,
           f"job `{GATE_JOB}` must carry exactly {len(GATE_STEPS)} steps, "
           + ", ".join(spec[0] for spec in GATE_STEPS)
           + f", in that order (found {len(ss)}): a step inserted here runs "
           "before every step after it and can change what they read (an "
           "entry appended to GITHUB_PATH puts another `gh` first), and a "
           "step removed takes its assertion with it")
    for n, (label, recognizer, want, keys, env_keys, optional) in enumerate(
            GATE_STEPS, 1):
        found = [s for s in ss if recognizer(s)]
        step = found[0] if found else None
        at = ss[n - 1] if len(ss) >= n else None
        c.item(step is not None and at is step, path,
               f"job `{GATE_JOB}` step {n} must be {label}, {want} (found "
               f"{step_label(at)}): the assertion runs the ci_events.py the "
               "checkout brought and the decision diffs the tree that "
               "checkout produced, so this order is the contract, not a "
               "preference")
        if step is not None:
            pinned_step_keys(c, path, label, step, keys, env_keys, optional)
    checkout = next((s for s in ss if _is_checkout_step(s)), None)
    with_ = checkout.get("with") if isinstance(checkout, dict) else None
    depth = with_.get("fetch-depth") if isinstance(with_, dict) else None
    c.item(depth == CHECKOUT_FETCH_DEPTH, path,
           f"{GATE_STEPS[0][0]} must set `fetch-depth: "
           f"{CHECKOUT_FETCH_DEPTH}` (found {depth!r}): the decision step "
           "diffs this head against the pull request's base commit, which a "
           "shallow clone does not carry, so a shallow gate silently falls "
           "back to the whole file list")


def script_difference(got, want):
    """The first line where a script differs from its canonical form, named
    rather than dumped: a whole-script listing of a twenty-line script buries
    the one line that moved."""
    for i in range(max(len(got), len(want))):
        g = got[i] if i < len(got) else None
        w = want[i] if i < len(want) else None
        if g != w:
            return (f"line {i + 1} must be {w!r} (found {g!r}); "
                    f"{len(want)} line(s) expected, {len(got)} found")
    return f"{len(want)} line(s) expected, {len(got)} found"


def check_decide_step(c, path, gate):
    """The decision step publishes `run_full`, the one value that decides
    whether the exhaustive gates run at all. Its keys and its env bindings
    are held in check_gate_steps; this holds its script, verbatim after
    whitespace normalization, the way the default-branch step's is. Binding
    the inputs without holding the body would leave `run_full=true` ->
    `run_full=false` a legal edit ([R0] on PR #239)."""
    found = [s for s in steps(gate) if _is_decide_step(s)]
    c.item(len(found) == 1, path, f"job `{GATE_JOB}` must carry exactly one "
           f"step with `id: {DECIDE_STEP_ID}` (found {len(found)})")
    if len(found) != 1:
        return
    run = found[0].get("run") if isinstance(found[0].get("run"), str) else ""
    lines = normalize_script(run)
    proofs = [i for i, l in enumerate(lines) if l == SELECTOR_SELFTEST]
    reads = [i for i, l in enumerate(lines) if SELECTOR_READ in l]
    c.item(len(proofs) == 1 and bool(reads) and proofs[0] < min(reads), path,
           f"the decision step must run `{SELECTOR_SELFTEST}` exactly once "
           "and before it reads the selector's answer (self-test at "
           f"{proofs}, reads at {reads}): a selector trusted without its own "
           "proof decides whether this run validates anything")
    c.item(tuple(lines) == CANONICAL_DECIDE_SCRIPT, path,
           "the decision step script is not the canonical form: "
           + script_difference(lines, CANONICAL_DECIDE_SCRIPT)
           + "; this script publishes `run_full`, so a line changed here "
           "selects the no-op path with every pinned name and key still in "
           "place")


def check_no_gh_env(c, path, where, env):
    """No `GH_*` above the assert step. Its own env is pinned to exactly
    GH_TOKEN, but a job- or workflow-level `env: GH_HOST` reaches its `gh`
    without appearing in the step at all (#209, O11/O12)."""
    env = env if isinstance(env, dict) else {}
    named = sorted(str(k) for k in env if str(k).startswith(GH_ENV_PREFIX))
    c.item(not named, path, f"{where} `env` must name no `{GH_ENV_PREFIX}*` "
           f"variable (found {', '.join(named)}): it reaches the "
           "default-branch step's `gh` without appearing in that step, whose "
           f"own env is pinned to exactly {', '.join(ASSERT_STEP_ENV)}")


def shard_denominators(text):
    """Every denominator of a `--shard <i>/<n>` argument in one script."""
    out = []
    for arg in SHARD_ARG_RE.findall(text or ""):
        if "/" in arg:
            out.append(arg.rsplit("/", 1)[1].strip())
    return out


def resolve_denominator(token, env):
    """A denominator as written -> what it stands for. A `$NAME` is followed
    once through the step's own env, which is where a derived value enters a
    script; anything else stands for itself."""
    m = SHELL_VAR_RE.match(token or "")
    if m and isinstance(env, dict) and m.group(1) in env:
        return str(env[m.group(1)]).strip()
    return (token or "").strip()


def check_shard_denominator(c, path, jid, job):
    """A sharded worker carries one checked count through ``matrix.total``.

    GitHub's ``strategy.job-total`` is naturally derived, but act v0.2.89
    renders it as a negative value. A singleton matrix dimension is portable
    to both engines. It remains derived in substance because this check proves
    it equals the shard list's size and proves every consumer names it.
    """
    strat = job.get("strategy") if isinstance(job, dict) else None
    matrix = strat.get("matrix") if isinstance(strat, dict) else None
    shard = matrix.get("shard") if isinstance(matrix, dict) else None
    if not isinstance(shard, list) or not shard:
        return
    size = str(len(shard))
    expansions = [key for key in ("include", "exclude") if key in matrix]
    c.item(
        not expansions,
        path,
        f"job `{jid}` sharded matrix must not define `include` or `exclude` "
        f"(found {expansions or 'none'}): those keys change the produced job "
        "set without changing the checked shard-list denominator",
    )
    total = matrix.get("total")
    total_ok = (isinstance(total, list) and len(total) == 1
                and str(total[0]) == size)
    c.item(total_ok, path,
           f"job `{jid}` shard denominator matrix `total` must be a singleton "
           f"equal to the `strategy.matrix.shard` list size, {size} "
           f"(found {total!r}): GitHub and act workers must receive the same "
           "checked count")
    seen = []
    name = job.get("name")
    if isinstance(name, str):
        seen += [(f"job `{jid}` name", d, None)
                 for d in NAME_SHARD_RE.findall(name)]
    for n, step in enumerate(steps(job), 1):
        env = step.get("env") if isinstance(step.get("env"), dict) else {}
        run = step.get("run") if isinstance(step.get("run"), str) else ""
        seen += [(f"job `{jid}` step {n}", d, env)
                 for d in shard_denominators(run)]
    c.item(bool(seen), path, f"job `{jid}` carries a `strategy.matrix.shard` "
           "list and must pass `--shard <i>/<n>` to the tool it shards: a "
           "matrix nothing reads splits nothing")
    for where, token, env in seen:
        got = resolve_denominator(token, env)
        c.item(got == DERIVED_SHARD_TOTAL, path,
               f"{where}: the shard denominator `{token}` must be "
               f"`{DERIVED_SHARD_TOTAL}` (it resolves to `{got}`): a literal "
               "does not move when the matrix changes, while "
               "`strategy.job-total` is not portable to the supported act "
               "runner")


def matrix_size(wf, job):
    """The shard count of the worker job this aggregate needs: the length of
    that job's `strategy.matrix.shard` list, derived, not restated."""
    needs = job.get("needs")
    needs = needs if isinstance(needs, list) else [needs]
    for n in needs:
        worker = jobs(wf).get(n) if isinstance(n, str) else None
        strat = worker.get("strategy") if isinstance(worker, dict) else None
        matrix = strat.get("matrix") if isinstance(strat, dict) else None
        shard = matrix.get("shard") if isinstance(matrix, dict) else None
        if isinstance(shard, list) and shard:
            return len(shard)
    return None


def canonical_verify_script(wf, job):
    """The verifier step's script, derived from the job's own download step
    (where the shards land, what they are called) and the worker matrix
    (how many there are). None when the job has no usable download step."""
    dl = next((s for s in steps(job) if uses(s, "actions/download-artifact")),
              None)
    with_ = dl.get("with") if isinstance(dl, dict) and isinstance(
        dl.get("with"), dict) else {}
    pattern, dest = with_.get("pattern"), with_.get("path")
    n = matrix_size(wf, job)
    if (not isinstance(pattern, str) or not isinstance(dest, str)
            or not dest.startswith(RUNNER_TEMP_PREFIX) or n is None):
        return None
    base = dest[len(RUNNER_TEMP_PREFIX):].strip("/")
    return (
        "shopt -s nullglob",
        f'roots=("$RUNNER_TEMP"/{base}/{pattern})',
        f"python3 scripts/ci_events.py {VERIFY_FLAG} --expect {n} "
        + " ".join(REQUIRED_SHA_ARGS[l] for l in REQUIRED_SHA_LABELS)
        + ' -- "${roots[@]}"',
    )


def check_verify_step(c, path, wf, jid, job, step):
    """The aggregate's verifier step: pinned keys, the one permitted `if`,
    env exactly GATE_SHA, and a script equal to the derived canonical form
    (so `--expect` is the worker matrix size and no line can reassign a
    source before the call)."""
    what = f"job `{jid}` verifier step"
    pinned_step_keys(c, path, what, step, VERIFY_STEP_KEYS, VERIFY_STEP_ENV)
    got_if = str(step.get("if", "")).strip()
    c.item(got_if == VERIFY_STEP_IF, path, f"{what} `if` must be exactly "
           f"`{VERIFY_STEP_IF}` (found `{got_if}`): any other condition can "
           "skip the verification, and a skipped step passes the job")
    run = step.get("run") if isinstance(step.get("run"), str) else ""
    lines = normalize_script(run)
    canon = canonical_verify_script(wf, job)
    c.item(canon is not None, path, f"{what}: the download step must name a "
           f"`pattern` and a `path` under `{RUNNER_TEMP_PREFIX}`, and the "
           "aggregate must need a worker with a `strategy.matrix.shard` list")
    if canon is None:
        return
    script = " ".join(lines)
    m = EXPECT_RE.search(script)
    want_n = canon[2].split("--expect ")[1].split()[0]
    c.item(m is not None and m.group(1) == want_n, path, f"{what} must pass "
           f"--expect {want_n}, the worker matrix size "
           f"(found {m.group(1) if m else 'no --expect'})")
    c.item(tuple(lines) == canon, path, f"{what} script is not the canonical "
           f"form derived from its download step and worker matrix: expected "
           f"exactly {list(canon)} (found {lines})")


def check_sha_sources(c, path, jid, step):
    """An aggregate passes exactly the three SHA sources, each in the form
    that binds it to what it claims: the gate's exported target through the
    step env, the aggregate's own GITHUB_SHA, and its checkout HEAD."""
    run = step.get("run") if isinstance(step.get("run"), str) else ""
    script = " ".join(normalize_script(run))
    labels = SHA_LABEL_RE.findall(script)
    missing = [l for l in REQUIRED_SHA_LABELS if l not in labels]
    unknown = sorted(set(labels) - set(REQUIRED_SHA_LABELS))
    dup = sorted({l for l in labels if labels.count(l) > 1})
    c.item(not missing and not unknown and not dup, path,
           f"job `{jid}` must pass --sha for exactly "
           f"{', '.join(REQUIRED_SHA_LABELS)}"
           + (f"; missing: {', '.join(missing)}" if missing else "")
           + (f"; unknown: {', '.join(unknown)}" if unknown else "")
           + (f"; repeated: {', '.join(dup)}" if dup else ""))
    for label, want in REQUIRED_SHA_ARGS.items():
        c.item(want in script, path, f"job `{jid}` must pass {want} "
               f"(the {label} source in its binding form)")
    # GATE_SHA's own binding is held by VERIFY_STEP_ENV through
    # pinned_step_keys, with every other pinned step's env.


def normalize_script(run):
    """Whitespace-normalized lines of a step script: continuation lines
    joined, runs of blanks collapsed, blank lines dropped. Comment lines stay,
    because a comment is not canonical either."""
    joined = re.sub(r"\\\n", " ", run or "")
    lines = []
    for raw in joined.splitlines():
        line = " ".join(raw.split())
        if line:
            lines.append(line)
    return lines


def check_default_branch_step(c, path, gate):
    """The gate reads the repository default branch live and hands it to
    --require-default-branch, in a shape that cannot be neutered quietly."""
    found = [s for s in steps(gate) if DEFAULT_BRANCH_FLAG in step_text(s)]
    c.item(len(found) == 1, path, f"job `{GATE_JOB}` must run scripts/"
           f"ci_events.py {DEFAULT_BRANCH_FLAG} in exactly one step "
           f"(found {len(found)})")
    if len(found) != 1:
        return
    step = found[0]
    text = step_text(step)
    # Its keys, its env names and the expression each name is bound to are
    # pinned in check_gate_steps beside its siblings': the same key on any
    # step of this job has the same effect, and ASSERT_STEP_ENV is the one
    # place that says GH_TOKEN must be `${{ github.token }}`.
    run = step.get("run") if isinstance(step.get("run"), str) else ""
    lines = normalize_script(run)
    code = [(i, l) for i, l in enumerate(lines) if not l.startswith("#")]
    # Structural reasons first, so a refusal names what went wrong.
    assigns = [(i, l) for i, l in code if OBSERVED_ASSIGNMENT.search(l)]
    c.item(len(assigns) == 1, path, "the default-branch step must assign "
           f"`observed` exactly once (found {len(assigns)}): a second "
           "assignment shadows the live value")
    c.item(bool(assigns) and all(l == CANONICAL_OBSERVED for _, l in assigns),
           path, "the default-branch step's observed value is not sourced "
           f"from the live API call: expected exactly {CANONICAL_OBSERVED} "
           f"(found {[l for _, l in assigns] or 'no assignment'})")
    flow = [l for _, l in code if CONTROL_FLOW.search(l)]
    c.item(not flow, path, "the default-branch step must read the setting "
           f"unconditionally: control flow found ({flow})")
    comments = [l for l in lines if l.startswith("#")]
    c.item(not comments, path, "the default-branch step script carries no "
           "comment lines (a `gh api` in a comment reads nothing; comments "
           f"belong above the step): {comments}")
    calls = [(i, l) for i, l in code if DEFAULT_BRANCH_FLAG in l]
    c.item(len(calls) == 1 and calls[0][1] == CANONICAL_CALL, path,
           "the default-branch step must call the verifier exactly as "
           f"`{CANONICAL_CALL}` (found {[l for _, l in calls]})")
    c.item(bool(assigns) and bool(calls) and calls[-1][0] > assigns[0][0],
           path, "the verifier call must follow the live read")
    c.item(tuple(lines) == CANONICAL_DEFAULT_BRANCH_SCRIPT, path,
           "the default-branch step script is not the canonical form: "
           f"expected exactly {list(CANONICAL_DEFAULT_BRANCH_SCRIPT)} "
           f"(found {lines})")
    neutered = bool(step.get("continue-on-error")) or "|| true" in text
    c.item(not neutered, path, "the default-branch step must fail closed: "
           "no continue-on-error, no `|| true`")


def check_fast_selector(c, wf):
    """Hold the fast workflow's complete checkout -> scope decision.

    `rtl-fast` accepts skipped RTL consumers for docs-only changes. Therefore
    an `if: false` on this job or its scope step, a shallow/moved checkout, or
    a scope body that publishes `rtl=false` is a false green unless the whole
    producer is part of the contract.
    """
    selector = jobs(wf).get(FAST_SELECTOR_JOB)
    c.item(isinstance(selector, dict), RTL_FAST,
           f"job `{FAST_SELECTOR_JOB}` must exist as the fast RTL selector")
    if not isinstance(selector, dict):
        return

    check_job_keys(c, RTL_FAST, FAST_SELECTOR_JOB, selector)
    c.item("env" not in selector, RTL_FAST,
           f"job `{FAST_SELECTOR_JOB}` must carry no `env` (found "
           f"{sorted(map(str, selector.get('env') or {}))}): a job-level "
           "value reaches the scope script without appearing in the pinned "
           "step, whose own env is the selector's whole input contract")
    c.item("defaults" not in wf, RTL_FAST,
           "the fast workflow must carry no top-level `defaults` "
           f"(found {wf.get('defaults')!r}): a `defaults.run.shell` changes "
           "how the selector script runs")

    raw_steps = selector.get("steps")
    ss = raw_steps if isinstance(raw_steps, list) else []
    mappings = [s for s in ss if isinstance(s, dict)]
    c.item(len(ss) == 2 and len(mappings) == 2, RTL_FAST,
           f"job `{FAST_SELECTOR_JOB}` must carry exactly two mapping steps, "
           "checkout then scope, in that order (found "
           f"{len(ss)} step(s), {len(mappings)} mapping(s)): an inserted or "
           "removed step changes whether and how the selector runs")

    checkouts = [s for s in mappings if _is_checkout_step(s)]
    scopes = [s for s in mappings if s.get("id") == FAST_SCOPE_STEP_ID]
    checkout = checkouts[0] if len(checkouts) == 1 else None
    scope = scopes[0] if len(scopes) == 1 else None
    c.item(len(checkouts) == 1 and len(scopes) == 1
           and len(ss) == 2 and ss[0] is checkout and ss[1] is scope,
           RTL_FAST, f"job `{FAST_SELECTOR_JOB}` steps must be exactly "
           f"`{FAST_CHECKOUT_USES}` then the step with "
           f"`id: {FAST_SCOPE_STEP_ID}` (found "
           f"{[step_label(s) for s in mappings]}): scope must inspect the "
           "tree the checkout brought")

    if checkout is not None:
        pinned_step_keys(c, RTL_FAST, "the fast selector checkout step",
                         checkout, CHECKOUT_STEP_KEYS, {},
                         CHECKOUT_STEP_OPTIONAL)
        got_uses = str(checkout.get("uses", "")).strip()
        c.item(got_uses == FAST_CHECKOUT_USES, RTL_FAST,
               "the fast selector checkout step must use exactly "
               f"`{FAST_CHECKOUT_USES}` (found `{got_uses}`)")
        with_ = checkout.get("with")
        with_ = with_ if isinstance(with_, dict) else {}
        pinned_bindings(c, RTL_FAST, "the fast selector checkout `with`",
                        with_, FAST_CHECKOUT_WITH,
                        "the scope step diffs against an earlier commit, so "
                        "the checkout must carry full history")

    if scope is not None:
        pinned_step_keys(c, RTL_FAST, "the fast selector scope step", scope,
                         FAST_SCOPE_STEP_KEYS, FAST_SCOPE_STEP_ENV)
        run = scope.get("run") if isinstance(scope.get("run"), str) else ""
        lines = normalize_script(run)
        proofs = [i for i, line in enumerate(lines)
                  if line == SELECTOR_SELFTEST]
        reads = [i for i, line in enumerate(lines) if SELECTOR_READ in line]
        c.item(len(proofs) == 1 and bool(reads)
               and proofs[0] < min(reads), RTL_FAST,
               f"the fast selector scope step must run `{SELECTOR_SELFTEST}` "
               "exactly once and before it reads the selector's answer "
               f"(self-test at {proofs}, reads at {reads})")
        c.item(tuple(lines) == CANONICAL_FAST_SCOPE_SCRIPT, RTL_FAST,
               "the fast selector scope script is not the canonical form: "
               + script_difference(lines, CANONICAL_FAST_SCOPE_SCRIPT)
               + "; this script publishes `rtl`, so an empty or false value "
               "skips both RTL consumers into the aggregate's accepted "
               "docs-only path")


def check_fast_aggregate(c, wf):
    """Hold the verdict half of the fast lane ([R2] on PR #239).

    The fast aggregate runs under `always() && !cancelled()`, so once its job
    keys are canonical the ONLY thing standing between a failed consumer and
    a green required context is its verdict step. An `if` on that step skips
    it and the job succeeds with `verilator-lint` FAILED; a result binding
    rebound to the literal `success` converts one named failure into a pass;
    a `case` widened to `success|skipped|failure` accepts them all. None of
    those touches a job key or the selector's publication path. So the
    verdict step is held the way the exhaustive workflow's verifier steps
    are: pinned keys, env derived from the aggregate's `needs`, script
    derived from the same list. The `needs` list itself must name every
    other job of the workflow, so no fast job can fail outside the required
    context's view and none can be quietly dropped from it."""
    all_jobs = jobs(wf)
    public = set(PUBLIC_NAMES.get(RTL_FAST, ()))
    for jid, job in all_jobs.items():
        if display_name(jid, job) not in public:
            continue
        needed = needs_list(job)
        others = [j for j in all_jobs if j != jid]
        missing = [j for j in others if j not in needed]
        surplus = [j for j in needed if j not in others]
        c.item(not missing and not surplus, RTL_FAST,
               f"job `{jid}` must need every other job of this workflow, "
               f"{', '.join(others)}"
               + (f"; missing: {', '.join(missing)}" if missing else "")
               + (f"; surplus: {', '.join(surplus)}" if surplus else "")
               + ": a fast job outside the aggregate's `needs` can fail "
               "with the required context still green, and a dropped entry "
               "silently removes that job's result from the verdict")
        ss = steps(job)
        c.item(len(ss) == 1, RTL_FAST,
               f"job `{jid}` must carry exactly one step, its verdict step "
               f"(found {len(ss)}): a step inserted beside the verdict can "
               "change what it reads, and a removed one takes the verdict "
               "with it")
        if len(ss) != 1:
            continue
        what = f"job `{jid}` verdict step"
        env_want = {fast_result_env_name(j): needs_result_ref(j)
                    for j in needed}
        pinned_step_keys(c, RTL_FAST, what, ss[0], FAST_VERDICT_STEP_KEYS,
                         env_want)
        run = ss[0].get("run") if isinstance(ss[0].get("run"), str) else ""
        lines = normalize_script(run)
        canon = canonical_fast_verdict_script(needed)
        c.item(tuple(lines) == canon, RTL_FAST,
               f"{what} script is not the canonical form derived from the "
               "aggregate's `needs`: "
               + script_difference(lines, canon)
               + "; this script is the whole required fast verdict, so a "
               "widened `case` or a dropped pair turns a named failure into "
               "a pass")


def check_fast_ooc_sh_selftest(c, wf):
    """#245: the ooc.sh refusal self-test stays wired, verbatim, in order."""
    path = RTL_FAST
    job = jobs(wf).get(OOC_SH_SELFTEST_JOB)
    c.item(job is not None, path,
           f"job `{OOC_SH_SELFTEST_JOB}` must exist (it fetches the "
           "submodule the ooc.sh refusal self-test reads)")
    if job is None:
        return
    slist = steps(job)
    hits = [i for i, s in enumerate(slist)
            if isinstance(s.get("run"), str)
            and tuple(normalize_script(s["run"])) == (OOC_SH_SELFTEST,)]
    c.item(len(hits) == 1, path,
           f"exactly one step must run `{OOC_SH_SELFTEST}` verbatim in "
           f"`{OOC_SH_SELFTEST_JOB}` (found {len(hits)}): it is the only "
           "hosted exercise of ooc.sh's refusals, and a neutralised or "
           "wrapped spelling is a different script")
    if len(hits) != 1:
        return
    # The step's KEYS are pinned too, exactly as the fast-verdict step's
    # are: `if:`, `continue-on-error:` and `shell:` each leave the pinned
    # run text byte-identical while disabling or reinterpreting its
    # execution ([R0] round two on PR #262) - a skipped or reinterpreted
    # self-test is the same false green as a deleted one.
    extra = sorted(set(slist[hits[0]].keys()) - {"name", "run"})
    c.item(not extra, path,
           f"the `{OOC_SH_SELFTEST}` step carries key(s) {extra} beyond "
           "name/run: any other key can disable or reinterpret the pinned "
           "invocation while its text stays pinned")
    fetch = [i for i, s in enumerate(slist)
             if OOC_SH_SUBMODULE_FETCH in step_text(s)
             and all(name in step_text(s) for name in OOC_SH_SUBMODULES)]
    c.item(bool(fetch) and fetch[0] < hits[0], path,
           f"`{OOC_SH_SELFTEST}` must run after a `{OOC_SH_SUBMODULE_FETCH}` "
           f"step that names {OOC_SH_SUBMODULES!r} (it reads the trees that "
           "step initialises; before it - or without it - every arm dies on "
           "setup, proving nothing)")


def check_rtl_fast(c, wf):
    check_push_and_pr(c, RTL_FAST, wf, exact_types=True)
    check_cancel_in_progress(c, RTL_FAST, wf)
    check_public_names(c, RTL_FAST, wf)
    check_fast_selector(c, wf)
    check_fast_aggregate(c, wf)
    check_fast_ooc_sh_selftest(c, wf)
    # The same selector -> outputs -> consumer path as the exhaustive
    # workflow, and the same false green if it is left unheld: this
    # aggregate counts a skipped consumer as a pass.
    check_publication_path(c, RTL_FAST, wf)


def check_builder_dependencies(c, path, wf, jid):
    """The hosted builder call is preceded by one complete, live checkout.

    ``actions/checkout`` leaves submodules absent.  The builder reads both
    processor trees and asks ``dp_srcs.py`` to resolve the verilog-axis
    leaves, so a partial checkout is a setup failure rather than evidence
    about the candidate.  Pin the setup as one command, before the call and
    under the same step condition, so a decoy or late checkout cannot satisfy
    the text recogniser.
    """
    c.item("defaults" not in wf, path,
           "the builder workflow must carry no top-level `defaults` "
           f"(found {wf.get('defaults')!r}): a `defaults.run.shell` changes "
           "how every builder command runs")
    job = jobs(wf).get(jid)
    c.item(isinstance(job, dict), path,
           f"builder job `{jid}` must exist")
    if not isinstance(job, dict):
        return
    check_job_keys(c, path, jid, job)
    ss = steps(job)
    checkouts = [(i, s) for i, s in enumerate(ss)
                 if uses(s, "actions/checkout")]
    c.item(len(checkouts) == 1, path,
           f"job `{jid}` must carry exactly one actions/checkout step "
           f"(found {len(checkouts)})")
    if len(checkouts) == 1:
        _, checkout = checkouts[0]
        c.item(checkout == BUILDER_CHECKOUTS[path], path,
               f"job `{jid}` checkout step must be exactly "
               f"{BUILDER_CHECKOUTS[path]!r} (found {checkout!r})")
    callers = [(i, s) for i, s in enumerate(ss)
               if BUILDER_CALL in (s.get("run")
                                   if isinstance(s.get("run"), str) else "")]
    c.item(len(callers) == 1, path,
           f"job `{jid}` must call `{BUILDER_CALL}` exactly once "
           f"(found {len(callers)})")
    fetchers = [(i, s) for i, s in enumerate(ss)
                if "git submodule update --init" in step_text(s)]
    c.item(len(fetchers) == 1, path,
           f"job `{jid}` must carry exactly one builder submodule checkout "
           f"(found {len(fetchers)})")
    if len(fetchers) != 1:
        return
    fetch_i, fetch = fetchers[0]
    run = fetch.get("run") if isinstance(fetch.get("run"), str) else ""
    for submodule in BUILDER_SUBMODULES:
        c.item(submodule in run, path,
               f"job `{jid}` builder checkout must initialize `{submodule}`")
    c.item(tuple(normalize_script(run)) == (BUILDER_COMMAND,), path,
           f"job `{jid}` builder checkout must be exactly `{BUILDER_COMMAND}` "
           f"(found {normalize_script(run)})")
    keys = (("name", "if", "run") if path == ELABORATE
            else ("name", "run"))
    pinned_step_keys(c, path, f"job `{jid}` builder checkout", fetch,
                     keys, {})
    installers = [(i, s) for i, s in enumerate(ss)
                  if "sv2v" in (s.get("run")
                                if isinstance(s.get("run"), str) else "")]
    c.item(len(installers) == 1, path,
           f"job `{jid}` must install the pinned sv2v front end exactly once "
           f"(found {len(installers)}): dp_srcs.py refuses without a front "
           "end, so the builder gate is red on a bare runner, and a second "
           "install could shadow the pin")
    if len(installers) == 1:
        sv2v_i, sv2v_step = installers[0]
        sv2v_run = (sv2v_step.get("run")
                    if isinstance(sv2v_step.get("run"), str) else "")
        c.item(tuple(normalize_script(sv2v_run)) == SV2V_INSTALL, path,
               f"job `{jid}` sv2v install must be exactly the pinned v0.0.12 "
               f"release script (found {normalize_script(sv2v_run)}): an "
               "unpinned front end is a silent toolchain drift under the "
               "portability evidence")
        pinned_step_keys(c, path, f"job `{jid}` sv2v install", sv2v_step,
                         keys, {})
        if path == ELABORATE:
            sv2v_if = str(sv2v_step.get("if", "")).strip()
            c.item(sv2v_if == BUILDER_IF, path,
                   f"job `{jid}` sv2v install `if` must be exactly "
                   f"`{BUILDER_IF}` (found {sv2v_if!r})")
    if len(callers) == 1:
        call_i, call = callers[0]
        call_run = call.get("run") if isinstance(call.get("run"), str) else ""
        c.item(tuple(normalize_script(call_run)) == BUILDER_RUNS[path], path,
               f"job `{jid}` builder call must be exactly "
               f"{list(BUILDER_RUNS[path])} "
               f"(found {normalize_script(call_run)})")
        pinned_step_keys(c, path, f"job `{jid}` builder call", call,
                         keys, {})
        if path == ELABORATE:
            fetch_if = str(fetch.get("if", "")).strip()
            call_if = str(call.get("if", "")).strip()
            c.item(fetch_if == BUILDER_IF, path,
                   f"job `{jid}` builder checkout `if` must be exactly "
                   f"`{BUILDER_IF}` (found {fetch_if!r})")
            c.item(call_if == BUILDER_IF, path,
                   f"job `{jid}` builder call `if` must be exactly "
                   f"`{BUILDER_IF}` (found {call_if!r})")
        if len(checkouts) == 1:
            checkout_i, _ = checkouts[0]
            c.item(checkout_i < fetch_i, path,
                   f"job `{jid}` must check out the repository before "
                   "initializing builder submodules")
        c.item(fetch_i < call_i, path,
               f"job `{jid}` must initialize builder submodules before "
               f"calling `{BUILDER_CALL}`")
        if len(installers) == 1:
            c.item(installers[0][0] < call_i, path,
                   f"job `{jid}` must install sv2v before calling "
                   f"`{BUILDER_CALL}`: installed after the call it decorates "
                   "a verdict already taken without a front end")


def check_docs(c, wf):
    check_push_and_pr(c, DOCS, wf, exact_types=False)
    check_public_names(c, DOCS, wf)
    check_required_context_carriers(c, DOCS, wf, held_by_builder=("docs-check",))
    check_builder_dependencies(c, DOCS, wf, "docs-check")
    texts = [step_text(s) for j in jobs(wf).values() for s in steps(j)]
    for flag in ("--check", "--selftest"):
        wired = any(f"scripts/ci_events.py {flag}" in t for t in texts)
        c.item(wired, DOCS, f"must run `python3 scripts/ci_events.py {flag}` "
               "(this gate is not a gate unless a workflow runs it)")
    docs_job = jobs(wf).get("docs-check")
    act_selftests = [s for s in steps(docs_job)
                     if tuple(normalize_script(
                         s.get("run") if isinstance(s.get("run"), str) else ""
                     )) == (ACT_CI_SELFTEST,)]
    c.item(len(act_selftests) == 1, DOCS,
           f"job `docs-check` must run `{ACT_CI_SELFTEST}` exactly once "
           f"(found {len(act_selftests)}): the runner's refusal and cleanup "
           "controls are not a hosted gate unless the required docs context "
           "executes their negative controls")
    if len(act_selftests) == 1:
        pinned_step_keys(c, DOCS, "local act runner contract step",
                         act_selftests[0], ("name", "run"), {})


def check_elaborate(c, wf):
    check_push_and_pr(c, ELABORATE, wf, exact_types=False)
    check_public_names(c, ELABORATE, wf)
    check_required_context_carriers(c, ELABORATE, wf,
                                    held_by_builder=("elaborate",))
    check_builder_dependencies(c, ELABORATE, wf, "elaborate")


def check(parsed):
    """The whole contract over a parsed world. Returns a Contract."""
    c = Contract()
    check_rtl_full(c, parsed[RTL_FULL], parsed[POLICY])
    check_rtl_fast(c, parsed[RTL_FAST])
    check_docs(c, parsed[DOCS])
    check_elaborate(c, parsed[ELABORATE])
    return c


# --------------------------------------------------------------------------
# --require-target-sha: the aggregate-side verifier
# --------------------------------------------------------------------------

def check_records(shas, roots, expect):
    """`shas` maps a label (gate, run, checkout) to the SHA that source
    reports; `roots` are the downloaded shard directories; `expect` is the
    worker matrix size, which the root count must equal. Returns
    (findings, lines): every finding is a refusal, lines are the verdict."""
    if not isinstance(expect, int) or expect < 1:
        raise CannotRun("--expect <n> is required: the number of shard "
                        "directories the worker matrix produces")
    findings, lines = [], []
    if len(roots) != expect:
        findings.append(f"expected {expect} shard director(y/ies), the worker "
                        f"matrix size, found {len(roots)}: a missing or "
                        "surplus shard is a failure, not a skip")
    missing = [l for l in REQUIRED_SHA_LABELS if l not in shas]
    unknown = sorted(set(shas) - set(REQUIRED_SHA_LABELS))
    if missing or unknown:
        findings.append("the SHA sources must be exactly "
                        f"{', '.join(REQUIRED_SHA_LABELS)}"
                        + (f"; missing: {', '.join(missing)}" if missing else "")
                        + (f"; unknown: {', '.join(unknown)}" if unknown else "")
                        + ": an aggregate that drops a source cannot prove "
                        "the gate, the run and its checkout agree")
    for label, sha in shas.items():
        if not SHA_RE.match(sha or ""):
            findings.append(f"{label} SHA {sha!r} is not a 40-digit lowercase "
                            "hexadecimal commit id")
    distinct = sorted(set(shas.values()))
    if len(distinct) != 1:
        findings.append("the sources disagree on which tree this run "
                        "validates: " + ", ".join(f"{k}={v}" for k, v in
                                                  sorted(shas.items())))
    expected = distinct[0] if len(distinct) == 1 else None
    if not roots:
        findings.append("no shard evidence directory to verify: the download "
                        "produced nothing, which is a failure, not a skip")
    for root in roots:
        record = pathlib.Path(root) / RECORD
        name = pathlib.Path(root).name
        if not record.is_file():
            findings.append(f"{name}: {RECORD} missing, the worker did not "
                            "record the tree it validated")
            continue
        try:
            got = record.read_text(encoding="utf-8").strip()
        except (OSError, UnicodeDecodeError) as exc:
            findings.append(f"{name}: {RECORD} unreadable: {exc}")
            continue
        if not SHA_RE.match(got):
            findings.append(f"{name}: {RECORD} holds {got!r}, not a commit id")
        elif expected is not None and got != expected:
            findings.append(f"{name}: validated {got}, this run is {expected}")
        else:
            lines.append(f"  ok   {name}  {got}")
    if findings:
        lines.append(f"target-sha: {len(findings)} finding(s); refusing this "
                     "evidence")
    else:
        lines.append(f"target-sha: OK, {len(roots)} record(s) all {expected}")
    return findings, lines


# --------------------------------------------------------------------------
# --require-default-branch: the live repository-setting assertion
# --------------------------------------------------------------------------

def check_default_branch(event, observed):
    """(findings, lines) for one run's view of the repository default branch.

    `event` is GITHUB_EVENT_NAME, `observed` what `gh api` returned (or the
    placeholder the gate substitutes when it could not read it). The events
    in DEFAULT_BRANCH_EVENTS refuse anything but PUSH_BRANCH, an unreadable
    value included; every other event prints and continues."""
    if not event:
        raise CannotRun("--event is required: the decision depends on it")
    observed = (observed or "").strip()
    governed = event in DEFAULT_BRANCH_EVENTS
    shown = observed or "<empty>"
    lines = [f"default_branch={shown} expected={PUSH_BRANCH} event={event} "
             f"({'governed' if governed else 'informational'})"]
    if observed == PUSH_BRANCH:
        lines.append("default-branch: OK")
        return [], lines
    if governed:
        return [f"the repository default branch is {shown!r}, not "
                f"{PUSH_BRANCH!r}: a {event} run would validate the wrong "
                "branch; refusing"], lines
    lines.append(f"default-branch: WARNING, {shown!r} is not {PUSH_BRANCH!r}; "
                 f"this {event} run continues, the next scheduled or "
                 "dispatched run will refuse")
    return [], lines


# --------------------------------------------------------------------------
# Self-test
# --------------------------------------------------------------------------

def _mutations():
    """(name, path-or-None, mutate(parsed_world), expected finding fragment).

    Every arm alters ONE contract item on a deep copy of the pristine parsed
    world and names the fragment the finding must carry. Arms that touch the
    policy page mutate its text and assert the text actually changed, so an
    arm cannot pass because its edit found nothing to edit."""

    def on(w, path):
        return triggers(w[path])

    def policy_replace(w, old, new):
        assert old in w[POLICY], f"fixture drift: {old!r} not on the page"
        w[POLICY] = w[POLICY].replace(old, new)

    def first_checkout(w, path=RTL_FULL):
        for job in jobs(w[path]).values():
            for s in steps(job):
                if uses(s, "actions/checkout"):
                    return s
        raise AssertionError("fixture drift: no checkout step")

    def job_steps(w, path, jid):
        return jobs(w[path])[jid]["steps"]

    def strip_steps(w, path, jid, needle):
        ss = job_steps(w, path, jid)
        kept = [s for s in ss if needle not in step_text(s)]
        assert len(kept) < len(ss), f"fixture drift: no step mentions {needle}"
        jobs(w[path])[jid]["steps"] = kept

    def m_push_main(path):
        def f(w):
            on(w, path)["push"]["branches"] = ["main"]
        return f

    def m_drop_pr(path):
        def f(w):
            del on(w, path)["pull_request"]
        return f

    def m_pr_type_missing(path):
        def f(w):
            on(w, path)["pull_request"]["types"].remove("converted_to_draft")
        return f

    def m_pr_type_extra(path):
        def f(w):
            on(w, path)["pull_request"]["types"].append("labeled")
        return f

    def m_cancel_false(path):
        def f(w):
            w[path]["concurrency"]["cancel-in-progress"] = False
        return f

    def m_no_concurrency(path):
        def f(w):
            del w[path]["concurrency"]
        return f

    def m_rename_job(path, jid):
        def f(w):
            jobs(w[path])[jid]["name"] = jid + "-renamed"
        return f

    def m_job_key(path, jid, key, value):
        # A neuter key on the JOB, not on one of its steps (#261): the step
        # arms leave the job's own run conditions untouched.
        def f(w):
            jobs(w[path])[jid][key] = value
        return f

    def m_second_carrier(path, name):
        # A second job publishing a required check name, so which run the
        # ruleset binds is ambiguous ([R2] on PR #239, widened by #261).
        def f(w):
            jobs(w[path])["decoy"] = {"name": name, "runs-on": "ubuntu-latest",
                                      "steps": [{"run": "true"}]}
        return f

    def m_expression_carrier(path, name):
        # The decoy's `name` is an EXPRESSION that evaluates to the required
        # name on the runner ([R4] on PR #293); the real job is untouched.
        def f(w):
            jobs(w[path])["decoy"] = {"name": "${{ '" + name + "' }}",
                                      "runs-on": "ubuntu-latest",
                                      "steps": [{"run": "true"}]}
        return f

    def m_matrix_carrier(path, name):
        # A matrix job whose `name` RENDERS the required name from its own
        # matrix list ([R4] on PR #293): the expression is the allowed
        # `matrix.<key>` form, so only enumeration can see the collision.
        def f(w):
            jobs(w[path])["decoy"] = {"name": "${{ matrix.n }}",
                                      "runs-on": "ubuntu-latest",
                                      "strategy": {"matrix": {"n": [name]}},
                                      "steps": [{"run": "true"}]}
        return f

    def m_swap_carrier(path, jid):
        # The real job renamed away and a `run: true` stub given the required
        # name ([R3] on PR #293): the unique carrier has no neuter key, the
        # id-named job keeps every pinned step, and the context runs nothing.
        def f(w):
            jobs(w[path])[jid]["name"] = jid + "-real"
            jobs(w[path])["decoy"] = {"name": jid, "runs-on": "ubuntu-latest",
                                      "steps": [{"run": "true"}]}
        return f

    def m_drop_dispatch(w):
        del on(w, RTL_FULL)["workflow_dispatch"]

    def m_dispatch_inputs(w):
        on(w, RTL_FULL)["workflow_dispatch"] = {
            "inputs": {"ref": {"type": "string", "required": True}}}

    def m_drop_schedule(w):
        del on(w, RTL_FULL)["schedule"]

    def m_two_crons(w):
        on(w, RTL_FULL)["schedule"].append({"cron": "17 13 * * *"})

    def m_cron_moved(w):
        on(w, RTL_FULL)["schedule"][0]["cron"] = "17 2 * * *"

    def m_cron_shape(w):
        on(w, RTL_FULL)["schedule"][0]["cron"] = "*/15 * * * *"

    def m_page_time(w):
        policy_replace(w, "01:17 UTC", "02:17 UTC")

    def m_page_cron(w):
        policy_replace(w, "`17 1 * * *`", "`17 1 * * 1-5`")

    def m_checkout_ref(w):
        first_checkout(w)["with"] = {"ref": "dev"}

    def m_checkout_ref_deep(w):
        s = first_checkout(w)
        s.setdefault("with", {})["ref"] = "${{ github.event.pull_request.head.sha }}"

    def m_drop_gate_output(w):
        del jobs(w[RTL_FULL])[GATE_JOB]["outputs"][GATE_OUTPUT]

    def m_gate_silent(w):
        strip_steps(w, RTL_FULL, GATE_JOB, "GITHUB_EVENT_NAME")

    def m_worker_no_record(w):
        strip_steps(w, RTL_FULL, "verilator-shards", RECORD)

    def m_yosys_no_record(w):
        strip_steps(w, RTL_FULL, "yosys-shards", RECORD)

    def m_record_after_upload(w):
        ss = job_steps(w, RTL_FULL, "verilator-shards")
        rec = next(i for i, s in enumerate(ss) if RECORD in step_text(s))
        ss.append(ss.pop(rec))

    def m_aggregate_no_verify(w):
        strip_steps(w, RTL_FULL, "verilator-suites", VERIFY_FLAG)

    def m_yosys_aggregate_no_verify(w):
        strip_steps(w, RTL_FULL, "yosys-portability", VERIFY_FLAG)

    def m_aggregate_without_gate(w):
        job = jobs(w[RTL_FULL])["verilator-suites"]
        job["needs"] = [n for n in job["needs"] if n != GATE_JOB]

    def m_artifact_aggregates_race(w):
        job = jobs(w[RTL_FULL])["yosys-portability"]
        assert "verilator-suites" in job["needs"], (
            "fixture drift: artifact aggregates are not ordered")
        job["needs"] = [n for n in job["needs"]
                        if n != "verilator-suites"]

    def db_step(w):
        for s in steps(jobs(w[RTL_FULL])[GATE_JOB]):
            if DEFAULT_BRANCH_FLAG in step_text(s):
                return s
        raise AssertionError("fixture drift: no default-branch step")

    def m_db_step_removed(w):
        strip_steps(w, RTL_FULL, GATE_JOB, DEFAULT_BRANCH_FLAG)

    def m_db_token_missing(w):
        del db_step(w)["env"]["GH_TOKEN"]

    def m_db_no_live_read(w):
        s = db_step(w)
        assert "gh api" in s["run"]
        s["run"] = s["run"].replace("gh api", "echo")

    def m_db_event_not_passed(w):
        s = db_step(w)
        assert '--event "$GITHUB_EVENT_NAME"' in s["run"]
        s["run"] = s["run"].replace('--event "$GITHUB_EVENT_NAME"',
                                    "--event push")

    def m_db_continue_on_error(w):
        db_step(w)["continue-on-error"] = True

    def m_db_or_true(w):
        s = db_step(w)
        s["run"] = s["run"].rstrip("\n") + " || true\n"

    def set_db_script(w, *lines):
        db_step(w)["run"] = "\n".join(lines) + "\n"

    def m_db_decoy_if_false(w):
        # The reviewer's decoy: a literal beside an unreachable live read.
        set_db_script(w, "set -euo pipefail", "observed=dev", "if false; then",
                      "  " + CANONICAL_OBSERVED, "fi", CANONICAL_CALL)

    def m_db_literal_after_call(w):
        set_db_script(w, *CANONICAL_DEFAULT_BRANCH_SCRIPT, "observed=dev")

    def m_db_literal_after_read(w):
        set_db_script(w, "set -euo pipefail", CANONICAL_OBSERVED,
                      "observed=dev", CANONICAL_CALL)

    def m_db_gh_api_in_comment(w):
        set_db_script(w, "set -euo pipefail", "# " + CANONICAL_OBSERVED,
                      "observed=dev", CANONICAL_CALL)

    def m_db_other_command(w):
        set_db_script(w, "set -euo pipefail",
                      'observed="$(git symbolic-ref --short '
                      'refs/remotes/origin/HEAD | sed s,origin/,,)"',
                      CANONICAL_CALL)

    def m_db_two_assignments(w):
        set_db_script(w, "set -euo pipefail", CANONICAL_OBSERVED,
                      CANONICAL_OBSERVED, CANONICAL_CALL)

    def m_db_call_before_read(w):
        set_db_script(w, "set -euo pipefail", CANONICAL_CALL,
                      CANONICAL_OBSERVED)

    def m_db_extra_line(w):
        set_db_script(w, *CANONICAL_DEFAULT_BRANCH_SCRIPT, "echo done")

    def m_db_no_set(w):
        set_db_script(w, CANONICAL_OBSERVED, CANONICAL_CALL)

    # #209: the conditions under which the gate job runs at all, rather than
    # what it does once it runs.
    def gate_step_list(w):
        return jobs(w[RTL_FULL])[GATE_JOB]["steps"]

    def pin_step(w):
        return next(s for s in gate_step_list(w)
                    if s.get("id") == PIN_STEP_ID)

    def decide_step(w):
        return next(s for s in gate_step_list(w)
                    if s.get("id") == DECIDE_STEP_ID)

    def m_gate_needs_a_skippable_job(w):
        # O1: a `noop` job that skips on schedule, and a gate that needs it.
        jobs(w[RTL_FULL])["noop"] = {
            "if": "${{ github.event_name != 'schedule' }}",
            "runs-on": "ubuntu-latest",
            "steps": [{"run": "true"}],
        }
        jobs(w[RTL_FULL])[GATE_JOB]["needs"] = ["noop"]

    def m_assert_before_checkout(w):
        # O14: the assertion runs before the checkout brings the script.
        ss = gate_step_list(w)
        i = next(i for i, s in enumerate(ss)
                 if DEFAULT_BRANCH_FLAG in step_text(s))
        ss.insert(0, ss.pop(i))

    def m_pin_and_assert_swapped(w):
        ss = gate_step_list(w)
        i = next(i for i, s in enumerate(ss) if s.get("id") == PIN_STEP_ID)
        ss[i], ss[i + 1] = ss[i + 1], ss[i]

    def m_gate_extra_path_step(w):
        # O6: a step before the assertion that puts another `gh` first.
        ss = gate_step_list(w)
        i = next(i for i, s in enumerate(ss)
                 if DEFAULT_BRANCH_FLAG in step_text(s))
        ss.insert(i, {"name": "Prepare tools",
                      "run": 'echo "$RUNNER_TEMP/bin" >> "$GITHUB_PATH"\n'})

    def m_pin_step_removed(w):
        ss = gate_step_list(w)
        del ss[next(i for i, s in enumerate(ss)
                    if s.get("id") == PIN_STEP_ID)]

    def m_checkout_shallow(w):
        del gate_step_list(w)[0]["with"]["fetch-depth"]

    def m_gate_env_gh_host(w):
        jobs(w[RTL_FULL])[GATE_JOB]["env"] = {"GH_HOST": "example.invalid"}

    def m_workflow_env_gh_host(w):
        w[RTL_FULL]["env"]["GH_HOST"] = "example.invalid"

    def m_decide_env_missing(w):
        del decide_step(w)["env"]["PR_BASE_SHA"]

    def m_decide_script_no_op(w):
        # O16: the guarded `run_full=true` becomes `run_full=false`. Every
        # pinned key, every pinned name and every binding survives.
        s = decide_step(w)
        assert re.search(r"^\s*run_full=true$", s["run"], re.M), (
            "fixture drift: no bare `run_full=true` in the decision step")
        s["run"] = re.sub(r"^(\s*)run_full=true$", r"\1run_full=false",
                          s["run"], count=1, flags=re.M)

    def m_decide_script_unproven_selector(w):
        # O16b: the selector decides the run without its own self-test.
        s = decide_step(w)
        assert SELECTOR_SELFTEST in s["run"], (
            "fixture drift: the decision step does not self-test the selector")
        s["run"] = s["run"].replace(SELECTOR_SELFTEST, "true", 1)

    # #209 O17-O20: the publication path. A selector's `outputs` map is a
    # NAME -> EXPRESSION mapping like a step's `env`, and every arm below
    # leaves every pinned step key, env binding and script character intact.
    def sel_outputs(w, path=RTL_FULL):
        return jobs(w[path])[SELECTOR_JOB[path]]["outputs"]

    def m_output_rebound(path, name, expr):
        def f(w):
            outs = sel_outputs(w, path)
            assert name in outs, f"fixture drift: no `{name}` output"
            outs[name] = expr
        return f

    def m_output_dropped(path, name):
        def f(w):
            outs = sel_outputs(w, path)
            assert name in outs, f"fixture drift: no `{name}` output"
            del outs[name]
        return f

    def m_output_surplus(w):
        sel_outputs(w)["shadow"] = step_output_ref(DECIDE_STEP_ID,
                                                   RUN_FULL_OUTPUT)

    def m_outputs_map_dropped(w):
        del jobs(w[RTL_FULL])[SELECTOR_JOB[RTL_FULL]]["outputs"]

    def set_job_if(path, jid, value):
        def f(w):
            jobs(w[path])[jid]["if"] = value
        return f

    def set_job_key_at(path, jid, key, value):
        def f(w):
            jobs(w[path])[jid][key] = value
        return f

    def fast_scope_step(w):
        found = [s for s in job_steps(w, RTL_FAST, FAST_SELECTOR_JOB)
                 if isinstance(s, dict)
                 and s.get("id") == FAST_SCOPE_STEP_ID]
        assert len(found) == 1, "fixture drift: no unique fast scope step"
        return found[0]

    def fast_checkout_step(w):
        found = [s for s in job_steps(w, RTL_FAST, FAST_SELECTOR_JOB)
                 if isinstance(s, dict) and _is_checkout_step(s)]
        assert len(found) == 1, "fixture drift: no unique fast checkout step"
        return found[0]

    def fast_bdd_run_step(w):
        found = [s for s in job_steps(w, RTL_FAST, "bdd-conformance")
                 if "behave --no-capture" in step_text(s)]
        assert len(found) == 1, "fixture drift: no unique BDD run step"
        return found[0]

    def fast_aggregate_job(w):
        return jobs(w[RTL_FAST])["rtl-fast"]

    def fast_verdict_step(w):
        ss = [s for s in fast_aggregate_job(w).get("steps", [])
              if isinstance(s, dict)]
        assert len(ss) == 1, "fixture drift: fast aggregate is not one step"
        return ss[0]

    def m_fast_verdict_case_widened(w):
        s = fast_verdict_step(w)
        assert "success|skipped)" in s["run"], (
            "fixture drift: no accept case in the fast verdict")
        s["run"] = s["run"].replace("success|skipped)",
                                    "success|skipped|failure)", 1)

    def m_fast_aggregate_forgets_bdd(w):
        # The whole trace of `bdd-conformance` removed from the aggregate
        # consistently: the `needs` entry, the env binding and the loop pair,
        # so the derived env and script agree with the shrunk `needs` and the
        # only refusal left is the `needs` universe itself.
        agg = fast_aggregate_job(w)
        assert "bdd-conformance" in agg["needs"], (
            "fixture drift: the aggregate does not need bdd-conformance")
        agg["needs"] = [n for n in agg["needs"] if n != "bdd-conformance"]
        step = fast_verdict_step(w)
        del step["env"]["BDD_CONFORMANCE_RESULT"]
        pair = '"bdd-conformance:$BDD_CONFORMANCE_RESULT"'
        step["run"], n = re.subn(r"\s*" + re.escape(pair) + r" \\", "",
                                 step["run"])
        assert n == 1, "fixture drift: no bdd pair line in the verdict loop"

    def m_fast_new_unaggregated_job(w):
        jobs(w[RTL_FAST])["extra-check"] = {
            "runs-on": "ubuntu-latest",
            "steps": [{"run": "true"}],
        }

    def m_fast_lint_masquerades_as_aggregate(w):
        job = jobs(w[RTL_FAST])["verilator-lint"]
        job["name"] = "rtl-fast"
        job["if"] = FAST_AGGREGATE_JOB_IF

    def m_fast_scope_publishes_false(w):
        # The selector still self-tests and reads the real answer, but exports
        # a literal false. Both RTL consumers skip and the aggregate passes.
        scope = fast_scope_step(w)
        old = 'echo "rtl=$rtl" >> "$GITHUB_OUTPUT"'
        assert old in scope["run"], "fixture drift: no fast rtl publication"
        scope["run"] = scope["run"].replace(
            old, 'echo "rtl=false" >> "$GITHUB_OUTPUT"', 1)

    def m_fast_scope_unproven(w):
        scope = fast_scope_step(w)
        assert SELECTOR_SELFTEST in scope["run"], (
            "fixture drift: fast scope does not self-test the selector")
        scope["run"] = scope["run"].replace(SELECTOR_SELFTEST, "true", 1)

    def m_fast_steps_swapped(w):
        ss = job_steps(w, RTL_FAST, FAST_SELECTOR_JOB)
        assert len(ss) == 2, "fixture drift: fast selector is not two steps"
        ss[0], ss[1] = ss[1], ss[0]

    def m_fast_checkout_shallow(w):
        del fast_checkout_step(w)["with"]["fetch-depth"]

    def m_fast_top_defaults(w):
        w[RTL_FAST]["defaults"] = {"run": {"shell": "bash -n {0}"}}

    def m_fast_bdd_needs_expression(expression):
        def f(w):
            fast_bdd_run_step(w)["if"] = expression
        return f

    def m_worker_needs_dropped(w):
        del jobs(w[RTL_FULL])["verilator-shards"]["needs"]

    def m_new_consumer_job(w):
        # The perimeter closed under addition: a job that depends on the
        # selector and carries no gate on its decision runs on every event.
        jobs(w[RTL_FULL])["extra-worker"] = {
            "needs": GATE_JOB,
            "runs-on": "ubuntu-latest",
            "steps": [{"run": "true"}],
        }

    def restate_shards(w, jid, value):
        """Turn a derived denominator back into a literal, everywhere the job
        states it: the display name, every script, every step env."""
        job = jobs(w[RTL_FULL])[jid]
        assert DERIVED_SHARD_TOTAL in job["name"], f"fixture drift: {jid} name"
        job["name"] = job["name"].replace(DERIVED_SHARD_TOTAL, value)
        for st in steps(job):
            if isinstance(st.get("run"), str):
                st["run"] = st["run"].replace(DERIVED_SHARD_TOTAL, value)
            env = st.get("env")
            if isinstance(env, dict):
                for k, v in list(env.items()):
                    if str(v).strip() == DERIVED_SHARD_TOTAL:
                        env[k] = value

    def m_shard_denominator_stale(w):
        # O9: the matrix grows, the restated denominator does not.
        restate_shards(w, "verilator-shards", "4")
        jobs(w[RTL_FULL])["verilator-shards"]["strategy"]["matrix"][
            "shard"].append(4)

    def m_shard_total_missing(w):
        del jobs(w[RTL_FULL])["verilator-shards"]["strategy"]["matrix"][
            "total"]

    def m_shard_total_wrong(w):
        jobs(w[RTL_FULL])["yosys-shards"]["strategy"]["matrix"]["total"] = [3]

    def m_shard_denominator_wrong(w):
        restate_shards(w, "yosys-shards", "3")

    def m_shard_name_stale(w):
        job = jobs(w[RTL_FULL])["verilator-shards"]
        job["name"] = job["name"].replace(DERIVED_SHARD_TOTAL, "3")

    def m_shard_matrix_include(w):
        jobs(w[RTL_FULL])["verilator-shards"]["strategy"]["matrix"][
            "include"
        ] = [{"shard": 4, "total": 5}]

    def m_shard_matrix_exclude(w):
        jobs(w[RTL_FULL])["yosys-shards"]["strategy"]["matrix"][
            "exclude"
        ] = [{"shard": 3}]

    def verify_step(w, jid):
        for s in steps(jobs(w[RTL_FULL])[jid]):
            if VERIFY_FLAG in step_text(s):
                return s
        raise AssertionError(f"fixture drift: no verifier step in {jid}")

    def m_drop_sha(jid, label):
        def f(w):
            s = verify_step(w, jid)
            want = REQUIRED_SHA_ARGS[label]
            assert want in s["run"], f"fixture drift: {want} not in {jid}"
            s["run"] = s["run"].replace(want + " ", "").replace(want, "")
        return f

    def m_extra_sha(w):
        s = verify_step(w, "verilator-suites")
        s["run"] = s["run"].replace(VERIFY_FLAG,
                                    VERIFY_FLAG + ' --sha extra="$GITHUB_SHA"')

    # The third-round escapes: keys beside a canonical script ([R1]).
    def set_step_key(getter, key, value):
        def f(w):
            getter(w)[key] = value
        return f

    def set_env_key(getter, key, value):
        def f(w):
            getter(w)["env"][key] = value
        return f

    def set_job_key(jid, key, value):
        def f(w):
            jobs(w[RTL_FULL])[jid][key] = value
        return f

    def m_top_defaults(w):
        w[RTL_FULL]["defaults"] = {"run": {"shell": "bash -n {0}"}}

    def m_verify_assigns_gate(w):
        s = verify_step(w, "verilator-suites")
        s["run"] = 'GATE_SHA="$GITHUB_SHA"\n' + s["run"]

    def m_verify_expect_wrong(w):
        s = verify_step(w, "yosys-portability")
        assert "--expect 4" in s["run"]
        s["run"] = s["run"].replace("--expect 4", "--expect 3")

    def m_verify_expect_missing(w):
        s = verify_step(w, "verilator-suites")
        assert "--expect 4 " in s["run"]
        s["run"] = s["run"].replace("--expect 4 ", "")

    def m_matrix_grows_expect_stays(w):
        jobs(w[RTL_FULL])["verilator-shards"]["strategy"]["matrix"]["shard"].append(4)

    def m_aggregate_if_loosened(w):
        jobs(w[RTL_FULL])["verilator-suites"]["if"] = "${{ always() }}"

    def m_aggregate_if_dropped(w):
        del jobs(w[RTL_FULL])["yosys-portability"]["if"]

    def m_aggregate_fail_open(w):
        jobs(w[RTL_FULL])["verilator-suites"]["if"] = (
            "${{ always() && !cancelled() && "
            "needs.full-ci-gate.outputs.run_full == 'true' }}"
        )

    va = lambda w: verify_step(w, "verilator-suites")  # noqa: E731
    ya = lambda w: verify_step(w, "yosys-portability")  # noqa: E731

    def m_docs_no_check(w):
        for job in jobs(w[DOCS]).values():
            for s in steps(job):
                if "scripts/ci_events.py --check" in step_text(s):
                    s["run"] = s["run"].replace("scripts/ci_events.py --check",
                                                "true")
                    return
        raise AssertionError("fixture drift: docs.yml does not run --check")

    def m_docs_no_selftest(w):
        for job in jobs(w[DOCS]).values():
            for s in steps(job):
                if "scripts/ci_events.py --selftest" in step_text(s):
                    s["run"] = s["run"].replace(
                        "scripts/ci_events.py --selftest", "true")
                    return
        raise AssertionError("fixture drift: docs.yml does not run --selftest")

    def docs_act_selftest_step(w):
        job = jobs(w[DOCS])["docs-check"]
        found = [s for s in steps(job)
                 if tuple(normalize_script(
                     s.get("run") if isinstance(s.get("run"), str) else ""
                 )) == (ACT_CI_SELFTEST,)]
        assert len(found) == 1, (
            "fixture drift: no unique act_ci.py self-test step")
        return found[0]

    def m_docs_no_act_selftest(w):
        job = jobs(w[DOCS])["docs-check"]
        target = docs_act_selftest_step(w)
        job["steps"].remove(target)

    def m_docs_act_selftest_key(key, value):
        def mutate(w):
            docs_act_selftest_step(w)[key] = value
        return mutate

    def builder_fetch_step(w, path, jid):
        found = [s for s in job_steps(w, path, jid)
                 if "git submodule update --init" in
                 (s.get("run") if isinstance(s.get("run"), str) else "")]
        assert len(found) == 1, (f"fixture drift: expected one builder "
                                 f"checkout in {path}:{jid}, found {len(found)}")
        return found[0]

    def builder_call_step(w, path, jid):
        found = [s for s in job_steps(w, path, jid)
                 if BUILDER_CALL in
                 (s.get("run") if isinstance(s.get("run"), str) else "")]
        assert len(found) == 1, (f"fixture drift: expected one builder call "
                                 f"in {path}:{jid}, found {len(found)}")
        return found[0]

    def m_builder_drop_submodule(path, jid, submodule):
        def f(w):
            s = builder_fetch_step(w, path, jid)
            assert submodule in s["run"], (
                f"fixture drift: {submodule} absent from {path}:{jid}")
            s["run"] = s["run"].replace(" " + submodule, "")
        return f

    def m_builder_checkout_after_call(path, jid):
        def f(w):
            ss = job_steps(w, path, jid)
            fetch = next(i for i, s in enumerate(ss)
                         if "git submodule update --init" in
                         (s.get("run") if isinstance(s.get("run"), str) else ""))
            call = next(i for i, s in enumerate(ss)
                        if BUILDER_CALL in
                        (s.get("run") if isinstance(s.get("run"), str) else ""))
            step = ss.pop(fetch)
            if fetch < call:
                call -= 1
            ss.insert(call + 1, step)
        return f

    def m_builder_checkout_before_repo(path, jid):
        def f(w):
            ss = job_steps(w, path, jid)
            fetch = next(i for i, s in enumerate(ss)
                         if s is builder_fetch_step(w, path, jid))
            checkout = next(i for i, s in enumerate(ss)
                            if uses(s, "actions/checkout"))
            step = ss.pop(fetch)
            if fetch < checkout:
                checkout -= 1
            ss.insert(checkout, step)
        return f

    def m_builder_checkout_key(path, jid, key, value):
        def f(w):
            checkout = next(s for s in job_steps(w, path, jid)
                            if uses(s, "actions/checkout"))
            checkout[key] = value
        return f

    def m_builder_checkout_version(path, jid):
        def f(w):
            checkout = next(s for s in job_steps(w, path, jid)
                            if uses(s, "actions/checkout"))
            checkout["uses"] = "actions/checkout@v1"
        return f

    def m_builder_decoy_env(path, jid):
        def f(w):
            s = builder_call_step(w, path, jid)
            line = next(line for line in BUILDER_RUNS[path]
                        if BUILDER_CALL in line)
            assert line in s["run"], f"fixture drift: {line!r} absent"
            s["run"] = s["run"].replace(line, "true")
            s["env"] = {"DECOY": BUILDER_CALL}
        return f

    def m_builder_continue_on_error(path, jid):
        def f(w):
            builder_call_step(w, path, jid)["continue-on-error"] = True
        return f

    def m_builder_job_defaults(path, jid):
        def f(w):
            jobs(w[path])[jid]["defaults"] = {
                "run": {"shell": "bash -n {0}"},
            }
        return f

    def m_builder_top_defaults(path):
        def f(w):
            w[path]["defaults"] = {"run": {"shell": "bash -n {0}"}}
        return f

    def m_builder_both_if_false(w):
        builder_fetch_step(w, ELABORATE, "elaborate")["if"] = False
        builder_call_step(w, ELABORATE, "elaborate")["if"] = False

    def sv2v_step(w, path, jid):
        found = [s for s in job_steps(w, path, jid)
                 if "sv2v" in (s.get("run")
                               if isinstance(s.get("run"), str) else "")]
        assert len(found) == 1, (f"fixture drift: expected one sv2v install "
                                 f"in {path}:{jid}, found {len(found)}")
        return found[0]

    def m_sv2v_dropped(path, jid):
        def f(w):
            ss = job_steps(w, path, jid)
            ss.remove(sv2v_step(w, path, jid))
        return f

    def m_sv2v_unpinned(path, jid):
        def f(w):
            s = sv2v_step(w, path, jid)
            assert "ver=v0.0.12" in s["run"], "fixture drift: pin absent"
            s["run"] = s["run"].replace("ver=v0.0.12", "ver=v0.0.13")
        return f

    def m_sv2v_after_call(path, jid):
        def f(w):
            ss = job_steps(w, path, jid)
            step = sv2v_step(w, path, jid)
            call = builder_call_step(w, path, jid)
            ss.remove(step)
            ss.insert(ss.index(call) + 1, step)
        return f

    def m_sv2v_if_disabled(w):
        sv2v_step(w, ELABORATE, "elaborate")["if"] = False

    # #245: the ooc.sh refusal self-test's step, by the three ways it was
    # shown to disappear undetected ([R-parallel] on PR #262).
    def _fast_ooc_job(w):
        job = jobs(w[RTL_FAST]).get(OOC_SH_SELFTEST_JOB)
        if job is None:
            raise AssertionError("fixture drift: rtl-fast.yml has no "
                                 f"`{OOC_SH_SELFTEST_JOB}` job")
        return job

    def _fast_ooc_index(job):
        for i, s in enumerate(steps(job)):
            if OOC_SH_SELFTEST in step_text(s):
                return i
        raise AssertionError("fixture drift: rtl-fast.yml does not run "
                             "the ooc.sh self-test")

    def m_ooc_selftest_removed(w):
        job = _fast_ooc_job(w)
        job["steps"] = [s for s in steps(job)
                        if OOC_SH_SELFTEST not in step_text(s)]

    def m_ooc_selftest_neutralised(w):
        job = _fast_ooc_job(w)
        steps(job)[_fast_ooc_index(job)]["run"] = (
            "true # " + OOC_SH_SELFTEST)

    def m_ooc_selftest_fetch_drops_submodule(submodule):
        def mutate(w):
            job = _fast_ooc_job(w)
            for s in steps(job):
                if OOC_SH_SUBMODULE_FETCH in step_text(s) \
                        and submodule in step_text(s):
                    s["run"] = str(s["run"]).replace(" " + submodule, "")
                    return
            raise AssertionError("fixture drift: rtl-fast.yml's ooc.sh job "
                                 f"does not fetch `{submodule}`")
        return mutate

    def m_ooc_selftest_before_fetch(w):
        job = _fast_ooc_job(w)
        slist = job["steps"]
        slist.insert(0, slist.pop(_fast_ooc_index(job)))

    def m_ooc_selftest_key(key, value):
        def f(w):
            job = _fast_ooc_job(w)
            steps(job)[_fast_ooc_index(job)][key] = value
        return f

    return [
        # rtl.yml triggers
        ("rtl push on main, not dev", m_push_main(RTL_FULL), "push must subscribe"),
        ("rtl no pull_request", m_drop_pr(RTL_FULL), "must subscribe pull_request"),
        ("rtl PR type missing", m_pr_type_missing(RTL_FULL), "pull_request.types"),
        ("rtl PR type extra", m_pr_type_extra(RTL_FULL), "pull_request.types"),
        ("rtl no workflow_dispatch", m_drop_dispatch, "workflow_dispatch"),
        ("rtl dispatch with inputs", m_dispatch_inputs, "no inputs"),
        ("rtl no schedule", m_drop_schedule, "exactly one cron"),
        ("rtl two crons", m_two_crons, "exactly one cron"),
        ("rtl cron moved, page unchanged", m_cron_moved, "cron's time"),
        ("rtl cron not daily", m_cron_shape, "daily"),
        ("page states another time", m_page_time, "cron's time"),
        ("page states another cron string", m_page_cron, "cron string"),
        ("rtl cancel-in-progress false", m_cancel_false(RTL_FULL),
         "cancel-in-progress"),
        ("rtl no concurrency block", m_no_concurrency(RTL_FULL),
         "cancel-in-progress"),
        # rtl.yml SHA contract
        ("rtl checkout overrides ref", m_checkout_ref, "must not override `ref`"),
        ("rtl checkout ref via expression", m_checkout_ref_deep,
         "must not override `ref`"),
        ("rtl gate drops target_sha output", m_drop_gate_output,
         f"missing: {GATE_OUTPUT}"),
        ("rtl gate prints nothing", m_gate_silent, "print the event name"),
        ("rtl Verilator worker records nothing", m_worker_no_record,
         f"write GITHUB_SHA into {RECORD}"),
        ("rtl Yosys worker records nothing", m_yosys_no_record,
         f"write GITHUB_SHA into {RECORD}"),
        ("rtl record written after the upload", m_record_after_upload,
         f"write GITHUB_SHA into {RECORD}"),
        ("rtl verilator-suites skips the verifier", m_aggregate_no_verify,
         VERIFY_FLAG),
        ("rtl yosys-portability skips the verifier",
         m_yosys_aggregate_no_verify, VERIFY_FLAG),
        ("rtl aggregate no longer needs the gate", m_aggregate_without_gate,
         f"must need `{GATE_JOB}`"),
        ("rtl artifact aggregates can initialize concurrently",
         m_artifact_aggregates_race, "concurrent first-use download actions"),
        ("rtl default-branch step removed", m_db_step_removed,
         "exactly one step"),
        ("rtl default-branch step without GH_TOKEN", m_db_token_missing,
         "GH_TOKEN"),
        ("rtl default-branch step reads nothing live", m_db_no_live_read,
         "gh api"),
        ("rtl default-branch step without the event", m_db_event_not_passed,
         "--event"),
        ("rtl default-branch step neutered by continue-on-error",
         m_db_continue_on_error, "fail closed"),
        ("rtl default-branch step neutered by || true", m_db_or_true,
         "fail closed"),
        ("rtl default-branch decoy: observed=dev beside gh api in `if false`",
         m_db_decoy_if_false, "not sourced from the live API call"),
        ("rtl default-branch decoy: control flow around the live read",
         m_db_decoy_if_false, "unconditionally"),
        ("rtl default-branch literal observed=dev after the real call",
         m_db_literal_after_call, "exactly once (found 2)"),
        ("rtl default-branch literal observed=dev after the real read",
         m_db_literal_after_read, "exactly once (found 2)"),
        ("rtl default-branch gh api inside a comment only",
         m_db_gh_api_in_comment, "not sourced from the live API call"),
        ("rtl default-branch comment line in the script",
         m_db_gh_api_in_comment, "no comment lines"),
        ("rtl default-branch observed from a different command",
         m_db_other_command, "not sourced from the live API call"),
        ("rtl default-branch two observed assignments",
         m_db_two_assignments, "exactly once (found 2)"),
        ("rtl default-branch verifier called before the read",
         m_db_call_before_read, "must follow the live read"),
        ("rtl default-branch script with an extra line", m_db_extra_line,
         "not the canonical form"),
        ("rtl default-branch script without set -euo pipefail", m_db_no_set,
         "not the canonical form"),
        ("rtl verilator-suites drops --sha gate",
         m_drop_sha("verilator-suites", "gate"), "missing: gate"),
        ("rtl verilator-suites drops --sha run",
         m_drop_sha("verilator-suites", "run"), "missing: run"),
        ("rtl verilator-suites drops --sha checkout",
         m_drop_sha("verilator-suites", "checkout"), "missing: checkout"),
        ("rtl yosys-portability drops --sha gate",
         m_drop_sha("yosys-portability", "gate"), "missing: gate"),
        ("rtl yosys-portability drops --sha run",
         m_drop_sha("yosys-portability", "run"), "missing: run"),
        ("rtl yosys-portability drops --sha checkout",
         m_drop_sha("yosys-portability", "checkout"), "missing: checkout"),
        ("rtl verilator-suites passes an unknown --sha label", m_extra_sha,
         "unknown: extra"),
        # [R1] third round: escapes beside the script.
        ("E9 assert step if: false", set_step_key(db_step, "if", False),
         "must carry no `if`"),
        ("E10 assert step if: pull_request only",
         set_step_key(db_step, "if", "${{ github.event_name == 'pull_request' }}"),
         "must carry no `if`"),
        ("E11 assert step shell: bash -n",
         set_step_key(db_step, "shell", "bash -n {0}"), "must carry no `shell`"),
        ("E12 full-ci-gate continue-on-error",
         set_job_key(GATE_JOB, "continue-on-error", True),
         "must carry no `continue-on-error`"),
        ("E13 full-ci-gate if: not schedule",
         set_job_key(GATE_JOB, "if", "${{ github.event_name != 'schedule' }}"),
         "must carry no `if`"),
        ("E14 assert step env GH_HOST",
         set_env_key(db_step, "GH_HOST", "example.invalid"), "surplus: GH_HOST"),
        ("E14b assert step env GH_CONFIG_DIR",
         set_env_key(db_step, "GH_CONFIG_DIR", "/tmp/gh"), "surplus: GH_CONFIG_DIR"),
        ("E17 full-ci-gate defaults.run.shell bash -n",
         set_job_key(GATE_JOB, "defaults", {"run": {"shell": "bash -n {0}"}}),
         "must carry no `defaults`"),
        ("workflow-level defaults.run.shell", m_top_defaults,
         "no top-level `defaults`"),
        ("assert step extra key working-directory",
         set_step_key(db_step, "working-directory", "/tmp"),
         "surplus: working-directory"),
        ("assert step continue-on-error",
         set_step_key(db_step, "continue-on-error", True),
         "must carry no `continue-on-error`"),
        ("S8 verilator-suites verifier if: false", set_step_key(va, "if", False),
         "`if` must be exactly"),
        ("yosys-portability verifier if: pull_request only",
         set_step_key(ya, "if", "${{ github.event_name == 'pull_request' }}"),
         "`if` must be exactly"),
        ("verifier step shell: bash -n", set_step_key(ya, "shell", "bash -n {0}"),
         "must carry no `shell`"),
        ("verifier step continue-on-error",
         set_step_key(va, "continue-on-error", True),
         "must carry no `continue-on-error`"),
        ("verifier step env GITHUB_SHA override",
         set_env_key(va, "GITHUB_SHA", "0" * 40), "surplus: GITHUB_SHA"),
        ("S5 verifier script reassigns GATE_SHA", m_verify_assigns_gate,
         "not the canonical form"),
        ("R4 verifier --expect disagrees with the matrix", m_verify_expect_wrong,
         "--expect 4"),
        ("R4 verifier without --expect", m_verify_expect_missing,
         "no --expect"),
        ("R4 matrix grows, --expect stays", m_matrix_grows_expect_stays,
         "--expect 5"),
        ("aggregate job if loosened", m_aggregate_if_loosened,
         "`if` must be exactly"),
        ("aggregate job if dropped", m_aggregate_if_dropped,
         "documented `if`"),
        ("aggregate skips when its selector fails", m_aggregate_fail_open,
         "`if` must be exactly"),
        ("aggregate job continue-on-error",
         set_job_key("verilator-suites", "continue-on-error", True),
         "must carry no `continue-on-error`"),
        ("aggregate job defaults.run.shell",
         set_job_key("yosys-portability", "defaults",
                     {"run": {"shell": "bash -n {0}"}}),
         "must carry no `defaults`"),
        # #209: the conditions under which the gate job and its steps run.
        ("O1 full-ci-gate needs a job that skips on schedule",
         m_gate_needs_a_skippable_job, "must carry no `needs`"),
        ("O10 decision step if: false",
         set_step_key(decide_step, "if", False), "must carry no `if`"),
        ("O10b decision step if: pull_request only",
         set_step_key(decide_step, "if",
                      "${{ github.event_name == 'pull_request' }}"),
         "must carry no `if`"),
        ("O13 pin step if: false", set_step_key(pin_step, "if", False),
         "must carry no `if`"),
        ("O13b pin step continue-on-error",
         set_step_key(pin_step, "continue-on-error", True),
         "must carry no `continue-on-error`"),
        ("O14 assert step moved before the checkout", m_assert_before_checkout,
         "step 1 must be the gate checkout step"),
        ("O6 a GITHUB_PATH step inserted before the assertion",
         m_gate_extra_path_step, "must carry exactly 4 steps"),
        ("gate pin step removed", m_pin_step_removed,
         "must carry exactly 4 steps"),
        ("gate pin and assert steps swapped", m_pin_and_assert_swapped,
         "step 2 must be the pin step"),
        ("gate checkout without fetch-depth: 0", m_checkout_shallow,
         "fetch-depth: 0"),
        ("decision step shell: bash -n",
         set_step_key(decide_step, "shell", "bash -n {0}"),
         "must carry no `shell`"),
        ("decision step working-directory",
         set_step_key(decide_step, "working-directory", "/tmp"),
         "surplus: working-directory"),
        ("decision step loses PR_BASE_SHA", m_decide_env_missing,
         "missing: PR_BASE_SHA"),
        # #209 O15/O16: the decision step's env bound to another source, and
        # its script rewritten, each leaving every pinned name and key alone.
        ("O15 decision step PR_DRAFT forced true",
         set_env_key(decide_step, "PR_DRAFT", "true"),
         "must bind `PR_DRAFT`"),
        ("O15b decision step PR_BASE_SHA rebound to this run's own SHA",
         set_env_key(decide_step, "PR_BASE_SHA", "${{ github.sha }}"),
         "must bind `PR_BASE_SHA`"),
        ("O15c decision step EVENT_NAME hard-coded to pull_request",
         set_env_key(decide_step, "EVENT_NAME", "pull_request"),
         "must bind `EVENT_NAME`"),
        ("O15d assert step GH_TOKEN rebound to another token",
         set_env_key(db_step, "GH_TOKEN", "${{ secrets.OTHER_TOKEN }}"),
         "must bind `GH_TOKEN`"),
        ("O15e verifier step GATE_SHA rebound to its own run",
         set_env_key(va, "GATE_SHA", "${{ github.sha }}"),
         "must bind `GATE_SHA`"),
        ("O16 decision script publishes the no-op decision always",
         m_decide_script_no_op, "decision step script is not the canonical"),
        ("O16b decision script drops the selector's self-test",
         m_decide_script_unproven_selector,
         "before it reads the selector's answer"),
        ("O11 full-ci-gate job env GH_HOST", m_gate_env_gh_host,
         "must name no `GH_*`"),
        ("O12 workflow-level env GH_HOST", m_workflow_env_gh_host,
         "must name no `GH_*`"),
        # #209 O17: the gate's published outputs map, held by content. Each
        # arm keeps every pinned step key, env binding and script character.
        ("O17 gate exports run_full as the literal 'false'",
         m_output_rebound(RTL_FULL, RUN_FULL_OUTPUT, "${{ 'false' }}"),
         f"must bind `{RUN_FULL_OUTPUT}`"),
        ("O17b gate stops exporting run_full at all",
         m_output_dropped(RTL_FULL, RUN_FULL_OUTPUT),
         f"missing: {RUN_FULL_OUTPUT}"),
        ("O17c gate exports run_full from the scope answer instead",
         m_output_rebound(RTL_FULL, RUN_FULL_OUTPUT,
                          step_output_ref(DECIDE_STEP_ID, RTL_OUTPUT)),
         f"must bind `{RUN_FULL_OUTPUT}`"),
        ("O17d gate exports rtl as the literal 'false'",
         m_output_rebound(RTL_FULL, RTL_OUTPUT, "${{ 'false' }}"),
         f"must bind `{RTL_OUTPUT}`"),
        ("O17e gate stops exporting rtl", m_output_dropped(RTL_FULL,
                                                           RTL_OUTPUT),
         f"missing: {RTL_OUTPUT}"),
        ("O17f gate exports target_sha from the run instead of the pin step",
         m_output_rebound(RTL_FULL, GATE_OUTPUT, "${{ github.sha }}"),
         f"must bind `{GATE_OUTPUT}`"),
        ("O17g gate exports no outputs map at all", m_outputs_map_dropped,
         f"missing: {RUN_FULL_OUTPUT}, {RTL_OUTPUT}, {GATE_OUTPUT}"),
        ("O17h gate exports a surplus output", m_output_surplus,
         "surplus: shadow"),
        # #209 O18: the consumers of that decision.
        ("O18 a worker gates on an output nobody publishes",
         set_job_if(RTL_FULL, "verilator-shards",
                    "${{ needs.full-ci-gate.outputs.run_ful == 'true' }}"),
         "must publish"),
        ("O18b a worker gates on if: false",
         set_job_if(RTL_FULL, "yosys-shards", False), "`if` must be exactly"),
        ("O18c a worker compares the decision with a value it never takes",
         set_job_if(RTL_FULL, "verilator-shards",
                    "${{ needs.full-ci-gate.outputs.run_full == 'nope' }}"),
         "`if` must be exactly"),
        ("O18d a worker turns its own failure into a pass",
         set_job_key("verilator-shards", "continue-on-error", True),
         "must carry no `continue-on-error`"),
        ("O18e a worker reads the decision without needing the gate",
         m_worker_needs_dropped, f"must list `{GATE_JOB}` in its `needs`"),
        ("O18f a worker parses every script instead of running it",
         set_job_key("yosys-shards", "defaults",
                     {"run": {"shell": "bash -n {0}"}}),
         "must carry no `defaults`"),
        ("O20 a new job depends on the gate and gates on nothing",
         m_new_consumer_job, "documented `if`"),
        # #209 O19: the same publication path in the fast workflow, whose
        # aggregate counts a skipped consumer as a pass.
        ("O19 fast selector exports rtl as the literal 'false'",
         m_output_rebound(RTL_FAST, RTL_OUTPUT, "${{ 'false' }}"),
         f"must bind `{RTL_OUTPUT}`"),
        ("O19b fast selector stops exporting rtl",
         m_output_dropped(RTL_FAST, RTL_OUTPUT), f"missing: {RTL_OUTPUT}"),
        ("O19c a fast consumer gates on an output nobody publishes",
         set_job_if(RTL_FAST, "verilator-lint",
                    "${{ needs.changes.outputs.rt == 'true' }}"),
         "must publish"),
        ("O19d a fast consumer gates on if: false",
         set_job_if(RTL_FAST, "yosys-elaboration", False),
         "`if` must be exactly"),
        # #209 O21: the producer of the fast answer must run and publish the
        # value it computed. Each arm leaves the selector output map and both
        # consumer conditions canonical while making their jobs skip.
        ("O21 fast selector job if: false",
         set_job_if(RTL_FAST, FAST_SELECTOR_JOB, False),
         f"job `{FAST_SELECTOR_JOB}` must carry no `if`"),
        ("O21b fast scope step if: false",
         set_step_key(fast_scope_step, "if", False),
         "fast selector scope step must carry no `if`"),
        ("O21c fast scope publishes literal rtl=false",
         m_fast_scope_publishes_false,
         "fast selector scope script is not the canonical form"),
        ("O21d fast scope drops the selector self-test",
         m_fast_scope_unproven,
         "before it reads the selector's answer"),
        ("O21e fast scope EVENT_NAME rebound to pull_request",
         set_env_key(fast_scope_step, "EVENT_NAME", "pull_request"),
         "fast selector scope step env must bind `EVENT_NAME`"),
        ("O21f fast selector continue-on-error",
         set_job_key_at(RTL_FAST, FAST_SELECTOR_JOB,
                        "continue-on-error", True),
         f"job `{FAST_SELECTOR_JOB}` must carry no `continue-on-error`"),
        ("O21g fast selector scope runs before checkout",
         m_fast_steps_swapped,
         "steps must be exactly `actions/checkout@v4`"),
        ("O21h fast selector checkout is shallow",
         m_fast_checkout_shallow,
         "fast selector checkout `with` must be exactly fetch-depth"),
        ("O21i fast workflow parses selector scripts instead of running",
         m_fast_top_defaults,
         "fast workflow must carry no top-level `defaults`"),
        # #209 O22: GitHub permits index and mixed property syntax for the
        # same needs context. These expressions sit on the otherwise
        # independent BDD job so only the closed reference audit can catch
        # them; the ordinary consumer-if comparison is not involved.
        ("O22 bracket needs reference names an unpublished output",
         m_fast_bdd_needs_expression(
             "${{ needs['changes'].outputs.bogus == 'true' }}"),
         "must publish"),
        ("O22b all-bracket needs reference omits its dependency",
         m_fast_bdd_needs_expression(
             "${{ needs['changes']['outputs']['rtl'] == 'true' }}"),
         "must list `changes` in its `needs`"),
        ("O22c mixed needs reference names an unpublished output",
         m_fast_bdd_needs_expression(
             "${{ needs.changes['outputs'].bogus == 'true' }}"),
         "must publish"),
        ("O22d dynamic needs reference cannot evade static audit",
         m_fast_bdd_needs_expression(
             "${{ needs[format('{0}', 'changes')].outputs.rtl == 'true' }}"),
         "cannot resolve statically"),
        # [R2] O23: the fast aggregate's verdict step, the one conversion of
        # four job results into the required context. Each arm leaves every
        # job key and the selector's whole publication path canonical.
        ("O23 fast verdict step if: false",
         set_step_key(fast_verdict_step, "if", False),
         "verdict step must carry no `if`"),
        ("O23b fast verdict lint result rebound to the literal success",
         set_env_key(fast_verdict_step, "VERILATOR_LINT_RESULT", "success"),
         "must bind `VERILATOR_LINT_RESULT`"),
        ("O23c fast verdict case widened to accept failure",
         m_fast_verdict_case_widened,
         "verdict step script is not the canonical form"),
        ("O23d fast verdict step continue-on-error",
         set_step_key(fast_verdict_step, "continue-on-error", True),
         "verdict step must carry no `continue-on-error`"),
        ("O23e fast verdict step shell: bash -n",
         set_step_key(fast_verdict_step, "shell", "bash -n {0}"),
         "verdict step must carry no `shell`"),
        # [R2] O24: the aggregate's `needs` universe. Membership in that list
        # is what puts a fast job's result inside the verdict at all.
        ("O24 fast aggregate drops bdd-conformance from its verdict",
         m_fast_aggregate_forgets_bdd, "missing: bdd-conformance"),
        ("O24b a new fast job lands outside the aggregate's needs",
         m_fast_new_unaggregated_job, "missing: extra-check"),
        # [R2] O25: a gate contributor that does not need the selector,
        # exactly bdd-conformance's shape, held to run as written.
        ("O25 bdd-conformance job if: false",
         set_job_if(RTL_FAST, "bdd-conformance", False),
         "job `bdd-conformance` must carry no `if`"),
        ("O25b bdd-conformance continue-on-error",
         set_job_key_at(RTL_FAST, "bdd-conformance",
                        "continue-on-error", True),
         "job `bdd-conformance` must carry no `continue-on-error`"),
        ("O25c bdd-conformance defaults.run.shell bash -n",
         set_job_key_at(RTL_FAST, "bdd-conformance", "defaults",
                        {"run": {"shell": "bash -n {0}"}}),
         "job `bdd-conformance` must carry no `defaults`"),
        # [R2] O26: a `.result` chain read from a job outside `needs` is the
        # same empty string O22 refuses for `.outputs.`, in the spelling the
        # fast verdict itself uses four lines from its accept case.
        ("O26 a .result read from a job outside needs",
         m_fast_bdd_needs_expression(
             "${{ needs.changes.result == 'success' }}"),
         "must list `changes` in its `needs`"),
        ("O26b the bracket spelling of the same .result read",
         m_fast_bdd_needs_expression(
             "${{ needs['changes']['result'] == 'success' }}"),
         "must list `changes` in its `needs`"),
        # [R2] O27: the public required name carried by a second job.
        ("O27 verilator-lint renamed to the public name rtl-fast",
         m_fast_lint_masquerades_as_aggregate,
         "carried by exactly one job"),
        # [R2] O28: a job-level env on the fast selector reaches the scope
        # script without appearing in the pinned step.
        ("O28 fast selector job-level env EVENT_NAME literal",
         set_job_key_at(RTL_FAST, FAST_SELECTOR_JOB, "env",
                        {"EVENT_NAME": "pull_request"}),
         "must carry no `env`"),
        # #209 O9 / #268: the portable matrix carrier is mandatory, equals
        # the shard-list size, and every consumer derives from it.
        ("O9 matrix total carrier is missing", m_shard_total_missing,
         "shard denominator matrix `total`"),
        ("O9a matrix total disagrees with the shard list", m_shard_total_wrong,
         "shard denominator matrix `total`"),
        ("O9 verilator matrix grows, the denominator is a literal",
         m_shard_denominator_stale, "shard denominator"),
        ("O9b yosys denominator below its matrix size",
         m_shard_denominator_wrong, "shard denominator"),
        ("O9c a worker name restates a stale denominator", m_shard_name_stale,
         "name: the shard denominator"),
        ("O9d sharded matrix adds an include expansion", m_shard_matrix_include,
         "must not define `include` or `exclude`"),
        ("O9e sharded matrix excludes a worker", m_shard_matrix_exclude,
         "must not define `include` or `exclude`"),
        ("rtl public name verilator-suites renamed",
         m_rename_job(RTL_FULL, "verilator-suites"), "`verilator-suites`"),
        ("rtl public name yosys-portability renamed",
         m_rename_job(RTL_FULL, "yosys-portability"), "`yosys-portability`"),
        # rtl-fast.yml
        ("fast push on main, not dev", m_push_main(RTL_FAST), "push must subscribe"),
        ("fast PR type missing", m_pr_type_missing(RTL_FAST), "pull_request.types"),
        ("fast cancel-in-progress false", m_cancel_false(RTL_FAST),
         "cancel-in-progress"),
        ("fast public name rtl-fast renamed", m_rename_job(RTL_FAST, "rtl-fast"),
         "`rtl-fast`"),
        # #245: the ooc.sh refusal self-test's pinned invocation.
        ("#245 ooc.sh self-test step removed", m_ooc_selftest_removed,
         "exactly one step must run"),
        ("#245 ooc.sh self-test neutralised", m_ooc_selftest_neutralised,
         "exactly one step must run"),
        ("#245 ooc.sh self-test before the submodule fetch",
         m_ooc_selftest_before_fetch, "must run after a"),
        ("#245 ooc.sh self-test fetch stops naming protocol-processor",
         m_ooc_selftest_fetch_drops_submodule("protocol-processor"),
         "must run after a"),
        ("#245 ooc.sh self-test fetch stops naming gptp-processor",
         m_ooc_selftest_fetch_drops_submodule("gptp-processor"),
         "must run after a"),
        ("#245 ooc.sh self-test disabled by if: false",
         m_ooc_selftest_key("if", False), "beyond name/run"),
        ("#245 ooc.sh self-test failure swallowed by continue-on-error",
         m_ooc_selftest_key("continue-on-error", True), "beyond name/run"),
        ("#245 ooc.sh self-test reinterpreted by shell: bash -n",
         m_ooc_selftest_key("shell", "bash -n {0}"), "beyond name/run"),
        # docs.yml
        ("docs push on main, not dev", m_push_main(DOCS), "push must subscribe"),
        ("docs no pull_request", m_drop_pr(DOCS), "must subscribe pull_request"),
        ("docs does not run --check", m_docs_no_check, "--check"),
        ("docs does not run --selftest", m_docs_no_selftest, "--selftest"),
        ("docs drops the local act runner self-test",
         m_docs_no_act_selftest, ACT_CI_SELFTEST),
        ("docs disables the local act runner self-test",
         m_docs_act_selftest_key("if", False), "must carry no `if`"),
        ("docs swallows a local act runner self-test failure",
         m_docs_act_selftest_key("continue-on-error", True),
         "must carry no `continue-on-error`"),
        ("docs only parses the local act runner self-test",
         m_docs_act_selftest_key("shell", "bash -n {0}"),
         "must carry no `shell`"),
        ("docs builder omits verilog-axis",
         m_builder_drop_submodule(DOCS, "docs-check",
                                  "third_party/verilog-axis"),
         "must initialize `third_party/verilog-axis`"),
        ("docs builder omits protocol-processor",
         m_builder_drop_submodule(DOCS, "docs-check", "protocol-processor"),
         "must initialize `protocol-processor`"),
        ("docs builder omits gptp-processor",
         m_builder_drop_submodule(DOCS, "docs-check", "gptp-processor"),
         "must initialize `gptp-processor`"),
        ("docs builder initializes submodules after the call",
         m_builder_checkout_after_call(DOCS, "docs-check"),
         "must initialize builder submodules before"),
        ("docs builder initializes submodules before repository checkout",
         m_builder_checkout_before_repo(DOCS, "docs-check"),
         "must check out the repository before"),
        ("docs builder checkout overrides the event SHA",
         m_builder_checkout_key(DOCS, "docs-check", "with", {"ref": "dev"}),
         "checkout step must be exactly"),
        ("docs builder checkout is disabled",
         m_builder_checkout_key(DOCS, "docs-check", "if", False),
         "checkout step must be exactly"),
        ("docs builder checkout action version drifts",
         m_builder_checkout_version(DOCS, "docs-check"),
         "checkout step must be exactly"),
        ("docs builder replaced by env decoy",
         m_builder_decoy_env(DOCS, "docs-check"),
         f"must call `{BUILDER_CALL}` exactly once"),
        ("docs builder call continue-on-error",
         m_builder_continue_on_error(DOCS, "docs-check"),
         "must carry no `continue-on-error`"),
        ("docs builder job defaults.run.shell bash -n",
         m_builder_job_defaults(DOCS, "docs-check"),
         "must carry no `defaults`"),
        ("docs builder workflow defaults.run.shell bash -n",
         m_builder_top_defaults(DOCS),
         "must carry no top-level `defaults`"),
        ("docs sv2v install dropped",
         m_sv2v_dropped(DOCS, "docs-check"),
         "must install the pinned sv2v front end exactly once"),
        ("docs sv2v version drifts off the pin",
         m_sv2v_unpinned(DOCS, "docs-check"),
         "exactly the pinned v0.0.12 release script"),
        ("docs sv2v installed after the builder call",
         m_sv2v_after_call(DOCS, "docs-check"),
         "must install sv2v before calling"),
        ("#261 `docs-check` job if: false",
         m_job_key(DOCS, "docs-check", "if", False),
         "job `docs-check` must carry no `if`"),
        ("#261 `docs-check` job continue-on-error",
         m_job_key(DOCS, "docs-check", "continue-on-error", True),
         "job `docs-check` must carry no `continue-on-error`"),
        ("#261 `docs-check` job needs a sibling",
         m_job_key(DOCS, "docs-check", "needs", ["wire-accountability"]),
         "job `docs-check` must carry no `needs`"),
        ("#261 a second job carries `docs-check`",
         m_second_carrier(DOCS, "docs-check"),
         "`docs-check` must be carried by exactly one job (carried by ['docs-check', 'decoy']"),
        ("#261 `docs-check` renamed",
         m_rename_job(DOCS, "docs-check"),
         "`docs-check` must be carried by exactly one job (carried by none"),
        ("#261 `docs-check` renamed away while a stub takes the name",
         m_swap_carrier(DOCS, "docs-check"),
         "required context `docs-check` must be carried by the job of that id"),
        ("#261 `wire-accountability` job if: false",
         m_job_key(DOCS, "wire-accountability", "if", False),
         "job `wire-accountability` must carry no `if`"),
        ("#261 `wire-accountability` job continue-on-error",
         m_job_key(DOCS, "wire-accountability", "continue-on-error", True),
         "job `wire-accountability` must carry no `continue-on-error`"),
        ("#261 `wire-accountability` job needs a sibling",
         m_job_key(DOCS, "wire-accountability", "needs", ["docs-check"]),
         "job `wire-accountability` must carry no `needs`"),
        ("#261 `wire-accountability` job defaults.run.shell bash -n",
         m_job_key(DOCS, "wire-accountability", "defaults", {"run": {"shell": "bash -n {0}"}}),
         "job `wire-accountability` must carry no `defaults`"),
        ("#261 a second job carries `wire-accountability`",
         m_second_carrier(DOCS, "wire-accountability"),
         "`wire-accountability` must be carried by exactly one job (carried by ['wire-accountability', 'decoy']"),
        ("#261 `wire-accountability` renamed",
         m_rename_job(DOCS, "wire-accountability"),
         "`wire-accountability` must be carried by exactly one job (carried by none"),
        ("#261 `wire-accountability` renamed away while a stub takes the name",
         m_swap_carrier(DOCS, "wire-accountability"),
         "required context `wire-accountability` must be carried by the job of that id"),
        ("#261 `docs-check-no-git` job if: false",
         m_job_key(DOCS, "docs-check-no-git", "if", False),
         "job `docs-check-no-git` must carry no `if`"),
        ("#261 `docs-check-no-git` job continue-on-error",
         m_job_key(DOCS, "docs-check-no-git", "continue-on-error", True),
         "job `docs-check-no-git` must carry no `continue-on-error`"),
        ("#261 `docs-check-no-git` job needs a sibling",
         m_job_key(DOCS, "docs-check-no-git", "needs", ["docs-check"]),
         "job `docs-check-no-git` must carry no `needs`"),
        ("#261 `docs-check-no-git` job defaults.run.shell bash -n",
         m_job_key(DOCS, "docs-check-no-git", "defaults", {"run": {"shell": "bash -n {0}"}}),
         "job `docs-check-no-git` must carry no `defaults`"),
        ("#261 a second job carries `docs-check-no-git`",
         m_second_carrier(DOCS, "docs-check-no-git"),
         "`docs-check-no-git` must be carried by exactly one job (carried by ['docs-check-no-git', 'decoy']"),
        ("#261 `docs-check-no-git` renamed",
         m_rename_job(DOCS, "docs-check-no-git"),
         "`docs-check-no-git` must be carried by exactly one job (carried by none"),
        ("#261 `docs-check-no-git` renamed away while a stub takes the name",
         m_swap_carrier(DOCS, "docs-check-no-git"),
         "required context `docs-check-no-git` must be carried by the job of that id"),
        # elaborate.yml
        ("elaborate push on main, not dev", m_push_main(ELABORATE),
         "push must subscribe"),
        ("elaborate public name renamed", m_rename_job(ELABORATE, "elaborate"),
         "`elaborate`"),
        ("elaborate builder omits verilog-axis",
         m_builder_drop_submodule(ELABORATE, "elaborate",
                                  "third_party/verilog-axis"),
         "must initialize `third_party/verilog-axis`"),
        ("elaborate builder omits protocol-processor",
         m_builder_drop_submodule(ELABORATE, "elaborate", "protocol-processor"),
         "must initialize `protocol-processor`"),
        ("elaborate builder omits gptp-processor",
         m_builder_drop_submodule(ELABORATE, "elaborate", "gptp-processor"),
         "must initialize `gptp-processor`"),
        ("elaborate builder initializes submodules before repository checkout",
         m_builder_checkout_before_repo(ELABORATE, "elaborate"),
         "must check out the repository before"),
        ("elaborate builder checkout overrides the event SHA",
         m_builder_checkout_key(ELABORATE, "elaborate", "with",
                                {"fetch-depth": 0, "ref": "dev"}),
         "checkout step must be exactly"),
        ("elaborate builder checkout is disabled",
         m_builder_checkout_key(ELABORATE, "elaborate", "if", False),
         "checkout step must be exactly"),
        ("elaborate builder checkout moves the tree",
         m_builder_checkout_key(ELABORATE, "elaborate", "with",
                                {"fetch-depth": 0, "path": "elsewhere"}),
         "checkout step must be exactly"),
        ("elaborate builder replaced by env decoy",
         m_builder_decoy_env(ELABORATE, "elaborate"),
         f"must call `{BUILDER_CALL}` exactly once"),
        ("elaborate builder call continue-on-error",
         m_builder_continue_on_error(ELABORATE, "elaborate"),
         "must carry no `continue-on-error`"),
        ("elaborate builder job defaults.run.shell bash -n",
         m_builder_job_defaults(ELABORATE, "elaborate"),
         "must carry no `defaults`"),
        ("elaborate builder workflow defaults.run.shell bash -n",
         m_builder_top_defaults(ELABORATE),
         "must carry no top-level `defaults`"),
        ("elaborate builder checkout and call both disabled",
         m_builder_both_if_false, "builder checkout `if` must be exactly"),
        ("elaborate sv2v install dropped",
         m_sv2v_dropped(ELABORATE, "elaborate"),
         "must install the pinned sv2v front end exactly once"),
        ("elaborate sv2v version drifts off the pin",
         m_sv2v_unpinned(ELABORATE, "elaborate"),
         "exactly the pinned v0.0.12 release script"),
        ("elaborate sv2v install disabled by if",
         m_sv2v_if_disabled, "sv2v install `if` must be exactly"),
        ("#261 `elaborate` job if: false",
         m_job_key(ELABORATE, "elaborate", "if", False),
         "job `elaborate` must carry no `if`"),
        ("#261 `elaborate` job continue-on-error",
         m_job_key(ELABORATE, "elaborate", "continue-on-error", True),
         "job `elaborate` must carry no `continue-on-error`"),
        ("#261 `elaborate` job needs another job",
         m_job_key(ELABORATE, "elaborate", "needs", ["noop"]),
         "job `elaborate` must carry no `needs`"),
        ("#261 a second job carries `elaborate`",
         m_second_carrier(ELABORATE, "elaborate"),
         "`elaborate` must be carried by exactly one job (carried by ['elaborate', 'decoy']"),
        ("#261 `elaborate` renamed away while a stub takes the name",
         m_swap_carrier(ELABORATE, "elaborate"),
         "required context `elaborate` must be carried by the job of that id"),
        # An expression-valued display name, one arm per file ([R4] on #293).
        ("#261 docs decoy named by an expression",
         m_expression_carrier(DOCS, "docs-check"),
         "job `decoy` `name` must be a literal or reference only"),
        ("#261 elaborate decoy named by an expression",
         m_expression_carrier(ELABORATE, "elaborate"),
         "job `decoy` `name` must be a literal or reference only"),
        ("#261 rtl-fast decoy named by an expression",
         m_expression_carrier(RTL_FAST, "rtl-fast"),
         "job `decoy` `name` must be a literal or reference only"),
        ("#261 rtl-full decoy named by an expression",
         m_expression_carrier(RTL_FULL, "verilator-suites"),
         "job `decoy` `name` must be a literal or reference only"),
        ("#261 docs decoy renders a required name from its own matrix",
         m_matrix_carrier(DOCS, "docs-check"),
         "job `decoy` `name` renders `docs-check` for one matrix combination"),
        ("#261 rtl-full decoy renders a required name from its own matrix",
         m_matrix_carrier(RTL_FULL, "yosys-portability"),
         "job `decoy` `name` renders `yosys-portability` for one matrix combination"),
    ]


def _run_mutations(checker, pristine):
    """Apply every arm to a deep copy and require `checker` to name the
    expected fragment. Returns the list of arms that did NOT bite."""
    misses = []
    for name, mutate, want in _mutations():
        world = copy.deepcopy(pristine)
        mutate(world)
        findings = checker(world)
        if not any(want in f for f in findings):
            misses.append(f"[{name}] expected a finding naming {want!r}, got "
                          f"{findings or 'no findings'}")
    return misses


def selftest(root):
    problems = []
    checked_arms = 0

    # The pristine tree is clean, and the contract is non-trivial.
    try:
        pristine = parse_world(read_tree(root))
    except CannotRun as exc:
        print(f"selftest: cannot load the pristine tree: {exc}")
        return RC_CANNOT_RUN
    clean = check(pristine)
    if clean.findings:
        problems.append("pristine tree is not clean: " +
                        "; ".join(clean.findings))
    if clean.checked < 30:
        problems.append(f"only {clean.checked} contract item(s) checked; the "
                        "contract has shrunk")

    # Every arm bites, one item at a time.
    real = lambda w: check(w).findings  # noqa: E731
    misses = _run_mutations(real, pristine)
    arms = _mutations()
    checked_arms += len(arms)
    for m in misses:
        problems.append("mutation not caught: " + m)
    for name, _, _ in arms:
        if not any(name in m for m in misses):
            print(f"  ok   caught: {name}")

    # Vacuity: a checker stubbed to find nothing must fail every arm above.
    stubbed = _run_mutations(lambda w: [], pristine)
    if len(stubbed) != len(arms):
        problems.append(f"vacuity: a stub checker failed only {len(stubbed)} "
                        f"of {len(arms)} arms; the arms do not depend on the "
                        "checker")
    else:
        print(f"  ok   vacuity: a stub that finds nothing fails all {len(arms)} arms")

    # Inputs the check cannot judge are rc 2, never a pass.
    for name, world in (
        ("missing rtl.yml", {k: v for k, v in read_tree(root).items()
                             if k != RTL_FULL}),
        ("unparseable rtl.yml", dict(read_tree(root), **{RTL_FULL: "on: [\n"})),
        ("scalar rtl.yml", dict(read_tree(root), **{RTL_FULL: "just text\n"})),
    ):
        try:
            parse_world(world)
        except CannotRun:
            print(f"  ok   cannot-run: {name}")
            checked_arms += 1
        else:
            problems.append(f"{name} was accepted instead of refused")

    # --require-target-sha arms, over a temporary directory.
    sha = "0123456789abcdef0123456789abcdef01234567"
    other = "fedcba9876543210fedcba9876543210fedcba98"
    with tempfile.TemporaryDirectory() as td:
        base = pathlib.Path(td)

        def shards(n, content=sha + "\n"):
            roots = []
            for i in range(n):
                d = base / f"suite-logs-{i}"
                d.mkdir(exist_ok=True)
                (d / RECORD).write_text(content)
                (d / f"suite{i}.log").write_text("checks: 1\n")
                roots.append(d)
            return roots

        three = dict(gate=sha, run=sha, checkout=sha)
        cases = []
        roots = shards(4)
        f, _ = check_records(three, roots, 4)
        cases.append(("four matching records with --expect 4 pass", not f))
        f, _ = check_records(three, roots[:3], 4)
        cases.append(("three of four shard directories are refused",
                      any("expected 4" in x and "found 3" in x for x in f)))
        f, _ = check_records(three, roots, 3)
        cases.append(("a surplus shard directory is refused",
                      any("expected 3" in x and "found 4" in x for x in f)))
        try:
            check_records(three, roots, None)
        except CannotRun:
            cases.append(("a missing --expect cannot run", True))
        else:
            cases.append(("a missing --expect cannot run", False))
        (roots[2] / RECORD).unlink()
        f, _ = check_records(three, roots, 4)
        cases.append(("a missing record is refused and named",
                      any("suite-logs-2" in x and "missing" in x for x in f)))
        roots = shards(4)
        (roots[1] / RECORD).write_text(other + "\n")
        f, _ = check_records(three, roots, 4)
        cases.append(("a record for another tree is refused",
                      any("suite-logs-1" in x and other in x for x in f)))
        (roots[1] / RECORD).write_text("not-a-sha\n")
        f, _ = check_records(three, roots, 4)
        cases.append(("a malformed record is refused",
                      any("not a commit id" in x for x in f)))
        roots = shards(4)
        f, _ = check_records(dict(gate=sha, run=other, checkout=sha), roots, 4)
        cases.append(("gate/run disagreement is refused",
                      any("disagree" in x for x in f)))
        f, _ = check_records(dict(gate=sha, run=sha, checkout=""), roots, 4)
        cases.append(("an empty source SHA is refused",
                      any("checkout" in x and "not a 40-digit" in x for x in f)))
        f, _ = check_records(three, [], 4)
        cases.append(("no shard directory at all is refused, not skipped",
                      any("produced nothing" in x for x in f)
                      and any("found 0" in x for x in f)))
        none = base / "none"
        none.mkdir()
        f, _ = check_records(three, [none], 1)
        cases.append(("the empty placeholder directory is refused",
                      any("none" in x and "missing" in x for x in f)))
        roots = shards(4)
        f, _ = check_records(dict(gate=sha, run=sha), roots, 4)
        cases.append(("a dropped checkout source is refused",
                      any("missing: checkout" in x for x in f)))
        f, _ = check_records(dict(run=sha, checkout=sha), roots, 4)
        cases.append(("a dropped gate source is refused",
                      any("missing: gate" in x for x in f)))
        f, _ = check_records(dict(gate=sha), roots, 4)
        cases.append(("a lone gate source is refused",
                      any("missing: run, checkout" in x for x in f)))
        f, _ = check_records({}, roots, 4)
        cases.append(("no source at all is refused",
                      any("missing: gate, run, checkout" in x for x in f)))
        f, _ = check_records(dict(three, extra=sha), roots, 4)
        cases.append(("an unknown source label is refused",
                      any("unknown: extra" in x for x in f)))
        for name, ok in cases:
            checked_arms += 1
            if ok:
                print(f"  ok   records: {name}")
            else:
                problems.append(f"records arm failed: {name}")

    # The canonical pin is whitespace-invariant: re-indenting and continuing
    # the same three lines differently is the same script and must pass.
    world = copy.deepcopy(pristine)
    for s in steps(jobs(world[RTL_FULL])[GATE_JOB]):
        if DEFAULT_BRANCH_FLAG in step_text(s):
            s["run"] = ("  set   -euo pipefail\n\n"
                        f"  {CANONICAL_OBSERVED}\n"
                        "  python3 scripts/ci_events.py \\\n"
                        "    --require-default-branch \\\n"
                        '    --event "$GITHUB_EVENT_NAME" \\\n'
                        '    --observed "$observed"\n')
    for s in steps(jobs(world[RTL_FULL])[GATE_JOB]):
        if s.get("id") == DECIDE_STEP_ID:
            s["run"] = "\n".join("   " + l if l.strip() else ""
                                  for l in s["run"].splitlines()) + "\n"
    for s in steps(jobs(world[RTL_FAST])[FAST_SELECTOR_JOB]):
        if s.get("id") == FAST_SCOPE_STEP_ID:
            s["run"] = "\n".join("   " + l if l.strip() else ""
                                  for l in s["run"].splitlines()) + "\n"
    for s in steps(jobs(world[RTL_FAST])["rtl-fast"]):
        if isinstance(s.get("run"), str):
            s["run"] = "\n".join("   " + l if l.strip() else ""
                                  for l in s["run"].splitlines()) + "\n"
    for s in steps(jobs(world[RTL_FULL])["yosys-portability"]):
        if VERIFY_FLAG in step_text(s):
            s["run"] = ("shopt   -s nullglob\n"
                        'roots=("$RUNNER_TEMP"/all-yosys-results/yosys-results-*)\n'
                        "python3 scripts/ci_events.py \\\n"
                        "  --require-target-sha --expect 4 \\\n"
                        '  --sha gate="$GATE_SHA" \\\n'
                        '  --sha run="$GITHUB_SHA" \\\n'
                        '  --sha checkout="$(git rev-parse HEAD)" \\\n'
                        '  -- "${roots[@]}"\n')
    checked_arms += 1
    if check(world).findings:
        problems.append("whitespace-only reformatting of the canonical scripts "
                        f"was refused: {check(world).findings}")
    else:
        print("  ok   canonical pins are whitespace-invariant (assert step, "
              "decision step, fast scope step, fast verdict step and "
              "verifier step)")

    # --require-default-branch arms: the decision for every event class. An
    # inverted or weakened comparison fails one of these, which is what makes
    # the YAML shape checks above worth having.
    def refuses(event, observed):
        f, _ = check_default_branch(event, observed)
        return bool(f) and any(observed in x or "<empty>" in x for x in f)

    def passes(event, observed):
        f, _ = check_default_branch(event, observed)
        return not f

    def warns(event, observed):
        f, lines = check_default_branch(event, observed)
        return not f and any("WARNING" in x for x in lines)

    db_cases = [
        ("schedule on dev passes", passes("schedule", PUSH_BRANCH)),
        ("dispatch on dev passes", passes("workflow_dispatch", PUSH_BRANCH)),
        ("schedule on main refuses, naming main", refuses("schedule", "main")),
        ("dispatch on main refuses", refuses("workflow_dispatch", "main")),
        ("schedule with an unreadable value refuses",
         refuses("schedule", "unreadable")),
        ("schedule with an empty value refuses", refuses("schedule", "")),
        ("schedule with surrounding whitespace still passes",
         passes("schedule", f" {PUSH_BRANCH}\n")),
        ("pull_request on main warns and continues",
         warns("pull_request", "main")),
        ("push on main warns and continues", warns("push", "main")),
    ]
    try:
        check_default_branch("", PUSH_BRANCH)
    except CannotRun:
        db_cases.append(("a missing event cannot run", True))
    else:
        db_cases.append(("a missing event cannot run", False))
    for name, ok in db_cases:
        checked_arms += 1
        if ok:
            print(f"  ok   default-branch: {name}")
        else:
            problems.append(f"default-branch arm failed: {name}")

    if problems:
        for p in problems:
            print("  FAIL " + p)
        print(f"selftest: {len(problems)} FAILURE(S)")
        return RC_FINDING
    print(f"selftest: PASS ({clean.checked} contract items, {checked_arms} "
          "arms)")
    return RC_OK


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def run_check(root):
    try:
        c = check(parse_world(read_tree(root)))
    except CannotRun as exc:
        print(f"ci_events: cannot run: {exc}")
        return RC_CANNOT_RUN
    for note in c.notes:
        print("  note " + note)
    for f in c.findings:
        print("  FAIL " + f)
    if c.findings:
        print(f"ci_events: {len(c.findings)} finding(s) over {c.checked} "
              "contract item(s)")
        return RC_FINDING
    print(f"ci_events: OK ({c.checked} contract item(s) across "
          f"{len(WORKFLOWS)} workflow files and {POLICY})")
    return RC_OK


def run_require(sha_args, roots, expect):
    shas = {}
    for arg in sha_args:
        if "=" not in arg:
            print(f"ci_events: --sha expects label=sha, got {arg!r}")
            return RC_CANNOT_RUN
        label, value = arg.split("=", 1)
        if label in shas:
            print(f"ci_events: --sha {label} given twice")
            return RC_CANNOT_RUN
        shas[label] = value.strip()
    try:
        findings, lines = check_records(shas, [pathlib.Path(r) for r in roots],
                                        expect)
    except CannotRun as exc:
        print(f"ci_events: cannot run: {exc}")
        return RC_CANNOT_RUN
    for line in lines:
        print(line)
    for f in findings:
        print("  FAIL " + f)
    return RC_FINDING if findings else RC_OK


def run_require_default_branch(event, observed):
    try:
        findings, lines = check_default_branch(event, observed)
    except CannotRun as exc:
        print(f"ci_events: cannot run: {exc}")
        return RC_CANNOT_RUN
    for line in lines:
        print(line)
    for f in findings:
        print("  FAIL " + f)
    return RC_FINDING if findings else RC_OK


def main(argv):
    parser = argparse.ArgumentParser(
        description="Hold the CI workflow files to their documented event "
                    "and SHA contract.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true",
                      help="the live tree against the contract")
    mode.add_argument("--selftest", action="store_true",
                      help="mutation arms over in-memory copies")
    mode.add_argument("--require-target-sha", action="store_true",
                      help="verify every shard's TARGET_SHA record")
    mode.add_argument("--require-default-branch", action="store_true",
                      help="assert the live repository default branch for "
                           "the events it governs")
    parser.add_argument("--root", type=pathlib.Path, default=ROOT,
                        help="repository root (default: this script's)")
    parser.add_argument("--sha", action="append", default=[],
                        metavar="LABEL=SHA",
                        help="a source of the run's SHA (gate, run, checkout)")
    parser.add_argument("--expect", type=int, default=None, metavar="N",
                        help="shard directories the worker matrix produces "
                             "(--require-target-sha)")
    parser.add_argument("--event", default="",
                        help="GITHUB_EVENT_NAME (--require-default-branch)")
    parser.add_argument("--observed", default="",
                        help="the default branch gh api reported "
                             "(--require-default-branch)")
    parser.add_argument("roots", nargs="*",
                        help="shard evidence directories (--require-target-sha)")
    args = parser.parse_args(argv[1:])
    if args.check:
        return run_check(args.root)
    if args.selftest:
        return selftest(args.root)
    if args.require_default_branch:
        return run_require_default_branch(args.event, args.observed)
    return run_require(args.sha, args.roots, args.expect)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

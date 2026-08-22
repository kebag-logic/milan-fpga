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
a gate/run/checkout SHA that is not one value. A missing record is a failure,
never a skip. `--check` refuses any `actions/checkout` step in rtl.yml that
overrides `ref`, requires every artifact-uploading job to record the SHA and
every artifact-downloading job to verify it.

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
#: The gate job of the exhaustive workflow and the output it exports.
GATE_JOB = "full-ci-gate"
GATE_OUTPUT = "target_sha"
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
#: Public check names the merge bar reads (AGENTS.md section 7), per file.
PUBLIC_NAMES = {
    RTL_FULL: ("verilator-suites", "yosys-portability"),
    RTL_FAST: ("rtl-fast",),
    ELABORATE: ("elaborate",),
}

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
    names = {display_name(jid, j) for jid, j in jobs(wf).items()}
    for want in PUBLIC_NAMES.get(path, ()):
        c.item(want in names, path,
               f"public check name `{want}` must exist as a job (found "
               f"{sorted(names)})")


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
        outputs = gate.get("outputs")
        c.item(isinstance(outputs, dict) and GATE_OUTPUT in outputs, path,
               f"job `{GATE_JOB}` must export the `{GATE_OUTPUT}` output")
        prints = any("GITHUB_EVENT_NAME" in step_text(s)
                     and "GITHUB_SHA" in step_text(s) for s in steps(gate))
        c.item(prints, path, f"job `{GATE_JOB}` must print the event name and "
               "GITHUB_SHA in one step")
        check_default_branch_step(c, path, gate)

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
            verifies = any(VERIFY_FLAG in step_text(s) and ref in step_text(s)
                           and "ci_events.py" in step_text(s) for s in ss)
            c.item(verifies, path, f"job `{jid}` downloads evidence and must "
                   f"run scripts/ci_events.py {VERIFY_FLAG} against {ref}")
            needs = job.get("needs")
            needs = needs if isinstance(needs, list) else [needs]
            c.item(GATE_JOB in needs, path,
                   f"job `{jid}` must need `{GATE_JOB}` to read its output")


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
    env = step.get("env") if isinstance(step.get("env"), dict) else {}
    token = str(env.get("GH_TOKEN", "")).strip()
    c.item(token == "${{ github.token }}", path, "the default-branch step "
           f"must carry GH_TOKEN: ${{{{ github.token }}}} (found {token!r})")
    c.item("ci_events.py" in text and "gh api" in text
           and "$GITHUB_REPOSITORY" in text and ".default_branch" in text,
           path, "the default-branch step must read the live setting with "
           "gh api repos/$GITHUB_REPOSITORY --jq .default_branch")
    c.item('--event "$GITHUB_EVENT_NAME"' in text and "--observed" in text,
           path, "the default-branch step must pass --event "
           "\"$GITHUB_EVENT_NAME\" and --observed to the verifier")
    neutered = bool(step.get("continue-on-error")) or "|| true" in text
    c.item(not neutered, path, "the default-branch step must fail closed: "
           "no continue-on-error, no `|| true`")


def check_rtl_fast(c, wf):
    check_push_and_pr(c, RTL_FAST, wf, exact_types=True)
    check_cancel_in_progress(c, RTL_FAST, wf)
    check_public_names(c, RTL_FAST, wf)


def check_docs(c, wf):
    check_push_and_pr(c, DOCS, wf, exact_types=False)
    texts = [step_text(s) for j in jobs(wf).values() for s in steps(j)]
    for flag in ("--check", "--selftest"):
        wired = any(f"scripts/ci_events.py {flag}" in t for t in texts)
        c.item(wired, DOCS, f"must run `python3 scripts/ci_events.py {flag}` "
               "(this gate is not a gate unless a workflow runs it)")


def check_elaborate(c, wf):
    check_push_and_pr(c, ELABORATE, wf, exact_types=False)
    check_public_names(c, ELABORATE, wf)


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

def check_records(shas, roots):
    """`shas` maps a label (gate, run, checkout) to the SHA that source
    reports; `roots` are the downloaded shard directories. Returns
    (findings, lines): every finding is a refusal, lines are the verdict."""
    findings, lines = [], []
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
         f"`{GATE_OUTPUT}` output"),
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
        # docs.yml
        ("docs push on main, not dev", m_push_main(DOCS), "push must subscribe"),
        ("docs no pull_request", m_drop_pr(DOCS), "must subscribe pull_request"),
        ("docs does not run --check", m_docs_no_check, "--check"),
        ("docs does not run --selftest", m_docs_no_selftest, "--selftest"),
        # elaborate.yml
        ("elaborate push on main, not dev", m_push_main(ELABORATE),
         "push must subscribe"),
        ("elaborate public name renamed", m_rename_job(ELABORATE, "elaborate"),
         "`elaborate`"),
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
        f, _ = check_records(three, roots)
        cases.append(("four matching records pass", not f))
        (roots[2] / RECORD).unlink()
        f, _ = check_records(three, roots)
        cases.append(("a missing record is refused and named",
                      any("suite-logs-2" in x and "missing" in x for x in f)))
        roots = shards(4)
        (roots[1] / RECORD).write_text(other + "\n")
        f, _ = check_records(three, roots)
        cases.append(("a record for another tree is refused",
                      any("suite-logs-1" in x and other in x for x in f)))
        (roots[1] / RECORD).write_text("not-a-sha\n")
        f, _ = check_records(three, roots)
        cases.append(("a malformed record is refused",
                      any("not a commit id" in x for x in f)))
        roots = shards(4)
        f, _ = check_records(dict(gate=sha, run=other, checkout=sha), roots)
        cases.append(("gate/run disagreement is refused",
                      any("disagree" in x for x in f)))
        f, _ = check_records(dict(gate=sha, run=sha, checkout=""), roots)
        cases.append(("an empty source SHA is refused",
                      any("checkout" in x and "not a 40-digit" in x for x in f)))
        f, _ = check_records(three, [])
        cases.append(("no shard directory at all is refused, not skipped",
                      any("produced nothing" in x for x in f)))
        none = base / "none"
        none.mkdir()
        f, _ = check_records(three, [none])
        cases.append(("the empty placeholder directory is refused",
                      any("none" in x and "missing" in x for x in f)))
        for name, ok in cases:
            checked_arms += 1
            if ok:
                print(f"  ok   records: {name}")
            else:
                problems.append(f"records arm failed: {name}")

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


def run_require(sha_args, roots):
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
    if not shas:
        print("ci_events: --require-target-sha needs at least one --sha label=sha")
        return RC_CANNOT_RUN
    findings, lines = check_records(shas, [pathlib.Path(r) for r in roots])
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
    return run_require(args.sha, args.roots)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

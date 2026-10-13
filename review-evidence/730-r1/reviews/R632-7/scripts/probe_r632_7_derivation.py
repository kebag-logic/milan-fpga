#!/usr/bin/env python3
"""Reviewer probe R632-7-D: derivation, refusal order, dry-run lines and range widths.

Usage: python3 -I probe_r632_7_derivation.py <tree>

D1  job_container_width against an independent oracle of act 0.2.89
    (pkg/model/workflow.go GetMaxParallel, pkg/runner/runner.go maxParallel,
    pkg/common/executor.go NewParallelExecutor floor), for literal shapes the
    runner accepts; every non-literal shape must be a Refusal.
D2  replay_container_concurrency over workflow files written to disk, for
    CONCURRENT_JOB_LIMIT 1..3, against the oracle (sum of the limit's widest).
D3  through the real run_validation dry-run path (GitHub, git, the slot daemon
    and the Docker boundary stood in, as the self-test's dry_run_transcript
    does), with the PR checkout's rtl.yml edited: max-parallel 2 plans 2
    ranges (the checkout is read, not the runner's copy); max-parallel 5 and
    an expression are Refusals raised before the slot is entered and before
    any plan line; a 39-CPU host refuses slot 1 before the slot is entered.
D4  the dry-run plan lines of every shipping workflow in slot 0 and slot 3.
D5  every job and staging range of slots 0..63 is exactly 4 CPUs wide
    (nproc 4) and disjoint, and slot N's ranges lie inside 20N..20N+19.
Exits 0 only if every check holds.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import shutil
import sys
import tempfile
from dataclasses import replace
from unittest import mock

TREE = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("act_ci_r632_7_d", TREE / "scripts" / "act_ci.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
failures = 0


def check(label: str, ok: bool, evidence: str = "") -> None:
    global failures
    failures += 0 if ok else 1
    print(f"  {'ok  ' if ok else 'FAIL'} {label}" + (f" [{evidence}]" if evidence else ""))


def act_width(job: dict) -> int:
    """act 0.2.89: legs at once for one job, upper-bounded (leg count not read)."""
    strategy = job.get("strategy")
    if strategy is None or "matrix" not in strategy:
        return 1
    raw = strategy.get("max-parallel")
    parallel = 4 if raw is None else int(raw)
    return max(1, parallel)


MATRIX = {"matrix": {"n": ["1", "2", "3", "4", "5"]}}
literal_shapes = [
    {},
    {"strategy": {"fail-fast": "false"}},
    {"strategy": {"max-parallel": "7"}},
    {"strategy": dict(MATRIX)},
    *({"strategy": {**MATRIX, "max-parallel": text}} for text in ("0", "1", "2", "3", "4", "02", "000004", "9", "999999")),
]
answers = [(job, m.job_container_width(job, "j"), act_width(job)) for job in literal_shapes]
check(
    "D1 every literal shape derives act 0.2.89's width (no strategy/no matrix 1; matrix default 4; "
    "literal max-parallel floored at 1)",
    all(ours == theirs for _job, ours, theirs in answers),
    "; ".join(f"{job.get('strategy', {}).get('max-parallel', '-')}:{ours}/{theirs}" for job, ours, theirs in answers),
)
refused = []
for raw in ("${{ inputs.n }}", "-1", "+3", "1.0", "1234567", " 3", "3 ", "", "0x4", ["3"], {"a": "1"}):
    try:
        m.job_container_width({"strategy": {**MATRIX, "max-parallel": raw}}, "j")
        refused.append(False)
    except m.Refusal:
        refused.append(True)
try:
    m.job_container_width({"strategy": ["matrix"]}, "j")
    refused.append(False)
except m.Refusal:
    refused.append(True)
check("D1 every non-literal max-parallel and a non-mapping strategy are Refusals", all(refused), str(refused))

PLAIN = "    runs-on: ubuntu-latest\n    steps:\n      - run: true\n"


def job_text(name: str, parallel: str | None, matrix: bool = True) -> str:
    body = f"  {name}:\n{PLAIN}"
    if matrix:
        body += "    strategy:\n"
        if parallel is not None:
            body += f"      max-parallel: {parallel}\n"
        body += "      matrix:\n        n: [1, 2, 3, 4, 5, 6]\n"
    return body


sets = {
    "rtl-full": [("a", None), ("b", "2"), ("c", "3"), ("d", "1")],
    "rtl-fast": [("x", "3"), ("y", None, False)],
    "docs": [("only", None, False)],
    "elaborate": [("p", "2"), ("q", "2")],
}
with tempfile.TemporaryDirectory() as raw:
    root = pathlib.Path(raw)
    widths: dict[str, list[int]] = {}
    for workflow, jobs in sets.items():
        text = "".join(job_text(*job) for job in jobs)
        path = root / m.WORKFLOWS[workflow]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"name: {workflow}\non: pull_request\njobs:\n{text}", encoding="utf-8")
        widths[workflow] = sorted(
            (act_width({"strategy": {**MATRIX, **({} if j[1] is None else {"max-parallel": j[1]})}} if (len(j) < 3 or j[2]) else {}) for j in jobs),
            reverse=True,
        )
    mismatches = []
    for limit in (1, 2, 3):
        with mock.patch.object(m, "CONCURRENT_JOB_LIMIT", limit):
            for selection in (("rtl-full",), ("rtl-fast",), ("docs",), ("elaborate",), ("docs", "elaborate"),
                              ("elaborate", "rtl-fast"), ("rtl-fast", "rtl-full", "docs"), tuple(m.WORKFLOWS)):
                ours = m.replay_container_concurrency(root, selection)
                theirs = max(sum(widths[w][:limit]) for w in selection)
                if ours != theirs:
                    mismatches.append(f"limit {limit} {selection}: {ours} != {theirs}")
    check("D2 a run's concurrency is the most, over its workflows, of the limit's widest jobs summed", not mismatches,
          "; ".join(mismatches) or "24 selections x 3 limits")

fixture = m.selftest_fixture()
resolved = m.resolve_validation_base(
    fixture.pr, fixture.repository, query_tip=lambda *_a: fixture.live_tip, emit=lambda *_a: None
)


def dry_run(workflow: str, slot_number: int, rtl_text: str | None, cpus: int = 128) -> tuple[str, list[str]]:
    """Printed text and the order of (derivation-relevant) events of one dry run."""
    order: list[str] = []
    with tempfile.TemporaryDirectory() as raw:
        shipping = pathlib.Path(raw) / "shipping"
        for name in m.WORKFLOWS.values():
            (shipping / name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(TREE / name, shipping / name)

        def materialize(_run, layout):
            target = layout.checkout / m.WORKFLOWS[workflow]
            target.parent.mkdir(parents=True, exist_ok=True)
            source = (TREE / m.WORKFLOWS[workflow]).read_text(encoding="utf-8")
            target.write_text(rtl_text if rtl_text is not None else source, encoding="utf-8")
            return layout.checkout

        @contextlib.contextmanager
        def slot_entered(_selected, **_kwargs):
            order.append("slot entered")
            yield

        @contextlib.contextmanager
        def no_boundary(planned, **_kwargs):
            order.append("boundary")
            yield replace(planned, network_id="a" * 64, gateway="172.18.0.1",
                          toolcache_owned=True, toolcache_seeded=True)

        transcript = io.StringIO()
        slot = m.ReplaySlot(slot_number)
        with mock.patch.multiple(
            m,
            materialize_remote_head=materialize,
            validate_checkout=lambda *_a, **_k: None,
            initialize_required_submodules=lambda *_a, **_k: order.append("submodules"),
            require_live_pull_request=lambda *_a, **_k: None,
            inspect_docker_boundary=lambda *_a, **_k: None,
            replay_slot=slot_entered,
            temporary_docker_boundary=no_boundary,
            allocate_tcp_port=lambda: 43210,
            require_tool=m.fake_host_tool,
        ), mock.patch.object(m.os, "cpu_count", return_value=cpus), contextlib.redirect_stdout(transcript):
            try:
                rc = m.run_validation(resolved, (workflow,), shipping,
                                      launch=m.LaunchOptions("/trusted/act", slot.isolated, True, slot))
                print(f"rc={rc}")
            except m.Refusal as exc:
                order.append("refused")
                print(f"act-ci: REFUSED: {exc}")
    return transcript.getvalue(), order


shipping_rtl = (TREE / m.WORKFLOWS["rtl-full"]).read_text(encoding="utf-8")
anchor = "      fail-fast: false\n      matrix:\n        shard: [0, 1, 2, 3, 4]\n"
assert shipping_rtl.count(anchor) == 1, "rtl.yml anchor"


def edited(value: str) -> str:
    return shipping_rtl.replace(anchor, f"      fail-fast: false\n      max-parallel: {value}\n      matrix:\n        shard: [0, 1, 2, 3, 4]\n")


text, order = dry_run("rtl-full", 0, edited("2"))
check("D3 a checkout whose rtl.yml narrows max-parallel to 2 plans the shard jobs' widest (yosys 4): still 4",
      "up to 4 at once" in text and "rc=0" in text, text.splitlines()[-1])
narrow = shipping_rtl.replace(anchor, "      fail-fast: false\n      max-parallel: 2\n      matrix:\n        shard: [0, 1, 2, 3, 4]\n")
yosys = "      fail-fast: false\n      matrix:\n        shard: [0, 1, 2, 3]\n"
assert narrow.count(yosys) == 1, "yosys anchor"
narrow = narrow.replace(yosys, "      fail-fast: false\n      max-parallel: 2\n      matrix:\n        shard: [0, 1, 2, 3]\n")
text, order = dry_run("rtl-full", 3, narrow)
plan = [line for line in text.splitlines() if "job container CPUs" in line]
check("D3 the PR checkout's own workflows are read: both shard jobs at max-parallel 2 plan 2 ranges in slot 3",
      plan == ["act-ci: job container CPUs: up to 2 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on "
               "--cpuset-cpus=60-63, then moved to a free one of --cpuset-cpus=64-67 --cpuset-cpus=68-71"],
      repr(plan))
for label, rtl_text, slot_number, cpus, needle in (
    ("max-parallel 5", edited("5"), 1, 128, "run up to 5 job containers at once"),
    ("an expression max-parallel", edited("${{ github.run_number }}"), 1, 128, "is not a literal integer"),
    ("a 39-CPU host for slot 1", None, 1, 39, "needs CPUs 20-39"),
):
    text, order = dry_run("rtl-full", slot_number, rtl_text, cpus)
    check(f"D3 {label} is refused before the slot is entered, before submodules and before any plan line",
          order == ["refused"] and needle in text and "job container CPUs" not in text,
          f"order={order} {text.strip().splitlines()[-1][:160]}")

lines = {}
for slot_number in (0, 3):
    for workflow in m.WORKFLOWS:
        text, order = dry_run(workflow, slot_number, None)
        lines[(slot_number, workflow)] = [line for line in text.splitlines() if "job container CPUs" in line]
        lines[(slot_number, workflow, "cmd")] = [
            word
            for line in text.splitlines()
            if line.startswith(f"act-ci: {workflow}: ")
            for word in line.replace("'", " ").split()
            if word.startswith("--cpuset-cpus=")
        ]
        print(f"    slot {slot_number} {workflow}: {' | '.join(lines[(slot_number, workflow)])}; "
              f"act command: {' '.join(lines[(slot_number, workflow, 'cmd')])}")
expected_staging = {0: "0-3", 3: "60-63"}
ok = True
for slot_number in (0, 3):
    for workflow in m.WORKFLOWS:
        plan = [line for line in lines[(slot_number, workflow)] if "job container CPUs" in line]
        width = 4 if workflow == "rtl-full" else 1
        base = 20 * slot_number
        ranges = " ".join(f"--cpuset-cpus={base + 4 * (i + 1)}-{base + 4 * (i + 1) + 3}" for i in range(width))
        want = (f"act-ci: job container CPUs: up to {width} at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each "
                f"created on --cpuset-cpus={expected_staging[slot_number]}, then moved to a free one of {ranges}")
        ok = ok and plan == [want] and lines[(slot_number, workflow, "cmd")] == [f"--cpuset-cpus={expected_staging[slot_number]}"]
check("D4 every shipping workflow's dry run in slots 0 and 3 prints its derived ranges and an act command on staging", ok)

layout = []
with mock.patch.object(m.os, "cpu_count", return_value=20 * 64):
    for slot_number in range(m.SLOT_LIMIT + 1):
        layout.append((f"{slot_number} staging", m.container_cpuset(slot_number), slot_number))
        layout.extend((f"{slot_number} job {i}", text, slot_number)
                      for i, text in enumerate(m.job_cpu_ranges(slot_number, m.SLOT_JOB_RANGES)))
cpus: dict[int, str] = {}
problems = []
for owner, text, slot_number in layout:
    first, last = (int(part) for part in text.split("-"))
    if last - first + 1 != 4:
        problems.append(f"{owner} {text} is not 4 wide")
    if not (20 * slot_number <= first and last <= 20 * slot_number + 19):
        problems.append(f"{owner} {text} leaves its block")
    for cpu in range(first, last + 1):
        if cpu in cpus:
            problems.append(f"{owner} and {cpus[cpu]} share {cpu}")
        cpus[cpu] = owner
check("D5 slots 0..63: 320 ranges, each 4 CPUs (nproc 4), inside the slot's 20-CPU block, none sharing a CPU",
      not problems and len(layout) == 320, "; ".join(problems[:3]) or f"{len(layout)} ranges, {len(cpus)} CPUs")
print(f"probe_r632_7_derivation: {'PASS' if not failures else 'FAIL'} ({failures} failure(s))")
sys.exit(1 if failures else 0)

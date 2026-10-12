#!/usr/bin/env python3
"""Reviewer probes of the #730 CPU-range layout, derivation, event record and monitor.

Usage: python3 -I probes.py <exact-head tree>
Imports <tree>/scripts/act_ci.py read-only and prints one PROBE line per
check: PROBE <id> <OK|NOTE|BAD> <detail>. Nothing here starts Docker,
a daemon, sudo or act; process and Docker seams are stood in.
"""

import contextlib
import importlib.util
import io
import itertools
import json
import pathlib
import subprocess
import sys
import tempfile
import threading
import time
from unittest import mock

tree = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("act_ci_probe", tree / "scripts" / "act_ci.py")
act = importlib.util.module_from_spec(spec)
sys.modules["act_ci_probe"] = act
spec.loader.exec_module(act)


def emit(pid: str, ok: bool | None, detail: str) -> None:
    state = "OK" if ok is True else ("BAD" if ok is False else "NOTE")
    print(f"PROBE {pid} {state} {detail}", flush=True)


def cpus(text: str) -> set[int]:
    first, last = (int(part) for part in text.split("-"))
    return set(range(first, last + 1))


# P1: derivation from the shipping workflow files, per job.
for name, relative in act.WORKFLOWS.items():
    jobs = act.load_workflow(tree, relative)["jobs"]
    widths = {job_id: act.job_container_width(job, job_id) for job_id, job in jobs.items()}
    derived = act.replay_container_concurrency(tree, (name,))
    wide = {k: v for k, v in widths.items() if v != 1}
    emit("P1." + name, None, f"derived={derived} jobs={len(widths)} non-unit widths={wide}")
emit(
    "P1.all",
    act.replay_container_concurrency(tree, tuple(act.WORKFLOWS)) == 4,
    "all four shipping workflows together derive "
    f"{act.replay_container_concurrency(tree, tuple(act.WORKFLOWS))}",
)

# P1b: derivation reads the replayed checkout, not a constant: a planted
# checkout with max-parallel 2 / 5 / an expression / a YAML int-like string.
plain = "    runs-on: ubuntu-latest\n    steps:\n      - run: true\n"
for label, body, expect in (
    ("mp2", f"  a:\n{plain}    strategy:\n      max-parallel: 2\n      matrix:\n        n: [1, 2, 3]\n", 2),
    ("mp5", f"  a:\n{plain}    strategy:\n      max-parallel: 5\n      matrix:\n        n: [1, 2, 3, 4, 5]\n", "refuse-range"),
    ("expr", f"  a:\n{plain}    strategy:\n      max-parallel: ${{{{ fromJSON('2') }}}}\n      matrix:\n        n: [1]\n", "refuse-derive"),
    ("quoted", f"  a:\n{plain}    strategy:\n      max-parallel: '3'\n      matrix:\n        n: [1]\n", 3),
    ("null", f"  a:\n{plain}    strategy:\n      max-parallel:\n      matrix:\n        n: [1]\n", "refuse-derive"),
    ("two-wide-jobs", f"  a:\n{plain}    strategy:\n      matrix:\n        n: [1]\n  b:\n{plain}    strategy:\n      matrix:\n        n: [1]\n", 4),
):
    with tempfile.TemporaryDirectory() as raw:
        root = pathlib.Path(raw)
        path = root / act.WORKFLOWS["rtl-full"]
        path.parent.mkdir(parents=True)
        path.write_text(f"name: x\non: pull_request\njobs:\n{body}", encoding="utf-8")
        try:
            derived = act.replay_container_concurrency(root, ("rtl-full",))
        except act.Refusal as exc:
            emit("P1b." + label, expect == "refuse-derive", f"derive refused: {exc}")
            continue
        try:
            with mock.patch.object(act.os, "cpu_count", return_value=128):
                ranges = act.job_cpu_ranges(1, derived)
            emit("P1b." + label, derived == expect, f"derived={derived} slot1 ranges={ranges}")
        except act.Refusal as exc:
            emit("P1b." + label, expect == "refuse-range", f"derived={derived}; ranges refused: {exc}")

# P2: exhaustive layout over hosts, slots and concurrencies, independent of the
# self-test's own helper: every range a run can be given, across all pairs.
hosts = (1, 2, 3, 4, 5, 7, 8, 19, 20, 23, 24, 39, 40, 127, 128, 129, 1280)
bad = []
counted = 0
for host in hosts:
    with mock.patch.object(act.os, "cpu_count", return_value=host):
        layouts: dict[tuple[int, int], tuple[str, tuple[str, ...]]] = {}
        for slot in range(act.SLOT_LIMIT + 1):
            for conc in range(1, act.SLOT_JOB_RANGES + 1):
                try:
                    staging = act.container_cpuset(slot)
                    ranges = act.job_cpu_ranges(slot, conc)
                except act.Refusal:
                    if slot == 0:
                        bad.append(f"host {host}: slot 0 refused at concurrency {conc}")
                    continue
                layouts[(slot, conc)] = (staging, ranges)
                counted += 1
                block = set(range(20 * slot, 20 * slot + 20))
                every = [staging, *ranges]
                if any(not cpus(each) <= block for each in every):
                    bad.append(f"host {host} slot {slot} conc {conc}: a range leaves the 20N block")
                if any(max(cpus(each)) >= host for each in every):
                    bad.append(f"host {host} slot {slot} conc {conc}: a CPU beyond the host")
                if any(len(cpus(each)) != act.CONTAINER_CPU_LIMIT for each in ranges):
                    bad.append(f"host {host} slot {slot} conc {conc}: a job range not 4 wide")
                if len(ranges) not in (0, conc):
                    bad.append(f"host {host} slot {slot} conc {conc}: {len(ranges)} ranges")
                if slot and len(ranges) != conc:
                    bad.append(f"host {host} slot {slot} conc {conc}: isolated slot fell back")
                for a, b in itertools.combinations(every, 2):
                    if cpus(a) & cpus(b):
                        bad.append(f"host {host} slot {slot} conc {conc}: {a} meets {b}")
                if slot and len(cpus(staging)) != act.CONTAINER_CPU_LIMIT:
                    bad.append(f"host {host} slot {slot}: staging not 4 wide")
        for (sa, ca), (sb, cb) in itertools.combinations(layouts, 2):
            if sa == sb:
                continue
            ua = set().union(*(cpus(x) for x in [layouts[(sa, ca)][0], *layouts[(sa, ca)][1]]))
            ub = set().union(*(cpus(x) for x in [layouts[(sb, cb)][0], *layouts[(sb, cb)][1]]))
            if ua & ub:
                bad.append(f"host {host}: slot {sa}/{ca} meets slot {sb}/{cb}")
                break
emit("P2", not bad, f"{counted} admitted (host, slot, concurrency) layouts; problems: {bad[:5]}")
with mock.patch.object(act.os, "cpu_count", return_value=128):
    def admitted(slot: int, conc: int) -> bool:
        try:
            act.job_cpu_ranges(slot, conc)
            return True
        except act.Refusal:
            return False

    fit1 = [s for s in range(act.SLOT_LIMIT + 1) if admitted(s, 1)]
    fit4 = [s for s in range(act.SLOT_LIMIT + 1) if admitted(s, 4)]
emit("P2.128", fit4 == list(range(6)) and fit1 == list(range(7)),
     f"128-CPU host admits slots {fit4} at concurrency 4 and {fit1} at concurrency 1")

# P2b: a pre-#730 runner's slot k (4k..4k+3) beside this runner's ranges.
with mock.patch.object(act.os, "cpu_count", return_value=128):
    new0 = set().union(*(cpus(x) for x in ["0-3", *act.job_cpu_ranges(0, 4)]))
old = {k: set(range(4 * k, 4 * k + 4)) for k in range(1, 32)}
emit("P2b", None, "pre-#730 slots whose CPUs meet this runner's slot 0 at concurrency 4: "
     f"{[k for k, s in old.items() if s & new0]}")

# P3: the event record under orderings the self-test does not plant.
token = "f" * 32
boundary = mock.Mock()
boundary.token = token


def line(action: str, cid: str, owner: str = token) -> str:
    actor = {"ID": cid, "Attributes": {act.DOCKER_OWNER_LABEL: owner}}
    return json.dumps({"Type": "container", "Action": action, "Actor": actor})


ok_reply = subprocess.CompletedProcess([], 0, "", "")
ids = {n: n * 64 for n in "abcde"}

# P3.1 restart after die: the range is reused while the first holder runs again.
moves = []
rec = act.JobCpuRanges(boundary, ("4-7", "8-11"), lambda c, r: moves.append((c[0], r)) or ok_reply)
for ev in (("create", "a"), ("update", "a"), ("start", "a"), ("die", "a"), ("create", "b"),
           ("update", "b"), ("start", "b"), ("start", "a")):
    rec.observe(line(ev[0], ids[ev[1]]))
emit("P3.1", None, f"restart after die: moves={moves} held={{{', '.join(k[0] + ':' + str(v) for k, v in rec.held.items())}}} "
     f"started_on_staging={rec.started_on_staging} problems={rec.problems} "
     "(a restarted a would run on 4-7 beside b; act 0.2.89 runs with --rm and no restart policy)")

# P3.2 a move the CLI reports failed (timeout) but the daemon applied.
moves = []


def assign_timeout(cid: str, cpus_text: str):
    moves.append((cid[0], cpus_text))
    if cid[0] == "a":
        raise act.Refusal("job container CPU-range move timed out")
    return ok_reply


rec = act.JobCpuRanges(boundary, ("4-7", "8-11"), assign_timeout)
for ev in (("create", "a"), ("create", "b")):
    rec.observe(line(ev[0], ids[ev[1]]))
emit("P3.2", None, f"move timed out for a, then b created: moves={moves} problems={rec.problems} "
     "(if the daemon applied a's move, a and b share 4-7; the run prints a WARNING)")

# P3.3 duplicate create (a replayed --since line) counts twice, moves once.
moves = []
rec = act.JobCpuRanges(boundary, ("4-7", "8-11"), lambda c, r: moves.append((c[0], r)) or ok_reply)
for ev in (("create", "a"), ("create", "a")):
    rec.observe(line(ev[0], ids[ev[1]]))
emit("P3.3", len(moves) == 1, f"duplicate create: moves={moves} created={rec.created} moved={rec.moved}")

# P3.4 container gone before its move: created counts it, moved does not, and no warning.
rec = act.JobCpuRanges(boundary, ("4-7",), lambda c, r: subprocess.CompletedProcess([], 1, "", "Error: No such container: x\n"))
rec.observe(line("create", ids["a"]))
emit("P3.4", None, f"gone before move: summary='{rec.summary()}' problems={rec.problems}")

# P3.5 daemon order with die and destroy of a container never held.
rec = act.JobCpuRanges(boundary, ("4-7",), lambda c, r: ok_reply)
for ev in (("die", "a"), ("destroy", "a"), ("create", "b")):
    rec.observe(line(ev[0], ids[ev[1]]))
emit("P3.5", rec.held == {ids["b"]: 0} and rec.problems == [], f"stale die/destroy ignored; held b on 0")

# P3.6 the five-legs-over-four-ranges sequence of rtl.yml's five-shard job at width 4.
moves = []
rec = act.JobCpuRanges(boundary, ("4-7", "8-11", "12-15", "16-19"), lambda c, r: moves.append((c[0], r)) or ok_reply)
for n in "abcd":
    rec.observe(line("create", ids[n]))
    rec.observe(line("update", ids[n]))
    rec.observe(line("start", ids[n]))
rec.observe(line("die", ids["c"]))
rec.observe(line("destroy", ids["c"]))
rec.observe(line("create", ids["e"]))
live = {k[0]: rec.ranges[v] for k, v in rec.held.items()}
emit("P3.6", sorted(live.values()) == sorted(rec.ranges) and live["e"] == "12-15" and rec.problems == [],
     f"fifth shard after the third leg ends: live={live}")

# P4: the monitor's exit paths with stand-in seams.


class Stream:
    def __init__(self, text: str, alive: bool = True):
        self.stdout = io.StringIO(text)
        self.pid = 515151
        self.returncode = None if alive else 0

    def poll(self):
        return self.returncode


def drive(body, terminate=None, start_fail=False, ranges=("4-7",), stream_text=""):
    calls = []
    stream = Stream(stream_text)

    def popen(command, **kwargs):
        calls.append("popen")
        return stream

    def term(process, *, use_sudo, primary):
        calls.append("terminate")
        if terminate:
            terminate()

    ctx = mock.Mock()
    ctx.use_sudo = False
    ctx.env = {}
    ctx.cwd = "/"
    patches = [mock.patch.object(act, "docker_prefix", lambda *_a: ["docker"]),
               mock.patch.object(act, "run_docker", lambda *a, **k: ok_reply)]
    if start_fail:
        patches.append(mock.patch.object(act, "start_cleanup_safe_thread", mock.Mock(side_effect=RuntimeError("no thread"))))
    outcome = "returned"
    with contextlib.ExitStack() as stack:
        for p in patches:
            stack.enter_context(p)
        try:
            with act.job_cpu_range_monitor(boundary, ranges, context=ctx,
                                           seams=act.ProcessSeams(popen=popen, terminate_group=term)):
                body()
        except BaseException as exc:  # noqa: BLE001 - probe records the outcome
            outcome = f"{type(exc).__name__}: {exc}"
    return calls, outcome, stream


def kbi():
    raise KeyboardInterrupt


calls, outcome, stream = drive(kbi)
emit("P4.1", calls == ["popen", "terminate"] and stream.stdout.closed and outcome.startswith("KeyboardInterrupt"),
     f"KeyboardInterrupt in the body: calls={calls} outcome={outcome} pipe closed={stream.stdout.closed}")
calls, outcome, stream = drive(lambda: (_ for _ in ()).throw(act.TerminationRequest(15)))
emit("P4.2", calls == ["popen", "terminate"] and "TerminationRequest" in outcome,
     f"TerminationRequest in the body: calls={calls} outcome={outcome}")
calls, outcome, stream = drive(lambda: None, start_fail=True)
emit("P4.3", calls == ["popen", "terminate"] and outcome.startswith("Refusal"),
     f"reader thread cannot start: calls={calls} outcome={outcome}")


def boom():
    raise act.Refusal("cannot reap interrupted host process leader")


calls, outcome, stream = drive(lambda: None, terminate=boom)
emit("P4.4", None, f"containment walk itself raises: calls={calls} outcome={outcome} "
     f"pipe closed={stream.stdout.closed} (the reader is not joined on this path)")

# P4.5 the join waits for an in-flight move: a slow assign is finished before exit.
order = []
slow_line = line("create", ids["a"]) + "\n"


def slow_run_docker(*a, **k):
    order.append("move-start")
    time.sleep(0.5)
    order.append("move-end")
    return ok_reply


ctx = mock.Mock()
ctx.use_sudo = False
ctx.env = {}
ctx.cwd = "/"
with mock.patch.object(act, "docker_prefix", lambda *_a: ["docker"]), \
        mock.patch.object(act, "run_docker", slow_run_docker):
    with act.job_cpu_range_monitor(boundary, ("4-7",), context=ctx,
                                   seams=act.ProcessSeams(popen=lambda c, **k: Stream(slow_line),
                                                          terminate_group=lambda p, **k: order.append("terminate"))):
        time.sleep(0.1)
    order.append("after-monitor")
emit("P4.5", order[-1] == "after-monitor" and "move-end" in order and order.index("move-end") < order.index("after-monitor"),
     f"in-flight move completes before the monitor exits: {order}")

# P5: a run whose monitor reports problems keeps act's verdict (code path read
# through execute_workflows with every collaborator stood in is the self-test's
# job; here the report function alone).
buf_out, buf_err = io.StringIO(), io.StringIO()
rec = act.JobCpuRanges(boundary, ("4-7",), lambda c, r: ok_reply)
rec.problems.append("planted")
with contextlib.redirect_stdout(buf_out), contextlib.redirect_stderr(buf_err):
    result = act.report_job_cpu_ranges("rtl-full", rec)
emit("P5", result is None and "WARNING: rtl-full: CPU ranges: planted" in buf_err.getvalue(),
     f"report returns {result!r}; stdout={buf_out.getvalue().strip()!r} stderr={buf_err.getvalue().strip()!r}")

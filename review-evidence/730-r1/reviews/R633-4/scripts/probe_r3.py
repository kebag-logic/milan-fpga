"""Reviewer probes for PR #731 round 3 (offline; run inside a disposable boundary).

Usage: python3 -I probe_r3.py <tree-root> [seeds]

Imports <tree-root>/scripts/act_ci.py as a module (its entry point does not
run) and exercises only pure functions and the JobCpuRanges record against an
independently written model daemon. No Docker, no subprocess, no signal.

P1  randomized lifecycles (create/start/die/destroy, restarts, moves applied
    then timed out, moves lost and landing late, refused moves, unreadable
    inspects, containers removed with no event, stale and duplicated events
    from an earlier stream window): after every step no two containers the
    daemon still has share a job range, and the staging range is never a job
    range;
P2  derivation: the most of any selected workflow, in either order;
P3  derivation reads only the files it is handed (planted checkout differs
    from the runner's own tree);
P4  layout: every slot 0..SLOT_LIMIT at every concurrency 1..SLOT_JOB_RANGES
    gives CONTAINER_CPU_LIMIT-wide ranges disjoint within and across slots,
    and refuses exactly when the host lacks the last CPU;
P5  a run deriving a range count never makes a range of another width
    (each leg's nproc stays CONTAINER_CPU_LIMIT).
Exits 1 if any probe fails.
"""

from __future__ import annotations

import importlib.util
import json
import pathlib
import random
import subprocess
import sys
import tempfile
from unittest import mock

ROOT = pathlib.Path(sys.argv[1]).resolve()
SEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 200
spec = importlib.util.spec_from_file_location("act_ci_under_review", ROOT / "scripts" / "act_ci.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

FAILED: list[str] = []


def report(name: str, ok: bool, detail: str) -> None:
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}")
    if not ok:
        FAILED.append(name)


def done(stdout: str = "", stderr: str = "", rc: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], rc, stdout, stderr)


class Daemon:
    """Each container's configured cpuset; the event log in daemon order; how moves misbehave."""

    def __init__(self, rng: random.Random, token: str, staging: str) -> None:
        self.rng = rng
        self.token = token
        self.staging = staging
        self.cpus: dict[str, str] = {}
        self.running: set[str] = set()
        self.pending: dict[str, str] = {}
        self.unreadable: set[str] = set()
        self.events: list[str] = []
        self.serial = 0

    def emit(self, action: str, cid: str, token: str | None = None) -> None:
        actor = {"ID": cid, "Attributes": {m.DOCKER_OWNER_LABEL: token or self.token}}
        self.events.append(json.dumps({"Type": "container", "Action": action, "Actor": actor}) + "\n")

    def new_id(self) -> str:
        self.serial += 1
        return f"{self.serial:064x}"

    def assign(self, cid: str, cpus: str) -> subprocess.CompletedProcess[str]:
        if cid not in self.cpus:
            return done(stderr=f"Error: No such container: {cid}\n", rc=1)
        fate = self.rng.choice(["ok"] * 6 + ["applied", "lost", "rejected", "unreadable"])
        if fate == "rejected":
            return done(stderr="Error response from daemon: busy\n", rc=1)
        if fate in ("lost", "unreadable"):
            self.pending[cid] = cpus
            if fate == "unreadable":
                self.unreadable.add(cid)
            raise m.Refusal("job container CPU-range move timed out")
        self.cpus[cid] = cpus
        self.emit("update", cid)
        if fate == "applied":
            raise m.Refusal("job container CPU-range move timed out")
        return done()

    def read_cpus(self, cid: str) -> subprocess.CompletedProcess[str]:
        if cid not in self.cpus:
            return done(stderr=f"Error: No such container: {cid}\n", rc=1)
        if cid in self.unreadable and self.rng.random() < 0.7:
            raise m.Refusal("job container CPU-range read timed out")
        return done(stdout=self.cpus[cid] + "\n")


def p1_lifecycles(seeds: int) -> None:
    ranges = ("4-7", "8-11", "12-15", "16-19")
    jobset = set(ranges)
    violations: list[str] = []
    steps = 0
    staged = 0
    for seed in range(seeds):
        rng = random.Random(seed)
        token = "t" * 32
        daemon = Daemon(rng, token, "0-3")
        boundary = mock.Mock(token=token)
        record = m.JobCpuRanges(boundary, ranges, daemon.assign, daemon.read_cpus)
        # Stale window: events from an earlier stream about containers already gone.
        for _ in range(rng.randint(0, 3)):
            stale = daemon.new_id()
            for action in rng.sample(["create", "start", "die", "destroy"], rng.randint(1, 4)):
                daemon.emit(action, stale)
        cursor = 0
        for _step in range(400):
            steps += 1
            op = rng.random()
            existing = list(daemon.cpus)
            if op < 0.16 and len(existing) < 7:
                cid = daemon.new_id()
                daemon.cpus[cid] = daemon.staging
                daemon.emit("create", cid)
            elif op < 0.30 and existing:
                cid = rng.choice(existing)
                if cid not in daemon.running:
                    daemon.running.add(cid)
                    daemon.emit("start", cid)
            elif op < 0.40 and daemon.running:
                cid = rng.choice(sorted(daemon.running))
                daemon.running.discard(cid)
                daemon.emit("die", cid)
            elif op < 0.50 and existing:
                cid = rng.choice(existing)
                if cid in daemon.running:
                    daemon.running.discard(cid)
                    daemon.emit("die", cid)
                del daemon.cpus[cid]
                daemon.pending.pop(cid, None)
                if rng.random() < 0.9:
                    daemon.emit("destroy", cid)
            elif op < 0.58 and daemon.pending:
                cid = rng.choice(sorted(daemon.pending))
                daemon.cpus[cid] = daemon.pending.pop(cid)
                daemon.emit("update", cid)
            elif op < 0.62 and daemon.events:
                daemon.events.append(rng.choice(daemon.events[: cursor or 1]))  # duplicate
            elif op < 0.64:
                daemon.emit("create", daemon.new_id(), token="f" * 32)  # foreign owner
            else:
                # The reader drains some events, in daemon order.
                for _ in range(rng.randint(1, 3)):
                    if cursor < len(daemon.events):
                        record.observe(daemon.events[cursor])
                        cursor += 1
            on_job: dict[str, list[str]] = {}
            for cid, cpus in daemon.cpus.items():
                if cpus in jobset:
                    on_job.setdefault(cpus, []).append(cid[-4:])
            for cpus, owners in on_job.items():
                if len(owners) > 1:
                    violations.append(f"seed {seed}: {cpus} configured on {owners}")
            for cid, cpus in daemon.cpus.items():
                if cpus in jobset and record.held.get(cid) != ranges.index(cpus):
                    violations.append(f"seed {seed}: {cid[-4:]} on {cpus} without holding it")
            if len(set(record.held.values())) != len(record.held):
                violations.append(f"seed {seed}: record maps two holders to one range")
        staged += sum(1 for v in record.outcome.values() if v == "staging")
    report(
        "P1 randomized lifecycles keep every job range to one existing container",
        not violations,
        f"{seeds} seeds x 400 steps = {steps} steps; staging outcomes {staged}; "
        f"violations {len(violations)} {violations[:3]}",
    )


def write(root: pathlib.Path, name: str, jobs: str) -> None:
    path = root / m.WORKFLOWS[name]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"name: {name}\non: pull_request\njobs:\n{jobs}", encoding="utf-8")


PLAIN = "    runs-on: ubuntu-latest\n    steps:\n      - run: true\n"


def p2_p3_derivation() -> None:
    with tempfile.TemporaryDirectory() as raw:
        root = pathlib.Path(raw)
        write(root, "rtl-full", f"  wide:\n{PLAIN}    strategy:\n      matrix:\n        n: [1, 2, 3, 4, 5]\n")
        write(root, "docs", f"  only:\n{PLAIN}")
        forward = m.replay_container_concurrency(root, ("docs", "rtl-full"))
        backward = m.replay_container_concurrency(root, ("rtl-full", "docs"))
    report("P2 concurrency is the most of any selected workflow in either order",
           forward == backward == 4, f"(docs, rtl-full) -> {forward}; (rtl-full, docs) -> {backward}")
    with tempfile.TemporaryDirectory() as raw:
        root = pathlib.Path(raw)
        write(root, "docs", f"  m:\n{PLAIN}    strategy:\n      max-parallel: 3\n      matrix:\n        n: [1, 2, 3]\n")
        planted = m.replay_container_concurrency(root, ("docs",))
        shipping = m.replay_container_concurrency(ROOT, ("docs",))
        write(root, "docs", f"  m:\n{PLAIN}    strategy:\n      max-parallel: 5\n      matrix:\n        n: [1, 2, 3]\n")
        wide = m.replay_container_concurrency(root, ("docs",))
        with mock.patch.object(m.os, "cpu_count", return_value=128):
            try:
                m.job_cpu_ranges(0, wide)
                refused = False
            except m.Refusal:
                refused = True
    report("P3 derivation reads the tree it is handed: a planted checkout's max-parallel wins, too wide refuses",
           planted == 3 and shipping == 1 and wide == 5 and refused,
           f"planted {planted}, runner tree {shipping}, planted 5 -> {wide}, refused {refused}")
    run_line = [line for line in (ROOT / "scripts" / "act_ci.py").read_text().splitlines()
                if "replay_container_concurrency(" in line and "def " not in line and "shipping" not in line
                and "root," not in line and "root)" not in line]
    report("P3b run_validation derives from the materialized checkout",
           any("layout.checkout" in line for line in run_line), "; ".join(s.strip() for s in run_line))


def p4_p5_layout() -> None:
    bad: list[str] = []
    widths: set[int] = set()
    named: list[tuple[str, str]] = []
    top = m.slot_cpu_base(m.SLOT_LIMIT) + (m.SLOT_JOB_RANGES + 1) * m.CONTAINER_CPU_LIMIT
    for slot in range(m.SLOT_LIMIT + 1):
        for conc in range(1, m.SLOT_JOB_RANGES + 1):
            need = m.slot_cpu_base(slot) + (conc + 1) * m.CONTAINER_CPU_LIMIT
            for host in (need - 1, need):
                with mock.patch.object(m.os, "cpu_count", return_value=host):
                    try:
                        got = m.job_cpu_ranges(slot, conc)
                    except m.Refusal:
                        got = None
                if (got is None) != (host < need):
                    bad.append(f"slot {slot} conc {conc} host {host}: {got}")
                if got:
                    widths |= {int(t.split('-')[1]) - int(t.split('-')[0]) + 1 for t in got}
        with mock.patch.object(m.os, "cpu_count", return_value=top):
            named.append((f"s{slot} staging", m.container_cpuset(slot)))
            named += [(f"s{slot} r{i}", t) for i, t in enumerate(m.job_cpu_ranges(slot, m.SLOT_JOB_RANGES))]
    overlaps = m.cpu_range_overlaps(named)
    report("P4 every slot and concurrency: refusal exactly at the last CPU, all ranges disjoint",
           not bad and not overlaps,
           f"slots 0-{m.SLOT_LIMIT}, {len(named)} ranges, boundary errors {bad[:2]}, overlaps {overlaps[:2]}")
    report("P5 every range is CONTAINER_CPU_LIMIT wide (nproc 4)", widths == {m.CONTAINER_CPU_LIMIT},
           f"widths {sorted(widths)}")


p1_lifecycles(SEEDS)
p2_p3_derivation()
p4_p5_layout()
print("probes: " + ("PASS" if not FAILED else "FAIL " + ", ".join(FAILED)))
raise SystemExit(1 if FAILED else 0)

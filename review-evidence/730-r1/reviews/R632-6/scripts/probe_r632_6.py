#!/usr/bin/env python3
"""Reviewer probe R632-6 for PR #731: CPU-range layout, derivation and lifecycle.

Usage: python3 -I probe_r632_6.py <tree> [seeds]
Loads <tree>/scripts/act_ci.py as a module (no network, no Docker, no act)
and checks, independently of the runner's own self-test helpers:

  L  layout: slot N's staging and job ranges, by this probe's own interval
     arithmetic, for slots 0..63 at every concurrency 1..4; no CPU shared
     inside a slot or between any two slots; width 4; host-size refusal.
  D  derivation from the workflow files themselves: shipping values, then
     copies of the workflow tree with max-parallel edited (literal, too wide,
     expression, zero, non-mapping strategy), and every selection order.
  R  lifecycle: a model daemon whose containers act creates, starts, stops,
     restarts and removes while the monitor lags, with moves that succeed,
     fail, time out after or before applying, or land late, and reads that
     fail. After every daemon change no two existing containers sit on one
     job range, and each container on a job range holds it in the record.
  P  the plan line for slot 0 and slot 3 of the shipping rtl-full.
Prints one line per check and exits 0 only if every check passes.
"""
from __future__ import annotations

import importlib.util
import itertools
import json
import os
import pathlib
import random
import shutil
import subprocess
import sys
import tempfile
from unittest import mock

TREE = pathlib.Path(sys.argv[1]).resolve()
SEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 2000
spec = importlib.util.spec_from_file_location("act_ci_r632_6", TREE / "scripts" / "act_ci.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

failures = 0


def check(label: str, ok: bool, detail: str = "") -> None:
    global failures
    print(f"  {'ok  ' if ok else 'FAIL'} {label}" + (f" ({detail})" if detail and not ok else ""))
    failures += 0 if ok else 1


def refused(action) -> str | None:
    try:
        action()
    except m.Refusal as exc:
        return str(exc)
    return None


def cpus(text: str) -> set[int]:
    first, last = (int(part) for part in text.split("-"))
    return set(range(first, last + 1))


# ---------------------------------------------------------------- L layout
print("L layout")
with mock.patch.object(os, "cpu_count", return_value=4096):
    owner: dict[int, str] = {}
    shared = []
    widths_ok = True
    for slot in range(64):
        staging = m.container_cpuset(slot)
        jobs = m.job_cpu_ranges(slot, 4)
        expect_base = slot * 20
        check(f"slot {slot} staging is {expect_base}-{expect_base + 3}", staging == f"{expect_base}-{expect_base + 3}") if slot in (0, 1, 3, 63) else None
        for count in range(1, 5):
            prefix = m.job_cpu_ranges(slot, count)
            if prefix != jobs[:count]:
                check(f"slot {slot} concurrency {count} is a prefix of the 4-range layout", False, repr(prefix))
        for name, text in [("staging", staging)] + [(f"job{i}", t) for i, t in enumerate(jobs)]:
            got = cpus(text)
            widths_ok &= len(got) == m.CONTAINER_CPU_LIMIT == 4
            for cpu in got:
                if cpu in owner:
                    shared.append((cpu, owner[cpu], f"slot{slot}:{name}"))
                owner[cpu] = f"slot{slot}:{name}"
    check("every staging and job range of slots 0..63 is 4 CPUs wide", widths_ok)
    check("no CPU is shared by two ranges in one slot or across slots 0..63 at full concurrency", not shared, repr(shared[:3]))
    check("slots 0..63 at full concurrency own exactly CPUs 0..1279", set(owner) == set(range(1280)))
    check("slot 0 job ranges are 4-7 8-11 12-15 16-19", m.job_cpu_ranges(0, 4) == ("4-7", "8-11", "12-15", "16-19"))
    check("slot 3 job ranges are 64-67 .. 76-79", m.job_cpu_ranges(3, 4) == ("64-67", "68-71", "72-75", "76-79"))
    check("a concurrency of 5 is refused", refused(lambda: m.job_cpu_ranges(0, 5)) is not None)
    check("a concurrency of 0 is refused", refused(lambda: m.job_cpu_ranges(0, 0)) is not None)
for host in (1, 4, 7, 8, 19, 20, 21, 79, 80, 128):
    with mock.patch.object(os, "cpu_count", return_value=host):
        for slot in (0, 3, 6):
            for count in (1, 4):
                need = slot * 20 + 4 * (count + 1)
                outcome = refused(lambda: m.job_cpu_ranges(slot, count))
                check(
                    f"host {host} slot {slot} x{count}: {'refused' if need > host else 'allowed'} (needs CPUs 0..{need - 1})",
                    (outcome is not None) == (need > host),
                    outcome or "allowed",
                )

# ---------------------------------------------------------------- D derivation
print("D derivation")
shipping = {name: m.replay_container_concurrency(TREE, [name]) for name in m.WORKFLOWS}
check("shipping derives rtl-full 4, docs/elaborate/rtl-fast 1", shipping == {"docs": 1, "elaborate": 1, "rtl-fast": 1, "rtl-full": 4}, repr(shipping))
for order in itertools.permutations(m.WORKFLOWS):
    got = m.replay_container_concurrency(TREE, list(order))
    if got != 4:
        check(f"order {order} derives 4", False, repr(got))
check("every order of the four shipping workflows derives 4", True)

scratch = pathlib.Path(tempfile.mkdtemp(prefix="r632-6-derive-"))


def edited(old: str, new: str, count: int = 1) -> pathlib.Path:
    root = scratch / f"t{abs(hash((old, new, count)))}"
    shutil.rmtree(root, ignore_errors=True)
    (root / ".github" / "workflows").mkdir(parents=True)
    for rel in m.WORKFLOWS.values():
        shutil.copy(TREE / rel, root / rel)
    path = root / ".github/workflows/rtl.yml"
    text = path.read_text()
    if text.count(old) < count:
        raise SystemExit(f"probe anchor missing: {old!r}")
    path.write_text(text.replace(old, new, count))
    return root


anchor = "      matrix:\n"
for value, expect in (("1", 1), ("2", 2), ("3", 3), ("4", 4), ("0", 1), ("007", 7)):
    root = edited(anchor, f"      max-parallel: {value}\n{anchor}", 2)
    got = m.replay_container_concurrency(root, ["rtl-full"])
    check(f"rtl.yml max-parallel {value} on both matrix jobs: rtl-full derives {expect} (the file is read, not a mirror)", got == expect, repr(got))
for value, expect in (("1", 4), ("3", 4), ("6", 6)):
    root = edited(anchor, f"      max-parallel: {value}\n{anchor}", 1)
    got = m.replay_container_concurrency(root, ["rtl-full"])
    check(f"max-parallel {value} on the first matrix job only: the other job's default keeps the maximum at {expect}", got == expect, repr(got))
for value in ("5", "64", "999999"):
    root = edited(anchor, f"      max-parallel: {value}\n{anchor}")
    derived = m.replay_container_concurrency(root, ["rtl-full"])
    with mock.patch.object(os, "cpu_count", return_value=4096):
        outcome = refused(lambda: m.job_cpu_ranges(0, derived))
    check(f"max-parallel {value} (too wide) is refused before any slot", outcome is not None, f"derived {derived}")
for value in ("${{ matrix.n }}", "'3 '", "-1", "1e1", "1234567", "[2]", "{a: 1}", "''"):
    root = edited(anchor, f"      max-parallel: {value}\n{anchor}")
    outcome = refused(lambda: m.replay_container_concurrency(root, ["rtl-full"]))
    check(f"max-parallel {value!r} (not a literal integer) is refused", outcome is not None)
root = edited("    strategy:\n", "    strategy: ${{ fromJSON('{}') }}\n    x-strategy:\n")
check("a strategy that is not a mapping is refused", refused(lambda: m.replay_container_concurrency(root, ["rtl-full"])) is not None)
with mock.patch.object(m, "CONCURRENT_JOB_LIMIT", 2):
    root = edited(anchor, f"      max-parallel: 3\n{anchor}")
    got = m.replay_container_concurrency(root, ["rtl-full"])
check("CONCURRENT_JOB_LIMIT 2 sums the two widest jobs (3 + 4 = 7)", got == 7, repr(got))
shutil.rmtree(scratch, ignore_errors=True)

# ---------------------------------------------------------------- R lifecycle
print("R lifecycle")
TOKEN = "b" * 32
BOUNDARY = m.DockerBoundary(token=TOKEN, name="r632-6-probe") if "name" in m.DockerBoundary.__dataclass_fields__ else m.DockerBoundary(token=TOKEN)
STAGING = "0-3"
RANGES = ("4-7", "8-11", "12-15", "16-19")


class World:
    def __init__(self, rng: random.Random, legs: int, width: int) -> None:
        self.rng = rng
        self.containers: dict[str, dict] = {}
        self.events: list[str] = []
        self.late: list[tuple[str, str, int]] = []
        self.todo = [f"{n:064x}" for n in range(1, legs + 1)]
        self.width = width
        self.phase: dict[str, int] = {}
        self.violations: list[str] = []
        self.record = None
        self.tick = 0

    def emit(self, action: str, cid: str) -> None:
        attrs = {m.DOCKER_OWNER_LABEL: TOKEN}
        self.events.append(json.dumps({"Type": "container", "Action": action, "Actor": {"ID": cid, "Attributes": attrs}}))

    def invariant(self, where: str) -> None:
        seen: dict[str, str] = {}
        for cid, c in self.containers.items():
            if c["cpus"] in RANGES:
                if c["cpus"] in seen:
                    self.violations.append(f"{where}: {seen[c['cpus']][:4]} and {cid[:4]} both on {c['cpus']}")
                seen[c["cpus"]] = cid
                if self.record is not None:
                    idx = self.record.held.get(cid)
                    if idx is None or RANGES[idx] != c["cpus"]:
                        self.violations.append(f"{where}: {cid[:4]} on {c['cpus']} without holding it")

    def act_step(self) -> bool:
        """One act-side lifecycle step; False when act has nothing left to do."""
        self.tick += 1
        for item in list(self.late):
            cid, target, due = item
            if due <= self.tick:
                self.late.remove(item)
                if cid in self.containers:
                    self.containers[cid]["cpus"] = target
                    self.emit("update", cid)
                    self.invariant("late landing")
        live = [cid for cid in self.containers]
        can_create = self.todo and len(live) < self.width
        choices = []
        if can_create:
            choices.append("create")
        choices += [cid for cid in live]
        if not choices:
            return bool(self.late)
        pick = self.rng.choice(choices)
        if pick == "create":
            cid = self.todo.pop(0)
            self.containers[cid] = {"cpus": STAGING, "running": False}
            self.phase[cid] = 0
            self.emit("create", cid)
        else:
            cid = pick
            c = self.containers[cid]
            if not c["running"]:
                if self.phase[cid] >= 2 and self.rng.random() < 0.5:
                    del self.containers[cid]
                    self.emit("destroy", cid)
                else:
                    c["running"] = True
                    self.phase[cid] += 1
                    self.emit("start", cid)
            else:
                c["running"] = False
                self.phase[cid] += 1
                self.emit("die", cid)
        self.invariant("act step")
        return True

    def interleave(self) -> None:
        for _ in range(self.rng.choice((0, 0, 1, 2, 4))):
            self.act_step()

    def assign(self, cid: str, target: str) -> subprocess.CompletedProcess[str]:
        mode = self.rng.choice(("ok", "ok", "ok", "applied_timeout", "lost_timeout", "late", "refused"))
        self.interleave()
        exists = cid in self.containers
        if mode in ("ok", "applied_timeout") and exists:
            self.containers[cid]["cpus"] = target
            self.emit("update", cid)
            self.invariant("move applied")
        if mode == "late" and exists:
            self.late.append((cid, target, self.tick + self.rng.randint(1, 6)))
        self.interleave()
        if mode in ("applied_timeout", "lost_timeout", "late"):
            raise m.Refusal("job container CPU-range move timed out")
        if not exists:
            return subprocess.CompletedProcess([], 1, "", f"Error response from daemon: No such container: {cid}\n")
        if mode == "refused":
            return subprocess.CompletedProcess([], 1, "", "Error response from daemon: Cannot update container\n")
        return subprocess.CompletedProcess([], 0, "", "")

    def read(self, cid: str) -> subprocess.CompletedProcess[str]:
        mode = self.rng.choice(("ok", "ok", "ok", "ok", "fail", "timeout"))
        self.interleave()
        if mode == "timeout":
            raise m.Refusal("job container CPU-range read timed out")
        if mode == "fail":
            return subprocess.CompletedProcess([], 1, "", "Error: daemon busy\n")
        if cid not in self.containers:
            return subprocess.CompletedProcess([], 1, "", f"Error: No such container: {cid}\n")
        return subprocess.CompletedProcess([], 0, self.containers[cid]["cpus"] + "\n", "")


def lifecycle(seed: int) -> list[str]:
    rng = random.Random(seed)
    width = rng.choice((1, 2, 3, 4, 4, 4, 5))
    ranges = RANGES[: rng.choice((1, 2, 3, 4, 4))]
    world = World(rng, rng.randint(1, 12), width)
    record = m.JobCpuRanges(BOUNDARY, ranges, world.assign, world.read)
    world.record = record
    global RANGES_ACTIVE
    while True:
        progressed = world.act_step()
        while world.events and rng.random() < 0.6:
            record.observe(world.events.pop(0))
            world.invariant("after observe")
        if not progressed and not world.events and not world.late:
            break
    while world.events:
        record.observe(world.events.pop(0))
        world.invariant("drain")
    if record.held:
        world.violations.append(f"ranges still held after every container was destroyed: {record.held}")
    if record.most_at_once > len(ranges):
        world.violations.append(f"most_at_once {record.most_at_once} > {len(ranges)}")
    return world.violations


bad = []
for seed in range(SEEDS):
    found = lifecycle(seed)
    if found:
        bad.append((seed, found[:2]))
check(f"{SEEDS} randomized lifecycles: no two existing containers on one job range, every occupant holds its range, all freed at the end", not bad, repr(bad[:3]))

# The exact R633-1 restart sequence, with a model daemon
seq_world = World(random.Random(0), 0, 9)
seq_world.rng = mock.Mock(choice=lambda xs: "ok" if "ok" in xs else 0, random=lambda: 1.0, randint=lambda a, b: a)
rec = m.JobCpuRanges(BOUNDARY, RANGES, seq_world.assign, seq_world.read)
seq_world.record = rec
A, B = f"{10:064x}", f"{11:064x}"


def daemon(action: str, cid: str) -> None:
    if action == "create":
        seq_world.containers[cid] = {"cpus": STAGING, "running": False}
    elif action == "start":
        seq_world.containers[cid]["running"] = True
    elif action == "die":
        seq_world.containers[cid]["running"] = False
    seq_world.emit(action, cid)
    rec.observe(seq_world.events.pop(0))
    while seq_world.events:
        rec.observe(seq_world.events.pop(0))
    seq_world.invariant(f"{action} {cid[-1]}")


for action, cid in (("create", A), ("start", A), ("die", A), ("create", B), ("start", B), ("start", A)):
    daemon(action, cid)
check("R633-1 sequence create A, update A, start A, die A, create B, update B, start B, start A: A and B never share a range",
      not seq_world.violations and seq_world.containers[A]["cpus"] == "4-7" and seq_world.containers[B]["cpus"] == "8-11",
      repr(seq_world.violations))

# ---------------------------------------------------------------- P plan line
print("P plan")
with mock.patch.object(os, "cpu_count", return_value=128):
    for slot in (0, 3):
        concurrency = m.replay_container_concurrency(TREE, ["rtl-full"])
        line = m.describe_job_cpu_ranges(slot, concurrency, m.job_cpu_ranges(slot, concurrency))
        print(f"    {line}")
        base = slot * 20
        want = " ".join(f"--cpuset-cpus={base + 4 * k}-{base + 4 * k + 3}" for k in range(1, 5))
        check(f"slot {slot} plan names staging {base}-{base + 3} and four job ranges", f"--cpuset-cpus={base}-{base + 3}, then" in line and line.endswith(want))

print(f"probe_r632_6: {'PASS' if failures == 0 else 'FAIL'} ({failures} failure(s))")
sys.exit(1 if failures else 0)

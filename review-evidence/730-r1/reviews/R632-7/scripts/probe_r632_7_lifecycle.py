#!/usr/bin/env python3
"""Reviewer probe R632-7-L: the CPU-range record under randomised container lifecycles.

Usage: python3 -I probe_r632_7_lifecycle.py <tree> [seeds-per-mode]

Drives the tree's own JobCpuRanges.observe with ``docker events`` lines from an
independent model daemon (not the self-test's ModelDaemon). Containers are
created, started, stopped, restarted and removed at random; the monitor reads
the event queue with a random lag, so its view trails the daemon. Each move
may succeed, be applied then time out, be lost and land later, or be refused;
each inspect may time out. After EVERY daemon step and every consumed event:

  I1  no two containers the daemon still has (any state) run on one job range;
  I2  a container the daemon has on a job range holds exactly that range;
  I3  a move that may still land targets a range reserved to its container;
  I4  no range is reserved twice; at most len(ranges) reservations.

Modes: ``actlike`` (at most 4 containers exist at once, as act's max-parallel 4
with CONCURRENT_JOB_LIMIT 1; events in daemon order; additionally I5: no
container is ever left on the staging range and no problem names a shortage),
``stress`` (up to 7 at once), ``reorder`` (events delivered out of order within
a window of 4), ``dup`` (each event may be delivered twice) and ``lostdestroy``
(a destroy event may never arrive; inspect must free the range).
Exits 0 only if no invariant is ever violated.
"""
from __future__ import annotations

import collections
import importlib.util
import json
import pathlib
import random
import sys

TREE = pathlib.Path(sys.argv[1]).resolve()
SEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
spec = importlib.util.spec_from_file_location("act_ci_r632_7_l", TREE / "scripts" / "act_ci.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

TOKEN = "e" * 32
BOUNDARY = m.DockerBoundary(token=TOKEN, name="r632-7-lifecycle")
RANGES = ("4-7", "8-11", "12-15", "16-19")
STAGING = "0-3"


def completed(code: int = 0, out: str = "", err: str = ""):
    import subprocess
    return subprocess.CompletedProcess([], code, out, err)


class Daemon:
    def __init__(self, rng: random.Random, mode: str) -> None:
        self.rng = rng
        self.mode = mode
        self.live: dict[str, dict[str, str]] = {}
        self.pending: dict[str, str] = {}
        self.queue: collections.deque[tuple[str, str]] = collections.deque()
        self.serial = 0
        self.faulty = mode != "actlike" or rng.random() < 0.7

    def emit(self, action: str, cid: str) -> None:
        self.queue.append((action, cid))
        if self.mode == "dup" and self.rng.random() < 0.3:
            self.queue.append((action, cid))

    def assign(self, cid: str, cpus: str):
        if cid not in self.live:
            return completed(1, err=f"Error: No such container: {cid}\n")
        roll = self.rng.random() if self.faulty else 1.0
        if roll < 0.08:
            return completed(1, err="Error response from daemon: cpuset busy\n")
        if roll < 0.16:
            self.pending[cid] = cpus
            raise m.Refusal("job container CPU-range move timed out")
        self.live[cid]["cpus"] = cpus
        self.emit("update", cid)
        if roll < 0.24:
            raise m.Refusal("job container CPU-range move timed out")
        return completed()

    def read(self, cid: str):
        if self.faulty and self.rng.random() < 0.1:
            raise m.Refusal("job container CPU-range read timed out")
        if cid not in self.live:
            return completed(1, err=f"Error: No such container: {cid}\n")
        return completed(out=self.live[cid]["cpus"] + "\n")


def line(action: str, cid: str) -> str:
    actor = {"ID": cid, "Attributes": {m.DOCKER_OWNER_LABEL: TOKEN, "name": "act-job"}}
    return json.dumps({"Type": "container", "Action": action, "Actor": actor}) + "\n"


def violations(d: Daemon, rec) -> list[str]:
    found = []
    on_range = [(cid, c["cpus"]) for cid, c in d.live.items() if c["cpus"] in RANGES]
    seen: dict[str, str] = {}
    for cid, cpus in on_range:
        if cpus in seen:
            found.append(f"I1 {seen[cpus][:4]} and {cid[:4]} both on {cpus}")
        seen[cpus] = cid
        if cid not in rec.held or RANGES[rec.held[cid]] != cpus:
            found.append(f"I2 {cid[:4]} on {cpus} without holding it")
    for cid, cpus in d.pending.items():
        if cid in d.live and (cid not in rec.held or RANGES[rec.held[cid]] != cpus):
            found.append(f"I3 {cid[:4]} may still land on {cpus} without holding it")
    values = list(rec.held.values())
    if len(set(values)) != len(values) or len(values) > len(RANGES):
        found.append(f"I4 reservations {sorted(values)}")
    return found


def run(seed: int, mode: str) -> tuple[list[str], dict[str, int]]:
    rng = random.Random(f"{mode}-{seed}")
    d = Daemon(rng, mode)
    rec = m.JobCpuRanges(BOUNDARY, RANGES, d.assign, d.read)
    cap = {"actlike": 4, "stress": 7}.get(mode, 5)
    lost_destroy = mode == "lostdestroy"
    bad: list[str] = []
    stats = collections.Counter()

    def deliver_one() -> None:
        if not d.queue:
            return
        if mode == "reorder" and len(d.queue) > 1:
            index = rng.randrange(min(4, len(d.queue)))
            d.queue.rotate(-index)
            action, cid = d.queue.popleft()
            d.queue.rotate(index)
        else:
            action, cid = d.queue.popleft()
        rec.observe(line(action, cid))
        stats["events"] += 1
        bad.extend(f"seed {seed} after event {action} {cid[:4]}: {v}" for v in violations(d, rec))

    for _step in range(400):
        roll = rng.random()
        states = collections.defaultdict(list)
        for cid, c in d.live.items():
            states[c["state"]].append(cid)
        if roll < 0.22 and len(d.live) < cap:
            d.serial += 1
            cid = f"{d.serial:064x}"
            d.live[cid] = {"cpus": STAGING, "state": "created"}
            d.emit("create", cid)
            stats["created"] += 1
        elif roll < 0.40 and (states["created"] or states["stopped"]):
            cid = rng.choice(states["created"] + states["stopped"])
            d.live[cid]["state"] = "running"
            d.emit("start", cid)
        elif roll < 0.52 and states["running"]:
            cid = rng.choice(states["running"])
            d.live[cid]["state"] = "stopped"
            d.emit("die", cid)
        elif roll < 0.64 and (states["stopped"] or states["created"]):
            cid = rng.choice(states["stopped"] + states["created"])
            del d.live[cid]
            d.pending.pop(cid, None)
            if lost_destroy and rng.random() < 0.5:
                stats["lost destroy"] += 1
            else:
                d.emit("destroy", cid)
        elif roll < 0.70 and d.pending:
            cid = rng.choice(sorted(d.pending))
            target = d.pending.pop(cid)
            if cid in d.live:
                d.live[cid]["cpus"] = target
                d.emit("update", cid)
                stats["late landings"] += 1
        else:
            for _ in range(rng.randrange(1, 4)):
                deliver_one()
        bad.extend(f"seed {seed} after daemon step: {v}" for v in violations(d, rec))
        if bad:
            break
    while d.queue and not bad:
        deliver_one()
    if mode == "actlike" and not bad:
        if "staging" in rec.outcome.values() or any("more than the" in p for p in rec.problems):
            bad.append(f"seed {seed}: I5 a container was left on staging with at most 4 alive: {rec.problems}")
    if rec.most_at_once > len(RANGES):
        bad.append(f"seed {seed}: peak {rec.most_at_once} exceeds {len(RANGES)} ranges")
    stats["moved"] += rec.moved
    stats["staging"] += sum(v == "staging" for v in rec.outcome.values())
    stats["peak"] = max(stats["peak"], rec.most_at_once)
    return bad, stats


failures = 0
for mode in ("actlike", "stress", "reorder", "dup", "lostdestroy"):
    total = collections.Counter()
    first: list[str] = []
    for seed in range(SEEDS):
        bad, stats = run(seed, mode)
        peak = max(total["peak"], stats.pop("peak"))
        total.update(stats)
        total["peak"] = peak
        if bad:
            failures += 1
            first = first or bad[:3]
    verdict = "PASS" if not first else "FAIL"
    print(f"{verdict} {mode}: {SEEDS} seeds, {dict(sorted(total.items()))}")
    for item in first:
        print(f"    {item}")
print(f"probe_r632_7_lifecycle: {'PASS' if not failures else 'FAIL'} ({failures} failing seed(s))")
sys.exit(1 if failures else 0)

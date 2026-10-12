"""Independent reviewer probes for PR #731 at its exact head (round R632-4).

Usage (inside a disposable boundary, e.g. sandbox.sh): python3 -I probe_r632_4.py <tree-root> [seeds]

Imports <tree-root>/scripts/act_ci.py as a module (its entry point does not
run). Starts no daemon, no Docker command and no act. Each probe prints
PASS/FAIL and the script exits 1 if any probe fails.

A1  fuzz: the JobCpuRanges record against an independently written daemon
    model with event lag (the daemon acts before the record reads its event),
    restarts, vanishing containers, applied/lost/rejected moves and transient
    inspect failures; after every daemon step and every observed event no two
    existing containers (counting moves that may still land) use one job
    range, and each one on a job range holds that range in the record.
A2  the previous workflow's tail events, replayed by --since into the next
    workflow's fresh record, move nothing that exists and raise nothing.
A3  a move whose CLI raises something other than Refusal stops the reader as
    a recorded problem; nothing is raised and no range is shared.
A4  run level: a dry run whose materialized checkout widens or narrows
    rtl-full's max-parallel derives from that checkout, not from the trusted
    runner's own workflows; an expression or too-wide value refuses the run.
A5  max-parallel spellings: leading zero accepted as act's Atoi does; signs,
    hex, whitespace-only and empty refused; no matrix means one container.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import os
import pathlib
import random
import subprocess
import sys
import tempfile
from unittest import mock

TREE = pathlib.Path(sys.argv[1]).resolve()
SEEDS = int(sys.argv[2]) if len(sys.argv) > 2 else 300
spec = importlib.util.spec_from_file_location("act_ci_probe", TREE / "scripts" / "act_ci.py")
m = importlib.util.module_from_spec(spec)
sys.modules["act_ci_probe"] = m
spec.loader.exec_module(m)

RESULTS: list[tuple[bool, str]] = []


def report(ok: bool, label: str) -> None:
    RESULTS.append((ok, label))
    print(("PASS " if ok else "FAIL ") + label, flush=True)


TOKEN = "e" * 32
BOUNDARY = m.DockerBoundary(
    token=TOKEN, name=f"milan-act-ci-{TOKEN}", network_id="b" * 64, gateway="172.30.0.1",
    toolcache_owned=True, toolcache_seeded=True, job_volume_prefixes=("act-rtl-full-",),
)
RANGES = ("4-7", "8-11", "12-15", "16-19")
STAGING = "0-3"


def line(action: str, cid: str, token: str = TOKEN) -> str:
    import json
    return json.dumps({"Type": "container", "Action": action,
                       "Actor": {"ID": cid, "Attributes": {m.DOCKER_OWNER_LABEL: token}}}) + "\n"


def done(rc: int = 0, out: str = "", err: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], rc, out, err)


class Daemon:
    """Containers' real cpusets, pending (lost) moves, and an event queue the record reads late."""

    def __init__(self, rng: random.Random) -> None:
        self.rng = rng
        self.cpus: dict[str, str] = {}
        self.running: set[str] = set()
        self.pending: dict[str, str] = {}
        self.queue: list[str] = []
        self.violations: list[str] = []

    def emit(self, action: str, cid: str) -> None:
        self.queue.append(line(action, cid))

    # the record's two seams
    def assign(self, cid: str, cpus: str) -> subprocess.CompletedProcess[str]:
        if cid not in self.cpus:
            return done(1, err=f"Error: No such container: {cid}\n")
        roll = self.rng.random()
        if roll < 0.10:
            return done(1, err="Error response from daemon: cpuset busy\n")
        if roll < 0.20:
            self.pending[cid] = cpus
            raise m.Refusal("job container CPU-range move timed out")
        self.cpus[cid] = cpus
        self.emit("update", cid)
        if roll < 0.30:
            raise m.Refusal("job container CPU-range move timed out")
        return done()

    def read(self, cid: str) -> subprocess.CompletedProcess[str]:
        if self.rng.random() < 0.08:
            raise m.Refusal("job container CPU-range read timed out")
        if cid not in self.cpus:
            return done(1, err=f"Error: No such container: {cid}\n")
        return done(0, out=self.cpus[cid] + "\n")

    def check(self, record: object, where: str) -> None:
        users: dict[str, list[str]] = {}
        for cid, cpus in list(self.cpus.items()) + list(self.pending.items()):
            if cpus in RANGES:
                users.setdefault(cpus, [])
                if cid not in users[cpus]:
                    users[cpus].append(cid)
                held = record.held.get(cid)
                if held is None or RANGES[held] != cpus:
                    self.violations.append(f"{where}: {cid[:1]} on {cpus} without its reservation")
        for cpus, who in users.items():
            if len(who) > 1:
                self.violations.append(f"{where}: {cpus} used by {[w[:1] for w in who]}")
        if len(set(record.held.values())) != len(record.held):
            self.violations.append(f"{where}: a range reserved twice")


def fuzz_once(seed: int) -> tuple[list[str], int, int]:
    rng = random.Random(seed)
    daemon = Daemon(rng)
    record = m.JobCpuRanges(BOUNDARY, RANGES, daemon.assign, daemon.read)
    names = [chr(ord("a") + i) * 64 for i in range(rng.randint(3, 8))]
    created: set[str] = set()
    destroyed: set[str] = set()
    for step in range(rng.randint(20, 70)):
        roll = rng.random()
        fresh = [n for n in names if n not in created]
        live = [n for n in created if n not in destroyed]
        if roll < 0.25 and fresh:
            cid = fresh[0]
            created.add(cid)
            daemon.cpus[cid] = STAGING
            daemon.emit("create", cid)
            if rng.random() < 0.7:
                daemon.running.add(cid)
                daemon.emit("start", cid)
        elif roll < 0.35 and live:
            cid = rng.choice(live)
            if cid in daemon.running:
                daemon.running.discard(cid)
                daemon.emit("die", cid)
            else:
                daemon.running.add(cid)
                daemon.emit("start", cid)
        elif roll < 0.47 and live:
            cid = rng.choice(live)
            destroyed.add(cid)
            daemon.running.discard(cid)
            daemon.cpus.pop(cid, None)
            daemon.pending.pop(cid, None)
            if rng.random() < 0.85:
                daemon.emit("destroy", cid)  # else it vanishes without its event
        elif roll < 0.55 and daemon.pending:
            cid = rng.choice(sorted(daemon.pending))
            daemon.cpus[cid] = daemon.pending.pop(cid)
            daemon.emit("update", cid)
        elif daemon.queue:
            # the record reads events late: any number may be waiting
            for _ in range(rng.randint(1, len(daemon.queue))):
                record.observe(daemon.queue.pop(0))
                daemon.check(record, f"seed {seed} step {step} after an event")
            continue
        daemon.check(record, f"seed {seed} step {step} after a daemon step")
    while daemon.queue:
        record.observe(daemon.queue.pop(0))
        daemon.check(record, f"seed {seed} drain")
    return daemon.violations, record.moved, sum(1 for v in record.outcome.values() if v == "staging")


def probe_fuzz() -> None:
    violations: list[str] = []
    moved = staging = 0
    for seed in range(SEEDS):
        found, each_moved, each_staging = fuzz_once(seed)
        violations.extend(found)
        moved += each_moved
        staging += each_staging
    report(
        not violations and moved > 0,
        f"A1 fuzz {SEEDS} seeds with event lag, restarts, vanishing containers, applied/lost/"
        f"rejected moves and read timeouts: no shared job range, no unreserved user "
        f"(moved={moved} staging={staging} first={violations[:2]})",
    )


def probe_replayed_tail() -> None:
    daemon_cpus: dict[str, str] = {}
    moves: list[tuple[str, str]] = []

    def assign(cid: str, cpus: str) -> subprocess.CompletedProcess[str]:
        moves.append((cid[:1], cpus))
        if cid not in daemon_cpus:
            return done(1, err=f"Error: No such container: {cid}\n")
        daemon_cpus[cid] = cpus
        return done()

    def read(cid: str) -> subprocess.CompletedProcess[str]:
        if cid not in daemon_cpus:
            return done(1, err=f"Error: No such container: {cid}\n")
        return done(0, out=daemon_cpus[cid] + "\n")

    record = m.JobCpuRanges(BOUNDARY, RANGES, assign, read)
    old = "f" * 64
    raised = ""
    try:
        for action in ("create", "start", "die", "destroy"):
            record.observe(line(action, old))  # gone already: the previous workflow's tail
        new = "a" * 64
        daemon_cpus[new] = STAGING
        record.observe(line("create", new))
    except Exception as exc:  # noqa: BLE001
        raised = repr(exc)
    report(
        raised == "" and record.held == {"a" * 64: 0} and daemon_cpus["a" * 64] == "4-7"
        and record.outcome.get(old) == "gone",
        f"A2 replayed tail of a previous workflow (create/start/die/destroy of a removed "
        f"container) moves nothing that exists, frees its reservation, and the next container "
        f"still gets 4-7: held={ {k[:1]: v for k, v in record.held.items()} } "
        f"outcome_old={record.outcome.get(old)} raised={raised!r} summary={record.summary()!r}",
    )


def probe_reader_oserror() -> None:
    calls: list[str] = []

    def assign(cid: str, cpus: str) -> subprocess.CompletedProcess[str]:
        calls.append(cid[:1])
        raise OSError("docker binary vanished")

    record = m.JobCpuRanges(BOUNDARY, RANGES, assign, lambda cid: done(0, out=STAGING))

    class Proc:
        stdout = io.StringIO(line("create", "a" * 64) + line("create", "b" * 64))

    raised = ""
    try:
        m.read_job_cpu_events(Proc(), record)  # type: ignore[arg-type]
    except BaseException as exc:  # noqa: BLE001
        raised = repr(exc)
    report(
        raised == "" and calls == ["a"]
        and record.problems == ["the CPU-range monitor stopped reading events: docker binary vanished"],
        f"A3 a move raising OSError stops the reader as a recorded problem, raises nothing: "
        f"calls={calls} problems={record.problems} held={len(record.held)}",
    )


def probe_run_level_source() -> None:
    fixture = m.selftest_fixture()
    resolved = m.ValidatedRun(fixture.pr, fixture.repository, fixture.base)
    shipping = (TREE / m.WORKFLOWS["rtl-full"]).read_text(encoding="utf-8")
    # both matrix jobs (verilator-shards, yosys-shards) get the planted max-parallel
    anchor = "      fail-fast: false\n      matrix:\n"
    outcomes = {}
    for label, value, expect in (
        ("max-parallel 2", "2", "ranges:4-7 8-11"),
        ("max-parallel 3", "3", "ranges:4-7 8-11 12-15"),
        ("max-parallel 9", "9", "refused"),
        ("expression", "${{ inputs.width }}", "refused"),
    ):
        with tempfile.TemporaryDirectory(prefix="r632-4-root-") as raw:
            root = pathlib.Path(raw)
            target = root / m.WORKFLOWS["rtl-full"]
            target.parent.mkdir(parents=True)
            if shipping.count(anchor) != 2:
                outcomes[label] = ("anchor", expect)
                continue
            target.write_text(
                shipping.replace(anchor, f"      fail-fast: false\n      max-parallel: {value}\n"
                                 "      matrix:\n"),
                encoding="utf-8",
            )
            rc, printed = m.dry_run_transcript(resolved, "rtl-full", m.ReplaySlot(0), root)
        if "act-ci: REFUSED:" in printed:
            got = "refused"
        else:
            plan = [p for p in printed.splitlines() if "then moved to a free one of" in p]
            got = "ranges:" + " ".join(
                w.split("=", 1)[1] for w in plan[0].split("free one of ", 1)[1].split()
            ) if plan else f"no plan rc={rc}"
        outcomes[label] = (got, expect)
    report(
        all(got == expect for got, expect in outcomes.values()),
        f"A4 run-level dry run reads the materialized checkout's rtl-full, not the trusted "
        f"runner's: {outcomes}",
    )


def probe_spellings() -> None:
    matrix = {"matrix": {"n": ["1"]}}
    answers = {}
    for raw in ("04", "+4", "0x4", " ", "", "4 ", "1_0"):
        try:
            answers[raw] = m.job_container_width({"strategy": {**matrix, "max-parallel": raw}}, "j")
        except m.Refusal:
            answers[raw] = "refused"
    no_matrix = m.job_container_width({"strategy": {"max-parallel": "9"}}, "j")
    report(
        answers == {"04": 4, "+4": "refused", "0x4": "refused", " ": "refused", "": "refused",
                    "4 ": "refused", "1_0": "refused"} and no_matrix == 1,
        f"A5 max-parallel spellings: {answers}; no matrix with max-parallel 9 -> {no_matrix}",
    )


def main() -> int:
    with mock.patch.object(os, "cpu_count", return_value=128):
        probe_fuzz()
        probe_replayed_tail()
        probe_reader_oserror()
        with contextlib.redirect_stderr(io.StringIO()):
            probe_run_level_source()
        probe_spellings()
    failed = [label for ok, label in RESULTS if not ok]
    print("probes:", "PASS" if not failed else "FAIL " + "; ".join(f[:60] for f in failed))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

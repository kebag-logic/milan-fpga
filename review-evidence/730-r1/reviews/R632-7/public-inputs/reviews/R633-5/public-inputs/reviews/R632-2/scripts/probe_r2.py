"""Reviewer probes for PR #731 round 2 (issue #730), run against an act_ci.py tree.

Usage (inside a disposable boundary with no Docker socket and no network):
    python3 -I probe_r2.py <tree-root> [fuzz-runs]

Loads <tree-root>/scripts/act_ci.py as a module and drives only its pure
record (JobCpuRanges), its layout functions, and its monitor shutdown with
stand-in processes. Nothing here starts Docker, act, sudo or a network call.
Prints one PASS/FAIL line per probe and exits 1 if any probe fails.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import pathlib
import random
import subprocess
import sys
import threading
import time
from unittest import mock

ROOT = pathlib.Path(sys.argv[1]).resolve()
RUNS = int(sys.argv[2]) if len(sys.argv) > 2 else 3000
spec = importlib.util.spec_from_file_location("act_ci_under_review", ROOT / "scripts" / "act_ci.py")
act = importlib.util.module_from_spec(spec)
sys.modules["act_ci_under_review"] = act
spec.loader.exec_module(act)

RANGES = ("4-7", "8-11", "12-15", "16-19")
STAGING = "0-3"
TOKEN = "f" * 32
failures: list[str] = []


def report(name: str, ok: bool, detail: str = "") -> None:
    print(f"{'PASS' if ok else 'FAIL'} {name}{(': ' + detail) if detail else ''}", flush=True)
    if not ok:
        failures.append(name)


def boundary() -> object:
    """A minimal stand-in carrying only the owner token the record compares."""
    return type("B", (), {"token": TOKEN})()


def event(action: str, cid: str) -> str:
    actor = {"ID": cid, "Attributes": {act.DOCKER_OWNER_LABEL: TOKEN}}
    return json.dumps({"Type": "container", "Action": action, "Actor": actor}) + "\n"


def done(rc: int = 0, out: str = "", err: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess([], rc, out, err)


class Daemon:
    """An independent daemon model.

    `cpus` is each existing container's cpuset (stopped ones keep theirs);
    `pending` is an update the CLI gave up on that the daemon may still apply
    at any moment while the container exists. `events` is the daemon's ordered
    event log; the record reads it with a lag, so the daemon can be ahead.
    """

    def __init__(self, rng: random.Random, faults: bool) -> None:
        self.rng = rng
        self.faults = faults
        self.cpus: dict[str, str] = {}
        self.running: set[str] = set()
        self.pending: dict[str, str] = {}
        self.events: list[str] = []
        self.next_id = 0
        self.violations: list[str] = []
        self.record: object | None = None
        self.in_callback = False

    # --- act-side actions (may run while the reader is inside a CLI call) ---
    def create(self) -> None:
        cid = f"{self.next_id:064x}"
        self.next_id += 1
        self.cpus[cid] = STAGING
        self.events.append(event("create", cid))

    def start(self, cid: str) -> None:
        if cid in self.cpus and cid not in self.running:
            self.running.add(cid)
            self.events.append(event("start", cid))

    def die(self, cid: str) -> None:
        if cid in self.running:
            self.running.discard(cid)
            self.events.append(event("die", cid))

    def destroy(self, cid: str) -> None:
        if cid in self.cpus:
            self.running.discard(cid)
            self.cpus.pop(cid)
            self.pending.pop(cid, None)
            self.events.append(event("destroy", cid))

    def land(self, cid: str) -> None:
        if cid in self.pending and cid in self.cpus:
            self.cpus[cid] = self.pending.pop(cid)
            self.events.append(event("update", cid))

    def random_step(self) -> None:
        live = list(self.cpus)
        roll = self.rng.random()
        if roll < 0.25 or not live:
            if len(self.cpus) < 6:
                self.create()
        elif roll < 0.45:
            self.start(self.rng.choice(live))
        elif roll < 0.6:
            self.die(self.rng.choice(live))
        elif roll < 0.8:
            self.destroy(self.rng.choice(live))
        elif self.pending:
            self.land(self.rng.choice(list(self.pending)))
        self.check_invariant()

    def concurrent_steps(self) -> None:
        """Let act and the daemon move on while the reader waits on a CLI call."""
        for _ in range(self.rng.randrange(0, 3)):
            self.random_step()

    # --- the record's CLI seams ---
    def assign(self, cid: str, target: str) -> subprocess.CompletedProcess[str]:
        self.concurrent_steps()
        if cid not in self.cpus:
            return done(1, err=f"Error: No such container: {cid}\n")
        fault = self.rng.choice(("ok", "ok", "ok", "applied", "lost", "rejected")) if self.faults else "ok"
        if fault == "rejected":
            return done(1, err="Error response from daemon: busy\n")
        if fault == "lost":
            self.pending[cid] = target
            self.concurrent_steps()
            raise act.Refusal("job container CPU-range move timed out")
        self.cpus[cid] = target
        self.events.append(event("update", cid))
        self.check_invariant()
        self.concurrent_steps()
        if fault == "applied":
            raise act.Refusal("job container CPU-range move timed out")
        return done()

    def read(self, cid: str) -> subprocess.CompletedProcess[str]:
        self.concurrent_steps()
        if self.faults and self.rng.random() < 0.1:
            raise act.Refusal("job container CPU-range read timed out")
        if cid not in self.cpus:
            return done(1, err=f"Error: No such container: {cid}\n")
        answer = self.cpus[cid]
        self.concurrent_steps()  # the answer can be stale by the time it is used
        return done(0, out=answer + "\n")

    # --- the safety property ---
    def check_invariant(self) -> None:
        """No two existing containers can be (now or after a pending move lands) on one job range."""
        claims: dict[str, str] = {}
        for cid in self.cpus:
            for cpus in {self.cpus[cid], self.pending.get(cid, self.cpus[cid])}:
                if cpus in RANGES:
                    if cpus in claims and claims[cpus] != cid:
                        self.violations.append(f"{claims[cpus][-4:]} and {cid[-4:]} both on {cpus}")
                    claims[cpus] = cid


def fuzz(runs: int, faults: bool) -> tuple[int, list[str], int, int]:
    violations: list[str] = []
    moved_total = 0
    staged_total = 0
    for seed in range(runs):
        rng = random.Random(seed * 7919 + (1 if faults else 0))
        daemon = Daemon(rng, faults)
        record = act.JobCpuRanges(boundary(), RANGES, daemon.assign, daemon.read)
        consumed = 0
        for _ in range(60):
            daemon.random_step()
            # the reader consumes a random number of queued events (lag)
            for _ in range(rng.randrange(0, 3)):
                if consumed < len(daemon.events):
                    line = daemon.events[consumed]
                    consumed += 1
                    record.observe(line)
                    daemon.check_invariant()
        while consumed < len(daemon.events):
            record.observe(daemon.events[consumed])
            consumed += 1
            daemon.check_invariant()
        if len(set(record.held.values())) != len(record.held):
            violations.append(f"seed {seed}: one range reserved twice")
        if daemon.violations:
            violations.append(f"seed {seed}: {daemon.violations[0]}")
        moved_total += record.moved
        staged_total += sum(1 for v in record.outcome.values() if v == "staging")
    return runs, violations, moved_total, staged_total


def directed_restart() -> None:
    """create A, update A, start A, die A, create B, update B, start B, start A."""
    rng = random.Random(0)
    daemon = Daemon(rng, False)
    daemon.concurrent_steps = lambda: None  # type: ignore[method-assign]
    record = act.JobCpuRanges(boundary(), RANGES, daemon.assign, daemon.read)
    a, b = "a" * 64, "b" * 64
    seq = []
    daemon.cpus[a] = STAGING
    record.observe(event("create", a))
    seq.append(("create A", dict(record.held)))
    record.observe(event("update", a)); daemon.running.add(a)
    record.observe(event("start", a)); daemon.running.discard(a)
    record.observe(event("die", a))
    daemon.cpus[b] = STAGING
    record.observe(event("create", b))
    record.observe(event("update", b)); daemon.running.add(b)
    record.observe(event("start", b)); daemon.running.add(a)
    record.observe(event("start", a))
    daemon.check_invariant()
    report(
        "P1 restart sequence: A and B never share a range; A keeps 4-7 across die/start, B gets 8-11",
        daemon.cpus[a] == "4-7" and daemon.cpus[b] == "8-11" and not daemon.violations
        and record.held == {a: 0, b: 1},
        f"cpus={ {k[:1]: v for k, v in daemon.cpus.items()} } held={ {k[:1]: v for k, v in record.held.items()} }",
    )


def directed_applied_then_timeout() -> None:
    """The update is applied on the daemon, then the CLI times out; the next create must not get that range."""
    a, b = "a" * 64, "b" * 64
    cpus = {a: STAGING}
    reads: list[str] = []

    def assign(cid: str, target: str) -> subprocess.CompletedProcess[str]:
        if cid == a:
            cpus[a] = target
            raise act.Refusal("job container CPU-range move timed out")
        cpus[cid] = target
        return done()

    def read(cid: str) -> subprocess.CompletedProcess[str]:
        reads.append(cid[:1])
        return done(0, out=cpus[cid] + "\n")

    record = act.JobCpuRanges(boundary(), RANGES, assign, read)
    record.observe(event("create", a))
    held_after_a = dict(record.held)
    cpus[b] = STAGING
    record.observe(event("create", b))
    report(
        "P2 update applied then CLI timeout: A's target 4-7 stays reserved (inspect shows it there); B gets 8-11",
        held_after_a == {a: 0} and record.held == {a: 0, b: 1} and cpus == {a: "4-7", b: "8-11"}
        and record.outcome[a] == "moved" and "a" in reads
        and any("reported job container CPU-range move timed out, but docker inspect shows it there" in p
                for p in record.problems),
        f"held={record.held} problems={record.problems}",
    )
    # and the variant where inspect also cannot answer: range stays reserved
    cpus2 = {a: STAGING}

    def assign2(cid: str, target: str) -> subprocess.CompletedProcess[str]:
        cpus2[cid] = target
        if cid == a:
            raise act.Refusal("job container CPU-range move timed out")
        return done()

    def read2(cid: str) -> subprocess.CompletedProcess[str]:
        if cid == a:
            raise act.Refusal("job container CPU-range read timed out")
        return done(0, out=cpus2[cid] + "\n")

    record2 = act.JobCpuRanges(boundary(), RANGES, assign2, read2)
    record2.observe(event("create", a))
    cpus2[b] = STAGING
    record2.observe(event("create", b))
    record2.observe(event("die", a))
    record2.observe(event("create", "c" * 64))
    report(
        "P2b applied, CLI timeout, inspect timeout: 4-7 stays reserved through die; later creates get 8-11, 12-15",
        record2.held == {a: 0, b: 1, "c" * 64: 2},
        f"held={record2.held}",
    )


def directed_slot0_small_host() -> None:
    """Slot 0 refuses a host without the derived ranges, before the slot is entered."""
    answers = {}
    for host in (4, 7, 8, 19, 20):
        for conc in (1, 4):
            with mock.patch.object(os, "cpu_count", return_value=host):
                try:
                    answers[host, conc] = act.job_cpu_ranges(0, conc)
                except act.Refusal as exc:
                    answers[host, conc] = "REFUSED: " + str(exc)
    ok = (
        all(str(answers[h, 4]).startswith("REFUSED") for h in (4, 7, 8, 19))
        and answers[20, 4] == RANGES
        and all(str(answers[h, 1]).startswith("REFUSED") for h in (4, 7))
        and answers[8, 1] == ("4-7",)
    )
    report("P3a slot 0 job_cpu_ranges refuses 4/7/8/19 CPUs for 4 containers and 4/7 for 1", ok, repr(answers[19, 4]))
    # Run level: the runner's own dry-run harness (real run_validation, shipping
    # rtl-full, slot 0) with its pinned 128-CPU host replaced by HOST CPUs, and
    # the slot entry spied, so a refusal must come before the slot is entered.
    real_patch_object = mock.patch.object

    for host, expect_refusal in ((19, True), (20, False)):
        entered: list[str] = []

        def patch_object(target, attribute, *args, host=host, **kwargs):
            if target is os and attribute == "cpu_count":
                kwargs["return_value"] = host
            return real_patch_object(target, attribute, *args, **kwargs)

        shim = type("MockShim", (), {})()
        shim.patch = type("PatchShim", (), {})()
        shim.patch.object = patch_object
        shim.patch.multiple = mock.patch.multiple
        original_multiple = mock.patch.multiple

        def multiple(target, **fakes):
            if "replay_slot" in fakes:
                inner = fakes["replay_slot"]

                @contextlib.contextmanager
                def spy(selected, **kwargs):
                    entered.append(f"slot {selected.number}")
                    with inner(selected, **kwargs):
                        yield

                fakes["replay_slot"] = spy
            return original_multiple(target, **fakes)

        shim.patch.multiple = multiple
        fixture = act.selftest_fixture()
        resolved = act.ValidatedRun(fixture.pr, fixture.repository, fixture.base)
        with mock.patch.object(act, "mock", shim), contextlib.redirect_stdout(io.StringIO()):
            rc, printed = act.dry_run_transcript(resolved, "rtl-full", act.ReplaySlot(0), ROOT)
        refused = "act-ci: REFUSED: replay slot 0 needs CPUs 0-19 for 4 concurrent job container(s), but this host has 19" in printed
        if expect_refusal:
            ok = rc is None and refused and entered == []
        else:
            ok = rc == act.RC_OK and entered == ["slot 0"] and "moved to a free one of --cpuset-cpus=4-7" in printed
        report(
            f"P3b run level, slot 0 dry run of shipping rtl-full on a {host}-CPU host: "
            + ("Refusal before the slot is entered" if expect_refusal else "runs, slot entered, ranges 4-7.."),
            ok,
            f"rc={rc} entered={entered} refused_line={refused}",
        )


def directed_reap_failure() -> None:
    """Reap failure in containment: reader joined, pipe closed, stream contained before the monitor returns; failures kept."""
    trail: list[str] = []
    body_done = threading.Event()
    contained = threading.Event()

    class Pipe:
        closed = False

        def __iter__(self):
            body_done.wait(5)
            yield event("create", "a" * 64)
            trail.append("stream ended" if contained.wait(5) else "stream gave up")

        def close(self):
            self.closed = True
            trail.append("pipe closed")

    class Stream:
        pid = 4242
        returncode = None

        def __init__(self):
            self.stdout = Pipe()

        def poll(self):
            return None

    stream = Stream()

    def terminate(process, *, use_sudo, primary):
        trail.append("contained")
        contained.set()
        raise act.Refusal("cannot reap interrupted host process leader")

    def run_docker(arguments, **_kwargs):
        if list(arguments[:2]) == ["container", "update"]:
            time.sleep(0.3)
            trail.append("moved")
        return done(0, out="4-7\n")

    body_error = RuntimeError("original body failure")
    caught: BaseException | None = None
    ctx = act.CommandContext(use_sudo=False, cwd=pathlib.Path("/tmp"), env={"PATH": "/usr/bin"})
    with mock.patch.multiple(act, run_docker=run_docker, require_tool=lambda name: f"/usr/bin/{name}"):
        try:
            with act.job_cpu_range_monitor(
                boundary(), ("4-7",), context=ctx,
                seams=act.ProcessSeams(popen=lambda *a, **k: stream, terminate_group=terminate),
            ):
                trail.append("body ended")
                body_done.set()
                raise body_error
        except BaseException as exc:  # noqa: BLE001 - the probe records whatever escapes
            caught = exc
    trail.append("monitor exited")
    alive = [t.name for t in threading.enumerate() if t.name == "act-ci-cpu-range-monitor"]
    chain = []
    cur = caught
    while cur is not None and len(chain) < 5:
        chain.append(f"{type(cur).__name__}({cur})")
        cur = cur.__cause__ or cur.__context__
    ok = (
        trail.index("contained") < trail.index("stream ended") < trail.index("pipe closed") < trail.index("monitor exited")
        and trail.index("moved") < trail.index("monitor exited")
        and not alive
        and isinstance(caught, act.Refusal)
        and "original body failure" in " ".join(chain)
    )
    report(
        "P4 injected reap failure with a failing body: containment, reader end, pipe close all precede exit; "
        "reap Refusal raised with the body failure kept in its chain",
        ok,
        f"trail={trail} chain={chain} alive={alive}",
    )


def directed_derivation() -> None:
    import tempfile
    rows = []
    with tempfile.TemporaryDirectory() as raw:
        root = pathlib.Path(raw)
        for label, strategy, expect in (
            ("default", "      matrix:\n        n: [1, 2, 3, 4, 5]\n", 4),
            ("max-parallel 2", "      max-parallel: 2\n      matrix:\n        n: [1, 2, 3]\n", 2),
            ("max-parallel 5", "      max-parallel: 5\n      matrix:\n        n: [1, 2, 3, 4, 5]\n", "refuse-range"),
            ("expression", "      max-parallel: ${{ inputs.n }}\n      matrix:\n        n: [1, 2]\n", "refuse"),
            ("quoted '3'", "      max-parallel: '3'\n      matrix:\n        n: [1, 2, 3]\n", 3),
            ("hex 0x4", "      max-parallel: 0x4\n      matrix:\n        n: [1, 2]\n", "refuse"),
        ):
            path = root / act.WORKFLOWS["rtl-full"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "name: x\non: pull_request\njobs:\n  j:\n    runs-on: ubuntu-latest\n    strategy:\n"
                + strategy + "    steps:\n      - run: true\n",
                encoding="utf-8",
            )
            try:
                got = act.replay_container_concurrency(root, ("rtl-full",))
                if expect == "refuse-range":
                    try:
                        with mock.patch.object(os, "cpu_count", return_value=128):
                            act.job_cpu_ranges(0, got)
                        got = f"{got} (not refused)"
                    except act.Refusal:
                        got = "refuse-range"
            except act.Refusal:
                got = "refuse"
            rows.append((label, got, expect))
    report("P7 derivation from a workflow file: default 4, literal, too wide refused, unreadable refused",
           all(g == e for _l, g, e in rows), repr(rows))
    shipping = {name: act.replay_container_concurrency(ROOT, (name,)) for name in act.WORKFLOWS}
    report("P7b shipping workflows derive rtl-full 4, others 1", shipping.get("rtl-full") == 4
           and all(v == 1 for k, v in shipping.items() if k != "rtl-full"), repr(shipping))


def directed_layout() -> None:
    host = 64 * 20
    named = []
    with mock.patch.object(os, "cpu_count", return_value=host):
        for slot in range(act.SLOT_LIMIT + 1):
            named.append((f"s{slot} staging", act.container_cpuset(slot)))
            named += [(f"s{slot} r{i}", r) for i, r in enumerate(act.job_cpu_ranges(slot, 4))]
    cpus = []
    for _o, text in named:
        a, b = (int(x) for x in text.split("-"))
        cpus.append(set(range(a, b + 1)))
    disjoint = sum(len(c) for c in cpus) == len(set().union(*cpus))
    widths = {len(c) for c in cpus}
    blocks = all(
        min(min(c) for (o, _t), c in zip(named, cpus) if o.startswith(f"s{s} ")) == 20 * s
        and max(max(c) for (o, _t), c in zip(named, cpus) if o.startswith(f"s{s} ")) == 20 * s + 19
        for s in range(act.SLOT_LIMIT + 1)
    )
    report("P8 independent layout check: slots 0-63 x (staging + 4), disjoint, every range 4 wide (nproc 4), slot N = 20N..20N+19",
           disjoint and widths == {4} and blocks, f"ranges={len(named)} widths={widths}")


def main() -> int:
    directed_restart()
    directed_applied_then_timeout()
    directed_slot0_small_host()
    directed_reap_failure()
    directed_derivation()
    directed_layout()
    runs, violations, moved, staged = fuzz(RUNS, faults=False)
    report(f"P9 fuzz without CLI faults: {runs} random interleavings with event lag and concurrent act steps; "
           "no two existing containers ever on one job range", not violations,
           f"moved={moved} staging={staged} first={violations[:2]}")
    runs, violations, moved, staged = fuzz(RUNS, faults=True)
    report(f"P10 fuzz with applied/lost/rejected moves and read timeouts: {runs} interleavings; "
           "no two existing containers (with pending moves) ever on one job range", not violations,
           f"moved={moved} staging={staged} first={violations[:2]}")
    print(f"probes: {'PASS' if not failures else 'FAIL ' + ', '.join(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

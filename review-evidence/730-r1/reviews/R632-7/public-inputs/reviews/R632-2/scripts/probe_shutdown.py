"""Reviewer probes of the CPU-range monitor's shutdown guarantees (PR #731 round 2).

Usage (inside a disposable boundary): python3 -I probe_shutdown.py <tree-root>

S1 a reader that outlives the bounded join is waited for (containment hold), never abandoned;
S2 a failed join is retried while the reader is still running after the retry pause;
S3 with a reap failure and a join failure, the first (the reap failure) is raised;
S4 cleanup signals are blocked while containment and the join run.
Exits 1 if any probe fails.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import signal
import subprocess
import sys
import threading
import time

ROOT = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("act_ci_under_review", ROOT / "scripts" / "act_ci.py")
act = importlib.util.module_from_spec(spec)
sys.modules["act_ci_under_review"] = act
spec.loader.exec_module(act)
failures: list[str] = []


def report(name: str, ok: bool, detail: str) -> None:
    print(f"{'PASS' if ok else 'FAIL'} {name}: {detail}", flush=True)
    if not ok:
        failures.append(name)


def record() -> object:
    b = type("B", (), {"token": "f" * 32})()
    return act.JobCpuRanges(b, ("4-7",), lambda *a: subprocess.CompletedProcess([], 0, "", ""),
                            lambda *a: subprocess.CompletedProcess([], 0, "", ""))


def worker(seconds: float, trail: list[str]) -> threading.Thread:
    thread = threading.Thread(target=lambda: (time.sleep(seconds), trail.append("reader ended")))
    thread.start()
    return thread


class FlakyJoin:
    def __init__(self, thread: threading.Thread) -> None:
        self.thread, self.ident, self.failed = thread, thread.ident, False

    def join(self, timeout: float | None = None) -> None:
        if not self.failed:
            self.failed = True
            raise RuntimeError("join interrupted")
        self.thread.join(timeout)

    def is_alive(self) -> bool:
        return self.thread.is_alive()


class Stream:
    pid = 4242
    returncode = None

    def __init__(self) -> None:
        self.stdout = io.StringIO("")

    def poll(self) -> None:
        return None


def s1_hold() -> None:
    trail: list[str] = []
    thread = worker(2.0, trail)
    rec = record()
    err = io.StringIO()
    old = act.DOCKER_COMMAND_TIMEOUT
    act.DOCKER_COMMAND_TIMEOUT = -9.5  # bounded wait = 0.5 s
    try:
        start = time.monotonic()
        with contextlib.redirect_stderr(err):
            result = act.join_job_cpu_reader(thread, rec, 4242)
        elapsed = time.monotonic() - start
    finally:
        act.DOCKER_COMMAND_TIMEOUT = old
    report("S1 reader alive past the bounded wait is held for, not abandoned",
           result is None and trail == ["reader ended"] and elapsed >= 1.9
           and "the CPU-range monitor survived its bounded shutdown" in rec.problems
           and "containment hold" in err.getvalue(),
           f"elapsed={elapsed:.2f}s trail={trail} problems={rec.problems}")


def s2_retry() -> None:
    trail: list[str] = []
    thread = worker(1.0, trail)
    start = time.monotonic()
    result = act.join_job_cpu_reader(FlakyJoin(thread), record(), 4242)
    elapsed = time.monotonic() - start
    report("S2 a failed join is retried while the reader still runs after the retry pause",
           isinstance(result, RuntimeError) and trail == ["reader ended"] and elapsed >= 0.9,
           f"elapsed={elapsed:.2f}s trail={trail} returned={result!r}")


def s3_first_failure() -> None:
    trail: list[str] = []
    thread = worker(0.6, trail)
    ctx = act.CommandContext(use_sudo=False, cwd=pathlib.Path("/tmp"), env={"PATH": "/usr/bin"})

    def terminate(*_a, **_k):
        raise act.Refusal("reap failed")

    raised = None
    try:
        act.stop_job_cpu_range_monitor(Stream(), FlakyJoin(thread), record(), context=ctx,
                                       seams=act.ProcessSeams(terminate_group=terminate))
    except BaseException as exc:  # noqa: BLE001
        raised = exc
    report("S3 reap failure then join failure: the first (reap) is raised, after the reader ended",
           isinstance(raised, act.Refusal) and str(raised) == "reap failed" and trail == ["reader ended"],
           f"raised={raised!r} trail={trail}")


def s4_masked() -> None:
    seen: list[bool] = []
    ctx = act.CommandContext(use_sudo=False, cwd=pathlib.Path("/tmp"), env={"PATH": "/usr/bin"})

    def terminate(*_a, **_k):
        mask = signal.pthread_sigmask(signal.SIG_BLOCK, set())
        seen.append(all(s in mask for s in act.CLEANUP_SIGNALS))

    act.stop_job_cpu_range_monitor(Stream(), None, record(), context=ctx,
                                   seams=act.ProcessSeams(terminate_group=terminate))
    report("S4 cleanup signals are blocked during containment", seen == [True], f"seen={seen}")


s1_hold()
s2_retry()
s3_first_failure()
s4_masked()
print(f"shutdown probes: {'PASS' if not failures else 'FAIL ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)

#!/usr/bin/env python3
"""Reviewer probe R632-6: the diagnostic of a signal that is itself the act boundary's failure.

Usage: python3 -I probe_r6_interrupt_diag.py <tree>
Through the real CPU-range monitor (inert stream stand-in) and the real act
boundary, inside run_with_cleanup_signals:
  A  a first signal arrives while the stand-in act runs (signals unblocked);
  B  a first signal is pending before the boundary opens (held by the monitor).
With no earlier failure, each must exit 128 + signal and print exactly the
conventional interrupt diagnostic, and no "act boundary closing was
interrupted" line, since nothing was propagating before the signal.
Exits 0 only if all six cases (A, B x INT/TERM/HUP) hold.
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
from unittest import mock

TREE = pathlib.Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("act_ci_r6_diag", TREE / "scripts" / "act_ci.py")
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)

fixture = m.selftest_fixture()
fixture_run = m.ValidatedRun(fixture.pr, fixture.repository, fixture.base)
failures = 0


def case(signum: int, where: str) -> tuple[bool, str]:
    trail: list[str] = []
    stream = m.FakeEventStream([], trail=trail)
    stream.stdout = m.HeldEventPipe([], stream.contained, stream.contained, trail)
    context = m.CommandContext(use_sudo=False, cwd=m.ROOT, env={})
    started: list[int] = []
    stderr = io.StringIO()

    def act_process(*_args: object, **_kwargs: object) -> subprocess.CompletedProcess[object]:
        started.append(1)
        if where == "during act":
            signal.raise_signal(signum)
        return subprocess.CompletedProcess([], 0)

    def contain(*_args: object, **_kwargs: object) -> None:
        trail.append("contained")
        stream.contained.set()

    def action() -> int:
        with m.job_cpu_range_monitor(
            m.DockerBoundary(token="c" * 32, name="r6-diag-probe"), ("4-7",), context=context,
            seams=m.ProcessSeams(popen=lambda *_a, **_k: stream, terminate_group=contain),
        ):
            if where == "pending before act":
                signal.raise_signal(signum)
            return m.execute_act_boundary(
                ["act"], run=fixture_run, context=context, integrity_check=lambda: None,
                seams=m.SpawnSeams(query=lambda *_a: fixture.pr, run_process=act_process),
            )

    incoming = signal.pthread_sigmask(signal.SIG_BLOCK, ())
    with mock.patch.object(m, "require_tool", m.fake_host_tool), contextlib.redirect_stderr(stderr):
        try:
            outcome: object = m.run_with_cleanup_signals(action)
        except BaseException as exc:  # noqa: BLE001 - recorded as the outcome
            outcome = exc
        finally:
            pending = m.settle_cleanup_signals(incoming)
            stream.contained.set()
            for thread in threading.enumerate():
                if thread.name == "act-ci-cpu-range-monitor":
                    thread.join(timeout=10)
    name = signal.Signals(signum).name
    text = stderr.getvalue()
    expected_started = [1] if where == "during act" else []
    ok = (
        outcome == 128 + signum
        and text == f"act-ci: interrupted by {name} after cleanup\n"
        and started == expected_started
        and "contained" in trail and stream.stdout.closed and not pending
    )
    return ok, f"outcome={outcome!r} started={started} stderr={text!r} trail={trail}"


for where in ("during act", "pending before act"):
    for signum in m.CLEANUP_SIGNALS:
        ok, evidence = case(signum, where)
        failures += 0 if ok else 1
        print(f"  {'ok  ' if ok else 'FAIL'} first {signal.Signals(signum).name} {where}, no earlier failure: "
              f"exit 128+signal, only the interrupt diagnostic, containment done ({evidence})")
print(f"probe_r6_interrupt_diag: {'PASS' if not failures else 'FAIL'} ({failures} failure(s))")
sys.exit(1 if failures else 0)

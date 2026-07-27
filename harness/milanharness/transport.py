# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
#
#! Transport: run things on the jump host, the controller host and the boards.
#!
#! Three facts about this bench shape the whole module:
#!
#!   1. **A board has no `scp`** (dropbear). Scripts are pushed by piping them
#!      into a remote shell: `ssh <board> 'sh -s' < script`.
#!   2. **A board has no Python.** Board-side steps are POSIX `sh` + `devmem`
#!      (and `dd`/`od` for block reads); all analysis happens on the host.
#!   3. **A campaign runs for days.** Reboots, host disconnects and network
#!      blips are NORMAL, not exceptional: every call retries with backoff and
#!      records the outage. Exhausting the budget is `Outage`, which the runner
#!      turns into **BLOCKED** - not FAILED, because the device did not fail,
#!      the harness could not reach it.

from __future__ import annotations

import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path


class Outage(Exception):
    """The endpoint stayed unreachable past the retry budget -> BLOCKED."""

    def __init__(self, target: str, seconds: float, attempts: int, last: str):
        super().__init__(
            f"{target} unreachable after {attempts} attempts / {seconds:.0f}s: {last}")
        self.target, self.seconds, self.attempts, self.last = (
            target, seconds, attempts, last)


class StepTimeout(Exception):
    """One step exceeded its own timeout. Fails THAT step, never the run."""


@dataclass
class Result:
    rc: int
    out: str
    err: str
    seconds: float
    attempts: int
    outage_s: float = 0.0

    @property
    def ok(self) -> bool:
        return self.rc == 0

    def lines(self) -> list[str]:
        return [l for l in self.out.splitlines() if l.strip()]


#: rc values that mean "could not reach it", as opposed to "it ran and failed".
#: 255 is ssh's own error; 124 is `timeout(1)`'s; 127 is command-not-found on
#: the far side, which for a jump-host hop also means we never landed.
_UNREACHABLE_RC = {255, 124}


class Transport:
    """Runs commands locally or over ssh, with retry/backoff and outage records.

    `on_outage` is called with a dict for every retry, so the runner can append
    a JSONL record: a days-long run must be able to say afterwards *when* the
    bench went away and for how long.
    """

    def __init__(self, cfg, *, on_outage=None, runner=None):
        self.cfg = cfg
        self.ssh = cfg.get("exec", "ssh", "ssh")
        self.ssh_opts = list(cfg.get("exec", "ssh_opts", []))
        self.default_timeout = int(cfg.get("exec", "command_timeout_s", 120))
        r = cfg.section("retry")
        self.attempts = int(r.get("attempts", 6))
        self.backoff0 = float(r.get("backoff_initial_s", 2.0))
        self.backoff_max = float(r.get("backoff_max_s", 60.0))
        self.outage_budget = float(r.get("outage_budget_s", 1800))
        self.jump = cfg.get("jump", "host", "")
        self.on_outage = on_outage
        #: Injection point for the mock. Signature: (argv, timeout, stdin) -> Result
        self._runner = runner or _local_run

    # ------------------------------------------------------------- argv build
    def _ssh_argv(self, host: str, via_jump: bool, remote_cmd: str) -> list[str]:
        argv = [self.ssh, *self.ssh_opts]
        if via_jump and self.jump:
            argv += ["-J", self.jump]
        argv += [host, remote_cmd]
        return argv

    # ------------------------------------------------------------------- api
    def local(self, argv: list[str], *, timeout: int | None = None,
              stdin: str = "") -> Result:
        """Run something on THIS host (the behave suite, analysis helpers).

        Deliberately bypasses the injected runner: a dry run mocks the BENCH,
        not the host. Mocking a host-side tool would only prove the mock works.
        """
        saved, self._runner = self._runner, _local_run
        try:
            return self._attempt("local", argv, timeout, stdin, retry=False)
        finally:
            self._runner = saved

    def run(self, host: str, cmd: str, *, via_jump: bool = True,
            timeout: int | None = None, stdin: str = "",
            retry: bool = True) -> Result:
        """Run one shell command on `host`. Survives reboots and blips."""
        argv = self._ssh_argv(host, via_jump, cmd)
        return self._attempt(host, argv, timeout, stdin, retry=retry)

    def push_sh(self, host: str, script: Path | str, *, via_jump: bool = True,
                args: list[str] | None = None, timeout: int | None = None) -> Result:
        """Push a POSIX sh script to a board and run it. The no-`scp` path.

        Arguments go through `sh -s -- <args>` so a board-side script keeps its
        normal `$1..$n`, and every argument is `shlex.quote`d here.
        """
        body = Path(script).read_text(encoding="utf-8") if _is_path(script) else str(script)
        tail = ""
        if args:
            tail = " -- " + " ".join(shlex.quote(str(a)) for a in args)
        return self.run(host, f"sh -s{tail}", via_jump=via_jump,
                        timeout=timeout, stdin=body)

    def push_sh_detached(self, host: str, script: Path | str, *,
                         via_jump: bool = True, args: list[str] | None = None,
                         tag: str = "step", timeout: int | None = None) -> Result:
        """Run a board script DETACHED, read the verdict back afterwards.

        Some steps cut the very session that drives them - a link event, a MAC
        loopback, a MAC reinit. Those must not depend on the ssh channel
        surviving: the script is written to the board, started with `setsid` and
        its output redirected to a file, and the caller polls
        `read_detached(host, tag)` later.
        """
        body = Path(script).read_text(encoding="utf-8") if _is_path(script) else str(script)
        remote = f"/tmp/mh-{tag}"
        tail = ""
        if args:
            tail = " " + " ".join(shlex.quote(str(a)) for a in args)
        launcher = (
            f"cat > {remote}.sh && chmod +x {remote}.sh && "
            f"rm -f {remote}.done {remote}.out && "
            f"(setsid sh {remote}.sh{tail} > {remote}.out 2>&1; "
            f" echo $? > {remote}.done) < /dev/null > /dev/null 2>&1 & "
            f"echo DETACHED {remote}"
        )
        return self.run(host, launcher, via_jump=via_jump, timeout=timeout,
                        stdin=body)

    def read_detached(self, host: str, tag: str, *, via_jump: bool = True,
                      wait_s: float = 120.0, poll_s: float = 5.0) -> Result:
        """Poll a detached step to completion. Missing verdict = StepTimeout."""
        remote = f"/tmp/mh-{tag}"
        deadline = time.monotonic() + wait_s
        last = Result(1, "", "not started", 0.0, 0)
        while time.monotonic() < deadline:
            r = self.run(host, f"cat {remote}.done 2>/dev/null; echo ---; "
                               f"cat {remote}.out 2>/dev/null",
                         via_jump=via_jump, timeout=60)
            head, _, body = r.out.partition("---")
            code = head.strip()
            if code:
                return Result(int(code) if code.lstrip("-").isdigit() else 1,
                              body.strip(), r.err, r.seconds, r.attempts,
                              r.outage_s)
            last = r
            time.sleep(poll_s)
        raise StepTimeout(
            f"detached step {tag!r} on {host} produced no verdict in {wait_s:.0f}s "
            f"(last output: {last.out[-200:]!r})")

    # -------------------------------------------------------------- internals
    def _attempt(self, target: str, argv: list[str], timeout: int | None,
                 stdin: str, *, retry: bool) -> Result:
        tmo = timeout or self.default_timeout
        attempts = self.attempts if retry else 1
        backoff = self.backoff0
        started = time.monotonic()
        outage_s = 0.0
        last = ""
        for n in range(1, attempts + 1):
            t0 = time.monotonic()
            res = self._runner(argv, tmo, stdin)
            res.attempts = n
            res.seconds = time.monotonic() - t0
            res.outage_s = outage_s
            if res.rc not in _UNREACHABLE_RC:
                return res
            last = (res.err or res.out).strip()[-200:]
            outage_s = time.monotonic() - started
            if self.on_outage:
                self.on_outage({"target": target, "attempt": n, "rc": res.rc,
                                "outage_s": round(outage_s, 1), "detail": last})
            if n == attempts or outage_s > self.outage_budget:
                raise Outage(target, outage_s, n, last)
            time.sleep(min(backoff, self.backoff_max))
            backoff = min(backoff * 2, self.backoff_max)
        raise Outage(target, time.monotonic() - started, attempts, last)


def _is_path(x) -> bool:
    if isinstance(x, Path):
        return True
    return isinstance(x, str) and ("\n" not in x) and Path(x).is_file()


def _local_run(argv: list[str], timeout: int, stdin: str) -> Result:
    try:
        p = subprocess.run(argv, input=stdin, capture_output=True, text=True,
                           timeout=timeout)
        return Result(p.returncode, p.stdout, p.stderr, 0.0, 1)
    except subprocess.TimeoutExpired:
        # 124 is `timeout(1)`'s convention; reuse it so one rc means "no answer".
        return Result(124, "", f"timed out after {timeout}s", float(timeout), 1)
    except FileNotFoundError as exc:
        return Result(127, "", str(exc), 0.0, 1)

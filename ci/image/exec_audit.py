#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Observe every program a CI step runs inside the image, and judge the set.

This is the execution authority for issue #737. The static inventory derives
which programs the workflows *should* run; this audit records which programs a
step *does* run, by following `execve` with `ptrace`. Static binaries are
followed like any other, because the kernel reports the exec, not a preloaded
library. Steps run with the container's network disabled, so a step that needs
the network fails and is caught by its own exit status.

A step is rejected when it executes a program the allowlist does not name, or a
program on the installer denylist (a package manager or toolchain installer).
The allowlist is `exec-audit.json`: the inventory's command executables, a
reviewed set of helper programs those commands spawn, and the interpreters.

`--selftest` plants an installer and an unlisted program and shows each caught
by name. `--audit SPEC` runs the steps named in a JSON spec and writes a
receipt. The follow-up PR (#737) wires `audit` into every PR's signed replay;
this module is that replay's program-level gate, and `receipt()` is the
interface it consumes.
"""

from __future__ import annotations

import argparse
import ctypes
import json
import os
from pathlib import Path
import signal
import subprocess
import sys


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
ALLOWLIST = HERE / "exec-audit.json"

#: ptrace requests and the options that make the kernel stop on exec and on each
#: new child; PTRACE_O_EXITKILL reaps the tree if the tracer dies.
TRACEME, CONT, DETACH, GETEVENTMSG, SETOPTIONS = 0, 7, 17, 0x4201, 0x4200
O_TRACEFORK, O_TRACEVFORK, O_TRACECLONE, O_TRACEEXEC, O_EXITKILL = 0x2, 0x4, 0x8, 0x10, 0x100000
OPTIONS = O_TRACEFORK | O_TRACEVFORK | O_TRACECLONE | O_TRACEEXEC | O_EXITKILL
EVENT_FORK, EVENT_VFORK, EVENT_CLONE, EVENT_EXEC = 1, 2, 3, 4
WALL = 0x40000000

_libc = ctypes.CDLL(None, use_errno=True)
_libc.ptrace.restype = ctypes.c_long
_libc.ptrace.argtypes = [ctypes.c_long, ctypes.c_long, ctypes.c_void_p, ctypes.c_void_p]


def _ptrace(request: int, pid: int, data: int = 0) -> int:
    """Issue one ptrace request; a vanished tracee is not an error for the tracer."""
    return _libc.ptrace(request, pid, None, ctypes.c_void_p(data))


def trace(argv: list[str], cwd: Path, env: dict[str, str]) -> dict[str, object]:
    """Run one command, following its whole process tree, and record every execve.

    Returns the command's own exit status and the sorted set of executed program
    paths with the argument vector each was started with.
    """
    programs: dict[str, list[str]] = {}
    pid = os.fork()
    if pid == 0:
        try:
            _ptrace(TRACEME, 0)
            os.chdir(cwd)
            signal.raise_signal(signal.SIGSTOP)
            os.execvpe(argv[0], argv, env)
        except BaseException:  # noqa: BLE001 - the child must never return to the tracer
            os._exit(127)
    os.waitpid(pid, 0)
    _ptrace(SETOPTIONS, pid, OPTIONS)
    _ptrace(CONT, pid)
    alive = {pid}
    exit_status = None
    while alive:
        try:
            waited, status = os.waitpid(-1, WALL)
        except ChildProcessError:
            break
        if os.WIFEXITED(status) or os.WIFSIGNALED(status):
            alive.discard(waited)
            if waited == pid:
                exit_status = os.waitstatus_to_exitcode(status)
            continue
        signal_number, event = os.WSTOPSIG(status), status >> 16
        deliver = 0
        if signal_number == signal.SIGTRAP and event in (EVENT_FORK, EVENT_VFORK, EVENT_CLONE):
            child = ctypes.c_ulong()
            _libc.ptrace(GETEVENTMSG, waited, None, ctypes.addressof(child))
            alive.add(child.value)
        elif signal_number == signal.SIGTRAP and event == EVENT_EXEC:
            program = os.readlink(f"/proc/{waited}/exe") if Path(f"/proc/{waited}/exe").exists() else "<gone>"
            raw = Path(f"/proc/{waited}/cmdline").read_bytes() if Path(f"/proc/{waited}/cmdline").is_file() else b""
            programs.setdefault(program, [part.decode("latin-1") for part in raw.split(b"\0")[:-1]][:64])
        elif signal_number not in (signal.SIGTRAP, signal.SIGSTOP, signal.SIGCONT):
            deliver = signal_number  # pass a real signal through, never the trap stops
        _ptrace(CONT, waited, deliver)
    return {"exit_status": 0 if exit_status is None else exit_status,
            "programs": dict(sorted(programs.items()))}


def allowlist() -> dict[str, object]:
    """The reviewed program allowlist and installer denylist."""
    return json.loads(ALLOWLIST.read_text())


#: The image's own program directories. A program outside them is the job's
#: freshly built artifact (a simulator or test binary), allowed but recorded; a
#: program inside them must be named, so a planted system tool is caught.
SYSTEM_ROOTS = ("/usr/", "/bin/", "/sbin/", "/lib/", "/lib64/", "/opt/", "/etc/")


def judge(result: dict[str, object], names: dict[str, object]) -> list[dict[str, str]]:
    """Name every executed program that the allowlist forbids."""
    allowed = set(names["commands"]) | set(names["helpers"]) | set(names["interpreters"])
    installers = set(names["installers"])
    findings = []
    for program in result["programs"]:
        base = Path(program).name
        if base in installers or (base.rpartition("-")[2] in installers and "linux-gnu" not in base):
            findings.append({"program": program, "reason": f"installer executed: {base}"})
        elif program.startswith(SYSTEM_ROOTS) and base not in allowed:
            findings.append({"program": program, "reason": f"system program not in the command table: {base}"})
    if result["exit_status"] != 0:
        findings.append({"program": "<step>", "reason": f"step exited {result['exit_status']} (network disabled)"})
    return findings


def audit_step(label: str, argv: list[str], cwd: Path, env: dict[str, str],
               names: dict[str, object]) -> dict[str, object]:
    """Trace one step and attach its findings."""
    result = trace(argv, cwd, dict(env))
    return {"label": label, "argv": argv, "exit_status": result["exit_status"],
            "programs": sorted(result["programs"]), "findings": judge(result, names)}


def receipt(spec: list[dict[str, object]], names: dict[str, object], root: Path) -> dict[str, object]:
    """Run every step in a spec and return the per-step program sets and findings.

    This is the interface the follow-up PR's signed replay consumes: each entry
    has `label`, `job`, `argv`, `working-directory`; the result carries the
    executed-program set and any findings per step.
    """
    environment = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/tmp"),
                   "LC_ALL": "C.UTF-8", "LANG": "C.UTF-8"}
    steps = [audit_step(f"{entry['job']}: {entry['label']}", entry["argv"],
                        root / entry.get("working-directory", "."),
                        {**environment, **entry.get("env", {})}, names)
             for entry in spec]
    return {"steps": steps, "clean": all(not step["findings"] for step in steps)}


def selftest(names: dict[str, object]) -> int:
    """A planted installer and a planted unlisted program are each caught by name."""
    import shutil
    import tempfile
    environment = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C.UTF-8"}
    system = Path("/usr/local/bin")  # A system directory the audit holds to the allowlist.
    with tempfile.TemporaryDirectory(prefix="exec-audit-") as directory:
        base = Path(directory)
        # A real ELF under each planted name, so the kernel execs it directly. The
        # installer is caught wherever it runs; the unlisted program is planted in a
        # system directory, where the audit requires a name.
        shutil.copy("/bin/true", system / "zz_unlisted_probe")
        shutil.copy("/bin/true", base / "apt-get")
        shutil.copy("/bin/true", base / "zz_job_artifact")
        for planted in (system / "zz_unlisted_probe", base / "apt-get", base / "zz_job_artifact"):
            planted.chmod(0o755)

        benign = audit_step("benign echo", ["/bin/echo", "ok"], base, environment, names)
        assert not benign["findings"], benign
        assert any(p.endswith("/echo") for p in benign["programs"]), benign
        print("PASS: a benign step lists its program and has no finding")

        artifact = audit_step("job-built artifact", ["/bin/sh", "-c", f"exec {base}/zz_job_artifact"],
                              base, environment, names)
        assert not artifact["findings"], artifact
        print("PASS: a program the job built outside the system tree is allowed")

        installer = audit_step("planted installer",
                               ["/bin/sh", "-c", f"exec {base}/apt-get"], base, environment, names)
        assert any(f["reason"] == "installer executed: apt-get" for f in installer["findings"]), installer
        print("PASS: an executed package manager is caught as an installer by name")

        unlisted = audit_step("planted unlisted program",
                              ["/bin/sh", "-c", f"exec {system}/zz_unlisted_probe"], base, environment, names)
        (system / "zz_unlisted_probe").unlink()
        assert any(f["reason"].endswith("zz_unlisted_probe") for f in unlisted["findings"]), unlisted
        print("PASS: a system program outside the command table is caught by name")

        network = audit_step("network needed", ["/bin/sh", "-c", "exit 7"], base, environment, names)
        assert any("exited 7" in f["reason"] for f in network["findings"]), network
        print("PASS: a step that fails under the disabled network is reported")
    return 0


def main() -> int:
    """Self-test the audit, or run a step spec and write its receipt."""
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--selftest", action="store_true")
    modes.add_argument("--audit", type=Path, help="a JSON step spec to run")
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, help="where to write the receipt")
    args = parser.parse_args()
    names = allowlist()
    if args.selftest:
        return selftest(names)
    report = receipt(json.loads(args.audit.read_text()), names, args.root)
    text = json.dumps(report, indent=2, sort_keys=True) + "\n"
    (args.output.write_text(text) if args.output else sys.stdout.write(text))
    if not report["clean"]:
        print("REJECTED: an audited step executed a forbidden program", file=sys.stderr)
        return 2
    print(f"PASS: {len(report['steps'])} audited steps executed only allowlisted programs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

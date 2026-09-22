#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Disposable handshake fixtures for the two production verification drivers."""

import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path

PROC = Path("/proc")
ROOT = Path(__file__).resolve().parent.parent

# A command publishes readiness only after its detached, stubborn child has
# installed both handlers. The release file, never a delay, controls progress.
WORKER = r'''
import hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path
control = Path(os.environ["PROBE_CONTROL"])
if sys.argv[1:] == ["child"]:
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    (control / "child-ready").write_text(str(os.getpid()))
    while True:
        time.sleep(0.02)
child = subprocess.Popen([sys.executable, __file__, "child"], start_new_session=True)
deadline = time.monotonic() + 10
while not (control / "child-ready").exists():
    assert time.monotonic() < deadline, "child handshake missing"
    time.sleep(0.01)
data = {"pid": os.getpid(), "child": child.pid, "cwd": str(Path.cwd())}
if (control / "mutation.json").exists():
    catalog = json.loads((control / "mutation.json").read_text())
    root = Path.cwd().parents[2]
    data["mutations"] = [row["name"] for row in catalog
                         if hashlib.sha256((root / row["path"]).read_bytes()).hexdigest() == row["hash"]]
    data["private"] = str(root)
    # Write both required dependencies, including modes. A link back to the
    # caller would corrupt the independently measured input snapshot.
    for name in ("gptp-processor", "third_party/verilog-axis"):
        target = root / name / "probe.txt"
        target.write_text("private dependency write\n")
        target.chmod(0o700)
(control / "ready.tmp").write_text(json.dumps(data))
(control / "ready.tmp").replace(control / "ready.json")
print("PARTIAL: owned command reached handshake", flush=True)
while not (control / "release").exists():
    time.sleep(0.02)
'''


def git(root: Path, *args: str) -> bytes:
    """Run fixture-only Git without caller Git redirection or index refresh."""
    env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
    return subprocess.check_output(["git", "--no-optional-locks", "-C", str(root), *args],
                                   env=env, stderr=subprocess.STDOUT)


def commit(root: Path) -> None:
    """Commit only a disposable fixture tree."""
    git(root, "add", "-A")
    git(root, "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-qm", "Disposable verification fixture")


def install(root: Path, relative: str) -> None:
    """Copy a production file into a disposable fixture without links."""
    target = root / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / relative, target)


def write(path: Path, text: str, executable: bool = False) -> None:
    """Create one fixture input with explicit permissions."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    path.chmod(0o755 if executable else 0o644)


def identity(pid: int) -> tuple[str, str] | None:
    """Observe start time and state independently of the production census."""
    try:
        fields = (PROC / str(pid) / "stat").read_text().rsplit(")", 1)[1].split()
        return fields[19], fields[0]
    except (FileNotFoundError, ProcessLookupError):
        return None


def snapshot(root: Path) -> dict:
    """Record tracked bytes, kinds, full modes and index, recursively at pins."""
    indexed = git(root, "ls-files", "--stage", "-z")
    result = {"index": indexed.hex(), "files": {}}
    for row in indexed.split(b"\0"):
        if not row:
            continue
        metadata, raw_name = row.split(b"\t", 1)
        name = os.fsdecode(raw_name)
        path = root / name
        if metadata.startswith(b"160000"):
            result["files"][name] = snapshot(path)
            continue
        if not path.exists() and not path.is_symlink():
            result["files"][name] = ["absent"]
            continue
        info = path.lstat()
        data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
        result["files"][name] = [info.st_mode, hashlib.sha256(data).hexdigest()]
    return result


class Probe:
    """Run a driver in its own session and retain its original transcripts."""

    def __init__(self, root: Path, label: str) -> None:
        self.root = root
        self.label = label
        self.control = root.parent / (label + "-control")
        self.control.mkdir()
        self.env = {key: value for key, value in os.environ.items()
                    if not key.startswith("GIT_")}
        self.env.update(PROBE_CONTROL=str(self.control), PYTHONDONTWRITEBYTECODE="1",
                        TMPDIR=str(self.control))
        write(self.control / "worker.py", WORKER)
        self.process = None

    def start(self, argv: list[str]) -> None:
        """Launch a production driver; keep output even if its assertion fails."""
        with (self.control / "driver.log").open("wb") as output:
            self.process = subprocess.Popen(argv, cwd=self.root, env=self.env,
                                            start_new_session=True, stdout=output,
                                            stderr=subprocess.STDOUT)

    def ready(self) -> dict:
        """Wait for a published boundary, refusing premature driver exit."""
        deadline = time.monotonic() + 15
        while time.monotonic() < deadline:
            path = self.control / "ready.json"
            if path.exists():
                data = json.loads(path.read_text())
                data["identities"] = {str(pid): identity(pid)
                                      for pid in (data["pid"], data["child"])}
                assert all(data["identities"].values()), data
                return data
            assert self.process.poll() is None, self.log()
            time.sleep(0.01)
        raise AssertionError(f"{self.label}: missing boundary: {self.log()}")

    def signal(self, signum: int) -> None:
        """Signal the unreaped driver through a stable identity handle."""
        fd = os.pidfd_open(self.process.pid)
        try:
            signal.pidfd_send_signal(fd, signum)
        finally:
            os.close(fd)

    def finish(self) -> tuple[int, str]:
        """Read the exact exit and transcript after bounded driver completion."""
        status = self.process.wait(timeout=12)
        self._retain(dict(raw_exit=status))
        return status, self.log()

    def log(self) -> str:
        """Return the unfiltered driver transcript."""
        return (self.control / "driver.log").read_text()

    def save(self, evidence: dict) -> None:
        """Print attributable identities; optionally retain every raw fixture log."""
        print(self.label + ": " + json.dumps(evidence, sort_keys=True), flush=True)
        self._retain(evidence)

    def _retain(self, evidence):
        destination = self.env.get("VERIFICATION_TEST_LOGS")
        if destination:
            target = Path(destination) / self.label
            target.mkdir(parents=True, exist_ok=True)
            shutil.copy2(self.control / "driver.log", target / "driver.log")
            (target / "evidence.json").write_text(json.dumps(evidence, indent=2) + "\n")
            logs = self.root / "logs"
            if logs.exists():
                shutil.copytree(logs, target / "suite-logs", dirs_exist_ok=True)


def assert_reaped(data: dict) -> None:
    """Require gone identities, rejecting both live and unreaped zombie state."""
    for pid, previous in data["identities"].items():
        current = identity(int(pid))
        assert current is None or current[0] != previous[0], (pid, previous, current)

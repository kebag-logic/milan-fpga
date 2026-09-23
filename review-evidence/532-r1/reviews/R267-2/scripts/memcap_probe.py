#!/usr/bin/env python3
"""Reviewer probe (round R267-2, PR #533): what a slice's own memory.events.local
records when a no-swap MemoryMax cap bites, with and without an OOM.

It mirrors the runner's attribution check (read `oom` from the cgroup's own
memory.events.local after the work) on a disposable transient user scope with
MemoryMax=128M and MemorySwapMax=0 (the slot slice uses MemoryMax=24G and
MemorySwapMax=0). Two workloads run in their own scopes:

  thrash   holds 100 MiB of anonymous memory and re-reads 192 MiB of files it
           wrote, so the remaining page cache is reclaimed and refaulted on
           every pass. It is timed against the same workload in an uncapped
           scope (MemoryMax=infinity).
  oom      a child allocates 256 MiB of anonymous memory and is OOM-killed;
           the positive control that `oom` counts in this setup.

No privilege is used: the scopes belong to the invoking user's own service
manager. Scratch files are removed at the end.

usage: memcap_probe.py SCRATCH_DIR            (orchestrates both scopes)
       memcap_probe.py --work thrash|oom DIR  (runs inside a scope)
"""
import os
import pathlib
import subprocess
import sys
import time

MIB = 1 << 20
FILES = 12
FILE_MIB = 16
HOLD_MIB = 100
PASSES = 6


def own_cgroup() -> pathlib.Path:
    return pathlib.Path("/sys/fs/cgroup") / pathlib.Path(
        open("/proc/self/cgroup").read().strip().split("::", 1)[1].lstrip("/"))


def events(cgroup: pathlib.Path) -> dict[str, int]:
    return {k: int(v) for k, v in
            (line.split() for line in (cgroup / "memory.events.local").read_text().splitlines())}


def pressure_full_us(cgroup: pathlib.Path) -> int:
    for line in (cgroup / "memory.pressure").read_text().splitlines():
        if line.startswith("full"):
            return int(line.rsplit("total=", 1)[1])
    return -1


def work(kind: str, directory: pathlib.Path) -> None:
    cgroup = own_cgroup()
    limit = (cgroup / "memory.max").read_text().strip()
    if kind == "oom":
        child = subprocess.run([sys.executable, "-c",
                                "b = bytearray(256 << 20)\nfor i in range(0, len(b), 4096): b[i] = 1\n"],
                               capture_output=True)
        print(f"oom: memory.max={limit} child exit={child.returncode} "
              f"events.local={events(cgroup)}", flush=True)
        return
    directory.mkdir(parents=True, exist_ok=True)
    block = os.urandom(MIB)
    paths = []
    for index in range(FILES):
        path = directory / f"f{index}"
        with open(path, "wb") as handle:
            for _ in range(FILE_MIB):
                handle.write(block)
            handle.flush()
            os.fsync(handle.fileno())
        paths.append(path)
    hold = bytearray(HOLD_MIB * MIB)
    for offset in range(0, len(hold), 4096):
        hold[offset] = 1
    before = events(cgroup)
    pressure_before = pressure_full_us(cgroup)
    started = time.monotonic()
    for _ in range(PASSES):
        for path in paths:
            with open(path, "rb") as handle:
                while handle.read(MIB):
                    pass
    elapsed = time.monotonic() - started
    after = events(cgroup)
    peak = (cgroup / "memory.peak").read_text().strip() if (cgroup / "memory.peak").exists() else "n/a"
    print(f"thrash: memory.max={limit} passes={PASSES} over {FILES * FILE_MIB} MiB "
          f"with {HOLD_MIB} MiB anon held: {elapsed:.2f} s; "
          f"events.local before={before} after={after}; "
          f"memory.pressure full total +{pressure_full_us(cgroup) - pressure_before} us; "
          f"memory.peak={peak}", flush=True)
    del hold
    for path in paths:
        path.unlink()


def scope(name: str, memory_max: str, kind: str, directory: pathlib.Path) -> str:
    # OOMPolicy=continue keeps the scope (and this probe) alive when the
    # kernel OOM-kills the child, as a service manager would not by default.
    command = ["systemd-run", "--user", "--scope", "--quiet", f"--unit={name}",
               f"--property=MemoryMax={memory_max}", "--property=MemorySwapMax=0",
               "--property=OOMPolicy=continue",
               sys.executable, "-I", str(pathlib.Path(__file__).resolve()),
               "--work", kind, str(directory)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=900)
    return f"$ {' '.join(command)}\nrc={result.returncode}\n{result.stdout}{result.stderr}"


def main() -> int:
    if sys.argv[1] == "--work":
        work(sys.argv[2], pathlib.Path(sys.argv[3]))
        return 0
    scratch = pathlib.Path(sys.argv[1]).resolve()
    stamp = os.getpid()
    print(f"kernel {os.uname().release}")
    print(scope(f"r267-memcap-oom-{stamp}", "128M", "oom", scratch / "oom"))
    print(scope(f"r267-memcap-capped-{stamp}", "128M", "thrash", scratch / "capped"))
    print(scope(f"r267-memcap-uncapped-{stamp}", "infinity", "thrash", scratch / "uncapped"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

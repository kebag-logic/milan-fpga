#!/usr/bin/env python3
"""The five tool entry points ctrl_pin.pin_controls runs on an edited clone
(MAAP differential both modes, AECP arms, campaign, wire comparison), plus the
pin CLI, each on a fresh clone with one stack file edited; also each on a clone
whose own configuration names a recorder as remote.origin.uploadpack beside a
missing pinned src/ tree object. Prints exit status, the last line naming
tsn-c-stack, and whether the recorder ran.
usage: python3 -I entry_points.py <superproject-root> <work-dir>"""
import os, shutil, subprocess, sys
from pathlib import Path

root, work = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
here = root / "sw/firmware/ctrl/test"
stack = root / "third_party/tsn-c-stack"
pin = subprocess.run(["git", "-C", str(root), "ls-files", "--stage", "--", "third_party/tsn-c-stack"],
                     capture_output=True, text=True, check=True).stdout.split()[1]
env0 = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def g(d, *a):
    subprocess.run(["git", "-c", "gc.auto=0", "-c", "maintenance.auto=false", "-C", str(d), *a], check=True,
                   capture_output=True, env=env0)


def clone(state, rel):
    c = work / "clone"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir(parents=True)
    g(work, "clone", "-q", "--no-hardlinks", str(stack), str(c))
    g(c, "-c", "advice.detachedHead=false", "checkout", "-q", pin)
    if state == "edited":
        p = c / rel
        p.write_bytes(p.read_bytes() + b"\n")
    else:
        rec = work / "recorder"
        rec.write_text('#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexit 1\n')
        rec.chmod(0o755)
        loose = work / "loose"
        g(work, "init", "-q", str(loose))
        g(loose, "-c", "fetch.unpackLimit=1000000", "fetch", "-q", "--no-tags", str(c), f"{pin}:refs/heads/p")
        g(loose, "-c", "advice.detachedHead=false", "checkout", "-q", pin)
        src = subprocess.run(["git", "-C", str(loose), "rev-parse", f"{pin}:src"], capture_output=True, text=True,
                             env=env0).stdout.strip()
        (loose / ".git/objects" / src[:2] / src[2:]).unlink()
        for k, v in (("core.repositoryformatversion", "1"), ("extensions.partialClone", "origin"),
                     ("remote.origin.url", str(c)), ("remote.origin.promisor", "true"),
                     ("remote.origin.uploadpack", str(rec))):
            g(loose, "config", k, v)
        c = loose
    return c


entries = [("pin CLI", "src/adp.c", lambda c: [sys.executable, "-I", str(here / "ctrl_build.py"), "--stack-pin", str(c)]),
           ("MAAP differential", "src/maap.c", lambda c: [sys.executable, "-B", str(here / "maap_differential.py"), "--stack", str(c)]),
           ("MAAP differential --self-test", "src/maap.c", lambda c: [sys.executable, "-B", str(here / "maap_differential.py"), "--stack", str(c), "--self-test"]),
           ("AECP arms", "src/acmp.c", lambda c: [sys.executable, "-B", str(here / "aecp_arms.py"), "--stack", str(c), "--output", str(work / "out"), "--app"]),
           ("AECP campaign", "src/acmp.c", lambda c: [sys.executable, "-B", str(here / "aecp_mutants.py"), "--stack", str(c), "--output", str(work / "out"), "--shard", "0", "1000"]),
           ("AECP wire comparison", "include/wire.h", lambda c: [sys.executable, "-B", str(here / "aecp_wire.py"), "--stack", str(c), "--output", str(work / "out"), "--reference", str(root / "protocol-processor"), "--verilator", "false"])]
bad = 0
for state in ("edited", "lazy-uploadpack"):
    for name, rel, argv in entries:
        c = clone(state, rel)
        r = subprocess.run(argv(c), capture_output=True, text=True, env={**env0, "VERILATOR": "false"}, timeout=900)
        said = [ln for ln in (r.stdout + r.stderr).splitlines() if "tsn-c-stack" in ln]
        ran = (work / "ran").exists()
        want = rel if state == "edited" else "outside the pin proof's allowlist"
        ok = r.returncode != 0 and said and want in said[-1] and not ran
        bad += not ok
        print(f"[{'ok' if ok else 'UNEXPECTED'}] {state} | {name} | exit {r.returncode} | RAN={int(ran)} | "
              f"{said[-1].strip()[:200] if said else 'no pin verdict'}", flush=True)
print(f"ENTRY POINTS: {bad} unexpected")

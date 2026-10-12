"""Probe: allowlisted stack keys whose VALUE names a program (an ext:: URL), judged by the pin check (#697).

Usage: python3 -I allowlisted_value_probe.py <checkout> <scratch-dir>
The Git is the first `git` on PATH. For each case, a fresh clone of the checkout's third_party/tsn-c-stack at its
gitlink gets keys of the allowlist's families whose values name a recorder through Git's ext:: transport, then
ctrl_build.stack_pin(clone, pin) runs. Prints the verdict and RAN (recorder starts during the check).
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

repo, scratch = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sys.path.insert(0, str(repo / "sw/firmware/ctrl/test"))
import ctrl_build  # noqa: E402

ENV = {"PATH": os.environ["PATH"], "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull, "HOME": str(scratch)}


def g(cwd, *a):
    r = subprocess.run(["git", *a], cwd=cwd, env=ENV, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"setup: git {a}: {r.stderr}")
    return r.stdout


pin = ctrl_build.stack_gitlink(repo)
CASES = [("V1 remote.origin.url = ext::<recorder>, pinned clone", False),
         ("V2 remote.origin.url = ext::<recorder>, pinned src/ tree object missing", True)]
for name, missing in CASES:
    own = scratch / name.split()[0]
    shutil.rmtree(own, ignore_errors=True)
    own.mkdir(parents=True)
    rec = own / "recorder"
    rec.write_text('#!/bin/sh\necho "$0 $*" >> "$(dirname "$0")/ran"\nexit 1\n')
    rec.chmod(0o755)
    clone = own / "stack"
    g(own, "clone", "-q", "--no-local", "--no-checkout", str(repo / "third_party/tsn-c-stack"), str(clone))
    g(clone, "-c", "advice.detachedHead=false", "checkout", "-q", pin)
    if missing:
        g(clone, "repack", "-a", "-d", "-q")
        # explode every object loose, then remove the src/ tree's
        packs = list((clone / ".git/objects/pack").glob("*.pack"))
        for p in packs:
            moved = own / p.name
            p.rename(moved)
            p.with_suffix(".idx").unlink()
            subprocess.run(["git", "unpack-objects", "-q"], cwd=clone, env=ENV, stdin=moved.open("rb"), check=True)
        src = g(clone, "rev-parse", f"{pin}:src").strip()
        (clone / ".git/objects" / src[:2] / src[2:]).unlink()
    g(clone, "config", "remote.origin.url", f"ext::{rec} %S")
    listed = g(clone, "config", "--list", "--local")
    try:
        verdict = f"ACCEPTED {ctrl_build.stack_pin(clone, pin)}"
    except ctrl_build.Refusal as exc:
        verdict = f"REFUSED {exc}"
    ran = (own / "ran").read_text().count("\n") if (own / "ran").exists() else 0
    print(f"{name}\n  local keys: {', '.join(l.split('=')[0] for l in listed.splitlines())}\n  {verdict[:230]} RAN={ran}",
          flush=True)

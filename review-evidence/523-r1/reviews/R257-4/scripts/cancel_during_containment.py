#!/usr/bin/env python3
"""Cancel a candidate's owned preflight while the containment self-test runs.

Usage: cancel_during_containment.py <repo> <scratch-dir> <INT|TERM> <trigger-regex>

The body is the candidate sweep's own `preflight` function (extracted verbatim)
running `check_merge_containment.py --selftest` as the sweep does, followed by a
next-step sentinel that must never execute after cancellation. The body runs
under the candidate's `owned_process.py`. The handshake is observable progress:
the signal is sent only after the self-test's log holds a line matching the
trigger. Every descendant identity (pid, start time) observed at that moment
must be gone afterwards, the sentinel must be absent, and the exit must be
128+N with the shell's own CANCELLED line. Prints one JSON verdict line.
"""
import json
import os
import re
import signal
import subprocess
import sys
import time
from pathlib import Path


def identity(pid):
    try:
        text = Path(f"/proc/{pid}/stat").read_text()
    except (FileNotFoundError, ProcessLookupError):
        return None
    fields = text.rsplit(")", 1)[1].split()
    return int(fields[1]), fields[19], fields[0]


def descendants(root):
    table = {}
    for entry in Path("/proc").iterdir():
        if entry.name.isdecimal():
            ident = identity(int(entry.name))
            if ident:
                table[int(entry.name)] = ident
    owned, frontier = set(), {root}
    while frontier:
        nxt = {p for p, (pp, _s, _st) in table.items() if pp in frontier} - owned
        owned |= nxt
        frontier = nxt
    return {p: table[p] for p in owned}


def cmdline(pid):
    try:
        return Path(f"/proc/{pid}/cmdline").read_bytes().replace(b"\0", b" ").decode(errors="replace").strip()
    except OSError:
        return "<gone>"


def main():
    repo, scratch, signame, trigger = sys.argv[1:5]
    signum = {"INT": signal.SIGINT, "TERM": signal.SIGTERM}[signame]
    scratch = Path(scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    out = scratch / "out"
    sentinel = scratch / "NEXT_STEP_RAN"
    sweep = Path(repo, "scripts/run_all_suites.sh").read_text()
    funcs = "\n".join(m.group(0) for m in re.finditer(
        r"^(?:preflight|prepare_logs)\(\) \{\n.*?^\}$", sweep, re.S | re.M))
    body = scratch / "body.sh"
    body.write_text(f"""set -u
ROOT={repo!r}
OUT={str(out)!r}
LOGS_READY=0
cancelled() {{
  echo "CANCELLED: $1; no completed sweep result" >&2
  if [ "$LOGS_READY" = 1 ]; then echo "partial logs: $OUT" >&2; fi
  exit "$2"
}}
trap 'cancelled INT 130' INT
trap 'cancelled TERM 143' TERM
{funcs}
prepare_logs
selftest_out=$(cd "$ROOT" && preflight check_merge_containment python3 "$ROOT/scripts/check_merge_containment.py" --selftest 2>&1)
selftest_rc=$?
echo "containment rc=$selftest_rc"
touch {str(sentinel)!r}
""")
    log = out / "preflight" / "check_merge_containment.log"
    proc = subprocess.Popen([sys.executable, str(Path(repo, "scripts/owned_process.py")), "--",
                             "bash", str(body)], start_new_session=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # "proc:<substring>": wait until a live descendant of the owner has that
    # substring in its command line (observable process state, no sleep
    # oracle). Otherwise the trigger is a regex over the self-test's log.
    pattern = None if trigger.startswith("proc:") else re.compile(trigger, re.M)
    deadline = time.monotonic() + 120
    matched = None
    while time.monotonic() < deadline and proc.poll() is None:
        if pattern is None:
            hits = [f"{p}: {c}" for p, ident in descendants(proc.pid).items()
                    if ident[2] != "Z" and trigger[5:] in (c := cmdline(p))]
            m = hits[0] if hits else None
        else:
            try:
                found = pattern.search(log.read_text(errors="replace"))
            except FileNotFoundError:
                found = None
            m = found.group(0) if found else None
        if m:
            matched = m[:200]
            break
        time.sleep(0.005)
    census = descendants(proc.pid)
    census_desc = {str(p): [ident[1], ident[2], cmdline(p)[:160]] for p, ident in census.items()}
    if matched is None:
        proc.kill()
        proc.wait()
        print(json.dumps({"signal": signame, "error": "trigger never observed", "exit": proc.returncode}))
        return 1
    os.kill(proc.pid, signum)
    try:
        stdout, stderr = proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()
        stdout, stderr = proc.communicate()
        print(json.dumps({"signal": signame, "error": "owner did not exit within 60 s"}))
        return 1
    time.sleep(0.2)
    survivors = {str(p): [ident[1], cmdline(p)[:160]] for p, ident in census.items()
                 if (now := identity(p)) is not None and now[1] == ident[1] and now[2] != "Z"}
    err = stderr.decode(errors="replace")
    verdict = {
        "signal": signame,
        "trigger": trigger,
        "matched": matched,
        "exit": proc.returncode,
        "expected_exit": 128 + int(signum),
        "shell_cancel_line": f"CANCELLED: {signame}; no completed sweep result" in err,
        "partial_logs_line": f"partial logs: {out}" in err,
        "owner_cancel_line": f"CANCELLED: signal {int(signum)}; no completed sweep result" in err,
        "next_step_ran": sentinel.exists(),
        "census_size": len(census),
        "census": census_desc,
        "survivors": survivors,
        "stdout": stdout.decode(errors="replace")[-400:],
        "stderr": err[-600:],
    }
    ok = (verdict["exit"] == verdict["expected_exit"] and verdict["shell_cancel_line"]
          and verdict["partial_logs_line"] and not verdict["next_step_ran"]
          and not survivors and len(census) >= 2)
    verdict["result"] = "PASS" if ok else "FAIL"
    print(json.dumps(verdict, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run every processor entry point and the parent gates on one committed head.

The processor head is fetched into a scratch clone and checked out there; the
scratch parent copy's protocol-processor gitlink is staged at the same head.
Nothing runs in the working tree. Each command runs in the foreground and its
exit, duration, log size and SHA-256 are appended to <scratch>/results.jsonl.
"""
import argparse
import hashlib
import json
import subprocess
import time
from pathlib import Path

PROCESSOR = [
    ["./scripts/run_suites.sh"],
    ["./scripts/lint_hdl.sh"],
    ["make", "check"],
    ["python3", "scripts/gen_matrix.py", "--check"],
    ["./syn/yosys/run.sh"],
    ["make", "-C", "tb/srp_top", "mutants"],
    ["make", "-C", "tb/nvm_port", "figures"],
]
PARENT = [
    ["python3", "scripts/xvlog_gate.py", "--check"],
    ["python3", "scripts/measure_test_evidence.py", "--check"],
    ["python3", "scripts/check_cpp_idiom.py"],
    ["python3", "scripts/check_py_idiom.py"],
]


def git(cwd: Path, *args: str) -> str:
    """Run one git command and return its standard output."""
    out = subprocess.run(["git", *args], cwd=cwd, check=True,
                         capture_output=True, text=True)
    return out.stdout.strip()


def checkout(repo: Path, source: Path, branch: str) -> str:
    """Fetch the branch head from the working tree and check it out cleanly."""
    git(repo, "fetch", "-q", str(source), branch)
    git(repo, "checkout", "-q", "-f", "FETCH_HEAD")
    git(repo, "clean", "-q", "-fdx")
    return git(repo, "rev-parse", "HEAD")


def run(label: str, cwd: Path, cmd: list[str], logs: Path, record: Path) -> int:
    """Run one command in the foreground, log it and record its exit."""
    name = f"{label}-" + "_".join(c.replace("/", "_") for c in cmd)[:80]
    log = logs / f"{name}.log"
    start = time.monotonic()
    with log.open("wb") as stream:
        rc = subprocess.run(cmd, cwd=cwd, stdout=stream,
                            stderr=subprocess.STDOUT, check=False).returncode
    data = log.read_bytes()
    row = {"group": label, "command": cmd, "rc": rc,
           "seconds": round(time.monotonic() - start, 1), "log": str(log),
           "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
    with record.open("a") as out:
        out.write(json.dumps(row) + "\n")
    print(f"{label} rc={rc} {row['seconds']}s {' '.join(cmd)}", flush=True)
    return rc


def main() -> int:
    """Check out the head in both scratch copies and run the selected gates."""
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tree", type=Path, required=True)
    ap.add_argument("--branch", required=True)
    ap.add_argument("--processor-scratch", type=Path, required=True)
    ap.add_argument("--parent-scratch", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--skip", nargs="*", default=[],
                    help="substrings of commands not to run this time")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    record = args.out / "results.jsonl"
    head = checkout(args.processor_scratch, args.tree, args.branch)
    sub = args.parent_scratch / "protocol-processor"
    assert checkout(sub, args.tree, args.branch) == head
    git(args.parent_scratch, "add", "protocol-processor")
    print(f"head {head}", flush=True)
    failed = 0
    for label, cwd, cmds in (("processor", args.processor_scratch, PROCESSOR),
                             ("parent", args.parent_scratch, PARENT)):
        for cmd in cmds:
            if any(s in " ".join(cmd) for s in args.skip):
                continue
            failed += run(label, cwd, cmd, args.out, record) != 0
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

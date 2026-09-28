#!/usr/bin/env python3
"""Run parent gates in a scratch export, with processor paths pointing at DONOR.

Usage: run_parent_gates.py DONOR PARENT GPTP_BARE SCRATCH
GPTP_BARE must contain the parent-pinned gPTP revision. Only SCRATCH is written.
The evidence gate is run both unchanged and with the proposed disposition row;
no ratchet, population check or verdict rule is changed.
"""
import io
import subprocess
import sys
import tarfile
from pathlib import Path

DISPOSITION = '"protocol-processor/tb/acmp_talker/retry_mutants.py":\n        "mutation campaign; plants named defects in a scratch copy and requires named assertion "\n        "failures from completed cycle-bounded simulations; reads no expected behavior from RTL",'


def git(path: Path, *args: str) -> str:
    """Read Git metadata without refreshing the source index."""
    return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()


def metadata(dest: Path, objects: Path, head: str) -> None:
    """Give a scratch export a private index for the gates population proof."""
    subprocess.run(["git", "init", "-q", str(dest)], check=True)
    (dest / ".git/objects/info/alternates").write_text(str(objects) + "\n")
    (dest / ".git/HEAD").write_text(head + "\n")
    subprocess.run(["git", "-C", str(dest), "read-tree", "HEAD"], check=True)


def export(source: Path, revision: str, dest: Path) -> None:
    """Extract committed inputs; no branch checkout is performed."""
    dest.mkdir(parents=True, exist_ok=True)
    data = subprocess.check_output(["git", "-C", str(source), "archive", revision])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(dest, filter="data")


def run(scratch: Path, script: str, receipt: str) -> int:
    """Record an unpiped foreground command and its exact return code."""
    result = subprocess.run([sys.executable, "scripts/" + script, "--check"],
                            cwd=scratch, capture_output=True, text=True, check=False)
    text = result.stdout + result.stderr + f"\nreturn code: {result.returncode}\n"
    (scratch / receipt).write_text(text)
    print(f"{script}: rc {result.returncode}; {receipt}", flush=True)
    return result.returncode


def main() -> int:
    """Stage the authorized gate inputs and grade both adoption variants."""
    donor, parent, gptp, scratch = [Path(arg).resolve() for arg in sys.argv[1:]]
    if scratch.exists():
        raise SystemExit("SCRATCH must be a new directory")
    head = git(donor, "rev-parse", "HEAD")
    parent_head = git(parent, "rev-parse", "HEAD")
    export(parent, parent_head, scratch)
    objects = Path(git(parent, "rev-parse", "--path-format=absolute", "--git-path", "objects"))
    metadata(scratch, objects, parent_head)
    pp = scratch / "protocol-processor"
    for source in donor.iterdir():
        if source.name != ".git":
            (pp / source.name).symlink_to(source, target_is_directory=source.is_dir())
    objects = Path(git(donor, "rev-parse", "--path-format=absolute", "--git-path", "objects"))
    metadata(pp, objects, head)
    gp_head = git(parent, "rev-parse", "HEAD:gptp-processor")
    gp = scratch / "gptp-processor"
    export(gptp, gp_head, gp)
    metadata(gp, gptp / "objects", gp_head)
    for name in ("protocol-processor", "gptp-processor"):
        url = git(parent, "config", "-f", ".gitmodules", "--get", f"submodule.{name}.url")
        subprocess.run(["git", "-C", str(scratch), "config", f"submodule.{name}.url", url], check=True)
    subprocess.run(["git", "-C", str(scratch), "update-index", "--cacheinfo",
                    "160000," + head + ",protocol-processor"], check=True)
    print(f"parent source {parent_head}; processor {head}; gPTP {gp_head}", flush=True)
    xvlog = run(scratch, "xvlog_gate.py", "xvlog.txt")
    raw = run(scratch, "measure_test_evidence.py", "evidence-original.txt")
    script = scratch / "scripts/measure_test_evidence.py"
    original = script.read_text()
    script.write_text(original.replace("DUT_READER_DISPOSITIONS = {",
                                      "DUT_READER_DISPOSITIONS = {\n    " + DISPOSITION, 1))
    adopted = run(scratch, "measure_test_evidence.py", "evidence-disposition.txt")
    print("Unchanged evidence gate rc " + str(raw) + "; proposed disposition only: rc " + str(adopted))
    return xvlog or adopted


if __name__ == "__main__":
    raise SystemExit(main())

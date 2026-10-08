"""Record final revision, dependency, process and memory evidence."""
import json
import os
import subprocess
from pathlib import Path

w = Path(__file__).resolve().parent
root = Path("$REPO")
expected = "85db353400c6bf3965d279a9f5b5d47e08a0d1ed"

def git(*args, cwd=root):
    return subprocess.check_output(["rtk", "proxy", "git", *args], cwd=cwd, text=True).strip()

head = git("rev-parse", "HEAD")
remote = git("remote", "get-url", "origin")
branch = git("branch", "--show-current")
assert head == expected
assert remote == "https://github.com/kebag-logic/milan-fpga.git"
assert branch == "645-ring-slip"
pins = {
    "protocol-processor": "2ad2f845dd583f8310075fa2380cb60a04fd091a",
    "gptp-processor": "5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d",
    "third_party/verilog-axis": "48ff7a7e2ef782cf778d47910cf85835c64b1bce",
}
dependencies = []
for name, wanted in pins.items():
    directory = root / name
    assert git("rev-parse", "--show-toplevel", cwd=directory) == str(directory)
    actual = git("rev-parse", "HEAD", cwd=directory)
    assert actual == wanted, (name, actual)
    assert git("rev-parse", "--show-toplevel", cwd=directory) == str(directory)
    status = git("status", "--porcelain=v1", cwd=directory)
    assert not status, (name, status)
    dependencies.append(dict(path=name, head=actual, root_verified=True, clean=True))
status = git("status", "--porcelain=v1")
assert not status, status
git("diff", "--check", "99e4eb6c14462aafa84bb1ac597fd241abc1a240", "HEAD")
commits = git("rev-list", "--first-parent", "2525eae9567865a8bc741901914bdf5a1caf2c26..HEAD").splitlines()
assert commits == [expected, "9a0d68e2016c0385171107277721aa187ce19674"], commits
messages = []
for sha in commits:
    message = git("show", "-s", "--format=%B", sha)
    assert len(message.splitlines()) == 1, (sha, message)
    messages.append(dict(commit=sha, subject=message))

runners = {
    "vendor_bank.py", "vendor_job.py", "run_job.py", "functional_bank.py",
    "finish_functional_bank.py", "firmware_campaigns.py", "firmware_shards.py",
    "parallel_sweeps.py", "restart_sweeps.py", "extra_bank.py", "litex_bank.py",
}
active = []
for proc in Path("/proc").iterdir():
    if not proc.name.isdigit() or int(proc.name) == os.getpid():
        continue
    try:
        state = (proc / "stat").read_text().rsplit(")", 1)[1].split()[0]
        if state == "Z":
            continue
        args = (proc / "cmdline").read_bytes().decode(errors="replace").split("\0")
        worker = any(arg == str(w / name) for name in runners for arg in args)
        cwd = str((proc / "cwd").resolve())
        vendor = cwd.startswith(str(w) + "/") and any(Path(arg).name == "vivado" for arg in args)
        scratch_process = cwd == str(w) or cwd.startswith(str(w) + "/")
        if worker or vendor or scratch_process:
            active.append(dict(pid=int(proc.name), kind="worker" if worker else "vendor" if vendor else "scratch process"))
    except (OSError, ProcessLookupError):
        continue
assert not active, active
cg = Path("/sys/fs/cgroup") / Path("/proc/self/cgroup").read_text().strip().split("::", 1)[1].lstrip("/")
memory = {key: (cg / key).read_text().strip() for key in ("memory.current", "memory.peak", "memory.high", "memory.max", "memory.events")}
assert int(memory["memory.peak"]) < 17_000_000_000, memory
report = dict(head=head, branch=branch, remote=remote, clean=True, dependencies=dependencies,
              first_parent_commits=messages, diff_check_rc=0, active_jobs=active, memory=memory)
(w / "final-audit.json").write_text(json.dumps(report, indent=2) + "\n")
print("Final audit PASS:", head, "clean; dependencies verified; no active jobs; peak bytes", memory["memory.peak"])

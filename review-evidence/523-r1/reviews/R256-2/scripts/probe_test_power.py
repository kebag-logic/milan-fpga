#!/usr/bin/env python3
"""Reviewer probe: plant one production defect at a time in a disposable copy
and run the owning focused test; a useful test must go red.

Usage: probe_test_power.py COPY OUT_JSON [NAME ...]
Each mutant is an exact single-occurrence replacement; the copy is restored
with `git checkout -- .` after every mutant and verified clean at the end.
"""
import json, os, subprocess, sys, time
from pathlib import Path

copy = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2])
only = set(sys.argv[3:])
LIFE = ["python3", "tb/verilator/gptp_shadow/test_mutant_lifecycle.py"]
SWEEP = ["python3", "scripts/test_suite_cancellation.py"]
BARE = ["python3", "scripts/check_baremetal_only.py", "--selftest"]
MUTANTS = [
    ("no-subreaper", "scripts/owned_process.py",
     "if self.libc.prctl(36, 1, 0, 0, 0):", "if self.libc.prctl(36, 0, 0, 0, 0):", [LIFE, SWEEP]),
    ("hardlink-copy", "tb/verilator/gptp_shadow/private_inputs.py",
     "        destination.write_bytes(content)\n        destination.chmod(stat.S_IMODE(info.st_mode) | stat.S_IWUSR)\n",
     "        os.link(source, destination)\n", [LIFE]),
    ("no-byte-hash", "tb/verilator/gptp_shadow/private_inputs.py",
     "if actual != blob or executable", "if executable", [LIFE]),
    ("no-mode-check", "tb/verilator/gptp_shadow/private_inputs.py",
     "if actual != blob or executable != (mode == \"100755\"):", "if actual != blob:", [LIFE]),
    ("no-untracked-check", "tb/verilator/gptp_shadow/private_inputs.py",
     "    if unknown:\n", "    if False:\n", [LIFE]),
    ("no-link-directory-check", "tb/verilator/gptp_shadow/private_inputs.py",
     "            raise InputRefused(f\"input directory is missing or linked: {current}\")", "            pass", [LIFE]),
    ("no-git-env-check", "tb/verilator/gptp_shadow/private_inputs.py",
     "    if overrides:\n", "    if False:\n", [LIFE]),
    ("no-private-restore", "tb/verilator/gptp_shadow/mutants.py",
     "        path.write_bytes(pristine)\n", "", [LIFE]),
    ("no-kill-escalation", "scripts/owned_process.py",
     "signum = signal.SIGKILL if now >= deadline else signal.SIGTERM", "signum = signal.SIGTERM", [LIFE, SWEEP]),
    ("no-identity-recheck", "scripts/owned_process.py",
     "if _identity(pid) == identity:", "if True:", [LIFE, SWEEP]),
    ("no-root-stop", "scripts/owned_process.py",
     "                self._signal(self.root_fd, signal.SIGSTOP)\n                self._signal(self.root_fd, signum)\n",
     "                self._signal(self.root_fd, signum)\n", [SWEEP]),
    ("no-shell-cancel-traps", "scripts/run_all_suites.sh",
     "trap 'cancelled INT 130' INT\ntrap 'cancelled TERM 143' TERM\n", "", [SWEEP]),
    ("no-sweep-owner", "scripts/run_all_suites.sh",
     "  exec python3 \"$ROOT/scripts/owned_process.py\" -- bash \"$0\" --owned-sweep \"$@\"\n",
     "  set -- --owned-sweep \"$@\"\n", [SWEEP]),
    ("mask-any-proc", "scripts/check_baremetal_only.py",
     "\"scripts/owned_process.py\": re.compile(r'(?<=^PROC = Path\\(\")/proc(?=\"\\)$)'),",
     "\"scripts/owned_process.py\": re.compile(r'/proc'),", [BARE]),
    ("mask-unanchored-start", "scripts/check_baremetal_only.py",
     "\"scripts/process_test_support.py\": re.compile(r'(?<=^PROC = Path\\(\")/proc(?=\"\\)$)'),",
     "\"scripts/process_test_support.py\": re.compile(r'(?<=PROC = Path\\(\")/proc(?=\"\\)$)'),", [BARE]),
]

def git(*args):
    return subprocess.run(["git", "-C", str(copy), *args], check=True, capture_output=True, text=True).stdout

env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
env["PYTHONDONTWRITEBYTECODE"] = "1"
results = []
for name, rel, old, new, tests in MUTANTS:
    if only and name not in only:
        continue
    path = copy / rel
    text = path.read_text()
    assert text.count(old) == 1, (name, text.count(old))
    path.write_text(text.replace(old, new, 1))
    row = dict(mutant=name, file=rel, runs=[])
    for argv in tests:
        start = time.monotonic()
        try:
            done = subprocess.run(argv, cwd=copy, env=env, capture_output=True, text=True, timeout=600)
            code, tail = done.returncode, (done.stdout + done.stderr).strip().splitlines()[-3:]
        except subprocess.TimeoutExpired as exc:
            code, tail = "timeout", [str(exc)[:200]]
        row["runs"].append(dict(test=" ".join(argv[1:]), exit=code, red=code != 0,
                                seconds=round(time.monotonic() - start, 1),
                                tail=[t[:300].replace(str(copy), "<copy>") for t in tail]))
    git("checkout", "-q", "--", ".")
    results.append(row)
    print(json.dumps(dict(mutant=name, reds=[r["red"] for r in row["runs"]], exits=[r["exit"] for r in row["runs"]])), flush=True)
assert git("status", "--porcelain") == "", "copy not restored"
out.write_text(json.dumps(results, indent=2) + "\n")

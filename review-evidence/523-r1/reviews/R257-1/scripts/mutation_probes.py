#!/usr/bin/env python3
"""Plant one defect per disposable copy of the reviewed tree and run the focused
test that should notice it. A copy is `git archive <head>` output (tracked files
only); nothing is written to the checkout. Exit status of the named test is the
verdict: non-zero = the planted defect was detected.
Usage: mutation_probes.py <checkout> <head> <workdir> <receipt-json> [ID ...]"""
import json, os, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

LIFE = ["python3", "tb/verilator/gptp_shadow/test_mutant_lifecycle.py"]
SWEEP = ["python3", "scripts/test_suite_cancellation.py"]
BARE = ["python3", "scripts/check_baremetal_only.py", "--selftest"]
PI, OP, RS, BM = ("tb/verilator/gptp_shadow/private_inputs.py", "scripts/owned_process.py",
                  "scripts/run_all_suites.sh", "scripts/check_baremetal_only.py")
PROBES = {
 "M01-hardlink-copy": (PI, "destination.write_bytes(content)", "os.link(source, destination)", LIFE),
 "M02-no-byte-mode-check": (PI, 'if actual != blob or executable != (mode == "100755"):', "if False:", LIFE),
 "M03-no-unknown-refusal": (PI, "    if unknown:\n", "    if False:\n", LIFE),
 "M04-no-linked-dir-refusal": (PI, "        _directory(root, str(Path(name).parent))\n", "        pass\n", LIFE),
 "M05-no-git-env-refusal": (PI, "    if overrides:\n", "    if False:\n", LIFE),
 "M06-no-pin-check": (PI, '_git(root, owner, "rev-parse", "HEAD").strip() != revision', "False", LIFE),
 "M07-no-index-vs-head": (PI, "if not expected or expected != indexed:", "if not expected:", LIFE),
 "M08-no-subreaper-sweep": (OP, "self.libc.prctl(36, 1, 0, 0, 0)", "self.libc.prctl(36, 0, 0, 0, 0)", SWEEP),
 "M09-no-kill-escalation-sweep": (OP, "signum = signal.SIGKILL if now >= deadline else signal.SIGTERM", "signum = signal.SIGTERM", SWEEP),
 "M10-no-identity-recheck-sweep": (OP, "if _identity(pid) == identity:", "if True:", SWEEP),
 "M11-no-cancel-traps": (RS, "trap 'cancelled INT 130' INT\ntrap 'cancelled TERM 143' TERM\n", "", SWEEP),
 "M12-original-cleanup-trap": (RS, "  trap cleanup EXIT\n", "  trap cleanup EXIT INT TERM\n", SWEEP),
 "M13-no-stale-log-clear": (RS, '  rm -f "$OUT"/*.log "$OUT/preflight"/*.log || exit 2\n', "", SWEEP),
 "M14-build-failure-counts": ("tb/verilator/gptp_shadow/mutants.py", "        return int(tally.group(1)) != 0\n    return False\n", "        return int(tally.group(1)) != 0\n    return status != 0\n", LIFE),
 "M15-ignore-zombies-sweep": (OP, "            owned = self._descendants()\n            if not owned:\n", "            owned = self._descendants()\n            if not {p for p in owned if _live(p)}:\n", SWEEP),
 "M16-broad-mask-owner": (BM, '"scripts/owned_process.py": re.compile(r\'(?<=^PROC = Path\\(")/proc(?="\\)$)\')', '"scripts/owned_process.py": re.compile(r\'/proc\')', BARE),
 "M17-unanchored-mask-support": (BM, '"scripts/process_test_support.py": re.compile(r\'(?<=^PROC = Path\\(")/proc(?="\\)$)\')', '"scripts/process_test_support.py": re.compile(r\'(?<=PROC = Path\\(")/proc(?="\\))\')', BARE),
 "M18-no-stop-on-cancel-sweep": (OP, "                self._signal(self.root_fd, signal.SIGSTOP)\n                self._signal(self.root_fd, signum)\n", "                self._signal(self.root_fd, signum)\n", SWEEP),
 "M19-no-mutation-restore-private": ("tb/verilator/gptp_shadow/mutants.py", "        path.write_bytes(pristine)\n", "", LIFE),
}

def one(pid, checkout, head, work):
    rel, old, new, test = PROBES[pid]
    tree = work / pid
    subprocess.run(["rm", "-rf", str(tree)], check=True); tree.mkdir(parents=True)
    arc = subprocess.run(["git", "-C", str(checkout), "archive", head], check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(tree)], input=arc, check=True)
    path = tree / rel; text = path.read_text()
    count = text.count(old)
    if count != 1:
        return pid, dict(planted=False, anchor_count=count)
    path.write_text(text.replace(old, new, 1))
    tmp = tree.parent / (pid + "-tmp"); tmp.mkdir(exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE="1")
    t0 = time.monotonic()
    try:
        r = subprocess.run(test, cwd=tree, env=env, capture_output=True, text=True, timeout=600)
        code, out = r.returncode, r.stdout + r.stderr
    except subprocess.TimeoutExpired as exc:
        code, out = "TIMEOUT", str(exc)
    (work / (pid + ".log")).write_text(out)
    tail = [l for l in out.splitlines() if l.strip()][-3:]
    return pid, dict(planted=True, file=rel, test=" ".join(test), exit=code,
                     detected=code != 0, seconds=round(time.monotonic() - t0, 1), tail=[t[:300] for t in tail])

checkout, head, work, receipt = Path(sys.argv[1]), sys.argv[2], Path(sys.argv[3]), Path(sys.argv[4])
ids = sys.argv[5:] or list(PROBES)
work.mkdir(parents=True, exist_ok=True)
with ThreadPoolExecutor(max_workers=int(os.environ.get("PROBE_JOBS", "3"))) as pool:
    results = dict(pool.map(lambda i: one(i, checkout, head, work), ids))
old = json.loads(receipt.read_text()) if receipt.exists() else {}
old.update(results); receipt.write_text(json.dumps(old, indent=1, sort_keys=True) + "\n")
for pid in ids:
    r = results[pid]; print(pid, "planted" if r.get("planted") else "NOT PLANTED", r.get("exit"), "DETECTED" if r.get("detected") else "survived", r.get("tail", [""])[-1:] )

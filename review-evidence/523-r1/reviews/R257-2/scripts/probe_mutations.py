#!/usr/bin/env python3
"""Independent reviewer mutation probe of the two focused tests.

Usage: probe_mutations.py CLONE SCRATCH OUTPUT_JSON [JOBS]

Each mutation is applied to its own disposable clone of the review clone at
the exact head (required submodules initialised from the clone's local module
repositories). The owning focused test then runs unmodified from that copy.
A mutation is DETECTED when the test exits non-zero. Anchors are asserted, so
a mutation that no longer applies is reported rather than silently skipped.
"""
import json
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HEAD = "26353960ae2763cc09741d0f7bcc720621bd5148"
SWEEP_TEST = "scripts/test_suite_cancellation.py"
LIFE_TEST = "tb/verilator/gptp_shadow/test_mutant_lifecycle.py"
OP = "scripts/owned_process.py"
PI = "tb/verilator/gptp_shadow/private_inputs.py"
RS = "scripts/run_all_suites.sh"

#: (id, file, old, new, test, what the defect is)
MUTATIONS = [
    ("no-new-session", OP, "argv, cwd=cwd, env=env, start_new_session=True,", "argv, cwd=cwd, env=env,",
     SWEEP_TEST, "owned command shares the owner's process group"),
    ("no-root-notify", OP, "                self._signal(self.root_fd, signal.SIGSTOP)\n                self._signal(self.root_fd, signum)\n                self.root_notified = True",
     "                pass", SWEEP_TEST, "handled signal is not forwarded to the sweep shell"),
    ("no-sigkill-escalation", OP, "signum = signal.SIGKILL if now >= deadline else signal.SIGTERM",
     "signum = signal.SIGTERM", SWEEP_TEST, "stubborn descendants are never killed"),
    ("no-subreaper", OP, "if self.prctl(PR_SET_CHILD_SUBREAPER, 1, 0, 0, 0):",
     "if self.prctl(PR_SET_CHILD_SUBREAPER, 0, 0, 0, 0):", SWEEP_TEST, "detached descendants escape adoption"),
    ("direct-children-only", OP, "            owned.update(more)\n", "            owned.update(more)\n            return {pid: population[pid] for pid in more}\n",
     SWEEP_TEST, "census covers only direct children"),
    ("no-pdeathsig", OP, "preexec_fn=self._die_with_owner,", "", SWEEP_TEST,
     "owned command outlives a hard-stopped owner (the R256-2/R257-1 MAJOR)"),
    ("pdeathsig-term-not-kill", OP, "PR_SET_PDEATHSIG, int(signal.SIGKILL)", "PR_SET_PDEATHSIG, int(signal.SIGTERM)",
     SWEEP_TEST, "parent-death signal is TERM, which the shell traps as a cancellation"),
    ("no-term-trap", RS, "trap 'cancelled TERM 143' TERM\n", "", SWEEP_TEST, "sweep shell has no TERM trap"),
    ("no-int-trap", RS, "trap 'cancelled INT 130' INT\n", "", SWEEP_TEST, "sweep shell has no INT trap"),
    ("no-partial-logs-message", RS, '    echo "partial logs: $OUT" >&2\n', '    :\n', SWEEP_TEST,
     "cancellation no longer names the partial log directory"),
    ("logs-ready-never-set", RS, "  LOGS_READY=1\n", "", SWEEP_TEST,
     "cancellation after log preparation claims logs were not prepared"),
    ("logs-ready-early", RS, "shift\nLOGS_READY=0\n", "shift\nLOGS_READY=1\n", SWEEP_TEST,
     "cancellation during selection or lock wait names a previous invocation's logs as this run's partial logs"),
    ("no-stale-preflight-clear", RS, 'rm -f "$OUT"/*.log "$OUT/preflight"/*.log || exit 2', 'rm -f "$OUT"/*.log || exit 2',
     SWEEP_TEST, "stale prerequisite logs survive into a new invocation"),
    ("no-relative-out-fix", RS, '    *) OUT="$PWD/$OUT" ;;\n', '    *) ;;\n', SWEEP_TEST,
     "relative outdir is resolved against a prerequisite's directory"),
    ("git-env-passthrough", PI, 'env = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}\n    return _read(',
     'env = None\n    return _read(', LIFE_TEST, "caller Git variables reach the identity commands"),
    ("drop-index-file-refusal", PI, '"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE",',
     '"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR",', LIFE_TEST, "one redirect variable no longer refused"),
    ("no-mode-check", PI, "if actual != blob or executable != (mode == \"100755\"):", "if actual != blob:",
     LIFE_TEST, "executable-mode drift accepted"),
    ("no-index-check", PI, "    if expected != indexed:\n        raise InputRefused(f\"index differs from {revision}: {root}\")\n", "",
     LIFE_TEST, "staged/untracked index state accepted"),
    ("hardlink-copies", PI, "        destination.write_bytes(content)\n", "        os.link(source, destination)\n",
     LIFE_TEST, "private copies are hardlinks into caller inputs"),
    ("no-include-closure", PI, "    pending = sorted(names)\n", "    pending = []\n", LIFE_TEST,
     "local C++ headers are not copied"),
    ("garbage-records-skipped", PI, '            raise InputRefused(f"unreadable Git identity record: {row[:120]!r}")',
     "            continue", LIFE_TEST, "an unreadable identity record is ignored"),
    ("no-directory-link-check", PI, "        _directory(root, str(Path(name).parent))\n", "        pass\n", LIFE_TEST,
     "linked input directories are followed"),
    ("no-toplevel-check", PI, '        if Path(_git(root, owner, "rev-parse", "--show-toplevel").strip()) != root:\n            raise InputRefused(f"required dependency has no checkout: {name}")\n',
     "", LIFE_TEST, "dependency toplevel identity not checked (defence in depth)"),
    ("no-pin-check", PI, '        if mode != "160000" or _git(root, owner, "rev-parse", "HEAD").strip() != revision:',
     '        if mode != "160000":', LIFE_TEST, "dependency checkout revision not compared with its gitlink"),
]


def run(argv, **kw):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(argv, env=env, capture_output=True, check=True, **kw)


def base_clone(clone, dest):
    run(["git", "clone", "-q", "--no-local", "--no-checkout", str(clone), str(dest)])
    run(["git", "-C", str(dest), "checkout", "-q", "--detach", HEAD])
    for name in ("gptp-processor", "third_party/verilog-axis"):
        run(["git", "-C", str(dest), "config", f"submodule.{name}.url", str(clone / ".git/modules" / name)])
        run(["git", "-C", str(dest), "-c", "protocol.file.allow=always", "submodule", "update", "-q", "--init", "--", name])


def one(scratch, base, mutation):
    ident, path, old, new, test, what = mutation
    work = scratch / ident
    shutil.copytree(base, work, symlinks=True)
    target = work / path
    text = target.read_text()
    applied = text.count(old) == 1
    rec = {"id": ident, "file": path, "test": test, "defect": what, "anchor_unique": applied}
    if not applied:
        rec["verdict"] = "NOT-APPLIED"
        return rec
    target.write_text(text.replace(old, new, 1))
    tmp = work.parent / (ident + "-tmp")
    tmp.mkdir()
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(TMPDIR=str(tmp), PYTHONDONTWRITEBYTECODE="1")
    t0 = time.monotonic()
    try:
        done = subprocess.run([sys.executable, str(work / test)], cwd=work, env=env, capture_output=True,
                              text=True, timeout=420)
        rec["exit"] = done.returncode
        out = done.stdout + done.stderr
    except subprocess.TimeoutExpired as exc:
        rec["exit"] = "timeout"
        out = (exc.stdout or b"").decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
    rec["seconds"] = round(time.monotonic() - t0, 1)
    rec["verdict"] = "DETECTED" if rec["exit"] != 0 else "SURVIVED"
    lines = [l for l in out.splitlines() if l.strip()]
    rec["evidence_tail"] = "\n".join(lines[-6:])[-1200:]
    return rec


def main():
    clone, scratch, output = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
    jobs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    only = set(sys.argv[5].split(",")) if len(sys.argv) > 5 else None
    scratch.mkdir(parents=True, exist_ok=True)
    base = scratch / "_base"
    if not base.exists():
        base_clone(clone, base)
    todo = [m for m in MUTATIONS if not only or m[0] in only]
    for m in todo:
        for leftover in (scratch / m[0], scratch / (m[0] + "-tmp")):
            if leftover.exists():
                shutil.rmtree(leftover)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        results = list(pool.map(lambda m: one(scratch, base, m), todo))
    for r in results:
        print(f"{r['id']:26s} {r['verdict']:11s} exit={r.get('exit')} {r.get('seconds')}s  {r['defect']}")
    previous = json.loads(output.read_text()) if output.exists() else []
    merged = {r["id"]: r for r in previous}
    merged.update({r["id"]: r for r in results})
    output.write_text(json.dumps(list(merged.values()), indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Run the focused gates this diff touches at the lane's exact HEAD.

Usage: run_gates.py <label> <expected-head>

Commands run in the lane checkout, which must be clean at <expected-head>;
temporary trees go under ../scratch.  Each command's argv, environment
overrides, exit status, duration and raw output are written to
../receipts/gates-<label>/.  At most eight commands run at once.
"""

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
PACKET = HERE.parent
SCRATCH = PACKET / "scratch"
LOCALES = SCRATCH / "locales"
LANE = Path("$LANES/423-retained-redundant-replay")
DEV = "483a133ed08867ea0d300d2b4a027b5b48a4282f"

PARENTS = {
    "default": {},
    "utf8-mode": {"PYTHONUTF8": "1"},
    "utf8-strict": {"LC_ALL": "en_US.UTF-8", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"},
    "ascii": {"LC_ALL": "C", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0"},
    "latin1": {"LC_ALL": "en_US.ISO-8859-1", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0",
               "LOCPATH": str(LOCALES)},
    "big5": {"LC_ALL": "zh_TW.BIG5", "PYTHONUTF8": "0", "PYTHONCOERCECLOCALE": "0",
             "LOCPATH": str(LOCALES)},
}

COMMANDS = [(f"selftest-{name}", ("python3", "-B", "scripts/check_merge_containment.py",
                                  "--selftest"), env)
            for name, env in PARENTS.items()]
COMMANDS += [(name, argv, {}) for name, argv in (
    ("docs-check", ("python3", "scripts/docs_check.py")),
    ("em-dash", ("python3", "scripts/check_em_dash.py", "--base", DEV)),
    ("em-dash-selftest", ("python3", "scripts/check_em_dash.py", "--selftest")),
    ("doc-style", ("python3", "scripts/check_doc_style.py")),
    ("doc-paths", ("python3", "scripts/check_doc_paths.py")),
    ("gen-toc-check", ("python3", "scripts/gen_toc.py", "--check")),
    ("gen-toc-anchors", ("python3", "scripts/gen_toc.py", "--verify-anchors")),
    ("feature-status", ("python3", "scripts/check_feature_status.py")),
    ("py-idiom", ("python3", "scripts/check_py_idiom.py")),
    ("py-idiom-selftest", ("python3", "scripts/check_py_idiom.py", "--selftest")),
    ("hygiene", ("python3", "scripts/check_hygiene.py", "--check")),
    ("hygiene-selftest", ("python3", "scripts/check_hygiene.py", "--selftest")),
    ("naming", ("python3", "scripts/measure_naming.py", "--check")),
    ("fail-fast", ("python3", "scripts/measure_fail_fast.py", "--check")),
    ("test-evidence", ("python3", "scripts/measure_test_evidence.py", "--check")),
    ("todo-ownership", ("python3", "scripts/check_todo_ownership.py")),
    ("whitespace", ("git", "diff", "--check", DEV, "HEAD")),
    ("whitespace-reviewed-head", ("git", "diff", "--check",
                                  "4671e582cfa4bba4809b9e3a354ce5b6eb967f99", "HEAD")),
)]


def run(name, argv, env_extra, outdir):
    env = dict(os.environ, TMPDIR=str(SCRATCH / "tmp-gates" / name), **env_extra)
    env.pop("PYTHONIOENCODING", None)
    if "LOCPATH" not in env_extra:
        env.pop("LOCPATH", None)
    Path(env["TMPDIR"]).mkdir(parents=True, exist_ok=True)
    start = time.monotonic()
    proc = subprocess.run(argv, cwd=LANE, env=env, capture_output=True, timeout=3600)
    seconds = round(time.monotonic() - start, 3)
    (outdir / (name + ".out")).write_bytes(proc.stdout + b"\n--stderr--\n" + proc.stderr)
    text = proc.stdout.decode("utf-8", "backslashreplace")
    record = {"name": name, "argv": list(argv), "cwd": str(LANE), "env": env_extra,
              "rc": proc.returncode, "seconds": seconds,
              "ok_lines": sum(1 for line in text.splitlines() if line.startswith("  ok")),
              "fail_lines": sum(1 for line in text.splitlines() if line.startswith("  FAIL")),
              "not_run": [line.strip() for line in text.splitlines() if "NOT RUN" in line],
              "tail": text.strip().splitlines()[-2:]}
    return name, record


def main():
    label, expected = sys.argv[1], sys.argv[2]
    head = subprocess.run(("git", "rev-parse", "HEAD"), cwd=LANE, capture_output=True,
                          text=True, check=True).stdout.strip()
    status = subprocess.run(("git", "status", "--porcelain"), cwd=LANE, capture_output=True,
                            check=True).stdout
    if head != expected or status:
        raise SystemExit(f"lane is not clean at {expected}: HEAD {head}, status {status!r}")
    outdir = PACKET / "receipts" / ("gates-" + label)
    outdir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=8) as pool:
        results = dict(pool.map(lambda c: run(*c, outdir), COMMANDS))
    after = subprocess.run(("git", "rev-parse", "HEAD"), cwd=LANE, capture_output=True,
                           text=True, check=True).stdout.strip()
    status = subprocess.run(("git", "status", "--porcelain"), cwd=LANE, capture_output=True,
                            check=True).stdout
    summary = {"head_before": head, "head_after": after, "status_after": status.decode(),
               "results": results}
    (outdir / "results.json").write_text(json.dumps(summary, indent=1) + "\n")
    for name, value in results.items():
        print(f"{name:26} rc={value['rc']:<3} {value['seconds']:>8}s ok={value['ok_lines']:<4}"
              f" fail={value['fail_lines']} {value['not_run'] or ''} {value['tail'][-1:]}")
    print(f"HEAD after: {after}; status clean: {not status}")
    return 0 if all(v["rc"] == 0 for v in results.values()) and not status else 1


if __name__ == "__main__":
    sys.exit(main())

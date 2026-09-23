#!/usr/bin/env python3
"""Run the composition gate bank for #504 / PR #521 on the candidate clone.

Portable: CLONE (default: current directory) is the candidate checkout and
OUT (default: ./receipts/gates) receives one log per command plus
results.json. Each command runs with cwd=CLONE; argv, exit status, seconds and
a SHA-256 of the log are recorded. Up to JOBS (default 4, max 8) run at once.
"""
import concurrent.futures
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time

CLONE = pathlib.Path(os.environ.get("CLONE", ".")).resolve()
OUT = pathlib.Path(os.environ.get("OUT", "receipts/gates")).resolve()
JOBS = min(int(os.environ.get("JOBS", "4")), 8)

BASE = "18271bebbd1a4abf2e32e7783477573114e2a5fa"      # candidate first parent
DEV = "ede8d48ecd7c7f589a14b957951f040d92c99c70"       # live dev
PR_HEAD = "4876423d4cf8e89b820c56f8339f230abefb4827"   # reviewed source head
CAND = "50c0d00ac3e7b7aa319ba4eab995d7e12b89149e"      # candidate

PY = [sys.executable, "-B"]
CHANGED_PY = [
    "scripts/check_baremetal_only.py", "scripts/ci_events.py",
    "scripts/ci_rv32_sdk.py", "scripts/ci_rv32_sdk_selftest.py",
    "sw/builder/test_builder.py", "sw/builder/test_firmware_compiler.py",
]

COMMANDS = [
    ("G01-merge-tree", ["git", "merge-tree", "--write-tree", BASE, PR_HEAD]),
    ("G02-diff-check", ["git", "diff", "--check", BASE, CAND]),
    ("G03-baremetal-check", PY + ["scripts/check_baremetal_only.py", "--check"]),
    ("G04-baremetal-selftest", PY + ["scripts/check_baremetal_only.py", "--selftest"]),
    ("G05-ci-events-check", PY + ["scripts/ci_events.py", "--check"]),
    ("G06-ci-events-selftest", PY + ["scripts/ci_events.py", "--selftest"]),
    ("G07-ci-scope-selftest", PY + ["scripts/ci_scope.py", "--selftest"]),
    ("G08-docs-check", PY + ["scripts/docs_check.py"]),
    ("G09-docs-check-selftest", PY + ["scripts/docs_check.py", "--selftest"]),
    ("G10-toc-check", PY + ["scripts/gen_toc.py", "--check"]),
    ("G11-toc-anchors", PY + ["scripts/gen_toc.py", "--verify-anchors"]),
    ("G12-toc-selftest", PY + ["scripts/gen_toc.py", "--selftest"]),
    ("G13-em-dash-base-parent", PY + ["scripts/check_em_dash.py", "--base", BASE]),
    ("G14-em-dash-base-dev", PY + ["scripts/check_em_dash.py", "--base", DEV]),
    ("G15-em-dash-selftest", PY + ["scripts/check_em_dash.py", "--selftest"]),
    ("G16-doc-style", PY + ["scripts/check_doc_style.py"]),
    ("G17-doc-style-selftest", PY + ["scripts/check_doc_style.py", "--selftest"]),
    ("G18-doc-paths", PY + ["scripts/check_doc_paths.py"]),
    ("G19-solution-docs", PY + ["scripts/check_solution_docs.py"]),
    ("G20-archive", PY + ["scripts/check_archive.py"]),
    ("G21-hygiene", PY + ["scripts/check_hygiene.py", "--check"]),
    ("G22-todo-ownership", PY + ["scripts/check_todo_ownership.py"]),
    ("G23-feature-status", PY + ["scripts/check_feature_status.py"]),
    ("G24-submodule-docs", PY + ["scripts/check_submodule_docs.py"]),
    ("G25-py-idiom", PY + ["scripts/check_py_idiom.py"]),
    ("G26-sh-idiom", PY + ["scripts/check_sh_idiom.py"]),
    ("G27-fail-fast", PY + ["scripts/measure_fail_fast.py", "--check"]),
    ("G28-test-evidence", PY + ["scripts/measure_test_evidence.py", "--check"]),
    ("G29-test-evidence-selftest", PY + ["scripts/measure_test_evidence.py", "--selftest"]),
    ("G30-naming", PY + ["scripts/measure_naming.py", "--check"]),
    ("G31-control-flow-selftest", PY + ["scripts/measure_control_flow.py", "--selftest"]),
    ("G32-cohesion-selftest", PY + ["scripts/measure_cohesion.py", "--selftest"]),
    ("G33-pp-srcs", PY + ["scripts/pp_srcs.py", "--check", "--selftest"]),
    ("G34-rv32-sdk-selftest", PY + ["scripts/ci_rv32_sdk_selftest.py"]),
    ("G35-firmware-compiler-selftest", PY + ["sw/builder/test_firmware_compiler.py", "--selftest"]),
    ("G36-py-compile", PY + ["-c", "import sys\n"
                             "for f in sys.argv[1:]:\n"
                             "    compile(open(f, 'rb').read(), f, 'exec')\n"
                             "print('compiled in memory', len(sys.argv)-1)"] + CHANGED_PY),
    ("G37-cpp-idiom", PY + ["scripts/check_cpp_idiom.py"]),
    ("G38-sv-idiom", PY + ["scripts/check_sv_idiom.py"]),
]


def run(name, argv):
    log = OUT / f"{name}.log"
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    start = time.monotonic()
    with open(log, "wb") as fh:
        proc = subprocess.run(argv, cwd=CLONE, stdout=fh, stderr=subprocess.STDOUT,
                              env=env, check=False)
    seconds = round(time.monotonic() - start, 3)
    digest = hashlib.sha256(log.read_bytes()).hexdigest()
    shown = [a if not a.startswith(sys.executable) else "python3" for a in argv]
    return {"name": name, "argv": shown, "exit_code": proc.returncode,
            "seconds": seconds, "log": log.name, "log_sha256": digest}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    head = subprocess.run(["git", "rev-parse", "HEAD", "HEAD^{tree}"], cwd=CLONE,
                          capture_output=True, text=True, check=True).stdout.split()
    with concurrent.futures.ThreadPoolExecutor(max_workers=JOBS) as pool:
        results = list(pool.map(lambda c: run(*c), COMMANDS))
    summary = {"head": head[0], "tree": head[1], "python": sys.version.split()[0],
               "jobs": JOBS, "results": results}
    (OUT / "results.json").write_text(json.dumps(summary, indent=1) + "\n")
    for r in results:
        print(f"{r['exit_code']:>3} {r['seconds']:>8.3f}s {r['name']}")
    failed = [r["name"] for r in results if r["exit_code"] != 0]
    print("FAILED:", failed if failed else "none")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

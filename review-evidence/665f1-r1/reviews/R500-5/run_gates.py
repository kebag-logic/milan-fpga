#!/usr/bin/env python3
"""Run focused composition checks in the foreground, retaining raw receipts."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import sys
import time

PACKET = Path(__file__).resolve().parent
SCRATCH = PACKET / "scratch"
TASKS = {
    "docs": ["scripts/docs_check.py"],
    "toc": ["scripts/gen_toc.py", "--check"],
    "anchors": ["scripts/gen_toc.py", "--verify-anchors"],
    "em-dash": ["scripts/check_em_dash.py", "--base", "9e05246c5455b2a1df26038345709437e13c6f18"],
    "ci-events": ["scripts/ci_events.py", "--check"],
    "ci-events-selftest": ["scripts/ci_events.py", "--selftest"],
    "record-space": ["scripts/check_nvm_record_space.py", "--self-test"],
    "capture-record": ["scripts/check_nvm_capture.py"],
    "module-matrix": ["docs/traceability/gen_module_matrix.py", "--check"],
    "mailbox-records": ["sw/mailbox/gen_mailbox.py", "--check", "--crosscheck"],
    "doc-paths": ["scripts/check_doc_paths.py"],
    "submodule-docs": ["scripts/check_submodule_docs.py"],
    "ci-scope-selftest": ["scripts/ci_scope.py", "--selftest"],
}


def run(item):
    name, args = item
    env = dict(os.environ, TMPDIR=str(SCRATCH), PYTHONDONTWRITEBYTECODE="1",
               GIT_NO_REPLACE_OBJECTS="1")
    start = time.monotonic()
    with (PACKET / (name + ".log")).open("wb") as log:
        try:
            result = subprocess.run([sys.executable, *args], env=env,
                                    stdout=log, stderr=subprocess.STDOUT, timeout=300)
            rc = result.returncode
        except subprocess.TimeoutExpired:
            log.write(b"\nREVIEW HARNESS TIMEOUT: 300 seconds\n")
            rc = 124
    (PACKET / (name + ".rc")).write_text(str(rc) + "\n")
    receipt = {"name": name, "command": ["python3", *args], "rc": rc,
               "elapsed_seconds": round(time.monotonic() - start, 3)}
    print(json.dumps(receipt), flush=True)
    return receipt


def main():
    SCRATCH.mkdir(exist_ok=True)
    selected = sys.argv[1:] or list(TASKS)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(run, [(name, TASKS[name]) for name in selected]))
    record = PACKET / "gate-results.json"
    previous = json.loads(record.read_text()) if record.exists() else []
    merged = {r["name"]: r for r in previous}
    merged.update({r["name"]: r for r in results})
    record.write_text(json.dumps(list(merged.values()), indent=2) + "\n")
    return int(any(r["rc"] for r in results))


if __name__ == "__main__":
    sys.exit(main())

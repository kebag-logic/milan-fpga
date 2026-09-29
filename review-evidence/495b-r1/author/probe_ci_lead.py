#!/usr/bin/env python3
"""Probe R354-3 S2: does CI_WORKFLOWS.md's lead definition reach the classifier's answer?

Run from the repository root. Reads scripts/ci_scope.py by path (never edits
it) and the lead paragraph of docs/testing/CI_WORKFLOWS.md, then checks:
  1. the classifier files the tap page as relevant, and its reader is under a
     gated root and outside DOCS_JOB_PY (the case the lead must cover);
  2. the lead no longer states the #444 criterion that files that page as
     documentation ("reads without `docs-check` reading it too");
  3. the lead's exemption is the classifier's: DOCS_JOB_PY is the builder bank
     alone, docs.yml runs it, and the root count it cites is GATED_ROOTS's.
Exit 0 only when all hold.
"""
import importlib.util
import re
import subprocess
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("ci_scope", Path("scripts/ci_scope.py"))
scope = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scope)
page = Path("docs/testing/CI_WORKFLOWS.md").read_text()
lead = page.split("A change containing only documentation", 1)[1].split("Everything else", 1)[0]
lead = " ".join(lead.split())
print("lead:", lead)
failures = []
tap = "docs/AAF_LATENCY_TAPS.md"
verdict = subprocess.run([sys.executable, "scripts/ci_scope.py"], input=tap + "\n", text=True,
                         capture_output=True, check=True).stdout.strip()
reader = "sw/builder/test_clock_contract.py"
if verdict != "true" or tap not in scope.GATE_READ_DOCS:
    failures.append(f"classifier no longer files {tap} as relevant ({verdict})")
if reader.split("/")[0] not in scope.GATED_ROOTS or reader in scope.DOCS_JOB_PY:
    failures.append(f"{reader} is not a gated module outside DOCS_JOB_PY")
if "reads without `docs-check` reading it too" in lead:
    failures.append("lead still states the criterion that files the tap page as documentation")
if scope.DOCS_JOB_PY != ("sw/builder/test_builder.py",):
    failures.append(f"DOCS_JOB_PY is {scope.DOCS_JOB_PY}, not the builder bank alone")
if "python3 sw/builder/test_builder.py" not in Path(".github/workflows/docs.yml").read_text():
    failures.append("docs.yml does not run the builder bank")
words = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
if not re.search(rf"\b{words[len(scope.GATED_ROOTS)]} roots\b", lead):
    failures.append(f"lead does not cite the {len(scope.GATED_ROOTS)} gated roots")
if "builder bank" not in lead or "tap page" not in lead:
    failures.append("lead names neither the builder-bank exemption nor the tap page")
for failure in failures:
    print("FAIL", failure)
print("PROBE", "PASS" if not failures else "FAIL")
sys.exit(1 if failures else 0)

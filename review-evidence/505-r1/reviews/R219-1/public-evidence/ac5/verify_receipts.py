"""Check completed, intentionally failing AC5 act receipts; not a CI pass."""
from pathlib import Path
import json
import sys
root = Path(sys.argv[1])
results = json.loads((root / "ac5-act/results.json").read_text())
assert results["head"] == "66ba210630ff7f412e5706427b3ea976ebee3ba2"
assert len(results["results"]) == 2
assert [r["exit_code"] for r in results["results"]] == [1, 1], "Require workflow failures, not setup/trust refusals"
assert (root / "ac5-act/complete.json").is_file(), "Both invocations must finish cleanup"
docs = (root / "ac5-act/01.log").read_text()
rtl = (root / "ac5-act/02.log").read_text()
normal = (root / "act-draft-fast/01.log").read_text()
assert "act-ci: docs: PASS at 6af65a151663e1301f1983a6c9d22650a0b35da9" in normal
for text in (docs, rtl):
    assert "66ba210630ff7f412e5706427b3ea976ebee3ba2" in text
    assert "job `docs-check`" in text and "`Python idiom gate`" in text
    assert "script is not the canonical form: line 1" in text
    assert "python3 scripts/check_py_idiom.py || true" in text
assert any("Success - Main Python idiom gate" in l for l in docs.splitlines())
assert any("Failure - Main CI event and SHA contract gate" in l for l in docs.splitlines())
assert any("docs-check" in l and "Job failed" in l for l in docs.splitlines())
assert any("Failure - Main Hold every workflow file to its contract" in l for l in rtl.splitlines())
for job in ("full-ci-gate", "verilator-suites", "yosys-portability"):
    assert any(job in l and "Job failed" in l for l in rtl.splitlines()), job
assert "act-ci: docs: FAILED (1)" in docs
assert "act-ci: rtl-full: FAILED (1)" in rtl
print("AC5 expected-failure observations present; manually inspect raw step/job context before accepting.")

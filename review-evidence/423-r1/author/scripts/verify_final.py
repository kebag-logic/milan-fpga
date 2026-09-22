"""Verify the final receipt bindings and unchanged original self-test population."""
import hashlib
import json
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parent.parent
state = json.loads((root / "receipts/final-state.json").read_text())
assert subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip() == state["head"]
assert subprocess.check_output(["git", "status", "--porcelain=v1"], text=True) == ""
assert subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], text=True).strip() == state["tree"]
original = [s for s in (root / "receipts/baseline-selftest.log").read_text().splitlines() if s.startswith("  ok   ")]
final = [s for s in (root / "receipts/final-selftest.stdout").read_text().splitlines() if s.startswith("  ok   ")]
assert len(original) == 145 and len(final) == 326 and final[:145] == original
for name in ("final-selftest", "final-public-matrix", "final-public-history", "final-guard-mutations", "final-alignment-probe", "em-dash"):
    receipt = json.loads((root / "receipts" / (name + ".json")).read_text())
    assert receipt["exit"] == 0 and receipt["head"] == state["head"] and receipt["index_tree"] == state["tree"]
    for path, digest in receipt["source_sha256"].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
for name, result in json.loads((root / "receipts/gates-summary.json").read_text()):
    receipt = json.loads((root / "receipts" / (name + ".json")).read_text())
    assert result == receipt["exit"] == 0 and receipt["index_tree"] == state["tree"]
    for path, digest in receipt["source_sha256"].items():
        assert hashlib.sha256(Path(path).read_bytes()).hexdigest() == digest
print("PASS: exact final head/tree, clean checkout, 145 unchanged + 181 new assertions, and receipt bindings.")

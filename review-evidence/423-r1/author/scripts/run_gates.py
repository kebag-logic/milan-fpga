"""Authorized focused repository gates; no builder, simulation or synthesis sweep."""
import json
from pathlib import Path
import subprocess
import sys

runner = Path(__file__).with_name("run_receipt.py")
gates = (
    ("docs-checked-tree", "scripts/docs_check.py"),
    ("toc-checked-tree", "scripts/gen_toc.py", "--check"),
    ("py-idiom-checked-tree", "scripts/check_py_idiom.py"),
    ("hygiene-checked-tree", "scripts/check_hygiene.py", "--check"),
    ("fail-fast", "scripts/measure_fail_fast.py", "--check"),
    ("test-evidence", "scripts/measure_test_evidence.py", "--check"),
    ("todo-ownership", "scripts/check_todo_ownership.py"),
    ("baremetal", "scripts/check_baremetal_only.py", "--check"),
    ("feature-status", "scripts/check_feature_status.py", "--self-test"),
    ("doc-paths", "scripts/check_doc_paths.py"),
    ("archive", "scripts/check_archive.py"),
    ("pp-sources", "scripts/pp_srcs.py", "--check"),
    ("soc-sources", "scripts/check_soc_sources.py"),
    ("source-lists-checked-tree", "scripts/check_rtl_source_lists.py"),
    ("port-contracts", "scripts/check_port_contracts.py"),
    ("naming", "scripts/measure_naming.py", "--check"),
    ("sv-idiom", "scripts/check_sv_idiom.py"),
    ("cpp-idiom", "scripts/check_cpp_idiom.py"),
    ("sh-idiom", "scripts/check_sh_idiom.py"),
    ("lint-rtl", "scripts/lint_rtl.py", "--check"),
)
results = []
for name, *args in gates:
    p = subprocess.run([sys.executable, str(runner), name, sys.executable, *args])
    results.append((name, p.returncode))
(root := runner.parent.parent).joinpath("receipts/gates-summary.json").write_text(json.dumps(results, indent=2) + "\n")
print("GATES", results)
sys.exit(any(rc for _, rc in results))

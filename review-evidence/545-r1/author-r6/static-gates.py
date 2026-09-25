import importlib.util
from pathlib import Path
import sys
spec = importlib.util.spec_from_file_location("gate_runner", Path(__file__).with_name("run-gates.py"))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)
gates = [
 ("docs", ["python3", "scripts/docs_check.py"]),
 ("em-dash", ["python3", "scripts/check_em_dash.py", "--base", "5c78ce2e9d831e588e759b696ed549804327e4d8"]),
 ("doc-style", ["python3", "scripts/check_doc_style.py"]),
 ("toc-check", ["python3", "scripts/gen_toc.py", "--check"]),
 ("toc-anchors", ["python3", "scripts/gen_toc.py", "--verify-anchors"]),
 ("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
 ("module-matrix", ["python3", "docs/traceability/gen_module_matrix.py", "--check"]),
 ("source-lists", ["python3", "scripts/check_rtl_source_lists.py"]),
 ("sv-idiom", ["python3", "scripts/check_sv_idiom.py"]),
 ("cpp-idiom", ["python3", "scripts/check_cpp_idiom.py"]),
 ("py-idiom", ["python3", "scripts/check_py_idiom.py"]),
 ("port-contracts", ["python3", "scripts/check_port_contracts.py"]),
 ("naming", ["python3", "scripts/measure_naming.py", "--check"]),
 ("test-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
 ("test-evidence-selftest", ["python3", "scripts/measure_test_evidence.py", "--selftest"]),
 ("diff-check", ["git", "diff", "--check"]),
]
failed = []
for name, command in gates:
    if r.run(name, command):
        failed.append(name)
print("Failed:", failed)
sys.exit(bool(failed))

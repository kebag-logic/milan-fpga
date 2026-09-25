import json, shlex, subprocess, sys
from pathlib import Path
out = Path(__file__).parent
sets = {
 "nvm": [
  ("nvm-backend", ["make", "-C", "tb/verilator/nvm_backend"]),
  ("nvm-hosttest", ["python3", "sw/firmware/nvm_hosttest/test_nvm_firmware.py", "--self-test"]),
 ],
 "static": [
  ("baremetal-only", ["python3", "scripts/check_baremetal_only.py", "--check"]),
  ("docs-git", ["python3", "-B", "scripts/docs_check.py"]),
  ("docs-no-git", ["env", "GIT_DIR=/dev/null", "python3", "-B", "scripts/docs_check.py"]),
  ("em-dash", ["python3", "scripts/check_em_dash.py", "--base", "a3d795ae24202bb00cfa7ba0f5bfb4fffc1eb8e4"]),
  ("doc-style", ["python3", "scripts/check_doc_style.py"]),
  ("toc", ["python3", "scripts/gen_toc.py", "--check"]),
  ("anchors", ["python3", "scripts/gen_toc.py", "--verify-anchors"]),
  ("doc-paths", ["python3", "scripts/check_doc_paths.py"]),
  ("matrix", ["python3", "docs/traceability/gen_module_matrix.py", "--check"]),
  ("xvlog", ["python3", "scripts/xvlog_gate.py", "--check"]),
  ("sv-idiom", ["python3", "scripts/check_sv_idiom.py"]),
  ("cpp-idiom", ["python3", "scripts/check_cpp_idiom.py"]),
  ("py-idiom", ["python3", "scripts/check_py_idiom.py"]),
  ("port-contracts", ["python3", "scripts/check_port_contracts.py"]),
  ("naming", ["python3", "scripts/measure_naming.py", "--check"]),
  ("test-evidence", ["python3", "scripts/measure_test_evidence.py", "--check"]),
  ("diff", ["git", "diff", "--check"]),
  ("diff-staged", ["git", "diff", "--cached", "--check"]),
 ]}
sets['docs-final'] = [(name, argv) for name, argv in sets['static'] if name in {
 'baremetal-only', 'docs-git', 'docs-no-git', 'em-dash', 'doc-style', 'toc',
 'anchors', 'doc-paths', 'diff', 'diff-staged'}]
failed = []
for name, argv in sets[sys.argv[1]]:
 print("RUN", name, shlex.join(argv), flush=True)
 with (out / ("gate-" + name + ".log")).open("w") as log:
  log.write("COMMAND " + shlex.join(argv) + "\n")
  log.flush()
  result = subprocess.run(argv, stdout=log, stderr=subprocess.STDOUT, timeout=10800)
 (out / ("gate-" + name + ".rc")).write_text(str(result.returncode) + "\n")
 with (out / "gate-results.jsonl").open("a") as ledger:
  ledger.write(json.dumps(dict(gate=name, command=argv, rc=result.returncode)) + "\n")
 print("RESULT", name, result.returncode, flush=True)
 if result.returncode: failed.append(name)
if failed: raise SystemExit("FAILED: " + ", ".join(failed))

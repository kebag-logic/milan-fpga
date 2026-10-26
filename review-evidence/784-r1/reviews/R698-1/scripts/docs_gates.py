import subprocess
import sys
commands = [
 ["scripts/docs_check.py"], ["scripts/check_feature_status.py"],
 ["scripts/check_em_dash.py", "--base", "d385b38e"],
 ["scripts/check_doc_style.py"], ["scripts/gen_toc.py", "--selftest"],
 ["scripts/gen_toc.py", "--verify-anchors"], ["scripts/gen_toc.py", "--check"],
 ["scripts/check_doc_paths.py"], ["scripts/check_baremetal_only.py", "--check"],
 ["docs/DOC_MAP.gen.py", "--check"], ["scripts/ci_gate_workflows.py", "--check"],
 ["scripts/generate_ci_evidence_pins.py", "--check"],
]
failed = []
for cmd in commands:
    print("COMMAND", *cmd, flush=True)
    rc = subprocess.run([sys.executable, *cmd]).returncode
    print("RETURN", rc, flush=True)
    if rc: failed.append(cmd)
print("FAILED", failed, flush=True)
sys.exit(bool(failed))

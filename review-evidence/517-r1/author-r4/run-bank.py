from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
static = [
 ('baremetal', ['python3','scripts/check_baremetal_only.py','--check']),
 ('baremetal-selftest', ['python3','scripts/check_baremetal_only.py','--selftest']),
 ('docs-git', ['python3','-B','scripts/docs_check.py']),
 ('docs-no-git', ['env','GIT_DIR=/nonexistent/517-no-git','python3','-B','scripts/docs_check.py']),
 ('em-dash', ['python3','scripts/check_em_dash.py','--base','5c78ce2e9d831e588e759b696ed549804327e4d8']),
 ('doc-style', ['python3','scripts/check_doc_style.py']),
 ('toc-check', ['python3','scripts/gen_toc.py','--check']),
 ('toc-anchors', ['python3','scripts/gen_toc.py','--verify-anchors']),
 ('doc-paths', ['python3','scripts/check_doc_paths.py']),
 ('module-matrix', ['python3','docs/traceability/gen_module_matrix.py','--check']),
 ('xvlog', ['python3','scripts/xvlog_gate.py','--check']),
 ('rtl-source-lists', ['python3','scripts/check_rtl_source_lists.py']),
 ('sv-idiom', ['python3','scripts/check_sv_idiom.py']),
 ('rtl-lint', ['python3','scripts/lint_rtl.py','--check']),
 ('cpp-idiom', ['python3','scripts/check_cpp_idiom.py']),
 ('py-idiom', ['python3','scripts/check_py_idiom.py']),
 ('port-contracts', ['python3','scripts/check_port_contracts.py']),
 ('naming', ['python3','scripts/measure_naming.py','--check']),
 ('test-evidence', ['python3','scripts/measure_test_evidence.py','--check']),
 ('behave', ['bash','-c','cd tests && behave --no-capture -f plain']),
 ('diff-check', ['git','diff','--check']),
 ('ci-events', ['python3','scripts/ci_events.py','--check']),
 ('ci-events-selftest', ['python3','scripts/ci_events.py','--selftest']),
 ('phase-observation', ['python3','tb/verilator/milan_dp/test_render_phase_observation.py']),
]
builder = [('builder-sdk', ['python3',str(out/'builder-sdk.py')]),
           ('builder-no-compiler', ['python3',str(out/'builder-no-compiler.py')])]
failed = []
for name, argv in {'static':static, 'builder':builder}[sys.argv[1]]:
    result = subprocess.run(['python3',str(out/'run-gate.py'),name+(sys.argv[2] if len(sys.argv)>2 else ''),*argv], check=False)
    if result.returncode:
        failed.append([name,result.returncode])
print('BANK FAILURES:',failed,flush=True)
sys.exit(bool(failed))

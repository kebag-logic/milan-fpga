"""Run the assigned independent gates sequentially in the foreground."""
from pathlib import Path
import subprocess
import sys

RUNNER = Path(__file__).with_name('run_gate.py')
checks = [
    ('rtl-lint', '1800', ['python3', 'scripts/lint_rtl.py', '--check', '--jobs', '8']),
    ('ci-scope', '600', ['python3', 'scripts/ci_scope.py', '--selftest']),
    ('baremetal-check', '600', ['python3', 'scripts/check_baremetal_only.py', '--check']),
    ('baremetal-selftest', '600', ['python3', 'scripts/check_baremetal_only.py', '--selftest']),
    ('docs', '600', ['python3', 'scripts/docs_check.py']),
    ('doc-style', '600', ['python3', 'scripts/check_doc_style.py']),
    ('doc-style-selftest', '600', ['python3', 'scripts/check_doc_style.py', '--selftest']),
    ('em-dash', '600', ['python3', 'scripts/check_em_dash.py', '--base', '6d5ebd7357c1e468e446f18a61527c5be6118a04']),
    ('doc-paths', '600', ['python3', 'scripts/check_doc_paths.py']),
    ('toc', '600', ['python3', 'scripts/gen_toc.py', '--check']),
    ('toc-selftest', '600', ['python3', 'scripts/gen_toc.py', '--selftest']),
    ('gptp-docs', '600', ['python3', 'scripts/check_gptp_docs.py', '--with-submodule']),
    ('feature-status', '600', ['python3', 'scripts/check_feature_status.py', '--self-test']),
    ('solution-docs', '600', ['python3', 'scripts/check_solution_docs.py']),
    ('submodule-docs', '600', ['python3', 'scripts/check_submodule_docs.py']),
    ('module-matrix', '600', ['python3', 'docs/traceability/gen_module_matrix.py', '--check']),
    ('diagram-pngs', '600', ['python3', 'scripts/check_diagram_pngs.py']),
    ('archive', '600', ['python3', 'scripts/check_archive.py']),
    ('source-lists', '600', ['python3', 'scripts/check_rtl_source_lists.py']),
    ('sv-idiom', '600', ['python3', 'scripts/check_sv_idiom.py']),
    ('cpp-idiom', '600', ['python3', 'scripts/check_cpp_idiom.py']),
    ('py-idiom', '600', ['python3', 'scripts/check_py_idiom.py']),
    ('hygiene', '600', ['python3', 'scripts/check_hygiene.py', '--check']),
    ('test-evidence', '600', ['python3', 'scripts/measure_test_evidence.py', '--check']),
    ('diff-check', '120', ['git', 'diff', '--check', '6d5ebd7357c1e468e446f18a61527c5be6118a04', 'HEAD']),
]
failures = []
for name, seconds, command in checks:
    result = subprocess.run(['rtk', 'proxy', 'python3', str(RUNNER), name, seconds, *command], check=False)
    if result.returncode:
        failures.append(name)
print('Failed gates:', failures, flush=True)
sys.exit(bool(failures))

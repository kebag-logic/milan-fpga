from run_gate import OUT, ROOT, run

commands = [
('baremetal', ['python3', 'scripts/check_baremetal_only.py', '--check']),
('baremetal-selftest', ['python3', 'scripts/check_baremetal_only.py', '--selftest']),
('docs-git', ['python3', '-B', 'scripts/docs_check.py']),
('em-dash', ['python3', 'scripts/check_em_dash.py', '--base', '5c78ce2e9d831e588e759b696ed549804327e4d8']),
('doc-style', ['python3', 'scripts/check_doc_style.py']),
('toc', ['python3', 'scripts/gen_toc.py', '--check']),
('anchors', ['python3', 'scripts/gen_toc.py', '--verify-anchors']),
('doc-paths', ['python3', 'scripts/check_doc_paths.py']),
('matrix', ['python3', 'docs/traceability/gen_module_matrix.py', '--check']),
('xvlog', ['python3', 'scripts/xvlog_gate.py', '--check']),
('rtl-sources', ['python3', 'scripts/check_rtl_source_lists.py']),
('sv-idiom', ['python3', 'scripts/check_sv_idiom.py']),
('rtl-lint', ['python3', 'scripts/lint_rtl.py', '--check']),
('cpp-idiom', ['python3', 'scripts/check_cpp_idiom.py']),
('py-idiom', ['python3', 'scripts/check_py_idiom.py']),
('port-contracts', ['python3', 'scripts/check_port_contracts.py']),
('naming', ['python3', 'scripts/measure_naming.py', '--check']),
('test-evidence', ['python3', 'scripts/measure_test_evidence.py', '--check']),
('ci-events', ['python3', 'scripts/ci_events.py', '--check']),
('ci-events-selftest', ['python3', 'scripts/ci_events.py', '--selftest']),
('phase-observation', ['python3', 'tb/verilator/milan_dp/test_render_phase_observation.py']),
('diff-check', ['git', 'diff', '--check']),
]
failed = []
for name, argv in commands:
    if run(name, argv):
        failed.append(name)
if run('behave', ['behave', '--no-capture', '-f', 'plain'], cwd=ROOT / 'tests'):
    failed.append('behave')
print('Failed:', failed)
raise SystemExit(bool(failed))

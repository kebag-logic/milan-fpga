"""Execute the assigned static and documentation gates, recording each exit."""
from pathlib import Path
import subprocess
import sys

OUT = Path(__file__).resolve().parent
commands = [
 ('test-evidence', ['python3', 'scripts/measure_test_evidence.py', '--check']),
 ('port-contracts', ['python3', 'scripts/check_port_contracts.py']),
 ('packer-tests', ['python3', 'protocol-processor/tb/desc_store/test_gen_desc_image.py']),
 ('py-idiom', ['python3', 'scripts/check_py_idiom.py']),
 ('diagram-check', ['python3', 'docs/diagrams/submodule_boundaries.gen.py', '--check']),
 ('diagram-selftest', ['python3', 'docs/diagrams/submodule_boundaries.gen.py', '--selftest']),
]
for script, options in [
 ('docs_check', [[], ['--selftest']]),
 ('check_em_dash', [['--base','682ecf0cb995473b72d5b4921088053ba753fc93'], ['--selftest']]),
 ('check_doc_style', [[], ['--selftest']]),
 ('check_gptp_docs', [[], ['--selftest']]),
 ('check_solution_docs', [[], ['--selftest']]),
 ('check_submodule_docs', [[], ['--selftest']]),
 ('check_diagram_pngs', [[], ['--selftest']]),
 ('check_archive', [[], ['--selftest']]),
 ('gen_hdl_reference', [['--selftest']]),
 ('check_doc_paths', [[]]),
 ('check_feature_status', [['--self-test']]),
 ('gen_toc', [['--selftest'], ['--verify-anchors'], ['--check']]),
]:
    for args in options:
        name = script + (('-' + args[0][2:]) if args else '')
        commands.append((name, ['python3', 'scripts/' + script + '.py', *args]))
commands.extend([
 ('timesync-check', ['python3', 'docs/diagrams/timesync_chain.gen.py', '--check']),
 ('timesync-selftest', ['python3', 'docs/diagrams/timesync_chain.gen.py', '--selftest']),
 ('module-matrix', ['python3', 'docs/traceability/gen_module_matrix.py', '--check']),
 ('doc-map-check', ['python3', 'docs/DOC_MAP.gen.py', '--check']),
 ('doc-map-selftest', ['python3', 'docs/DOC_MAP.gen.py', '--selftest']),
])
start = next(i for i, (name, _) in enumerate(commands) if name == sys.argv[1]) if len(sys.argv) > 1 else 0
for name, command in commands[start:]:
    if command[0] == 'python3':
        command[0] = sys.executable
    subprocess.run([sys.executable, str(OUT/'run_gate.py'), name, *command], check=True, timeout=14460)

"""Run the ten consumer gates in the foreground: PARENT-GATES.py PARENT_TREE."""
from pathlib import Path
import subprocess
import sys
out = Path(__file__).resolve().parent
root = Path(sys.argv[1]).resolve()
gates = [
    ('parent-cpp-idiom', ['python3', 'scripts/check_cpp_idiom.py']),
    ('parent-py-idiom', ['python3', 'scripts/check_py_idiom.py']),
    ('parent-xvlog', ['python3', 'scripts/xvlog_gate.py', '--check']),
    ('parent-source-lists', ['python3', 'scripts/check_rtl_source_lists.py']),
    ('parent-pp-srcs', ['python3', 'scripts/pp_srcs.py', '--check', '--selftest']),
    ('parent-port-contracts', ['python3', 'scripts/check_port_contracts.py']),
    ('parent-naming', ['python3', 'scripts/measure_naming.py', '--check']),
    ('parent-test-evidence', ['python3', 'scripts/measure_test_evidence.py', '--check']),
    ('parent-docs', ['python3', 'scripts/docs_check.py']),
    ('parent-pp-shadow', ['make', '-C', 'tb/verilator/pp_shadow', '-j8']),
]
for name, command in gates:
    subprocess.run([sys.executable, str(out / 'run-gate.py'), name, str(root), *command],
                   check=True, timeout=14460)

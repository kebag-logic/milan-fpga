import os
import subprocess
from pathlib import Path

root = Path('$LANES/546-crf-talker-step')
out = Path(__file__).resolve().parent
env = dict(os.environ)
env['PATH'] = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin:$VALIDATION_TOOLS/verilator-v5.050/bin:$WORKSPACE_HOME/Xilinx/2026.1/Vivado/bin:' + env['PATH']
gates = [
 ('docs', ['python3', 'scripts/docs_check.py']),
 ('doc-style', ['python3', 'scripts/check_doc_style.py']),
 ('toc', ['python3', 'scripts/gen_toc.py', '--check']),
 ('doc-paths', ['python3', 'scripts/check_doc_paths.py']),
 ('matrix', ['python3', 'docs/traceability/gen_module_matrix.py', '--check']),
 ('xvlog', ['python3', 'scripts/xvlog_gate.py', '--check']),
 ('source-lists', ['python3', 'scripts/check_rtl_source_lists.py']),
 ('cpp-idiom', ['python3', 'scripts/check_cpp_idiom.py']),
 ('py-idiom', ['python3', 'scripts/check_py_idiom.py']),
 ('sv-idiom', ['python3', 'scripts/check_sv_idiom.py']),
 ('lint', ['python3', 'scripts/lint_rtl.py', '--check']),
 ('test-evidence', ['python3', 'scripts/measure_test_evidence.py', '--check']),
 ('behave', ['behave', '--no-capture', '-f', 'plain']),
 ('diff-check', ['git', 'diff', '--check']),
 ('diff-cached-check', ['git', 'diff', '--cached', '--check']),
]
with (out / 'gates.tsv').open('w') as table:
 for name, command in gates:
  with (out / (name + '.log')).open('w') as log:
   result = subprocess.run(command, cwd=root / 'tests' if name == 'behave' else root,
                           env=env, stdout=log, stderr=subprocess.STDOUT, timeout=1800)
  table.write(f'{name}\t{result.returncode}\t{" ".join(command)}\n'); table.flush()
  print(f'{name}: rc={result.returncode}', flush=True)

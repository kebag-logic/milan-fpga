import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

root = Path('/data/milan/reviews/r218-503-r2')
scratch = Path(__file__).resolve().parent
out = scratch / 'gates'
out.mkdir(exist_ok=True)
commands = '''
scripts/docs_check.py
scripts/check_doc_style.py
scripts/check_solution_docs.py
scripts/check_doc_paths.py
scripts/check_archive.py
scripts/gen_toc.py --verify-anchors
scripts/gen_toc.py --check
docs/traceability/gen_module_matrix.py --check
scripts/check_feature_status.py
scripts/check_submodule_docs.py
scripts/check_hygiene.py --check
scripts/check_todo_ownership.py
scripts/check_em_dash.py --base 07294a76e833f1831d9fcbceb8123b8380c4ae76
scripts/check_nvm_record_space.py
scripts/check_nvm_record_space.py --self-test
scripts/check_port_contracts.py
scripts/check_rtl_source_lists.py
scripts/check_soc_sources.py
scripts/check_cpp_idiom.py
scripts/check_py_idiom.py
scripts/check_sv_idiom.py
scripts/check_sh_idiom.py
scripts/ci_scope.py --selftest
scripts/measure_naming.py --check
scripts/measure_fail_fast.py --check
scripts/measure_test_evidence.py --check
'''.strip().splitlines()
results = []
for i, command in enumerate(commands):
    p = subprocess.run([sys.executable, '-B', *shlex.split(command)], cwd=root,
                       env=dict(os.environ, TMPDIR=str(scratch/'tmp'), PYTHONDONTWRITEBYTECODE='1'),
                       text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    (out/f'{i:02d}.log').write_text(p.stdout)
    results.append({'command': 'python3 -B ' + command, 'exit': p.returncode, 'log': f'{i:02d}.log'})
    print(p.returncode, command, p.stdout.strip()[-220:].replace('\n', ' | '), flush=True)
(out/'results.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(any(x['exit'] for x in results))

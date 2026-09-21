import os
from pathlib import Path
import subprocess
import sys

root = Path('/data/milan/reviews/r217-503-r1')
out = Path('/data/milan/reviews/r217-scratch/docs')
out.mkdir(exist_ok=True)
commands = [
    ['scripts/docs_check.py'],
    ['scripts/check_doc_style.py'],
    ['scripts/check_doc_paths.py'],
    ['scripts/check_solution_docs.py'],
    ['scripts/check_feature_status.py'],
    ['scripts/check_submodule_docs.py'],
    ['docs/traceability/gen_module_matrix.py', '--check'],
    ['scripts/gen_toc.py', '--verify-anchors'],
    ['scripts/gen_toc.py', '--check'],
    ['scripts/check_archive.py'],
    ['scripts/check_hygiene.py', '--check'],
    ['scripts/check_em_dash.py', '--base', '07294a76e833f1831d9fcbceb8123b8380c4ae76'],
    ['scripts/check_nvm_record_space.py'],
    ['scripts/check_nvm_record_space.py', '--self-test'],
]
bad = 0
for n, command in enumerate(commands):
    argv = [sys.executable, '-B', *command]
    result = subprocess.run(argv, cwd=root, capture_output=True, text=True,
                            env={**os.environ, 'TMPDIR': str(out), 'PYTHONDONTWRITEBYTECODE': '1'})
    (out / f'{n:02d}-{Path(command[0]).stem}.log').write_text(result.stdout + result.stderr)
    print(result.returncode, ' '.join(argv), flush=True)
    bad += result.returncode != 0
print('SUMMARY', len(commands), 'gates;', bad, 'failures', flush=True)
sys.exit(bool(bad))

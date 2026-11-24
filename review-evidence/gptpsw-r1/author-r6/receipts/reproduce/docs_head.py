import subprocess, sys
commands = [
    ['python3', 'scripts/docs_check.py'],
    ['python3', 'scripts/check_doc_style.py'],
    ['python3', 'scripts/check_doc_paths.py'],
    ['$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3', 'scripts/docs_inventory.py', '--check'],
    ['git', 'diff', '--check', '165476c7', 'HEAD'],
]
failed = 0
for cmd in commands:
    print('COMMAND', ' '.join(cmd), flush=True)
    r = subprocess.run(cmd, check=False)
    print('EXIT', r.returncode, flush=True)
    failed += r.returncode != 0
sys.exit(bool(failed))

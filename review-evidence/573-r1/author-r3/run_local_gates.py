"""Run the assignment's focused gates in the physical candidate directory."""
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
root = Path('$LANES/573-builder-refusals')
markdown_python = '/tmp/573-a355/venv/bin/python'
commands = [
    ('declarations', ['python3', '-B', 'sw/builder/test_declarations.py']),
    ('descriptor-audit', ['python3', 'scripts/audit_pp_descriptors.py', '--output', '/tmp/573-a355/audit-head.json']),
    ('aem-store-selftest', ['python3', 'avdecc/gen_aem_store.py', '--self-test']),
    ('rtl-lint', ['python3', 'scripts/lint_rtl.py', '--check']),
    ('python-idiom', ['python3', 'scripts/check_py_idiom.py']),
    ('naming', ['python3', 'scripts/measure_naming.py', '--check']),
    ('docs-git', ['python3', 'scripts/docs_check.py']),
    ('docs-no-git', ['env', 'GIT_DIR=/dev/null', 'python3', 'scripts/docs_check.py']),
    ('em-dash', [markdown_python, 'scripts/check_em_dash.py', '--base', 'e0920d77']),
    ('doc-style', ['python3', 'scripts/check_doc_style.py']),
    ('toc', [markdown_python, 'scripts/gen_toc.py', '--check']),
    ('anchors', [markdown_python, 'scripts/gen_toc.py', '--verify-anchors']),
    ('doc-paths', ['python3', 'scripts/check_doc_paths.py']),
    ('diff-worktree', ['git', 'diff', '--check']),
    ('diff-branch', ['git', 'diff', '--check', 'e0920d77', 'HEAD']),
]
for label, command in commands:
    subprocess.run([sys.executable, str(out / 'run_gate.py'), label, *command],
                   cwd=root, check=True, timeout=10800)

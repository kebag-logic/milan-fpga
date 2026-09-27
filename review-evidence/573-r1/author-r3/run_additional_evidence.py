"""Run historical controls and current removed-check mutations unchanged."""
import json
import os
from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
scratch = Path('/tmp/573-a355')
head = scratch / 'head'
scripts = scratch / 'reviews/R340-2/scripts'
env = dict(os.environ, **json.loads((scratch / 'head-git-env.json').read_text()))
commands = [
    ('author-mutants', ['python3', '-B', scripts / 'mutants_r2.py', head,
                        out / 'author-mutation-cases.json', out / 'author-mutants.json']),
    ('historical-internal-probes', ['python3', '-B', scripts / 'r340-1/probes.py', head,
                                     out / 'historical-probes.json']),
    ('historical-buffer-wrap', ['python3', '-B', scripts / 'r340-1/buffer_wrap_probe.py', head]),
    ('historical-bypass-probes', ['python3', '-B', scripts / 'r341-1/bypass_probes.py', head]),
    ('historical-format-boundary', ['python3', '-B', out / 'check_format_reproducer.py']),
    ('historical-internal-mutants', ['python3', '-B', scripts / 'r340-1/mutants.py', head,
                                    scripts / 'r340-1/mutant_cases.json', out / 'historical-internal-mutants.json']),
    ('historical-external-mutants', ['python3', '-B', scripts / 'r341-1/run_mutants.py', head,
                                    scripts / 'r341-1/reviewer_mutants.json']),
]
for label, command in commands:
    subprocess.run([sys.executable, str(out / 'run_gate.py'), label, *map(str, command)],
                   cwd=head, env=env, check=True, timeout=10800)
sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=head, env=env, text=True).strip()
tree = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}'], cwd=head, env=env, text=True).strip()
subprocess.run([sys.executable, str(out / 'run_gate.py'), 'archive-integrity', 'bash',
                str(scripts / 'clone_integrity.sh'), str(head), sha, tree],
               cwd=head, env=env, check=True, timeout=900)

#!/usr/bin/env python3
"""Disposable independent controls. No workflow or installer is executed."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import subprocess
import contextlib
import io

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
prefix = os.environ.get('REVIEW_RECEIPT_PREFIX', '')
os.environ['CI_IMAGE_SHFMT'] = str(packet / 'scratch/shfmt')
sys.path.insert(0, str(root / 'scripts'))
from ci_inventory_patterns_selftest import Fixture
import ci_tool_inventory as inventory

cases = [
    ('literal-inline-marker', '''bash -c 'echo "<dynamic>"; brand_new_command' ''', {}),
    ('sourced-directory', 'source fragment.sh; bash bootstrap.sh',
     {'fragment.sh': 'cd sub\n', 'bootstrap.sh': 'echo root\n',
      'sub/bootstrap.sh': 'brand_new_command\n'}),
    ('sourced-variable', 'name=bootstrap.sh; source fragment.sh; bash "$name"',
     {'fragment.sh': 'name=sub/bootstrap.sh\n', 'bootstrap.sh': 'echo root\n',
      'sub/bootstrap.sh': 'brand_new_command\n'}),
    ('background-directory', 'cd sub & bash bootstrap.sh',
     {'bootstrap.sh': 'brand_new_command\n', 'sub/bootstrap.sh': 'echo root\n'}),
    ('branch-functions', 'if true; then f() { brand_new_command; }; else f() { echo okay; }; fi; f', {}),
    ('make-selected-shell', 'make',
     {'Makefile': 'SHELL := ./runner.sh\nall: ; echo okay\n',
      'runner.sh': '#!/bin/sh\nbrand_new_command\n'}),
    ('make-selected-shell-override', 'make SHELL=./runner.sh',
     {'Makefile': 'all: ; echo okay\n', 'runner.sh': '#!/bin/sh\nbrand_new_command\n'}),
    ('make-function-lazy', 'make',
     {'Makefile': 'all: ; $(if yes,echo okay,brand_new_command)\n'}),
    ('literal-python-package', 'python3 bootstrap.py',
     {'bootstrap.py': 'import localpkg\n', 'localpkg/__init__.py':
      'import subprocess\nsubprocess.run(["brand_new_command"])\n'}),
    ('literal-shadow-package', 'python3 bootstrap.py',
     {'bootstrap.py': 'import json\n', 'json/__init__.py':
      'import subprocess\nsubprocess.run(["brand_new_command"])\n'}),
]
results = []
for name, command, files in cases:
    with tempfile.TemporaryDirectory(prefix=name + '-', dir=packet / 'scratch') as directory:
        fixture = Fixture(Path(directory))
        for path, content in files.items():
            fixture.file(path, content)
            if path.endswith('.sh'):
                (fixture.root / path).chmod(0o755)
        fixture.file('bin/brand_new_command', '#!/bin/sh\nprintf "REACHED_UNCLASSIFIED_COMMAND\\n"\n')
        (fixture.root / 'bin/brand_new_command').chmod(0o755)
        (fixture.root / 'bin/python3').symlink_to(sys.executable)
        if name == 'literal-python-package':
            fixture.declare('bootstrap.py')
        fixture.run(command)
        row = dict(name=name, command=command, files=files)
        try:
            derived = inventory.derive(fixture.root)
            row.update(result='ACCEPTED', tools=derived['tools'], inputs=sorted(derived['inputs']),
                       residue=derived['residue'])
        except inventory.Refusal as error:
            row.update(result='REFUSED', diagnostic=str(error).replace(directory, '<fixture>'))
        modes = []
        saved = sys.argv
        for mode in ('--write', '--check'):
            sys.argv = ['ci_tool_inventory.py', '--root', str(fixture.root), mode]
            captured = io.StringIO()
            with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
                rc = inventory.main()
            modes.append(dict(mode=mode, rc=rc, output=captured.getvalue()))
        sys.argv = saved
        row['cli_modes'] = modes
        # Execute only these authored fixtures; the unknown name is a harmless local stub.
        environment = dict(os.environ, PATH=str(fixture.root / 'bin') + ':' + os.environ['PATH'],
                           PYTHONDONTWRITEBYTECODE='1')
        actual = subprocess.run(['bash', '-c', command], cwd=fixture.root, env=environment,
                                text=True, capture_output=True, timeout=20)
        row.update(actual_rc=actual.returncode, actual_stdout=actual.stdout,
                   actual_stderr=actual.stderr.replace(directory, '<fixture>'),
                   real_execution_reached_unclassified='REACHED_UNCLASSIFIED_COMMAND' in actual.stdout)
        results.append(row)
        print(json.dumps(row, sort_keys=True), flush=True)
(packet / (prefix + 'traversal-probes.json')).write_text(json.dumps(results, indent=2) + '\n')

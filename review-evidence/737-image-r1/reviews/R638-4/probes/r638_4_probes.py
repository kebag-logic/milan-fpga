#!/usr/bin/env python3
"""R638-4 reviewer probes for the CI inventory deriver (no source edits).

Usage: CI_IMAGE_SHFMT=<pinned shfmt> python3 r638_4_probes.py <clone>/scripts <outdir>

Each probe builds a disposable fixture tree with the head's command table and
source lock, runs the head's deriver in --write then --check mode, and records
whether generation REFUSED or ACCEPTED.  A hidden file containing the
unclassified command `brand_new_command` stands for any unreviewed installer:
when the real tool (bash, make, GitHub runner) would execute it, a deriver that
follows real semantics must refuse.  ACCEPTED on such a probe means the hidden
command was never classified (silent acceptance or mis-resolution).
"""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.path.insert(0, sys.argv[1])
import ci_tool_inventory as inventory  # noqa: E402
import yaml  # noqa: E402

OUT = Path(sys.argv[2])
RESULTS = []


class Fixture:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.workflow = root / '.github/workflows/fixture.yml'
        self.workflow.parent.mkdir(parents=True)
        (root / 'ci/image').mkdir(parents=True)
        for name in ('command-table.json', 'sources.lock.json'):
            shutil.copyfile(inventory.ROOT / 'ci/image' / name, root / 'ci/image' / name)
        self.table = json.loads((root / 'ci/image/command-table.json').read_text())

    def file(self, name: str, text: str) -> None:
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def doc(self, doc: dict) -> None:
        self.workflow.write_text(yaml.safe_dump(doc))

    def run(self, command: str, **step) -> None:
        self.doc({'jobs': {'gate': {'steps': [{'run': command, **step}]}}})

    def declare(self, name: str) -> None:
        self.table['scripts'][name] = {
            'class': 'reviewed non-installing', 'reason': 'Probe boundary.',
            'sha256': hashlib.sha256((self.root / name).read_bytes()).hexdigest()}
        (self.root / 'ci/image/command-table.json').write_text(inventory.serialized(self.table))

    def outcome(self) -> tuple[str, str, object]:
        saved = sys.argv
        texts = []
        rcs = []
        try:
            for mode in ('--write', '--check'):
                sys.argv = ['ci_tool_inventory.py', '--root', str(self.root), mode]
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                    try:
                        rc = inventory.main()
                    except Exception as error:  # crash is not a named refusal
                        rc = f'CRASH {type(error).__name__}: {error}'
                rcs.append(rc)
                texts.append(buf.getvalue().strip())
        finally:
            sys.argv = saved
        inv = self.root / inventory.OUTPUT
        tools = None
        if inv.is_file():
            data = json.loads(inv.read_text())
            tools = [(t['tool'], t['kind'], t['pin']) for t in data['tools']]
            tools.append(('RESIDUE', data['residue']))
        status = 'ACCEPTED' if rcs == [0, 0] else ('REFUSED' if rcs == [2, 2] else f'MIXED {rcs}')
        return status, ' || '.join(texts), tools


def probe(pid: str, description: str, expected: str, setup) -> None:
    with tempfile.TemporaryDirectory(prefix='r638-4-probe-', dir=OUT / 'tmp') as d:
        fixture = Fixture(Path(d))
        setup(fixture)
        status, text, tools = fixture.outcome()
    defect = status != expected
    RESULTS.append({'id': pid, 'description': description, 'expected': expected,
                    'observed': status, 'defect': defect, 'output': text, 'tools': tools})
    print(f"{'DEFECT' if defect else 'ok    '} {pid}: expected {expected}, observed {status}: {description}")
    print(f"         {text[:300]}")


HIDDEN = 'brand_new_command\n'


def common(f: Fixture) -> None:
    f.file('bootstrap.sh', 'echo root\n')
    f.file('sub/bootstrap.sh', HIDDEN)
    f.file('hidden.sh', HIDDEN)


def p(fn):
    def setup(f):
        common(f)
        fn(f)
    return setup


# Baseline: the hidden command is refused when followed directly.
probe('B0', 'baseline: hidden script followed directly', 'REFUSED', p(lambda f: f.run('bash hidden.sh')))
probe('B1', 'baseline: benign script accepted', 'ACCEPTED', p(lambda f: f.run('bash bootstrap.sh')))

# Workflow-level semantics.
probe('W1', 'step shell: custom shell program runs hidden.sh with the step file', 'REFUSED',
      p(lambda f: f.run('echo okay', shell='bash hidden.sh {0}')))
probe('W2', 'workflow defaults.run.shell custom shell runs hidden.sh', 'REFUSED',
      p(lambda f: f.doc({'defaults': {'run': {'shell': 'bash hidden.sh {0}'}},
                         'jobs': {'gate': {'steps': [{'run': 'echo okay'}]}}})))
probe('W3', 'step env BASH_ENV=hidden.sh: bash sources it before the step body', 'REFUSED',
      p(lambda f: f.run('echo okay', env={'BASH_ENV': 'hidden.sh'})))
probe('W4', 'GITHUB_PATH write puts ./tools first; later step "git rev-parse HEAD" runs tools/git', 'REFUSED',
      p(lambda f: (f.file('tools/git', HIDDEN),
                   f.doc({'jobs': {'gate': {'steps': [
                       {'run': 'echo "$PWD/tools" >> "$GITHUB_PATH"'},
                       {'run': 'git rev-parse HEAD'}]}}}))))
probe('W5', 'PATH=tools:$PATH then "git rev-parse HEAD" runs tools/git', 'REFUSED',
      p(lambda f: (f.file('tools/git', HIDDEN), f.run('export PATH="tools:$PATH"; git rev-parse HEAD'))))

# Wrapper semantics.
probe('X1', 'xargs appends stdin words to "python3 -m pip install"', 'REFUSED',
      p(lambda f: f.run('echo evilpkg | xargs python3 -m pip install')))
probe('X2', 'xargs appends stdin words to "apt-get install -y"', 'REFUSED',
      p(lambda f: f.run('echo evilpkg | sudo xargs apt-get install -y')))
probe('X3', 'xargs appends stdin path to "bash"', 'REFUSED',
      p(lambda f: f.run('echo hidden.sh | xargs bash')))

# Shell variable semantics.
probe('S1', 'shift inside a function moves $1 to the second argument', 'REFUSED',
      p(lambda f: f.run('f() { shift; bash "$1"; }; f bootstrap.sh hidden.sh')))
probe('S2', 'printf -v assigns the variable used as the script path', 'REFUSED',
      p(lambda f: f.run("name=bootstrap.sh; printf -v name '%s' hidden.sh; bash \"$name\"")))
probe('S3', 'read -r f assigns the variable used as the script path', 'REFUSED',
      p(lambda f: f.run('f=bootstrap.sh; read -r f <<< hidden.sh; bash "$f"')))
probe('S4', 'source: assignment in the sourced file reaches the parent', 'REFUSED',
      p(lambda f: (f.file('fragment.sh', 'name=hidden.sh\n'),
                   f.run('name=bootstrap.sh; source fragment.sh; bash "$name"'))))
probe('S5', 'source: cd in the sourced file changes the parent directory', 'REFUSED',
      p(lambda f: (f.file('fragment.sh', 'cd sub\n'), f.run('source fragment.sh; bash bootstrap.sh'))))
probe('S6', 'literal marker text "<dynamic>" in bash -c in an undeclared workflow', 'REFUSED',
      p(lambda f: f.run("bash -c 'brand_new_command <dynamic>'")))
probe('S7', 'bare script name uses PATH, not the working directory', 'REFUSED',
      p(lambda f: f.run('PATH="sub:$PATH" bootstrap.sh')))

# Make semantics.
probe('M1', 'Make SHELL := ./hidden.sh: make runs every recipe through hidden.sh', 'REFUSED',
      p(lambda f: (f.file('Makefile', 'SHELL := ./hidden.sh\nall:\n\techo okay\n'), f.run('make'))))
probe('M2', 'Make ?= keeps a workflow env value (TOOL=brand_new_command)', 'REFUSED',
      p(lambda f: (f.file('Makefile', 'TOOL ?= echo\nall:\n\t$(TOOL) okay\n'),
                   f.run('make', env={'TOOL': 'brand_new_command'}))))
probe('M2b', 'Make ?= keeps a shell-exported value (TOOL=brand_new_command)', 'REFUSED',
      p(lambda f: (f.file('Makefile', 'TOOL ?= echo\nall:\n\t$(TOOL) okay\n'),
                   f.run('export TOOL=brand_new_command; make'))))
probe('M3', 'Make $(@D) is the target directory, not empty', 'REFUSED',
      p(lambda f: (f.file('Makefile', 'all: sub/x\nsub/x:\n\tbash ./$(@D)/bootstrap.sh\n'), f.run('make'))))
probe('M4', 'command-line override propagates to a recursive $(MAKE)', 'REFUSED',
      p(lambda f: (f.file('Makefile', 'all:\n\t$(MAKE) -C sub\n'),
                   f.file('sub/Makefile', 'TOOL = echo\nall:\n\t$(TOOL) okay\n'),
                   f.run('make TOOL=brand_new_command'))))

# Python semantics.
probe('Y1', 'ctypes libc system() executes a command', 'REFUSED',
      p(lambda f: (f.file('bootstrap.py', 'import ctypes\nctypes.CDLL(None).system(b"brand_new_command")\n'),
                   f.run('python3 bootstrap.py'))))
probe('Y2', 'getattr(os, "system") executes a command in an undeclared script', 'REFUSED',
      p(lambda f: (f.file('bootstrap.py', 'import os\ngetattr(os, "system")("brand_new_command")\n'),
                   f.run('python3 bootstrap.py'))))


def y3(f):
    f.file('firmware/__init__.py', '')
    f.file('firmware/hidden.py', 'import subprocess\nsubprocess.run(["brand_new_command"])\n')
    f.file('bootstrap.py', 'from firmware import hidden\n')
    f.run('python3 bootstrap.py')


probe('Y3', 'local package submodule (allow-listed package name) is never followed', 'REFUSED', p(y3))

exec(open(Path(__file__).with_name('prior_forms.py')).read())
exec(open(Path(__file__).with_name('literal_dollar.py')).read())

(OUT / 'probe-results.json').write_text(json.dumps(RESULTS, indent=2) + '\n')
print('defects:', [r['id'] for r in RESULTS if r['defect']])

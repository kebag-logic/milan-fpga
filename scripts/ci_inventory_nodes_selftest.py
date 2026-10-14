#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Check typed data operands and the structural inventory boundary."""

import hashlib
import json
import tempfile
from pathlib import Path

import yaml

from ci_command_table import Audit, Runtime, normalize, nodes, shell_tree
from ci_syntax import semantic_node
from ci_inventory_patterns_selftest import Fixture


def data_controls() -> None:
    """Data lists admit source changes but never executable options."""
    pattern = ['--lint-only', {'data_paths': '.sv'}, 'top.sv']
    assert Audit.matches(['--lint-only', 'first.sv', 'top.sv'], pattern)
    assert Audit.matches(['--lint-only', 'first.sv', 'second.sv', 'top.sv'], pattern)
    for operand in ('--exe=payload.sv', 'payload.cpp', Runtime('source.sv')):
        assert not Audit.matches(['--lint-only', operand, 'top.sv'], pattern)
    assert not Audit.matches(['--lint-only', 'top.sv'], pattern)
    assert Audit.matches(['generated/header.svh'], [{'data_path': '.svh'}])
    assert not Audit.matches(['-eprogram.svh'], [{'data_path': '.svh'}])
    print('PASS: typed data operands and variable source populations')


def shell_controls(fixture: Fixture) -> None:
    """Reproduce every reported shell scope and literal-program escape."""
    fixture.file('bootstrap.sh', 'echo okay\n')
    fixture.file('hidden.sh', 'brand_new_command\n')
    fixture.file('sub/bootstrap.sh', 'brand_new_command\n')
    fixture.file('fragment.sh', 'cd sub\n')
    fixture.run('source fragment.sh; bash bootstrap.sh')
    fixture.check('sourced directory', 'brand_new_command')
    fixture.file('fragment.sh', 'name=hidden.sh\n')
    fixture.run('name=bootstrap.sh; source fragment.sh; bash "$name"')
    fixture.check('sourced variable', 'brand_new_command')
    for command in (
        'cd sub & bash bootstrap.sh',
        'if true; then f() { brand_new_command; }; else f() { echo okay; }; fi; f',
        "name=bootstrap.sh; printf -v name '%s' hidden.sh; bash \"$name\"",
        'name=bootstrap.sh; read -r name <<< hidden.sh; bash "$name"',
        'echo "$PWD/tools" >> "$GITHUB_PATH"; git rev-parse HEAD',
        'echo "PATH=tools" >> "$GITHUB_ENV"',
        'export PATH="tools:$PATH"; git rev-parse HEAD',
        'PATH="sub:$PATH" bootstrap.sh', 'IFS=x; echo okay',
        'BASH_ENV=hidden.sh bash bootstrap.sh', 'ENV=hidden.sh sh bootstrap.sh',
        'echo evilpkg | xargs python3 -m pip install',
        'echo evilpkg | sudo xargs apt-get install -y',
        "bash -c 'brand_new_command <dynamic>'",
        "bash -c 'echo \"<dynamic>\"; brand_new_command'",
        'coproc echo okay', 'select value in one two; do echo okay; done',
        'echo ${!name}', 'echo $((value ** 2))', 'printf -v value %s hidden.sh',
        'env PATH=tools bash bootstrap.sh', 'exec brand_new_command',
    ):
        fixture.run(command)
        fixture.check(command, 'REFUSED:')
    for owner in ('step', 'job', 'workflow'):
        doc = {'jobs': {'gate': {'steps': [{'run': 'echo okay'}]}}}
        if owner == 'step':
            doc['jobs']['gate']['steps'][0]['shell'] = 'bash hidden.sh {0}'
        else:
            target = doc if owner == 'workflow' else doc['jobs']['gate']
            target['defaults'] = {'run': {'shell': 'bash hidden.sh {0}'}}
        fixture.workflow.write_text(yaml.safe_dump(doc))
        fixture.check(owner + ' shell selection', 'workflow shell')
    fixture.workflow.write_text(yaml.safe_dump({'jobs': {'gate': {'steps': [
        {'run': 'echo okay', 'env': {'BASH_ENV': 'hidden.sh'}}]}}}))
    fixture.check('workflow startup file', 'workflow environment')


def alternative_controls(fixture: Fixture) -> None:
    """A censused conditional preserves both definitions, including the first one."""
    command = 'if true; then f() { brand_new_command; }; else f() { echo okay; }; fi; f'
    fixture.run(command)
    census_path = fixture.root / 'ci/image/syntax-census.json'
    census = json.loads(census_path.read_text())
    audit = Audit(fixture.root, {})
    for node in nodes(shell_tree(command, audit.parser)):
        if node.get('Type') == 'FuncDecl':
            raw = json.dumps(semantic_node(node), sort_keys=True, separators=(',', ':')).encode()
            census['shell_exact_uses'][hashlib.sha256(raw).hexdigest()] = {
                'sources': ['.github/workflows/fixture.yml'], 'kinds': ['conditional-function']}
    census_path.write_text(json.dumps(census))
    fixture.check('censused first function alternative', 'brand_new_command')


def make_controls(fixture: Fixture) -> None:
    """Make environment and override propagation cannot select a benign decoy."""
    fixture.run('make')
    for variable in ('SHELL', '.SHELLFLAGS', 'MAKEFLAGS', 'MAKE'):
        fixture.file('Makefile', variable + ' := ./hidden.sh\nall: ; echo okay\n')
        fixture.check('Make assignment ' + variable, 'uncensused Make')
    fixture.file('Makefile', 'all: ; echo okay\n')
    for variable in ('SHELL', 'MAKEFLAGS', 'MAKE'):
        fixture.run('make ' + variable + '=./hidden.sh')
        fixture.check('Make override ' + variable, 'uncensused Make')
    fixture.file('Makefile', 'TOOL ?= echo\nall: ; $(TOOL) okay\n')
    fixture.workflow.write_text(yaml.safe_dump({'jobs': {'gate': {'steps': [
        {'run': 'make', 'env': {'TOOL': 'brand_new_command'}}]}}}))
    fixture.check('Make environment default', 'brand_new_command')
    fixture.run('export TOOL=brand_new_command; make')
    fixture.check('Make exported default', 'brand_new_command')
    fixture.run('TOOL=brand_new_command; make')
    fixture.check('unexported shell variable stays private')
    fixture.file('Makefile', 'all: sub/x\nsub/x: ; bash ./$(@D)/bootstrap.sh\n')
    fixture.run('make')
    fixture.check('automatic directory form', 'unsupported Make automatic')
    fixture.file('Makefile', 'all: ; $(MAKE) -C sub\n')
    fixture.file('sub/Makefile', 'TOOL = echo\nall: ; $(TOOL) okay\n')
    fixture.run('make TOOL=brand_new_command')
    fixture.check('recursive Make override', 'brand_new_command')
    fixture.file('sub$x/Makefile', 'all: ; brand_new_command\n')
    fixture.run("make -C 'sub$x'")
    fixture.check('literal dollar directory', 'brand_new_command')


def python_controls(fixture: Fixture) -> None:
    """Initializers, shadow packages and foreign-function execution are capabilities."""
    fixture.run('python3 bootstrap.py')
    for source in ('import ctypes\nctypes.CDLL(None).system(b"brand_new_command")\n',
                   'import cffi\ncffi.FFI().dlopen(None)\n'):
        fixture.file('bootstrap.py', source)
        fixture.check('foreign-function capability', 'undeclared executing')
    fixture.file('json/__init__.py', 'import subprocess\nsubprocess.run(["brand_new_command"])\n')
    fixture.file('bootstrap.py', 'import json\n')
    fixture.check('local shadow initializer', 'undeclared executing')
    fixture.file('firmware/__init__.py', '')
    fixture.file('firmware/hidden.py', 'import subprocess\nsubprocess.run(["brand_new_command"])\n')
    fixture.file('bootstrap.py', 'from firmware import hidden\n')
    fixture.check('local package member', 'undeclared executing')
    fixture.file('localpkg/__init__.py', 'import subprocess\nsubprocess.run(["brand_new_command"])\n')
    fixture.file('bootstrap.py', 'import localpkg\n')
    fixture.declare('bootstrap.py')
    fixture.check('declared importer does not cover initializer', 'undeclared executing')
    fixture.file('bootstrap.py', 'async def run(): pass\n')
    fixture.declare('bootstrap.py')
    fixture.check('new Python node kind', 'uncensused Python node')


def main() -> int:
    """Run the structural controls without executing candidate commands."""
    data_controls()
    for root in (Path('/src'), Path('/include')):
        value = str(root) + '/third_party/library' + str(root) + '/unit.c'
        assert normalize(value, root) == '${CHECKOUT}/third_party/library' + str(root) + '/unit.c'
    for controls in (shell_controls, alternative_controls, make_controls, python_controls):
        with tempfile.TemporaryDirectory(prefix='ci-nodes-') as directory:
            controls(Fixture(Path(directory)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

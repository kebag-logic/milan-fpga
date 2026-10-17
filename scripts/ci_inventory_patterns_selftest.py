#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Exercise positive command forms and real file, target and directory selection."""

import contextlib
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys
import tempfile

import ci_tool_inventory as inventory
import ci_command_table

# Walker semantics are tested without the census gate; ci_differential_selftest.py holds the gate.
ci_command_table.GATE = False
from ci_command_table import Audit, shell_tree
from ci_syntax import semantic_node


class Fixture:
    """Run both public CLI modes against a disposable workflow tree."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.workflow = root / '.github/workflows/fixture.yml'
        self.workflow.parent.mkdir(parents=True)
        (root / 'ci/image').mkdir(parents=True)
        for name in ('command-table.json', 'sources.lock.json', 'syntax-census.json', 'make-builtins.json',
                     'differential-receipt.json'):
            shutil.copyfile(inventory.ROOT / 'ci/image' / name, root / 'ci/image' / name)
        self.table = json.loads((root / 'ci/image/command-table.json').read_text())
        # The existing source-scope controls use this exact reviewed fixture call.
        audit = Audit(root, {})
        call = shell_tree('source ./fragment.sh', audit.parser)['Stmts'][0]['Cmd']
        raw = json.dumps(semantic_node(call), sort_keys=True, separators=(',', ':')).encode()
        audit.census['shell_exact_uses'][hashlib.sha256(raw).hexdigest()] = {
            'sources': ['.github/workflows/fixture.yml'], 'kinds': ['source']}
        self.file('ci/image/syntax-census.json', inventory.serialized(audit.census))

    def file(self, name: str, text: str) -> None:
        """Write one fixture input without executing it."""
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def run(self, command: str, directory: str | None = None) -> None:
        """Install a literal run step, optionally in a selected directory."""
        import yaml
        step = {'run': command}
        if directory is not None:
            step['working-directory'] = directory
        self.workflow.write_text(yaml.safe_dump({'jobs': {'gate': {'steps': [step]}}}))

    def environment(self, names: list[str]) -> None:
        """Review workflow `env:` names solely to test what the walker does with their values."""
        census = json.loads((self.root / 'ci/image/syntax-census.json').read_text())
        census['workflow_environment'].update({name: 'Fixture environment control.' for name in names})
        self.file('ci/image/syntax-census.json', inventory.serialized(census))

    def declare(self, name: str) -> None:
        """Pin a reviewed fixture solely to test the classification boundary."""
        self.table['scripts'][name] = {
            'class': 'reviewed non-installing', 'reason': 'Fixture execution boundary control.',
            'sha256': hashlib.sha256((self.root / name).read_bytes()).hexdigest(),
        }
        self.save_table()

    def save_table(self) -> None:
        """Keep the declaration and its exact source bytes together."""
        self.file('ci/image/command-table.json', inventory.serialized(self.table))

    def check(self, name: str, refusal: str | None = None) -> None:
        """Require generation and comparison to agree, including named refusals."""
        saved = sys.argv
        try:
            for mode in ('--write', '--check'):
                sys.argv = ['ci_tool_inventory.py', '--root', str(self.root), mode]
                output = io.StringIO()
                with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                    rc = inventory.main()
                if refusal is None:
                    assert rc == 0, (name, mode, output.getvalue())
                else:
                    assert rc == 2 and refusal in output.getvalue(), (name, mode, output.getvalue())
        finally:
            sys.argv = saved
        print(f'PASS: {name}: generation and comparison')


def command_controls(fixture: Fixture) -> None:
    """All round-three literal execution surfaces must refuse by name."""
    for command in (
        'gh extension install example/fixture', 'gh release download v1 -R example/tool',
        'git submodule add https://example.invalid/tool',
        'git config submodule.x.url https://example.invalid/tool',
        'git clone --no-hardlinks git@host:org/tool.git',
        'git archive --remote=https://example.invalid/tool HEAD', '/unclassified/git rev-parse HEAD',
        'node -e "require(\'https\')"', 'java -jar download.jar', 'cmake --install build',
        'sbt "install fixture"', 'eval "echo okay"', 'bash -c "npx fixture"',
        "echo 'npx fixture' | bash", "bash <<< 'npx fixture'",
        "python3 <<'END'\nimport urllib.request\nEND",
        "python3 -I - <<'END'\nimport urllib.request\nEND",
        'echo ${MISSING:-$(npx fixture)}', 'for ((i=$(npx fixture);i<1;i++)); do true; done',
        'selected=$RUNTIME_FUNCTION; $selected', 'find . -ok npx fixture {} \\;',
        'sed -n \'1e npx fixture #$\' "$PWD/sw/litex/sweep.sh"',
        'awk \'BEGIN { system("npx fixture") }; { print $1 }\'',
        '"\\e\\c\\h\\o" okay',
    ):
        fixture.run(command)
        fixture.check(command.splitlines()[0], 'REFUSED:')
    fixture.run('git rev-parse HEAD')
    fixture.check('recognized Git argv')
    fixture.run(f"sed -n '1e npx fixture #$' '{fixture.root}/sw/litex/sweep.sh'")
    fixture.check('literal dollar text cannot match runtime argument', 'unclassified command')
    fixture.run('git rev-parse HEAD --unlisted-option')
    fixture.check('extra Git argument', 'unclassified git')
    fixture.run('sudo --unlisted-option echo okay')
    fixture.check('unknown wrapper option', 'unclassified sudo option')
    fixture.run('env MODE=check timeout 2 echo okay')
    fixture.check('wrapper child classification')
    fixture.workflow.write_text('jobs:\n  gate:\n    uses: example/tools/.github/workflows/install.yml@main\n')
    fixture.check('reusable job', 'reusable workflow')
    # A fixed program's data slot takes one literal file, never an option, a runtime word or a second file.
    program = '$1 == "MemTotal:" && $3 == "kB" { print $2 }'
    fixture.run(f"awk '{program}' data-file")
    fixture.check('a fixed program reads a literal data file')
    for operand, label in (('-f other.awk', 'an option'), ('"$RUNTIME_FILE"', 'a runtime word'),
                           ('data-file other-file', 'a second file')):
        fixture.run(f"awk '{program}' {operand}")
        fixture.check(f'a fixed program with {label} in its data slot', 'unclassified command')


def python_controls(fixture: Fixture) -> None:
    """Detection precedes decoding for aliases, keywords and network imports."""
    fixture.run('python3 bootstrap.py')
    for source in (
        'import os\nos.popen("npx fixture")\n',
        'import os\nos.execvp("npx", ["npx", "fixture"])\n',
        'import os\nos.spawnlp(0, "npx", "npx", "fixture")\n',
        'import os\nos.posix_spawn("npx", ["npx"], {})\n',
        'import asyncio\nasyncio.create_subprocess_exec("npx", "fixture")\n',
        'import pty\npty.spawn(["npx", "fixture"])\n',
        'import pip._internal\npip._internal.main(["install", "fixture"])\n',
        'import urllib3\n', 'import asyncio, ssl\nasyncio.open_connection("host", 443, ssl=True)\n',
        'import subprocess\nsubprocess.run(**{"args": ["npx", "fixture"]})\n',
        'import subprocess\nrunner = subprocess.run\nrunner(["npx", "fixture"])\n',
        'import importlib\nimportlib.import_module("urllib.request")\n',
    ):
        fixture.file('bootstrap.py', source)
        fixture.check(source.splitlines()[0], 'REFUSED:')
    for source in (
        'import subprocess\nsubprocess.run(**{"args": ["npx", "fixture"]})\n',
        'import subprocess\nrunner = subprocess.run\nrunner(["npx", "fixture"])\n',
    ):
        fixture.file('bootstrap.py', source)
        fixture.declare('bootstrap.py')
        fixture.check('declared literal unpacking or alias', "unclassified command 'npx'")
    fixture.file('bootstrap.py', 'import subprocess\nsubprocess.run(args=["echo", "okay"])\n')
    fixture.declare('bootstrap.py')
    fixture.check('declared keyword command')
    fixture.file('bootstrap.py', 'import subprocess\nsubprocess.run(args=["echo", "changed"])\n')
    fixture.check('changed declaration', 'changed declared script')


def shell_controls(fixture: Fixture) -> None:
    """Keep directory scope, substitutions, functions and inline text explicit."""
    fixture.file('bootstrap.sh', 'echo root\n')
    fixture.file('sub/bootstrap.sh', 'brand_new_command\n')
    fixture.run('bash bootstrap.sh', 'sub')
    fixture.check('step working directory', 'brand_new_command')
    fixture.run('(cd sub); bash bootstrap.sh')
    fixture.check('subshell does not leak directory')
    fixture.run('(cd sub && bash bootstrap.sh)')
    fixture.check('subshell child directory', 'brand_new_command')
    fixture.run('cd sub; bash bootstrap.sh')
    fixture.check('top-level directory persists', 'brand_new_command')
    fixture.run('(cd "$UNKNOWN" && echo okay)')
    fixture.check('computed subshell directory', 'unresolved shell cd')
    fixture.run('{ cd sub; }; bash bootstrap.sh')
    fixture.check('block preserves parent scope', 'brand_new_command')
    fixture.run('cd sub || cd elsewhere; bash bootstrap.sh')
    fixture.check('a cd into an existing directory is never certain: its fallback is followed',
                  'ambiguous shell directory')
    fixture.run('cd "$UNKNOWN" || cd sub; bash bootstrap.sh')
    fixture.check('a fallback after an uncertain cd leaves the directory ambiguous', 'unresolved shell cd')
    fixture.run('cd sub || exit 2; bash bootstrap.sh')
    fixture.check('terminating fallback preserves successful directory', 'brand_new_command')
    fixture.run('if true; then cd sub; fi; bash bootstrap.sh')
    fixture.check('a test that always succeeds takes its branch', 'brand_new_command')
    fixture.run('if [ -e "$UNKNOWN" ]; then cd sub; fi; bash bootstrap.sh')
    fixture.check('ambiguous conditional directory', 'ambiguous shell directory')
    fixture.run('if true; then cd sub; else cd sub; fi; bash bootstrap.sh')
    fixture.check('common conditional directory persists', 'brand_new_command')
    fixture.run('if cd sub; then echo okay; fi; bash bootstrap.sh')
    fixture.check('a cd test is never certain: both paths continue', 'ambiguous shell directory')
    fixture.file('function.sh', 'f() { echo okay; }; f\n')
    fixture.run('bash function.sh')
    fixture.check('same-file function')
    fixture.run('f() { cd sub; }; (f() { echo okay; }); f; bash bootstrap.sh')
    fixture.check('subshell function definition does not leak', 'brand_new_command')
    fixture.run('f() { cd sub; }; { f() { echo okay; }; } | true; f; bash bootstrap.sh')
    fixture.check('pipeline function definition does not leak', 'brand_new_command')
    fixture.run('name=bootstrap.sh; f() { name=sub/bootstrap.sh; }; f; bash "$name"')
    fixture.check('function global assignment persists', 'brand_new_command')
    fixture.run('name=sub/bootstrap.sh; f() { local name=bootstrap.sh; }; f; bash "$name"')
    fixture.check('function local assignment is restored', 'brand_new_command')
    fixture.run('bash function.sh; f')
    fixture.check('foreign function', "unclassified command 'f'")
    fixture.run('source ./missing.sh')
    fixture.check('missing sourced file', 'unresolved script')
    fixture.file('fragment.sh', 'echo okay\n')
    fixture.run('source ./fragment.sh')
    fixture.check('followed source')
    fixture.run('source fragment.sh')
    fixture.check('a slash-free source operand searches PATH', 'uncensused shell source path search')
    fixture.file('fragment.sh', 'g() { echo okay; }\n')
    fixture.declare('fragment.sh')
    fixture.run('source ./fragment.sh; g')
    fixture.check('pinned imported function')
    fixture.file('fragment.sh', 'g() { echo changed; }\n')
    fixture.check('changed imported function', 'changed declared script')
    fixture.run('echo okay && true || echo alternate; echo $(echo nested) > out')
    fixture.check('sequences and substitutions')
    fixture.run('for value in one two; do echo "$value"; done')
    fixture.check('literal loop values')
    fixture.run('for value in one two; do brand_new_command; done')
    fixture.check('loop body refusal', 'brand_new_command')
    program = 'print("fixture")'
    key = 'python3:' + hashlib.sha256(program.encode()).hexdigest()
    fixture.table['inline'][key] = {'class': 'non-installing', 'reason': 'Print a fixture constant.'}
    fixture.save_table()
    fixture.run("python3 -c '" + program + "'")
    fixture.check('pinned inline text')
    fixture.run("python3 -c '" + program + " '")
    fixture.check('changed inline byte', 'unclassified inline')
    for default in ('workflow', 'job'):
        import yaml
        doc = {'jobs': {'gate': {'steps': [{'run': 'bash bootstrap.sh'}]}}}
        owner = doc if default == 'workflow' else doc['jobs']['gate']
        owner['defaults'] = {'run': {'working-directory': 'sub'}}
        fixture.workflow.write_text(yaml.safe_dump(doc))
        fixture.check(default + ' directory default', 'brand_new_command')


def make_controls(fixture: Fixture) -> None:
    """Select the same file, target, stem and literal variable values as make."""
    fixture.file('Makefile', 'all:\n\techo okay\n')
    fixture.file('install.mk', 'all:\n\tbrand_new_command\n')
    fixture.file('sub/Makefile', 'all:\n\tbrand_new_command\n')
    for command in ('make --file=install.mk', 'make -finstall.mk', 'make -f install.mk',
                    'make --directory=sub', 'make -Csub', 'make -C sub'):
        fixture.run(command)
        fixture.check(command, 'brand_new_command')
    fixture.file('bootstrap.sh', 'brand_new_command\n')
    fixture.file('sub/bootstrap.sh', 'echo okay\n')
    fixture.file('sub/selected.mk', 'all:\n\tbash bootstrap.sh\n')
    fixture.run('make -f sub/selected.mk')
    fixture.check('selected Makefile preserves invocation directory', 'brand_new_command')
    fixture.run('make -C sub -f selected.mk')
    fixture.check('directory option changes recipe directory')
    fixture.run('make', 'sub')
    fixture.check('Make step directory', 'brand_new_command')
    fixture.run('make')
    fixture.file('Makefile', 'benign:\n\techo okay\n.DEFAULT_GOAL := install\ninstall:\n\tbrand_new_command\n')
    fixture.check('literal default selects actual goal', 'brand_new_command')
    fixture.file('Makefile', 'benign:\n\techo okay\n.DEFAULT_GOAL := $(GOAL)\n')
    fixture.check('computed default', 'computed .DEFAULT_GOAL')
    fixture.file('Makefile', 'all: generated\n%:\n\tbrand_new_command\n')
    fixture.check('pattern prerequisite', 'brand_new_command')
    fixture.file('Makefile', '.PHONY: all\nall: generated\ngenerated:\n%:\n\tbrand_new_command\n')
    fixture.check('implicit recipe behind explicit prerequisite rule', 'brand_new_command')
    fixture.file('Makefile', 'all: obj_test\nobj_%:\n\techo $*\n')
    fixture.check('unique stem')
    fixture.file('Makefile', 'all: obj_test\nobj_%:\n\techo $*\n%_test:\n\techo $*\n')
    fixture.check('ambiguous stem', 'ambiguous Make pattern')
    fixture.file('Makefile', 'all: ; echo okay\nVALUE := $(shell echo literal)\n')
    fixture.check('literal Make shell')
    fixture.file('Makefile', 'all: ; echo okay\nVALUE := $(shell $$RUNTIME_TOOL)\n')
    fixture.check('computed Make shell', 'computed Make shell')
    fixture.file('Makefile', 'TOOL = brand_new_command\nall:\n\t$(TOOL)\n')
    fixture.check('literal command variable', 'brand_new_command')
    fixture.file('Makefile', 'VALUE := $(info anything)\nall: ; echo okay\n')
    fixture.check('unsupported Make function', 'unsupported Make function')
    fixture.file('Makefile', 'VALUE := $(eval anything)\nall: ; echo okay\n')
    fixture.check('Make eval in an assignment', 'unmodelled Make eval outside a parse-time line')
    fixture.file('Makefile', 'include install.mk\nall: ; echo okay\n')
    fixture.check('unsupported include', 'unsupported Make construct')
    fixture.file('Makefile', 'define SAY\necho $(1)\nendef\nWORDS = one two\nWORDS += three\n'
                 'all: $(foreach v,$(WORDS),obj_$(v))\nobj_%:\n\t$(call SAY,$*)\n')
    fixture.check('macro list and automatic stem')
    fixture.file('Makefile', 'all:\n\t$(call MISSING,value)\n')
    fixture.check('undefined macro', 'undefined or unmodelled Make macro')
    fixture.file('Makefile', 'all: ; echo $!\n')
    fixture.check('unsupported automatic variable', 'unsupported Make automatic')
    fixture.file('Makefile', '.PHONY: all\nall: ; echo okay\n')
    fixture.check('first ordinary target after special declaration')
    fixture.file('Makefile', 'all: | prepare\n\techo okay\nprepare: ; echo ready\n')
    fixture.check('order-only prerequisite')
    for automatic in ('$<', '$^'):
        fixture.file('Makefile', 'all: | bootstrap.sh\n\t' + automatic + '\n')
        fixture.check('order-only excluded from ' + automatic)
    fixture.file('Makefile', 'all: ; echo $?\n')
    fixture.check('uncensused automatic variable', 'unsupported Make automatic')
    fixture.file('Makefile', 'all: TOOL = echo\nall: ; $(TOOL) okay\n')
    fixture.check('target-specific literal variable')
    fixture.file('Makefile', 'all: TOOL = $(RUNTIME)\nall: ; echo okay\n')
    fixture.check('computed target-specific variable', 'computed target-specific')
    fixture.file('Makefile', 'VALUE := fixed\nifneq ($(VALUE),fixed)\n$(error wrong)\nendif\nall: ; echo okay\n')
    fixture.check('conditional error guard')
    fixture.file('Makefile', 'ifeq (one,one)\nTOOL = echo\nendif\nall: ; $(TOOL) okay\n')
    fixture.check('unsupported conditional assignment', 'unsupported conditional Make body')
    for expression in (
        '$(subst original,brand_new_command,original)',
        '$(patsubst obj_%,brand_new_%,obj_command)',
        '$(filter brand_new_command,echo brand_new_command)',
        '$(filter-out echo,echo brand_new_command)',
        '$(addprefix brand_new_,command)',
        '$(firstword brand_new_command echo)',
        '$(strip   brand_new_command   )',
        '$(if yes,brand_new_command,echo)',
        '$(and yes,brand_new_command)',
    ):
        fixture.file('Makefile', 'TOOL = ' + expression + '\nall: ; $(TOOL)\n')
        fixture.check('resolved ' + expression, 'brand_new_command')
    fixture.file('Makefile', 'all: ; echo okay\n')
    fixture.run('make missing')
    fixture.check('unknown target', 'unresolved Make target')
    fixture.run('make --unlisted-option')
    fixture.check('unknown Make option', 'unsupported make option')


def main() -> int:
    """Keep each control family isolated from preceding source declarations."""
    for controls in (command_controls, python_controls, shell_controls, make_controls):
        with tempfile.TemporaryDirectory(prefix='ci-patterns-') as directory:
            controls(Fixture(Path(directory)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

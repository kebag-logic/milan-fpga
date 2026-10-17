#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Hold the walker to exact make and bash semantics: refuse by name what it does not model.

Each planted fixture is resolved the way GNU Make 4.3 and bash 5.2 resolve it in
the image, or refused by name before generation. Both CLI modes are exercised.
"""

from pathlib import Path
import tempfile

import yaml

from ci_inventory_patterns_selftest import Fixture
from ci_shell_walk import posix_dirname


#: The image's coreutils 9.4 `dirname -- VALUE` for each operand.
DIRNAME = {'': '.', '/': '/', '//': '/', '///': '/', 'a': '.', 'a/': '.', 'a/b': 'a', 'a//b//': 'a',
           '/a': '/', '/a/': '/', '//a': '/', '//a/b': '//a', './x': '.', '../x/y': '../x',
           'a b/c': 'a b', 'x/..': 'x', '.': '.'}


def step(fixture: Fixture, command: str, env: dict | None = None) -> None:
    """Install one run step, optionally with step environment values."""
    body = {'run': command, **({'env': env} if env else {})}
    fixture.environment(sorted(env or {}))
    fixture.workflow.write_text(yaml.safe_dump({'jobs': {'gate': {'steps': [body]}}}))


def canonical_controls(fixture: Fixture) -> None:
    """Only canonical lines are read; make's own reading decides every other spelling."""
    fixture.file('bootstrap.sh', 'echo okay\n')
    fixture.file('sub/bootstrap.sh', 'brand_new_command\n')
    fixture.run('make')
    for text, refusal in (
            ('CMD = echo ok\n CMD = sudo apt-get install -y cowsay # note:\nall: ; $(CMD)\n',
             'non-canonical indented Make line'),
            ('X != sudo apt-get install -y cowsay >&2; echo a:\nall: ; echo okay\n',
             "uncensused Make assignment operator '!='"),
            ('X ::= echo\nall: ; echo okay\n', 'uncensused Make double-colon form'),
            ('all:: ; echo okay\n', 'uncensused Make double-colon form'),
            ('X = a\\\\#b\nall: ; echo $(X)\n', 'unmodelled escaped Make number sign'),
            ('X = a\\\\\nall: ; echo okay\n', 'unmodelled escaped Make line end'),
            ('VPATH = sub\nall: ; echo okay\n', "uncensused Make assignment 'VPATH'"),
            ('all: ; echo $(MAKEFILE_LIST)\n', "unmodelled Make variable 'MAKEFILE_LIST'"),
            ('all:\n\t# $(shell brand_new_command)\n\techo okay\n', "unclassified command 'brand_new_command'"),
            ('DIR = sub   # trailing blanks stay in the value\nall: ; bash $(DIR)/bootstrap.sh\n',
             "unsupported script language 'sub'"),
            ('define STEPS\ncd sub\nbash bootstrap.sh\nendef\nall: ; $(STEPS)\n', None),
            ('X = echo \\\n    okay\nall: ; $(X)\n', None)):
        fixture.file('Makefile', text)
        fixture.check('canonical Make: ' + text.splitlines()[0], refusal)
    fixture.file('bootstrap.sh', 'brand_new_command\n')
    fixture.file('sub/bootstrap.sh', 'echo okay\n')
    fixture.file('Makefile', 'define STEPS\ncd sub\nbash bootstrap.sh\nendef\nall: ; $(STEPS)\n')
    fixture.check('each expanded recipe line runs in its own shell', "unclassified command 'brand_new_command'")


def rule_controls(fixture: Fixture) -> None:
    """Built-in, implicit and target-specific rules resolve as make resolves them, or refuse."""
    fixture.file('probe_builtin.c', 'int main(void) { return 0; }\n')
    fixture.file('gen.y', '%%\n')
    fixture.file('benign.sh', 'echo okay\n')
    fixture.file('probe_evil.sh', 'brand_new_command\n')
    fixture.file('sub/car.sh', 'brand_new_command\n')
    for command, text, refusal in (
            ('make probe_builtin', 'CC = sudo apt-get install -y cowsay ; cc\nprobe_builtin: probe_builtin.c\n',
             "built-in implicit rule '%: %.c' may apply to 'probe_builtin'"),
            ('make', 'all: gen.c ; echo okay\n', "built-in implicit rule '%.c: %.y' may apply to 'gen.c'"),
            ('make probe_builtin', 'MAKEFLAGS += -r\nprobe_builtin: probe_builtin.c\n', None),
            ('make', 'MAKEFLAGS += -R\nall: ; echo okay\n', "uncensused Make assignment 'MAKEFLAGS'"),
            ('make probe.out', 'probe.out: benign.sh\n%.out: %_evil.sh\n\tbash $<\n',
             "unclassified command 'brand_new_command'"),
            ('make', 'all: sub/eat.out\nsub/eat.out:\ne%t.out: c%r.sh\n\tbash $<\n',
             "unclassified command 'brand_new_command'"),
            ('make', 'all: x.a\n%.a %.b: %.c ; echo okay\n', 'unsupported multiple-target pattern rule'),
            ('make', 'all: x\nx y &: ; echo okay\n', 'unsupported Make grouped or archive target'),
            ('make', '%.o: %.c\nall: ; echo okay\n', 'unsupported recipe-less Make pattern rule'),
            ('make', '%.o: X = echo\nall: ; echo okay\n', 'unsupported pattern-specific Make variable'),
            ('make', 'all: X ?= echo\nall: ; $(X) okay\n', 'unsupported Make target-specific form'),
            ('make SCRIPT=probe_evil.sh', 'all: SCRIPT=benign.sh\nall: ; bash $(SCRIPT)\n',
             "target-specific 'SCRIPT' for 'all' is overridden by a command-line value"),
            ('make', 'CXX ?= brand_new_command\nall: ; $(CXX) --version\n', None)):
        fixture.run(command)
        fixture.file('Makefile', text)
        fixture.check(f'Make rule: {command}: {text.splitlines()[0]}', refusal)
    step(fixture, 'make', {'SCRIPT': 'probe_evil.sh'})
    fixture.file('Makefile', 'all: SCRIPT=benign.sh\nall: ; bash $(SCRIPT)\n')
    fixture.check('target-specific value beats the environment, as in make')


def traversal_controls(fixture: Fixture) -> None:
    """Every distinct incoming environment is walked; an identical one is not walked again."""
    fixture.file('Makefile', 'TOOL ?= echo\nall: ; $(TOOL) okay\n')
    fixture.run('TOOL=echo make; TOOL=brand_new_command make')
    fixture.check('repeated Make under a new environment', "unclassified command 'brand_new_command'")
    fixture.file('bootstrap.sh', '"$TOOL" okay\n')
    fixture.run('TOOL=echo bash bootstrap.sh; TOOL=brand_new_command bash bootstrap.sh')
    fixture.check('repeated script under a new environment', "unclassified command 'brand_new_command'")
    fixture.run('TOOL=echo bash bootstrap.sh; TOOL=echo bash bootstrap.sh')
    fixture.check('repeated script under the same environment')
    fixture.file('bootstrap.sh', 'bash "$name"\n')
    fixture.file('hidden.sh', 'brand_new_command\n')
    fixture.run('name=hidden.sh; bash bootstrap.sh')
    fixture.check('an unexported variable stays in its own shell', 'unclassified runtime command name')
    fixture.file('child.sh', '"$TOOL" okay\n')
    fixture.file('Makefile', 'TOOL = echo\nall: ; bash child.sh\n')
    step(fixture, 'make', {'TOOL': 'brand_new_command'})
    fixture.check('a recipe inherits the makefile value of an environment name')
    fixture.run('make TOOL=brand_new_command')
    fixture.check('a recipe inherits command-line values', "unclassified command 'brand_new_command'")


def substitution_controls(fixture: Fixture) -> None:
    """Command substitution yields a value only in exact, unredirected shapes."""
    for value, expected in DIRNAME.items():
        assert posix_dirname(value) == expected, (value, posix_dirname(value), expected)
    print('PASS: dirname model equals the image coreutils for every recorded operand')
    fixture.file('zz_probe_cwd.py', 'import subprocess\nsubprocess.run(["brand_new_command"])\n')
    fixture.file('scripts/zz_probe_cwd.py', 'VALUE = 1\n')
    fixture.file('sub/bootstrap.sh', 'brand_new_command\n')
    fixture.file('bootstrap.sh', 'echo okay\n')
    for name, operand in (('dirname', 'sub/bootstrap.sh'), ('realpath', 'sub/bootstrap.sh'),
                          ('dirname', 'scripts/run.sh')):
        fixture.table['commands'][name]['patterns'].append([operand])
    fixture.save_table()
    for command, refusal in (
            ('cd "$(cd scripts && pwd > /dev/null)"; python3 zz_probe_cwd.py', 'unresolved shell cd'),
            ('cd "$(cd scripts; pwd)"; python3 zz_probe_cwd.py', 'unresolved shell cd'),
            ('cd "$(echo x; pwd)"; python3 zz_probe_cwd.py', 'unresolved shell cd'),
            ('X="$(cd sub && pwd)"; cd "$X"; bash bootstrap.sh', "unclassified command 'brand_new_command'"),
            ('cd "$(cd sub && pwd)"; bash bootstrap.sh', 'unresolved shell cd'),
            ('bash "$(dirname sub/bootstrap.sh)/bootstrap.sh"', "unclassified command 'brand_new_command'"),
            ('bash "$(realpath sub/bootstrap.sh)"', 'unclassified runtime command name')):
        fixture.run(command)
        fixture.check('substitution: ' + command, refusal)
    # realpath reads links as they are when it runs: only a script's own path, before it runs a command.
    fixture.file('own/run.sh', 'bash "$(dirname "$(realpath "$0")")/x.sh"\n')
    fixture.file('own/late.sh', 'echo started\nbash "$(dirname "$(realpath "$0")")/x.sh"\n')
    fixture.file('own/x.sh', 'brand_new_command\n')
    for name, operand in (('realpath', 'own/run.sh'), ('dirname', '${CHECKOUT}/own/run.sh'),
                          ('realpath', 'own/late.sh')):
        fixture.table['commands'][name]['patterns'].append([operand])
    fixture.save_table()
    fixture.run('bash own/run.sh')
    fixture.check("realpath of the running script's own path", "unclassified command 'brand_new_command'")
    fixture.run('bash own/late.sh')
    fixture.check('realpath after the script ran a command is runtime', 'unclassified command "dirname \'${RUNTIME}\'"')
    fixture.file('scripts/run.sh', 'set -e\ncd sub\nbash "$(dirname "$0")/x.sh"\n')
    fixture.file('scripts/x.sh', 'echo okay\n')
    fixture.file('sub/scripts/x.sh', 'brand_new_command\n')
    fixture.run('bash scripts/run.sh')
    fixture.check('$0 is the exact invocation word', "unclassified command 'brand_new_command'")
    fixture.file('scripts/run.sh', 'bash "${BASH_SOURCE[1]}"\n')
    fixture.check('only BASH_SOURCE[0] is modelled', 'unclassified runtime command name')


def main() -> int:
    """Run each family in its own disposable tree."""
    for controls in (canonical_controls, rule_controls, traversal_controls, substitution_controls):
        with tempfile.TemporaryDirectory(prefix='ci-exact-') as directory:
            controls(Fixture(Path(directory)))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

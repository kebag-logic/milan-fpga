#!/usr/bin/env python3
# SPDX-License-Identifier: CERN-OHL-W-2.0
"""Differential fixtures: one focus fixture per census shape, and every reviewer probe.

Each fixture is data for ci_differential.py. `zz_probe` is the observed sentinel;
its directory and arguments are what the walker and the real tool must agree on.
`expect` is `identical`, `residue` or `refused`; `shapes` names the census shapes
the fixture is the focus fixture for; `probe` names the review finding it replays.
`variants` are extra environments for the real runs only, so that every branch
the walker resolves is taken by some real run.
"""

SH = 'zz_probe'


def shell(name: str, shapes: list[str], run: str, expect: str = 'identical', **more: object) -> dict:
    """A workflow step run under bash -e, as the hosted runner runs it."""
    return {'id': name, 'shapes': shapes, 'expect': expect, 'run': run, **more}


def make(name: str, shapes: list[str], makefile: str, run: str = 'make\n', **more: object) -> dict:
    """A Makefile run by GNU Make 4.3; its recipes run under /bin/sh."""
    files = {'Makefile': makefile, **more.pop('files', {})}
    return {'id': name, 'shapes': shapes, 'expect': more.pop('expect', 'identical'), 'run': run,
            'files': files, **more}


def python(name: str, shapes: list[str], files: dict, run: str = 'python3 main.py\n', **more: object) -> dict:
    """Python programs run by CPython 3.12.3."""
    return {'id': name, 'shapes': shapes, 'expect': more.pop('expect', 'identical'), 'run': run,
            'files': files, **more}


EXECUTE = "import subprocess\nsubprocess.run(['zz_probe', '{}'])\n"
OK = 'zz_probe ok\n'
EVIL = 'zz_probe hidden\n'
#: An undeclared program that changes no command but removes a directory in one variant.
CLEAN = "import os\nimport shutil\nif os.environ.get('RM'):\n    shutil.rmtree('sub')\n"
#: An undeclared program that changes no command but re-points a link in one variant.
RELINK = "import os\nif os.environ.get('RELINK'):\n    os.remove('sub/link')\n    os.symlink('../b', 'sub/link')\n"
#: A directory that exists in one variant only, so a `cd` into it can fail.
MADE = 'if [ "$V" = 1 ]; then mkdir -p obj_fw; fi\n'
EITHER = [{'V': '1'}, {'V': '0'}]

FIXTURES = [
    # Bash words and simple commands.
    shell('bash-command', ['bash:word.literal', 'bash:call.command', 'cmd:table'], 'zz_probe alpha beta\n'),
    shell('bash-quotes', ['bash:word.single-quoted', 'bash:word.double-quoted'],
          'zz_probe \'a b\' "c d" \'e\'"f" "$HOME"x\n'),
    shell('bash-assignment', ['bash:assignment', 'bash:word.parameter'],
          'X=one\nX=two\nY=\nzz_probe "$X" "$Y"\n'),
    shell('bash-special-parameters', ['bash:shift', 'bash:word.special-parameter'],
          'f() { shift; zz_probe "$1" "$#"; }\nf a b\n'),
    shell('bash-parameter-operators', ['bash:word.parameter-operator'],
          'X=val\nzz_probe "${X:-default}" "${#X}" "${X%%l}"\n'),
    shell('bash-command-substitution', ['bash:word.command-substitution'], 'zz_probe "$(echo hi)"\n'),
    shell('bash-process-substitution', ['bash:word.process-substitution'], 'zz_probe <(echo x)\n'),
    shell('bash-arithmetic', ['bash:for.arithmetic', 'bash:word.arithmetic'],
          'for ((i = 0; i < 2; i++)); do zz_probe "$i"; done\nzz_probe $((1 + 1))\n'),
    shell('bash-split-runtime', ['bash:word.split-runtime'], 'zz_probe $(echo c d) end\n'),
    shell('bash-split-literal', [], 'X="a b"\nzz_probe $X "$X"\n'),
    shell('bash-pathname-expansion', ['bash:word.pathname-expansion'], 'zz_probe g/*.txt\n',
          files={'g/a.txt': '', 'g/b.txt': ''}),
    shell('bash-tilde', ['bash:word.tilde'], 'zz_probe ~/x\n'),
    shell('bash-arrays', ['bash:assignment.array', 'bash:assignment.index'],
          'a=(x y)\na[2]=z\nzz_probe "${a[0]}" "${a[@]}"\n'),
    shell('bash-argv0', ['bash:word.argv0', 'cmd:shell.script.bash'], 'bash sub/run.sh\n',
          files={'sub/run.sh': 'zz_probe "$0"\n'}),
    shell('bash-bash-source', ['bash:word.bash-source'], '. sub/lib.sh\n',
          files={'sub/lib.sh': 'zz_probe "${BASH_SOURCE[0]}"\n'}, exact_uses={'source': ['. sub/lib.sh']}),
    shell('bash-dirname', ['bash:word.dirname'], 'zz_probe "$(dirname sub/x.sh)"\n',
          patterns={'dirname': [['sub/x.sh']]}),
    # realpath reads the links on its path when it runs: in a step its output is a runtime value.
    shell('bash-realpath', [], 'zz_probe "$(realpath sub/x.sh)"\n',
          files={'sub/x.sh': ''}, patterns={'realpath': [['sub/x.sh']]}),
    # A script's own path, before the script runs a command, holds the links the shell read it through.
    shell('bash-realpath-script-path', ['bash:word.realpath.script-path'], 'bash sub/run.sh\n',
          files={'sub/run.sh': 'set -u\nHERE="$(dirname "$(realpath "$0")")"\nzz_probe "$HERE"\n'},
          patterns={'realpath': [['sub/run.sh']], 'dirname': [['${CHECKOUT}/sub/run.sh']]}),
    # After a program has run, a link on the path may point elsewhere: the output is a runtime value.
    shell('bash-realpath-after-a-program', [], 'bash run.sh\n', expect='refused', executes=True,
          probe='R638-8-N4',
          files={'run.sh': 'python3 relink.py\nX="$(realpath sub/link)"\nbash "$X/run.sh"\n',
                 'relink.py': RELINK, 'a/run.sh': OK, 'b/run.sh': EVIL},
          links={'sub/link': '../a'}, patterns={'realpath': [['sub/link']]}, variants=[{}, {'RELINK': '1'}]),
    shell('bash-cd-pwd', ['bash:word.cd-pwd'], 'X="$(cd sub && pwd)"\nzz_probe "$X"\n', files={'sub/.keep': ''}),
    # A script's own directory exists while the shell reads the script, until a command runs.
    shell('bash-cd-pwd-script-directory', ['bash:word.cd-pwd.script-directory'], 'bash sub/run.sh\n',
          files={'sub/run.sh': 'set -u\nROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"\nzz_probe "$ROOT"\n'},
          patterns={'dirname': [['sub/run.sh']]}),
    # After a program has run, the directory may be gone: the output is a runtime value.
    shell('bash-cd-pwd-after-a-program', [], 'bash run.sh\n', expect='refused', executes=True,
          files={'run.sh': 'python3 clean.py\nX="$(cd sub && pwd)"\nbash "$X/run2.sh"\n',
                 'clean.py': CLEAN, 'sub/run2.sh': OK}, variants=[{}, {'RM': '1'}]),
    # Bash state: every reachable path, joined.
    shell('bash-and', ['bash:and'],
          'X=start\n[ -e "$FLAG" ] && X=flagged\nzz_probe "$X"\n(cd sub && zz_probe in-sub)\nzz_probe after\n',
          files={'sub/.keep': ''}, variants=[{'FLAG': 'missing'}, {'FLAG': 'sub'}]),
    shell('bash-or', ['bash:or'], 'X=a\n[ -e missing ] || X=b\nzz_probe "$X"\ncd sub || exit 1\nzz_probe in-sub\n',
          files={'sub/.keep': ''}),
    shell('bash-pipe', ['bash:pipe'], 'X=a\necho x | X=b\nzz_probe "$X"\necho x | zz_probe piped\n'),
    shell('bash-block', ['bash:block'], '{ cd sub; X=b; }\nzz_probe "$X"\n', files={'sub/.keep': ''}),
    shell('bash-subshell', ['bash:subshell'], 'X=a\n(cd sub; X=b; zz_probe "$X")\nzz_probe "$X"\n',
          files={'sub/.keep': ''}),
    shell('bash-if', ['bash:if'],
          'if [ "$V" = 1 ]; then X=one; zz_probe then; else X=two; zz_probe else; fi\nzz_probe "$X"\n',
          variants=[{'V': '1'}, {'V': '2'}]),
    # A cd is never certain, whatever the checkout holds: both paths continue, and differ.
    shell('bash-if-certain', [],
          'if cd sub; then X=then; else X=else; fi\nzz_probe "$X"\n'
          'if true; then zz_probe true; else zz_probe never; fi\n', files={'sub/.keep': ''}, expect='refused',
          refusal='ambiguous shell directory'),
    shell('bash-if-outside', [], 'if cd /tmp; then X=moved; fi\nzz_probe "$X"\n', expect='refused'),
    # A failed cd changes nothing: under errexit it ends the shell; in a test it continues where it started.
    shell('bash-cd-test-fails', [], 'cd missing && true\nzz_probe here\n', expect='refused'),
    shell('bash-cd-test-last', [], MADE + 'cd obj_fw && zz_probe in-obj-fw\n',
          variants=EITHER),
    shell('bash-or-certain', [], 'cd sub || zz_probe never\nzz_probe after\n', files={'sub/.keep': ''},
          expect='refused', refusal='ambiguous shell directory'),
    shell('bash-true-certain', [], 'if true; then zz_probe true; else zz_probe never; fi\n: || zz_probe never\n'),
    shell('bash-negated-cd', [], 'if ! cd missing; then zz_probe failed; fi\n'),
    shell('bash-errexit-cd', [], MADE + 'cd obj_fw\nzz_probe in-obj-fw\n',
          variants=EITHER),
    shell('bash-set-errexit', ['bash:set.errexit'], 'bash run.sh\n',
          files={'run.sh': 'set -euo pipefail\n' + MADE + 'cd obj_fw\nzz_probe in-obj-fw\n'},
          variants=EITHER),
    shell('bash-no-errexit-cd', [], 'bash run.sh\n',
          files={'run.sh': MADE + 'cd obj_fw\nzz_probe after\n'},
          variants=EITHER, expect='refused'),
    shell('bash-set-plus-e', [], 'set +e\ncd missing\nzz_probe after\n', expect='refused'),
    shell('bash-function-in-test', [], 'f() {\n  cd missing\n  zz_probe in-f\n}\nf || true\n',
          expect='refused'),
    shell('bash-case', ['bash:case'],
          'case "$V" in\n  a) X=1; zz_probe a ;;\n  *) zz_probe other ;;\nesac\nzz_probe "$X"\n',
          variants=[{'V': 'a'}, {'V': 'b'}]),
    shell('bash-negation', ['bash:negation'],
          'if ! [ -e "$F" ]; then zz_probe absent; else zz_probe present; fi\n',
          variants=[{'F': 'missing'}, {'F': '.'}]),
    shell('bash-for-words', ['bash:for.words'], 'for x in one two; do zz_probe "$x"; done\nzz_probe "$x"\n'),
    shell('bash-while', ['bash:while'],
          'n=0\nwhile [ "$n" != 2 ]; do zz_probe "$n"; n=$((n + 1)); done\nzz_probe "$n"\n'),
    shell('bash-loop-escapes', ['bash:escape.break', 'bash:escape.continue'],
          'X=none\nfor x in a b c; do\n  [ "$x" = b ] && continue\n  [ "$x" = c ] && break\n  X=$x\ndone\n'
          'zz_probe "$X"\n'),
    shell('bash-return', ['bash:escape.return', 'bash:function.call', 'bash:function.definition'],
          'f() {\n  X=a\n  [ -e "$F" ] && return\n  X=b\n}\nf\nzz_probe "$X"\n',
          variants=[{'F': 'missing'}, {'F': '.'}]),
    shell('bash-exit', ['bash:escape.exit'], 'zz_probe before\nexit 0\nzz_probe after\n'),
    shell('bash-function-partly-defined', ['bash:function.call-partly-defined'], 'bash run.sh\n',
          expect='residue', files={'run.sh': 'if [ "$V" = 1 ]; then\n  f() { zz_probe defined; }\nfi\nf\n'},
          declare=['run.sh'], observe=['f'], variants=[{'V': '1'}, {'V': '0'}],
          exact_uses={'conditional-function': ['f() { zz_probe defined; }']}, exact_source='run.sh'),
    shell('bash-declarations', ['bash:declaration.local', 'bash:declaration.declare',
                                'bash:declaration.declare-global', 'bash:declaration.export'],
          'f() {\n  local L=in\n  declare D=in\n  declare -gA G=()\n  X=global\n}\nL=out\nD=out\nf\n'
          'zz_probe "$L" "$D" "$X"\nexport E=exported\nbash child.sh\n', files={'child.sh': 'zz_probe "$E"\n'}),
    shell('bash-prefix-assignment', ['bash:call.prefix-assignment'],
          'X=outer\nX=inner bash child.sh\nX=temp zz_probe "$X"\nzz_probe "$X"\n',
          files={'child.sh': 'zz_probe "$X"\n'}),
    shell('bash-read', ['bash:read'], "printf 'v\\n' > in.txt\nread -r X < in.txt\nzz_probe \"$X\"\n",
          exact_uses={'read': ['read -r X']}),
    shell('bash-unset', ['bash:unset'], 'X=a\nunset X\nzz_probe "$X"\n'),
    shell('bash-source', ['bash:source'], '. ./lib.sh\nzz_probe "$V"\n', files={'lib.sh': 'V=from-lib\n'},
          exact_uses={'source': ['. ./lib.sh']}),
    shell('bash-trap', ['bash:trap'], 'X=early\ntrap \'zz_probe "$X"\' EXIT\nX=late\n'),
    shell('bash-trap-runtime', ['bash:trap.runtime'], 'bash run.sh\n', expect='residue',
          files={'run.sh': 't=$(mktemp -d)\ntrap "zz_probe \'$t\'" EXIT\n'}, declare=['run.sh']),
    shell('bash-cd', ['bash:cd'], 'cd sub\nzz_probe here\ncd ..\nzz_probe back\n', files={'sub/.keep': ''}),
    shell('bash-cd-runtime', ['bash:cd.runtime'], 'bash run.sh\n',
          files={'run.sh': 'cd "$(mktemp -d)"\nzz_probe there\n'}, declare=['run.sh']),
    shell('bash-heredoc', ['bash:heredoc', 'bash:redirect'],
          'true <<EOF\nline $HOME\nEOF\nzz_probe done > /dev/null 2>&1\n'),
    shell('bash-heredoc-python', ['bash:heredoc.python', 'cmd:python.inline'],
          "python3 - <<'EOF'\n" + EXECUTE.format('inline') + 'EOF\n', expect='residue',
          inline={'python3': [EXECUTE.format('inline')]}),
    # Command classification and wrappers.
    shell('cmd-data', ['cmd:data'], 'test -e sub && zz_probe exists\ntrue\necho note\n', files={'sub/.keep': ''}),
    shell('cmd-direct-bash', ['cmd:direct.bash'], './run.sh\n',
          files={'run.sh': '#!/bin/bash\nzz_probe "$0"\n'}, executable=['run.sh']),
    shell('cmd-find', ['cmd:find'], "find sub -name '*.sh' -exec zz_probe {} \\;\n", files={'sub/a.sh': ''},
          patterns={'find': [['sub', '-name', '*.sh', '-exec', 'zz_probe', '{}', ';']]}),
    shell('cmd-git', ['cmd:git'], 'git rev-parse HEAD\n', observe=['git']),
    shell('cmd-installer', ['cmd:installer'], 'apt-get install -y cowsay\n', observe=['apt-get']),
    shell('cmd-python-installer', ['cmd:python.installer'], 'python3 -m pip install --quiet cowsay==6.1\n',
          observe=['python3']),
    shell('cmd-python-isolated-script', ['cmd:python.isolated-script'], 'python3 -I sub/prog.py\n',
          files={'sub/json.py': EXECUTE.format('shadow'),
                 'sub/prog.py': 'import json\n' + EXECUTE.format('isolated')},
          declare=['sub/prog.py', 'sub/json.py']),
    shell('cmd-runtime-script', ['cmd:runtime-script'], 'bash run.sh\n', expect='residue',
          files={'run.sh': "s=$(printf '%s' child.sh)\nbash \"$s\"\n", 'child.sh': 'zz_probe child\n'},
          declare=['run.sh']),
    shell('cmd-shell-inline-sh', ['cmd:shell.inline.sh'], "sh -c 'zz_probe inline'\n",
          inline={'sh': ['zz_probe inline']}),
    shell('cmd-shell-runtime-inline', ['cmd:shell.runtime-inline'], 'bash run.sh\n', expect='residue',
          files={'run.sh': "c=$(printf '%s' 'zz_probe rt')\nbash -c \"$c\"\n"}, declare=['run.sh']),
    shell('cmd-shell-syntax-check', ['cmd:shell.syntax-check'], 'bash -n run.sh\n',
          files={'run.sh': 'zz_probe never\n'}),
    shell('cmd-wrapper-command', ['cmd:wrapper.command'],
          'zz_probe() { :; }\ncommand zz_probe via-command\ncommand -v zz_probe > /dev/null\nzz_probe via-function\n'),
    shell('cmd-wrapper-env', ['cmd:wrapper.env'], 'export Y=kept\nenv -u Y X=1 bash child.sh\n',
          files={'child.sh': 'zz_probe "$X" "$Y"\n'}),
    shell('cmd-wrapper-exec', ['cmd:wrapper.exec'], 'zz_probe first\nexec zz_probe last\nzz_probe never\n'),
    shell('cmd-wrapper-flock', ['cmd:wrapper.flock'], 'flock lock zz_probe locked\n'),
    shell('cmd-wrapper-sudo', ['cmd:wrapper.sudo'], 'sudo ./bin/zz_probe as-root\n', stub_directory='bin'),
    shell('cmd-wrapper-time', ['cmd:wrapper.time'], "/usr/bin/time -f '%e' zz_probe timed\n"),
    shell('cmd-wrapper-timeout', ['cmd:wrapper.timeout'], 'timeout 10 zz_probe bounded\n'),
    shell('cmd-wrapper-xargs', ['cmd:wrapper.xargs'],
          "printf 'a\\nb\\n' | xargs -n 1 zz_probe item\nprintf 'c\\n' | xargs -I{} zz_probe at-{}\n",
          exact_uses={'xargs': ['xargs -n 1 zz_probe item', 'xargs -I{} zz_probe at-{}']},
          patterns={'xargs': [['-n', '1', 'zz_probe', 'item'], ['-I{}', 'zz_probe', 'at-{}']]}),
    # GNU Make.
    make('make-basic', ['make:invocation', 'make:rule', 'make:recipe-line', 'make:recipe', 'make:phony',
                        'sh:word.literal', 'sh:call.command'], '.PHONY: all\nall:\n\tzz_probe alpha beta\n'),
    make('make-goal', ['make:goal.command-line', 'make:option.goal'],
         'first: ; zz_probe first\nsecond: ; zz_probe second\n', run='make second\n'),
    make('make-inline-recipe', ['make:inline-recipe'], 'all: ; zz_probe inline\n'),
    make('make-directory', ['make:option.directory'], 'all: ; zz_probe top\n', run='make -C sub\n',
         files={'sub/Makefile': 'all: ; zz_probe in-sub\n'}),
    make('make-file', ['make:option.file'], 'all: ; zz_probe default\n', run='make -f other.mk\n',
         files={'other.mk': 'all: ; zz_probe other\n'}),
    make('make-jobs', ['make:option.jobs'], 'all: a b\na: ; zz_probe a\nb: ; zz_probe b\n', run='make -j2\n'),
    make('make-silent', ['make:option.s', 'make:option.no-print-directory'], 'all: ; zz_probe quiet\n',
         run='make -s --no-print-directory\n'),
    make('make-command-line', ['make:option.variable', 'make:variable.command-line'],
         'X = file\nall: ; zz_probe $(X)\n', run='make X=cmd\n'),
    make('make-recursive-flags', ['make:invocation.inherited-flags', 'make:variable.MAKE'],
         'all:\n\t$(MAKE) -C sub\n\tMAKEFLAGS= $(MAKE) -C sub\n', run='make X=top\n',
         files={'sub/Makefile': 'X = sub\nall: ; zz_probe $(X)\n'},
         exact_uses={'assignment': ['MAKEFLAGS= make -C sub']}, exact_source='Makefile'),
    make('make-assignments', ['make:assignment.=', 'make:assignment.:=', 'make:assignment.?=',
                              'make:assignment.+=', 'make:variable.reference'],
         'A = $(B)\nB = late\nC := $(B)\nB = later\nD ?= dflt\nE = e1\nE += e2\nall: ; zz_probe $(A) $(C) $(D) $(E)\n'),
    make('make-curdir', ['make:variable.CURDIR'], 'all: ; zz_probe $(CURDIR)\n'),
    make('make-shell-status', ['make:variable.shell-status', 'make:function.shell'],
         'X := $(shell zz_probe parse-time)\nall: ; zz_probe $(.SHELLSTATUS)\n'),
    make('make-pattern-rule', ['make:pattern-rule', 'make:prerequisite-file', 'make:automatic.@',
                               'make:automatic.<', 'make:automatic.*'],
         'all: out.x\n%.x: %.src\n\tzz_probe $@ $< $*\n', files={'out.src': ''}),
    make('make-call', ['make:function.call', 'make:call.argument'], 'M = $(0)-$(1)\nall: ; zz_probe $(call M,arg)\n'),
    make('make-conditional', ['make:conditional', 'make:function.error'],
         'ifeq ($(V),bad)\n$(error bad value)\nendif\nall: ; zz_probe ok\n'),
    make('make-default-goal', ['make:default-goal'],
         '.DEFAULT_GOAL := second\nfirst: ; zz_probe first\nsecond: ; zz_probe second\n'),
    make('make-define', ['make:define'], 'define STEP\nzz_probe defined\nendef\nall: ; $(STEP)\n'),
    make('make-functions', ['make:function.abspath', 'make:function.addprefix', 'make:function.and',
                            'make:function.filter', 'make:function.filter-out', 'make:function.firstword',
                            'make:function.foreach', 'make:function.if', 'make:function.patsubst',
                            'make:function.strip', 'make:function.subst', 'make:function.wildcard'],
         'all: ; zz_probe $(abspath sub/../x) $(addprefix p-,a b) $(and x,y) $(filter %.c,a.c b.h) '
         '$(filter-out %.c,a.c b.h) $(firstword f g) $(foreach v,1 2,v$(v)) $(if x,yes,no) '
         '$(patsubst %.c,%.o,a.c) $(strip  s  t ) $(subst a,b,aaa) $(wildcard w/*.txt)\n',
         files={'w/1.txt': '', 'w/2.txt': ''}),
    make('make-order-only', ['make:order-only'], 'all: | dir\n\tzz_probe x $^\ndir: ; zz_probe made-dir\n'),
    make('make-target-specific', ['make:target-specific'], 'all: X = ts\nall: ; zz_probe $(X)\n'),
    # POSIX shell recipes, run by /bin/sh (dash).
    make('sh-quotes', ['sh:word.single-quoted', 'sh:word.double-quoted'], 'all: ; zz_probe \'a b\' "c d"\n'),
    make('sh-assignment', ['sh:assignment', 'sh:word.parameter'], 'all: ; X=a; zz_probe "$$X"\n'),
    make('sh-and', ['sh:and'], 'all: ; X=s; [ -e "$$F" ] && X=f; zz_probe "$$X"\n',
         variants=[{'F': 'missing'}, {'F': 'Makefile'}]),
    make('sh-or', ['sh:or'], 'all: ; X=a; [ -e missing ] || X=b; zz_probe "$$X"\n'),
    make('sh-pipe', ['sh:pipe'], 'all: ; echo x | zz_probe piped\n'),
    make('sh-block', ['sh:block'], 'all: ; { cd sub && zz_probe in-sub; }\n', files={'sub/.keep': ''}),
    make('sh-if', ['sh:if'], 'all: ; if [ "$$V" = 1 ]; then zz_probe one; else zz_probe two; fi\n',
         variants=[{'V': '1'}, {'V': '2'}]),
    make('sh-case', ['sh:case'], 'all: ; case "$$V" in a) zz_probe a ;; *) zz_probe other ;; esac\n',
         variants=[{'V': 'a'}, {'V': 'b'}]),
    make('sh-for', ['sh:for.words'], 'all: ; for x in one two; do zz_probe "$$x"; done\n'),
    make('sh-negation', ['sh:negation'], 'all: ; if ! [ -e "$$F" ]; then zz_probe absent; fi\n',
         variants=[{'F': 'missing'}, {'F': 'Makefile'}]),
    make('sh-exit', ['sh:escape.exit'], 'all: ; zz_probe before; exit 0; zz_probe after\n'),
    make('sh-redirect', ['sh:redirect'], 'all: ; zz_probe quiet > /dev/null 2>&1\n'),
    make('sh-arithmetic', ['sh:word.arithmetic', 'sh:word.split-runtime'], 'all: ; zz_probe $$((1 + 1))\n'),
    make('sh-command-substitution', ['sh:word.command-substitution'], 'all: ; zz_probe "$$(echo hi)"\n'),
    make('sh-parameter-operator', ['sh:word.parameter-operator'], 'all: ; zz_probe "$${X:-dflt}"\n'),
    make('sh-pathname-expansion', ['sh:word.pathname-expansion'], 'all: ; zz_probe g/*.txt\n',
         files={'g/a.txt': '', 'g/b.txt': ''}),
    make('sh-special-parameter', ['sh:word.special-parameter'], 'all: ; zz_probe "$$#"\n'),
    make('sh-prefix-assignment', ['sh:call.prefix-assignment'], 'all: ; X=inner bash child.sh\n',
         files={'child.sh': 'zz_probe "$X"\n'}),
    make('sh-cd', ['sh:cd'], 'all: ; cd sub && zz_probe here\n', files={'sub/.keep': ''}),
    make('sh-cd-test-last', [], 'all: ; if [ "$$V" = 1 ]; then mkdir -p obj_fw; fi; cd obj_fw && zz_probe in\n',
         variants=EITHER),
    make('sh-cd-test-fails', [], 'all: ; cd missing && true; zz_probe here\n', expect='refused'),
    make('sh-plain-cd', [], 'all: ; cd missing; zz_probe here\n', expect='refused'),
    make('sh-set-errexit', ['sh:set.errexit'],
         'all: ; @set -e; if [ "$$V" = 1 ]; then mkdir -p obj_fw; fi; cd obj_fw; zz_probe in\n', variants=EITHER),
    # Python.
    python('py-script', ['cmd:python.script', 'py:program', 'py:capability.declared', 'py:exec.argv'],
           {'main.py': EXECUTE.format('argv')}, declare=['main.py']),
    python('py-import-module', ['py:import.module'],
           {'main.py': 'import helper\n', 'helper.py': EXECUTE.format('helper')}, declare=['helper.py']),
    python('py-import-shadows-stdlib', [],
           {'main.py': 'import json\n', 'json.py': EXECUTE.format('shadow')}, declare=['json.py']),
    python('py-import-external', ['py:import.external'], {'main.py': 'import json\nprint(json.dumps(1))\n'}),
    python('py-capability-import', ['py:capability.import'],
           {'main.py': "import pydoc\npydoc.pipepager('text', 'zz_probe pager')\n"}, expect='refused',
           refusal='undeclared executing', executes=True),
    python('py-capability-namespace', ['py:capability.namespace'],
           {'main.py': "import sys\nsys.modules['os'].system('zz_probe namespace')\n"}, expect='refused',
           refusal='undeclared executing', executes=True),
    python('py-capability-reflection', ['py:capability.reflection'],
           {'main.py': "import os\nos.__dict__['system']('zz_probe reflection')\n"}, expect='refused',
           refusal='undeclared executing', executes=True),
    python('py-loader-run-path', ['py:loader.run_path'],
           {'main.py': "import runpy\nrunpy.run_path('sub/mod.py')\n", 'sub/mod.py': EXECUTE.format('run-path')},
           declare=['sub/mod.py']),
    python('py-loader-spec', ['py:loader.spec_from_file_location', 'py:loader.module_from_spec',
                              'py:loader.exec_module'],
           {'main.py': "import importlib.util\nspec = importlib.util.spec_from_file_location('mod', 'sub/mod.py')\n"
                       "module = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(module)\n",
            'sub/mod.py': EXECUTE.format('spec')}, declare=['main.py', 'sub/mod.py']),
    python('py-search-path', ['py:search-path.entry', 'py:path.file', 'py:path.resolve', 'py:path.parent',
                              'py:path.join-operator', 'py:path.str', 'py:path.pathlib.Path'],
           {'main.py': "import sys\nfrom pathlib import Path\n"
                       "sys.path.insert(0, str(Path(__file__).resolve().parent / 'lib'))\nimport helper\n",
            'lib/helper.py': EXECUTE.format('lib')}, declare=['lib/helper.py']),
    python('py-search-path-name', ['py:path.parents', 'py:path.name', 'py:path.constant'],
           {'main.py': "import sys\nfrom pathlib import Path\nROOT = Path(__file__).resolve().parents[0]\n"
                       "sys.path.append(str(ROOT / 'lib'))\nimport helper\n",
            'lib/helper.py': EXECUTE.format('lib')}, declare=['lib/helper.py']),
    python('py-imported-constant', ['py:path.imported-constant'],
           {'main.py': "import sys\nfrom consts import LIB\nsys.path.insert(0, LIB)\nimport helper\n",
            'consts.py': "LIB = 'lib'\n", 'lib/helper.py': EXECUTE.format('lib')}, declare=['lib/helper.py']),
]

# R638-6 Make probes: the reviewers' hidden command is the sentinel.
R638_MAKE = [
    ('M1', 'refused', {'Makefile': 'ifeq (a,b)\nelseX = echo\nendif\nall: ; $(elseX) zz_probe hidden\n'}, 'make\n', {}),
    ('M2', 'refused', {'Makefile': 'ifeq (a,b)\nendifX = echo\nendif\nall: ; $(endifX) zz_probe hidden\n'},
     'make\n', {}),
    ('M3', 'identical', {'Makefile': 'FOO += $(BAR)\nBAR = ; zz_probe hidden\nall: ; $(FOO) okay\n'}, 'make\n',
     {'env': {'FOO': 'echo'}, 'workflow_environment': ['FOO']}),
    ('M3b', 'identical', {'Makefile': 'FOO += $(BAR)\nBAR = ; zz_probe hidden\nall: ; $(FOO) okay\n'},
     'export FOO=echo; make\n', {}),
    ('M4', 'identical', {'Makefile': 'RUN = $(if $(0),,echo) zz_probe hidden\nall: ; $(call RUN)\n'}, 'make\n', {}),
    ('M5', 'identical', {'Makefile': 'inner = $(if $(2),echo,zz_probe) okay\nouter = $(call inner,x)\n'
                                     'all: ; $(call outer,a,b)\n'}, 'make\n', {}),
    ('M6', 'identical', {'Makefile': 'all: X = zz_probe\nall: dep ; @echo done\ndep: ; $(X) okay\n'}, 'make\n', {}),
    ('M7', 'refused', {'Makefile': 'define X\necho a\n\tendef\nY = zz_probe\nendef\nall: ; $(X) $(Y)\n'},
     'make\n', {}),
    ('M8', 'identical', {'b.sh': 'zz_probe b\n', 'a.sh': 'zz_probe a\n',
                         'Makefile': 'all: ; bash $(firstword $(wildcard *.sh))\n'}, 'make\n', {}),
    ('M9', 'identical', {'Makefile': 'all: ; $(if x,echo,$(shell zz_probe hidden)) okay\n'}, 'make\n', {}),
    ('M10', 'identical', {'Makefile': 'first: ; echo okay\nsecond: ; zz_probe hidden\n.DEFAULT_GOAL := second\n'},
     'make\n', {}),
    ('M11', 'refused', {'Makefile': 'BAR = zz_probe\nall: ; $(FOO) okay\n'}, "make 'FOO=$(BAR)'\n", {}),
    ('M12', 'identical', {'Makefile': 'X := $(subst a,#,abc)\nall: ; echo $(X) ; zz_probe hidden\n'}, 'make\n', {}),
    ('M13', 'identical', {'Makefile': 'all: TOOL = echo\nall: ; $(TOOL) okay\n'}, 'TOOL=zz_probe make\n', {}),
    ('M14', 'identical', {'Makefile': 'all: ;\n\tzz_probe hidden\n'}, 'make\n', {}),
    ('M15', 'refused', {'Makefile': 'ifeq (a,b)\nelse: ; echo\nendif\nall: ; echo okay\n'}, 'make\n', {}),
    ('M16', 'identical', {'Makefile': 'all:\n\techo okay\n\n# c\n\tzz_probe hidden\n'}, 'make\n', {}),
    ('M17', 'refused', {'Makefile': 'ifeq (a,b)\nelsewhere: ; zz_probe hidden\nendif\nall: elsewhere ; echo okay\n'},
     'make\n', {}),
    ('M18', 'identical', {'Makefile': 'all: ; $(MAKE) -C sub\n', 'sub/Makefile': 'all: ; zz_probe hidden\n'},
     'make -n\n', {}),
    ('M19', 'identical', {'Makefile': 'X = echo\nall: dep\ndep: ; $(X) okay\nall: X = zz_probe\n'}, 'make\n', {}),
    ('M20', 'identical', {'Makefile': 'all: ; bash $(abspath sub/link/../run.sh)\n', 'sub/run.sh': EVIL,
                          'other/deep/.keep': '', 'other/run.sh': OK}, 'make\n',
     {'links': {'sub/link': '../other/deep'}}),
    ('M21', 'refused', {'Makefile': 'all: ; dirname() { echo sub; }; bash "$$(dirname x/run.sh)/run.sh"\n',
                        'x/run.sh': OK, 'sub/run.sh': EVIL}, 'make\n', {}),
]
# R638-6 shell probes.
R638_SHELL = [
    ('S1', 'refused', {'x/run.sh': OK, 'sub/run.sh': EVIL},
     'dirname() { echo sub; }\nbash "$(dirname x/run.sh)/run.sh"\n'),
    ('S2', 'refused', {'scripts/run.sh': OK, 'run.sh': EVIL},
     'cd() { :; }\nd="$(cd scripts && pwd)"\nbash "$d/run.sh"\n'),
    ('S3', 'refused', {'scripts/run.sh': OK, 'sub/run.sh': EVIL},
     'pwd() { echo sub; }\nbash "$(cd scripts && pwd)/run.sh"\n'),
    ('S4', 'identical', {'scripts/run.sh': OK, 'run.sh': EVIL}, 'cd() { :; }\ncd scripts\nbash run.sh\n'),
    ('S5', 'refused', {'-/run.sh': OK, 'run.sh': EVIL, 'sub/run.sh': EVIL},
     'cd sub\ncd ..\nbash "$(cd - > /dev/null && pwd)/run.sh"\n'),
    ('S6', 'refused', {'x/run.sh': OK, 'sub/run.sh': EVIL},
     'realpath() { echo sub/run.sh; }\nbash "$(realpath x/run.sh)"\n'),
    ('S7', 'identical', {}, 'echo() { zz_probe hidden; }\necho okay\n'),
    ('S8', 'identical', {'run.sh': OK}, 'bash() { zz_probe hidden; }\nbash run.sh\n'),
    ('S9', 'refused', {'run.sh': OK}, 'shopt -s expand_aliases\nalias bash=zz_probe\nbash run.sh\n'),
    ('S10', 'refused', {'scripts/run.sh': OK, 'run.sh': EVIL}, 'command cd scripts\nbash run.sh\n'),
]
# R638-6 Python capability probes, each in an undeclared program.
R638_PYTHON = [
    ('PYW1', "import sys\nsys.modules['os'].system('zz_probe pyw1')\n"),
    ('PYW2', "import subprocess\nimport sys\nsys.modules['subprocess'].run(['zz_probe', 'pyw2'])\n"),
    ('PYW3', "import os\ngetattr(os, 'sys' + 'tem')('zz_probe pyw3')\n"),
    ('PYW4', "import os\nos.__dict__['system']('zz_probe pyw4')\n"),
    ('PYW5', "import builtins\ngetattr(builtins, 'ex' + 'ec')(\"import os; os.system('zz_probe pyw5')\")\n"),
    ('PYW6', "import builtins\nbuiltins.eval(\"__import__('os').system('zz_probe pyw6')\")\n"),
    ('import-builtin', "__import__('os').system('zz_probe import')\n"),
    ('exec', "exec(\"import os; os.system('zz_probe exec')\")\n"),
    ('compile', "eval(compile(\"__import__('os').system('zz_probe compile')\", 'x', 'eval'))\n"),
    ('from-alias', "from os import system as s\ns('zz_probe alias')\n"),
    ('import-module', "import importlib\nimportlib.import_module('os').system('zz_probe module')\n"),
    ('ctypes', "import ctypes\nctypes.CDLL(None).system(b'zz_probe ctypes')\n"),
    ('posix-spawnp', "import os\nos.waitpid(os.posix_spawnp('zz_probe', ['zz_probe', 'spawn'], os.environ), 0)\n"),
    ('execvp', "import os\nos.execvp('zz_probe', ['zz_probe', 'execvp'])\n"),
    ('pty', "import pty\npty.spawn(['zz_probe', 'pty'])\n"),
    ('asyncio', "import asyncio\nasync_run = asyncio.run\n"
                "async_run(asyncio.create_subprocess_exec('zz_probe', 'asyncio'))\n"),
    ('runpy', "import runpy\nrunpy.run_module('zz_hidden_module')\n"),
    ('pip', "import pip\n"),
    ('socket', "import socket\n"),
    ('webbrowser', "import webbrowser\n"),
    ('popen', "import os\nos.popen('zz_probe popen').read()\n"),
]
EXECUTES = {'PYW1', 'PYW2', 'PYW3', 'PYW4', 'PYW5', 'PYW6', 'import-builtin', 'exec', 'compile', 'from-alias',
            'import-module', 'ctypes', 'posix-spawnp', 'execvp', 'pty', 'popen'}
# R639-6 walker probes.
R639 = [
    ('make-explicit-stem', 'refused', {'Makefile': 'all: probe.c\nprobe.c: ; bash $*bootstrap.sh\n',
                                       'bootstrap.sh': OK, 'probebootstrap.sh': EVIL}, 'make\n'),
    ('shell-short-circuit', 'refused', {'evil.sh': EVIL, 'benign.sh': OK},
     'X=evil.sh; [ -e missing ] && X=benign.sh; bash "$X"\n'),
    ('make-unlisted', 'refused', {'Makefile': 'override X = echo\nall: ; $(X) okay\n'}, 'make\n'),
    ('shell-unlisted', 'refused', {}, 'select x in a; do echo "$x"; done\n'),
    ('python-unlisted', 'refused', {'probe.py': 'async def probe():\n pass\n'}, 'python3 probe.py\n'),
    ('python-network', 'refused', {'probe.py': 'import urllib.request\n'}, 'python3 probe.py\n'),
    ('shell-pwd-shadow', 'refused', {'safe/bootstrap.sh': OK, 'evil/bootstrap.sh': EVIL},
     'pwd() { echo evil; }; cd "$(cd safe && pwd)"; bash bootstrap.sh\n'),
]

FIXTURES += [{'id': f'R638-6-{name}', 'shapes': [], 'expect': expect, 'files': files, 'run': run,
              'probe': f'R638-6 {name}', 'executes': expect == 'refused' and name not in ('M7', 'M15', 'M17'), **more}
             for name, expect, files, run, more in R638_MAKE]
FIXTURES += [{'id': f'R638-6-{name}', 'shapes': [], 'expect': expect, 'files': files, 'run': run,
              'probe': f'R638-6 {name}', 'executes': expect == 'refused'}
             for name, expect, files, run in R638_SHELL]
FIXTURES += [{'id': f'R638-6-python-{name}', 'shapes': [], 'expect': 'refused', 'files': {'main.py': source},
              'run': 'python3 main.py\n', 'probe': f'R638-6 Python {name}', 'executes': name in EXECUTES}
             for name, source in R638_PYTHON]
FIXTURES += [{'id': f'R639-6-{name}', 'shapes': [], 'expect': expect, 'files': files, 'run': run,
              'probe': f'R639-6 {name}', 'executes': name in ('make-explicit-stem', 'shell-short-circuit',
                                                              'shell-pwd-shadow')}
             for name, expect, files, run in R639]

# Probes for workflow environment names, checkout state and local declarations.
HOOK_NAMES = ('PERL5OPT', 'NODE_OPTIONS', 'GIT_EXEC_PATH', 'GIT_CONFIG_COUNT', 'GIT_CONFIG_KEY_0', 'PYTHONUSERBASE',
              'PYTHONSTARTUP', 'LD_AUDIT', 'HOME')
#: Two scripts a `cd` chooses between, and a program that removes one directory in one variant.
BRANCHES = {'clean.py': CLEAN, 'sub/run.sh': 'zz_probe sub\n', 'other/run.sh': 'zz_probe other\n'}
ROUND7 = [
    ('R638-7-N3a-exported-function', 'refused', {}, 'echo ok\n',
     {'env': {'BASH_FUNC_echo%%': '() { zz_probe hidden; }'}, 'refusal': 'exported shell function'}),
    ('R638-7-N3a-unmodelled-name', 'refused', {}, 'zz_probe ok\n',
     {'env': {'ZZ_UNMODELLED': 'x'}, 'refusal': 'unmodelled workflow environment name'}),
    *[(f'R638-7-N3a-{name}', 'refused', {}, 'zz_probe ok\n',
       {'env': {name: 'x'}, 'refusal': 'interpreter hook in workflow environment'}) for name in HOOK_NAMES],
    ('R638-7-N3b-if', 'refused', BRANCHES,
     'python3 clean.py\nif cd sub; then :; else cd other; fi\nbash run.sh\n',
     {'variants': [{}, {'RM': '1'}], 'refusal': 'ambiguous shell directory'}),
    ('R638-7-N3b-or', 'refused', BRANCHES,
     'python3 clean.py\ncd sub || cd other\nbash run.sh\n',
     {'variants': [{}, {'RM': '1'}], 'refusal': 'ambiguous shell directory'}),
    ('R639-7-F1-initializer', 'identical', {'bootstrap.sh': 'true\n', 'evilbootstrap.sh': EVIL},
     'X=evil\nf() { local X="$X"; bash "${X}bootstrap.sh"; }\nf\n', {}),
    ('R639-7-F1-redeclared-local', 'identical', {}, 'f() { local X=first; local X; zz_probe "$X"; }\nf\n', {}),
    ('R639-7-F1-new-local', 'identical', {}, 'X=outer\nf() { local X; zz_probe "x$X"; }\nf\nzz_probe "$X"\n', {}),
    ('R639-7-F1-words-first', 'identical', {},
     'X=outer\nf() { local X=1 Y="$X"; zz_probe "$Y" "$X"; }\nf\nzz_probe "$X"\n', {}),
    ('R639-7-F1-declare', 'identical', {}, 'X=outer\nf() { declare X="$X"; zz_probe "$X"; X=inner; }\nf\n'
     'zz_probe "$X"\n', {}),
    ('R639-7-F1-nested-scope', 'identical', {},
     'X=outer\ng() { zz_probe "$X"; local X; zz_probe "y$X"; }\nf() { local X=mid; g; zz_probe "$X"; }\nf\n', {}),
    ('R639-7-F1-appending', 'refused', {}, 'f() { local X+=a; zz_probe "$X"; }\nf\n',
     {'refusal': 'uncensused shell Args.Append'}),
]
FIXTURES += [{'id': name, 'shapes': [], 'expect': expect, 'files': files, 'run': run, 'probe': name,
              'executes': expect == 'refused', **more}
             for name, expect, files, run, more in ROUND7]

"""Run reviewer probes through the head's differential harness functions (walker vs the real tool on PATH).

usage: CI_IMAGE_SHFMT=... python3 -I walker_probes.py CLONE OUT.jsonl [ID ...]
Each probe uses only the harness's fixture schema; `uncensused` lists shapes the census does not accept.
"""
import json, sys, tempfile
from pathlib import Path
clone = Path(sys.argv[1]); sys.path.insert(0, str(clone / 'scripts'))
import ci_differential as d

ENVSH = 'zz_probe bash-env\n'
PROBES = [
 {'id': 'pipe-assignment-subshell', 'run': 'X=a\ntrue | X=b\nzz_probe "$X"\n', 'expect': 'identical'},
 {'id': 'make-target-specific-inherited', 'files': {'Makefile': 'all: X = zz_probe\nall: dep ; @true\ndep: ; $(X) inherited\n'},
  'run': 'make\n', 'expect': 'identical'},
 {'id': 'make-shell-override', 'files': {'Makefile': 'SHELL = /bin/bash\nall: ; [[ a == a ]] && zz_probe bashonly\n'},
  'run': 'make\n', 'expect': 'identical'},
 {'id': 'make-env-makeflags-variable', 'files': {'Makefile': 'X = true\nall: ; $(X) mf\n'},
  'run': "export MAKEFLAGS='X=zz_probe'\nmake\n", 'expect': 'identical'},
 {'id': 'make-prefix-makeflags-variable', 'files': {'Makefile': 'X = true\nall: ; $(X) mf\n'},
  'run': "MAKEFLAGS='X=zz_probe' make\n", 'expect': 'identical'},
 {'id': 'make-env-makefiles', 'files': {'Makefile': 'X ?= true\nall: ; $(X) mk\n', 'extra.mk': 'X = zz_probe\n'},
  'run': 'MAKEFILES=extra.mk make\n', 'expect': 'identical'},
 {'id': 'bash-env-startup-file', 'files': {'env.sh': ENVSH, 'run.sh': 'true\n'},
  'run': 'BASH_ENV=./env.sh bash run.sh\n', 'expect': 'identical'},
 {'id': 'bash-cdpath', 'files': {'sub/run.sh': 'zz_probe plain\n', 'other/sub/run.sh': 'zz_probe cdpath\n'},
  'run': 'export CDPATH=other\ncd sub\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'path-shadows-table-command', 'files': {'bin/git': '#!/bin/sh\nzz_probe shadowed-git\n'}, 'executable': ['bin/git'],
  'run': 'export PATH="$PWD/bin:$PATH"\ngit --version\n', 'expect': 'identical'},
 {'id': 'pythonpath-module', 'files': {'main.py': 'import zzmod\n', 'other/zzmod.py': "import subprocess\nsubprocess.run(['zz_probe', 'pythonpath'])\n"},
  'run': 'PYTHONPATH=other python3 main.py\n', 'expect': 'identical'},
 {'id': 'bash-and-assignment-unexecuted', 'run': 'X=a\nfalse && X=b || true\nzz_probe "$X"\n', 'expect': 'identical'},
 {'id': 'bash-loop-cd', 'files': {'run.sh': 'zz_probe root\n', 'sub/run.sh': 'zz_probe sub\n', 'sub/sub/run.sh': 'zz_probe subsub\n'},
  'run': 'for i in 1 2; do bash run.sh; cd sub; done\n', 'expect': 'identical'},
 {'id': 'bash-function-cd-escape', 'files': {'sub/run.sh': 'zz_probe sub\n', 'run.sh': 'zz_probe root\n'},
  'run': 'f() { cd sub; return 0; }\nf\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'bash-subshell-cd', 'files': {'sub/run.sh': 'zz_probe sub\n', 'run.sh': 'zz_probe root\n'},
  'run': '(cd sub)\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'bash-pipe-cd', 'files': {'sub/run.sh': 'zz_probe sub\n', 'run.sh': 'zz_probe root\n'},
  'run': 'cd sub | true\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'bash-cd-dotdot-symlink', 'files': {'real/inner/run.sh': 'zz_probe physical\n', 'inner2/run.sh': 'zz_probe logical\n', 'run.sh': 'true\n'},
  'links': {'link': 'real/inner'}, 'run': 'cd link\ncd ..\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'bash-env-prefix-function', 'run': 'f() { zz_probe "$X"; }\nX=a\nX=b f\nzz_probe "$X"\n', 'expect': 'identical'},
 {'id': 'bash-readonly-assignment-fails', 'run': 'X=zz_probe\nexport X\n"$X" ok\n', 'expect': 'identical'},
 {'id': 'make-recipe-prefix-env', 'files': {'Makefile': 'all: ; X=zz_probe; $$X recipevar\n'}, 'run': 'make\n', 'expect': 'identical'},
 {'id': 'make-oneshell', 'files': {'Makefile': '.ONESHELL:\nall:\n\tcd sub\n\tbash run.sh\n', 'sub/run.sh': 'zz_probe oneshell\n', 'run.sh': 'zz_probe noshell\n'},
  'run': 'make\n', 'expect': 'identical'},
 {'id': 'make-static-pattern-stem', 'files': {'Makefile': 'all: a.x\na.x: %.x: ; zz_probe $*\n'}, 'run': 'make\n', 'expect': 'identical'},
 {'id': 'make-env-override', 'files': {'Makefile': 'X = true\nall: ; $(X) envoverride\n'}, 'run': 'X=zz_probe make -e\n', 'expect': 'identical'},
 {'id': 'make-vpath-script', 'files': {'Makefile': 'vpath %.sh sub\nall: run.sh ; bash $<\n', 'sub/run.sh': 'zz_probe vpath\n'}, 'run': 'make\n', 'expect': 'identical'},
 {'id': 'bash-ifs-split', 'files': {}, 'run': 'IFS=:\nX="zz_probe:split"\n$X\n', 'expect': 'identical'},
 {'id': 'bash-noglob', 'files': {'zz_probe': ''}, 'run': 'set -f\nzz_probe *\n', 'expect': 'identical'},
 {'id': 'bash-cd-env-pwd', 'files': {'sub/run.sh': 'zz_probe sub\n', 'run.sh': 'zz_probe root\n'},
  'run': 'cd sub\nbash "$OLDPWD/run.sh"\n', 'expect': 'identical'},
 {'id': 'bash-source-args', 'files': {'lib.sh': 'zz_probe "$1"\n'}, 'run': 'set -- outer\n. ./lib.sh inner\n', 'expect': 'identical'},
 {'id': 'env-cdpath', 'env': {'CDPATH': 'other'}, 'files': {'sub/run.sh': 'zz_probe plain\n', 'other/sub/run.sh': 'zz_probe cdpath\n'},
  'run': 'cd sub\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'env-bash-env', 'env': {'BASH_ENV': './env.sh'}, 'files': {'env.sh': ENVSH, 'run.sh': 'true\n'},
  'run': 'bash run.sh\n', 'expect': 'identical'},
 {'id': 'env-makeflags', 'env': {'MAKEFLAGS': 'X=zz_probe'}, 'files': {'Makefile': 'X = true\nall: ; $(X) mf\n'},
  'run': 'make\n', 'expect': 'identical'},
 {'id': 'env-makefiles', 'env': {'MAKEFILES': 'extra.mk'}, 'files': {'Makefile': 'X ?= true\nall: ; $(X) mk\n', 'extra.mk': 'X = zz_probe\n'},
  'run': 'make\n', 'expect': 'identical'},
 {'id': 'env-pythonpath', 'env': {'PYTHONPATH': 'other'}, 'files': {'main.py': 'import zzmod\n', 'other/zzmod.py': "import subprocess\nsubprocess.run(['zz_probe', 'pythonpath'])\n"},
  'run': 'python3 main.py\n', 'expect': 'identical'},
 {'id': 'env-path-shadow', 'env': {'PATH': 'bin:/usr/bin:/bin'}, 'files': {'bin/git': '#!/bin/sh\nzz_probe shadowed-git\n'}, 'executable': ['bin/git'],
  'run': 'git --version\n', 'expect': 'identical'},
 {'id': 'env-ifs', 'env': {'IFS': ':'}, 'run': 'X="zz_probe:split"\nzz_probe $X\n', 'expect': 'identical'},
 {'id': 'env-make-var', 'env': {'X': 'zz_probe'}, 'files': {'Makefile': 'X ?= true\nall: ; $(X) envvar\n'}, 'run': 'make\n', 'expect': 'identical'},
 {'id': 'env-shellopts', 'env': {'SHELLOPTS': 'noglob'}, 'files': {'zz_probe': ''}, 'run': 'zz_probe *\n', 'expect': 'identical'},
 {'id': 'env-pythonsafepath', 'env': {'PYTHONSAFEPATH': '1', 'PYTHONPATH': 'other'}, 'files': {'main.py': 'import zzmod\n', 'zzmod.py': "import subprocess\nsubprocess.run(['zz_probe', 'scriptdir'])\n", 'other/zzmod.py': "import subprocess\nsubprocess.run(['zz_probe', 'pythonpath'])\n"},
  'run': 'python3 main.py\n', 'expect': 'identical'},
 {'id': 'env-gnumakeflags', 'env': {'GNUMAKEFLAGS': 'X=zz_probe'}, 'files': {'Makefile': 'X = true\nall: ; $(X) gmf\n'},
  'run': 'make\n', 'expect': 'identical'},
 {'id': 'env-function-export', 'env': {'BASH_FUNC_git%%': '() { zz_probe exported-function; }'}, 'files': {'run.sh': 'git --version\n'},
  'run': 'bash run.sh\n', 'expect': 'identical'},
 {'id': 'env-function-export-echo', 'env': {'BASH_FUNC_echo%%': '() { zz_probe exported-function; }'}, 'files': {'run.sh': 'echo ok\n'},
  'run': 'bash run.sh\n', 'expect': 'identical'},
 {'id': 'env-function-export-step', 'env': {'BASH_FUNC_echo%%': '() { zz_probe exported-function; }'},
  'run': 'echo ok\n', 'expect': 'identical'},
 {'id': 'env-wrapper-function', 'files': {'run.sh': 'echo ok\n'},
  'run': "env 'BASH_FUNC_echo%%=() { zz_probe exported-function; }' bash run.sh\n", 'expect': 'identical'},
 {'id': 'env-wrapper-cdpath', 'files': {'sub/run.sh': 'zz_probe plain\n', 'other/sub/run.sh': 'zz_probe cdpath\n', 'go.sh': 'cd sub\nbash run.sh\n'},
  'run': "env CDPATH=other bash go.sh\n", 'expect': 'identical'},
 {'id': 'env-perl5opt-step', 'env': {'PERL5OPT': '-Mzzmod', 'PERL5LIB': 'lib'}, 'files': {'lib/zzmod.pm': "package zzmod; system('zz_probe', 'perl5opt'); 1;\n"},
  'run': "perl -e 1\n", 'expect': 'identical'},
 {'id': 'certain-cd-after-rm', 'files': {'sub/run.sh': 'zz_probe sub\n', 'other/run.sh': 'zz_probe other\n'},
  'run': 'rm -rf sub\nif cd sub; then :; else cd other; fi\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'certain-cd-after-mv', 'files': {'sub/run.sh': 'zz_probe sub\n', 'other/run.sh': 'zz_probe other\n'},
  'run': 'mv sub gone\ncd sub || cd other\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'certain-cd-file-replaced', 'files': {'sub/run.sh': 'zz_probe sub\n', 'run.sh': 'zz_probe root\n'},
  'run': 'rm -rf sub && touch sub\ncd sub || true\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'certain-cd-after-python-rmtree', 'files': {'sub/run.sh': 'zz_probe sub\n', 'other/run.sh': 'zz_probe other\n', 'clean.py': "import shutil\nshutil.rmtree('sub')\n"},
  'run': 'python3 clean.py\nif cd sub; then :; else cd other; fi\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'certain-cd-or-after-python-rmtree', 'files': {'sub/run.sh': 'zz_probe sub\n', 'other/run.sh': 'zz_probe other\n', 'clean.py': "import shutil\nshutil.rmtree('sub')\n"},
  'run': 'python3 clean.py\ncd sub || cd other\nbash run.sh\n', 'expect': 'identical'},
 {'id': 'script-replaced-by-python', 'files': {'run.sh': 'true\n', 'gen.py': "open('run.sh', 'w').write('zz_probe regenerated\\n')\n"},
  'run': 'python3 gen.py\nbash run.sh\n', 'expect': 'identical'},
]

census = set(json.loads((clone / 'ci/image/syntax-census.json').read_text())['shapes'])
only = set(sys.argv[3:])
with open(sys.argv[2], 'w') as out:
    for fixture in PROBES:
        if only and fixture['id'] not in only:
            continue
        fixture.setdefault('observe', [])
        with tempfile.TemporaryDirectory(prefix='r638-probe-') as directory:
            scratch = Path(directory); tree = scratch / 'tree'; tree.mkdir()
            d.build(fixture, tree)
            walker = d.walk(fixture, tree)
            ran, statuses = d.run(fixture, tree, scratch)
            result = d.outcome(fixture, walker, ran)
            row = {'id': fixture['id'], 'outcome': result, 'refusal': walker['refusal'] and walker['refusal'][:160],
                   'walker': walker['resolved'], 'real': ran, 'statuses': statuses, 'residue': walker['residue'],
                   'uncensused': sorted(set(walker['shapes']) - census)}
            row = json.loads(json.dumps(row).replace(str(tree.resolve()), '<fixture>').replace(str(tree), '<fixture>'))
        out.write(json.dumps(row) + '\n'); print(json.dumps(row)[:600], flush=True)

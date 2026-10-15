"""Python capability probes through the head's differential harness (walker vs CPython 3.12 on PATH).

usage: CI_IMAGE_SHFMT=... python3 -I python_probes.py CLONE OUT.jsonl
"""
import json, sys, tempfile
from pathlib import Path
clone = Path(sys.argv[1]); sys.path.insert(0, str(clone / 'scripts'))
import ci_differential as d
BODIES = {
 'getoutput': "import subprocess\nsubprocess.getoutput('zz_probe getoutput')\n",
 'getstatusoutput': "import subprocess\nsubprocess.getstatusoutput('zz_probe gso')\n",
 'os-popen': "import os\nos.popen('zz_probe popen').read()\n",
 'pty-spawn': "import pty\npty.spawn(['zz_probe', 'pty'])\n",
 'posix-spawnp': "import os\nos.waitpid(os.posix_spawnp('zz_probe', ['zz_probe', 'ps'], dict(os.environ)), 0)\n",
 'spawnlp': "import os\nos.spawnlp(os.P_WAIT, 'zz_probe', 'zz_probe', 'spawnlp')\n",
 'import-module': "import importlib\nimportlib.import_module('subprocess').run(['zz_probe', 'im'])\n",
 'dunder-import': "__import__('subprocess').run(['zz_probe', 'di'])\n",
 'from-import-alias': "from subprocess import run as r\nr(['zz_probe', 'alias'])\n",
 'bound-alias': "import subprocess as sp\nf = sp.run\nf(['zz_probe', 'bound'])\n",
 'partial': "import functools, subprocess\nfunctools.partial(subprocess.run, ['zz_probe', 'partial'])()\n",
 'map': "import subprocess\nlist(map(subprocess.run, [['zz_probe', 'map']]))\n",
 'lambda': "import subprocess\n(lambda f: f(['zz_probe', 'lambda']))(subprocess.run)\n",
 'thread': "import subprocess, threading\nt = threading.Thread(target=subprocess.run, args=(['zz_probe', 'thread'],))\nt.start(); t.join()\n",
 'atexit': "import atexit, os\natexit.register(os.system, 'zz_probe atexit')\n",
 'ctypes-system': "import ctypes\nctypes.CDLL(None).system(b'zz_probe ctypes')\n",
 'exec-builtin': "exec(\"import subprocess; subprocess.run(['zz_probe', 'exec'])\")\n",
 'methodcaller': "import operator, subprocess\noperator.methodcaller('run', ['zz_probe', 'mc'])(subprocess)\n",
 'list-argv-var': "import subprocess\ncmd = ['zz_probe', 'var']\nsubprocess.run(cmd)\n",
 'argv-mutated': "import subprocess\ncmd = ['true', 'x']\ncmd[0] = 'zz_probe'\nsubprocess.run(cmd)\n",
 'argv-append-in-branch': "import subprocess, os\ncmd = ['true']\nif os.environ.get('ZZ_UNSET') is None:\n    cmd = ['zz_probe', 'branch']\nsubprocess.run(cmd)\n",
 'function-default-arg': "import subprocess\ndef go(c=['zz_probe', 'default']):\n    subprocess.run(c)\ngo()\n",
 'class-method': "import subprocess\nclass A:\n    def go(self):\n        subprocess.run(['zz_probe', 'method'])\nA().go()\n",
 'decorator': "import subprocess\ndef deco(f):\n    subprocess.run(['zz_probe', 'deco'])\n    return f\n@deco\ndef g():\n    pass\n",
 'shadowed-subprocess': "import subprocess\nclass subprocess:\n    @staticmethod\n    def run(c):\n        import os; os.system('zz_probe shadow')\nsubprocess.run(['true'])\n",
 'os-execvp-fork': "import os\npid = os.fork()\nif pid == 0:\n    os.execvp('zz_probe', ['zz_probe', 'fork'])\nos.waitpid(pid, 0)\n",
 'multiprocessing': "import multiprocessing, subprocess\nif __name__ == '__main__':\n    p = multiprocessing.Process(target=subprocess.run, args=(['zz_probe', 'mp'],)); p.start(); p.join()\n",
 'environ-path': "import os, subprocess\nos.environ['PATH'] = os.getcwd() + '/bin:' + os.environ['PATH']\nsubprocess.run(['git', '--version'])\n",
}
census = set(json.loads((clone / 'ci/image/syntax-census.json').read_text())['shapes'])
with open(sys.argv[2], 'w') as out:
    for name, body in BODIES.items():
        files = {'main.py': body}
        fixture = {'id': f'py-{name}', 'files': files, 'run': 'python3 main.py\n', 'expect': 'identical', 'observe': []}
        if name == 'environ-path':
            files['bin/git'] = '#!/bin/sh\nzz_probe shadowed-git\n'; fixture['executable'] = ['bin/git']
        with tempfile.TemporaryDirectory(prefix='r638-py-') as directory:
            scratch = Path(directory); tree = scratch / 'tree'; tree.mkdir()
            d.build(fixture, tree)
            walker = d.walk(fixture, tree)
            ran, statuses = d.run(fixture, tree, scratch)
            row = {'id': fixture['id'], 'outcome': d.outcome(fixture, walker, ran),
                   'refusal': walker['refusal'] and walker['refusal'][:140], 'walker': walker['resolved'], 'real': ran,
                   'statuses': statuses, 'residue': walker['residue'], 'uncensused': sorted(set(walker['shapes']) - census)}
            row = json.loads(json.dumps(row).replace(str(tree.resolve()), '<fixture>'))
        out.write(json.dumps(row) + '\n'); print(json.dumps(row)[:420], flush=True)

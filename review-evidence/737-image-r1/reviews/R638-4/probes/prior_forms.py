# Included by r638_4_probes.py: every form R638-3 and R639-3 listed, new-construct
# refusals, and one unsupported variant per supported construct.
NPX = 'npx fixture\n'


def r(cmd, **step):
    return p(lambda f: f.run(cmd, **step))


def py(src):
    return p(lambda f: (f.file('bootstrap.py', src), f.run('python3 bootstrap.py')))


for pid, desc, setup in [
    ('R638-3-01', 'gh extension install', r('gh extension install example/gh-fixture')),
    ('R638-3-02', 'gh release download', r('gh release download v1.0 -R example/tool')),
    ('R638-3-03', 'git submodule add <url>', r('git submodule add https://example.invalid/tool')),
    ('R638-3-04', 'git config submodule url then update', r('git config submodule.x.url https://example.invalid/tool && git submodule update --init x')),
    ('R638-3-05', 'git clone host:path', r('git clone --no-hardlinks git@host:org/tool.git')),
    ('R638-3-06', 'git archive --remote', r('git archive --remote=https://example.invalid/tool HEAD')),
    ('R638-3-07', 'python3 heredoc without -', r("python3 <<'EOF'\nimport urllib.request\nEOF")),
    ('R638-3-08', 'python3 -I - heredoc', r("python3 -I - <<'EOF'\nimport urllib.request\nEOF")),
    ('R638-3-09', 'os.popen', py('import os\nos.popen("npx fixture")\n')),
    ('R638-3-10', 'os.execvp', py('import os\nos.execvp("npx", ["npx", "fixture"])\n')),
    ('R638-3-11', 'os.spawnlp', py('import os\nos.spawnlp(0, "npx", "npx", "fixture")\n')),
    ('R638-3-12', 'asyncio.create_subprocess_exec', py('import asyncio\nasyncio.create_subprocess_exec("npx", "fixture")\n')),
    ('R638-3-13', 'pip._internal install', py('import pip._internal\npip._internal.main(["install", "fixture"])\n')),
    ('R638-3-14', 'urllib3 import', py('import urllib3\n')),
    ('R638-3-15', 'asyncio.open_connection ssl', py('import asyncio, ssl\nasyncio.open_connection("h", 443, ssl=True)\n')),
    ('R638-3-16', 'pattern-rule prerequisite', p(lambda f: (f.file('Makefile', 'all: gen\n%:\n\tnpx fixture\n'), f.run('make')))),
    ('R638-3-17', 'make --directory=fx run', p(lambda f: (f.file('Makefile', 'run:\n\techo ok\n'), f.file('fx/Makefile', 'run:\n\tnpx fixture\n'), f.run('make --directory=fx run')))),
    ('R638-3-18', 'make with working-directory: fx', p(lambda f: (f.file('Makefile', 'all:\n\techo ok\n'), f.file('fx/Makefile', 'all:\n\tnpx fixture\n'), f.run('make', **{'working-directory': 'fx'})))),
    ('R638-3-19', 'job-level reusable workflow', p(lambda f: f.doc({'jobs': {'gate': {'uses': 'example/tools/.github/workflows/install.yml@main'}}}))),
    ('R638-3-B1', "echo 'npx' | bash", r("echo 'npx fixture' | bash")),
    ('R638-3-B2', "bash <<< 'npx'", r("bash <<< 'npx fixture'")),
    ('R638-3-B3', 'alias runner = subprocess.run (undeclared)', py('import subprocess\nrunner = subprocess.run\nrunner(["npx", "fixture"])\n')),
    ('R638-3-B4', 'importlib.import_module urllib', py('import importlib\nimportlib.import_module("urllib.request")\n')),
    ('R638-3-I3', 'moving container tag', p(lambda f: f.doc({'jobs': {'gate': {'container': 'ubuntu:24.04', 'steps': [{'run': 'echo ok'}]}}}))),
    ('R638-3-I4', 'moving service tag', p(lambda f: f.doc({'jobs': {'gate': {'services': {'db': {'image': 'postgres:16'}}, 'steps': [{'run': 'echo ok'}]}}}))),
    ('R639-3-01', 'make --file=install.mk', p(lambda f: (f.file('Makefile', 'all:\n\techo ok\n'), f.file('install.mk', 'all:\n\tbrand_new_command install tool\n'), f.run('make --file=install.mk')))),
    ('R639-3-02', 'make -finstall.mk', p(lambda f: (f.file('Makefile', 'all:\n\techo ok\n'), f.file('install.mk', 'all:\n\tbrand_new_command install tool\n'), f.run('make -finstall.mk')))),
    ('R639-3-03', '.DEFAULT_GOAL := install', p(lambda f: (f.file('Makefile', 'benign:\n\techo ok\n.DEFAULT_GOAL := install\ninstall:\n\tbrand_new_command install tool\n'), f.run('make')))),
    ('R639-3-04', 'make install via %: rule', p(lambda f: (f.file('Makefile', 'all:\n\techo ok\n%:\n\tbrand_new_command install tool\n'), f.run('make install')))),
    ('R639-3-05', 'subprocess.run(**{args}) undeclared', py('import subprocess\nsubprocess.run(**{"args": ["brand_new_command", "install"]})\n')),
    ('R639-3-07', 'working-directory: subdir + bash bootstrap.sh', p(lambda f: (f.file('subdir/bootstrap.sh', HIDDEN), f.run('bash bootstrap.sh', **{'working-directory': 'subdir'})))),
    ('R639-3-08', '(cd subdir); bash bootstrap.sh', p(lambda f: (f.file('bootstrap.sh', HIDDEN), f.file('subdir/bootstrap.sh', 'echo ok\n'), f.run('(cd subdir); bash bootstrap.sh')))),
    ('NEW-01', 'new command name', r('brand_new_command')),
    ('NEW-02', 'coproc', r('coproc bash bootstrap.sh')),
    ('NEW-03', '[[ ]] test clause', r('[[ -n x ]] && echo ok')),
    ('NEW-04', 'time keyword', r('time echo ok')),
    ('NEW-05', 'arithmetic command', r('(( x = 1 ))')),
    ('NEW-06', 'select loop', r('select x in a; do echo ok; done')),
    ('NEW-07', 'Make vpath directive', p(lambda f: (f.file('Makefile', 'vpath %.c src\nall:\n\techo ok\n'), f.run('make')))),
    ('NEW-08', 'Make ifdef', p(lambda f: (f.file('Makefile', 'ifdef X\nendif\nall:\n\techo ok\n'), f.run('make')))),
    ('NEW-09', 'Make $(info)', p(lambda f: (f.file('Makefile', 'all:\n\techo $(info x)\n'), f.run('make')))),
    ('NEW-10', 'Make .ONESHELL', p(lambda f: (f.file('Makefile', '.ONESHELL:\nall:\n\techo ok\n'), f.run('make')))),
    ('NEW-11', 'Make != shell assignment', p(lambda f: (f.file('Makefile', 'X != brand_new_command\nall:\n\techo ok\n'), f.run('make')))),
    ('NEW-12', 'eval', r('eval "echo ok"')),
    ('NEW-13', 'alias', r("alias ls='bash hidden.sh'")),
    ('VAR-01', 'computed .DEFAULT_GOAL', p(lambda f: (f.file('Makefile', 'a:\n\techo ok\n.DEFAULT_GOAL := $(G)\n'), f.run('make')))),
    ('VAR-02', 'target matching two pattern rules', p(lambda f: (f.file('Makefile', 'all: obj_t\nobj_%:\n\techo $*\n%_t:\n\techo $*\n'), f.run('make')))),
    ('VAR-03', 'subshell cd to computed path', r('(cd "$UNKNOWN" && echo ok)')),
    ('VAR-04', 'changed byte of a pinned inline program', r("python3 -c 'import sys; print(sys.version) '")),
    ('VAR-05', 'function called from another file', p(lambda f: (f.file('function.sh', 'f() { echo ok; }\n'), f.run('bash function.sh; f')))),
    ('VAR-06', 'computed $(shell)', p(lambda f: (f.file('Makefile', 'X := $(shell $$TOOL)\nall:\n\techo ok\n'), f.run('make')))),
    ('VAR-07', 'computed function name', r('name=f; f() { echo ok; }; "${name}x"')),
]:
    probe(pid, desc, 'REFUSED', setup)


def recorded_images(f):
    common(f)
    f.doc({'jobs': {'gate': {'container': 'ubuntu@sha256:' + 'a' * 64,
                             'services': {'db': {'image': 'postgres@sha256:' + 'b' * 64}},
                             'steps': [{'run': 'echo ok'}]}}})


probe('R638-3-I1/I2', 'container and service digests recorded', 'ACCEPTED', recorded_images)


def declared_kwargs(f):
    common(f)
    f.file('bootstrap.py', 'import subprocess\nsubprocess.run(**{"args": ["brand_new_command", "install"]})\n')
    f.declare('bootstrap.py')
    f.run('python3 bootstrap.py')


probe('R639-3-06', 'declared script with literal unpacked unclassified command still refused', 'REFUSED', declared_kwargs)


def declared_changed(f):
    common(f)
    f.file('bootstrap.py', 'import subprocess\nsubprocess.run(["echo", "ok"])\n')
    f.declare('bootstrap.py')
    f.file('bootstrap.py', 'import subprocess\nsubprocess.run(["echo", "changed"])\n')
    f.run('python3 bootstrap.py')


probe('DECL-01', 'changed declared script refused', 'REFUSED', declared_changed)
probe('DECL-02', 'undeclared network import refused', 'REFUSED', py('import urllib.request\n'))


def declared_ok(f):
    common(f)
    f.file('bootstrap.py', 'import subprocess\nsubprocess.run(["echo", "ok"])\n')
    f.declare('bootstrap.py')
    f.run('python3 bootstrap.py')


probe('DECL-03', 'declared script with classified command accepted', 'ACCEPTED', declared_ok)

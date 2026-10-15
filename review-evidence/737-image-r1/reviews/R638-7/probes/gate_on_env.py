"""Derive a planted one-step workflow with the census gate ON (as ci_differential_selftest does); print rc and output.

usage: CI_IMAGE_SHFMT=... python3 -I gate_on_env.py CLONE
"""
import contextlib, io, json, shutil, sys, tempfile
from pathlib import Path
clone = Path(sys.argv[1]); sys.path.insert(0, str(clone / 'scripts'))
import yaml, ci_command_table, ci_tool_inventory as inventory
assert ci_command_table.GATE
CASES = [
    ('certain cd after an accepted Python rmtree', {}, 'python3 clean.py\nif cd sub; then :; else cd other; fi\nbash run.sh\n',
     {'sub/run.sh': 'echo sub\n', 'other/run.sh': 'zz_probe other\n', 'clean.py': "import shutil\nshutil.rmtree('sub')\n"}),
    ('followed script rewritten by an accepted Python program', {}, 'python3 gen.py\nbash run.sh\n',
     {'run.sh': 'true\n', 'gen.py': "open('run.sh', 'w').write('zz_probe regenerated\\n')\n"}),
    ('exported function in workflow env, builtin call', {'BASH_FUNC_echo%%': '() { zz_probe exported-function; }'}, 'echo ok\n', {}),
    ('control: CDPATH in workflow env', {'CDPATH': 'other'}, 'echo ok\n', {}),
    ('control: no env', {}, 'echo ok\n', {}),
    ('control: hidden command reached directly', {}, 'bash other/run.sh\n', {'other/run.sh': 'zz_probe other\n'}),
]
for label, env, run, files in CASES:
    with tempfile.TemporaryDirectory(prefix='r638-gate-') as directory:
        root = Path(directory)
        (root / 'ci/image').mkdir(parents=True); (root / '.github/workflows').mkdir(parents=True)
        for name in ('command-table.json', 'sources.lock.json', 'syntax-census.json', 'make-builtins.json', 'differential-receipt.json'):
            shutil.copyfile(clone / 'ci/image' / name, root / 'ci/image' / name)
        for name, text in files.items():
            (root / name).parent.mkdir(parents=True, exist_ok=True); (root / name).write_text(text)
        step = {'run': run, **({'env': env} if env else {})}
        (root / '.github/workflows/fixture.yml').write_text(yaml.safe_dump({'jobs': {'gate': {'steps': [step]}}}))
        saved, output = sys.argv, io.StringIO()
        try:
            sys.argv = ['ci_tool_inventory.py', '--root', str(root), '--write']
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
                rc = inventory.main()
        finally:
            sys.argv = saved
        print(json.dumps({'case': label, 'rc': rc, 'output': output.getvalue().strip()[-300:]}))

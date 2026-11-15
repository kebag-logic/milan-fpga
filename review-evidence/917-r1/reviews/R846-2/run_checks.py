"""Focused foreground checks. Usage: python3 -B run_checks.py CHECKOUT PACKET TASK.
TASK is budget, generator or model. Scratch outputs stay below PACKET/scratch.
"""
import os
import subprocess
import sys
from pathlib import Path

root, packet = (Path(a).resolve() for a in sys.argv[1:3])
task = sys.argv[3]
scratch = packet / 'scratch' / task
scratch.mkdir(parents=True, exist_ok=True)
env = dict(os.environ, TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1')
fw = root / 'sw/firmware/ctrl'
if task == 'budget':
    commands = [[sys.executable, '-B', 'tb/verilator/ctrl_service_budget/selftest.py']]
elif task == 'generator':
    commands = [[sys.executable, '-B', 'sw/mailbox/gen_mailbox.py', option]
                for option in ('--check', '--crosscheck', '--selftest')]
elif task == 'model':
    includes = [fw / p for p in ('mbx', 'host', 'port', 'loop', 'adp', 'maap', 'acmp', 'app', 'test')]
    includes += [root / 'third_party/tsn-c-stack/include', root / 'sw/firmware/ctrl_nvm', root / 'tb/verilator/mbx']
    inc = ['-I' + str(p) for p in includes]
    commands = [
        ['cc', '-std=c11', '-O2', '-Wall', '-Wextra', '-Werror', '-pedantic', *inc,
         '-c', str(fw / 'host/mbx_model.c'), '-o', str(scratch / 'model.o')],
        ['c++', '-std=c++17', '-O2', '-Wall', '-Wextra', '-Werror', *inc,
         str(root / 'tb/verilator/mbx/model_main.cpp'), str(scratch / 'model.o'), '-o', str(scratch / 'model')],
        [str(scratch / 'model')],
    ]
else:
    raise SystemExit('unknown task')
with (packet / (task + '.log')).open('w') as log:
    for command in commands:
        shown = ' '.join(command).replace(str(root), '<checkout>').replace(str(packet), '<packet>')
        log.write('COMMAND ' + shown + '\n')
        log.flush()
        result = subprocess.run(command, cwd=root, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        log.write(result.stdout.decode(errors='replace').replace(str(root), '<checkout>').replace(str(packet), '<packet>'))
        log.write(f'RC {result.returncode}\n')
        log.flush()
        if result.returncode:
            (packet / (task + '.rc')).write_text(str(result.returncode) + '\n')
            raise SystemExit(result.returncode)
(packet / (task + '.rc')).write_text('0\n')
print(task + ': PASS')

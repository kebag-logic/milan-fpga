import json, os, shlex, subprocess, sys, time
from pathlib import Path
out = Path('$MANAGEMENT/2026-09-23/545-a308')
name, *cmd = sys.argv[1:]
log = out / (name + '.log')
start = time.monotonic()
with log.open('w') as stream:
    stream.write('COMMAND: ' + shlex.join(cmd) + '\nCWD: ' + os.getcwd() + '\n')
    stream.flush()
    try:
        result = subprocess.run(cmd, stdout=stream, stderr=subprocess.STDOUT, timeout=21600, check=False)
        rc = result.returncode
    except subprocess.TimeoutExpired:
        rc = 124
    elapsed = time.monotonic() - start
    stream.write(f'\nEXIT: {rc}; WALL_SECONDS: {elapsed:.3f}\n')
record = {'name': name, 'command': cmd, 'cwd': os.getcwd(), 'exit': rc, 'wall_seconds': round(elapsed, 3), 'log': log.name}
with (out / 'gates.jsonl').open('a') as stream:
    stream.write(json.dumps(record) + '\n')
with (out / 'HANDOFF.md').open('a') as stream:
    stream.write(f'\nCompleted `{name}`: exit {rc}, {elapsed:.3f} s; `{log.name}`.\n')
print(json.dumps({k: record[k] for k in ('name', 'exit', 'wall_seconds', 'log')}), flush=True)
print(''.join(line for line in log.read_text(errors='replace').splitlines(keepends=True)[-12:] if len(line)<350), flush=True)
sys.exit(rc)

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

repo, scratch, output, interpreter, parser, docker_config = map(Path, sys.argv[1:])
os.environ.update(TMPDIR=str(scratch), PYTHONDONTWRITEBYTECODE='1', CI_IMAGE_SHFMT=str(parser))
docker = 'sudo -n -u <account> -g docker docker --config ' + str(docker_config)
commands = []
for label in ('a', 'b'):
    work = scratch / ('cold-' + label)
    commands.append((label + '-build', [str(interpreter), 'ci/image/build.py', '--work', str(work),
                     '--docker-command', docker, '--no-cache', '--defer-lock']))
    if label == 'a':
        commands.append(('a-record', [str(interpreter), 'ci/image/build.py', '--work', str(work), '--record-lock']))
    else:
        commands.append(('b-verify', [str(interpreter), 'ci/image/build.py', '--work', str(work),
                         '--check-lock', '--verify-archive', str(work / 'image.tar')]))
results = []
for name, command in commands:
    log = scratch / (name + '.log')
    started = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=repo, stdout=stream, stderr=subprocess.STDOUT, check=False)
    with log.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    row = {'step': name, 'rc': result.returncode, 'wall_seconds': round(time.monotonic() - started, 3),
           'log_size': log.stat().st_size, 'log_sha256': digest}
    results.append(row)
    (output / 'round3-build-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(row), flush=True)
    if result.returncode:
        (scratch / 'builds.done').write_text(str(result.returncode) + '\n')
        raise SystemExit(result.returncode)
(scratch / 'builds.done').write_text('0\n')

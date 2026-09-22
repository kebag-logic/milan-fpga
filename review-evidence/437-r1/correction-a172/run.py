"""Record exact argv, working directory, source identity, exits and output."""
import datetime
import hashlib
import json
import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
LANE = Path('$CANDIDATE')


def run(name, args, cwd=LANE):
    argv = ['rtk', 'proxy', *args]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    result = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    (OUT / 'logs').mkdir(exist_ok=True)
    (OUT / 'logs' / (name + '.log')).write_text(result.stdout + result.stderr)
    row = {'name': name, 'argv': argv, 'cwd': str(cwd), 'utc': start,
           'exit': result.returncode,
           'head': subprocess.check_output(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], cwd=LANE, text=True).strip(),
           'source_sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                             for p in (LANE / 'scripts').glob('gen_toc*.py')}}
    (OUT / 'logs' / (name + '.json')).write_text(json.dumps(row, indent=2) + '\n')
    print(name, 'exit', result.returncode, result.stdout[-700:].strip(), flush=True)
    return result.returncode


if __name__ == '__main__':
    sys.exit(run(sys.argv[1], sys.argv[2:]))

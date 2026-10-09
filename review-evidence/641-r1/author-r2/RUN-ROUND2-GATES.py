import json, os, subprocess, sys, time
from pathlib import Path
commands = json.loads(Path(sys.argv[1]).read_text())
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
rows = []
for name, argv, options in commands:
    argv = [os.environ['MD_PYTHON'] if v == '$MD_PYTHON' else
            str(Path(os.environ['PACKET']) / v[8:]) if v.startswith('$PACKET/') else v
            for v in argv]
    env = dict(os.environ, **options.get('env', {}))
    start = time.monotonic()
    with (out / (name + '.log')).open('w') as log:
        run = subprocess.run(argv, env=env, stdout=log, stderr=subprocess.STDOUT, check=False)
    row = dict(name=name, rc=run.returncode, seconds=round(time.monotonic()-start, 2))
    rows.append(row)
    (out / (name + '.rc')).write_text(str(run.returncode) + '\n')
    (out / 'results.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(name, run.returncode, flush=True)
rc = int(any(r['rc'] for r in rows))
(out / 'rc').write_text(str(rc) + '\n')
raise SystemExit(rc)

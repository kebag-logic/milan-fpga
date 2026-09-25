"""Run a gate in the foreground, saving its unfiltered output and direct status."""
import json, os, pathlib, subprocess, sys, time
name, cwd, *cmd = sys.argv[1:]
out = pathlib.Path(__file__).resolve().parent
env = dict(os.environ)
start = time.time()
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=cwd, text=True).strip()
with (out / (name + '.log')).open('w') as stream:
    result = subprocess.run(cmd, cwd=cwd, env=env, stdout=stream,
                            stderr=subprocess.STDOUT, timeout=14400)
record = dict(name=name, command=cmd, head=head, rc=result.returncode,
              seconds=round(time.time()-start, 2), log=name+'.log')
with (out / 'gate-results.jsonl').open('a') as stream:
    stream.write(json.dumps(record) + '\n')
print(json.dumps(record), flush=True)
print('\n'.join((out / (name + '.log')).read_text(errors='replace').splitlines()[-10:]))
sys.exit(result.returncode)

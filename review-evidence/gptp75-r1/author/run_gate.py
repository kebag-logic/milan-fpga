from pathlib import Path
import datetime, subprocess, sys, time
out=Path(__file__).resolve().parent
name, cwd, *command=sys.argv[1:]
start=time.monotonic()
with (out/(name+'.log')).open('w') as log:
    log.write('COMMAND '+repr(command)+'\nCWD '+cwd+'\n')
    log.flush()
    result=subprocess.run(command,cwd=cwd,stdout=log,stderr=subprocess.STDOUT,timeout=14400)
elapsed=time.monotonic()-start
with (out/'gates.tsv').open('a') as ledger:
    ledger.write(f'{name}\t{result.returncode}\t{elapsed:.1f}\t{datetime.datetime.now(datetime.timezone.utc).isoformat()}\n')
print(f'{name}: rc={result.returncode}, seconds={elapsed:.1f}',flush=True)
print(''.join((out/(name+'.log')).read_text().splitlines(keepends=True)[-18:]))
sys.exit(result.returncode)

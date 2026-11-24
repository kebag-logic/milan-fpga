#!/usr/bin/env python3
"""Foreground command receipt with exact exit status and bounded console output."""
import datetime
import json
import os
from pathlib import Path
import subprocess
import sys
import time

out = Path(sys.argv[1])
out.parent.mkdir(parents=True, exist_ok=True)
cmd = sys.argv[2:]
start = time.time()
metadata = {'argv': cmd, 'cwd': os.getcwd(), 'start': datetime.datetime.now(datetime.timezone.utc).isoformat()}
source = os.environ.get('A837_SOURCE', '/data-2/milan/lanes/opt-gptp-sw')
metadata['source'] = source
metadata['head'] = subprocess.check_output(['git', '-C', source, 'rev-parse', 'HEAD'], text=True).strip()
with out.open('w') as log:
    log.write(json.dumps(metadata) + '\n')
    log.flush()
    result = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, timeout=21600, check=False)
metadata.update(rc=result.returncode, seconds=time.time() - start)
out.with_suffix(out.suffix + '.json').write_text(json.dumps(metadata, indent=2) + '\n')
print(json.dumps(metadata), flush=True)
print('\n'.join(out.read_text(errors='replace').splitlines()[-12:]), flush=True)
sys.exit(result.returncode)

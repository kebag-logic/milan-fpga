#!/bin/bash
# Rebuild census 4's eight images at the head, then compare each native executable with census 4's.
S=$VALIDATION_STORAGE/arty4x4-a863; cd $LANES/arty-4x4
for v in none answering-ports answering-every-port valid-destinations declaring-outputs answering-later talker-notices shutdown-entry; do
  $S/tools/run-env.sh python3 -B $S/tools/build-variant.py $S/c4q/$v $v > $S/c4q/$v-build.log 2>&1 || echo "BUILD FAILED $v"
done
python3 - <<'P'
import json
from pathlib import Path
S=Path('$VALIDATION_STORAGE/arty4x4-a863')
same=[]
for d in sorted((S/'c4').iterdir()):
    if (d/'build.json').exists():
        a=json.loads((d/'build.json').read_text()); b=json.loads((S/'c4q'/d.name/'build.json').read_text())
        same.append((d.name,a['executable_sha256']==b['executable_sha256'],a['executable_sha256'][:12],b['executable_sha256'][:12]))
print(json.dumps(same)); print('ALL IDENTICAL' if all(x[1] for x in same) else 'DIFFER')
P

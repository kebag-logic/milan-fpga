import json
import sys
from run_gate import BANK, OUT, run
commands = json.loads(BANK.read_text())['commands']
for i in range(int(sys.argv[1]), int(sys.argv[2])):
    argv = commands[i]
    if i == 47:
        argv = [str(OUT / 'full-builder-sdk.py') if x == '$VALIDATION_STORAGE/400-403-manager-r2/full-builder-sdk.py' else x for x in argv]
    if run(f'bank-{i:02}', argv):
        raise SystemExit(1)

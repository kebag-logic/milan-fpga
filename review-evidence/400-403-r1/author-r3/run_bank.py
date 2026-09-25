from pathlib import Path
import subprocess, sys
out = Path(__file__).resolve().parent
codes = []
for number in range(1, 49):
    if number == 31:
        continue
    code = subprocess.run([sys.executable, str(out/'run_gate.py'), f'bank-{number:02d}'], timeout=43200).returncode
    codes.append((number, code))
print('BANK RESULTS', codes, flush=True)
sys.exit(int(any(code for _, code in codes)))

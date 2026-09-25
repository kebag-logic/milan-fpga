from pathlib import Path
import subprocess
import sys

out = Path(__file__).resolve().parent
for name,jobs,temperature in [('sequential-cold','1','cold'),
                              ('sequential-warm','1','warm'),
                              ('pooled-cold','2','cold'),
                              ('pooled-warm','2','warm')]:
    result = subprocess.run(['python3',str(out/'run-gate.py'),name,
                             'python3',str(out/'benchmark.py'),name,jobs,temperature],check=False)
    if result.returncode:
        sys.exit(result.returncode)

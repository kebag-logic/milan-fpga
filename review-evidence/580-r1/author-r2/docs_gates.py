"""Run the complete assigned documentation gate set in the foreground."""
import json
from pathlib import Path
import subprocess
import sys
OUT = Path(__file__).resolve().parent
gates = json.loads((OUT/'docs-gates.json').read_text())
start = next(i for i, (name, _) in enumerate(gates) if name == sys.argv[1]) if len(sys.argv) > 1 else 0
for name, command in gates[start:]:
    subprocess.run(['rtk', 'proxy', sys.executable, str(OUT/'gate.py'), name,
                    'rtk', 'proxy', *command], check=True, timeout=14400)

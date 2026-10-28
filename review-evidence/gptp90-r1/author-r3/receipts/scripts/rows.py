"""Print label, rc, seconds, head and head_unchanged for every gate row in the given directories."""
import json, sys
from pathlib import Path
for d in sys.argv[1:]:
    for f in sorted(Path(d).glob("*.json")):
        if f.name.startswith("DONE"):
            continue
        r = json.loads(f.read_text())
        print(f"{d.rstrip('/').split('/')[-1]:10} {r['label']:20} rc={r['exit_code']} {r['seconds']:>8} {r['head'][:8]} {r['head_unchanged']}")

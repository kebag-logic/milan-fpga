"""Re-hash every image a prepared measurement directory recorded (scratch)."""
import hashlib, json, sys
from pathlib import Path
for arg in sys.argv[1:]:
    records = json.loads(Path(arg).read_text())
    for record in records:
        data = Path(record['path']).read_bytes()
        assert len(data) == record['bytes'], record['path'] + ' size changed'
        assert hashlib.sha256(data).hexdigest() == record['sha256'], record['path'] + ' hash changed'
    print(Path(arg).parent.name + ': ' + str(len(records)) + ' image receipts match')

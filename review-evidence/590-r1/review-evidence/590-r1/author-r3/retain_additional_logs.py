"""Keep the native missing-publication raw log after the bank finishes."""
from pathlib import Path
import gzip
import hashlib
import json

out = Path(__file__).parent
manifest = out / "native-artifacts.json"
items = json.loads(manifest.read_text())
source = Path("$VALIDATION_STORAGE/590-a411/service-no-publish-all/service-all-1-0-0.log")
raw = source.read_bytes()
body = gzip.compress(raw, mtime=0) if len(raw) > 200000 else raw
name = "service-no-publish-all-raw.log" + (".gz" if len(raw) > 200000 else "")
assert not any(item["name"] == name for item in items)
stored = []
for index, start in enumerate(range(0, len(body), 190000)):
    part = body[start:start+190000]
    target = out / "native-evidence" / (name + (f".part{index:02d}" if len(body) > 190000 else ""))
    target.write_bytes(part)
    stored.append(dict(path=str(target.relative_to(out)), size=len(part), sha256=hashlib.sha256(part).hexdigest()))
items.append(dict(name=name, raw_size=len(raw), raw_sha256=hashlib.sha256(raw).hexdigest(), stored=stored))
manifest.write_text(json.dumps(items, indent=2) + "\n")
print("Missing-publication raw log retained")

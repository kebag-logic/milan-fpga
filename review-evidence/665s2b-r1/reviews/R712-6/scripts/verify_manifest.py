"""Verify MANIFEST.json's published_sha256 for every entry under a prefix, against the files under the manifest's
directory, and list files under the prefix the manifest omits. Usage: python3 -I verify_manifest.py <MANIFEST.json> <prefix>"""
import hashlib, json, sys
from pathlib import Path
man = Path(sys.argv[1]); base = man.parent; pre = sys.argv[2]
ent = [e for e in json.loads(man.read_text()) if e['file'].startswith(pre)]
bad = [e['file'] for e in ent if not (base / e['file']).is_file()
       or hashlib.sha256((base / e['file']).read_bytes()).hexdigest() != e['published_sha256']]
redacted = [e['file'] for e in ent if e['original_sha256'] != e['published_sha256'] or e['path_redacted']]
files = {str(f.relative_to(base)) for f in (base / pre).rglob('*') if f.is_file()}
print(f'entries {len(ent)} bad {len(bad)} {bad[:5]}; redacted/rewritten {len(redacted)} {redacted[:8]}; '
      f'files not in manifest {sorted(files - {e["file"] for e in ent})[:8]}')

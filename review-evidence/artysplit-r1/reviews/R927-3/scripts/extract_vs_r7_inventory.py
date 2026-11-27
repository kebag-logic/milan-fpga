"""Check a compact census extract's FILES.json against the round-7 packet's published FILES inventory:
every source path and SHA256 it names is listed there, and each 'identical' file hashes to its single source.
usage: python3 -I extract_vs_r7_inventory.py EXTRACT_DIR R7_RECEIPTS_DIR"""
import hashlib, json, sys
from pathlib import Path
ext, r7 = Path(sys.argv[1]), Path(sys.argv[2])
rec = json.loads((r7 / 'FILES.manifest.json').read_text())
text = b''.join((r7 / p['file']).read_bytes() for p in rec['parts'])
assert hashlib.sha256(text).hexdigest() == rec['sha256']
inv = {p: h for p, _, h in (l.split('\t') for l in text.decode().splitlines()[1:] if l)}
files = json.loads((ext / 'FILES.json').read_text())
missing = sum(1 for e in files for s in e['sources'] if inv.get(s['path']) != s['sha256'])
ident = [e for e in files if e['relation'] == 'identical']
bad_ident = sum(1 for e in ident if len(e['sources']) != 1 or e['sha256'] != e['sources'][0]['sha256'])
multi = sum(1 for e in ident if len(e['sources']) != 1)
print(f'RESULT entries={len(files)} sources_not_in_r7_inventory={missing} identical_entries={len(ident)} '
      f'identical_not_single_source_equal={bad_ident} (multi-part sources {multi}) r7_inventory_files={len(inv)}')

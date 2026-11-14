#!/usr/bin/env python3
"""Check the author's round-8 packet (argv[1] = an extraction of review-evidence/894-r1 at the evidence commit):
every author-r8 file against MANIFEST.json's published_sha256, and against INDEX.md's rows."""
import hashlib, json, os, re, sys
os.chdir(sys.argv[1])
m = [e for e in json.load(open('MANIFEST.json')) if e['file'].startswith('author-r8/')]
bad = [e['file'] for e in m if hashlib.sha256(open(e['file'], 'rb').read()).hexdigest() != e['published_sha256']]
print(f"MANIFEST.json author-r8 entries {len(m)}; published hash mismatches {len(bad)} {bad}; "
      f"path-redacted {[e['file'] for e in m if e['path_redacted']]}")
rows = re.findall(r'\| `([^`]+)` \| ([\d,]+) \| `([0-9a-f]{64})` \|', open('author-r8/INDEX.md').read())
missing = [p for p, _, _ in rows if not os.path.exists('author-r8/' + p)]
differ = [p for p, _, h in rows if p not in missing and
          hashlib.sha256(open('author-r8/' + p, 'rb').read()).hexdigest() != h]
present = {os.path.relpath(os.path.join(r, f), 'author-r8') for r, _, fs in os.walk('author-r8') for f in fs}
print(f"INDEX.md rows {len(rows)}; not published {missing}; bytes differ from the index {differ}; "
      f"published but not indexed {sorted(present - {p for p, _, _ in rows})}")

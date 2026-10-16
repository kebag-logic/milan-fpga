#!/usr/bin/env python3
"""Cross-check every SHA-256 and byte count in the added lines of the two B19
sections against the packet's RAW-ARTIFACTS.json, MANIFEST.sha256 and file
bytes. Usage: check_page_hashes.py <repo> <base> <packet-author-dir>"""
import hashlib, json, os, re, subprocess, sys
repo, base, auth = sys.argv[1:4]
raw = json.load(open(os.path.join(auth, 'RAW-ARTIFACTS.json')))
note = raw['note']; files = raw['files']
byhash = {}
for f in files: byhash.setdefault(f['sha256'], []).append(f)
man = {}
for line in open(os.path.join(auth, 'MANIFEST.sha256')):
    if line.strip():
        h, p = line.split(None, 1); man.setdefault(h, []).append(p.strip())
print('RAW-ARTIFACTS note:', note)
print('raw files', len(files), 'bytes', sum(f['bytes'] for f in files),
      'over 200000:', sum(1 for f in files if f['bytes'] > 200000))
diff = subprocess.run(['git', '-C', repo, 'diff', '-U0', base, 'HEAD', '--',
                       'docs/findings/117_GPTP_SILICON_EVIDENCE.md',
                       'docs/findings/387_SOFTWARE_GM_STEP.md'],
                      capture_output=True, text=True, check=True).stdout
known_tools = {}
for d, _, fs in os.walk(os.path.join(auth, 'tools')):
    for f in fs:
        known_tools[hashlib.sha256(open(os.path.join(d, f), 'rb').read()).hexdigest()] = f
cur = None; n = ok = 0; unmatched = []
for line in diff.splitlines():
    if line.startswith('+++ '): cur = line[6:]; continue
    if not line.startswith('+'): continue
    for h in re.findall(r'`([0-9a-f]{64})`', line):
        n += 1
        nums = [int(x.replace(',', '')) for x in re.findall(r'\|\s*([0-9][0-9,]*)\s*(?=\||;)', line)]
        if h in byhash:
            ent = byhash[h]
            sizes = {e['bytes'] for e in ent}
            sz_ok = (not nums) or any(s in nums for s in sizes) or any(str(s) in line.replace(',', '') for s in sizes)
            ok += 1
            print('RAW ', h[:12], [e['path'].replace('/tmp/a624/raw/', '') for e in ent], sorted(sizes), 'size-in-line' if sz_ok else 'SIZE-NOT-IN-LINE', '|', cur.split('/')[-1])
        elif h in man:
            ok += 1; print('PKT ', h[:12], man[h], '|', cur.split('/')[-1])
        elif h in known_tools:
            ok += 1; print('TOOL', h[:12], known_tools[h], '|', cur.split('/')[-1])
        else:
            unmatched.append((cur, h, line[:140]))
print('hashes in added lines', n, 'matched', ok)
for u in unmatched: print('UNMATCHED', u[0].split('/')[-1], u[1], '::', u[2])

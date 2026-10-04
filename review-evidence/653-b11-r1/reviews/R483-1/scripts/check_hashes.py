#!/usr/bin/env python3
"""Compare the page's capture table and per-cycle short hashes with RAW-ARTIFACTS.json,
and the page's lane-file hashes with the packet files and build receipts.
usage: check_hashes.py <page.md> <packet author dir>"""
import json, re, sys, hashlib, os, glob
page, au = sys.argv[1], sys.argv[2]
txt = open(page, encoding='utf-8').read()
raw = {os.path.basename(f['path']): f for f in json.load(open(os.path.join(au, 'RAW-ARTIFACTS.json')))['files']}
fails = 0
caps = re.findall(r'^\| `(b11-a535-[^`]+\.pcap)` \| ([\d,]+) \| `([0-9a-f]{64})` \|$', txt, re.M)
print('page capture rows:', len(caps))
for name, b, h in caps:
    r = raw.get(name)
    ok = r is not None and r['bytes'] == int(b.replace(',', '')) and r['sha256'] == h
    fails += not ok
    print(('OK  ' if ok else 'FAIL'), name, b, h[:12])
short = re.findall(r'^\| (C0 \(control\)|A\d\d|R\d\d) \|.*\| `([0-9a-f]{12})` \|$', txt, re.M)
print('per-cycle rows:', len(short))
full = {re.sub(r'.*-(C0|A\d\d|R\d\d)\.pcap', r'\1', n): h for n, b, h in caps}
for cyc, s in short:
    k = 'C0' if cyc.startswith('C0') else cyc
    ok = full.get(k, '').startswith(s)
    fails += not ok
    print(('OK  ' if ok else 'FAIL'), 'short', cyc, s)
lane = re.findall(r'^\| ([^|]+) \| `([0-9a-f]{64})` \|$', txt, re.M)
files = {os.path.relpath(p, au): hashlib.sha256(open(p, 'rb').read()).hexdigest()
         for p in glob.glob(os.path.join(au, '**', '*'), recursive=True) if os.path.isfile(p)}
blob = '\n'.join(open(p, errors='replace').read() for p in glob.glob(os.path.join(au, '**', '*'), recursive=True)
                 if os.path.isfile(p) and os.path.getsize(p) < 2_000_000)
for label, h in lane:
    where = [k for k, v in files.items() if v == h]
    cited = blob.count(h)
    print(('OK  ' if (where or cited) else 'FAIL'), label.strip(), h[:12], 'file-match:', where, 'mentions-in-packet:', cited)
    fails += not (where or cited)
print('FAILS', fails)
sys.exit(1 if fails else 0)

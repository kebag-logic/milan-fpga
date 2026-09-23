#!/usr/bin/env python3
"""Confirm identity-token hits without printing the tokens: for each token
class, report its length, and for each hit the file, the byte offset, and a
structural locator (JSONL line number and key path for hex hits; pcap record
number, ethertype and payload offset for raw hits).

usage: confirm_hits.py REPO ORIG_ROOT PUB_ROOT
"""
import sys, os, json, struct, hashlib
sys.argv, args = sys.argv[:1] + sys.argv[1:4], sys.argv[1:4]
repo, orig_root, pub_root = args
# reuse the recovery logic by importing the sweep module's token builder
import importlib.util
spec = importlib.util.spec_from_file_location('sweep', os.path.join(os.path.dirname(__file__), 'identity_sweep.py'))
src = open(spec.origin).read().split("\ndef forms(")[0]
ns = {'__name__': 'x'}
sys.argv = ['x', repo, orig_root, pub_root]
exec(compile(src, spec.origin, 'exec'), ns)
tokens = ns['tokens']
for t, c in sorted(tokens.items(), key=lambda x: x[1]):
    print('token', c, 'len', len(t), 'id', ns['ids'][t],
          'printable' if all(32 <= ch < 127 for ch in t) else 'binary')


def pcap_records(data):
    magic = data[:4]
    endian = '<' if magic in (b'\xd4\xc3\xb2\xa1', b'\x4d\x3c\xb2\xa1') else '>'
    off, n = 24, 0
    while off + 16 <= len(data):
        ts, tu, incl, orig = struct.unpack(endian + 'IIII', data[off:off + 16])
        yield n, off + 16, data[off + 16:off + 16 + incl]
        off += 16 + incl
        n += 1


def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + '/' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + '[%d]' % i)
    else:
        yield path, o


for dp, dn, fn in os.walk(pub_root):
    for f in fn:
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, pub_root)
        data = open(p, 'rb').read()
        for t, c in tokens.items():
            if rel.endswith('.pcap') and t in data:
                for n, base, rec in pcap_records(data):
                    i = rec.find(t)
                    if i >= 0:
                        et = rec[12:14].hex()
                        if et == '8100':
                            et = '8100/' + rec[16:18].hex()
                        print('RAW', c, rel, 'record', n, 'ethertype', et, 'frame_offset', i, 'frame_len', len(rec))
            if rel.endswith('.jsonl') or rel.endswith('.json'):
                hx = t.hex()
                if hx in data.decode('latin-1').lower():
                    for ln, line in enumerate(data.decode('latin-1').splitlines(), 1):
                        if hx not in line.lower():
                            continue
                        try:
                            obj = json.loads(line)
                        except Exception:
                            print('HEX', c, rel, 'line', ln, 'non-json line')
                            continue
                        for kp, v in walk(obj):
                            if isinstance(v, str) and hx in v.lower():
                                print('HEX', c, rel, 'line', ln, 'key', kp, 'hex_offset', v.lower().find(hx) // 2)

#!/usr/bin/env python3
"""Sweep evidence and PR blobs for bench identity in raw, hex, base64 and UTF-16 encodings.

usage: identity_sweep.py <repo-with-docs_check.py> <tokens.json> <label>=<git-dir>:<rev-range-or-commit>[:<pathspec>] ...
  tokens.json: {"class label": ["token", ...]} (kept private; this script prints class labels only)
Each target set is every blob reachable (all versions) from the named commits under the pathspec,
plus the commit messages and identities. Also applies the repository's own SCRUB_RULES
(scripts/docs_check.py) to the raw text and to hex- and base64-decoded runs.
Prints per-hit: set, class, encoding, path, offset. Never prints matched text.
"""
import base64, binascii, importlib.util, json, re, subprocess, sys, collections
repo, tokfile = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('dc', repo + '/scripts/docs_check.py')
dc = importlib.util.module_from_spec(spec); spec.loader.exec_module(dc)
rules = [(rx, cls) for rx, cls, _ in dc.SCRUB_RULES]
toks = json.load(open(tokfile))

def b64_cores(t):
    out = set()
    for pad in range(3):
        e = base64.b64encode(b'\0' * pad + t).decode()
        lead = (pad * 8 + 5) // 6 + (1 if pad else 0)
        core = e[lead:]
        core = core.rstrip('=')
        tail = (len(b'\0' * pad + t) % 3)
        if tail: core = core[:-2]
        if len(core) >= 4: out.add(core.encode())
    return out

pats = []  # (class, encoding, compiled bytes regex)
for cls, lst in toks.items():
    for t in lst:
        tb = t.encode('latin-1')
        pats.append((cls, 'raw', re.compile(re.escape(tb), re.I)))
        pats.append((cls, 'utf16le', re.compile(re.escape(t.encode('utf-16-le')), re.I)))
        pats.append((cls, 'utf16be', re.compile(re.escape(t.encode('utf-16-be')), re.I)))
        hx = tb.hex()
        pats.append((cls, 'hex', re.compile(hx.encode(), re.I)))
        for sep in (b':', b' ', b'-', b'\\x'):
            pats.append((cls, 'hex-sep', re.compile(re.escape(sep.join(hx[i:i+2].encode() for i in range(0, len(hx), 2))), re.I)))
        for core in b64_cores(tb):
            pats.append((cls, 'base64', re.compile(re.escape(core))))
        if re.search(r'[^A-Za-z0-9._-]', t):
            q = ''.join(c if c.isalnum() or c in '._-' else '%%%02X' % ord(c) for c in t)
            pats.append((cls, 'percent', re.compile(re.escape(q.encode()), re.I)))

HEXRUN = re.compile(rb'(?:[0-9a-fA-F]{2}[:\s-]?){6,}')
B64RUN = re.compile(rb'[A-Za-z0-9+/]{12,}={0,2}')
def views(data):
    yield 'raw', data
    for m in HEXRUN.finditer(data):
        h = re.sub(rb'[^0-9a-fA-F]', b'', m.group(0))
        if len(h) % 2: h = h[:-1]
        try: yield 'hexdecoded@%d' % m.start(), binascii.unhexlify(h)
        except Exception: pass
    for m in B64RUN.finditer(data):
        s = m.group(0)
        for k in range(4):
            seg = s[k:]; seg = seg[:len(seg) - len(seg) % 4]
            try: yield 'b64decoded@%d' % m.start(), base64.b64decode(seg, validate=False)
            except Exception: pass

def blobs(gd, spec):
    parts = spec.split(':')
    rng, path = parts[0], (parts[1] if len(parts) > 1 else '')
    commits = subprocess.run(['git', '-C', gd, 'rev-list', rng] if '..' in rng else ['git', '-C', gd, 'rev-list', '--no-walk', rng], capture_output=True, text=True).stdout.split()
    seen = {}
    msgs = []
    for c in commits:
        msgs.append((c, subprocess.run(['git', '-C', gd, 'cat-file', 'commit', c], capture_output=True).stdout))
        ls = subprocess.run(['git', '-C', gd, 'ls-tree', '-r', c, '--'] + ([path] if path else []), capture_output=True, text=True).stdout
        for l in ls.splitlines():
            meta, p = l.split('\t', 1); mode, typ, oid = meta.split()
            if typ == 'blob' and oid not in seen: seen[oid] = (p, c)
    return commits, seen, msgs

summary = collections.Counter(); hits = []
for arg in sys.argv[3:]:
    label, rest = arg.split('=', 1)
    gd, spec = rest.split(':', 1)
    commits, seen, msgs = blobs(gd, spec)
    items = [('commit ' + c[:12], data) for c, data in msgs] + [(p + ' @' + c[:12] + ' blob ' + oid[:12], subprocess.run(['git', '-C', gd, 'cat-file', 'blob', oid], capture_output=True).stdout) for oid, (p, c) in seen.items()]
    nbytes = 0
    for name, data in items:
        nbytes += len(data)
        for cls, enc, rx in pats:
            for m in rx.finditer(data):
                hits.append((label, cls, enc, name, m.start())); summary[(label, cls, enc)] += 1
        for vname, v in views(data):
            txt = v.decode('latin-1')
            for rx, cls in rules:
                for m in rx.finditer(txt):
                    hits.append((label, 'repo rule: ' + cls, vname, name, m.start())); summary[(label, 'repo rule: ' + cls, vname.split('@')[0])] += 1
    print(f'set {label}: {len(commits)} commit(s), {len(seen)} distinct blob(s), {nbytes} bytes scanned, {len(pats)} token patterns x encodings, {len(rules)} repo rules x raw/hex/base64 views')
print('hits by (set, class, encoding):')
for k, v in sorted(summary.items()): print('  ', k, v)
print('total hits', len(hits))
for h in hits: print('HIT', *h, sep='\t')

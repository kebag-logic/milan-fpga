"""Independently compare the start and end controller census.

usage: compare_census.py <census-start.jsonl> <census-end.jsonl>
Prints every key whose response differs; stream states report conn_count.
"""
import json, re, sys
HEX = re.compile(r'^[0-9a-fA-F]{12,}$')
def red(v, field=''):
    """Redact device identifiers; classify destination addresses."""
    if isinstance(v, dict):
        return {k: red(x, k) for k, x in v.items()}
    if isinstance(v, str) and HEX.match(v):
        if field == 'dmac':
            return 'all-zero' if int(v, 16) == 0 else ('MAAP-range' if v.lower().startswith('91e0f000') else 'other')
        return f'<{len(v)}-hex redacted>'
    return v
def load(p):
    out = {}
    for line in open(p):
        r = json.loads(line)
        if 'role' in r and 'what' in r:
            out[(r['role'], r['what'])] = r.get('response')
    return out
a, b = load(sys.argv[1]), load(sys.argv[2])
print('keys start', len(a), 'end', len(b), 'same key set', set(a) == set(b))
states = sorted(k for k in a if k[1].startswith('state-'))
print('stream states:', len(states))
for k in states:
    print(f'  {k[0]}:{k[1]} start conn={a[k].get("conn_count")} end conn={b.get(k, {}).get("conn_count")}')
diff = [k for k in sorted(a) if a[k] != b.get(k)]
print('differing keys:', len(diff))
for k in diff:
    x, y = a[k], b.get(k)
    if isinstance(x, dict) and isinstance(y, dict):
        print(' ', k, {f: (red(x.get(f), f), red(y.get(f), f)) for f in sorted(set(x) | set(y)) if x.get(f) != y.get(f)})
    else:
        print(' ', k, 'start', str(red(x))[:120], 'end', str(red(y))[:120])

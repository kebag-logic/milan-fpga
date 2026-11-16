"""Check each module-level dict-of-dicts cell in a merged file against the composition rule:
the side that moved a cell from the merge base wins; the larger where both moved it."""
import ast, sys
def tables(path):
    t = ast.parse(open(path).read()); out = {}
    for n in t.body:
        if isinstance(n, (ast.Assign, ast.AnnAssign)):
            tgt = n.targets[0] if isinstance(n, ast.Assign) else n.target
            if isinstance(tgt, ast.Name) and isinstance(n.value, ast.Dict):
                try: v = ast.literal_eval(n.value)
                except Exception: continue
                if all(isinstance(x, dict) for x in v.values()): out[tgt.id] = v
    return out
B, P1, P2, M = (tables(p) for p in sys.argv[1:5])
bad = 0; n = 0
for name in sorted(set(B) | set(P1) | set(P2) | set(M)):
    for pt in sorted(set().union(*(x.get(name, {}).keys() for x in (B, P1, P2, M)))):
        keys = set().union(*(x.get(name, {}).get(pt, {}).keys() for x in (B, P1, P2, M)))
        for k in sorted(keys):
            g = lambda x: x.get(name, {}).get(pt, {}).get(k)
            b, a1, a2, m = g(B), g(P1), g(P2), g(M); n += 1
            if a1 == b: want = a2
            elif a2 == b: want = a1
            else: want = max(a1, a2) if None not in (a1, a2) else 'BOTH'
            if m != want:
                bad += 1; print('MISMATCH', name, pt, k, 'base', b, 'P1', a1, 'P2', a2, 'M', m)
            elif a1 != b and a2 != b and a1 != a2:
                print('BOTH-MOVED', name, pt, k, b, a1, a2, '->', m)
print('cells', n, 'mismatches', bad)

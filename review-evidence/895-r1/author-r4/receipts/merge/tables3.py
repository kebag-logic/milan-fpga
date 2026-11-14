import ast, sys
def tables(p):
    t = ast.parse(open(p).read()); out = {}
    for n in t.body:
        if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name) and n.targets[0].id in ('STATED_US', 'STATED_US_DONOR'):
            out[n.targets[0].id] = ast.literal_eval(n.value)
    return out
b, o, t = (tables(p) for p in sys.argv[1:4])
for tab in ('STATED_US', 'STATED_US_DONOR'):
    for pt in sorted(set(b[tab]) | set(o[tab]) | set(t[tab])):
        keys = sorted(set(b[tab].get(pt, {})) | set(o[tab].get(pt, {})) | set(t[tab].get(pt, {})))
        for k in keys:
            vb, vo, vt = (x[tab].get(pt, {}).get(k) for x in (b, o, t))
            if not (vb == vo == vt):
                print(f"{tab:16} {pt:9} {k:20} base={vb} ours={vo} theirs={vt}")

import sys, collections
def scan(path):
    mx = collections.Counter(); tot = collections.Counter(); n = collections.Counter()
    with open(path, errors='replace') as f:
        for line in f:
            if line.startswith('SPAN '):
                p = line.split()
                if len(p) >= 6:
                    c = int(p[3]); fn = p[5]
                    mx[fn] = max(mx[fn], c); tot[fn] += c; n[fn] += 1
    return mx, tot, n
a, ta, na = scan(sys.argv[1]); b, tb, nb = scan(sys.argv[2])
rows = sorted(set(a) | set(b), key=lambda k: -(tb[k] - ta[k]))
print(f"{'function':40s} {'max r1':>8s} {'max r2':>8s} {'mean r1':>9s} {'mean r2':>9s} {'n r1':>7s} {'n r2':>7s}")
for k in rows[:25]:
    print(f"{k:40s} {a[k]:8d} {b[k]:8d} {ta[k]/max(na[k],1):9.1f} {tb[k]/max(nb[k],1):9.1f} {na[k]:7d} {nb[k]:7d}")
